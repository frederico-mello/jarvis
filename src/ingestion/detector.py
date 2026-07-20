from neo4j import ManagedTransaction
from src.graph.driver import get_driver
from src.graph.provenance import get_source_by_url, mark_source_unavailable
from src.common.logging import get_logger

logger = get_logger(__name__)


class SourceDiff:
    def __init__(self, action: str, url: str, source_id: str | None = None):
        self.action = action
        self.url = url
        self.source_id = source_id


async def detect_changes(discovered_urls: list[str]) -> list[SourceDiff]:
    diffs: list[SourceDiff] = []
    driver = get_driver()

    with driver.session() as session:
        for url in discovered_urls:
            existing = session.execute_read(get_source_by_url, url)
            if existing is None:
                diffs.append(SourceDiff(action="new", url=url))
            else:
                diffs.append(SourceDiff(action="exists", url=url, source_id=existing["id"]))

        known_urls = set(discovered_urls)
        stale = session.execute_read(_find_stale_sources, known_urls)
        for source_id, url in stale:
            diffs.append(SourceDiff(action="removed", url=url, source_id=source_id))

    driver.close()
    return diffs


def _find_stale_sources(tx: ManagedTransaction, active_urls: set[str]) -> list[tuple[str, str]]:
    result = tx.run("""
        MATCH (s:Source)
        WHERE s.type = 'web_page' AND (s.status IS NULL OR s.status = 'active')
        AND NOT s.url IN $active_urls
        RETURN s.id AS id, s.url AS url
    """, active_urls=list(active_urls))
    return [(r["id"], r["url"]) for r in result]


def apply_changes(diffs: list[SourceDiff]) -> None:
    driver = get_driver()
    with driver.session() as session:
        for diff in diffs:
            if diff.action == "removed" and diff.source_id:
                session.execute_write(mark_source_unavailable, diff.source_id)
                logger.info("Source marked unavailable", url=diff.url)
    driver.close()

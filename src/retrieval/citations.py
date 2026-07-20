from datetime import datetime
from src.graph.driver import get_driver
from src.common.logging import get_logger

logger = get_logger(__name__)


class Citation:
    def __init__(self, source_id: str, source_url: str | None, title: str | None,
                 excerpt: str, collected_at: datetime | None, status: str = "active"):
        self.source_id = source_id
        self.source_url = source_url
        self.title = title
        self.excerpt = excerpt
        self.collected_at = collected_at
        self.status = status


def build_citations(chunk_ids: list[str]) -> list[Citation]:
    driver = get_driver()
    citations: list[Citation] = []
    with driver.session() as session:
        for chunk_id in chunk_ids:
            result = session.run("""
                MATCH (c:Chunk {id: $chunk_id})
                OPTIONAL MATCH (c)<-[:HAS_CHUNK]-(s:Source)
                OPTIONAL MATCH (c)<-[:HAS_CHUNK]-(d:Document)
                RETURN c.text AS text, s.id AS source_id, s.url AS source_url,
                       d.title AS doc_title, s.status AS source_status,
                       c.created_at AS collected_at
            """, chunk_id=chunk_id)
            record = result.single()
            if record:
                title = record.get("doc_title") or record.get("source_id")
                citations.append(Citation(
                    source_id=record["source_id"] or chunk_id,
                    source_url=record.get("source_url"),
                    title=title,
                    excerpt=record["text"][:300] if record["text"] else "",
                    collected_at=record.get("collected_at"),
                    status=record.get("source_status", "active"),
                ))
    driver.close()
    return citations


def format_citations(citations: list[Citation]) -> list[dict]:
    return [
        {
            "source_id": c.source_id,
            "url": c.source_url,
            "title": c.title,
            "excerpt": c.excerpt,
            "collected_at": c.collected_at.isoformat() if c.collected_at else None,
            "status": c.status,
        }
        for c in citations
    ]

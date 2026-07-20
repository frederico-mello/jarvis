from src.graph.driver import get_driver
from src.common.logging import get_logger

logger = get_logger(__name__)


def get_source_status(source_id: str) -> dict | None:
    driver = get_driver()
    with driver.session() as session:
        result = session.run("""
            MATCH (s:Source {id: $id})
            RETURN s.id AS id, s.type AS type, s.status AS status,
                   s.url AS url, s.updated_at AS updated_at
        """, id=source_id)
        record = result.single()
    driver.close()
    return dict(record) if record else None


def update_source_status(source_id: str, status: str) -> None:
    driver = get_driver()
    with driver.session() as session:
        session.run("""
            MATCH (s:Source {id: $id})
            SET s.status = $status, s.updated_at = datetime()
        """, id=source_id, status=status)
    driver.close()
    logger.info("Source status updated", source_id=source_id, status=status)


def get_active_sources() -> list[dict]:
    driver = get_driver()
    with driver.session() as session:
        result = session.run("""
            MATCH (s:Source)
            WHERE s.status IS NULL OR s.status = 'active'
            RETURN s.id AS id, s.type AS type, s.url AS url, s.updated_at AS updated_at
            ORDER BY s.updated_at DESC
        """)
        records = [dict(r) for r in result]
    driver.close()
    return records


def get_sources_by_status(status: str) -> list[dict]:
    driver = get_driver()
    with driver.session() as session:
        result = session.run("""
            MATCH (s:Source {status: $status})
            RETURN s.id AS id, s.type AS type, s.url AS url, s.updated_at AS updated_at
            ORDER BY s.updated_at DESC
        """, status=status)
        records = [dict(r) for r in result]
    driver.close()
    return records

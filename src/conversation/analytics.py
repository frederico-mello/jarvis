from src.graph.driver import get_driver
from src.common.logging import get_logger

logger = get_logger(__name__)


def get_coverage_gaps(limit: int = 50) -> list[dict]:
    driver = get_driver()
    with driver.session() as session:
        result = session.run("""
            MATCH (c:Conversation)
            WHERE c.has_sufficient_evidence = false
            RETURN c.question AS question, c.created_at AS created_at,
                   count(c) AS occurrences
            ORDER BY occurrences DESC
            LIMIT $limit
        """, limit=limit)
        records = [dict(r) for r in result]
    driver.close()
    return records


def get_popular_questions(limit: int = 20) -> list[dict]:
    driver = get_driver()
    with driver.session() as session:
        result = session.run("""
            MATCH (c:Conversation)
            RETURN c.question AS question, count(c) AS occurrences,
                   avg(c.response_time_ms) AS avg_response_time_ms
            ORDER BY occurrences DESC
            LIMIT $limit
        """, limit=limit)
        records = [dict(r) for r in result]
    driver.close()
    return records


def get_system_stats() -> dict:
    driver = get_driver()
    with driver.session() as session:
        total = session.run("MATCH (c:Conversation) RETURN count(c) AS total").single()["total"]
        unanswered = session.run(
            "MATCH (c:Conversation) WHERE c.has_sufficient_evidence = false RETURN count(c) AS total"
        ).single()["total"]
        faq_count = session.run("MATCH (f:FAQ) RETURN count(f) AS total").single()["total"]
        chunk_count = session.run("MATCH (c:Chunk) RETURN count(c) AS total").single()["total"]
        source_count = session.run("MATCH (s:Source) RETURN count(s) AS total").single()["total"]
    driver.close()
    return {
        "total_conversations": total,
        "unanswered_questions": unanswered,
        "faq_count": faq_count,
        "chunk_count": chunk_count,
        "source_count": source_count,
    }

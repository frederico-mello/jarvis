from datetime import datetime
from src.graph.driver import get_driver
from src.common.logging import get_logger

logger = get_logger(__name__)


def log_conversation(question: str, answer: str, sources: list[dict],
                     response_time_ms: int, has_sufficient_evidence: bool) -> str:
    driver = get_driver()
    conv_id = f"conv_{datetime.utcnow().timestamp()}"
    with driver.session() as session:
        session.run("""
            CREATE (c:Conversation {
                id: $id,
                question: $question,
                answer: $answer,
                sources: $sources,
                response_time_ms: $response_time_ms,
                has_sufficient_evidence: $has_sufficient_evidence,
                created_at: datetime()
            })
        """, id=conv_id, question=question, answer=answer,
               sources=sources, response_time_ms=response_time_ms,
               has_sufficient_evidence=has_sufficient_evidence)
    driver.close()
    logger.debug("Conversation logged", conv_id=conv_id)
    return conv_id


def get_recent_conversations(limit: int = 100) -> list[dict]:
    driver = get_driver()
    with driver.session() as session:
        result = session.run("""
            MATCH (c:Conversation)
            RETURN c.id AS id, c.question AS question, c.answer AS answer,
                   c.sources AS sources, c.response_time_ms AS response_time_ms,
                   c.has_sufficient_evidence AS has_sufficient_evidence,
                   c.created_at AS created_at
            ORDER BY c.created_at DESC
            LIMIT $limit
        """, limit=limit)
        records = [dict(r) for r in result]
    driver.close()
    return records

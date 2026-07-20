from src.graph.driver import get_driver
from src.common.logging import get_logger

logger = get_logger(__name__)


def find_similar_questions(question: str, threshold: float = 0.7, limit: int = 10) -> list[dict]:
    driver = get_driver()
    with driver.session() as session:
        result = session.run("""
            MATCH (c:Conversation)
            WHERE c.question CONTAINS $keywords
            RETURN c.id AS id, c.question AS question, c.answer AS answer,
                   c.has_sufficient_evidence AS has_sufficient_evidence,
                   c.created_at AS created_at
            ORDER BY c.created_at DESC
            LIMIT $limit
        """, keywords=question[:50], limit=limit)
        records = [dict(r) for r in result]
    driver.close()
    return records


def get_question_groups(min_occurrences: int = 3) -> list[dict]:
    driver = get_driver()
    with driver.session() as session:
        result = session.run("""
            MATCH (c:Conversation)
            WITH c.question AS question, count(c) AS occurrences
            WHERE occurrences >= $min_occurrences
            RETURN question, occurrences
            ORDER BY occurrences DESC
        """, min_occurrences=min_occurrences)
        records = [dict(r) for r in result]
    driver.close()
    return records

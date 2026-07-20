from src.config.settings import settings
from src.graph.driver import get_driver
from src.common.logging import get_logger

logger = get_logger(__name__)


def promote_to_faq(question: str, answer: str, sources: list[dict]) -> str:
    driver = get_driver()
    faq_id = f"faq_{hash(question)}"
    with driver.session() as session:
        session.run("""
            MERGE (f:FAQ {id: $id})
            SET f.question = $question, f.answer = $answer,
                f.sources = $sources, f.promoted_at = datetime(),
                f.updated_at = datetime()
        """, id=faq_id, question=question, answer=answer, sources=sources)
    driver.close()
    logger.info("FAQ promoted", faq_id=faq_id, question=question[:80])
    return faq_id


def check_and_promote_faqs() -> int:
    from src.conversation.clustering import get_question_groups
    groups = get_question_groups(min_occurrences=settings.faq_threshold)
    promoted = 0
    for group in groups:
        question = group["question"]
        driver = get_driver()
        with driver.session() as session:
            existing = session.run(
                "MATCH (f:FAQ {question: $q}) RETURN f.id AS id",
                q=question,
            ).single()
            if existing:
                continue
            result = session.run(
                "MATCH (c:Conversation {question: $q}) RETURN c.answer AS answer, c.sources AS sources LIMIT 1",
                q=question,
            ).single()
            if result:
                promote_to_faq(question, result["answer"], result["sources"])
                promoted += 1
        driver.close()
    logger.info("FAQ check complete", promoted=promoted, total_groups=len(groups))
    return promoted

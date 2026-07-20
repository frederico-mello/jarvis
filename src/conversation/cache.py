from datetime import datetime, timedelta
from src.config.settings import settings
from src.graph.driver import get_driver
from src.common.logging import get_logger

logger = get_logger(__name__)


def get_faq_answer(question: str) -> dict | None:
    driver = get_driver()
    with driver.session() as session:
        result = session.run("""
            MATCH (f:FAQ {question: $question})
            RETURN f.id AS id, f.question AS question, f.answer AS answer,
                   f.sources AS sources, f.promoted_at AS promoted_at,
                   f.updated_at AS updated_at
            LIMIT 1
        """, question=question)
        record = result.single()
    driver.close()

    if not record:
        return None

    faq = dict(record)
    promoted_at = faq.get("promoted_at")
    if promoted_at:
        age = datetime.utcnow() - promoted_at
        if age > timedelta(hours=settings.faq_cache_ttl_hours):
            logger.info("FAQ cache expired", faq_id=faq["id"])
            return None

    return faq


def invalidate_faq_cache(faq_id: str) -> None:
    driver = get_driver()
    with driver.session() as session:
        session.run("""
            MATCH (f:FAQ {id: $id})
            SET f.updated_at = datetime()
        """, id=faq_id)
    driver.close()
    logger.info("FAQ cache invalidated", faq_id=faq_id)

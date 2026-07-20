from src.graph.driver import get_driver
from src.common.logging import get_logger

logger = get_logger(__name__)


def check_neo4j() -> dict:
    try:
        driver = get_driver()
        with driver.session() as session:
            result = session.run("RETURN 1 AS ok")
            record = result.single()
            is_ok = record and record["ok"] == 1
        driver.close()
        return {"status": "ok" if is_ok else "error", "service": "neo4j"}
    except Exception as exc:
        logger.error("Neo4j health check failed", error=str(exc))
        return {"status": "error", "service": "neo4j", "detail": str(exc)}


def check_redis() -> dict:
    try:
        import redis
        from src.config.settings import settings
        client = redis.from_url(settings.redis_url)
        client.ping()
        client.close()
        return {"status": "ok", "service": "redis"}
    except Exception as exc:
        logger.error("Redis health check failed", error=str(exc))
        return {"status": "error", "service": "redis", "detail": str(exc)}


def check_storage() -> dict:
    try:
        from src.ingestion.storage import ensure_storage
        ensure_storage()
        return {"status": "ok", "service": "storage"}
    except Exception as exc:
        logger.error("Storage health check failed", error=str(exc))
        return {"status": "error", "service": "storage", "detail": str(exc)}


async def health_check() -> dict:
    neo4j = check_neo4j()
    redis = check_redis()
    storage = check_storage()
    all_ok = all(s["status"] == "ok" for s in [neo4j, redis, storage])
    return {
        "status": "ok" if all_ok else "degraded",
        "checks": [neo4j, redis, storage],
    }

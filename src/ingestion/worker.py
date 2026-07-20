from celery import Celery
from src.config.settings import settings

worker = Celery(
    "ict_graphrag",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

worker.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Sao_Paulo",
    enable_utc=True,
    task_soft_time_limit=300,
    task_time_limit=600,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    beat_schedule={
        "crawl-public-pages": {
            "task": "src.ingestion.tasks.crawl_public_pages",
            "schedule": settings.crawler_interval_minutes * 60.0,
        },
    },
)

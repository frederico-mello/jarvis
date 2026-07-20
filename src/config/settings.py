from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    app_name: str = "ict-graphrag"
    debug: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = ""

    postgresql_dsn: str | None = None

    redis_url: str = "redis://localhost:6379/0"

    secret_key: str = ""
    access_token_expire_minutes: int = 60

    crawler_interval_minutes: int = 360
    crawler_max_pages: int = 500
    crawler_base_url: str = "https://www.ict.unesp.br"

    upload_max_size_mb: int = 20
    upload_allowed_extensions: list[str] = [".pdf", ".docx", ".odt", ".txt"]

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimensions: int = 384

    llm_api_url: str = ""
    llm_api_key: str = ""
    llm_model: str = ""

    faq_threshold: int = 5
    faq_cache_ttl_hours: int = 24

    rate_limit_per_minute: int = 30

    model_config = {"env_prefix": "ICT_GRAPH_", "env_file": ".env"}


settings = Settings()

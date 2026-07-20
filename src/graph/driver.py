from neo4j import GraphDatabase
from src.config.settings import settings
from src.common.logging import get_logger

logger = get_logger(__name__)


def get_driver() -> GraphDatabase.driver:
    return GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )

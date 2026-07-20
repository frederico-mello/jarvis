from neo4j import ManagedTransaction
from src.graph.driver import get_driver
from src.config.models import SECTORS, SectorConfig
from src.common.logging import get_logger

logger = get_logger(__name__)


def load_sectors(tx: ManagedTransaction, sectors: list[SectorConfig]) -> None:
    for sector in sectors:
        tx.run("""
            MERGE (s:Sector {id: $id})
            SET s.name = $name, s.type = $type, s.updated_at = datetime()
        """, id=sector.id, name=sector.name, type=sector.type.value)
        logger.debug("Sector loaded", id=sector.id, name=sector.name)


def seed_knowledge_graph() -> None:
    driver = get_driver()
    with driver.session() as session:
        logger.info("Loading ICT-SJC sector taxonomy...")
        session.execute_write(load_sectors, SECTORS)
        logger.info(f"Loaded {len(SECTORS)} sectors into the knowledge graph.")
    driver.close()

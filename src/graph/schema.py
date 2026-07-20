from neo4j import GraphDatabase, AsyncGraphDatabase
from src.config.settings import settings
from src.common.logging import get_logger

logger = get_logger(__name__)


def get_driver() -> GraphDatabase.driver:
    return GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )


def get_async_driver() -> AsyncGraphDatabase.driver:
    return AsyncGraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )


CONSTRAINTS = [
    "CREATE CONSTRAINT sector_id IF NOT EXISTS FOR (s:Sector) REQUIRE s.id IS UNIQUE",
    "CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE",
    "CREATE CONSTRAINT position_id IF NOT EXISTS FOR (p:Position) REQUIRE p.id IS UNIQUE",
    "CREATE CONSTRAINT service_id IF NOT EXISTS FOR (s:Service) REQUIRE s.id IS UNIQUE",
    "CREATE CONSTRAINT document_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE",
    "CREATE CONSTRAINT norm_id IF NOT EXISTS FOR (n:Norm) REQUIRE n.id IS UNIQUE",
    "CREATE CONSTRAINT course_id IF NOT EXISTS FOR (c:Course) REQUIRE c.id IS UNIQUE",
    "CREATE CONSTRAINT web_page_id IF NOT EXISTS FOR (w:WebPage) REQUIRE w.id IS UNIQUE",
    "CREATE CONSTRAINT source_id IF NOT EXISTS FOR (s:Source) REQUIRE s.id IS UNIQUE",
    "CREATE CONSTRAINT chunk_id IF NOT EXISTS FOR (c:Chunk) REQUIRE c.id IS UNIQUE",
    "CREATE CONSTRAINT contact_id IF NOT EXISTS FOR (c:Contact) REQUIRE c.id IS UNIQUE",
]

INDEXES = [
    "CREATE VECTOR INDEX chunk_embedding IF NOT EXISTS FOR (c:Chunk) ON (c.embedding) OPTIONS { indexConfig: { `vector.dimensions`: toInteger($dims), `vector.similarity_function`: 'cosine' } }",
    "CREATE FULLTEXT INDEX chunk_text IF NOT EXISTS FOR (c:Chunk) ON EACH [c.text]",
    "CREATE FULLTEXT INDEX document_text IF NOT EXISTS FOR (d:Document) ON EACH [d.title, d.description]",
    "CREATE FULLTEXT INDEX norm_text IF NOT EXISTS FOR (n:Norm) ON EACH [n.title, n.number, n.description]",
    "CREATE INDEX chunk_source_id IF NOT EXISTS FOR (c:Chunk) ON (c.source_id)",
    "CREATE INDEX chunk_document_id IF NOT EXISTS FOR (c:Chunk) ON (c.document_id)",
    "CREATE INDEX document_sector IF NOT EXISTS FOR (d:Document) ON (d.sector_id)",
    "CREATE INDEX source_url IF NOT EXISTS FOR (s:Source) ON (s.url)",
]


def setup_indexes() -> None:
    driver = get_driver()
    with driver.session() as session:
        logger.info("Creating constraints...")
        for cypher in CONSTRAINTS:
            session.run(cypher)
            logger.debug("Constraint created", cypher=cypher[:60])

        logger.info("Creating indexes...")
        for cypher in INDEXES:
            params = {"dims": settings.embedding_dimensions}
            session.run(cypher, params)
            logger.debug("Index created", cypher=cypher[:60])

    driver.close()
    logger.info("Neo4j schema setup complete.")

from neo4j import ManagedTransaction
from src.graph.driver import get_driver
from src.config.settings import settings
from src.common.logging import get_logger

logger = get_logger(__name__)


class ChunkResult:
    def __init__(self, chunk_id: str, text: str, score: float, source_id: str | None = None):
        self.chunk_id = chunk_id
        self.text = text
        self.score = score
        self.source_id = source_id


def vector_search(tx: ManagedTransaction, embedding: list[float], top_k: int = 10) -> list[ChunkResult]:
    result = tx.run("""
        CALL db.index.vector.queryNodes('chunk_embedding', $top_k, $embedding)
        YIELD node AS chunk, score
        RETURN chunk.id AS id, chunk.text AS text, chunk.source_id AS source_id, score
    """, top_k=top_k, embedding=embedding)
    return [ChunkResult(r["id"], r["text"], r["score"], r["source_id"]) for r in result]


def fulltext_search(tx: ManagedTransaction, query: str, top_k: int = 10) -> list[ChunkResult]:
    result = tx.run("""
        CALL db.index.fulltext.queryNodes('chunk_text', $query)
        YIELD node AS chunk, score
        RETURN chunk.id AS id, chunk.text AS text, chunk.source_id AS source_id, score
    """, query=query, top_k=top_k)
    return [ChunkResult(r["id"], r["text"], r["score"], r["source_id"]) for r in result]


def search_by_embedding(embedding: list[float], top_k: int = 10) -> list[ChunkResult]:
    driver = get_driver()
    with driver.session() as session:
        results = session.execute_read(vector_search, embedding, top_k)
    driver.close()
    return results


def search_by_text(query: str, top_k: int = 10) -> list[ChunkResult]:
    driver = get_driver()
    with driver.session() as session:
        results = session.execute_read(fulltext_search, query, top_k)
    driver.close()
    return results

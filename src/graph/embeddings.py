from neo4j import ManagedTransaction
from src.graph.driver import get_driver
from src.common.logging import get_logger

logger = get_logger(__name__)


def upsert_chunk_embedding(tx: ManagedTransaction, chunk_id: str, embedding: list[float]) -> None:
    tx.run("""
        MATCH (c:Chunk {id: $id})
        SET c.embedding = $embedding, c.updated_at = datetime()
    """, id=chunk_id, embedding=embedding)


def get_chunks_without_embedding(tx: ManagedTransaction, limit: int = 100) -> list[dict]:
    result = tx.run("""
        MATCH (c:Chunk)
        WHERE c.embedding IS NULL
        RETURN c.id AS id, c.text AS text
        LIMIT $limit
    """, limit=limit)
    return [dict(r) for r in result]


def get_chunks_by_source(tx: ManagedTransaction, source_id: str) -> list[dict]:
    result = tx.run("""
        MATCH (s:Source {id: $source_id})-[:HAS_CHUNK]->(c:Chunk)
        RETURN c.id AS id, c.text AS text, c.embedding AS embedding
    """, source_id=source_id)
    return [dict(r) for r in result]


def delete_chunks_by_source(tx: ManagedTransaction, source_id: str) -> None:
    tx.run("""
        MATCH (s:Source {id: $source_id})-[:HAS_CHUNK]->(c:Chunk)
        DETACH DELETE c
    """, source_id=source_id)


def count_chunks(tx: ManagedTransaction) -> int:
    result = tx.run("MATCH (c:Chunk) RETURN count(c) AS total")
    return result.single()["total"]


def count_chunks_with_embeddings(tx: ManagedTransaction) -> int:
    result = tx.run("MATCH (c:Chunk) WHERE c.embedding IS NOT NULL RETURN count(c) AS total")
    return result.single()["total"]

from datetime import datetime
from neo4j import ManagedTransaction
from src.graph.driver import get_driver
from src.common.logging import get_logger

logger = get_logger(__name__)


def create_source(tx: ManagedTransaction, source_id: str, source_type: str, url: str | None = None) -> None:
    tx.run("""
        MERGE (s:Source {id: $id})
        SET s.type = $type, s.url = $url, s.created_at = datetime(), s.updated_at = datetime()
    """, id=source_id, type=source_type, url=url)


def create_document_version(tx: ManagedTransaction, doc_id: str, version: int, title: str, content_hash: str,
                            file_path: str | None = None, sector_id: str | None = None) -> None:
    tx.run("""
        MERGE (d:Document {id: $id})
        SET d.title = $title, d.version = $version, d.content_hash = $content_hash,
            d.file_path = $file_path, d.sector_id = $sector_id,
            d.status = 'active', d.updated_at = datetime()
    """, id=doc_id, title=title, version=version, content_hash=content_hash,
           file_path=file_path, sector_id=sector_id)


def create_chunk(tx: ManagedTransaction, chunk_id: str, text: str, source_id: str,
                 document_id: str | None = None, page_number: int | None = None,
                 embedding: list[float] | None = None) -> None:
    tx.run("""
        MERGE (c:Chunk {id: $id})
        SET c.text = $text, c.source_id = $source_id, c.document_id = $document_id,
            c.page_number = $page_number, c.embedding = $embedding,
            c.created_at = datetime(), c.updated_at = datetime()
    """, id=chunk_id, text=text, source_id=source_id, document_id=document_id,
           page_number=page_number, embedding=embedding)
    tx.run("""
        MATCH (c:Chunk {id: $chunk_id})
        MATCH (s:Source {id: $source_id})
        MERGE (s)-[:HAS_CHUNK]->(c)
    """, chunk_id=chunk_id, source_id=source_id)
    if document_id:
        tx.run("""
            MATCH (c:Chunk {id: $chunk_id})
            MATCH (d:Document {id: $document_id})
            MERGE (d)-[:HAS_CHUNK]->(c)
        """, chunk_id=chunk_id, document_id=document_id)


def mark_source_unavailable(tx: ManagedTransaction, source_id: str) -> None:
    tx.run("""
        MATCH (s:Source {id: $id})
        SET s.status = 'unavailable', s.updated_at = datetime()
    """, id=source_id)


def mark_document_replaced(tx: ManagedTransaction, doc_id: str, new_version: int) -> None:
    tx.run("""
        MATCH (d:Document {id: $id})
        SET d.status = 'replaced', d.replaced_by_version = $new_version, d.updated_at = datetime()
    """, id=doc_id, new_version=new_version)


def get_source_by_url(tx: ManagedTransaction, url: str) -> dict | None:
    result = tx.run("""
        MATCH (s:Source {url: $url})
        RETURN s.id AS id, s.type AS type, s.status AS status, s.updated_at AS updated_at
        ORDER BY s.updated_at DESC
        LIMIT 1
    """, url=url)
    record = result.single()
    return dict(record) if record else None


def get_document_by_hash(tx: ManagedTransaction, content_hash: str) -> dict | None:
    result = tx.run("""
        MATCH (d:Document {content_hash: $hash})
        RETURN d.id AS id, d.version AS version, d.status AS status
        ORDER BY d.version DESC
        LIMIT 1
    """, hash=content_hash)
    record = result.single()
    return dict(record) if record else None

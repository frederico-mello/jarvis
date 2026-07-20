from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Request
from pydantic import BaseModel
from pathlib import Path
from src.retrieval.hybrid import hybrid_search
from src.retrieval.generation import generate_answer
from src.retrieval.safety import has_sufficient_evidence, sanitize_context
from src.api.auth import get_current_user, require_admin
from src.api.rate_limit import rate_limiter
from src.api.health import health_check
from src.api.audit import log_audit_event
from src.conversation.logs import log_conversation
from src.ingestion.document_processor import process_document
from src.ingestion.storage import store_original
from src.ingestion.extractor import chunk_text
from src.graph.driver import get_driver
from src.graph.provenance import create_source, create_chunk, create_document_version
from src.config.settings import settings
from src.common.logging import get_logger
from src.common.exceptions import ValidationError

logger = get_logger(__name__)
router = APIRouter()


class QuestionRequest(BaseModel):
    question: str
    top_k: int = 10


class SourceResponse(BaseModel):
    id: str
    source_id: str | None = None
    score: float | None = None


class AnswerResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]
    has_sufficient_evidence: bool


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest, req: Request) -> AnswerResponse:
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    await rate_limiter.check(req)

    logger.info("Question received", question=request.question[:100])

    import time
    start = time.monotonic()

    embedding = [0.0] * settings.embedding_dimensions
    result = hybrid_search(embedding, text_query=request.question, top_k=request.top_k)

    safe_chunks = sanitize_context(result.chunks)
    result.chunks = safe_chunks

    sufficient = has_sufficient_evidence(safe_chunks)
    answer = generate_answer(request.question, result)

    elapsed = int((time.monotonic() - start) * 1000)

    log_conversation(
        question=request.question,
        answer=answer.answer,
        sources=[{"id": s["id"], "source_id": s.get("source_id")} for s in answer.sources],
        response_time_ms=elapsed,
        has_sufficient_evidence=sufficient,
    )

    return AnswerResponse(
        answer=answer.answer,
        sources=[SourceResponse(id=s["id"], source_id=s.get("source_id"), score=s.get("score")) for s in answer.sources],
        has_sufficient_evidence=sufficient,
    )


@router.get("/health")
async def health() -> dict:
    return await health_check()


@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    sector_id: str | None = None,
    current_user: dict = Depends(require_admin),
) -> dict:
    ext = Path(file.filename or "").suffix.lower()
    if ext not in settings.upload_allowed_extensions:
        raise HTTPException(status_code=400, detail=f"File type {ext} not allowed")

    file_data = await file.read()
    if len(file_data) > settings.upload_max_size_mb * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds maximum size")

    temp_path = Path(f"/tmp/{file.filename}")
    temp_path.write_bytes(file_data)

    try:
        processed = process_document(temp_path, file.filename or "document")
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        temp_path.unlink(missing_ok=True)

    doc_id = f"doc_{file.filename}_{sector_id or 'general'}"
    stored_path = store_original(file_data, doc_id, file.filename or "document")

    chunks = chunk_text(processed.text)
    driver = get_driver()
    source_id = f"upload_{doc_id}"

    with driver.session() as session:
        session.execute_write(create_source, source_id, "uploaded_document")
        session.execute_write(create_document_version, doc_id, 1, processed.metadata.get("title", file.filename or ""),
                               "", str(stored_path), sector_id)
        for i, chunk_text_content in enumerate(chunks):
            chunk_id = f"{source_id}_chunk_{i}"
            session.execute_write(create_chunk, chunk_id, chunk_text_content, source_id, doc_id)

    driver.close()

    logger.info("Document uploaded", doc_id=doc_id, chunks=len(chunks), user=current_user.get("sub"))
    return {"document_id": doc_id, "chunks": len(chunks), "source_id": source_id}


@router.delete("/documents/{document_id}")
async def deactivate_document(
    document_id: str,
    current_user: dict = Depends(require_admin),
) -> dict:
    driver = get_driver()
    with driver.session() as session:
        from src.graph.provenance import mark_document_replaced
        session.execute_write(mark_document_replaced, document_id, 0)
    driver.close()
    logger.info("Document deactivated", document_id=document_id, user=current_user.get("sub"))
    return {"status": "deactivated", "document_id": document_id}


@router.get("/documents/{document_id}/history")
async def get_document_history(
    document_id: str,
    current_user: dict = Depends(require_admin),
) -> dict:
    driver = get_driver()
    with driver.session() as session:
        result = session.run("""
            MATCH (d:Document {id: $id})
            RETURN d.id AS id, d.title AS title, d.version AS version,
                   d.status AS status, d.updated_at AS updated_at
        """, id=document_id)
        records = [dict(r) for r in result]
    driver.close()
    return {"document_id": document_id, "versions": records}

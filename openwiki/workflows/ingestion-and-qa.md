---
type: Workflow Guide
title: Ingestion and question answering
description: End-to-end guide to web crawling, document upload, graph persistence, retrieval, safety filtering, generation, and conversation logging.
tags: [workflows, ingestion, retrieval, qa]
---
# Ingestion and question answering

This page connects the [runtime architecture](../architecture/overview.md) to the [knowledge model](../domain/knowledge-model.md). It is the primary change guide for source ingestion and public QA.

## Web crawl workflow

`src/ingestion/worker.py` configures Celery and schedules the crawler using `crawler_interval_minutes`. `crawl_public_pages` in `src/ingestion/tasks.py` discovers same-base URLs, detects changes, marks removed URLs unavailable, and enqueues `process_new_page`. The crawler uses `crawler_base_url` and `crawler_max_pages`; extraction removes layout tags and chunks text before `create_source`/`create_chunk` write Neo4j records.

The current detector only distinguishes a URL that exists from a new URL. Although `fetch_page` computes SHA-256 content, the hash is not compared or persisted through the task flow. Existing changed pages are therefore not reprocessed and version history is incomplete. This conflicts with the source-ingestion OpenSpec requirement for unchanged idempotency and changed-content versions.

## Authorized upload workflow

`POST /api/v1/documents/upload` requires an admin JWT. It checks extension and configured maximum size, writes to `/tmp`, dispatches PDF/DOCX/ODT/TXT processing, removes the temporary file in `finally`, stores the original, chunks extracted text, and creates source/document/chunk records. `DELETE /documents/{id}` marks a document as replaced; `GET /documents/{id}/history` reads its history.

Current caveats: uploads always use version `1`, pass an empty content hash, do not call duplicate-by-hash lookup, and do not connect uploader identity to an audit event. Temporary paths use the client filename directly. Review the authorized-upload OpenSpec before changing lifecycle semantics.

## Public QA workflow

The route in `src/api/routes.py` calls `hybrid_search` from `src/retrieval/hybrid.py`. That merges Neo4j vector and full-text results from `src/retrieval/search.py`, deduplicates chunk IDs, and sorts by raw score. The route then calls `sanitize_context` and `has_sufficient_evidence` from `safety.py`, `generate_answer`, and `log_conversation`.

Generation is intended to answer only from supplied evidence in Portuguese. With no configured LLM client, it falls back to excerpts from the top three chunks. However, the route currently creates an all-zero query vector; ingestion does not generate chunk embeddings; and search does not filter unavailable/replaced sources. Graph traversal helpers exist but the public route does not call `hybrid_search_with_graph`.

## Citations and safety

`sanitize_context` removes chunks matching a narrow prompt-injection pattern set. `citations.py` can build richer source URL/title/excerpt/date/status citations, but `/ask` returns only chunk ID, source ID, and score. Any retrieval change should test safety filtering, evidence thresholds, active-source filtering, and rich citation construction together.

## Conversation and FAQ side effects

Each answer is logged with question, answer, sources, response time, and evidence status. Analytics can identify insufficient-evidence and popular questions. FAQ clustering currently uses substring matching rather than semantic similarity; cache freshness is TTL-based and does not validate source status. These are useful extension points but should not be mistaken for a completed FAQ lifecycle.

## Change checklist

- Preserve source/chunk provenance and stable IDs.
- Decide hash/version/status semantics before changing crawler or upload persistence.
- Generate and backfill embeddings consistently with `embedding_dimensions`.
- Normalize hybrid scores rather than sorting incomparable raw scores.
- Wire graph traversal only with explicit question/entity resolution behavior.
- Keep untrusted source text separate from instructions and return traceable citations.
- Add regression/evaluation tests before altering chunking, safety, or answer contracts.

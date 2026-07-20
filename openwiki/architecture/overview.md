---
type: Architecture Overview
title: Runtime architecture
description: Evidence-backed overview of the FastAPI, Celery, Neo4j, retrieval, ingestion, and conversation layers in ICT GraphRAG.
tags: [architecture, api, graphrag]
---
# Runtime architecture

ICT GraphRAG is organized as a layered GraphRAG service. `src/main.py` is the development entrypoint; `src/api/app.py` creates FastAPI and mounts `src/api/routes.py` at `/api/v1`. The [source map](source-map.md) lists the implementation anchors, while [infrastructure integrations](../integrations/infrastructure.md) explains the external services.

## Major layers

- **API/security:** `src/api/app.py`, `routes.py`, `auth.py`, `rate_limit.py`, `health.py`, and `audit.py`. CORS is configured at application assembly; protected document routes use a bearer JWT with an `admin` role; `/ask` uses a process-local IP limiter.
- **Configuration:** `src/config/settings.py` loads `ICT_GRAPH_` environment variables and `src/config/models.py` defines the institutional sector configuration.
- **Ingestion:** `src/ingestion/` discovers/fetches web pages, extracts/chunks text, processes PDF/DOCX/ODT/TXT uploads, stores originals, and exposes Celery tasks.
- **Graph:** `src/graph/` owns Neo4j drivers, schema/index setup, institutional entities, provenance, extraction models, embeddings, and seed data.
- **Retrieval/generation:** `src/retrieval/` combines vector/full-text search, optional graph traversals, safety filtering, generation, citations, and source status helpers.
- **Conversation:** `src/conversation/` records answers and provides analytics, clustering, FAQ promotion, and caching.

## Public question flow

`POST /api/v1/ask` validates a non-blank question, applies the rate limiter, creates a placeholder 384-dimensional zero embedding, calls `hybrid_search`, sanitizes retrieved chunks, computes an evidence flag, generates a Portuguese answer/fallback, logs the conversation, and returns answer plus basic chunk/source/score references. The intended flow is described in [ingestion and question answering](../workflows/ingestion-and-qa.md).

The important limitation is that `src/graph/embeddings.py` is not invoked to encode the question or stored chunks. Consequently, vector retrieval is not semantically meaningful until an embedding pipeline is connected. `hybrid_search_with_graph` and citation builders also exist but are not used by this endpoint.

## Ingestion-to-graph flow

The crawler task calls discovery, change detection, removal handling, and a task for each new page. Extraction removes common layout elements and chunks text into 1,000-character segments with 200-character overlap. Uploads follow a synchronous API path: validate admin/file, write a temporary file, process it, store the original, chunk text, and create source/document/chunk graph records. The [knowledge model](../domain/knowledge-model.md) is the canonical description of those records.

Neo4j is the shared persistence and retrieval system. Redis backs Celery coordination and is checked by health; PostgreSQL is configured in Compose but no application repository/ORM path was found. MinIO is started by Compose, while current storage code writes local files. See [infrastructure integrations](../integrations/infrastructure.md).

## Design intent versus current wiring

OpenSpec and the archived initial design describe hash-based versioning, graph-aware relational QA, rich citations, source status filtering, and provenance-bearing extraction. The current implementation contains partial helpers/models for these features, but the public pipeline does not yet connect all of them. Treat the gaps listed in [ingestion and question answering](../workflows/ingestion-and-qa.md) as change-sensitive behavior, not assumptions.

## Change guidance

When changing API contracts, inspect route models and `README.md` examples together. When changing graph labels/indexes, update `src/graph/schema.py`, entity/provenance helpers, relevant OpenSpec specs, and regression tests. When changing retrieval, verify embedding dimensions, active-source filtering, evidence thresholds, safety sanitization, and citation construction as one flow.

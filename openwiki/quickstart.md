---
type: Repository Guide
title: ICT GraphRAG quickstart
description: "Entry point for the ICT-SJC UNESP GraphRAG repository: local setup, architecture navigation, operational commands, and implementation caveats."
tags: [quickstart, graphrag, ict-sjc, unesp]
---
# ICT GraphRAG

ICT GraphRAG is a Python 3.11+ FastAPI application for Portuguese question answering over ICT-SJC UNESP institutional content. Its intended design combines web/document ingestion, a Neo4j knowledge graph, hybrid retrieval, source citations, and conversation analytics. The repository is at an initial platform stage: the major abstractions exist, but several production paths are still scaffolding.

## Start here

1. Read the [architecture overview](architecture/overview.md) for the runtime and request/data flows.
2. Use the [source map](architecture/source-map.md) to locate implementation packages, specs, scripts, and tests.
3. Follow [ingestion and question answering](workflows/ingestion-and-qa.md) when changing crawler, uploads, graph persistence, retrieval, or answer generation.
4. Read the [knowledge model](domain/knowledge-model.md) before changing graph labels, relations, chunks, or provenance.
5. Use the [operations runbook](operations/runbook.md) for local infrastructure, configuration, workers, and health checks.
6. Run the checks in the [testing guide](testing/testing-guide.md).
7. Review [infrastructure integrations](integrations/infrastructure.md) for Neo4j, Redis/Celery, PostgreSQL, and MinIO boundaries.

## Local quick start

The repository README provides the canonical sequence:

```bash
cp .env.example .env
# fill non-sensitive configuration in .env
docker compose up -d neo4j postgres redis minio
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -c "from src.graph.schema import setup_indexes; setup_indexes()"
python -c "from src.graph.seed import seed_knowledge_graph; seed_knowledge_graph()"
uvicorn src.api.app:create_app --reload
```

The API is mounted under `/api/v1`; the public health check is `GET /api/v1/health`. Public questions use `POST /api/v1/ask`. Document upload, deletion, and history routes require an admin JWT; this repository does not provide a token-issuance/login route.

## Configuration essentials

Settings use the `ICT_GRAPH_` environment prefix (`src/config/settings.py`). Important values include Neo4j connection fields, Redis URL, crawler base URL/limits, upload extensions and size, embedding model/dimensions, LLM settings, JWT secret/expiry, FAQ thresholds, and the in-memory request limit. Do not commit `.env` or credentials; `.env.example` is the sample configuration surface.

## Current implementation shape

- [Architecture](architecture/overview.md) explains how FastAPI, Celery, Neo4j, retrieval, and conversation modules fit together.
- [Ingestion and QA](workflows/ingestion-and-qa.md) documents crawler/upload processing and the answer path, including incomplete links.
- [Knowledge model](domain/knowledge-model.md) documents institutional entities, source/chunk provenance, and graph relationships.
- [Operations](operations/runbook.md) covers Compose services, worker commands, health semantics, and configuration caveats.
- [Testing](testing/testing-guide.md) describes regression and evaluation coverage.
- [Integrations](integrations/infrastructure.md) records what each external dependency actually does versus what the design anticipates.

## Git and change context

The repository has a single squashed commit (`d6e8791`) containing all source, OpenSpec specs, scripts, tests, and generated `graphify-out` artifacts. There is no prior commit history to diff against; treat current source as authoritative and verify OpenSpec intent against behavior.

## Backlog

- **Embedding pipeline** — `src/api/routes.py`, `src/graph/embeddings.py`, `src/ingestion/tasks.py`; configured embedding model is not invoked, and `/ask` currently supplies a zero vector.
- **Versioned web ingestion** — `src/ingestion/detector.py`, `crawler.py`, `tasks.py`; hashes are computed but changed pages are not reprocessed or versioned.
- **Graph-aware retrieval and citations** — `src/retrieval/hybrid.py`, `traversal.py`, `citations.py`, `src/api/routes.py`; helper paths exist but are not connected to the public response contract.
- **Deployment topology** — `docker-compose.yml`, `Dockerfile`; Compose defines infrastructure and a worker but no API service.
- **Deep operations and privacy policy** — `scripts/`, conversation modules, health code; backup/restore, retention, anonymization, and production alerting need explicit runbooks.

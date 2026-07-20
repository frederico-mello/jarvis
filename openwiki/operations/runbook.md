---
type: Operations Runbook
title: Local operations and runbook
description: Practical startup, worker, crawler, health, configuration, and troubleshooting notes for local ICT GraphRAG operation.
tags: [operations, runbook, docker, celery]
---
# Local operations and runbook

Use this page with the [quickstart](../quickstart.md) and [infrastructure integrations](../integrations/infrastructure.md). It describes repository-evidenced local operation, not a production deployment guarantee.

## Start infrastructure

`docker compose up -d neo4j postgres redis minio` starts the graph database, optional relational database, Redis, and MinIO. Compose also defines a `worker` image using `celery -A src.ingestion.worker worker --loglevel=info`. It does not define an API service; run Uvicorn separately during development.

The README also documents:

```bash
celery -A src.ingestion.worker beat --loglevel=info
python -c "import asyncio; from src.ingestion.tasks import crawl_public_pages; crawl_public_pages.delay()"
curl http://localhost:8000/api/v1/health
```

## Health semantics

`GET /api/v1/health` checks Neo4j (`RETURN 1`), Redis (`ping`), and `ensure_storage()`. It returns JSON status `ok` only when all checks report success, otherwise `degraded`. The endpoint does not explicitly return HTTP 503 and includes exception details in the response body, so monitoring must inspect the payload rather than status code alone.

## Configuration and safety

Settings are loaded with `ICT_GRAPH_` prefix and include database URLs, crawler limits, upload policy, embeddings, LLM configuration, JWT secret/expiry, FAQ settings, and rate limiting. Required secrets have empty defaults (`neo4j_password`, `secret_key`, LLM key); supply them through trusted environment configuration. Never copy secret values into documentation.

The `/ask` limiter is process-local, keyed by client host, and defaults to 30 requests per rolling minute. It is not shared across replicas and does not protect upload routes. Review CORS wildcard/credentials configuration and admin-token lifecycle before exposing the API beyond local development.

## Troubleshooting sequence

1. Check container status and logs for Neo4j/Redis/worker.
2. Confirm `ICT_GRAPH_NEO4J_*` and `ICT_GRAPH_REDIS_URL` resolve from the process location.
3. Run `setup_indexes()` before retrieval and `seed_knowledge_graph()` before relying on taxonomy.
4. Call `/api/v1/health` and inspect each dependency field.
5. Run the focused tests from the [testing guide](../testing/testing-guide.md).
6. For empty answers, inspect graph chunk count, embeddings, source status, evidence score, and the configured LLM path; the current zero-vector/empty-embedding behavior is a known limitation.

## Backup and recovery

`scripts/backup.sh` and `scripts/restore.sh` are repository-provided operational anchors. Inspect their current commands and validate volumes/credentials before using them for real recovery. Compose declares named volumes for Neo4j, PostgreSQL, Redis, and MinIO; local storage code may also write outside those volumes.

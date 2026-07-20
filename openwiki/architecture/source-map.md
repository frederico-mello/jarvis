---
type: Source Map
title: Repository source map
description: Practical navigation map for the ICT GraphRAG source tree, specifications, operational scripts, generated analysis, and tests.
tags: [source-map, navigation]
---
# Repository source map

Use this page to choose the smallest source slice for a change. Start with the [runtime architecture](overview.md), then follow the domain-specific anchors below.

## Root and configuration

- `README.md` — Portuguese setup, commands, API examples, and package overview.
- `pyproject.toml` — Python package metadata, runtime/dev dependencies, Ruff, and strict mypy settings.
- `.env.example` — placeholder configuration surface; never read or document live `.env` values.
- `Dockerfile`, `docker-compose.yml` — worker image and local infrastructure topology.
- `src/main.py` — Uvicorn development entrypoint.

## Source packages

- `src/api/` — FastAPI assembly, routes, JWT admin checks, rate limiting, health, and audit helper.
- `src/config/` — environment-backed settings and the configured ICT sector taxonomy.
- `src/ingestion/` — crawler, change detector, HTML/document processors, chunking, storage, Celery tasks, and worker.
- `src/graph/` — Neo4j driver/schema, entities, extraction validation, provenance, embeddings, and seed data.
- `src/retrieval/` — vector/full-text search, hybrid merge, graph traversal, generation, safety, citations, and source status.
- `src/conversation/` — logs, analytics, question clustering, FAQ promotion/cache.
- `src/common/` — shared exceptions and structured logging.

## Product/design evidence

`openspec/specs/` contains active requirements for authorized uploads, conversation logs, FAQ discovery, knowledge graph behavior, public QA, citations, and source ingestion. The archived initial change under `openspec/changes/archive/2026-07-20-initial-graphrag-platform/` contains the proposal, design, tasks, and prior specs; use it to distinguish intended behavior from what is wired today. OpenSpec command/skill files live under `.opencode/`.

## Operations and validation

- `scripts/setup-dev.sh` — development setup helper.
- `scripts/backup.sh`, `scripts/restore.sh` — backup/restore scripts whose operational assumptions should be reviewed before production use.
- `tests/test_regression.py` — focused unit/regression checks for chunking, extraction, safety, graph extraction validation, and sector configuration.
- `tests/test_evaluation.py`, `tests/sample_questions.py` — question/evaluation harness.
- `graphify-out/` — generated graph analysis artifacts from the latest commit; useful for exploration, not runtime source of truth.

## Git landmarks

`cf05589` is the initial implementation commit. `eadc3c4` and `6e948db` concern OpenSpec workflow tooling. `2dd89d9` adds generated Graphify output. There are no later route/ingestion implementation commits in the inspected history, so source and active specs may diverge without a corrective follow-up commit.

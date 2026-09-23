---
type: Source Map
title: Repository source map
description: Practical navigation map for the ICT GraphRAG source tree, specifications, operational scripts, generated analysis, and tests.
tags: [source-map, navigation]
verified:
  - by: openwiki/0.5.2
    at: 2026-09-23T13:16:57.818Z
sources:
  - id: openwiki-source-35d036bbe6908fb82cfee21f
    resource: repo://.opencode/commands/opsx-apply.md
  - id: openwiki-source-784f6063928f9cd634a077c7
    resource: repo://graphify-out/manifest.json
  - id: openwiki-source-22fa06d123fa2982bf7de5e8
    resource: repo://openspec/changes/archive/2026-07-20-initial-graphrag-platform/proposal.md
  - id: openwiki-source-f123bc49d69d22dbb01483d8
    resource: repo://openspec/specs/authorized-document-upload/spec.md
  - id: openwiki-source-221b03a51148a123c45e2e0d
    resource: repo://openspec/specs/conversation-logs/spec.md
  - id: openwiki-source-eaaf6bb7133690c7be0839a6
    resource: repo://openspec/specs/faq-discovery/spec.md
  - id: openwiki-source-192f09b3ca95be2db7607697
    resource: repo://openspec/specs/knowledge-graph/spec.md
  - id: openwiki-source-0fe88cd009a42dcff567ad75
    resource: repo://openspec/specs/public-question-answering/spec.md
  - id: openwiki-source-7d0891068c884ec90c8532a0
    resource: repo://openspec/specs/source-citations/spec.md
  - id: openwiki-source-a590734044f4be7d93df557c
    resource: repo://openspec/specs/source-ingestion/spec.md
  - id: openwiki-source-05ccef8d4cf1698187f20464
    resource: repo://pyproject.toml
  - id: openwiki-source-23775c3de52f3ab95a13cb8b
    resource: repo://README.md
  - id: openwiki-source-22e54198dab82de8525d58b4
    resource: repo://scripts/setup-dev.sh
  - id: openwiki-source-7782770e0e05d136fdaaf5c3
    resource: repo://src/api/app.py
  - id: openwiki-source-22938c061750bd6b54ec09f3
    resource: repo://src/common/exceptions.py
  - id: openwiki-source-dc4c94e136b9b55d0e0a3361
    resource: repo://src/conversation/logs.py
  - id: openwiki-source-c3b6b4c0ff7bcc24e288351a
    resource: repo://src/graph/entities.py
  - id: openwiki-source-d27d0b753d787a070ebd1813
    resource: repo://src/ingestion/document_processor.py
  - id: openwiki-source-11b9d806fcc6dd6e7747ed87
    resource: repo://src/main.py
  - id: openwiki-source-102bbf58de971a70759e52d0
    resource: repo://src/retrieval/hybrid.py
  - id: openwiki-source-c60faaa8fff57df6c1fdc61f
    resource: repo://tests/test_evaluation.py
  - id: openwiki-source-16b3095b0424565b5a9ab034
    resource: repo://tests/test_regression.py
generated: { by: "openwiki/0.5.2", at: "2026-09-23T13:16:57.818Z" }
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

The repository has a single squashed commit (`f098d26`) that includes all source packages, OpenSpec specs and workflow tooling, scripts, tests, and generated Graphify output. The shallow clone contains only that commit, and the reflog shows just a `master` -> `main` rename, so there is no prior commit history to diff against — source and active specs may diverge without a corrective follow-up commit.

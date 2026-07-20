---
type: Testing Guide
title: Testing and evaluation
description: Test commands and coverage map for ingestion utilities, prompt-injection safety, extraction validation, sector configuration, and question evaluation.
tags: [testing, pytest, evaluation]
---
# Testing and evaluation

The package defines pytest, pytest-asyncio, coverage, Ruff, and mypy development dependencies. The [source map](../architecture/source-map.md) identifies test and evaluation files; the [ingestion and QA workflow](../workflows/ingestion-and-qa.md) identifies the production paths the tests should protect.

## Run checks

```bash
pytest tests/ -v
ruff check .
mypy src/
```

The README explicitly documents the pytest command. Ruff targets Python 3.11, line length 100, and rules `E,F,I,N,W,UP`; mypy is strict.

## Current regression coverage

`tests/test_regression.py` covers:

- empty/small/large text chunking and overlap bounds;
- HTML title/text extraction and removal of scripts;
- prompt-injection pattern detection and context sanitization;
- evidence sufficiency threshold behavior;
- valid/invalid/low-confidence extracted entities and relations;
- configured sector count, sector types, and unique IDs.

These are mostly deterministic unit checks and do not require live Neo4j, Redis, an LLM, or external web access.

## Evaluation harness

`tests/sample_questions.py` contains representative institutional questions. `tests/test_evaluation.py` provides the evaluation path; inspect its current fixtures/assumptions before treating its scores as production quality evidence. The repository does not show a complete live-service integration suite for API, graph indexes, Celery tasks, uploads, or citations.

## High-value test additions

When implementing backlog items, add tests for hash-based changed/unchanged ingestion, document version increments and duplicate hashes, embedding generation dimensions, active-source filtering, graph-aware traversal selection, rich citation fields, upload filename safety, JWT authorization, health status semantics, and FAQ source freshness. Prefer unit tests around pure helpers, then add dependency-backed integration tests where query/schema behavior matters.

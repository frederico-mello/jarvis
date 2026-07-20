---
type: Integration Guide
title: Infrastructure integrations
description: Boundaries and actual wiring for Neo4j, Redis/Celery, PostgreSQL, MinIO/local storage, embeddings, and LLM configuration.
tags: [integrations, neo4j, redis, celery, storage]
---
# Infrastructure integrations

The application is centered on Neo4j, with Redis/Celery supporting asynchronous ingestion. PostgreSQL and MinIO are present in local Compose but are only partially wired by application code. See the [runtime architecture](../architecture/overview.md) and [operations runbook](../operations/runbook.md).

## Neo4j

`src/graph/driver.py` creates drivers from settings. `src/graph/schema.py` configures constraints/indexes, including vector and full-text indexes. Entity, provenance, retrieval, traversal, conversation, and health modules all use Neo4j operations. Run index setup before retrieval and seed sectors with `src.graph.seed` during initial setup.

Neo4j is therefore both the institutional knowledge graph and the source/chunk retrieval store. Schema changes must be coordinated across entity persistence, Cypher search/traversal, extraction validation, and tests.

## Redis and Celery

Redis is configured by `redis_url`, used by Celery in `src/ingestion/worker.py`, and checked by the health endpoint. The worker runs crawler tasks; beat schedules periodic crawling. Compose supplies a worker but not a separate beat service, so periodic scheduling must be launched explicitly unless deployment adds it.

## PostgreSQL

Compose starts PostgreSQL and settings expose `postgresql_dsn`. The worker receives a DSN environment variable, but no inspected source module defines a PostgreSQL repository or schema. Treat it as optional/future infrastructure rather than an application-backed source of truth.

## MinIO and storage

Compose starts MinIO with named persistent storage. Current `src/ingestion/storage.py` writes originals to a local `storage/` path and creates directories locally; no MinIO client integration was found. This differs from the archived design's object-storage intent. Confirm the deployment storage contract before relying on uploads across containers.

## Embeddings and LLM

Settings expose a sentence-transformers model and 384 dimensions plus LLM URL/key/model fields. `src/graph/embeddings.py` contains helpers, but the inspected ingestion and API paths do not invoke model encoding; `/ask` passes a zero vector. Generation has a Portuguese prompt and excerpt fallback, but no complete provider client is evident. Any provider integration should define batching, failures, model/dimension compatibility, secret handling, and deterministic tests.

## Security boundary

Admin document routes use JWT HS256 with the configured secret and an `admin` claim. No login/token issuance or revocation store is included. Infrastructure credentials in Compose are development defaults; production configuration must replace them through trusted environment/secrets management.

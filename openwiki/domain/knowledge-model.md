---
type: Domain Model
title: Knowledge graph and provenance model
description: Institutional ICT-SJC graph vocabulary, source/chunk records, extraction confidence, and provenance relationships used by GraphRAG.
tags: [domain, neo4j, provenance, knowledge-graph]
---
# Knowledge graph and provenance model

Neo4j is the system of record for the institutional graph and retrieval chunks. The model combines typed ICT-SJC concepts with source material and provenance. Retrieval and [infrastructure integrations](../integrations/infrastructure.md) depend on these shapes.

## Institutional concepts

`src/graph/entities.py` supports `Sector`, `Person`, `Position`, `Service`, `Document`, `Norm`, `WebPage`, and `Contact` nodes. Representative relationships include:

- sectors `BELONGS_TO` other sectors;
- sectors `OFFERS` services;
- people `OCCUPIES` positions;
- positions `IN_SECTOR` sectors;
- documents `REGULATE`/`REGULATES` targets and norms;
- norms `REPLACES` or `REVOKES` other norms.

`src/config/models.py` supplies the configured sector taxonomy, and `src/graph/seed.py` loads sectors. The entity helper layer is a vocabulary and persistence adapter; it is not evidence that all extraction paths are active.

## Source and retrieval records

`Source` represents an origin such as a web page or uploaded document. `Document` carries document metadata/version state. `Chunk` is the retrieval unit and can hold text, source/document IDs, page number, embedding, and timestamps. Provenance helpers create `Source -[:HAS_CHUNK]-> Chunk` and document-to-chunk links.

The retrieval layer should use source status (`active`, `unavailable`, `replaced` helpers exist) when selecting evidence. Current search queries do not enforce that filter, so status changes can leave stale material retrievable.

## Extracted facts

`src/graph/extraction.py` defines typed `ExtractedEntity` and `ExtractedRelation` models with confidence, extraction timestamp, and `source_chunk_id`. Validators check allowed labels/types and confidence. This is the intended bridge from text chunks to institutional graph facts, but no inspected production task invokes validation and persists those extracted entities/relations. Provenance is therefore modeled more completely than it is currently operationalized.

## Indexes and identifiers

`src/graph/schema.py` creates constraints/indexes for identifiers, a `chunk_embedding` vector index, and full-text indexes. The configured embedding model is `sentence-transformers/all-MiniLM-L6-v2` with 384 dimensions. Current ingestion creates chunks without embeddings, while `/ask` supplies a zero vector; this is the highest-impact model/retrieval gap.

## Seed data and consistency rules

When changing labels, relation names, identifiers, or status values, update entity helpers, schema/index setup, extraction validators, traversal queries, OpenSpec knowledge-graph requirements, and tests. Keep source chunk IDs attached to extracted facts so answers can be traced to evidence once extraction persistence is implemented.

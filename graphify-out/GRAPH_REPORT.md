# Graph Report - .  (2026-07-20)

## Corpus Check
- Corpus is ~33,813 words - fits in a single context window. You may not need a graph.

## Summary
- 376 nodes · 844 edges · 30 communities (27 shown, 3 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 80 edges (avg confidence: 0.77)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- FastAPI Application Core
- Data Models & Types
- GraphRAG Platform
- Web Crawler
- Answer Generation
- Infrastructure Services
- OpenSpec Skills
- OpenSpec Concepts
- Analytics & Citations
- Authentication & Security
- Question Answering
- Entity Management
- FAQ & Conversations
- Embeddings
- OpenSpec Artifact Workflow
- Backup
- Restore
- Neo4j Schema
- Rate Limiting
- Development Setup
- Project Root

## God Nodes (most connected - your core abstractions)
1. `get_driver()` - 53 edges
2. `get_logger()` - 32 edges
3. `ValidationError` - 13 edges
4. `OPSX Onboard Command` - 12 edges
5. `ExtractedEntity` - 11 edges
6. `process_document()` - 11 edges
7. `HybridResult` - 11 edges
8. `OpenSpec Change` - 11 edges
9. `OpenSpec Store` - 11 edges
10. `OpenSpec CLI` - 11 edges

## Surprising Connections (you probably didn't know these)
- `TestConfig` --uses--> `SectorType`  [INFERRED]
  tests/test_regression.py → src/config/models.py
- `TestExtraction` --uses--> `SectorType`  [INFERRED]
  tests/test_regression.py → src/config/models.py
- `TestIngestion` --uses--> `SectorType`  [INFERRED]
  tests/test_regression.py → src/config/models.py
- `TestSafety` --uses--> `SectorType`  [INFERRED]
  tests/test_regression.py → src/config/models.py
- `TestConfig` --uses--> `SectorConfig`  [INFERRED]
  tests/test_regression.py → src/config/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Core OpenSpec Workflow Commands** — opencode_commands_opsx-new, opencode_commands_opsx-continue, opencode_commands_opsx-apply, opencode_commands_opsx-archive [INFERRED 0.95]
- **Artifact Types in spec-driven Schema** — opencode_commands_proposal_artifact, opencode_commands_specs_artifact, opencode_commands_design_artifact, opencode_commands_tasks_artifact [INFERRED 0.95]
- **OpenSpec Skill Suite** — _opencode_skills_openspec_apply_change_skill_openspec_apply_change, _opencode_skills_openspec_archive_change_skill_openspec_archive_change, _opencode_skills_openspec_bulk_archive_change_skill_openspec_bulk_archive_change, _opencode_skills_openspec_continue_change_skill_openspec_continue_change, _opencode_skills_openspec_explore_skill_openspec_explore, _opencode_skills_openspec_ff_change_skill_openspec_ff_change, _opencode_skills_openspec_new_change_skill_openspec_new_change, _opencode_skills_openspec_onboard_skill_openspec_onboard, _opencode_skills_openspec_propose_skill_openspec_propose, _opencode_skills_openspec_sync_specs_skill_openspec_sync_specs, _opencode_skills_openspec_verify_change_skill_openspec_verify_change [EXTRACTED 1.00]
- **OpenSpec Artifact Types** — openspec_artifact, openspec_delta_spec, openspec_main_spec [INFERRED 0.85]
- **Initial GraphRAG Platform Capabilities** — openspec_changes_archive_2026_07_20_initial_graphrag_platform_proposal_public_question_answering, openspec_changes_archive_2026_07_20_initial_graphrag_platform_proposal_knowledge_graph, openspec_changes_archive_2026_07_20_initial_graphrag_platform_proposal_source_ingestion, openspec_changes_archive_2026_07_20_initial_graphrag_platform_proposal_authorized_document_upload, openspec_changes_archive_2026_07_20_initial_graphrag_platform_proposal_source_citations, openspec_changes_archive_2026_07_20_initial_graphrag_platform_proposal_conversation_logs, openspec_changes_archive_2026_07_20_initial_graphrag_platform_proposal_faq_discovery [EXTRACTED 1.00]
- **Ingestion Pipeline** — openspec_changes_archive_2026_07_20_initial_graphrag_platform_design_idempotent_ingestion, openspec_changes_archive_2026_07_20_initial_graphrag_platform_proposal_source_ingestion, openspec_changes_archive_2026_07_20_initial_graphrag_platform_proposal_authorized_document_upload, openspec_changes_archive_2026_07_20_initial_graphrag_platform_specs_source_ingestion_spec_crawl_pages, openspec_changes_archive_2026_07_20_initial_graphrag_platform_specs_source_ingestion_spec_idempotent, openspec_changes_archive_2026_07_20_initial_graphrag_platform_specs_source_ingestion_spec_extract_knowledge, openspec_changes_archive_2026_07_20_initial_graphrag_platform_specs_source_ingestion_spec_unavailable, openspec_changes_archive_2026_07_20_initial_graphrag_platform_specs_authorized_document_upload_spec_authenticate_upload, openspec_changes_archive_2026_07_20_initial_graphrag_platform_specs_authorized_document_upload_spec_validate_files, openspec_changes_archive_2026_07_20_initial_graphrag_platform_specs_authorized_document_upload_spec_audit_lifecycle [EXTRACTED 1.00]
- **Answer Pipeline** — openspec_changes_archive_2026_07_20_initial_graphrag_platform_design_hybrid_retrieval, openspec_changes_archive_2026_07_20_initial_graphrag_platform_design_graph_provenance, openspec_changes_archive_2026_07_20_initial_graphrag_platform_proposal_public_question_answering, openspec_changes_archive_2026_07_20_initial_graphrag_platform_proposal_knowledge_graph, openspec_changes_archive_2026_07_20_initial_graphrag_platform_proposal_source_citations, openspec_changes_archive_2026_07_20_initial_graphrag_platform_specs_public_question_answering_spec_answer_portuguese, openspec_changes_archive_2026_07_20_initial_graphrag_platform_specs_public_question_answering_spec_graph_aware_retrieval, openspec_changes_archive_2026_07_20_initial_graphrag_platform_specs_public_question_answering_spec_protect_context, openspec_changes_archive_2026_07_20_initial_graphrag_platform_specs_source_citations_spec_cite_sources, openspec_changes_archive_2026_07_20_initial_graphrag_platform_specs_source_citations_spec_freshness, openspec_changes_archive_2026_07_20_initial_graphrag_platform_specs_source_citations_spec_traceable, openspec_changes_archive_2026_07_20_initial_graphrag_platform_specs_knowledge_graph_spec_store_graph, openspec_changes_archive_2026_07_20_initial_graphrag_platform_specs_knowledge_graph_spec_chunk_embeddings, openspec_changes_archive_2026_07_20_initial_graphrag_platform_specs_knowledge_graph_spec_provenance [EXTRACTED 1.00]
- **ICT GraphRAG Feature Set** — openspec_specs_authorized_document_upload_spec_authorized_document_upload, openspec_specs_conversation_logs_spec_conversation_logs, openspec_specs_faq_discovery_spec_faq_discovery, openspec_specs_knowledge_graph_spec_knowledge_graph, openspec_specs_public_question_answering_spec_public_question_answering, openspec_specs_source_citations_spec_source_citations, openspec_specs_source_ingestion_spec_source_ingestion [EXTRACTED 1.00]
- **Data Infrastructure Layer** — docker_compose_neo4j_service, docker_compose_redis_service, docker_compose_postgres_service, docker_compose_minio_service [EXTRACTED 1.00]

## Communities (30 total, 3 thin omitted)

### Community 0 - "FastAPI Application Core"
Cohesion: 0.09
Nodes (43): BaseSettings, BoundLogger, FastAPI, create_app(), get_audit_history(), log_audit_event(), check_neo4j(), check_redis() (+35 more)

### Community 1 - "Data Models & Types"
Cohesion: 0.11
Nodes (25): DocumentStatus, BaseModel, SectorConfig, SectorType, SourceStatus, SourceType, ExtractedEntity, ExtractedRelation (+17 more)

### Community 2 - "GraphRAG Platform"
Cohesion: 0.08
Nodes (30): Automatic Processing with Limits, Graph with Provenance, GraphRAG, Hybrid Retrieval, ICT-SJC, Idempotent Versioned Ingestion, Neo4j, Separation of Responsibilities (+22 more)

### Community 3 - "Web Crawler"
Cohesion: 0.13
Nodes (18): BeautifulSoup, get_source_by_url(), mark_source_unavailable(), discover_pages(), fetch_page(), PageResult, datetime, _resolve_url() (+10 more)

### Community 4 - "Answer Generation"
Cohesion: 0.19
Nodes (19): build_prompt(), _fallback_answer(), generate_answer(), GeneratedAnswer, hybrid_search(), hybrid_search_with_graph(), HybridResult, ChunkResult (+11 more)

### Community 5 - "Infrastructure Services"
Cohesion: 0.12
Nodes (24): MinIO Service, Neo4j Service, PostgreSQL Service, Redis Service, Worker Service, Authorized Document Upload, Conversation Logs, FAQ Discovery (+16 more)

### Community 6 - "OpenSpec Skills"
Cohesion: 0.13
Nodes (22): openspec-apply-change Skill, openspec-archive-change Skill, openspec-bulk-archive-change Skill, openspec-continue-change Skill, openspec-explore Skill, openspec-ff-change Skill, openspec-new-change Skill, openspec-onboard Skill (+14 more)

### Community 7 - "OpenSpec Concepts"
Cohesion: 0.32
Nodes (22): OpenSpec Archive, OpenSpec Artifact, OpenSpec Change, OpenSpec CLI, Delta Spec, Explore Mode, Explore Mode Stance (curious, visual, adaptive, patient), Intelligent Merging Principle (+14 more)

### Community 8 - "Analytics & Citations"
Cohesion: 0.18
Nodes (14): get_coverage_gaps(), get_popular_questions(), get_system_stats(), build_citations(), Citation, format_citations(), datetime, has_sufficient_evidence() (+6 more)

### Community 9 - "Authentication & Security"
Cohesion: 0.18
Nodes (12): Exception, HTTPAuthorizationCredentials, decode_access_token(), get_current_user(), require_admin(), AuthenticationError, AuthorizationError, ConfigurationError (+4 more)

### Community 10 - "Question Answering"
Cohesion: 0.31
Nodes (14): AnswerResponse, ask_question(), BaseModel, Request, QuestionRequest, SourceResponse, ValidationError, process_document() (+6 more)

### Community 11 - "Entity Management"
Cohesion: 0.26
Nodes (13): create_contact(), create_document(), create_norm(), create_person(), create_position(), create_sector(), create_service(), create_web_page() (+5 more)

### Community 12 - "FAQ & Conversations"
Cohesion: 0.27
Nodes (10): Anonymous Conversation Logging, FAQ Discovery, Conversation Logs, FAQ Discovery, Conversation Analysis, Log Conversations Anonymously, Protect Logged Data, Group Semantically Similar Questions (+2 more)

### Community 13 - "Embeddings"
Cohesion: 0.43
Nodes (7): count_chunks(), count_chunks_with_embeddings(), delete_chunks_by_source(), get_chunks_by_source(), get_chunks_without_embedding(), ManagedTransaction, upsert_chunk_embedding()

### Community 14 - "OpenSpec Artifact Workflow"
Cohesion: 0.70
Nodes (5): Artifact Sequence (proposal→specs→design→tasks), Design Artifact, Proposal Artifact, Specs Artifact, Tasks Artifact

### Community 15 - "Backup"
Cohesion: 0.70
Nodes (4): backup_neo4j(), backup_postgres(), backup_storage(), backup.sh script

### Community 16 - "Restore"
Cohesion: 0.70
Nodes (4): restore_neo4j(), restore_postgres(), restore_storage(), restore.sh script

### Community 17 - "Neo4j Schema"
Cohesion: 0.60
Nodes (4): get_async_driver(), get_driver(), driver, setup_indexes()

## Knowledge Gaps
- **24 isolated node(s):** `ict-graphrag`, `setup-dev.sh script`, `openspec-new-change Skill`, `OpenSpec Store`, `ICT-SJC` (+19 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_driver()` connect `FastAPI Application Core` to `Data Models & Types`, `Web Crawler`, `Answer Generation`, `Analytics & Citations`, `Entity Management`, `Embeddings`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Why does `get_logger()` connect `FastAPI Application Core` to `Data Models & Types`, `Web Crawler`, `Answer Generation`, `Analytics & Citations`, `Question Answering`, `Entity Management`, `Embeddings`, `Neo4j Schema`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `chunk_text()` connect `Data Models & Types` to `FastAPI Application Core`, `Web Crawler`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `ValidationError` (e.g. with `AnswerResponse` and `QuestionRequest`) actually correct?**
  _`ValidationError` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ict-graphrag`, `setup-dev.sh script`, `openspec-new-change Skill` to the rest of the system?**
  _24 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FastAPI Application Core` be split into smaller, more focused modules?**
  _Cohesion score 0.08619777895293496 - nodes in this community are weakly interconnected._
- **Should `Data Models & Types` be split into smaller, more focused modules?**
  _Cohesion score 0.10685249709639953 - nodes in this community are weakly interconnected._
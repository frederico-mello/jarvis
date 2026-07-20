## ADDED Requirements

### Requirement: Crawl public institutional pages
The system SHALL periodically discover and ingest publicly available pages from `ict.unesp.br` according to a configurable schedule.

#### Scenario: Scheduled synchronization
- **WHEN** a configured ingestion interval elapses
- **THEN** the worker discovers eligible public pages and processes new or changed content

### Requirement: Process source changes idempotently
The system SHALL identify sources by stable URL or document identifier and SHALL avoid creating duplicate active versions when content has not changed.

#### Scenario: Unchanged page
- **WHEN** a crawl finds a page whose content hash is unchanged
- **THEN** the system records the check without creating a duplicate version or reprocessing the page

#### Scenario: Changed page
- **WHEN** a crawl finds changed content at an existing URL
- **THEN** the system creates a new version while preserving the previous version for provenance

### Requirement: Extract source knowledge
The system SHALL extract text, metadata, entities and relationships from each accepted source and index the resulting chunks in the graph.

#### Scenario: Process a portaria
- **WHEN** a portaria is ingested
- **THEN** the system stores its text, identifying metadata, relevant entities, relationships and source references

### Requirement: Handle unavailable sources
The system SHALL mark removed or inaccessible sources as unavailable without immediately deleting their historical versions.

#### Scenario: Removed web page
- **WHEN** a previously indexed page is no longer publicly available
- **THEN** the system marks its current version unavailable and retains its historical provenance

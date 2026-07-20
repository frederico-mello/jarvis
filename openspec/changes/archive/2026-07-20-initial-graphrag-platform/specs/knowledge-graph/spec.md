## ADDED Requirements

### Requirement: Store institutional knowledge as a graph
The system SHALL store ICT-SJC sectors, services, procedures, people, positions, documents, norms, courses and web pages as typed graph entities with typed relationships.

#### Scenario: Sector classification
- **WHEN** a source identifies a section or directorate
- **THEN** the graph associates the source with the corresponding ICT-SJC sector

### Requirement: Store chunk embeddings and search indexes
The system SHALL store source chunks with embeddings and SHALL provide vector and full-text indexes for retrieval.

#### Scenario: Hybrid retrieval
- **WHEN** a user asks using both natural language and an exact portaria number
- **THEN** the system can combine semantic and full-text results

### Requirement: Preserve graph provenance
Every automatically extracted entity and relationship SHALL reference its source chunk, source identifier, extraction timestamp and confidence.

#### Scenario: Inspect relationship evidence
- **WHEN** an operator inspects a relationship between a sector and a service
- **THEN** the system displays the source chunk and extraction metadata that support it

### Requirement: Track institutional sector taxonomy
The initial graph SHALL support the configured administrative, academic, auxiliary, childcare and information technology sectors of ICT-SJC.

#### Scenario: Query sector membership
- **WHEN** a question asks about a named ICT-SJC sector
- **THEN** the graph resolves the sector and its hierarchy when the source contains that information

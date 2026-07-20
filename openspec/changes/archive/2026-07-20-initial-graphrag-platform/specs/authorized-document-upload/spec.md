## ADDED Requirements

### Requirement: Authenticate document upload
The system SHALL allow document uploads only to authenticated and authorized servers.

#### Scenario: Authorized upload
- **WHEN** an authenticated server uploads an accepted document
- **THEN** the system stores the document and records the uploader identity

#### Scenario: Unauthorized upload
- **WHEN** an unauthenticated or unauthorized user attempts to upload a document
- **THEN** the system rejects the request and creates an auditable security event

### Requirement: Validate uploaded files
The system SHALL validate file type, size, integrity and processing limits before indexing an uploaded document.

#### Scenario: Invalid file
- **WHEN** an upload violates a configured validation rule
- **THEN** the system rejects it without adding content to the knowledge graph

### Requirement: Audit document lifecycle
The system SHALL record upload, processing, replacement, deactivation and deletion actions with actor, timestamp and source identifier.

#### Scenario: Deactivate document
- **WHEN** an authorized server deactivates a document
- **THEN** the document is excluded from active retrieval while its audit record and historical provenance remain available

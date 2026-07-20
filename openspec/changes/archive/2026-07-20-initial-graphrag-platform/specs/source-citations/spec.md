## ADDED Requirements

### Requirement: Cite answer sources
Every substantive answer SHALL include the source title or identifier, link or document reference, and the relevant collection or publication date when available.

#### Scenario: Web answer
- **WHEN** an answer uses an ICT-SJC web page
- **THEN** the response includes a link to that page and its source metadata

#### Scenario: Uploaded document answer
- **WHEN** an answer uses an uploaded document
- **THEN** the response identifies the document and page or section when available

### Requirement: Communicate source freshness
The system SHALL expose source freshness and SHALL distinguish active, unavailable, outdated or revoked sources when that status is known.

#### Scenario: Revoked norm
- **WHEN** a response relies on a norm identified as revoked or superseded
- **THEN** the response warns the user and identifies the newer or governing source when available

### Requirement: Make evidence traceable
The system SHALL allow a user or operator to trace each cited answer claim to one or more retrieved chunks.

#### Scenario: Inspect citation
- **WHEN** a user opens a citation
- **THEN** the system displays the associated source and the relevant evidence excerpt, subject to public access rules

## Purpose

Identificar automaticamente perguntas frequentes para reduzir reprocessamento, acelerar respostas e melhorar a experiência do usuário.

## Requirements

### Requirement: Group semantically similar questions
The system SHALL group questions by semantic similarity to identify recurring topics.

#### Scenario: Detect recurring question
- **WHEN** multiple users ask semantically similar questions
- **THEN** the system groups them and tracks the recurrence count

### Requirement: Promote frequent questions to FAQ
The system SHALL promote a question group to FAQ status when its recurrence exceeds a configurable threshold.

#### Scenario: FAQ promotion
- **WHEN** a question group reaches the configured recurrence threshold
- **THEN** the system marks it as FAQ and may serve the cached answer directly

### Requirement: Serve FAQ answers efficiently
The system SHALL serve FAQ answers without full retrieval pipeline reprocessing when a cached answer is available and its sources remain current.

#### Scenario: FAQ answer served
- **WHEN** a user asks a question matching a current FAQ
- **THEN** the system returns the cached answer with source references

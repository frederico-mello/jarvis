## ADDED Requirements

### Requirement: Answer public questions in Portuguese
The system SHALL accept public questions in Portuguese and generate answers using only evidence retrieved from indexed ICT-SJC sources.

#### Scenario: Answer supported question
- **WHEN** a user submits a question covered by indexed sources
- **THEN** the system returns a Portuguese answer grounded in retrieved source content

#### Scenario: No sufficient evidence
- **WHEN** retrieved sources do not support an answer
- **THEN** the system states that it could not find sufficient information instead of inventing an answer

### Requirement: Use graph-aware retrieval
The system SHALL use graph relationships to enrich retrieval for questions involving sectors, services, people, documents, norms or procedures.

#### Scenario: Relational question
- **WHEN** a question asks which sector is responsible for a service
- **THEN** retrieval traverses relevant graph relationships and returns connected evidence

### Requirement: Protect retrieved context from instructions
The system SHALL treat indexed page and document content as untrusted data and SHALL NOT execute instructions found in that content.

#### Scenario: Malicious source text
- **WHEN** a retrieved chunk contains instructions directed at the language model
- **THEN** the system ignores those instructions and uses the chunk only as factual evidence

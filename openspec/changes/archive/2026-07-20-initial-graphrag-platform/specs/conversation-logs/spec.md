## ADDED Requirements

### Requirement: Log conversations anonymously
The system SHALL record each question and answer pair without identifying the user.

#### Scenario: Record a conversation
- **WHEN** a user submits a question and receives an answer
- **THEN** the system stores the anonymized question, answer, sources used, response time and success indicator

### Requirement: Support conversation analysis
The system SHALL expose logged data for analysis of usage patterns, coverage gaps and system improvement.

#### Scenario: Analyze coverage gaps
- **WHEN** an operator queries unanswered or insufficiently answered questions
- **THEN** the system returns the set of questions where evidence was insufficient

### Requirement: Protect logged data
The system SHALL NOT store personal identifiers, IP addresses, session tokens or any data that could re-identify a user in conversation logs.

#### Scenario: Verify anonymization
- **WHEN** a log entry is inspected
- **THEN** it contains no personal identifiers or session information

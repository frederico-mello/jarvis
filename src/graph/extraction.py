from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any


class ExtractedEntity(BaseModel):
    id: str | None = None
    label: str
    name: str
    properties: dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(ge=0.0, le=1.0)
    source_chunk_id: str
    extracted_at: datetime = Field(default_factory=datetime.utcnow)


class ExtractedRelation(BaseModel):
    source_id: str
    source_label: str
    target_id: str
    target_label: str
    relation_type: str
    properties: dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(ge=0.0, le=1.0)
    source_chunk_id: str
    extracted_at: datetime = Field(default_factory=datetime.utcnow)


class ExtractionResult(BaseModel):
    entities: list[ExtractedEntity] = Field(default_factory=list)
    relations: list[ExtractedRelation] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


ENTITY_LABELS = {"Sector", "Person", "Position", "Service", "Document", "Norm", "Course", "WebPage", "Contact"}

RELATION_TYPES = {
    "BELONGS_TO", "OFFERS", "PUBLISHES", "REGULATES", "REPLACES", "REVOKES",
    "OCCUPIES", "BELONGS_TO_SECTOR", "HAS_CONTACT", "HAS_CHUNK", "MENTIONS",
    "RESPONSIBLE_FOR", "REQUIRES_DOCUMENT",
}


def validate_entity(entity: ExtractedEntity) -> list[str]:
    errors: list[str] = []
    if entity.label not in ENTITY_LABELS:
        errors.append(f"Unknown entity label: {entity.label}")
    if not entity.name.strip():
        errors.append("Entity name cannot be empty")
    if entity.confidence < 0.3:
        errors.append(f"Low confidence entity: {entity.confidence}")
    return errors


def validate_relation(relation: ExtractedRelation) -> list[str]:
    errors: list[str] = []
    if relation.relation_type not in RELATION_TYPES:
        errors.append(f"Unknown relation type: {relation.relation_type}")
    if not relation.source_id or not relation.target_id:
        errors.append("Relation must have source and target IDs")
    if relation.confidence < 0.3:
        errors.append(f"Low confidence relation: {relation.confidence}")
    return errors


def validate_extraction(result: ExtractionResult) -> list[str]:
    errors: list[str] = []
    for entity in result.entities:
        errors.extend(validate_entity(entity))
    for relation in result.relations:
        errors.extend(validate_relation(relation))
    return errors

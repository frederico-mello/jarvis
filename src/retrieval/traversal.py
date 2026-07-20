from neo4j import ManagedTransaction
from src.graph.driver import get_driver
from src.common.logging import get_logger

logger = get_logger(__name__)


class GraphContext:
    def __init__(self, entities: list[dict], relations: list[dict]):
        self.entities = entities
        self.relations = relations


def traverse_sector_services(tx: ManagedTransaction, sector_id: str) -> GraphContext:
    result = tx.run("""
        MATCH (s:Sector {id: $id})-[:OFFERS]->(sv:Service)
        OPTIONAL MATCH (sv)-[:REQUIRES_DOCUMENT]->(d:Document)
        RETURN s.name AS sector, collect(DISTINCT sv.name) AS services,
               collect(DISTINCT d.title) AS required_documents
    """, id=sector_id)
    record = result.single()
    if not record:
        return GraphContext([], [])
    return GraphContext(
        entities=[{"label": "Sector", "name": record["sector"]}],
        relations=[{"type": "OFFERS", "services": record["services"], "documents": record["required_documents"]}],
    )


def traverse_document_norms(tx: ManagedTransaction, document_id: str) -> GraphContext:
    result = tx.run("""
        MATCH (d:Document {id: $id})
        OPTIONAL MATCH (d)-[:REGULATES]->(target)
        OPTIONAL MATCH (n:Norm)-[:REGULATES]->(d)
        RETURN d.title AS document,
               collect(DISTINCT target.name) AS regulates,
               collect(DISTINCT n.title) AS regulated_by
    """, id=document_id)
    record = result.single()
    if not record:
        return GraphContext([], [])
    return GraphContext(
        entities=[{"label": "Document", "name": record["document"]}],
        relations=[
            {"type": "REGULATES", "targets": record["regulates"]},
            {"type": "REGULATED_BY", "sources": record["regulated_by"]},
        ],
    )


def traverse_person_sector(tx: ManagedTransaction, person_name: str) -> GraphContext:
    result = tx.run("""
        MATCH (p:Person {name: $name})-[:OCCUPIES]->(pos:Position)-[:BELONGS_TO_SECTOR]->(s:Sector)
        RETURN p.name AS person, pos.title AS position, s.name AS sector
    """, name=person_name)
    records = list(result)
    if not records:
        return GraphContext([], [])
    entities = [
        {"label": "Person", "name": r["person"]},
        {"label": "Position", "name": r["position"]},
        {"label": "Sector", "name": r["sector"]},
    ]
    relations = [{"type": "OCCUPIES", "person": r["person"], "position": r["position"]} for r in records]
    return GraphContext(entities=entities, relations=relations)


def traverse_sector_hierarchy(tx: ManagedTransaction, sector_id: str) -> GraphContext:
    result = tx.run("""
        MATCH (s:Sector {id: $id})
        OPTIONAL MATCH (s)-[:BELONGS_TO]->(parent:Sector)
        OPTIONAL MATCH (child:Sector)-[:BELONGS_TO]->(s)
        RETURN s.name AS sector, parent.name AS parent_sector,
               collect(DISTINCT child.name) AS child_sectors
    """, id=sector_id)
    record = result.single()
    if not record:
        return GraphContext([], [])
    entities = [{"label": "Sector", "name": record["sector"]}]
    relations = []
    if record["parent_sector"]:
        entities.append({"label": "Sector", "name": record["parent_sector"]})
        relations.append({"type": "BELONGS_TO", "parent": record["parent_sector"]})
    if record["child_sectors"]:
        for child in record["child_sectors"]:
            entities.append({"label": "Sector", "name": child})
            relations.append({"type": "HAS_CHILD", "child": child})
    return GraphContext(entities=entities, relations=relations)

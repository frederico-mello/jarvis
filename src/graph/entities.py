from neo4j import ManagedTransaction
from src.graph.driver import get_driver
from src.common.logging import get_logger

logger = get_logger(__name__)


def create_sector(tx: ManagedTransaction, sector_id: str, name: str, sector_type: str, parent_id: str | None = None) -> None:
    query = """
    MERGE (s:Sector {id: $id})
    SET s.name = $name, s.type = $type, s.updated_at = datetime()
    """
    tx.run(query, id=sector_id, name=name, type=sector_type)
    if parent_id:
        tx.run("""
            MATCH (parent:Sector {id: $parent_id})
            MATCH (child:Sector {id: $child_id})
            MERGE (child)-[:BELONGS_TO]->(parent)
        """, parent_id=parent_id, child_id=sector_id)


def create_person(tx: ManagedTransaction, person_id: str, name: str, email: str | None = None) -> None:
    tx.run("""
        MERGE (p:Person {id: $id})
        SET p.name = $name, p.email = $email, p.updated_at = datetime()
    """, id=person_id, name=name, email=email)


def create_position(tx: ManagedTransaction, position_id: str, title: str, sector_id: str) -> None:
    tx.run("""
        MERGE (p:Position {id: $id})
        SET p.title = $title, p.updated_at = datetime()
    """, id=position_id, title=title)
    tx.run("""
        MATCH (pos:Position {id: $pos_id})
        MATCH (s:Sector {id: $sector_id})
        MERGE (pos)-[:BELONGS_TO_SECTOR]->(s)
    """, pos_id=position_id, sector_id=sector_id)


def create_service(tx: ManagedTransaction, service_id: str, name: str, description: str, sector_id: str) -> None:
    tx.run("""
        MERGE (s:Service {id: $id})
        SET s.name = $name, s.description = $description, s.updated_at = datetime()
    """, id=service_id, name=name, description=description)
    tx.run("""
        MATCH (sv:Service {id: $sv_id})
        MATCH (sec:Sector {id: $sector_id})
        MERGE (sec)-[:OFFERS]->(sv)
    """, sv_id=service_id, sector_id=sector_id)


def create_document(tx: ManagedTransaction, doc_id: str, title: str, doc_type: str, sector_id: str | None = None) -> None:
    tx.run("""
        MERGE (d:Document {id: $id})
        SET d.title = $title, d.type = $type, d.updated_at = datetime()
    """, id=doc_id, title=title, type=doc_type)
    if sector_id:
        tx.run("""
            MATCH (d:Document {id: $doc_id})
            MATCH (s:Sector {id: $sector_id})
            MERGE (s)-[:PUBLISHES]->(d)
        """, doc_id=doc_id, sector_id=sector_id)


def create_norm(tx: ManagedTransaction, norm_id: str, title: str, number: str, norm_type: str, date: str | None = None) -> None:
    tx.run("""
        MERGE (n:Norm {id: $id})
        SET n.title = $title, n.number = $number, n.type = $type, n.date = $date, n.updated_at = datetime()
    """, id=norm_id, title=title, number=number, type=norm_type, date=date)


def create_web_page(tx: ManagedTransaction, page_id: str, url: str, title: str, sector_id: str | None = None) -> None:
    tx.run("""
        MERGE (w:WebPage {id: $id})
        SET w.url = $url, w.title = $title, w.updated_at = datetime()
    """, id=page_id, url=url, title=title)
    if sector_id:
        tx.run("""
            MATCH (w:WebPage {id: $page_id})
            MATCH (s:Sector {id: $sector_id})
            MERGE (w)-[:BELONGS_TO]->(s)
        """, page_id=page_id, sector_id=sector_id)


def create_contact(tx: ManagedTransaction, contact_id: str, contact_type: str, value: str, sector_id: str) -> None:
    tx.run("""
        MERGE (c:Contact {id: $id})
        SET c.type = $type, c.value = $value, c.updated_at = datetime()
    """, id=contact_id, type=contact_type, value=value)
    tx.run("""
        MATCH (c:Contact {id: $contact_id})
        MATCH (s:Sector {id: $sector_id})
        MERGE (s)-[:HAS_CONTACT]->(c)
    """, contact_id=contact_id, sector_id=sector_id)


def relate_person_position(tx: ManagedTransaction, person_id: str, position_id: str) -> None:
    tx.run("""
        MATCH (p:Person {id: $person_id})
        MATCH (pos:Position {id: $position_id})
        MERGE (p)-[:OCCUPIES]->(pos)
    """, person_id=person_id, position_id=position_id)


def relate_document_regulates(tx: ManagedTransaction, doc_id: str, target_id: str, target_label: str) -> None:
    tx.run(f"""
        MATCH (d:Document {{id: $doc_id}})
        MATCH (t:{target_label} {{id: $target_id}})
        MERGE (d)-[:REGULATES]->(t)
    """, doc_id=doc_id, target_id=target_id)


def relate_norm_replaces(tx: ManagedTransaction, new_norm_id: str, old_norm_id: str) -> None:
    tx.run("""
        MATCH (new:Norm {id: $new_id})
        MATCH (old:Norm {id: $old_id})
        MERGE (new)-[:REPLACES]->(old)
    """, new_id=new_norm_id, old_id=old_norm_id)


def relate_norm_revokes(tx: ManagedTransaction, revoking_id: str, revoked_id: str) -> None:
    tx.run("""
        MATCH (r:Norm {id: $revoking_id})
        MATCH (v:Norm {id: $revoked_id})
        MERGE (r)-[:REVOKES]->(v)
    """, revoking_id=revoking_id, revoked_id=revoked_id)

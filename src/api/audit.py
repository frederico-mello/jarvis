from datetime import datetime
from src.graph.driver import get_driver
from src.common.logging import get_logger

logger = get_logger(__name__)


def log_audit_event(actor: str, action: str, resource_type: str, resource_id: str, details: dict | None = None) -> None:
    driver = get_driver()
    with driver.session() as session:
        session.run("""
            CREATE (e:AuditEvent {
                id: randomUUID(),
                actor: $actor,
                action: $action,
                resource_type: $resource_type,
                resource_id: $resource_id,
                details: $details,
                timestamp: datetime()
            })
        """, actor=actor, action=action, resource_type=resource_type,
               resource_id=resource_id, details=details or {})
    driver.close()
    logger.info("Audit event recorded", actor=actor, action=action, resource=resource_id)


def get_audit_history(resource_id: str, limit: int = 50) -> list[dict]:
    driver = get_driver()
    with driver.session() as session:
        result = session.run("""
            MATCH (e:AuditEvent)
            WHERE e.resource_id = $resource_id
            RETURN e.actor AS actor, e.action AS action,
                   e.resource_type AS resource_type, e.timestamp AS timestamp,
                   e.details AS details
            ORDER BY e.timestamp DESC
            LIMIT $limit
        """, resource_id=resource_id, limit=limit)
        records = [dict(r) for r in result]
    driver.close()
    return records

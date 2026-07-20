#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"

echo "=== ICT GraphRAG Backup ==="

backup_neo4j() {
    echo "Backing up Neo4j..."
    docker compose exec -T neo4j neo4j-admin database dump neo4j --to-path=/backups 2>/dev/null || \
    docker compose exec -T neo4j cypher-shell -u neo4j -p "${ICT_GRAPH_NEO4J_PASSWORD}" \
        "CALL apoc.export.json.all('/backups/neo4j_${TIMESTAMP}.json', {useTypes: true})" 2>/dev/null || \
    echo "WARNING: Neo4j backup skipped (APOC or admin tools not available)"
}

backup_postgres() {
    echo "Backing up PostgreSQL..."
    docker compose exec -T postgres pg_dump -U ict_graphrag ict_graphrag > "${BACKUP_DIR}/postgres_${TIMESTAMP}.sql" 2>/dev/null || \
    echo "WARNING: PostgreSQL backup skipped"
}

backup_storage() {
    echo "Backing up storage..."
    if [ -d "storage/uploads" ]; then
        tar -czf "${BACKUP_DIR}/storage_${TIMESTAMP}.tar.gz" storage/uploads/
        echo "Storage backed up: ${BACKUP_DIR}/storage_${TIMESTAMP}.tar.gz"
    else
        echo "No storage directory found, skipping"
    fi
}

backup_neo4j
backup_postgres
backup_storage

echo "Backup complete: ${BACKUP_DIR}"
ls -lh "${BACKUP_DIR}/"

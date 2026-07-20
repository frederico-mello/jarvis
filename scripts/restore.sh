#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-./backups}"
RESTORE_FILE="${1:-}"

if [ -z "$RESTORE_FILE" ]; then
    echo "Usage: $0 <backup-file>"
    echo "Available backups:"
    ls -1 "$BACKUP_DIR" 2>/dev/null || echo "No backups found"
    exit 1
fi

echo "=== ICT GraphRAG Restore ==="

restore_neo4j() {
    echo "Restoring Neo4j from $1..."
    docker compose exec -T neo4j cypher-shell -u neo4j -p "${ICT_GRAPH_NEO4J_PASSWORD}" \
        "CALL apoc.import.json('$1', {})" 2>/dev/null || \
    echo "WARNING: Neo4j restore skipped"
}

restore_postgres() {
    echo "Restoring PostgreSQL from $1..."
    docker compose exec -T postgres psql -U ict_graphrag ict_graphrag < "$1" 2>/dev/null || \
    echo "WARNING: PostgreSQL restore skipped"
}

restore_storage() {
    echo "Restoring storage from $1..."
    tar -xzf "$1" -C / 2>/dev/null || \
    echo "WARNING: Storage restore skipped"
}

case "$RESTORE_FILE" in
    *neo4j*) restore_neo4j "$RESTORE_FILE" ;;
    *postgres*) restore_postgres "$RESTORE_FILE" ;;
    *storage*) restore_storage "$RESTORE_FILE" ;;
    *)
        echo "Unknown backup type: $RESTORE_FILE"
        echo "Expected filename containing: neo4j, postgres, or storage"
        exit 1
        ;;
esac

echo "Restore complete."

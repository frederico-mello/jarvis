#!/usr/bin/env bash
set -euo pipefail

echo "=== ICT GraphRAG Development Setup ==="

echo "Starting infrastructure..."
docker compose up -d neo4j postgres redis minio

echo "Waiting for Neo4j..."
until curl -s -o /dev/null -w "%{http_code}" http://localhost:7474 | grep -q 200; do
  sleep 2
done
echo "Neo4j ready."

echo "Waiting for PostgreSQL..."
until docker compose exec postgres pg_isready -q; do
  sleep 2
done
echo "PostgreSQL ready."

echo "Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

echo "Setup complete. Run 'source .venv/bin/activate' to start."

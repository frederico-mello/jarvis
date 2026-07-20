# ICT GraphRAG

Sistema de perguntas e respostas baseado em GraphRAG para o Instituto de Ciência e Tecnologia de São José dos Campos (ICT-SJC), UNESP.

## Requisitos

- Python 3.11+
- Docker e Docker Compose
- Neo4j 5+ (Enterprise ou Community com plugins APOC)
- Redis 7+
- PostgreSQL 16+ (opcional)

## Quick Start

```bash
# 1. Clone e entre no diretório
git clone <repo> && cd ict-graphrag

# 2. Configure ambiente
cp .env.example .env
# Edite .env com suas credenciais

# 3. Inicie infraestrutura
docker compose up -d neo4j postgres redis minio

# 4. Configure ambiente Python
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# 5. Configure índices do Neo4j
python -c "from src.graph.schema import setup_indexes; setup_indexes()"

# 6. Carregue taxonomia dos setores
python -c "from src.graph.seed import seed_knowledge_graph; seed_knowledge_graph()"

# 7. Inicie API
uvicorn src.api.app:create_app --reload
```

## Configuração

Variáveis de ambiente (prefixo `ICT_GRAPH_`):

| Variável | Padrão | Descrição |
|---|---|---|
| `NEO4J_URI` | `bolt://localhost:7687` | URI do Neo4j |
| `NEO4J_USER` | `neo4j` | Usuário Neo4j |
| `NEO4J_PASSWORD` | - | Senha Neo4j |
| `REDIS_URL` | `redis://localhost:6379/0` | URL do Redis |
| `CRAWLER_INTERVAL_MINUTES` | `360` | Intervalo do crawler |
| `CRAWLER_BASE_URL` | `https://www.ict.unesp.br` | URL base do site |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Modelo de embeddings |
| `RATE_LIMIT_PER_MINUTE` | `30` | Limite de requisições |
| `SECRET_KEY` | - | Chave JWT |

## Comandos

```bash
# Iniciar worker de ingestão
celery -A src.ingestion.worker worker --loglevel=info

# Agendar crawler periódico
celery -A src.ingestion.worker beat --loglevel=info

# Executar crawler manual
python -c "import asyncio; from src.ingestion.tasks import crawl_public_pages; crawl_public_pages.delay()"

# Verificar status
curl http://localhost:8000/api/v1/health

# Testes
pytest tests/ -v
```

## API

### POST /api/v1/ask
Pergunta pública.

```json
{"question": "Qual o horário da Seção de Gestão de Pessoas?", "top_k": 10}
```

### POST /api/v1/documents/upload
Upload autenticado (requer token admin).

```bash
curl -X POST -H "Authorization: Bearer <token>" -F "file=@documento.pdf" http://localhost:8000/api/v1/documents/upload
```

### DELETE /api/v1/documents/{id}
Desativa documento (requer token admin).

### GET /api/v1/documents/{id}/history
Histórico de versões (requer token admin).

## Arquitetura

```
src/
├── api/            # FastAPI, rotas, autenticação, rate limit
├── common/         # Logging, exceções
├── config/         # Settings, modelos de configuração
├── conversation/   # Logs, clustering, FAQ, cache, analytics
├── graph/          # Driver, schema, entidades, proveniência, embeddings, extração, seed
├── ingestion/      # Crawler, detector, extrator, processador, worker, storage
├── retrieval/      # Search, traversal, hybrid, generation, safety, citations, source_status
└── main.py         # Entrypoint
```

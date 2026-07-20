## 1. Fundação do projeto

- [x] 1.1 Definir estrutura Python, configuração por ambiente, logging e tratamento de erros
- [x] 1.2 Provisionar Neo4j, PostgreSQL opcional, armazenamento de objetos e worker local para desenvolvimento
- [x] 1.3 Criar constraints, índices vetoriais e índices full-text do Neo4j
- [x] 1.4 Definir modelos de configuração para setores, tipos de fonte, estados e intervalo do crawler

## 2. Modelo de conhecimento

- [x] 2.1 Implementar entidades e relações institucionais com identificadores estáveis
- [x] 2.2 Implementar nós de fonte, documento, versão e chunk com metadados de proveniência
- [x] 2.3 Implementar armazenamento de embeddings e atualização idempotente de chunks
- [x] 2.4 Implementar extração estruturada de entidades e relações com validação de esquema e confiança
- [x] 2.5 Carregar a taxonomia inicial dos setores do ICT-SJC

## 3. Ingestão de fontes

- [x] 3.1 Implementar descoberta e coleta de páginas públicas de `ict.unesp.br`
- [x] 3.2 Implementar detecção de conteúdo inalterado, novas versões e páginas removidas
- [x] 3.3 Implementar extração de texto e metadados de páginas web
- [x] 3.4 Implementar processamento dos formatos de documentos aceitos
- [x] 3.5 Implementar fila de tarefas, retries, timeouts e execução periódica configurável
- [x] 3.6 Implementar armazenamento dos arquivos originais e referências no grafo

## 4. Recuperação GraphRAG

- [x] 4.1 Implementar busca vetorial e full-text sobre chunks
- [x] 4.2 Implementar traversal Cypher para entidades, setores, serviços e normas relacionadas
- [x] 4.3 Implementar recuperação híbrida com limites de profundidade e quantidade de contexto
- [x] 4.4 Implementar geração de respostas em português baseada somente no contexto recuperado
- [x] 4.5 Implementar resposta de insuficiência de evidência e proteção contra prompt injection

## 5. API e acesso

- [x] 5.1 Implementar endpoint público de perguntas e retorno estruturado de resposta e fontes
- [x] 5.2 Implementar autenticação e autorização para servidores
- [x] 5.3 Implementar endpoint autenticado de upload com validação de tipo, tamanho e integridade
- [x] 5.4 Implementar desativação, substituição e consulta do histórico de documentos
- [x] 5.5 Implementar auditoria de uploads, processamentos e alterações de estado
- [x] 5.6 Implementar rate limiting, limites de requisição e timeouts da API pública

## 6. Conversas e FAQ

- [x] 6.1 Implementar registro anônimo de perguntas, respostas, fontes e tempo de resposta
- [x] 6.2 Implementar agrupamento semântico de perguntas similares
- [x] 6.3 Implementar promoção automática a FAQ com limiar configurável
- [x] 6.4 Implementar cache de respostas FAQ com verificação de atualidade das fontes
- [x] 6.5 Implementar painel de análise de lacunas de cobertura e perguntas sem resposta

## 7. Citações e qualidade

- [x] 7.1 Implementar citações com URL ou referência documental, data e trecho de evidência
- [x] 7.2 Implementar estados de fonte ativa, indisponível, desatualizada e revogada
- [x] 7.3 Criar conjunto inicial de perguntas reais de funcionários e alunos
- [x] 7.4 Avaliar recuperação, precisão das citações, cobertura e respostas sem evidência
- [x] 7.5 Criar testes de regressão para ingestão, traversal, segurança e respostas

## 8. Operação e publicação

- [x] 8.1 Criar documentação de instalação, configuração e operação
- [x] 8.2 Criar health checks, métricas e logs de ingestão e consulta
- [x] 8.3 Configurar backups e restauração do Neo4j, PostgreSQL e arquivos originais
- [x] 8.4 Executar carga inicial controlada e validar fontes dos setores definidos
- [x] 8.5 Publicar API e interface com configuração segura de produção

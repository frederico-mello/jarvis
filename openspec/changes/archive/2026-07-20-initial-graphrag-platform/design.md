## Context

O ICT-SJC possui informações distribuídas entre páginas públicas, setores administrativos e acadêmicos, portarias, legislações e documentos operacionais. O sistema será público para consulta, mas somente servidores autorizados poderão enviar documentos. O conteúdo público do site será sincronizado em intervalos configuráveis.

O repositório está no início e não possui arquitetura ou dados legados. A solução precisa nascer como GraphRAG, em Python, com rastreabilidade das fontes e capacidade de evoluir sem exigir que toda pergunta seja respondida por uma consulta complexa ao grafo.

## Goals / Non-Goals

**Goals:**

- Qualquer funcionário ou aluno encontra resposta em menos de 30 segundos.
- Construir um grafo institucional com entidades, relações, chunks, embeddings e proveniência.
- Oferecer recuperação híbrida por vetor, texto completo e traversal do grafo.
- Ingerir páginas públicas do site e documentos enviados por servidores autorizados.
- Responder em português com citações, datas e indicação explícita de incerteza.
- Detectar alterações, versões, remoções e documentos revogados.
- Separar consulta pública de operações administrativas autenticadas.
- Registrar conversas anônimas para análise de melhoria contínua.
- Identificar automaticamente perguntas frequentes para reduzir reprocessamento.

**Non-Goals:**

- Indexar inicialmente áreas privadas ou autenticadas do site.
- Permitir upload público ou publicação sem autenticação.
- Substituir a fonte institucional por fatos inventados pelo modelo.
- Criar um agente autônomo com acesso irrestrito a sistemas externos.
- Implementar, na primeira versão, revisão humana obrigatória antes da publicação.
- Notificações push ou alertas para usuários sobre novos documentos.
- API pública para consumo por sistemas externos ao ICT.
- Aplicativo mobile nativo (a interface será web responsiva).
- Integração com sistemas internos do ICT (SIG, sistemas acadêmicos, RH) além do crawler do site público.
- Suporte multilíngue.

## Decisions

### Banco central: Neo4j

Neo4j será o banco principal para entidades, relações, documentos, chunks, embeddings e proveniência. Seus índices vetoriais e full-text permitem começar com um único sistema de recuperação, enquanto Cypher permite enriquecer resultados com relações institucionais.

Alternativas consideradas:

- PostgreSQL + pgvector: simples para RAG convencional, mas exige modelar e consultar o grafo fora do banco.
- Neo4j + Qdrant: pode escalar a busca vetorial, mas cria sincronização e operação duplicadas sem necessidade inicial.
- ArangoDB: alternativa válida, porém Neo4j possui integração e padrões mais maduros para GraphRAG em Python.

### Recuperação híbrida

Cada consulta poderá combinar busca vetorial, full-text e traversal. Termos exatos como número de portaria, artigo, sigla e nome de setor terão peso lexical; perguntas relacionais usarão o grafo; perguntas abertas usarão embeddings. Um reranker poderá ser adicionado após avaliação.

### Ingestão idempotente e versionada

Fontes serão identificadas por URL, identificador de documento ou hash. O pipeline SHALL evitar duplicatas, criar nova versão quando o conteúdo mudar e preservar a versão anterior para auditoria. Páginas removidas serão marcadas como indisponíveis, não apagadas imediatamente.

### Grafo com proveniência

Entidades e relações extraídas automaticamente deverão apontar para um ou mais chunks de origem, incluindo confiança, modelo de extração e data. O gerador só poderá usar fatos recuperados com fonte identificável.

### Separação de responsabilidades

FastAPI será responsável pela API; um worker agendado executará crawling e processamento; Neo4j armazenará o conhecimento; PostgreSQL poderá armazenar autenticação, auditoria e configurações; arquivos originais ficarão em armazenamento de objetos.

### Processamento automático com limites

LLMs poderão extrair entidades, relações, metadados e respostas, mas o pipeline deverá validar esquema, tamanho, tipos e referências. Conteúdo ingerido será tratado como dado, nunca como instrução para o modelo, para reduzir prompt injection.

### Registro anônimo de conversas

Cada pergunta e resposta será registrada sem identificação do usuário. O registro conterá pergunta anonimizada, resposta, fontes utilizadas, tempo de resposta e indicador de sucesso (resposta encontrada ou insuficiência). Estes dados alimentarão análise de melhoria contínua e identificação de perguntas frequentes.

### Identificação de perguntas frequentes

Perguntas semanticamente similares serão agrupadas automaticamente. Quando um grupo atingir um limiar configurável de recorrência, a pergunta e resposta poderão ser promovidas a FAQ, reduzindo reprocessamento e acelerando respostas para consultas comuns.

## Risks / Trade-offs

- **[Extração automática incorreta]** → preservar evidência, confiança e origem; não apresentar relações sem suporte.
- **[Legislação desatualizada ou revogada]** → versionar fontes, extrair datas e estados, e exibir a data de coleta.
- **[Custo e latência do GraphRAG]** → usar recuperação em etapas e limitar profundidade de traversal.
- **[Abuso da API pública]** → rate limiting, limites de tamanho, logs, timeouts e proteção de custos do modelo.
- **[Prompt injection em documentos ou páginas]** → separar instruções do contexto recuperado e validar saída estruturada.
- **[Licenciamento e operação do Neo4j]** → validar edição/licença para uso institucional antes do deploy de produção.
- **[Site com conteúdo renderizado por JavaScript]** → usar sitemap/API autorizada quando disponível e Playwright somente como fallback.

## Migration Plan

Não há migração de dados legados. O primeiro deploy deverá:

1. Provisionar Neo4j, autenticação administrativa, armazenamento de objetos e worker.
2. Criar constraints e índices do grafo.
3. Executar uma carga inicial limitada às páginas públicas e setores definidos.
4. Validar respostas, citações, versões e relações extraídas.
5. Habilitar o crawler periódico e a consulta pública gradualmente.

Em caso de rollback, desabilitar consulta pública e workers, preservar os dados capturados e retornar à versão anterior da API. O conteúdo original não deverá ser destruído durante rollback.

## Open Questions

- Qual provedor ou modelo de linguagem e embeddings será utilizado em produção?
- O Neo4j será autogerenciado no ICT ou hospedado em serviço gerenciado?
- Qual intervalo padrão do crawler e qual limite de páginas por execução?
- Quais formatos de arquivo serão aceitos no primeiro release?
- Qual mecanismo de autenticação estará disponível para servidores autorizados?

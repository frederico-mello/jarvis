## Why

Funcionários e alunos do ICT-SJC perdem tempo ligando para setores para obter informações que deveriam estar disponíveis institucionalmente. Cada ligação interrompe o trabalho de outro servidor, e quando a informação não é encontrada, o solicitante escala a busca para instâncias superiores até descobrir a resposta. O site institucional existe, mas a informação está dispersa entre páginas, portarias, legislações e documentos de diferentes setores, sem um ponto único de consulta.

## What Changes

- Criar um sistema público de perguntas e respostas em português sobre o ICT-SJC.
- Qualquer funcionário ou aluno poderá perguntar e receber resposta em menos de 30 segundos.
- As respostas serão fundamentadas exclusivamente em fontes institucionais, com citações verificáveis.
- Servidores autorizados poderão enviar documentos para manter o conhecimento atualizado.
- Páginas públicas do site institucional serão sincronizadas automaticamente em intervalos regulares.
- Conversas anônimas serão registradas para análise de melhoria contínua.
- Perguntas frequentes serão identificadas automaticamente para reduzir reprocessamento.

## Capabilities

### New Capabilities

- `public-question-answering`: perguntas públicas em português com respostas fundamentadas em fontes institucionais.
- `knowledge-graph`: modelo do conhecimento institucional com entidades, relações e proveniência entre setores, serviços, pessoas, documentos e normas.
- `source-ingestion`: coleta periódica de páginas públicas e processamento de documentos enviados por servidores autorizados.
- `authorized-document-upload`: upload autenticado com auditoria, versionamento e desativação de documentos.
- `source-citations`: citações verificáveis com metadados de origem, data e indicação de ausência de evidência.
- `conversation-logs`: registro anônimo de perguntas e respostas para análise de uso e melhoria do sistema.
- `faq-discovery`: identificação automática de perguntas frequentes para reduzir reprocessamento e acelerar respostas.

### Modified Capabilities

Nenhuma. O repositório não possui especificações existentes.

## Non-Goals

- Notificações push ou alertas para usuários sobre novos documentos.
- API pública para consumo por sistemas externos ao ICT.
- Aplicativo mobile nativo (a interface será web responsiva).
- Integração com sistemas internos do ICT (SIG, sistemas acadêmicos, RH) além do crawler do site público.
- Suporte multilíngue.
- Moderação humana de respostas antes da exibição ao usuário.

## Impact

- A comunidade do ICT-SJC ganha um novo canal de consulta unificado, reduzindo ligações e interrupções entre setores.
- Servidores autorizados precisarão aprender a operar o upload e a desativação de documentos.
- O setor de TI operará e manterá o sistema, incluindo crawler, indexação e atualização de fontes.
- O site institucional será acessado periodicamente por crawler para sincronização de conteúdo público.
- O sistema será público, exigindo proteções contra abuso, conteúdo malicioso em fontes e exposição de dados não autorizados.

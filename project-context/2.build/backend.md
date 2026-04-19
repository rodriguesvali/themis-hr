# Themis HR
## Backend Handoff

Data: 2026-04-19
Responsável alvo: `@backend-eng`
Status: brief inicial do bootstrap; deve ser atualizado in place conforme o backend for implementado.

## Mission

Implementar o backend do MVP do Themis HR com:

- FastAPI
- CrewAI
- persistência mínima
- Alembic

## Inputs

- `project-context/1.define/prd.md`
- `project-context/1.define/sad.md`
- `project-context/2.build/setup.md`
- `CONTEXT.md`

## Scope

### In Scope

- scaffold do backend FastAPI
- estrutura de orquestração do CrewAI
- configuração mínima de persistência
- versionamento de schema com Alembic
- endpoints mínimos do MVP

### Out of Scope

- integrações externas além do escopo do MVP
- analytics avançados
- automações fora do fluxo principal de atendimento
- expansão do banco além do mínimo necessário

## Required Outcomes

- estrutura de projeto backend coerente com o SAD
- endpoint de healthcheck
- endpoint inicial de conversa
- configuração inicial de sessions/persistência
- configuração explícita de migrations
- documentação de decisões em `project-context/2.build/backend.md`

## MVP Persistence Boundary

Persistir somente:

- conversa
- mensagem
- classificação principal
- evento de escalonamento
- referência de conhecimento

## CrewAI Expectations

- agents e tasks preferencialmente orientados a arquivo
- fluxo sequencial no MVP
- separação clara entre intake, classificação, conhecimento, resposta, sentimento e escalonamento

## Open Questions to Resolve During Implementation

- SQLite ou PostgreSQL já no primeiro run funcional
- provider/model inicial do runtime multiagente
- formato final da camada de retrieval no MVP

## Deliverable

Atualizar este arquivo com:

### Decisões de implementação
- A stack do backend foi montada usando FastAPI, SQLAlchemy 2.0 e Alembic.
- O banco escolhido para o primeiro `run` já foi o PostgreSQL conectado via `psycopg`, pois o `.devcontainer` já prove o banco pronto, economizando tempo de refatoração do SQLite futuramente.
- A estrutura de módulos foi padronizada (`api`, `core`, `db`, `models`, `schemas`, `services`, `orchestration`, `knowledge`).
- Tabelas iniciais (`conversations` e `messages`) foram criadas e as migrações aplicadas.
- Endpoints MOCK (`/health`, `POST /api/v1/conversations`, `GET /api/v1/conversations/{id}`) criados no `main.py`.

### Estrutura Criada
O backend está encapsulado na pasta `backend/src/themis_hr_api`. O Alembic está gerenciando os scripts em `backend/alembic`. Dependências listadas em `backend/requirements.txt`.

### Gaps conhecidos
- O `POST /api/v1/conversations` ainda devolve uma string de resposta estática. A integração real com a lib do `crewai` não foi acoplada ao endpoint.
- O Provider/Modelo para LLM está mockado no `.env.example` usando OpenAI, requer chaves reais no ambiente final para quando CrewAI for ligado.

### Próximos passos
- (Para a fase de Integração/Desenvolvimento profundo) Substituir o *mock* do bot_reply no `main.py` por uma chamada real à pipeline CrewAI construindo os agentes (Intake, Classification, etc).
- Assumir a persona do `@frontend-eng` para estruturar a tela do chat Angular que consome estes endpoints.

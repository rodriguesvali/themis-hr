# Themis HR
## Setup Phase

Data: 2026-04-19
Responsável: `@project-mgr`
Status: **Concluído**. Estrutura base de diretórios e arquivos de ambiente (`.env.example`) criados com sucesso. Prontos para handoff aos engenheiros.

## Objective

Preparar a estrutura inicial do projeto para permitir o desenvolvimento do MVP do Themis HR com:

- frontend Angular;
- PrimeNG com preset Nora;
- backend FastAPI;
- orquestração de agentes com CrewAI;
- persistência relacional mínima com Alembic.

## Scope of This Phase

Esta fase cobre:

- organização do workspace;
- definição de diretórios principais;
- arquivos-base de ambiente;
- manifests iniciais de backend e frontend;
- convenções de desenvolvimento;
- preparação para evolução do banco e do runtime dos agentes;
- documentação de handoff para os agentes que executarão a implementação depois, dentro do Dev Container.

Esta fase não cobre:

- implementação funcional do chat;
- implementação completa dos agentes de negócio;
- integração real com base de conhecimento;
- interfaces finais de usuário.

## Important Note for This Stage

Neste momento, o objetivo principal é **preparar contexto, convenções e handoffs**.

- a implementação do produto será conduzida depois, no Dev Container;
- os agentes do GitHub Copilot devem usar este material como base de execução;
- qualquer scaffold técnico criado antes desta decisão deve ser tratado apenas como referência inicial, não como início obrigatório da implementação final.

## Workspace Structure

A estrutura abaixo descreve o alvo do workspace após o setup. Os diretórios principais (`backend/`, `frontend/`, `infra/`) e arquivos de base (`.env.example`) já foram criados.

```text
themis-hr/
├── backend/
│   ├── src/themis_hr_api/
│   ├── tests/
│   └── README.md
├── frontend/
│   ├── src/
│   └── README.md
├── infra/
│   └── README.md
├── project-context/
│   ├── 1.define/
│   ├── 2.build/
│   └── 3.deliver/
├── .devcontainer/
├── .env.example
├── .editorconfig
└── README.md
```

## Environment Strategy

### Dev Environment

- desenvolvimento principal via Dev Container;
- serviço PostgreSQL disponível via Compose;
- suporte a SQLite para experimentação local do backend, quando necessário.

### Environment Variables

Arquivo base: `.env.example`

Variáveis mínimas definidas:

- `APP_ENV`
- `BACKEND_PORT`
- `FRONTEND_PORT`
- `DATABASE_URL`
- `CREWAI_MODEL`
- `CREWAI_PROVIDER`
- `KNOWLEDGE_BASE_PATH`
- `LOG_LEVEL`

## Backend Setup Decisions

### Stack

- Python 3.12
- FastAPI
- SQLAlchemy 2.x
- Alembic
- CrewAI
- CrewAI Tools
- Uvicorn

### Packaging

- projeto Python isolado em `backend/`
- código-fonte em `backend/src/themis_hr_api/`
- testes em `backend/tests/`

### Initial Backend Modules

- `main.py` para boot da API
- `config.py` para settings
- `api/` para routers
- `db/` para engine/session
- `models/` para entidades persistidas
- `schemas/` para DTOs
- `services/` para casos de uso
- `orchestration/` para integração com CrewAI
- `knowledge/` para retrieval adapters

## Frontend Setup Decisions

### Stack

- Angular
- PrimeNG
- preset Nora
- TypeScript

### Initial Frontend Direction

O frontend nascerá em `frontend/` e deverá evoluir com:

- shell principal da aplicação;
- feature de helpdesk;
- services para comunicação com backend;
- base visual centralizada em PrimeNG;
- customização progressiva via design tokens.

## Database Strategy

### MVP Persistence

Persistência mínima prevista:

- sessões de conversa;
- mensagens;
- classificação principal;
- evento de escalonamento;
- referências de conhecimento;

### Migration Strategy

- Alembic como ferramenta única de versionamento;
- migration inicial assim que os primeiros modelos forem definidos;
- caminho claro de SQLite para PostgreSQL, se necessário.

## Commands Planned for Next Steps

### Backend

```bash
cd backend
python -m venv .venv
pip install -e .
```

### Frontend

```bash
cd frontend
npm install
```

### Dev Container

```bash
Dev Containers: Rebuild and Reopen in Container
```

## Risks and Notes

- As pastas `frontend/` e `backend/` foram inicializadas vazias/minimamente. O Scaffold Angular e o empacotamento do FastAPI/CrewAI ocorrerão nas etapas seguintes.
- Os manifests criados agora são base inicial e poderão ser refinados pelos próximos agentes.
- O projeto ainda não define o provider final de LLM (padrão assumido local: `gpt-4o-mini` via OpenAI no `.env.example`).
- A estratégia exata de knowledge base será detalhada na fase de backend/orquestração.

## Next Handoffs

- `@backend-eng`: scaffold técnico do backend FastAPI + Alembic + CrewAI
- `@frontend-eng`: scaffold Angular + PrimeNG/Nora
- `@integration-eng`: ligação frontend ↔ backend após existência dos dois lados
- `@qa-eng`: validação funcional do MVP após integração mínima

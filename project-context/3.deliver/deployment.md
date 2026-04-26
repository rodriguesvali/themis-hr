# Themis HR
## Deployment

Data: 2026-04-26
Responsável: DevOps / Deliver
Status: guia de demonstração local; não representa produção.

## Environment

Ambiente atual suportado:

- Dev Container do repositório;
- frontend Angular na porta `4200`;
- backend FastAPI na porta `8000`;
- PostgreSQL via Docker Compose na porta `5432`;
- LLM provider Google/Gemini via CrewAI;
- PDF local da CLT em `backend/docs/consolidacao_leis_trabalho.pdf`.

## Configuration

Usar `.env.example` como contrato de variáveis, preenchendo segredos fora do versionamento.

Valores críticos:

- `DATABASE_URL=postgresql://themis:themis@postgres:5432/themis_db` no Dev Container;
- `CREWAI_PROVIDER=google`;
- `CREWAI_MODEL` com modelo Gemini compatível;
- `GOOGLE_API_KEY` configurada no ambiente local;
- `CLT_PDF_PATH` quando o caminho padrão não for usado.

## Steps

1. Reabrir o projeto no Dev Container.
2. Instalar dependências se necessário:
   - backend: ambiente Python do projeto;
   - frontend: `npm install` em `frontend/`.
3. Aplicar migrations do backend com Alembic.
4. Iniciar FastAPI com Uvicorn na porta `8000`.
5. Iniciar Angular com `npm start` em `frontend/`.
6. Validar `GET http://localhost:8000/health`.
7. Validar chat em `http://localhost:4200/`.

## Access

- Frontend: `http://localhost:4200`
- Backend: `http://localhost:8000`
- Healthcheck: `http://localhost:8000/health`
- Banco: PostgreSQL interno ao Compose/dev container

Não usar dados reais de colaboradores neste estágio.

## Rollback

- Parar os processos locais.
- Remover/recriar banco local se a migration ou dados ficarem inconsistentes.
- Reaplicar migrations até o head conhecido.
- Reverter mudanças de configuração local.

## Open Questions

- Qual será a topologia de staging?
- Haverá frontend servido estaticamente por infraestrutura separada ou junto a um gateway?
- Como serão gerenciadas chaves LLM no ambiente alvo?

## Audit

- Criado por Codex em 2026-04-26.

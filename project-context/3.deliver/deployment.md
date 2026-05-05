# Themis HR
## Deployment

Data: 2026-05-05
Responsável: DevOps / Deliver
Status: guia de demonstração local repetível; não representa produção.

## Environment

Ambiente atual suportado:

- Dev Container do repositório;
- frontend Angular na porta `4200`;
- backend FastAPI na porta `8000`;
- PostgreSQL via Docker Compose na porta `5432`;
- LLM provider Google/Gemini via CrewAI;
- PDF local da CLT em `backend/docs/consolidacao_leis_trabalho.pdf`.
- dados exclusivamente fictícios para smoke e apresentação.

## Configuration

Usar `.env.example` como contrato de variáveis, preenchendo segredos fora do versionamento.

Valores críticos:

- `DATABASE_URL=postgresql://themis:themis@postgres:5432/themis_db` no Dev Container;
- `CREWAI_PROVIDER=google`;
- `CREWAI_MODEL` com modelo Gemini compatível;
- `GOOGLE_API_KEY` configurada no ambiente local como chave canônica da demo;
- `GEMINI_API_KEY` aceito apenas como fallback legado quando `GOOGLE_API_KEY` estiver ausente;
- `CLT_PDF_PATH` quando o caminho padrão não for usado.

Não configurar `GOOGLE_API_KEY` e `GEMINI_API_KEY` simultaneamente para a demo. Se ambas existirem, o backend registra warning e usa `GOOGLE_API_KEY`.

## Steps

1. Reabrir o projeto no Dev Container.
2. Instalar dependências se necessário:
   - backend: ambiente Python do projeto;
   - frontend: `npm install` em `frontend/`.
3. Aplicar migrations do backend com Alembic.
4. Confirmar o head: `.venv/bin/alembic current` em `backend/` deve retornar `8b9f2d4c1a3e (head)`.
5. Iniciar FastAPI com Uvicorn na porta `8000`.
6. Iniciar Angular com `npm start` em `frontend/`.
7. Validar `GET http://localhost:8000/health`.
8. Validar chat em `http://localhost:4200/` com pergunta fictícia comum.
9. Validar escalonamento com caso fictício sensível.
10. Parar temporariamente o backend e validar fallback visual do chat.

## Demo Script

1. Abrir `http://localhost:4200/`.
2. Enviar: "Tenho 15 dias de ferias vencidas. Como devo solicitar o descanso?"
3. Confirmar que a Themis responde ou faz handoff controlado para RH.
4. Enviar: "Quero denunciar assedio moral recorrente do meu gestor e tenho medo de retaliacao."
5. Confirmar que a conversa é escalada para atendimento humano.
6. Com o backend parado, enviar uma nova mensagem fictícia.
7. Confirmar que o fallback visual aparece e o estado "Themis está digitando..." não fica preso.

## Access

- Frontend: `http://localhost:4200`
- Backend: `http://localhost:8000`
- Healthcheck: `http://localhost:8000/health`
- Banco: PostgreSQL interno ao Compose/dev container

Não usar dados reais de colaboradores neste estágio.

## Troubleshooting

- Backend não sobe: revisar `DATABASE_URL`, porta `8000` e logs do Uvicorn.
- Alembic falha: confirmar PostgreSQL acessível e reaplicar migrations em base local limpa.
- LLM falha: confirmar `CREWAI_PROVIDER`, `CREWAI_MODEL` e uma única chave LLM válida.
- Frontend não conecta: validar `environment.apiUrl`, CORS e disponibilidade do backend.
- Chat fica lento: aguardar processamento síncrono do CrewAI; latência segue risco residual do MVP.

## Rollback

- Parar os processos locais.
- Remover/recriar banco local se a migration ou dados ficarem inconsistentes.
- Reaplicar migrations até o head conhecido.
- Reverter mudanças de configuração local.

## Open Questions

- Qual será a topologia de staging?
- Haverá frontend servido estaticamente por infraestrutura separada ou junto a um gateway?
- Como serão gerenciadas chaves LLM no ambiente alvo fora da demo local?

## Audit

- Criado por Codex em 2026-04-26.
- Atualizado por Codex em 2026-05-05 para roteiro repetível de demonstração local.

# Themis HR
## Release Readiness

Data: 2026-05-05
Responsável: consolidação Deliver / DevOps
Status: pronto para demonstração local controlada e repetível; não aprovado para produção.

## Version / Change Set

Escopo validado localmente:

- frontend Angular 21 com PrimeNG 21, preset Nora, chat principal e rota administrativa inicial;
- backend FastAPI com `/health`, `POST /api/v1/conversations` e `GET /api/v1/conversations/{conversation_id}`;
- persistência mínima de conversas e mensagens com SQLAlchemy e Alembic;
- orquestração CrewAI em fluxo condicional: `principal_agent`, especialista sob demanda e `legal_reviewer_agent`;
- consulta textual ao PDF local da CLT em `backend/docs/consolidacao_leis_trabalho.pdf`;
- metadados jurídicos persistidos em `messages`;
- fallback visual no chat quando o backend está indisponível;
- configuração LLM com `GOOGLE_API_KEY` como chave canônica e `GEMINI_API_KEY` apenas como fallback legado;
- artefatos AAMAD Codex-native recriados em `.codex/aamad/`.

## Verification Summary

Evidências consolidadas em `project-context/3.deliver/release-evidence.md`:

- testes unitários backend: `backend/.venv/bin/python -m unittest discover -s backend/tests` com 7 testes OK;
- testes unitários frontend: `npm test -- --watch=false` em `frontend/` com 3 testes OK;
- build frontend: `npm run build` em `frontend/`;
- smoke de healthcheck via FastAPI `TestClient` e `curl`;
- Alembic no head `8b9f2d4c1a3e`;
- round-trip real via backend com CrewAI/Gemini;
- escalonamento real para caso sensível;
- round-trip browser via Playwright em `http://localhost:4200/`;
- fallback browser via Playwright com backend indisponível.

## Deployment Steps

Para demonstração local:

1. Abrir no Dev Container ou ambiente equivalente.
2. Garantir PostgreSQL acessível via `DATABASE_URL`.
3. Aplicar migrations Alembic no backend e confirmar `8b9f2d4c1a3e (head)`.
4. Configurar uma chave LLM válida por variável de ambiente, preferencialmente `GOOGLE_API_KEY`.
5. Iniciar backend em `http://localhost:8000`.
6. Iniciar frontend em `http://localhost:4200`.
7. Executar smoke: `/health`, pergunta fictícia comum, caso fictício sensível e fallback com backend indisponível.

## Configuration

Variáveis esperadas:

- `APP_ENV`
- `BACKEND_PORT`
- `FRONTEND_PORT`
- `DATABASE_URL`
- `CREWAI_MODEL`
- `CREWAI_PROVIDER`
- `GOOGLE_API_KEY`
- `GEMINI_API_KEY` somente como fallback legado quando `GOOGLE_API_KEY` estiver ausente
- `KNOWLEDGE_BASE_PATH`
- `CLT_PDF_PATH`
- `LOG_LEVEL`

Para a demonstração, evitar configurar `GOOGLE_API_KEY` e `GEMINI_API_KEY` simultaneamente. Se ambas existirem, o backend registra warning e usa `GOOGLE_API_KEY`.

## Go / No-Go

Go para demo local quando:

- backend tests, frontend tests e build frontend passam;
- Alembic está no head;
- `/health` retorna HTTP 200;
- pergunta comum renderiza resposta ou handoff controlado;
- caso sensível retorna escalonamento;
- fallback visual aparece quando o backend está indisponível;
- não há dados reais de colaboradores.

No-go quando qualquer item acima falhar, quando a chave LLM estiver ausente/inválida, ou quando a demo exigir staging, produção, dados reais ou parecer jurídico conclusivo.

## Monitoring

Monitoramento mínimo para demo:

- logs do backend;
- status HTTP do `/health`;
- status das conversas persistidas;
- eventos de escalonamento;
- risco jurídico e status de revisão nos metadados da mensagem.

## Rollback

Para demo local, rollback significa:

- parar frontend/backend;
- reverter variáveis para `.env.example`;
- restaurar banco local ou reaplicar migrations em base limpa;
- voltar para o último commit conhecido se mudanças futuras quebrarem o MVP.

## Approvals

- Aprovado somente para demonstração local controlada.
- Produção, staging compartilhado ou demo com dados reais exigem novo gate de segurança, dados e operação.

## Sources

- `project-context/3.deliver/release-evidence.md`
- `project-context/2.build/qa.md`
- `project-context/2.build/integration.md`
- `backend/src/themis_hr_api/core/config.py`
- `backend/src/themis_hr_api/main.py`
- `backend/src/themis_hr_api/orchestration/crew.py`
- `frontend/src/app/chat.service.ts`

## Audit

- Criado por Codex em 2026-04-26 durante recriação da configuração AAMAD Codex-native.
- Atualizado por Codex em 2026-05-05 para fechar readiness de demonstração local.

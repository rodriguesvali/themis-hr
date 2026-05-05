# Themis HR
## Operations

Data: 2026-05-05
Responsável: DevOps / Operação técnica
Status: guia operacional de demonstração local.

## Runtime

Componentes em runtime:

- Angular em desenvolvimento local;
- FastAPI com endpoint de conversa;
- PostgreSQL com schema Alembic;
- CrewAI executando classificação, especialista sob demanda e revisão jurídica;
- ferramenta local de busca textual em PDF da CLT;
- bases mockadas por área em `backend/src/themis_hr_api/knowledge/`;
- fallback visual no frontend para indisponibilidade do backend.

## Monitoring

Métricas e sinais mínimos:

- disponibilidade de `/health`;
- taxa de erro em `POST /api/v1/conversations`;
- tempo de resposta percebido do chat;
- número de conversas `active` versus `escalated`;
- `confidence`, `legal_reviewed`, `legal_risk_level` e `escalation_reason`;
- falhas na leitura/consulta do PDF da CLT.
- warnings de configuração LLM, especialmente dupla definição de `GOOGLE_API_KEY` e `GEMINI_API_KEY`.

## Alerts

Alertas futuros recomendados:

- backend indisponível;
- banco indisponível;
- falha de credencial LLM;
- configuração simultânea de `GOOGLE_API_KEY` e `GEMINI_API_KEY`;
- latência acima do limite definido para demo/piloto;
- aumento anormal de escalonamentos por categoria;
- falhas recorrentes da revisão jurídica automática.

## Runbooks

Runbooks mínimos para demo local:

- reiniciar backend: parar Uvicorn e iniciar novamente na porta `8000`;
- reiniciar frontend: parar `npm start` e iniciar novamente na porta `4200`;
- validar chave LLM: manter `GOOGLE_API_KEY` como canônica e remover `GEMINI_API_KEY` salvo fallback legado;
- aplicar e diagnosticar migrations Alembic: executar `.venv/bin/alembic current` em `backend/`;
- resetar banco local de demonstração quando dados de smoke ficarem inconsistentes;
- diagnosticar falha de CORS confirmando frontend em `http://localhost:4200`;
- diagnosticar erro de consulta ao PDF da CLT confirmando `CLT_PDF_PATH`;
- validar fallback visual parando temporariamente o backend e enviando mensagem fictícia no chat.

## Ownership

- Produto/escopo: `@product-mgr`
- Arquitetura: `@system-arch`
- Backend/runtime CrewAI: `@backend-eng`
- Frontend Angular/PrimeNG: `@frontend-eng`
- Integração ponta a ponta: `@integration-eng`
- QA e riscos residuais: `@qa-eng`
- Deploy/operação: DevOps/Deliver

## Known Gaps

- Sem observabilidade estruturada de produção.
- Sem autenticação ou autorização real.
- Sem fila/SSE/WebSocket para chamadas longas.
- Sem tabela própria para evidências jurídicas e tool calls.
- Sem runbook validado em staging.
- Sem métricas persistidas de latência ou taxa de erro.

## Audit

- Criado por Codex em 2026-04-26.
- Atualizado por Codex em 2026-05-05 após validação de readiness da demo local.

# Themis HR
## Operations

Data: 2026-04-26
Responsável: DevOps / Operação técnica
Status: guia operacional inicial para MVP local.

## Runtime

Componentes em runtime:

- Angular em desenvolvimento local;
- FastAPI com endpoint de conversa;
- PostgreSQL com schema Alembic;
- CrewAI executando classificação, especialista sob demanda e revisão jurídica;
- ferramenta local de busca textual em PDF da CLT;
- bases mockadas por área em `backend/src/themis_hr_api/knowledge/`.

## Monitoring

Métricas e sinais mínimos:

- disponibilidade de `/health`;
- taxa de erro em `POST /api/v1/conversations`;
- tempo de resposta percebido do chat;
- número de conversas `active` versus `escalated`;
- `confidence`, `legal_reviewed`, `legal_risk_level` e `escalation_reason`;
- falhas na leitura/consulta do PDF da CLT.

## Alerts

Alertas futuros recomendados:

- backend indisponível;
- banco indisponível;
- falha de credencial LLM;
- latência acima do limite definido para demo/piloto;
- aumento anormal de escalonamentos por categoria;
- falhas recorrentes da revisão jurídica automática.

## Runbooks

Runbooks mínimos a criar antes de staging:

- reiniciar backend/frontend local;
- validar chave LLM e provider;
- aplicar e diagnosticar migrations Alembic;
- resetar banco local de demonstração;
- diagnosticar falha de CORS;
- diagnosticar erro de consulta ao PDF da CLT.

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

## Audit

- Criado por Codex em 2026-04-26.

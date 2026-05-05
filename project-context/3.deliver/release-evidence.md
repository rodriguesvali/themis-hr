# Themis HR
## Release Evidence

Data: 2026-05-05
Responsável alvo: consolidação de entrega
Status: pronto para demonstração local controlada e repetível; não aprovado para produção.

## Objective

Consolidar as evidências de entrega do MVP local do Themis HR após Define, Architecture, Build, Integration e Validation.

## Scope

### In Scope

- registrar estado atual do MVP local;
- consolidar validações automatizadas executadas;
- identificar riscos residuais para demonstração ou rollout;
- definir próximos gates de validação.

### Out of Scope

- declarar produção ou rollout externo;
- validar conformidade jurídica completa;
- executar testes de performance, segurança ou carga;
- validar provider LLM em ambiente remoto.

## Delivery Status

O projeto concluiu o gate de Delivery/readiness para demonstração local controlada.

O MVP local possui:

- frontend Angular com PrimeNG/Nora;
- tela de chat e rota administrativa inicial;
- integração HTTP do chat via `ChatService`;
- backend FastAPI com `/health`, `POST /api/v1/conversations` e `GET /api/v1/conversations/{conversation_id}`;
- persistência mínima de conversas e mensagens;
- orquestração CrewAI em modelo principal + especialista sob demanda;
- revisão jurídica automática apoiada por consulta textual ao PDF local da CLT;
- testes unitários cobrindo o fluxo de revisão jurídica;
- fallback visual do chat para backend indisponível;
- configuração LLM com `GOOGLE_API_KEY` como chave canônica e `GEMINI_API_KEY` apenas como fallback legado.

## Evidence

### Automated Validation

- **Backend unit tests:** `backend/.venv/bin/python -m unittest discover -s backend/tests`
  - Resultado: 5 testes executados, todos OK.
- **Frontend production build:** `npm run build` em `frontend/`
  - Resultado: build concluído e artefatos gerados em `frontend/dist/frontend`.
- **API health smoke test:** FastAPI `TestClient` em `GET /health`
  - Resultado: HTTP 200 com `{"status": "ok", "app_env": "development"}`.
- **Alembic runtime check:** `alembic current`
  - Resultado: banco PostgreSQL acessível e no head `8b9f2d4c1a3e`.
- **Backend real conversation smoke:** `POST /api/v1/conversations`
  - Resultado: HTTP 200, conversa `49`, status `active`, resposta gerada por CrewAI/Gemini com revisão jurídica.
  - Persistência confirmada: mensagem da Themis com categoria `Férias e Licenças`, especialista `ferias`, confiança `media`, `legal_reviewed = true` e risco jurídico `baixo`.
- **Escalation smoke:** `POST /api/v1/conversations`
  - Mensagem: denúncia de assédio moral.
  - Resultado: HTTP 200, conversa `50`, status `escalated`, resposta de encaminhamento humano.
- **Browser round-trip:** Playwright Chromium em `http://localhost:4200/`
  - Resultado: tela carregou, mensagem enviada pelo chat, estado "Themis está digitando..." exibido e resposta final renderizada na UI.
  - Persistência confirmada: conversa `52`, `user_id = 1`, status `active`, categoria `Férias e Licenças`, especialista `ferias`, confiança `media`, `legal_reviewed = true`, risco jurídico `baixo`.

### Artifact Validation

- `project-context/2.build/backend.md` registra a implementação do CrewAI, especialistas, revisão jurídica e metadados persistidos.
- `project-context/2.build/frontend.md` registra Angular 21, PrimeNG 21, Nora, rotas `chat` e `admin`, e remoção do Tailwind.
- `project-context/2.build/integration.md` foi atualizado para refletir que o endpoint atual aciona CrewAI, não apenas resposta mockada.
- `project-context/2.build/qa.md` foi atualizado com evidências de 2026-04-25 e limitações de validação runtime.

### Readiness Validation em 2026-05-05

- **Backend unit tests:** `backend/.venv/bin/python -m unittest discover -s backend/tests`
  - Resultado: 7 testes executados, todos OK.
  - Cobertura adicionada: precedência de `GOOGLE_API_KEY` sobre `GEMINI_API_KEY` e fallback legado quando apenas `GEMINI_API_KEY` existe.
- **Frontend unit tests:** `npm test -- --watch=false` em `frontend/`
  - Resultado: 2 arquivos de teste, 3 testes executados, todos OK.
  - Cobertura adicionada: erro HTTP no `ChatService` renderiza fallback compreensível e limpa o estado de digitação.
- **Frontend production build:** `npm run build` em `frontend/`
  - Resultado: build concluído e artefatos gerados em `frontend/dist/frontend`.
- **Alembic runtime check:** `.venv/bin/alembic current` em `backend/`
  - Resultado: banco PostgreSQL acessível e no head `8b9f2d4c1a3e`.
- **API health smoke:** `curl http://localhost:8000/health`
  - Resultado: HTTP 200 com `{"status":"ok","app_env":"development"}`.
- **Backend real conversation smoke:** `POST /api/v1/conversations`
  - Mensagem fictícia: solicitação de 15 dias de férias vencidas.
  - Resultado: HTTP 200, conversa `55`, status `escalated`, com resposta de handoff para RH por ausência de procedimento operacional interno na base.
- **Escalation smoke:** `POST /api/v1/conversations`
  - Mensagem fictícia: denúncia de assédio moral com medo de retaliação.
  - Resultado: HTTP 200, conversa `56`, status `escalated`, com handoff humano.
- **Browser round-trip:** Playwright Chromium em `http://localhost:4200/`
  - Resultado: tela carregou, mensagem enviada pelo chat, estado "Themis está digitando..." exibido e resposta final renderizada.
- **Browser backend-failure fallback:** Playwright Chromium com backend indisponível
  - Resultado: fallback visual "Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente mais tarde." renderizado e indicador de digitação ausente ao final.
- **Configuração LLM:** backend normaliza o runtime para `GOOGLE_API_KEY` como chave canônica.
  - Resultado: `GEMINI_API_KEY` permanece fallback legado quando `GOOGLE_API_KEY` está ausente; quando ambas existem, o backend registra warning e usa `GOOGLE_API_KEY`.

## Release Decision

**Decisão:** aprovado para demonstração local controlada e repetível, não para produção.

O MVP foi validado em ambiente local com frontend, backend, PostgreSQL, CrewAI/Gemini e revisão jurídica. Para repetir a demonstração, o ambiente precisa manter:

- banco disponível e migrations aplicadas;
- variáveis de ambiente revisadas;
- uma única chave LLM válida configurada, preferencialmente `GOOGLE_API_KEY`;
- backend em `http://localhost:8000`;
- frontend em `http://localhost:4200`.

## Residual Risks

- O endpoint de conversa executa CrewAI de forma síncrona; chamadas com LLM podem ultrapassar o tempo aceitável de resposta.
- O fluxo completo com LLM real foi validado localmente, mas ainda não foi medido sob carga, concorrência ou ambiente staging.
- O frontend ainda não recupera histórico após reload, apesar do backend expor endpoint de consulta.
- A auditoria jurídica detalhada ainda não persiste os trechos exatos recuperados da CLT em tabela própria.
- Casos trabalhistas ambíguos ou sensíveis devem continuar escalando para humano.

## Next Gates

1. Repetir o fluxo em staging, quando existir.
2. Medir latência real do endpoint de conversa com LLM sob cenários controlados.
3. Definir se a próxima iteração resolve histórico de chat ou processamento assíncrono primeiro.
4. Definir requisitos mínimos de LGPD/security review antes de demonstração com dados reais.

## Sources

- `CONTEXT.md`
- `project-context/1.define/prd.md`
- `project-context/1.define/sad.md`
- `project-context/2.build/setup.md`
- `project-context/2.build/frontend.md`
- `project-context/2.build/backend.md`
- `project-context/2.build/integration.md`
- `project-context/2.build/qa.md`
- `backend/src/themis_hr_api/main.py`
- `backend/src/themis_hr_api/core/config.py`
- `backend/src/themis_hr_api/orchestration/crew.py`
- `backend/tests/test_config.py`
- `backend/tests/test_legal_review.py`
- `frontend/src/app/chat.service.ts`
- `frontend/src/app/chat.service.spec.ts`
- Execução local de `alembic current` em 2026-04-25.
- Execução local de `curl` para `/health` e `POST /api/v1/conversations` em 2026-04-25.
- Execução local de Playwright Chromium contra `http://localhost:4200/` em 2026-04-25.
- Execução local de testes, build, Alembic, curl e Playwright Chromium em 2026-05-05.

## Assumptions

- Adapter ativo: `crewai`.
- O ambiente de demonstração usa as mesmas portas padrão: frontend `4200`, backend `8000`.
- As credenciais LLM serão fornecidas via variáveis de ambiente, nunca versionadas.
- O gate atual continua limitado a demonstração local controlada com dados fictícios.

## Open Questions

- Qual provider/modelo LLM será o padrão oficial do MVP?
- A próxima etapa deve priorizar processamento assíncrono ou histórico de conversa na UI?
- Haverá requisito mínimo de auditoria jurídica antes da primeira demonstração para stakeholders?

## Audit

- Criado por Codex em 2026-04-25.
- Baseado em inspeção local, testes automatizados e atualização dos artefatos de QA e integração.
- Atualizado por Codex em 2026-05-05 para fechar Delivery/readiness de demonstração local.

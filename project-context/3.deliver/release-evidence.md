# Themis HR
## Release Evidence

Data: 2026-04-25
Responsável alvo: consolidação de entrega
Status: pronto para gate de demonstração local, com ressalvas explícitas.

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

O projeto está no fechamento do Module 6: Validation e entrou na etapa Deliver.

O MVP local possui:

- frontend Angular com PrimeNG/Nora;
- tela de chat e rota administrativa inicial;
- integração HTTP do chat via `ChatService`;
- backend FastAPI com `/health`, `POST /api/v1/conversations` e `GET /api/v1/conversations/{conversation_id}`;
- persistência mínima de conversas e mensagens;
- orquestração CrewAI em modelo principal + especialista sob demanda;
- revisão jurídica automática apoiada por consulta textual ao PDF local da CLT;
- testes unitários cobrindo o fluxo de revisão jurídica.

## Evidence

### Automated Validation

- **Backend unit tests:** `backend/.venv/bin/python -m unittest discover -s backend/tests`
  - Resultado: 5 testes executados, todos OK.
- **Frontend production build:** `npm run build` em `frontend/`
  - Resultado: build concluído e artefatos gerados em `frontend/dist/frontend`.
- **API health smoke test:** FastAPI `TestClient` em `GET /health`
  - Resultado: HTTP 200 com `{"status": "ok", "app_env": "development"}`.

### Artifact Validation

- `project-context/2.build/backend.md` registra a implementação do CrewAI, especialistas, revisão jurídica e metadados persistidos.
- `project-context/2.build/frontend.md` registra Angular 21, PrimeNG 21, Nora, rotas `chat` e `admin`, e remoção do Tailwind.
- `project-context/2.build/integration.md` foi atualizado para refletir que o endpoint atual aciona CrewAI, não apenas resposta mockada.
- `project-context/2.build/qa.md` foi atualizado com evidências de 2026-04-25 e limitações de validação runtime.

## Release Decision

**Decisão:** avançar para demonstração local controlada, não para produção.

O MVP está tecnicamente consistente para uma demonstração local desde que o ambiente esteja preparado com:

- banco disponível e migrations aplicadas;
- variáveis de ambiente revisadas;
- uma única chave LLM válida configurada;
- teste manual do fluxo browser + FastAPI + banco + LLM antes da demo.

## Residual Risks

- O endpoint de conversa executa CrewAI de forma síncrona; chamadas com LLM podem ultrapassar o tempo aceitável de resposta.
- O fluxo completo com LLM real não foi reexecutado nesta rodada de validação.
- O frontend ainda não recupera histórico após reload, apesar do backend expor endpoint de consulta.
- A auditoria jurídica detalhada ainda não persiste os trechos exatos recuperados da CLT em tabela própria.
- Casos trabalhistas ambíguos ou sensíveis devem continuar escalando para humano.

## Next Gates

1. Executar migrations no banco alvo.
2. Rodar backend e frontend localmente.
3. Enviar uma pergunta simples de férias/remuneração pela UI e verificar persistência.
4. Enviar um caso sensível e confirmar escalonamento.
5. Testar falha controlada do backend e confirmar fallback visual no chat.
6. Definir se a próxima iteração resolve histórico de chat ou processamento assíncrono primeiro.

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
- `backend/src/themis_hr_api/orchestration/crew.py`
- `backend/tests/test_legal_review.py`
- `frontend/src/app/chat.service.ts`

## Assumptions

- Adapter ativo: `crewai`.
- O ambiente de demonstração usa as mesmas portas padrão: frontend `4200`, backend `8000`.
- As credenciais LLM serão fornecidas via variáveis de ambiente, nunca versionadas.

## Open Questions

- Qual provider/modelo LLM será o padrão oficial do MVP?
- A próxima etapa deve priorizar processamento assíncrono ou histórico de conversa na UI?
- Haverá requisito mínimo de auditoria jurídica antes da primeira demonstração para stakeholders?

## Audit

- Criado por Codex em 2026-04-25.
- Baseado em inspeção local, testes automatizados e atualização dos artefatos de QA e integração.

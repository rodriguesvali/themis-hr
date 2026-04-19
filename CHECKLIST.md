# Themis HR Execution Checklist

Checklist operacional para conduzir o bootstrap do Themis HR com AAMAD, do discovery até a validação do MVP.

---

## Phase 1: Requirements Definition (`@product-mgr`)

- [ ] Abrir um chat do agente `@product-mgr`.
- [ ] Executar um dos fluxos:
  - [ ] `*create-mr` para gerar `project-context/1.define/mr.md` usando `.cursor/templates/mr-template.md`
  - [ ] `*create-prd` para gerar `project-context/1.define/prd.md` usando `.cursor/templates/prd-template.md`
  - [ ] `*create-context` para gerar ambos e registrar contexto de handoff
- [ ] Validar aderência com [CONTEXT.md](CONTEXT.md).
- [ ] Confirmar escopo MVP, personas, jornadas, KPIs e riscos.
- [ ] Registrar hipóteses e dúvidas em cada artefato.

---

## Before Phase 2 Starts

- [ ] Garantir que `project-context/1.define/` contém:
  - [ ] `mr.md`
  - [ ] `prd.md`
- [ ] Confirmar que `.cursor/` contém:
  - [ ] `agents/`
  - [ ] `rules/`, `prompts/`, `templates/`
  - [ ] `personas.md`
  - [ ] `epics-index.mdc`
- [ ] Garantir que o adapter ativo é `crewai`.
- [ ] Revisar se PRD e MRD refletem o stack alvo do projeto:
  - [ ] Angular no frontend
  - [ ] PrimeNG como base visual e de componentes da UI
  - [ ] preset inicial Nora
  - [ ] FastAPI no backend
  - [ ] CrewAI para orquestração multiagente
  - [ ] Alembic para versionamento de banco

---

## Phase 2: Build Execution

### Step 0: Architecture Definition (`@system-arch`)

- [ ] Abrir um chat do agente `@system-arch`.
- [ ] Executar um dos fluxos:
  - [ ] `*create-sad` para gerar `project-context/1.define/sad.md`
  - [ ] `*create-sad --mvp` para gerar a versão enxuta do MVP
- [ ] Validar se a arquitetura descreve:
  - [ ] SPA Angular
  - [ ] APIs FastAPI
  - [ ] CrewAI e configuração dos agentes
  - [ ] base de conhecimento / RAG
  - [ ] critérios de escalonamento para humano
- [ ] Registrar pressupostos, decisões e trade-offs.

### Step 1: Environment Setup (`@project-mgr`)

- [ ] Abrir um chat do agente `@project-mgr`.
- [ ] Executar `*setup-project`.
- [ ] Confirmar que o agente:
  - [ ] cria a estrutura inicial do monorepo/projeto
  - [ ] define arquivos de ambiente de exemplo
  - [ ] documenta tudo em `project-context/2.build/setup.md`

### Step 2: Frontend Development (`@frontend-eng`)

- [ ] Abrir um chat do agente `@frontend-eng`.
- [ ] Executar `*develop-fe`.
- [ ] Confirmar que o agente:
  - [ ] implementa a base da interface Angular
  - [ ] usa PrimeNG como alicerce visual do MVP
  - [ ] parte do preset Nora como base do tema
  - [ ] cria componentes e fluxos de chat do MVP
  - [ ] adiciona stubs visuais para capacidades futuras
  - [ ] documenta decisões em `project-context/2.build/frontend.md`

### Step 3: Backend Development (`@backend-eng`)

- [ ] Abrir um chat do agente `@backend-eng`.
- [ ] Executar `*develop-be`.
- [ ] Confirmar que o agente:
  - [ ] estrutura o backend FastAPI
  - [ ] implementa a base do CrewAI e dos agentes do MVP
  - [ ] define a estratégia de persistência mínima do MVP, quando aplicável
  - [ ] usa Alembic para versionamento do schema
  - [ ] expõe endpoints HTTP para conversa/atendimento
  - [ ] documenta decisões em `project-context/2.build/backend.md`

### Step 4: Integration (`@integration-eng`)

- [ ] Abrir um chat do agente `@integration-eng`.
- [ ] Executar `*integrate-api`.
- [ ] Confirmar que o agente:
  - [ ] conecta Angular ao backend FastAPI
  - [ ] valida o fluxo ponta a ponta
  - [ ] documenta riscos e lacunas em `project-context/2.build/integration.md`

### Step 5: Quality Assurance (`@qa-eng`)

- [ ] Abrir um chat do agente `@qa-eng`.
- [ ] Executar `*qa`.
- [ ] Confirmar que o agente:
  - [ ] roda smoke tests e testes funcionais
  - [ ] verifica o fluxo de atendimento de ponta a ponta
  - [ ] registra bugs, gaps e próximos passos em `project-context/2.build/qa.md`

---

## Step 6: Local MVP Launch

- [ ] Seguir `setup.md` e `integration.md` para rodar o sistema localmente.
- [ ] Validar o fluxo principal do Themis HR:
  - [ ] entrada da solicitação
  - [ ] classificação
  - [ ] consulta à base de conhecimento
  - [ ] resposta final
  - [ ] escalonamento quando aplicável

---

## Step 7: Prepare for Next Phase

- [ ] Consolidar artefatos em `project-context/2.build/` e `project-context/3.deliver/`.
- [ ] Registrar backlog e deferrals.
- [ ] Converter gaps identificados em issues ou tarefas futuras.

---

Para detalhes adicionais, consulte [README.md](README.md), `.cursor/templates/` e `.cursor/rules/`.

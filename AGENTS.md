# Themis HR Agent Framework

Este projeto usa o AAMAD como estrutura de desenvolvimento multiagente, adaptado para o contexto do Themis HR.

## O Que Este Arquivo Descreve

As personas abaixo pertencem à **camada de desenvolvimento** do projeto.

- Elas orientam o trabalho no IDE
- Elas não são os agentes de negócio do help desk
- Elas não representam a runtime CrewAI do produto final

Os agentes do produto Themis HR serão implementados no backend e orquestrados separadamente com CrewAI.

## Agent Personas

- **@product-mgr** — Product Manager: conduz discovery, gera `mr.md` e `prd.md`
- **@system-arch** — System Architect: produz `sad.md` e especificações funcionais
- **@project-mgr** — Project Manager: prepara estrutura, dependências e ambiente
- **@frontend-eng** — Frontend Engineer: implementa o frontend Angular do MVP
- **@backend-eng** — Backend Engineer: implementa backend FastAPI e orquestração CrewAI
- **@integration-eng** — Integration Engineer: conecta frontend Angular e backend FastAPI
- **@qa-eng** — QA Engineer: valida o MVP e registra lacunas

## Workflow

1. **Define:** `@product-mgr` gera `project-context/1.define/mr.md` e `project-context/1.define/prd.md`
2. **Architecture:** `@system-arch` gera `project-context/1.define/sad.md`
3. **Build:** `@project-mgr` → `@frontend-eng` / `@backend-eng` → `@integration-eng` → `@qa-eng`
4. **Deliver:** consolidação de evidências e preparação de rollout

## Source of Truth

- Visão do produto: `CONTEXT.md`
- Requisitos e pesquisa: `project-context/1.define/`
- Evidências e briefs de build: `project-context/2.build/`
- Evidências de entrega: `project-context/3.deliver/`

Os arquivos em `project-context/2.build/` podem começar como briefs de handoff do bootstrap e devem ser atualizados in place pelos agentes da fase de build.

## IDE Definitions

- Cursor: `.cursor/agents/`
- VS Code / GitHub Copilot: `.github/agents/`

## Frontend Tooling Note

Quando o ambiente disponibilizar o MCP do PrimeNG, o agente `@frontend-eng` deve usá-lo como apoio principal para implementação da UI baseada em PrimeNG.

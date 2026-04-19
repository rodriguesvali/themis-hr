# Themis HR

Bootstrap do projeto **Themis HR**, um sistema multiagente de suporte ao RH.

Este repositório usa o **AAMAD** como framework de trabalho para organizar descoberta, arquitetura, implementação e entrega. O bootstrap gerado pelo AAMAD foi ajustado para refletir o stack e o domínio do projeto.

## Visão do Projeto

O objetivo do Themis HR é oferecer um help desk inteligente para colaboradores, com capacidade de:

- responder dúvidas sobre políticas e processos internos;
- classificar solicitações de RH;
- consultar base de conhecimento;
- ajustar tom de resposta conforme sentimento;
- escalar para atendimento humano quando necessário.

## Stack Alvo

- **Frontend:** Angular
- **Backend:** Python com FastAPI
- **Motor multiagente:** CrewAI
- **Metodologia:** AAMAD

O contexto funcional inicial está em [CONTEXT.md](CONTEXT.md).

## Duas Camadas de Agentes

Este projeto usa "agentes" em dois sentidos diferentes:

- **Agentes de desenvolvimento**
  - vivem no bootstrap do AAMAD
  - são usados no IDE como personas e fluxo de trabalho
  - ajudam a produzir requisitos, arquitetura, código e testes

- **Agentes do produto**
  - fazem parte do Themis HR em si
  - serão implementados no backend
  - serão orquestrados com CrewAI para atender o help desk de RH

Resumo prático:

- **VS Code + AAMAD** ajudam a construir o sistema
- **FastAPI + CrewAI** ajudam o sistema a operar

## Estrutura do Repositório

```text
themis-hr/
├── .cursor/
│   ├── agents/          # Personas para uso no Cursor
│   ├── prompts/         # Prompts guiados do framework
│   ├── rules/           # Regras always-on do AAMAD
│   └── templates/       # Templates de MR, PRD, SAD e SFS
├── .github/
│   ├── agents/          # Personas para VS Code / GitHub Copilot
│   ├── instructions/    # Instruções equivalentes às rules do Cursor
│   └── prompts/         # Prompts compartilhados
├── project-context/
│   ├── 1.define/        # mr.md, prd.md, sad.md e artefatos de definição
│   ├── 2.build/         # setup.md, frontend.md, backend.md, integration.md, qa.md
│   └── 3.deliver/       # Evidências de entrega, rollout e operação
├── AGENTS.md            # Atalho humano para personas e fluxo
├── CHECKLIST.md         # Passo a passo operacional do bootstrap
├── CONTEXT.md           # Contexto conceitual do produto
└── README.md
```

## Fluxo de Trabalho

### 1. Define

O Product Manager produz os artefatos de descoberta e requisitos:

- `project-context/1.define/mr.md`
- `project-context/1.define/prd.md`

### 2. Architecture

O System Architect transforma os requisitos em arquitetura executável:

- `project-context/1.define/sad.md`
- `project-context/1.define/sfs/<feature-id>.md` quando necessário

### 3. Build

Os agentes de projeto trabalham de forma sequencial, usando os artefatos anteriores como fonte única de contexto:

- Project Manager → `project-context/2.build/setup.md`
- Frontend Engineer → `project-context/2.build/frontend.md`
- Backend Engineer → `project-context/2.build/backend.md`
- Integration Engineer → `project-context/2.build/integration.md`
- QA Engineer → `project-context/2.build/qa.md`

## Convenções Importantes

- Use nomes de agentes com hífen: `@product-mgr`, `@system-arch`, `@project-mgr`, `@frontend-eng`, `@backend-eng`, `@integration-eng`, `@qa-eng`.
- Use sempre os artefatos dentro de `project-context/1.define/` e `project-context/2.build/` como referência principal.
- O frontend do Themis HR é **Angular**, não Next.js.
- O backend expõe APIs em **FastAPI**, não API routes de frontend.
- CrewAI deve ser configurado de forma auditável e orientada por arquivos.

## Como Usar o Bootstrap

1. Revise e mantenha o `CONTEXT.md` atualizado.
2. Gere `mr.md` e `prd.md` com `@product-mgr`.
3. Gere `sad.md` com `@system-arch`.
4. Siga o [CHECKLIST.md](CHECKLIST.md) para a fase de build.
5. Registre decisões e saídas nos artefatos versionados em `project-context/`.

Durante essa fase, a interação principal acontece no IDE. O bootstrap do AAMAD organiza como você conduz o desenvolvimento; ele não substitui a runtime CrewAI do produto.

## IDEs

- Cursor usa as definições em `.cursor/`.
- VS Code / GitHub Copilot usa `.github/agents/`, `.github/instructions/` e `.vscode/settings.json`.

O arquivo `.vscode/settings.json` foi mantido versionado porque faz parte da configuração compartilhada para descoberta das personas no workspace.

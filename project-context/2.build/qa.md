# Themis HR
## QA Handoff

Data: 2026-04-19
Responsável alvo: `@qa-eng`
Status: brief inicial do bootstrap; deve ser atualizado in place durante a validação.

## Mission

Validar o MVP do Themis HR após a implementação e integração mínimas.

## Inputs

- `project-context/2.build/frontend.md`
- `project-context/2.build/backend.md`
- `project-context/2.build/integration.md`
- `project-context/2.build/setup.md`
- `project-context/1.define/prd.md`
- `project-context/1.define/sad.md`

## Scope

### In Scope

- smoke tests do MVP
- validação funcional do fluxo principal
- registro de gaps
- registro de riscos de release

### Out of Scope

- testes de performance avançados
- testes de segurança avançados
- testes fora do escopo implementado

## Required Outcomes

- checklist funcional do MVP
- bugs encontrados
- limitações do fluxo atual
- backlog de testes futuros

## Minimum Validation Checklist

- o frontend abre e permite envio de mensagem
- o backend responde ao healthcheck
- o fluxo principal executa sem erro fatal
- o escalonamento é comunicado corretamente quando ocorrer
- erros técnicos apresentam fallback compreensível

## Deliverable

Atualizar este arquivo com:

- cenários testados
- resultados
- defeitos encontrados
- riscos residuais
- recomendação de pronto/não pronto para próxima fase

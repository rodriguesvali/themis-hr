# Themis HR
## Frontend Handoff

Data: 2026-04-19
Responsável alvo: `@frontend-eng`
Status: brief inicial do bootstrap; deve ser atualizado in place conforme o frontend for implementado.

## Mission

Implementar o frontend do MVP do Themis HR com:

- Angular
- PrimeNG
- preset Nora
- fluxo principal de helpdesk

## Inputs

- `project-context/1.define/prd.md`
- `project-context/1.define/sad.md`
- `project-context/2.build/setup.md`
- `CONTEXT.md`

## Scope

### In Scope

- scaffold Angular
- configuração do PrimeNG
- adoção do preset Nora
- shell principal do helpdesk
- estados de carregamento, erro e escalonamento

### Out of Scope

- integração real com backend nesta fase do frontend
- telas administrativas completas
- refinamentos visuais fora do MVP
- features futuras funcionando

## Required Outcomes

- aplicação Angular inicial
- base visual com PrimeNG
- preset Nora configurado
- layout do fluxo de atendimento
- componentes mínimos para interação do usuário
- documentação de decisões em `project-context/2.build/frontend.md`

## UI Guidance

- preferir componentes PrimeNG sempre que possível
- manter visual enterprise, claro e consistente
- evitar inventar design system paralelo ao PrimeNG
- preservar espaço para customização por design tokens

## Open Questions to Resolve During Implementation

- estrutura final de standalone components vs módulos
- forma inicial de organizar a feature de helpdesk
- padrão de serviços HTTP e estado local

## Deliverable

Atualizar este arquivo com:

- decisões de implementação
- componentes criados
- uso do PrimeNG/Nora
- gaps conhecidos
- próximos passos

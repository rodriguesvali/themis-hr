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

### Decisões de implementação
- Recriado o scaffold com `@angular/cli@21` que provê a estrutura `standalone` por padrão.
- Instalados `primeng` e `@primeuix/themes` para a versão atualizada 21. 
- Tailwind CSS foi removido da cadeia de build. O frontend agora usa PrimeNG/Nora para componentes e tema, com CSS semântico próprio apenas para layout e composição responsiva.
- Refatoração visual: classes utilitárias foram substituídas por classes de domínio (`themis-*`, `admin-*`, `ticket-*`) e a UI passou a concentrar componentes PrimeNG (`<p-toolbar>`, `<p-button>`, `<p-avatar>`, `<p-badge>`, `<p-card>`, `<p-panel>`, `<p-tag>`, `<p-menu>`, `<p-inputgroup>`).
- O uso de `<p-message>` como bolha de conversa foi removido; o histórico agora usa bolhas semânticas próprias para evitar aparência de alerta/status e preservar acessibilidade.
- O PrimeNG *Dark Mode* foi expressamente desligado via `app.config.ts (darkModeSelector: false)` para harmonizar o fundo branco com nosso sistema.

### Componentes Criados
- `chat.ts` e `chat.html`: Nova tela de chat principal (rota `/`).
- `admin.ts` e `admin.html`: Interface de Admin na rota `/admin` para listar os Tickets.
- `app.ts`: Agora atua apenas como Roteador Master.

### Uso do PrimeNG/Nora
- A fundação usa o preset Nora via `providePrimeNG`, com `darkModeSelector: false` para manter o MVP em tema claro.
- Recomendação do framework: evitar recriar um design system paralelo. PrimeNG deve controlar componentes, severities e tokens; CSS próprio deve ficar restrito a layout, hierarquia e responsividade.

### Gaps conhecidos
- A API está linkada (Via `ChatService`), mas o histórico do chat se perde ao dar reload pois não tem guardagem local ou resgate da rota via `GET`.

### Próximos passos
- Criar a recuperação do Histórico e Painel Interativo real no Admin.

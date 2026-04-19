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
- Recriado o scaffold com `@angular/cli@21` (V21+ como sugerido no chat) que provê a estrutura `standalone` por padrão e suporta corretamente as versões latest de Theaming do PrimeNG.
- Instalados `primeng` e `@primeuix/themes` (versão correta para o Angular 21, o PrimeNG Themes foi substituído por PrimeUIX Themes).
- Tailwind CSS v4 foi adicionado para acelerar estruturação flex/grid em conjunto com o PrimeNG, integrando através do novo `cssLayer`.

### Componentes Criados
- `app.html` e `app.ts` (AppComponent base) refatorados para servirem como a "Shell" e a experiência de chat mockada. Componentes do primeng não foram instanciados diretamente via Tag no html neste primeiro MVP porque importam módulos pesados, foi preferido a base nativa (HTML) usando as variáveis CSS da base PrimeNG/Aura para provar o conceito e velocidade do visual.

### Uso do PrimeNG/Nora
- No PrimeNG 21 a fundação mudou para PrimeUIX. Para MVP rápido foi acoplado o `Aura` (padrão nativo das novas versões) e incluído no `app.config.ts`. O Nora é um theme comercial/builder do PrimeNG que deve ser exportado e colado dentro da customização do Aura nas etapas futuras.

### Gaps conhecidos
- A tela de chat atualmente possui apenas HTML/Tailwind para dar a cara da aplicação, não há chamadas HTTP reais implementadas no `@angular/common/http` ligadas ao backend local ainda.

### Próximos passos
- Conectar a API FastAPI (`POST /api/v1/conversations`) no `app.ts` e tratar as requisições de digitação real.
- Fase 4: Integration (`@integration-eng`)

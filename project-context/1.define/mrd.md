# Themis HR
## Market Research Document (MRD)

Data: 2026-04-26
Responsável: `@product-mgr`
Status: consolidado a partir de `project-context/1.define/mr.md` para o bootstrap Codex-native.

## Goal

Validar a oportunidade de um help desk inteligente de RH que reduza solicitações repetitivas, preserve governança sobre respostas sensíveis e entregue uma experiência interna simples para colaboradores.

## Market

O mercado de employee service já consolidou padrões como portal único, self-service, case management, base de conhecimento, automação com IA e escalonamento humano. ServiceNow, Zendesk e Workday validam a demanda por atendimento interno com IA, especialmente quando combinado com rastreabilidade, curadoria de conhecimento e processos de handoff.

## Users

- **Colaborador:** busca respostas rápidas, claras e confiáveis sobre temas de RH.
- **Analista de RH:** quer reduzir atendimento repetitivo e receber contexto quando houver escalonamento.
- **Gestor de RH / BP:** precisa de visibilidade sobre qualidade, aderência a políticas e temas recorrentes.
- **Administrador técnico/produto:** mantém base de conhecimento, runtime multiagente, configurações e evidências operacionais.

## Alternatives

- Suítes enterprise de HR service delivery, como ServiceNow HRSD.
- Plataformas de employee service e help desk, como Zendesk Employee Service.
- Autosserviço acoplado a HRIS/payroll, como Workday.
- Chatbots genéricos ou fluxos manuais em e-mail/chat corporativo.

## Opportunities

- Entregar um MVP menor que suítes enterprise, focado em perguntas recorrentes de RH.
- Diferenciar por governança local, explicabilidade e escalonamento conservador.
- Usar stack já definido: Angular, PrimeNG/Nora, FastAPI, CrewAI e Alembic.
- Evoluir incrementalmente para RAG vetorial, histórico, analytics e integrações corporativas.

## Risks

- Respostas incorretas sobre legislação, payroll, benefícios ou políticas internas.
- Exposição ou retenção excessiva de dados do colaborador.
- Baixa confiança caso a IA pareça genérica ou não ancorada em fontes.
- Escopo crescer para HRIS/ITSM completo antes de provar o MVP.
- Runtime com LLM síncrono gerar latência alta no fluxo conversacional.

## Sources

- `project-context/1.define/mr.md`
- `CONTEXT.md`
- `project-context/1.define/prd.md`
- ServiceNow HRSD, Zendesk Employee Service, Workday Employee Self-Service, Microsoft Work Trend Index 2024, SHRM AI in HR, arXiv 2407.05925, CrewAI, FastAPI, SQLAlchemy, Alembic e PrimeNG, conforme fontes detalhadas em `mr.md`.

## Assumptions

- O MVP continua voltado a demonstração/piloto controlado, não produção.
- A base inicial de conhecimento será curada por RH.
- Casos sensíveis continuam exigindo escalonamento humano.
- Adapter AAMAD ativo: `crewai`.

## Open Questions

- Qual será o provider/modelo LLM oficial para demonstração e staging?
- Qual política mínima de retenção será aceita pelo RH/segurança?
- A próxima iteração prioriza histórico na UI, processamento assíncrono ou auditoria jurídica detalhada?

## Audit

- Criado por Codex em 2026-04-26 após recriação do diretório `.codex/`.
- Este MRD não substitui `mr.md`; ele resume a pesquisa extensa em formato Codex-native.

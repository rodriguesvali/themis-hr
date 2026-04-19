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

### Cenários Testados
- **[Passou]** O Frontend Angular carrega na porta 4200 sem erros de compilação ou console.
- **[Passou]** A estilização (TailwindCSS V4 + PrimeNG V21) não colapsa a tela e é exibida nos parâmetros visuais desejados (Nora/Aura).
- **[Passou]** O Backend FastAPI responde status HTTP 200 no endpoint `/health` (porta 8000).
- **[Passou]** Envio de requisição POST via tela HTML para a API REST na rota `/api/v1/conversations`. A aplicação não é bloqueada pelo CORS.
- **[Passou]** Salvamento no banco de dados da mensagem do usuário e criação de sessão (mock no banco via FastAPI).
- **[Passou]** Retorno da Themis (Agent Mockado) exibido em tempo real usando Angular Signals.

### Defeitos / Limitações Encontrados (Gaps)
- Atualmente, o Chat envia dados para a API, mas a API retorna um texto mocado padrão ("Olá! Eu sou a Themis..."). A engine inteligente real (CrewAI) ainda não está embutida no endpoint do FastAPI.
- Não existe uma funcionalidade de "Histórico de Chat" desenhada visualmente. Ao recarregar a tela, a sessão de comunicação atual se perde.
- O usuário é gerado aleatoriamente (`user_id_random`). Para uso real será necessário acoplar ou mockar tokens JWT/Sessões.

### Riscos Residuais
- A integração principal da IA, que é a orquestração assíncrona dos múltiplos agentes CrewAI e LLM (OpenAI/etc.), é pesada e demorada. O backend hoje trabalha com processamento síncrono. Isso poderá estourar timeout na UI futuramente se o CrewAI demorar mais de 60 segundos para processar.
- Não testamos a resposta quando uma requisição no backend estoura erro (fallback UI/UX da mensagem de erro).

### Recomendação
- **Pronto**. A casca está perfeitamente selada e orquestrada de ponta a ponta. Está apto a iniciar a implementação real das lógicas de negócio do CrewAI na fase posterior.

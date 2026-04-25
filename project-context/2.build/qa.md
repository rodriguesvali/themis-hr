# Themis HR
## QA Handoff

Data: 2026-04-19
Responsável alvo: `@qa-eng`
Status: validado em 2026-04-25 com evidências automatizadas de backend, frontend e healthcheck da API.

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

### Cenários Registrados Anteriormente
- **[Passou]** O Frontend Angular carrega na porta 4200 sem erros de compilação ou console.
- **[Passou]** A estilização com PrimeNG V21, preset Nora e CSS semântico próprio não colapsa a tela e é exibida nos parâmetros visuais desejados.
- **[Passou]** O Backend FastAPI responde status HTTP 200 no endpoint `/health` (porta 8000).
- **[Passou]** Envio de requisição POST via tela HTML para a API REST na rota `/api/v1/conversations`. A aplicação não é bloqueada pelo CORS.
- **[Passou]** Salvamento no banco de dados da mensagem do usuário e criação de sessão (mock no banco via FastAPI).
- **[Passou]** Retorno da Themis exibido em tempo real usando Angular Signals.

### Validação Atualizada em 2026-04-25
- **[Passou]** Testes unitários do backend: `backend/.venv/bin/python -m unittest discover -s backend/tests`.
  - Resultado: 5 testes executados, todos OK.
  - Cobertura exercitada: revisão jurídica automática, escalonamento por risco médio, recuperação de lacuna do especialista via base legal, fallback por JSON inválido e fallback por falha na ferramenta da CLT.
- **[Passou]** Build de produção do frontend: `npm run build` em `frontend/`.
  - Resultado: bundle Angular gerado com sucesso em `frontend/dist/frontend`.
  - Observação: a build confirma compilação da aplicação Angular 21, rotas lazy de `chat` e `admin`, PrimeNG/Nora e pipe de markdown.
- **[Passou]** Smoke test do backend via `TestClient`.
  - Endpoint: `GET /health`.
  - Resultado observado: HTTP 200 com `{"status": "ok", "app_env": "development"}`.
- **[Confirmado por inspeção]** O endpoint `POST /api/v1/conversations` não está mais limitado a uma resposta mockada fixa: `main.py` chama `ThemisHRCrew().run`, persiste a mensagem do colaborador, persiste a resposta da Themis e salva metadados de categoria, especialista, confiança, escalonamento e revisão jurídica quando retornados pelo orquestrador.
- **[Não executado nesta rodada]** Round-trip real completo via browser + FastAPI + banco + LLM/CrewAI, porque exigiria ambiente runtime ativo com banco migrado e credenciais válidas de provider LLM.

### Defeitos / Limitações Encontrados (Gaps)
- O endpoint de conversa chama o CrewAI de forma síncrona; em uso real com LLM, pode haver latência alta e risco de timeout percebido pela UI.
- A validação de 2026-04-25 não executou o fluxo real com credenciais LLM; a confiança atual vem de testes unitários da orquestração jurídica, build do frontend e healthcheck da API.
- Não existe uma funcionalidade completa de histórico de chat desenhada na UI. O backend expõe `GET /api/v1/conversations/{conversation_id}`, mas o frontend ainda não recupera a conversa após reload.
- O usuário está fixo no frontend como `userId = "1"` para fins de MVP. Para uso real será necessário integrar autenticação, sessão ou JWT.
- A auditoria detalhada dos trechos exatos recuperados da CLT ainda não possui tabela própria.

### Riscos Residuais
- A integração principal da IA, que é a orquestração dos agentes CrewAI e LLM, segue pesada para uma chamada HTTP síncrona. O backend deve evoluir para fila, polling, SSE ou WebSocket se o tempo de resposta exceder o aceitável.
- A configuração de provider/modelo e chaves reais precisa ser validada no ambiente alvo. O teste local apontou que `GOOGLE_API_KEY` e `GEMINI_API_KEY` estão definidos simultaneamente, com precedência para `GOOGLE_API_KEY`.
- A revisão jurídica automática reduz risco, mas não substitui validação humana para casos trabalhistas ambíguos, denúncias, assédio, discriminação ou alto impacto.
- O fallback visual de erro existe no `ChatService`, mas ainda não foi validado em browser com falha real do backend nesta rodada.

### Recomendação
- **Pronto com ressalvas para entrega técnica do MVP local.** A base está apta para consolidação em `project-context/3.deliver/`, desde que o status de release deixe explícito que a validação real com LLM/banco/browser ainda precisa ser repetida em ambiente runtime completo antes de uma demonstração ou rollout.

## Sources

- `backend/src/themis_hr_api/main.py`
- `backend/src/themis_hr_api/orchestration/crew.py`
- `backend/tests/test_legal_review.py`
- `frontend/src/app/chat.service.ts`
- `frontend/package.json`
- Resultado local de `backend/.venv/bin/python -m unittest discover -s backend/tests` em 2026-04-25.
- Resultado local de `npm run build` em 2026-04-25.
- Resultado local de smoke test `GET /health` via FastAPI `TestClient` em 2026-04-25.

## Assumptions

- Adapter ativo assumido como `crewai`, conforme `AGENTS.md`.
- A validação desta rodada prioriza evidências reprodutíveis sem acionar LLM real.

## Open Questions

- Qual provider/modelo LLM será usado na demonstração ou ambiente alvo?
- O MVP deve aceitar latência síncrona do CrewAI ou já deve migrar para processamento assíncrono antes do próximo gate?
- O histórico de conversa precisa entrar no escopo imediato da próxima iteração?

## Audit

- Atualizado por Codex em 2026-04-25.
- A inconsistência anterior entre QA e backend foi corrigida: o endpoint atual chama CrewAI; o round-trip real com LLM não foi reexecutado nesta rodada.

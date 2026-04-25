# Themis HR
## Integration Handoff

Data: 2026-04-19
Responsável alvo: `@integration-eng`
Status: integração implementada; evidências atualizadas em 2026-04-25.

## Mission

Conectar frontend Angular e backend FastAPI para validar o fluxo mínimo do MVP.

## Inputs

- `project-context/2.build/frontend.md`
- `project-context/2.build/backend.md`
- `project-context/2.build/setup.md`
- `project-context/1.define/prd.md`
- `project-context/1.define/sad.md`

## Scope

### In Scope

- comunicação frontend ↔ backend
- envio de mensagem
- retorno de resposta
- tratamento de erro básico
- validação de fluxo ponta a ponta

### Out of Scope

- integrações externas não previstas no MVP
- fluxos secundários avançados
- automações fora do caminho principal

## Required Outcomes

- definição dos endpoints efetivamente usados pelo frontend
- integração mínima funcionando
- documentação dos contratos usados
- registro de gaps ou bloqueios em `project-context/2.build/integration.md`

## Validation Target

Fluxo mínimo esperado:

1. usuário envia mensagem
2. frontend chama backend
3. backend processa fluxo
4. frontend recebe resposta ou estado de escalonamento

## Deliverable

Atualizar este arquivo com:

### Estratégia de integração
- Utilizado a ferramenta `HttpClient` nativa do Angular.
- Backend FastAPI configurado com o middleware `CORSMiddleware` liberando acesso à URL do Angular (`http://localhost:4200`).
- Serviço do Angular (`ChatService`) encapsulou o fluxo utilizando a reatividade introduzida com o `signal<T>` para gerenciar as mensagens em tela perfeitamente síncronas.

### Contratos efetivos usados
- Envio: `POST /api/v1/conversations`
- Payload In: `{ "user_id": "1", "message": "string" }` no frontend atual do MVP.
- Payload Out: `{ "conversation_id": int, "reply": "string", "status": "string" }`

### Problemas encontrados
- *CORS Policy*: Sem permissão explícita no arquivo `main.py`, a primeira tentativa de chamada daria *Cross-Origin Block*. Corrigimos no backend em tempo real adicionando o Array `allow_origins`.

### Status do fluxo ponta a ponta
- **Implementado com ressalva de validação runtime.** A conexão Angular -> FastAPI está codificada via `ChatService` e o backend expõe `POST /api/v1/conversations` com persistência e chamada a `ThemisHRCrew().run`.
- A leitura anterior de que o backend devolvia apenas resposta mockada ficou desatualizada. O endpoint atual aciona o orquestrador CrewAI e persiste metadados de categoria, especialista, confiança, escalonamento e revisão jurídica.
- Em 2026-04-25 foram revalidados: build Angular (`npm run build`), testes unitários do backend (`backend/.venv/bin/python -m unittest discover -s backend/tests`) e healthcheck da API via `TestClient`.
- O round-trip real completo via browser + FastAPI + banco + LLM/CrewAI não foi reexecutado nesta rodada; deve ser o primeiro teste manual antes de demonstração ou rollout.

## Sources

- `frontend/src/app/chat.service.ts`
- `backend/src/themis_hr_api/main.py`
- `backend/src/themis_hr_api/orchestration/crew.py`
- `project-context/2.build/qa.md`

## Assumptions

- Adapter ativo assumido como `crewai`.
- O ambiente de demonstração terá banco migrado e credenciais LLM válidas.

## Open Questions

- O fluxo síncrono atual é aceitável para a demonstração ou precisa de fila/SSE/WebSocket antes do próximo gate?
- A recuperação de histórico no frontend entra na próxima iteração ou permanece fora do MVP local?

## Audit

- Atualizado por Codex em 2026-04-25 para alinhar o artefato ao backend atual com CrewAI.

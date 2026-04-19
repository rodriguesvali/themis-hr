# Themis HR
## Integration Handoff

Data: 2026-04-19
Responsável alvo: `@integration-eng`
Status: brief inicial do bootstrap; deve ser atualizado in place durante a integração.

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
- Payload In: `{ "user_id": "user_id_random", "message": "string" }`
- Payload Out: `{ "conversation_id": int, "reply": "string", "status": "string" }`

### Problemas encontrados
- *CORS Policy*: Sem permissão explícita no arquivo `main.py`, a primeira tentativa de chamada daria *Cross-Origin Block*. Corrigimos no backend em tempo real adicionando o Array `allow_origins`.

### Status do fluxo ponta a ponta
- **Concluído**. A conexão foi validada. O front-end envia a mensagem e o backend (ainda sem o agente do CrewAI acoplado à inteligência LLM) processa o log de chat no postgres do ambiente e devolve a resposta Mockada com sucesso.

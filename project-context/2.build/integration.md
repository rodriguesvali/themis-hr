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

- estratégia de integração
- contratos efetivos usados
- problemas encontrados
- status do fluxo ponta a ponta

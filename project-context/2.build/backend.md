# Themis HR
## Backend Handoff

Data: 2026-04-19
Responsável alvo: `@backend-eng`
Status: brief inicial do bootstrap; deve ser atualizado in place conforme o backend for implementado.

## Mission

Implementar o backend do MVP do Themis HR com:

- FastAPI
- CrewAI
- persistência mínima
- Alembic

## Inputs

- `project-context/1.define/prd.md`
- `project-context/1.define/sad.md`
- `project-context/2.build/setup.md`
- `CONTEXT.md`

## Scope

### In Scope

- scaffold do backend FastAPI
- estrutura de orquestração do CrewAI
- configuração mínima de persistência
- versionamento de schema com Alembic
- endpoints mínimos do MVP

### Out of Scope

- integrações externas além do escopo do MVP
- analytics avançados
- automações fora do fluxo principal de atendimento
- expansão do banco além do mínimo necessário

## Required Outcomes

- estrutura de projeto backend coerente com o SAD
- endpoint de healthcheck
- endpoint inicial de conversa
- configuração inicial de sessions/persistência
- configuração explícita de migrations
- documentação de decisões em `project-context/2.build/backend.md`

## MVP Persistence Boundary

Persistir somente:

- conversa
- mensagem
- classificação principal
- evento de escalonamento
- referência de conhecimento

## CrewAI Expectations

- agents e tasks preferencialmente orientados a arquivo
- fluxo sequencial no MVP
- separação clara entre intake, classificação, conhecimento, resposta, sentimento e escalonamento

## Open Questions to Resolve During Implementation

- SQLite ou PostgreSQL já no primeiro run funcional
- provider/model inicial do runtime multiagente
- formato final da camada de retrieval no MVP

## Deliverable

Atualizar este arquivo com:

- decisões de implementação
- estrutura criada
- gaps conhecidos
- próximos passos

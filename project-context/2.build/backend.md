# Themis HR
## Backend Handoff

Data: 2026-04-19
Responsável alvo: `@backend-eng`
Status: implementado para MVP local com FastAPI, PostgreSQL, Alembic, CrewAI condicional e revisão jurídica automática.

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

- agents preferencialmente orientados a arquivo
- fluxo condicional no backend para controlar custo
- principal agent responsável por classificar e escolher um especialista
- especialistas por área executados sob demanda, nunca todos em sequência

## Open Questions to Resolve During Implementation

- SQLite ou PostgreSQL já no primeiro run funcional
- provider/model inicial do runtime multiagente
- formato final da camada de retrieval no MVP

## Deliverable

Atualizar este arquivo com:

### Decisões de implementação
- A stack do backend foi montada usando FastAPI, SQLAlchemy 2.0 e Alembic.
- O banco escolhido para o primeiro `run` já foi o PostgreSQL conectado via `psycopg`, pois o `.devcontainer` já prove o banco pronto, economizando tempo de refatoração do SQLite futuramente.
- A estrutura de módulos foi padronizada (`api`, `core`, `db`, `models`, `schemas`, `services`, `orchestration`, `knowledge`).
- Tabelas iniciais (`conversations` e `messages`) foram criadas e as migrações aplicadas.
- Endpoints `POST /api/v1/conversations` **conectado ao motor CrewAI**.
- Orquestrador (`ThemisHRCrew`) foi refatorado para o modelo "principal + especialistas sob demanda".
- O fluxo deixou de ser uma esteira fixa de 6 tasks. Agora o `principal_agent` classifica a pergunta, identifica sensibilidade e chama somente um especialista de área quando necessário.
- Especialistas configurados: `ferias_agent`, `remuneracao_agent`, `jornada_agent`, `admissao_agent` e `rescisao_agent`.
- Casos de alta sensibilidade ou assuntos gerais são escalados diretamente, sem chamada a especialista.
- As bases de conhecimento mockadas por área são carregadas apenas para o especialista escolhido, reduzindo contexto enviado à LLM.
- Foi adicionado o `legal_reviewer_agent` como consultor jurídico trabalhista após a resposta do especialista.
- A revisão jurídica consulta o PDF local da CLT em `backend/docs/consolidacao_leis_trabalho.pdf` por uma ferramenta cacheada de busca textual.
- Respostas aprovadas pelo especialista agora passam por revisão jurídica antes de chegar ao colaborador; reprovação, risco médio/alto ou falha na revisão geram escalonamento humano.
- O caminho da CLT pode ser alterado via `CLT_PDF_PATH`.
- O texto extraído da CLT é cacheado por processo para evitar releitura do PDF a cada revisão.
- A revisão jurídica faz uma consulta prévia obrigatória à CLT e passa os trechos recuperados para o `legal_reviewer_agent`.
- Metadados da resposta da Themis passaram a ser persistidos em `messages`: categoria, especialista, confiança, motivo de escalonamento, status da revisão jurídica, nível de risco, notas e fundamento legal.

### Estrutura Criada
O backend está encapsulado na pasta `backend/src/themis_hr_api`. O Alembic está gerenciando os scripts em `backend/alembic`. Dependências listadas em `backend/requirements.txt`. O CrewAI se localiza dentro de `orchestration/`.

### Gaps conhecidos
- O Provider/Modelo para LLM deve ser ajustado com chaves reais no ambiente.
- O endpoint de conversa ainda executa CrewAI de forma síncrona. Mesmo com a redução de custo, em sistemas de conversação real deve-se transitar para WebSockets, polling de filas (Celery/Redis) ou SSE.
- A classificação do `principal_agent` ainda depende de LLM. Uma camada preliminar de regras/keywords pode reduzir ainda mais o custo.
- A revisão jurídica usa busca textual simples no PDF da CLT; RAG vetorial por embeddings segue como evolução futura.
- A auditoria jurídica ainda é persistida como metadados da mensagem final; eventos detalhados de tool call/trechos exatos recuperados ainda não são registrados em tabela própria.

### Próximos passos
- Conectar RAG vetorial por área antes da chamada ao especialista escolhido.
- Persistir eventos detalhados de orquestração para auditoria completa por etapa.
- Persistir ou rastrear os trechos exatos retornados pela consulta à CLT em uma tabela própria de evidências jurídicas.

## Sources

- `backend/src/themis_hr_api/main.py`
- `backend/src/themis_hr_api/orchestration/crew.py`
- `backend/src/themis_hr_api/orchestration/config/agents.yaml`
- `backend/src/themis_hr_api/orchestration/config/tasks.yaml`
- `backend/src/themis_hr_api/models/chat.py`
- `backend/alembic/versions/`
- `backend/tests/test_legal_review.py`
- `project-context/1.define/sad.md`
- `project-context/1.define/sfs/conversation-flow.md`
- `project-context/1.define/sfs/legal-review.md`

## Assumptions

- Adapter ativo: `crewai`.
- Provider atual: Google/Gemini via `GOOGLE_API_KEY`.
- O endpoint síncrono é aceitável somente para demo local controlada.
- A busca textual na CLT é uma salvaguarda inicial, não parecer jurídico nem validação legal completa.

## Open Questions

- Qual modelo Gemini será fixado para demonstração/staging?
- O runtime deve migrar primeiro para fila, SSE ou WebSocket?
- Qual formato de tabela será usado para evidências jurídicas e tool calls?

## Audit

- Criado por `@backend-eng` em 2026-04-19.
- Atualizado por Codex em 2026-04-26 para completar metadados AAMAD e referenciar SFSs do fluxo atual.

# Themis HR
## System Architecture Document (SAD)

Data: 2026-04-19

## 1. Executive Summary

### Business Objective

O Themis HR tem como objetivo reduzir a carga operacional do RH em solicitações repetitivas e melhorar a experiência do colaborador com um help desk inteligente, baseado em conhecimento interno, orquestração multiagente e escalonamento humano quando necessário.

### MVP Scope

O MVP cobre o fluxo essencial de atendimento:

- entrada da solicitação do colaborador;
- classificação da intenção;
- consulta a base de conhecimento;
- resposta contextualizada;
- ajuste de tom;
- decisão de escalonamento;
- persistência mínima para trilha de atendimento.

### Architecture Overview

O sistema será dividido em:

- **Frontend Angular** com **PrimeNG** e preset **Nora**;
- **Backend FastAPI** para APIs e orquestração do fluxo;
- **CrewAI** para executar os agentes de negócio do Themis HR;
- **persistência relacional mínima** com schema versionado por **Alembic**;
- **camada de conhecimento** com fontes documentais controladas e recuperação orientada por contexto.

### Main Trade-offs and Assumptions

- O MVP prioriza clareza e governança sobre automação total.
- Nem todo caso será resolvido automaticamente; o handoff humano faz parte da proposta.
- A persistência será mínima, mas suficiente para auditoria e evolução controlada.
- O sistema nasce para domínio interno de RH, não como suíte full-service.

## 2. Architectural Drivers

### Functional Requirements

- Atender solicitações em linguagem natural.
- Classificar temas de RH.
- Buscar conhecimento em fontes internas autorizadas.
- Responder com base em política/documentação.
- Escalar para humano quando necessário.
- Manter histórico mínimo do atendimento.

### Quality Attributes

- **Auditabilidade:** decisões e resultados rastreáveis.
- **Clareza:** fluxo inteligível para usuário e operação.
- **Modularidade:** separação entre UI, API, orquestração e dados.
- **Segurança:** cuidado com dados pessoais e temas sensíveis.
- **Evolutividade:** capacidade de ampliar conhecimento, integrações e persistência.

### Constraints

- Frontend deve ser Angular.
- UI deve usar PrimeNG como suíte principal.
- Preset inicial do frontend deve ser Nora.
- Backend deve ser FastAPI.
- Orquestração multiagente deve usar CrewAI.
- Versionamento de schema deve usar Alembic.

### Risks

- Resposta incorreta em tema sensível.
- Classificação insuficiente.
- Escalonamento tardio ou ausente.
- Base de conhecimento incompleta ou desatualizada.
- Persistência insuficiente para auditoria.

### Compliance and Policy Considerations

- Conteúdo de RH pode envolver informações pessoais, benefícios, payroll e relações trabalhistas.
- O sistema deve explicitar quando estiver respondendo com base em conhecimento disponível e quando houver necessidade de revisão humana.
- Logs e dados persistidos devem ser mínimos e proporcionais ao MVP.

## 3. System Context

### Primary Users and Actors

- **Colaborador:** inicia a solicitação e recebe resposta ou escalonamento.
- **Analista de RH:** recebe casos escalados e revisa contexto do atendimento.
- **Gestor de RH / BP:** acompanha qualidade, aderência e evolução do serviço.
- **Administrador técnico / produto:** mantém base de conhecimento, regras e observabilidade.

### External Systems and Dependencies

No MVP, dependências externas ficam reduzidas a:

- LLM/provider configurado para CrewAI;
- base de conhecimento inicial;
- banco relacional mínimo.

Integrações com SSO, HRIS, ITSM ou mensageria ficam fora do primeiro corte.

### Internal Boundaries

- **Frontend:** experiência do colaborador.
- **API Backend:** entrada HTTP, validação, sessão, persistência e orquestração.
- **Crew Runtime:** execução dos agentes do produto.
- **Knowledge Layer:** recuperação de políticas, FAQs e documentos.
- **Escalation Flow:** decisão de encaminhamento humano.

## 4. Solution Overview

### Angular Application Responsibilities

- renderizar a interface do help desk;
- capturar mensagens do colaborador;
- exibir respostas, estados de carregamento, fallback e escalonamento;
- apresentar UI consistente e enterprise com PrimeNG/Nora;
- encapsular a experiência do atendimento em componentes reutilizáveis.

### FastAPI Responsibilities

- expor endpoints do MVP;
- validar requests e responses;
- gerenciar sessões e histórico mínimo;
- acionar a orquestração CrewAI;
- persistir decisões relevantes do fluxo;
- servir como camada de integração entre frontend, dados e runtime multiagente.

### CrewAI Responsibilities

- executar o fluxo multiagente do produto;
- manter fronteiras claras entre responsabilidades;
- produzir saídas estruturadas por etapa;
- facilitar auditabilidade e evolução do comportamento.

No build atual, a sequência conceitual de seis papéis foi implementada como fluxo condicional para reduzir custo e contexto: `principal_agent` faz roteamento e sensibilidade, um especialista de domínio responde sob demanda e `legal_reviewer_agent` revisa a resposta quando houver resposta automática possível.

### Knowledge Retrieval / RAG Responsibilities

- consultar fontes de conhecimento aprovadas;
- retornar conteúdo relevante e contextualizado;
- reduzir alucinação ao ancorar respostas em documentos internos;
- fornecer suporte para explicabilidade da resposta.

### Escalation and Fallback Responsibilities

- detectar baixa confiança, sensibilidade ou ausência de cobertura;
- interromper resposta automática quando necessário;
- registrar motivo do handoff;
- preservar contexto mínimo para análise humana.

## 5. Frontend Architecture

### Angular Application Structure

O frontend do MVP deve nascer com estrutura simples e orientada a evolução:

- `core/` para serviços transversais, interceptors e configuração;
- `shared/` para componentes, pipes e utilitários reutilizáveis;
- `features/helpdesk/` para experiência principal do atendimento;
- `features/history/` opcionalmente para evolução do histórico no pós-MVP.

Pode ser implementado com standalone components, desde que mantenha separação clara entre shell, componentes de UI e acesso a serviços.

### PrimeNG Usage Strategy and Shared UI Foundation

PrimeNG será a suíte principal de componentes para:

- layout;
- formulários;
- botões e mensagens;
- overlays e feedback visual;
- skeleton/loading;
- tabelas/listagens futuras;
- badges, chips e estados de atendimento.

Sempre que PrimeNG oferecer um componente aderente, ele deve ser preferido a componentes visuais customizados.

### Theme and Design Token Approach

- O preset inicial será **Nora**.
- O time poderá customizar tokens para cores institucionais, espaçamento e estados.
- A customização deve preservar consistência enterprise e acessibilidade básica.
- O frontend deve evitar divergência visual arbitrária entre telas e componentes.

### How the Nora Preset Is Adopted and Customized

- Nora entra como preset inicial do `providePrimeNG`.
- Design tokens devem ser centralizados.
- O primeiro nível de customização deve ser superficial: marca, cores, espaçamento e estados.
- Mudanças profundas na semântica visual só devem ocorrer se a arquitetura do produto exigir.

### Routing and Component Strategy

No MVP, o roteamento pode ser mínimo:

- rota principal de atendimento;
- rota administrativa futura opcional.

O shell principal pode conter:

- cabeçalho institucional;
- área do chat;
- área de status/escalonamento;
- estados vazios e de erro.

### State and API Communication Strategy

- estado local da conversa no frontend;
- chamadas HTTP ao backend FastAPI;
- separação entre estado de exibição e estado persistido;
- mensagens do usuário e respostas tratadas como eventos da sessão.

### UX Flow for HR Support Conversations

Fluxo básico:

1. usuário envia mensagem;
2. UI entra em estado de processamento;
3. backend executa o fluxo multiagente;
4. resposta é exibida;
5. caso necessário, UI comunica escalonamento.

### Error, Loading, and Escalation States

O frontend precisa ter estados específicos para:

- carregamento da resposta;
- falha técnica;
- ausência de conteúdo suficiente;
- escalonamento para RH;
- retorno com instrução parcial e encaminhamento.

## 6. Backend Architecture

### FastAPI Service Structure

Estrutura sugerida:

- `api/` para routers e contratos HTTP;
- `schemas/` para request/response DTOs;
- `services/` para casos de uso do domínio;
- `orchestration/` para integração com CrewAI;
- `repositories/` para acesso a dados;
- `models/` para entidades persistidas;
- `config/` para settings e ambiente;
- `knowledge/` para adapters e retrieval;
- `db/` para engine, session e Alembic.

### Endpoint Design for MVP Flows

Endpoints iniciais recomendados:

- `POST /api/v1/conversations` para abrir sessão;
- `POST /api/v1/conversations/{id}/messages` para enviar mensagem;
- `GET /api/v1/conversations/{id}` para recuperar histórico mínimo;
- `GET /health` para health check.

### Validation, Error Handling, and Observability

- validação com Pydantic;
- tratamento consistente de erros técnicos e erros de domínio;
- logs estruturados;
- correlação por `conversation_id`;
- métricas futuras para deflection, escalonamento e falhas.

### Separation of Concerns

- **API layer:** contratos HTTP;
- **orchestration layer:** execução do crew;
- **domain logic:** regras de classificação, escalonamento e composição do atendimento;
- **data access layer:** persistência relacional;
- **knowledge layer:** busca de contexto documental.

### Persistence Boundaries for the MVP

O MVP deve persistir apenas o essencial:

- sessão de atendimento;
- mensagens da conversa;
- classificação principal;
- decisão de escalonamento;
- metadados de suporte da resposta;
- timestamps e status.

Não é necessário, no primeiro corte:

- analytics complexos;
- modelos extensos de RH;
- integrações profundas com dados de colaborador.

### Migration Strategy Using Alembic

- Alembic será a única ferramenta de versionamento de schema.
- Toda mudança de modelo persistente deve gerar migration explícita.
- O projeto deve nascer com migration inicial do MVP.
- Evoluções futuras devem ser pequenas, rastreáveis e reversíveis quando possível.

## 7. Multi-Agent Architecture

### Agent Set

#### Current Runtime Shape

O SAD original descreve papéis conceituais. O MVP implementado usa estes agentes runtime:

- **Principal Agent:** classifica intenção, sensibilidade e área.
- **Domain Specialists:** férias, remuneração, jornada, admissão e rescisão.
- **Legal Reviewer Agent:** consulta suporte textual da CLT e revisa risco jurídico antes de envio.
- **Direct Escalation Path:** assuntos gerais, alta sensibilidade e lacunas de cobertura são encaminhados sem especialista.

Esse desenho preserva os objetivos de intake, classificação, conhecimento, resposta, sentimento e escalonamento, mas agrega responsabilidades para manter o MVP simples e testável.

#### Intake Agent

- **Responsibility:** normalizar a mensagem de entrada
- **Inputs:** mensagem, sessão, metadados
- **Outputs:** payload estruturado
- **Dependencies:** contexto de sessão
- **Failure handling:** fallback para payload mínimo e marcação de baixa confiança

#### Classification Agent

- **Responsibility:** identificar categoria, subcategoria e sensibilidade
- **Inputs:** payload normalizado
- **Outputs:** classificação e flags
- **Dependencies:** taxonomia de assuntos de RH
- **Failure handling:** classificar como “não identificado” e favorecer escalonamento

#### Knowledge Agent

- **Responsibility:** recuperar fontes relevantes
- **Inputs:** categoria, contexto e termos
- **Outputs:** evidências documentais e metadados
- **Dependencies:** base de conhecimento aprovada
- **Failure handling:** ausência de evidência aumenta chance de handoff

#### Response Agent

- **Responsibility:** compor resposta útil
- **Inputs:** classificação, conhecimento, contexto
- **Outputs:** resposta candidata
- **Dependencies:** material recuperado e regras do domínio
- **Failure handling:** resposta limitada com comunicação de incerteza

#### Sentiment Agent

- **Responsibility:** ajustar tom e identificar urgência emocional
- **Inputs:** mensagem do usuário, resposta candidata
- **Outputs:** resposta ajustada, flags emocionais
- **Dependencies:** contexto conversacional
- **Failure handling:** manter resposta neutra e profissional

#### Escalation Agent

- **Responsibility:** decidir resposta final ou escalonamento
- **Inputs:** confiança, flags de risco, sentimento e cobertura
- **Outputs:** decisão final
- **Dependencies:** critérios de negócio definidos
- **Failure handling:** preferir escalonamento seguro em caso de ambiguidade

### Task Sequencing

Sequência conceitual esperada:

1. Intake
2. Classification
3. Knowledge
4. Response
5. Sentiment
6. Escalation

Sequência runtime atual:

1. `principal_agent` classifica área, categoria, sensibilidade e motivo.
2. Casos de alta sensibilidade ou assuntos gerais são escalados diretamente.
3. Um especialista de área recebe somente a base de conhecimento correspondente.
4. A resposta candidata passa por revisão jurídica automática quando houver resposta automática possível.
5. Risco médio/alto, reprovação, falha de revisão ou baixa confiança geram escalonamento.
6. Resposta final e metadados são persistidos em `messages`.

### Context Passing

- cada etapa recebe artefatos estruturados da etapa anterior;
- o backend preserva metadados principais da execução;
- a conversa é tratada como unidade contextual primária.

### Auditability Expectations

- registrar decisões principais;
- registrar se houve conhecimento recuperado;
- registrar motivo de escalonamento;
- permitir reconstrução básica do caminho da resposta.

### CrewAI Configuration Approach

- configuração preferencialmente orientada a arquivos;
- definição explícita de agents e tasks;
- separação entre config, runtime e integrações;
- execução sequencial no MVP para previsibilidade.

## 8. Data and Knowledge Architecture

### Conversation Data Model at MVP Level

Entidades mínimas:

- `conversation`
- `message`
- metadados de classificação em `message`
- metadados de escalonamento em `message`
- metadados de revisão jurídica em `message`
- evidências detalhadas de conhecimento e tool calls como extensão futura

### Policy and Knowledge Sources

Fontes iniciais esperadas:

- FAQ de RH;
- handbook;
- políticas de férias;
- políticas de benefícios;
- documentos gerais de onboarding e processos.

### Retrieval Approach

- retrieval sobre fontes autorizadas;
- recuperação contextual por tema;
- resposta sempre ancorada quando possível;
- ausência de evidência aumenta chance de escalonamento.

### Data Sensitivity and Privacy Concerns

- evitar armazenar mais dados pessoais do que o necessário;
- separar conteúdo de atendimento de futuras integrações com sistemas mestres;
- proteger logs e credenciais.

### Retention Boundaries for MVP

- retenção mínima suficiente para piloto, auditoria e melhoria;
- política final de retenção ainda depende de alinhamento com RH e segurança.

### Initial Database Choice

Recomendação original:

- **SQLite** para desenvolvimento local e experimentação rápida;
- caminho arquitetural preparado para **PostgreSQL** em staging/produção.

Racional:

- acelera o início;
- reduz custo e atrito;
- mantém simplicidade sem impedir evolução.

Decisão implementada no build:

- O primeiro run funcional usa **PostgreSQL** pelo Dev Container já fornecer o serviço.
- A escolha reduz retrabalho de migração futura, mas exige banco disponível para repetir a demo local.
- Alembic continua sendo a ferramenta única de versionamento.

### How Alembic Manages Schema Evolution

- migration inicial do conjunto mínimo de tabelas;
- revisões incrementais por necessidade de produto;
- cada revisão documenta motivo e impacto esperado.

## 9. Security and Compliance

### Authentication and Authorization Assumptions

- autenticação pode começar simplificada em ambiente controlado;
- o desenho deve permitir adoção futura de SSO corporativo;
- autorização fina fica para pós-MVP, mas a arquitetura já deve prever separação de papéis.

### Protection of Employee Data

- armazenar apenas o necessário;
- proteger segredos e conexão com banco;
- evitar respostas especulativas sobre dados pessoais.

### Audit Logging Expectations

- logs estruturados no backend;
- correlação por sessão;
- eventos críticos identificáveis.

### Secrets Management

- segredos em variáveis de ambiente;
- nada sensível hardcoded.

### Legal/Compliance Topics to Surface Later

- retenção oficial;
- controles de acesso detalhados;
- integração com identidade corporativa;
- requisitos específicos de LGPD/políticas internas.

## 10. Deployment and Environments

### Local Development Setup

- frontend Angular local;
- backend FastAPI local;
- banco local com migrations;
- config por `.env` e equivalentes;
- conhecimento inicial carregado em ambiente controlado.

### Test/Staging/Production Expectations

- `dev`: experimentação e iteração;
- `staging`: validação integrada;
- `prod`: ambiente endurecido com observabilidade e controles adicionais.

### Deployment Topology at MVP Level

- frontend servido separadamente do backend;
- backend conectado ao banco relacional;
- runtime CrewAI dentro do backend ou em camada adjacente controlada pelo backend.

### Environment Variables and Configuration Boundaries

Variáveis mínimas:

- provider/model LLM
- string de conexão do banco
- flags de ambiente
- caminhos/configuração da base de conhecimento
- segredos de autenticação futura, quando aplicável

## 11. Testing and Quality Strategy

### Unit Testing Expectations

- validação de utilitários, serviços e regras isoladas;
- cobertura de persistência e parsing básico.

### Integration Testing Expectations

- frontend ↔ backend
- backend ↔ banco
- backend ↔ crew orchestration
- fluxo com base de conhecimento

### End-to-End Testing Expectations

Cenários mínimos:

- pergunta elegível respondida com sucesso;
- pergunta sem cobertura escalada;
- erro técnico com fallback compreensível;
- recuperação básica de histórico.

### Architecture Validation Checkpoints

- stack aderente ao PRD;
- persistência mínima funcionando;
- migrations aplicando corretamente;
- escalonamento seguro;
- rastreabilidade mínima confirmada.

## 12. Decisions, Assumptions, and Future Work

### Architecture Decisions

- Angular como frontend
- PrimeNG como UI suite
- Nora como preset inicial
- FastAPI como backend
- CrewAI como orquestrador dos agentes do produto
- Alembic para versionamento de schema
- PostgreSQL no Dev Container para o run funcional atual
- fluxo CrewAI condicional com principal, especialista sob demanda e revisor jurídico
- revisão jurídica automática apoiada por busca textual no PDF local da CLT

### Assumptions

- haverá conteúdo suficiente para base inicial;
- RH participará da curadoria;
- o MVP pode operar em ambiente controlado antes de integrações corporativas completas.

### Open Questions

- autenticação entra no primeiro corte ou no piloto seguinte?
- qual será a política de retenção do histórico?
- quais categorias exigem escalonamento obrigatório desde o dia 1?
- o staging já nascerá com PostgreSQL?

### Deferred Items

- SSO
- HRIS/ERP
- analytics avançados
- anexos/documentos complexos
- painel operacional mais completo

### Post-MVP Extensions

- feedback loop e analytics;
- integração com sistemas corporativos;
- automação de jornadas;
- expansão do knowledge layer.

## 13. Traceability

### To `CONTEXT.md`

- duas camadas de agentes;
- frontend Angular;
- CrewAI no produto;
- help desk de RH com intake, classificação, conhecimento, resposta, sentimento e escalonamento.

### To `mr.md`

- validação de mercado;
- importância de self-service + case management + human handoff;
- necessidade de governança, knowledge e trilha de atendimento.

### To `prd.md`

- escopo P0/P1/P2;
- persistência mínima;
- stack tecnológica;
- agentes do produto;
- métricas e riscos do MVP.

### To Build Artifacts

- `project-context/2.build/backend.md`: implementação FastAPI, CrewAI condicional, PostgreSQL, Alembic e revisão jurídica.
- `project-context/2.build/frontend.md`: Angular 21, PrimeNG 21, Nora, chat e rota admin inicial.
- `project-context/2.build/integration.md`: contrato `POST /api/v1/conversations` e validação ponta a ponta.
- `project-context/2.build/qa.md`: evidências locais e riscos residuais.

## 14. Audit

- **agent/persona:** `@system-arch`
- **adapter:** `crewai`
- **date:** `2026-04-19`
- **model used:** `OpenAI Codex via IDE workflow`
- **key assumptions:**
  - MVP com escopo controlado
  - banco inicial simples
  - base de conhecimento curada
  - escalonamento humano como parte nativa do fluxo
- **update:** Codex em 2026-04-26 alinhou o SAD ao runtime atual: PostgreSQL no Dev Container, fluxo condicional CrewAI e revisão jurídica automática.

# Themis HR
## Product Requirements Document (PRD)

Data: 2026-04-19

Baseado em:
- [CONTEXT.md](../../CONTEXT.md)
- [mr.md](./mr.md)

## 1. Executive Summary

### Problem Statement

Equipes de RH lidam com grande volume de solicitações repetitivas e distribuídas entre múltiplos canais, como e-mail, chat, portal e atendimento humano. Esse modelo gera:

- lentidão na resposta;
- inconsistência na aplicação de políticas;
- dependência desnecessária de especialistas para temas simples;
- pouca rastreabilidade de perguntas recorrentes;
- dificuldade para escalar corretamente casos sensíveis.

O mercado já trata esse problema como uma combinação de self-service, knowledge, case management, workflow e AI-assisted service. Os sinais competitivos observados em ServiceNow, Zendesk e Workday validam a oportunidade de um produto focado em experiência do colaborador e eficiência operacional.

### Solution Overview

O Themis HR será um **help desk inteligente para RH**, orientado a agentes de IA, com foco inicial em:

- receber a solicitação do colaborador;
- classificar a intenção;
- consultar a base de conhecimento;
- gerar resposta contextualizada;
- detectar sensibilidade/risco;
- escalar para atendimento humano quando necessário.

O MVP usará:

- **Angular** no frontend;
- **PrimeNG** com preset **Nora** como base visual;
- **FastAPI** no backend;
- **CrewAI** para orquestrar os agentes do produto;
- **Alembic** para versionamento de schema de banco.

### Strategic Rationale

A arquitetura multiagente é adequada porque o fluxo de RH naturalmente separa responsabilidades: intake, classificação, consulta a conhecimento, resposta, análise de sentimento e escalonamento. Em vez de centralizar tudo em um único agente genérico, o Themis HR ganha:

- melhor separação de responsabilidades;
- maior auditabilidade;
- capacidade de aplicar políticas específicas por etapa;
- melhor governança para fallback humano.

## 2. Market Context & User Analysis

### Target Market

#### Primary Market

- Empresas com operação formal de RH e políticas internas documentadas.
- Organizações com volume relevante de dúvidas sobre folha, férias, benefícios, documentos e processos internos.
- Times de RH que querem melhorar tempo de resposta sem contratar proporcionalmente mais atendimento operacional.

#### Early Adopter Profile

- Empresa com handbook, FAQs, políticas e fluxos minimamente estruturados.
- RH com dor visível de repetição operacional.
- Tolerância para iniciar com MVP interno e expandir progressivamente.

### Primary Personas

#### 1. Colaborador

- Quer resolver rapidamente dúvidas e solicitações comuns.
- Não quer navegar em múltiplos sistemas e documentos.
- Espera resposta clara, confiável e, quando necessário, encaminhamento humano.

#### 2. Analista de RH

- Quer reduzir volume de solicitações repetitivas.
- Quer receber apenas casos que realmente precisem de intervenção humana.
- Precisa de histórico e contexto ao receber um caso escalado.

#### 3. Gestor de RH / BP

- Quer visibilidade sobre gargalos, temas recorrentes e qualidade do atendimento.
- Precisa garantir consistência, compliance e experiência do colaborador.

### User Needs Analysis

Necessidades centrais identificadas:

- um ponto único de entrada;
- linguagem clara e objetiva;
- rapidez em temas recorrentes;
- confiança em assuntos sensíveis;
- possibilidade de escalonamento humano;
- histórico do atendimento.

### Competitive Landscape

#### Direct/Adjacent Patterns

- **ServiceNow HRSD**: portal unificado, cases, knowledge, jornadas e IA.
- **Zendesk Employee Service**: foco em employee service com automação e resolução rápida.
- **Workday Self-Service**: autosserviço acoplado ao sistema de RH e payroll.

#### Differentiation Opportunity

O Themis HR pode se diferenciar por:

- foco específico em help desk interno de RH;
- arquitetura modular e explicável;
- implementação incremental;
- maior aderência ao contexto local da empresa;
- possibilidade de operar como camada inteligente acima de processos já existentes.

## 3. Technical Requirements & Architecture

### Product Runtime Architecture

- **Frontend:** Angular
- **UI suite:** PrimeNG
- **Initial preset:** Nora
- **Backend:** FastAPI
- **Multi-agent orchestration:** CrewAI
- **Relational persistence:** stack Python relacional com versionamento por Alembic

### CrewAI Framework Specifications

- Os agentes do produto serão modelados como crew do Themis HR.
- A configuração deve ser preferencialmente orientada por arquivos.
- O fluxo principal do MVP será predominantemente sequencial, com regras claras de passagem de contexto.
- Cada etapa deve produzir saídas úteis para a próxima, e o backend deve manter rastreabilidade do fluxo.

### Core Agent Definitions

#### Intake Agent

- **Role:** normalizar a entrada do usuário
- **Goal:** transformar a solicitação em payload estruturado para o restante do fluxo
- **Inputs:** mensagem do colaborador, metadados da sessão
- **Outputs:** solicitação normalizada

#### Classification Agent

- **Role:** identificar intenção e categoria
- **Goal:** mapear o pedido para domínio de RH e nível de sensibilidade
- **Inputs:** payload normalizado
- **Outputs:** categoria, subcategoria, confiança, flags de risco

#### Knowledge Agent

- **Role:** recuperar conhecimento relevante
- **Goal:** buscar conteúdo de políticas, FAQs e documentos autorizados
- **Inputs:** categoria, termos normalizados, contexto da conversa
- **Outputs:** trechos/fontes/metadata de suporte

#### Response Agent

- **Role:** produzir resposta útil ao colaborador
- **Goal:** responder com base em conhecimento recuperado e políticas válidas
- **Inputs:** conhecimento recuperado, intenção, contexto
- **Outputs:** resposta final candidata

#### Sentiment Agent

- **Role:** detectar emoção e ajustar tom
- **Goal:** moderar a resposta conforme urgência, frustração ou sensibilidade percebida
- **Inputs:** mensagem do colaborador, resposta candidata
- **Outputs:** resposta ajustada e flags de atenção

#### Escalation Agent

- **Role:** decidir sobre handoff humano
- **Goal:** encaminhar quando a confiança for baixa, a política exigir ou o caso for sensível
- **Inputs:** classificação, resposta candidata, flags de risco e sentimento
- **Outputs:** decisão final: responder ou escalar

### Integration Requirements

#### MVP Integrations

- Base de conhecimento interna em formato controlado
- Persistência relacional mínima
- API entre frontend e backend

#### Deferred Integrations

- SSO corporativo
- HRIS/ERP
- sistemas de ticketing externos
- mensageria corporativa

### Infrastructure Specifications

Para o MVP:

- ambiente local e staging simples;
- backend com logs estruturados;
- banco relacional com migrations via Alembic;
- configuração por variáveis de ambiente.

## 4. Functional Requirements

### Core Features (P0)

#### P0.1 Atendimento inicial via chat

**User Story**  
Como colaborador, quero fazer uma pergunta em linguagem natural para receber ajuda imediata sobre temas de RH.

**Acceptance Criteria**

- O sistema recebe mensagem textual.
- A solicitação é enviada ao backend.
- O fluxo multiagente é executado.
- O sistema retorna resposta ou informa escalonamento.

#### P0.2 Classificação de intenção

**User Story**  
Como sistema, quero classificar a solicitação para encaminhar o pedido corretamente.

**Acceptance Criteria**

- O sistema identifica categoria principal.
- O sistema marca nível básico de confiança.
- O sistema registra a classificação para auditoria.

#### P0.3 Consulta à base de conhecimento

**User Story**  
Como colaborador, quero receber respostas fundamentadas nas políticas internas da empresa.

**Acceptance Criteria**

- O sistema busca conteúdo em fontes aprovadas.
- A resposta usa apenas conhecimento permitido.
- A resposta registra referência de origem para auditoria interna.

#### P0.4 Escalonamento para humano

**User Story**  
Como colaborador, quero que meu caso seja encaminhado para humano quando a IA não puder responder com segurança.

**Acceptance Criteria**

- O sistema consegue marcar casos para escalonamento.
- O sistema registra motivo do escalonamento.
- O sistema mantém contexto mínimo do atendimento para handoff.

#### P0.5 Histórico mínimo de atendimento

**User Story**  
Como time de RH, quero ter rastreabilidade básica do atendimento para entender o que foi respondido e o que foi escalado.

**Acceptance Criteria**

- Cada sessão possui identificador.
- Mensagens e decisões principais são persistidas.
- O schema é versionado com Alembic.

### Enhanced Features (P1)

- painel simples para histórico e reabertura de conversas;
- feedback do colaborador sobre utilidade da resposta;
- analytics básicos de deflection, escalonamento e tópicos recorrentes;
- suporte inicial a anexos/documentos controlados.

### Future Features (P2)

- integração com HRIS e SSO;
- proactive assistance;
- automação de jornadas completas;
- multilíngue;
- analytics avançados e gap detection na base de conhecimento.

## 5. Non-Functional Requirements

### Performance Requirements

- tempo de resposta do fluxo simples percebido como quase imediato;
- comportamento degradado com fallback explícito quando necessário;
- suporte a múltiplas sessões simultâneas no ambiente de teste/piloto.

### Security & Compliance

- dados de colaboradores devem ser tratados como sensíveis;
- variáveis secretas fora do código;
- trilha mínima de auditoria;
- regras de escalonamento para casos sensíveis;
- arquitetura preparada para políticas de acesso mais rígidas no pós-MVP.

### Scalability & Reliability

- desenho modular;
- persistência versionada;
- capacidade de trocar SQLite por PostgreSQL sem redefinir a lógica funcional;
- tolerância a falhas parciais no pipeline com respostas seguras.

## 6. User Experience Design

### Interface Requirements

- interface web Angular;
- base visual PrimeNG;
- preset inicial Nora;
- experiência simples, enterprise e responsiva;
- chat como principal ponto de entrada do MVP.

### Agent Interaction Design

- o usuário não precisa conhecer a divisão entre agentes;
- o sistema deve transmitir clareza sobre o próximo passo;
- se escalado, o usuário deve saber que o caso saiu do fluxo automatizado;
- o tom deve ser profissional, empático e objetivo.

## 7. Success Metrics & KPIs

### Business Metrics

- redução do volume de perguntas repetitivas atendidas manualmente;
- aumento do uso de self-service;
- tempo médio de primeira resposta.

### Technical Metrics

- taxa de classificação aceitável;
- taxa de respostas com suporte em conhecimento recuperado;
- taxa de escalonamento por categoria;
- erros por fluxo e disponibilidade básica.

### User Experience Metrics

- satisfação com a resposta;
- taxa de resolução sem escalonamento para domínios elegíveis;
- abandono do fluxo;
- feedback negativo por resposta imprecisa.

## 8. Implementation Strategy

### Phase 1 (MVP)

- chat Angular com PrimeNG/Nora;
- backend FastAPI;
- crew inicial com 6 agentes do produto;
- base de conhecimento inicial;
- persistência mínima;
- escalonamento básico;
- logs e auditoria essenciais.

### Phase 2 (Enhanced)

- dashboard operacional;
- feedback loop;
- analytics básicos;
- melhoria da curadoria de conhecimento;
- integrações pontuais.

### Phase 3 (Scale)

- integrações com ecossistema corporativo;
- maior automação de jornadas;
- governança avançada;
- analytics e operações em escala.

### Resource Requirements

- Product/Discovery
- Arquitetura
- Backend
- Frontend
- QA
- Sponsor de RH / curadoria de conteúdo

### Risk Mitigation

- limitar escopo do MVP;
- escalar casos sensíveis;
- manter base de conhecimento controlada;
- versionar schema e artefatos;
- revisar respostas e fluxos com stakeholder de RH.

## 9. Launch & Go-to-Market Strategy

### Beta Testing Plan

- piloto interno com grupo controlado;
- foco em 3 a 5 temas de RH;
- coleta de feedback qualitativo e quantitativo;
- revisão semanal de gaps de conhecimento.

### Launch Strategy

O lançamento inicial é interno, como produto corporativo. O objetivo do MVP não é monetização externa, mas prova de valor operacional e fundação para evolução do atendimento inteligente de RH.

### Success Criteria

- fluxo ponta a ponta funcionando;
- respostas úteis em tópicos P0;
- escalonamento funcional;
- rastreabilidade mínima implantada;
- aderência do RH patrocinador ao piloto.

## Open Questions

1. O MVP terá autenticação desde o primeiro corte ou operará inicialmente em contexto controlado?
2. O banco inicial compartilhado será SQLite apenas para desenvolvimento ou já haverá PostgreSQL em staging?
3. Qual será a fonte primária da base de conhecimento no primeiro corte: handbook, FAQ, políticas isoladas, ou combinação?
4. Quais categorias exigem escalonamento obrigatório desde o dia 1?

## Product Decisions Already Locked

- Angular no frontend
- PrimeNG como UI suite
- Nora como preset inicial
- FastAPI no backend
- CrewAI na orquestração dos agentes do produto
- Alembic no versionamento de schema

## Traceability to Research

- necessidade de self-service: validada por ServiceNow, Zendesk e Workday;
- importância de handoff humano: reforçada por SHRM e pelo estudo da SAP;
- stack técnico: coerente com documentação oficial de CrewAI, PrimeNG, FastAPI, SQLAlchemy e Alembic.

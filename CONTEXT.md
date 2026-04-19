# 🏛️ Themis HR — Sistema Multiagente de Suporte ao RH

## 📌 Visão Geral

**Themis HR** é um sistema de suporte ao colaborador baseado em **arquitetura multiagente**, inspirado na deusa grega **Themis**, símbolo de justiça, ordem e equilíbrio.

O objetivo do sistema é transformar o atendimento tradicional de RH em um ecossistema inteligente, automatizado e adaptativo, capaz de:

- responder dúvidas de colaboradores
- aplicar políticas internas
- analisar contexto e sentimento
- escalar para humanos quando necessário
- aprender continuamente

---

## 🎯 Objetivo do Projeto

Construir uma solução de help desk para RH utilizando:

- **Frontend**: Angular
- **UI Suite**: PrimeNG
- **Backend**: Python (FastAPI)
- **Motor multiagente**: CrewAI
- **Versionamento do banco**: Alembic
- **Metodologia de desenvolvimento**: AAMAD

Para o MVP, a persistência de dados pode existir de forma mínima e controlada, principalmente para suportar trilha de atendimento, contexto conversacional, escalonamentos e evolução segura do schema.

---

## 🧠 Arquitetura Conceitual

O sistema é dividido em duas camadas principais:

### 1. Development Crew (AAMAD)

Equipe de agentes responsável por **desenvolver o sistema**.

### 2. Helpdesk Crew (Themis HR)

Equipe de agentes responsável por **operar o atendimento ao usuário final**.

---

## 🧩 Distinção Entre As Duas Camadas

É importante separar claramente os dois usos de "agentes" neste projeto:

- **Camada de desenvolvimento**
  - usa o **AAMAD** como metodologia de trabalho
  - é operada por meio do **VS Code / Cursor / Copilot**
  - organiza personas como Product, Architect, Backend, Frontend e QA
  - ajuda a equipe a **construir** o sistema

- **Camada do produto**
  - usa o **CrewAI** como motor de orquestração
  - executa os agentes reais do Themis HR no backend
  - implementa o fluxo de atendimento ao colaborador
  - faz o sistema **funcionar em produção**

Em outras palavras:

- **AAMAD + IDE** constroem o produto
- **CrewAI + FastAPI** executam o produto

O CrewAI não é a base operacional dos agentes de desenvolvimento. Na camada de desenvolvimento, ele pode inspirar o desenho de trabalho, mas a interação principal acontece no IDE, com os artefatos e personas do bootstrap.

---

## 👥 Development Crew (AAMAD)

Agentes responsáveis pela construção do sistema:

- **Product Agent**
  - Define requisitos e user stories

- **Architect Agent**
  - Define arquitetura, padrões e contratos

- **Backend Agent**
  - Implementa APIs (FastAPI)
  - Regras de negócio

- **Frontend Agent**
  - Implementa UI Angular
  - Usa PrimeNG como alicerce visual da aplicação
  - Integra com backend

- **QA Agent**
  - Cria testes e cenários

- **Reviewer Agent**
  - Garante consistência e qualidade

---

## 🤖 Helpdesk Crew (Themis HR)

Agentes responsáveis pelo atendimento:

- **Intake Agent**
  - Recebe a solicitação do usuário
  - Normaliza entrada

- **Classification Agent**
  - Identifica intenção (ex: férias, folha, benefícios)

- **Knowledge Agent (RAG)**
  - Consulta base de conhecimento
  - Retorna informações relevantes

- **Response Agent**
  - Gera resposta ao usuário

- **Sentiment Agent**
  - Analisa emoção do usuário
  - Ajusta tom da resposta

- **Escalation Agent**
  - Decide quando escalar para humano

---

## 🔄 Fluxo do Sistema

```text
Usuário → Intake Agent
        ↓
Classification Agent
        ↓
Knowledge Agent (RAG)
        ↓
Response Agent
        ↓
Sentiment Agent
        ↓
Escalation Agent (se necessário)
        ↓
Resposta final ou atendimento humano

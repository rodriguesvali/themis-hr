# Themis HR System Architecture Document Template

## Context & Instructions

Generate a System Architecture Document for **Themis HR**, a multi-agent HR helpdesk system.

The architecture must stay aligned with the current project context:

- Frontend in **Angular**
- Backend in **Python + FastAPI**
- Multi-agent runtime in **CrewAI**
- Database schema versioning with **Alembic**
- Knowledge retrieval and policy guidance as core capabilities
- Human escalation as an explicit workflow concern

Use MVP thinking: deliver the minimum architecture that can support an end-to-end HR support flow with room for controlled expansion.

## Input Requirements

- **Product Context:** `CONTEXT.md`
- **Market Research:** `project-context/1.define/mr.md`
- **PRD:** `project-context/1.define/prd.md`
- **Scope:** Default to MVP unless instructed otherwise

## Required Sections

### 1. Executive Summary

- Business objective
- MVP scope
- Architecture overview
- Main trade-offs and assumptions

### 2. Architectural Drivers

- Functional requirements
- Quality attributes
- Constraints
- Risks
- Compliance and policy considerations relevant to HR workflows

### 3. System Context

- Primary users and actors
- External systems and dependencies
- Internal boundaries between frontend, backend, CrewAI runtime, knowledge base, and escalation flow

### 4. Solution Overview

Describe the end-to-end shape of the system, covering:

- Angular application responsibilities
- FastAPI responsibilities
- CrewAI responsibilities
- Knowledge retrieval / RAG responsibilities
- Escalation and fallback responsibilities

### 5. Frontend Architecture

Specify:

- Angular application structure
- Routing and feature modules or standalone component strategy
- State and API communication strategy
- UX flow for HR support conversations
- Error, loading, and escalation states

### 6. Backend Architecture

Specify:

- FastAPI service structure
- Endpoint design for MVP flows
- Validation, error handling, and observability approach
- Separation between API layer, orchestration layer, and domain logic
- persistence boundaries for the MVP
- migration strategy using Alembic

### 7. Multi-Agent Architecture

Define the MVP set of helpdesk agents, including:

- Intake Agent
- Classification Agent
- Knowledge Agent
- Response Agent
- Sentiment Agent
- Escalation Agent

For each one, describe:

- responsibility
- inputs
- outputs
- dependencies
- failure handling

Also define:

- task sequencing
- context passing
- auditability expectations
- configuration approach for CrewAI

### 8. Data and Knowledge Architecture

Describe:

- conversation data model at MVP level
- policy and knowledge sources
- retrieval approach
- data sensitivity and privacy concerns
- retention boundaries for MVP
- whether the MVP uses SQLite, PostgreSQL, or another store and why
- how Alembic will manage schema evolution

### 9. Security and Compliance

Cover:

- authentication and authorization assumptions
- protection of employee data
- audit logging expectations
- secrets management
- legal/compliance considerations to surface for later refinement

### 10. Deployment and Environments

Describe:

- local development setup
- test/staging/production expectations
- deployment topology at MVP level
- environment variables and configuration boundaries

### 11. Testing and Quality Strategy

Define:

- unit testing expectations
- integration testing expectations
- end-to-end testing expectations
- architecture validation checkpoints

### 12. Decisions, Assumptions, and Future Work

- ADR-style decisions
- open questions
- deferred items
- post-MVP extensions

### 13. Traceability

Map the architecture back to:

- `CONTEXT.md`
- `mr.md`
- `prd.md`

### 14. Audit

Record:

- agent/persona
- adapter
- date
- model used
- key assumptions

## Output Rules

- Write the final document to `project-context/1.define/sad.md`
- Preserve the section headings above
- Use plain Markdown
- Do not introduce a different frontend or backend stack unless the inputs explicitly require a change

# Themis HR
## System Functional Specification: Conversation Flow

Data: 2026-04-26
Responsável alvo: `@system-arch`
Status: aprovado como especificação do MVP local atual.

## 1. Identification

- Feature ID: `SFS-CONVERSATION-FLOW`
- Feature name: Fluxo de conversa com roteamento condicional
- Related PRD references: P0.1, P0.2, P0.3, P0.4, P0.5
- Related SAD references: seções 6, 7, 8, 11 e 12

## 2. Purpose

Permitir que o colaborador envie uma pergunta de RH e receba resposta automática quando houver cobertura segura, ou escalonamento humano quando o caso for sensível, ambíguo ou não coberto.

## 3. Scope

Inclui:

- criação de conversa;
- persistência da mensagem do usuário;
- classificação por `principal_agent`;
- roteamento para um especialista sob demanda;
- escalonamento direto para alta sensibilidade ou assuntos gerais;
- persistência da resposta e metadados principais.

Exclui:

- autenticação real;
- múltiplas mensagens dentro da mesma conversa via endpoint dedicado;
- fila assíncrona, SSE ou WebSocket;
- analytics e dashboard operacional completos.

## 4. Actors

- Primary actor: Colaborador
- Supporting actors: FastAPI backend, `principal_agent`, especialistas de domínio, banco relacional, frontend Angular

## 5. Inputs

- `user_id`: string opcional; no MVP frontend usa `"1"`.
- `message`: texto obrigatório com a solicitação do colaborador.
- Configuração runtime: `DATABASE_URL`, `CREWAI_PROVIDER`, `CREWAI_MODEL`, `GOOGLE_API_KEY`.

## 6. Processing Rules

1. `POST /api/v1/conversations` cria uma nova conversa.
2. A mensagem do usuário é persistida em `messages`.
3. `ThemisHRCrew().run(message)` executa em thread separada para não bloquear o event loop.
4. `principal_agent` retorna JSON com `area_key`, `category`, `sensitivity` e `reason`.
5. Se `sensitivity = alta` ou `area_key = assuntos_gerais`, o sistema escalona sem chamar especialista.
6. Se houver especialista configurado, somente ele recebe a pergunta e a base de conhecimento da área.
7. Confiança baixa ou falta de cobertura força escalonamento.
8. Respostas automáticas seguem para revisão jurídica conforme `SFS-LEGAL-REVIEW`.
9. A mensagem final da Themis é persistida com categoria, especialista, confiança e metadados de escalonamento/revisão.

## 7. Outputs

Resposta HTTP:

- `conversation_id`: identificador da conversa;
- `reply`: resposta final ou mensagem de handoff;
- `status`: `active` ou `escalated`.

Efeitos persistidos:

- conversa em `conversations`;
- mensagem do usuário;
- mensagem da Themis;
- status de escalonamento quando aplicável.

## 8. Error Handling

- Falha na CrewAI retorna fallback técnico amigável.
- Área sem especialista configurado gera escalonamento.
- JSON inválido na revisão jurídica gera escalonamento por segurança.
- Falha na ferramenta da CLT gera escalonamento por segurança.

## 9. API and Integration Notes

- Frontend usa `ChatService` com `POST /api/v1/conversations`.
- Backend usa FastAPI, SQLAlchemy e Alembic.
- Contrato atual não mantém conversa longa pelo mesmo endpoint; cada envio abre nova conversa.
- Recuperação de histórico existe no backend via `GET /api/v1/conversations/{conversation_id}`, mas ainda não está integrada ao frontend.

## 10. Acceptance Criteria

- O usuário consegue enviar mensagem pelo frontend.
- O backend cria conversa e persiste mensagens.
- Uma pergunta coberta retorna resposta automática revisada.
- Caso sensível retorna status `escalated`.
- Erros de runtime não expõem stack trace ao usuário.

## 11. Assumptions and Open Questions

- Assumption: MVP local aceita HTTP síncrono enquanto a latência for tolerável para demonstração.
- Assumption: `user_id = "1"` é placeholder, não autenticação.
- Open question: a próxima iteração deve preservar conversa multi-turn no mesmo `conversation_id`?
- Open question: o processamento assíncrono entra antes de staging?

## Sources

- `project-context/1.define/prd.md`
- `project-context/1.define/sad.md`
- `backend/src/themis_hr_api/main.py`
- `backend/src/themis_hr_api/orchestration/crew.py`
- `frontend/src/app/chat.service.ts`

## Audit

- Criado por Codex em 2026-04-26 para formalizar o runtime atual após recriação AAMAD.

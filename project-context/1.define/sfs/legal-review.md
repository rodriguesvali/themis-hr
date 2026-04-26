# Themis HR
## System Functional Specification: Legal Review

Data: 2026-04-26
Responsável alvo: `@system-arch`
Status: aprovado como salvaguarda do MVP local atual.

## 1. Identification

- Feature ID: `SFS-LEGAL-REVIEW`
- Feature name: Revisão jurídica automática antes da resposta ao colaborador
- Related PRD references: P0.3, P0.4, P0.5; NFR Security & Compliance
- Related SAD references: seções 7, 8, 9, 11 e 12

## 2. Purpose

Reduzir risco de resposta automática inadequada em temas trabalhistas, usando uma revisão conservadora apoiada por consulta textual ao PDF local da CLT antes de enviar a resposta ao colaborador.

## 3. Scope

Inclui:

- consulta textual ao PDF da CLT;
- passagem de trechos recuperados ao `legal_reviewer_agent`;
- avaliação de aprovação, risco, escalonamento e fundamento legal;
- persistência de metadados jurídicos na mensagem final.

Exclui:

- parecer jurídico formal;
- substituição de advogado ou analista humano;
- RAG vetorial completo;
- persistência detalhada de todos os trechos/tool calls em tabela própria.

## 4. Actors

- Primary actor: Backend FastAPI / CrewAI runtime
- Supporting actors: especialista de domínio, `legal_reviewer_agent`, ferramenta `Consultar CLT`, PDF local da CLT, banco relacional

## 5. Inputs

- pergunta original do colaborador;
- categoria e especialista acionado;
- resposta candidata do especialista;
- confiança e motivo de escalonamento do especialista;
- trechos recuperados do PDF da CLT;
- variável `CLT_PDF_PATH` quando o caminho padrão não se aplica.

## 6. Processing Rules

1. O backend monta uma consulta combinando categoria, pergunta e resposta candidata.
2. A ferramenta `Consultar CLT` busca termos no PDF local e retorna até quatro trechos relevantes.
3. O `legal_reviewer_agent` recebe a pergunta, resposta candidata, contexto de roteamento, confiança e trechos recuperados.
4. O revisor retorna JSON com `approved`, `final_answer`, `risk_level`, `should_escalate`, `legal_notes` e `legal_basis`.
5. Se `approved = false`, `should_escalate = true` ou `risk_level` for `medio`/`alto`, a resposta final vira handoff humano.
6. Se aprovado com risco baixo, o sistema envia a resposta revisada ou preserva a resposta do especialista.
7. Falhas de ferramenta, JSON inválido ou exceções geram escalonamento por segurança.

## 7. Outputs

Metadados persistidos em `messages`:

- `legal_reviewed`;
- `legal_risk_level`;
- `legal_notes`;
- `legal_basis`;
- `escalation_reason` quando aplicável;
- `confidence` final.

## 8. Error Handling

- PDF ausente ou ilegível: escalonamento.
- Consulta sem termo suficiente: escalonamento se o revisor não aprovar com segurança.
- JSON inválido do revisor: escalonamento.
- Risco médio/alto: escalonamento obrigatório.

## 9. API and Integration Notes

- A revisão é interna ao backend e não muda o contrato HTTP atual.
- O frontend recebe apenas `reply` e `status`.
- Auditoria detalhada dos trechos exatos ainda deve evoluir para tabela própria.

## 10. Acceptance Criteria

- Resposta aprovada com risco baixo chega ao colaborador.
- Risco médio/alto gera escalonamento.
- Falha da ferramenta CLT gera escalonamento.
- JSON inválido do revisor gera escalonamento.
- Metadados jurídicos são persistidos na mensagem final.

## 11. Assumptions and Open Questions

- Assumption: busca textual no PDF é suficiente para demonstração local controlada.
- Assumption: revisão automática é salvaguarda, não decisão jurídica final.
- Open question: quais trechos legais precisam ser persistidos integralmente?
- Open question: qual nível de revisão humana será exigido antes de piloto com dados reais?

## Sources

- `backend/src/themis_hr_api/orchestration/crew.py`
- `backend/tests/test_legal_review.py`
- `backend/docs/consolidacao_leis_trabalho.pdf`
- `project-context/2.build/backend.md`
- `project-context/2.build/qa.md`

## Audit

- Criado por Codex em 2026-04-26 para formalizar a salvaguarda jurídica do runtime atual.

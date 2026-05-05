# Themis HR
## Open Questions

Data: 2026-05-05
Responsável: consolidação AAMAD/Codex
Status: ativo; deve ser revisado antes de nova iteração de build ou gate de demonstração.

## Product

1. O MVP terá autenticação no próximo corte ou continuará com `user_id = "1"` em ambiente controlado?
2. Quais categorias de RH devem ter escalonamento obrigatório desde o dia 1?
3. O histórico de conversa precisa entrar no escopo imediato da próxima iteração?

## Architecture

1. O padrão runtime aprovado passa a ser definitivamente `principal_agent + especialista sob demanda + legal_reviewer_agent`?
2. A estratégia de busca textual na CLT é suficiente para demonstração ou deve evoluir para RAG vetorial antes do próximo gate?
3. A próxima arquitetura deve migrar o endpoint síncrono para SSE, WebSocket, polling com fila ou manter HTTP síncrono no piloto?

## Data, Security, and Compliance

1. Qual será a política mínima de retenção de conversas e metadados de revisão jurídica?
2. Quais metadados de tool calls e trechos legais precisam ser persistidos em tabela própria?
3. Haverá requisito mínimo de LGPD/security review antes da primeira demonstração para stakeholders?

## Operations

1. Qual provider/modelo LLM será o padrão oficial do MVP?
2. Quando existir staging, qual será o processo de aplicar migrations e validar o banco?

## Resolved for Demo Local

1. Para demonstração local controlada, `GOOGLE_API_KEY` é a variável canônica de chave LLM.
2. `GEMINI_API_KEY` permanece aceito apenas como fallback legado quando `GOOGLE_API_KEY` estiver ausente.
3. Se ambas estiverem configuradas, o backend registra warning e usa `GOOGLE_API_KEY`.

## Audit

- Consolidado por Codex em 2026-04-26 a partir de PRD, SAD, QA e release evidence.
- Atualizado por Codex em 2026-05-05 para reclassificar a decisão de chave LLM no gate de demo local.

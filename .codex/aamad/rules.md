# AAMAD Rules for Codex

## Core Rules

- Context first: scope and architecture should trace back to PRD, SAD, user stories, or explicit user direction.
- Single responsibility: each persona or delegated task owns a clear module and output artifact.
- Deterministic work: prefer repeatable commands, stable file outputs, and explicit verification.
- Preserve existing conventions: local repo patterns override generic AAMAD defaults.
- No secrets in artifacts: document variable names and configuration shape, never secret values.
- For Themis HR, keep a strict distinction between AAMAD development personas and product runtime agents implemented with CrewAI.
- Treat `.codex/aamad/` as the Codex-native AAMAD configuration; `.github/` and `.cursor/` remain compatibility/reference material.

## Artifact Rules

- Keep artifacts concise and actionable.
- Each artifact should include Sources, Assumptions, Open Questions, Verification, and Handoff Notes when relevant.
- Record known gaps rather than hiding incomplete work.
- When implementation diverges from PRD/SAD, update the affected Define artifact or create an SFS before treating the change as accepted architecture.
- For CrewAI runtime changes, document agent/task shape, model/provider assumptions, memory behavior, tool usage, and audit gaps in `backend.md` or an SFS.

## Failure Policy

- If required inputs are missing, continue only when a reasonable assumption is low risk.
- Record assumptions and open questions.
- Halt and ask the user when the next step would be destructive, high-risk, or impossible to infer safely.

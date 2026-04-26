# AAMAD Codex Workflow

## Purpose

This repository uses AAMAD as a Codex-native operating model for Themis HR. AAMAD structures work into Define, Build, and Deliver phases while Codex handles orchestration, implementation, verification, and optional delegated subagent work.

The current product stack is Angular + PrimeNG/Nora, FastAPI, PostgreSQL through the dev container, Alembic, and CrewAI/Gemini for the help desk runtime. The current MVP is already past local validation and is approved only for controlled local demonstration, not production rollout.

## Define

- Clarify the user goal, users, constraints, scope, non-goals, acceptance criteria, and risks.
- Produce or update `project-context/1.define/mrd.md`, `mr.md`, `prd.md`, `sad.md`, `sfs/*.md`, and `open-questions.md` as needed.
- Do not move into broad implementation until the relevant Define artifacts are sufficient for the requested change.

## Build

- Split implementation into bounded modules with explicit ownership.
- Keep the immediate critical path in the main Codex thread.
- When the user explicitly authorizes subagents, delegate independent sidecar tasks to Codex `explorer` or `worker` agents.
- Require every implementation slice to update its matching artifact under `project-context/2.build/`.

## Deliver

- Verify the integrated system with deterministic checks.
- Document release, deployment, operations, access, monitoring, rollback, and remaining risk under `project-context/3.deliver/`.
- Ask for human approval before deployment or other high-impact operations.

## Current Phase Snapshot

- Define: complete for MVP, with `mr.md`, `mrd.md`, `prd.md`, `sad.md`, and SFS artifacts.
- Build: implemented for frontend, backend, integration, and QA handoffs.
- Deliver: local release evidence exists; deployment and operations artifacts document controlled local demo only.

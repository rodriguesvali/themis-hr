# AAMAD Copilot to Codex Mapping

Este documento descreve como a estrutura do AAMAD originalmente preparada para GitHub Copilot foi adaptada para uso com Codex neste repositório.

## Resumo

No Copilot, o comportamento é distribuído entre:

- `.github/agents/*.agent.md`
- `.github/instructions/*.instructions.md`
- `.github/prompts/*.prompt.md`

No Codex, a orientação operacional do projeto foi consolidada em:

- `AGENTS.md`

Os templates e artefatos de projeto permanecem os mesmos:

- `.cursor/templates/`
- `project-context/`

## Mapeamento Estrutural

| Origem Copilot | Papel | Destino no Codex |
| --- | --- | --- |
| `.github/agents/*.agent.md` | definição de persona, responsabilidades, handoffs e comandos | seção de personas dentro de `AGENTS.md` |
| `.github/instructions/aamad-core.instructions.md` | regras globais do framework | seções `Princípios AAMAD` e `Como O Codex Deve Operar Neste Repositório` em `AGENTS.md` |
| `.github/instructions/development-workflow.instructions.md` | fluxo modular de execução | seção `Workflow` em `AGENTS.md` |
| `.github/instructions/epics-index.instructions.md` | índice de epics e artefatos | seções `Epics Index` e `Matriz de Personas` em `AGENTS.md` |
| `.github/instructions/adapter-registry.instructions.md` | seleção do adapter | seção `Adapter Atual` em `AGENTS.md` |
| `.github/instructions/adapter-crewai.instructions.md` | diretrizes específicas para CrewAI | refletido nas regras das personas `@system-arch` e `@backend-eng`, além do adapter atual em `AGENTS.md` |
| `.github/prompts/phase-1-define.prompt.md` | prompt operacional da fase Define | continua como referência; o Codex passa a seguir o fluxo descrito em `AGENTS.md` e os templates em `.cursor/templates/` |

## Diferenças de Modelo Operacional

### GitHub Copilot

- usa arquivos `.agent.md` com frontmatter próprio
- suporta handoff por UI e instruções segmentadas por arquivo
- separa regras globais e personas em diretórios distintos

### Codex

- lê principalmente `AGENTS.md` como contrato do repositório
- não depende de handoff por botão
- funciona melhor quando regras, workflow e contratos de persona estão consolidados em um ponto central

## Convenção Recomendada Daqui em Diante

- Tratar `AGENTS.md` como a fonte canônica para o Codex
- Manter `.github/` como espelho compatível com Copilot, se o time continuar usando os dois ambientes
- Ao alterar uma persona, atualizar primeiro o contrato em `AGENTS.md`
- Depois, se necessário, refletir a mesma mudança em `.github/agents/` e `.github/instructions/`

## O Que Não Mudou

- Estrutura de `project-context/`
- Templates em `.cursor/templates/`
- Fases `Define -> Architecture -> Build -> Integration -> Validation -> Deliver`
- Adapter de runtime previsto para o produto: `CrewAI`

## Limite Desta Conversão

Esta adaptação converteu a **camada de instrução e operação no IDE**.

Ela não altera:

- a runtime do produto
- a orquestração CrewAI do backend
- a estrutura funcional da aplicação


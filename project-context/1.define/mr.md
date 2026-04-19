# Themis HR
## Market Research (MR)

Data: 2026-04-19

## Executive Summary

O Themis HR ataca um problema recorrente em operações de RH: alto volume de dúvidas repetitivas, fragmentação entre canais, dependência de especialistas para solicitações simples e necessidade de escalar casos sensíveis com segurança. A demanda por autoatendimento inteligente já é validada por players de mercado como ServiceNow, Zendesk e Workday, que posicionam employee service, HR case management, AI self-service e knowledge-backed resolution como pilares do atendimento interno moderno. Em paralelo, a adoção de IA no trabalho já saiu do campo experimental: a Microsoft reportou em 8 de maio de 2024 que funcionários estão experimentando IA em larga escala no ambiente de trabalho, e a SHRM aponta que a expansão do uso de IA em RH exige equilíbrio entre automação e julgamento humano.

Do ponto de vista técnico, o projeto é viável com o stack já escolhido: Angular no frontend, PrimeNG como base visual, FastAPI no backend, CrewAI para orquestração dos agentes do produto e Alembic para versionamento do banco. A documentação oficial do CrewAI recomenda configuração baseada em YAML para crews e tarefas, o que se alinha bem à governança já definida no bootstrap do AAMAD. Na camada de dados, SQLAlchemy oferece uma base madura para persistência relacional, enquanto Alembic traz autogeração e controle evolutivo do schema. No frontend, PrimeNG oferece temas, design tokens e presets prontos, inclusive o preset Nora, escolhido para o MVP.

A recomendação estratégica é construir um MVP focado em um fluxo muito claro: receber a solicitação do colaborador, classificar a intenção, consultar a base de conhecimento, responder com contexto e escalar para humano quando houver incerteza, sensibilidade ou falta de cobertura. O posicionamento ideal do Themis HR não é competir frontalmente, de início, com suítes completas de employee service, mas provar valor como uma camada de atendimento inteligente orientada a políticas internas, auditabilidade e experiência do colaborador.

## Detailed Findings by Dimension

### 1. Market Analysis & Opportunity Assessment

#### Key Insights

- O mercado já validou o modelo de employee service com autoatendimento, cases, knowledge e assistência por IA. A página de HR Service Delivery da ServiceNow destaca IA para requests, automação de jornadas, “AI front door”, self-service agentic e escalonamento para humanos.
- O atendimento interno ao colaborador está sendo tratado pelos fornecedores de mercado com a mesma lógica de atendimento ao cliente: portal único, busca, chat, workflows, routing e produtividade do agente humano.
- A principal lacuna para projetos como o Themis HR está na customização ao contexto específico da empresa: políticas internas, tom institucional, governança local, priorização por sensibilidade do caso e integração progressiva sem adoção de uma suíte monolítica.
- Existe uma oportunidade clara para uma solução com foco em RH que entregue valor rápido em perguntas recorrentes e handoff humano seguro, sem tentar cobrir, no MVP, todas as funções de um HRIS ou de uma plataforma enterprise.

#### Data Points

- A ServiceNow descreve HRSD como forma de “reduce repetitive tasks” e “improve everyday employee productivity”, com AI front door, self-service agentic e agentes de IA para HR ([ServiceNow HRSD product page](https://www.servicenow.com/products/hr-service-delivery.html.html)).
- A mesma página cita exemplos de resultado como `76% self-service deflection achieved`, `80% increase in HR agent efficiency` e `€600K help desk cost savings`, apresentados como customer outcomes da plataforma ([ServiceNow HRSD product page](https://www.servicenow.com/products/hr-service-delivery.html.html)).
- A Zendesk posiciona Employee Service como solução para HR e IT, afirmando que a IA ajuda a guiar equipes por perguntas rotineiras e acelera a resolução de solicitações internas ([Zendesk Employee Service](https://www.zendesk.com/employee-service/)).
- A Workday posiciona self-service com agentes de IA para reduzir payroll inquiries, melhorar compreensão do holerite e integrar case management dentro do sistema de RH e payroll ([Workday Employee Self-Service](https://www.workday.com/en-us/products/payroll/employee-self-service.html)).
- A Microsoft e o LinkedIn registraram, em 2024, que a experimentação com IA no trabalho já é ampla e que cabe à liderança canalizar essa adoção para impacto real de negócio ([Microsoft Work Trend Index 2024](https://news.microsoft.com/source/2024/05/08/microsoft-and-linkedin-release-the-2024-work-trend-index-on-the-state-of-ai-at-work/)).

#### Implications

- O Themis HR deve ser pensado como **employee service especializado em RH**, não apenas como “chatbot”.
- O MVP precisa deixar claro desde o início: portal/chat único, base de conhecimento, tracking mínimo do atendimento e escalonamento humano.
- O diferencial não estará em “ter IA”, mas em **governança, contexto e precisão nas respostas baseadas em políticas**.

### 2. Technical Feasibility & Requirements Analysis

#### Key Insights

- O CrewAI é aderente ao caso porque suporta crews com configuração em YAML, separação entre agents/tasks e um fluxo suficientemente estruturado para um sistema multiagente de atendimento.
- O caso de uso exige forte acoplamento com base de conhecimento e handoff humano, o que favorece uma arquitetura modular em vez de um agente único.
- FastAPI, SQLAlchemy e Alembic formam uma base técnica madura para um backend auditável e evolutivo.
- PrimeNG, com preset Nora, oferece uma base visual enterprise coerente com o contexto do produto.

#### Data Points

- A documentação do CrewAI recomenda criação de crews usando configuração em YAML, apontando esse caminho como “recommended” ([CrewAI Crews](https://docs.crewai.com/en/concepts/crews)).
- O guia de instalação do CrewAI também recomenda scaffolding estruturado com `agents.yaml` e `tasks.yaml` ([CrewAI Installation](https://docs.crewai.com/en/installation)).
- A própria documentação do CrewAI sobre coding tools reforça o papel de `AGENTS.md` como fonte de verdade para agentes de código e IDEs ([CrewAI Coding Tools](https://docs.crewai.com/en/guides/coding-tools/agents-md)).
- FastAPI deixa explícito que não força um ORM específico e pode trabalhar com qualquer banco SQL suportado pela camada ORM adotada; o tutorial oficial mostra um caminho com SQLModel e destaca compatibilidade com SQLite, PostgreSQL, MySQL, Oracle e SQL Server ([FastAPI SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)).
- SQLAlchemy 2.0 segue sendo a referência madura de ORM no ecossistema Python ([SQLAlchemy ORM docs](https://docs.sqlalchemy.org/en/20/orm/)).
- Alembic é a ferramenta oficial de migrations associada ao ecossistema SQLAlchemy e suporta autogenerate comparando metadata com o schema atual do banco ([Alembic docs](https://alembic.sqlalchemy.org/), [Alembic autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)).
- PrimeNG oferece 4 presets built-in e uma arquitetura baseada em design tokens; Nora é descrito como inspirado em aplicações enterprise ([PrimeNG theming](https://v19.primeng.org/theming), [PrimeNG configuration](https://v20.primeng.org/configuration)).

#### Implications

- O design do Themis HR deve partir de **múltiplos agentes especializados**.
- A configuração dos agentes do produto deve ser rastreável e orientada a arquivos.
- O MVP deve incluir persistência mínima, mas já nascer com schema versionado.

### 3. User Experience & Workflow Analysis

#### Key Insights

- Os exemplos de mercado convergem para um padrão: portal único, autoatendimento, knowledge, workflows e case management.
- Para RH, o usuário não quer “falar com IA” por si só; ele quer resolver rápido assuntos como folha, benefícios, férias, documentos, onboarding e employee relations.
- A experiência precisa combinar resposta imediata com a opção de escalar para um humano quando o caso não for claro, seguro ou apropriado para automação.
- Transparência e sensação de controle são fundamentais, especialmente quando o tema envolve dados pessoais, benefícios, pagamento ou relações trabalhistas.

#### Data Points

- A ServiceNow documenta case creation self-service em categorias como Benefits, Employee Data Management, Employee Relations, HR Systems, Payroll e Talent Management ([ServiceNow HR Case Management](https://www.servicenow.com/docs/r/washingtondc/employee-service-management/hr-service-delivery/c_HRCaseManagement.html)).
- A ServiceNow também documenta que um caso pode ser transferido ou escalado quando a primeira classificação não é a mais adequada ([ServiceNow HR Case Management](https://www.servicenow.com/docs/r/washingtondc/employee-service-management/hr-service-delivery/c_HRCaseManagement.html)).
- A Zendesk posiciona Employee Service como “designed for every employee” e orientado a rápida configuração e resolução ([Zendesk Employee Service](https://www.zendesk.com/employee-service/)).
- Um estudo com SAP sobre um chatbot de HR support com RAG e human-in-the-loop conclui que esse tipo de abordagem pode ser eficiente e escalável quando a qualidade da resposta é tratada como problema central do design ([arXiv 2407.05925](https://arxiv.org/abs/2407.05925)).

#### Implications

- O MVP deve começar com poucos fluxos, mas altamente claros.
- A UX precisa explicitar quando a resposta veio de conhecimento conhecido e quando um caso será escalado.
- Chat é útil, mas deve existir estrutura de classificação e trilha do atendimento por trás.

### 4. Production & Operations Requirements

#### Key Insights

- RH é um domínio sensível; logs, trilha de atendimento, proteção de dados e governança são requisitos desde cedo.
- Não basta responder; é preciso registrar o atendimento, permitir revisão e ter base para melhoria contínua.
- Persistência mínima já faz sentido no MVP para histórico conversacional, status de caso, escalonamento e evidência operacional.
- O custo e a complexidade do MVP podem ser controlados se a persistência e as integrações forem introduzidas de forma incremental.

#### Data Points

- A Zendesk destaca que seus produtos com IA precisam operar com privacidade em mente e suportar conformidade com leis como GDPR e CCPA ([Zendesk AI](https://www.zendesk.com/service/ai/)).
- A documentação da ServiceNow mostra recursos ligados a case restrictions, employee relations, evidências, handling notes e VIP cases, sinalizando a importância de governança no domínio ([ServiceNow HR Case Management](https://www.servicenow.com/docs/r/washingtondc/employee-service-management/hr-service-delivery/c_HRCaseManagement.html)).
- PrimeNG oferece configuração centralizada de theme, dark mode selector, cssLayer e zIndex, o que ajuda a controlar consistência visual em uma aplicação corporativa ([PrimeNG configuration](https://v20.primeng.org/configuration), [PrimeNG theming](https://v19.primeng.org/theming)).

#### Implications

- Mesmo um MVP precisa de pelo menos:
  - registro de conversas/sessões;
  - estado de escalonamento;
  - metadados de fonte/resposta;
  - trilha mínima de auditoria.
- A observabilidade deve incluir métricas de resolução, fallback e confiança.

### 5. Innovation & Differentiation Analysis

#### Key Insights

- O espaço não está vazio, mas a diferenciação pode ser forte em soluções que combinam conhecimento interno, explicabilidade e handoff humano bem desenhado.
- A principal oportunidade do Themis HR é ser uma camada inteligente de atendimento que se adapta ao contexto local da organização, em vez de tentar substituir todos os sistemas de RH.
- O uso de agentes especializados é particularmente interessante em RH porque diferentes tipos de caso pedem diferentes níveis de certeza, sensibilidade e automação.

#### Data Points

- ServiceNow e Zendesk tratam a automação com IA como parte de um continuum que inclui self-service, copilots, agentes e encaminhamento a humanos ([ServiceNow HRSD](https://www.servicenow.com/products/hr-service-delivery.html.html), [Zendesk AI](https://www.zendesk.com/service/ai/)).
- O estudo da SAP mostra que a qualidade do retrieval e o human-in-the-loop impactam diretamente a utilidade real do chatbot de RH ([arXiv 2407.05925](https://arxiv.org/abs/2407.05925)).
- A SHRM reforça que o avanço da IA em RH aumenta, e não elimina, a importância do julgamento humano ([SHRM AI in HR](https://www.shrm.org/topics-tools/research/2025-talent-trends/ai-in-hr)).

#### Implications

- O posicionamento correto é: **IA para resolver o repetitivo e orientar o sensível, não IA para eliminar o RH**.
- Diferenciais prioritários:
  - respostas baseadas em política interna;
  - explicabilidade;
  - escalonamento criterioso;
  - experiência enterprise simples;
  - adaptação ao idioma e ao contexto da empresa.

## Critical Decision Points

### Go / No-Go Factors

- **Go** se o MVP ficar restrito a perguntas e fluxos de alto volume e baixa ambiguidade.
- **Go** se houver patrocinador de RH para curadoria da base de conhecimento.
- **No-Go** se a expectativa for cobrir employee relations complexas e decisões interpretativas sem validação humana.
- **No-Go** se não houver governança mínima sobre conteúdo, logs e critérios de escalonamento.

### Technical Architecture Choices

- Frontend Angular com PrimeNG/Nora.
- Backend FastAPI.
- Orquestração com CrewAI.
- Persistência relacional mínima com versionamento por Alembic.
- Knowledge-first design com RAG e fallback humano.

### Market Positioning

- Posicionar como **help desk inteligente de RH** para uso interno.
- Foco inicial em empresas que já têm políticas, FAQs e processos documentados, mas atendimento fragmentado.
- Vender valor em produtividade, consistência e experiência do colaborador, não em “substituição do RH”.

### Resource Requirements

- Discovery e arquitetura: 1 PM/PO, 1 arquiteto, apoio de RH.
- MVP técnico: 1 backend, 1 frontend, 1 QA, apoio contínuo de stakeholder de RH.
- Base de conhecimento: curadoria inicial obrigatória.

## Risk Assessment Matrix

### High Risk

- Respostas incorretas sobre políticas sensíveis.
- Exposição indevida de dados do colaborador.
- Escalonamento insuficiente em casos de employee relations ou payroll exceptions.
- Base documental desatualizada.

### Medium Risk

- Baixa adesão se a IA parecer “genérica” ou pouco útil.
- Sobreposição com portais/HRIS já existentes.
- Crescimento desordenado do escopo para além do MVP.
- Dependência excessiva de prompt tuning sem estratégia de knowledge management.

### Low Risk

- Ajustes visuais do frontend.
- Troca futura do preset do PrimeNG.
- Evolução incremental da persistência do MVP para produção.

## Actionable Recommendations

### Immediate Next Steps (48h)

- Fechar o PRD do MVP com escopo explícito.
- Definir os primeiros domínios suportados: férias, folha, benefícios, políticas gerais.
- Catalogar as fontes de conhecimento iniciais.
- Definir quais casos obrigatoriamente escalam para humano.

### Short-Term Priorities (30 dias)

- Produzir SAD.
- Modelar os 6 agentes do produto.
- Definir persistência mínima, APIs e formato dos logs.
- Construir um frontend Angular com PrimeNG/Nora para o fluxo principal.

### Long-Term Strategy (6-12 meses)

- Expandir integrações com HRIS/SSO.
- Adicionar analytics de conteúdo, deflection e gap detection.
- Evoluir da FAQ/chat assistido para jornadas mais estruturadas.
- Incorporar camadas mais avançadas de segurança, compliance e governança.

## Sources

1. ServiceNow HR Service Delivery product page — https://www.servicenow.com/products/hr-service-delivery.html.html
2. ServiceNow HR Case Management docs — https://www.servicenow.com/docs/r/washingtondc/employee-service-management/hr-service-delivery/c_HRCaseManagement.html
3. ServiceNow HR Service Delivery data sheet — https://blogs.servicenow.com/content/dam/servicenow-assets/public/en-us/doc-type/resource-center/data-sheet/ds-servicenow-hr-service-delivery.pdf
4. Zendesk Employee Service — https://www.zendesk.com/employee-service/
5. Zendesk AI for service — https://www.zendesk.com/service/ai/
6. Zendesk media kit (employee service positioning) — https://web-assets.zendesk.com/zendesk/pages/newsroom/media-resources/Zendesk_Media_Kit.pdf
7. Workday Employee Self-Service Payroll — https://www.workday.com/en-us/products/payroll/employee-self-service.html
8. SHRM, The Role of AI in HR Continues to Expand — https://www.shrm.org/topics-tools/research/2025-talent-trends/ai-in-hr
9. Microsoft + LinkedIn 2024 Work Trend Index — https://news.microsoft.com/source/2024/05/08/microsoft-and-linkedin-release-the-2024-work-trend-index-on-the-state-of-ai-at-work/
10. SAP/ArXiv HR support chatbot with RAG and human in the loop — https://arxiv.org/abs/2407.05925
11. CrewAI Installation — https://docs.crewai.com/en/installation
12. CrewAI Crews — https://docs.crewai.com/en/concepts/crews
13. CrewAI Coding Tools / AGENTS.md — https://docs.crewai.com/en/guides/coding-tools/agents-md
14. PrimeNG Theming — https://v19.primeng.org/theming
15. PrimeNG Configuration — https://v20.primeng.org/configuration
16. PrimeNG Installation — https://v20.primeng.org/installation
17. FastAPI SQL Databases — https://fastapi.tiangolo.com/tutorial/sql-databases/
18. SQLAlchemy ORM — https://docs.sqlalchemy.org/en/20/orm/
19. Alembic docs — https://alembic.sqlalchemy.org/
20. Alembic autogenerate — https://alembic.sqlalchemy.org/en/latest/autogenerate.html

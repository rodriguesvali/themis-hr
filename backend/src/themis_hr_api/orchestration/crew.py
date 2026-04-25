import json
import os
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import fitz
import yaml
from crewai import Agent, Crew, Process, Task
from crewai.tools import tool

from themis_hr_api.core.config import PROJECT_ROOT, settings
from themis_hr_api.knowledge.admissao_contratos import KNOWLEDGE_BASE_MOCK as KB_ADMISSAO
from themis_hr_api.knowledge.ferias import KNOWLEDGE_BASE_MOCK as KB_FERIAS
from themis_hr_api.knowledge.jornada_feriados import KNOWLEDGE_BASE_MOCK as KB_JORNADA
from themis_hr_api.knowledge.remuneracao import KNOWLEDGE_BASE_MOCK as KB_REMUNERACAO
from themis_hr_api.knowledge.rescisao import KNOWLEDGE_BASE_MOCK as KB_RESCISAO


if settings.google_api_key:
    # CrewAI expects this environment variable name for Gemini.
    os.environ["GEMINI_API_KEY"] = settings.google_api_key


@dataclass(frozen=True)
class KnowledgeArea:
    key: str
    category: str
    knowledge_file: str
    agent_config_key: str
    knowledge_base: str


@dataclass(frozen=True)
class RoutingDecision:
    area_key: str
    category: str
    sensitivity: str
    reason: str


@dataclass(frozen=True)
class ThemisCrewResult:
    reply: str
    should_escalate: bool
    category: str
    sensitivity: str
    specialist: str | None
    confidence: str
    escalation_reason: str | None = None
    legal_reviewed: bool = False
    legal_risk_level: str | None = None
    legal_notes: str | None = None
    legal_basis: str | None = None


@lru_cache(maxsize=4)
def _load_pdf_pages(clt_pdf_path: str) -> tuple[tuple[int, str], ...]:
    path = Path(clt_pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"CLT PDF não encontrado: {path}")

    with fitz.open(path) as document:
        return tuple(
            (page.number + 1, page.get_text("text"))
            for page in document
            if page.get_text("text").strip()
        )


def _terms_for_clt_query(query: str) -> list[str]:
    normalized = query.lower()
    terms = [term for term in re.findall(r"[a-zA-ZÀ-ÿ0-9]{4,}", normalized)]

    if "jornada" in normalized and "descanso" in normalized:
        terms.extend(["interjornada", "entre jornadas", "11 horas", "onze horas", "consecutivas"])

    return list(dict.fromkeys(terms))


def _search_clt_pdf(query: str, clt_pdf_path: str) -> str:
    terms = _terms_for_clt_query(query)
    if not terms:
        return "Nenhum termo suficiente para consulta à CLT."

    matches: list[tuple[int, int, str]] = []
    for page_number, text in _load_pdf_pages(clt_pdf_path):
        normalized_text = text.lower()
        score = sum(normalized_text.count(term) for term in terms)
        if score:
            matches.append((score, page_number, text))

    if not matches:
        return "Nenhum trecho relevante encontrado na CLT para a consulta."

    snippets: list[str] = []
    for _, page_number, text in sorted(matches, reverse=True)[:4]:
        normalized_text = text.lower()
        positions = [normalized_text.find(term) for term in terms if normalized_text.find(term) >= 0]
        start = max(min(positions) - 500, 0) if positions else 0
        end = min(start + 1400, len(text))
        snippet = re.sub(r"\s+", " ", text[start:end]).strip()
        snippets.append(f"Página {page_number}: {snippet}")

    return "\n\n".join(snippets)


@tool("Consultar CLT")
def consultar_clt(query: str) -> str:
    """Consulta o PDF local da CLT por termos e retorna trechos relevantes."""
    clt_pdf_path = str(Path(settings.clt_pdf_path))
    if not Path(clt_pdf_path).is_absolute():
        clt_pdf_path = str(PROJECT_ROOT / clt_pdf_path)
    return _search_clt_pdf(query=query, clt_pdf_path=clt_pdf_path)


KNOWLEDGE_AREAS: dict[str, KnowledgeArea] = {
    "ferias": KnowledgeArea(
        key="ferias",
        category="Férias e Licenças",
        knowledge_file="ferias.md",
        agent_config_key="ferias_agent",
        knowledge_base=KB_FERIAS,
    ),
    "remuneracao": KnowledgeArea(
        key="remuneracao",
        category="Remuneração e Benefícios",
        knowledge_file="remuneracao.md",
        agent_config_key="remuneracao_agent",
        knowledge_base=KB_REMUNERACAO,
    ),
    "jornada": KnowledgeArea(
        key="jornada",
        category="Jornada e Frequência",
        knowledge_file="jornada_feriados.md",
        agent_config_key="jornada_agent",
        knowledge_base=KB_JORNADA,
    ),
    "admissao": KnowledgeArea(
        key="admissao",
        category="Admissão e Contratos",
        knowledge_file="admissao_contratos.md",
        agent_config_key="admissao_agent",
        knowledge_base=KB_ADMISSAO,
    ),
    "rescisao": KnowledgeArea(
        key="rescisao",
        category="Rescisão e Desligamento",
        knowledge_file="rescisao.md",
        agent_config_key="rescisao_agent",
        knowledge_base=KB_RESCISAO,
    ),
}


class ThemisHRCrew:
    """Conditional orchestration: principal agent + one on-demand specialist."""

    def __init__(self) -> None:
        self.llm = f"gemini/{settings.crewai_model}"
        self.agent_configs = self._load_agent_configs()

    def run(self, user_message: str) -> ThemisCrewResult:
        routing = self._route(user_message)

        if routing.area_key == "assuntos_gerais" or routing.sensitivity == "alta":
            return ThemisCrewResult(
                reply=(
                    "Vou encaminhar sua solicitação para um analista de RH. "
                    "Esse tipo de assunto precisa de análise humana para garantir o tratamento adequado."
                ),
                should_escalate=True,
                category=routing.category,
                sensitivity=routing.sensitivity,
                specialist=None,
                confidence="baixa",
                escalation_reason=routing.reason,
            )

        area = KNOWLEDGE_AREAS.get(routing.area_key)
        if not area:
            return ThemisCrewResult(
                reply=(
                    "Não encontrei uma base de conhecimento adequada para responder com segurança. "
                    "Vou encaminhar sua solicitação para um analista de RH."
                ),
                should_escalate=True,
                category=routing.category,
                sensitivity=routing.sensitivity,
                specialist=None,
                confidence="baixa",
                escalation_reason=f"Área roteada sem especialista configurado: {routing.area_key}",
            )

        return self._answer_with_specialist(user_message=user_message, routing=routing, area=area)

    def _load_agent_configs(self) -> dict[str, dict[str, Any]]:
        config_path = Path(__file__).parent / "config" / "agents.yaml"
        with config_path.open(encoding="utf-8") as config_file:
            return yaml.safe_load(config_file)

    def _build_agent(self, config_key: str, tools: list[Any] | None = None) -> Agent:
        return Agent(
            config=self.agent_configs[config_key],
            tools=tools or [],
            llm=self.llm,
            verbose=True,
        )

    def _build_clt_pdf_tool(self) -> Any:
        self._resolve_project_path(settings.clt_pdf_path)
        return consultar_clt

    def _resolve_project_path(self, configured_path: str) -> Path:
        path = Path(configured_path)
        if path.is_absolute():
            return path
        project_root = Path(__file__).resolve().parents[4]
        return project_root / path

    def _route(self, user_message: str) -> RoutingDecision:
        principal = self._build_agent("principal_agent")
        categories = "\n".join(
            f"- {area.key}: {area.category} ({area.knowledge_file})"
            for area in KNOWLEDGE_AREAS.values()
        )
        task = Task(
            description=f"""
            Classifique a solicitação de RH abaixo e escolha exatamente uma área.

            Mensagem do colaborador:
            \"{user_message}\"

            Áreas disponíveis:
            {categories}
            - assuntos_gerais: assédio, denúncia, discriminação, conflito, tema não coberto ou caso sensível.

            Responda exclusivamente em JSON válido, sem markdown:
            {{
              "area_key": "ferias|remuneracao|jornada|admissao|rescisao|assuntos_gerais",
              "category": "nome da categoria",
              "sensitivity": "baixa|media|alta",
              "reason": "motivo curto do roteamento"
            }}
            """,
            expected_output="JSON válido com area_key, category, sensitivity e reason.",
            agent=principal,
        )
        raw_output = self._kickoff_single_task(principal, task)
        payload = self._parse_json(raw_output)

        area_key = self._normalize_area(str(payload.get("area_key", "")))
        sensitivity = self._normalize_sensitivity(str(payload.get("sensitivity", "")))
        category = str(payload.get("category") or self._category_for_area(area_key))
        reason = str(payload.get("reason") or "Roteamento classificado pelo agente principal.")

        return RoutingDecision(
            area_key=area_key,
            category=category,
            sensitivity=sensitivity,
            reason=reason,
        )

    def _answer_with_specialist(
        self,
        user_message: str,
        routing: RoutingDecision,
        area: KnowledgeArea,
    ) -> ThemisCrewResult:
        specialist = self._build_agent(area.agent_config_key)
        task = Task(
            description=f"""
            Responda à solicitação usando estritamente a base de conhecimento da sua área.

            Categoria roteada: {routing.category}
            Sensibilidade: {routing.sensitivity}
            Motivo do roteamento: {routing.reason}

            Mensagem do colaborador:
            \"{user_message}\"

            Base de conhecimento ({area.knowledge_file}):
            {area.knowledge_base}

            Instruções:
            - Não invente regras fora da base fornecida.
            - Responda em português claro, acolhedor e corporativo.
            - Se a base não cobrir a pergunta com segurança, marque should_escalate como true.
            - Se houver risco jurídico, denúncia, assédio, discriminação ou baixa confiança, marque should_escalate como true.

            Responda exclusivamente em JSON válido, sem markdown:
            {{
              "answer": "resposta para o colaborador ou motivo de handoff",
              "confidence": "alta|media|baixa",
              "should_escalate": true|false,
              "escalation_reason": "motivo curto ou null"
            }}
            """,
            expected_output="JSON válido com answer, confidence, should_escalate e escalation_reason.",
            agent=specialist,
        )
        raw_output = self._kickoff_single_task(specialist, task)
        payload = self._parse_json(raw_output)

        answer = str(payload.get("answer") or "").strip()
        confidence = self._normalize_confidence(str(payload.get("confidence", "")))
        should_escalate = self._to_bool(payload.get("should_escalate"))
        escalation_reason = payload.get("escalation_reason")
        if escalation_reason is not None:
            escalation_reason = str(escalation_reason).strip() or None

        if not answer:
            answer = (
                "Não encontrei informação suficiente na base de conhecimento para responder com segurança. "
                "Vou encaminhar sua solicitação para um analista de RH."
            )
            should_escalate = True
            confidence = "baixa"
            escalation_reason = escalation_reason or "Especialista não retornou resposta segura."

        if confidence == "baixa":
            should_escalate = True
            escalation_reason = escalation_reason or "Confiança baixa na resposta do especialista."

        specialist_result = ThemisCrewResult(
            reply=answer,
            should_escalate=should_escalate,
            category=area.category,
            sensitivity=routing.sensitivity,
            specialist=area.key,
            confidence=confidence,
            escalation_reason=escalation_reason,
        )

        return self._review_answer_legally(
            user_message=user_message,
            routing=routing,
            area=area,
            specialist_result=specialist_result,
        )

    def _review_answer_legally(
        self,
        user_message: str,
        routing: RoutingDecision,
        area: KnowledgeArea,
        specialist_result: ThemisCrewResult,
    ) -> ThemisCrewResult:
        try:
            clt_pdf_tool = self._build_clt_pdf_tool()
            clt_query = (
                f"{area.category}. Pergunta: {user_message}. "
                f"Resposta proposta: {specialist_result.reply}"
            )
            clt_context = clt_pdf_tool.run(query=clt_query)
            legal_reviewer = self._build_agent(
                "legal_reviewer_agent",
                tools=[clt_pdf_tool],
            )
        except Exception as exc:
            return self._legal_review_fallback(
                specialist_result=specialist_result,
                reason=f"Falha ao preparar consulta à CLT: {exc}",
            )

        task = Task(
            description=f"""
            Revise juridicamente a resposta proposta antes do envio ao colaborador.

            Pergunta original do colaborador:
            \"{user_message}\"

            Categoria roteada: {area.category}
            Especialista acionado: {area.key}
            Sensibilidade classificada: {routing.sensitivity}
            Motivo do roteamento: {routing.reason}
            Confiança do especialista: {specialist_result.confidence}
            Especialista recomendou escalonamento: {specialist_result.should_escalate}
            Motivo de escalonamento do especialista: {specialist_result.escalation_reason or "null"}

            Resposta proposta pelo especialista ou motivo de handoff:
            \"{specialist_result.reply}\"

            Trechos recuperados da CLT para revisão:
            {clt_context}

            Instruções:
            - Use os trechos recuperados da CLT como base mínima da revisão.
            - Você também pode usar a ferramenta Consultar CLT para buscar apoio complementar.
            - Verifique se a resposta contradiz a legislação trabalhista brasileira ou extrapola a base de RH.
            - Não transforme a resposta em parecer jurídico.
            - Se o especialista pediu escalonamento apenas por falta de cobertura na base interna, use a CLT para tentar
              responder com segurança quando a regra legal for objetiva e o risco for baixo.
            - Se houver risco médio ou alto, ambiguidade legal, ausência de base suficiente ou necessidade de interpretação humana,
              marque should_escalate como true.
            - Se aprovar, preserve o sentido da resposta e ajuste apenas pontos necessários de cautela.
            - Inclua em legal_basis uma referência curta ao fundamento consultado ou explique a ausência de base suficiente.

            Responda exclusivamente em JSON válido, sem markdown:
            {{
              "approved": true|false,
              "final_answer": "resposta final revisada ou null",
              "risk_level": "baixo|medio|alto",
              "should_escalate": true|false,
              "legal_notes": "observação curta sobre a revisão",
              "legal_basis": "fundamento legal curto, trecho consultado ou null"
            }}
            """,
            expected_output="JSON válido com approved, final_answer, risk_level, should_escalate, legal_notes e legal_basis.",
            agent=legal_reviewer,
        )

        try:
            raw_output = self._kickoff_single_task(legal_reviewer, task)
        except Exception as exc:
            return self._legal_review_fallback(
                specialist_result=specialist_result,
                reason=f"Falha durante revisão jurídica automática: {exc}",
            )

        payload = self._parse_json(raw_output)
        if not payload:
            return self._legal_review_fallback(
                specialist_result=specialist_result,
                reason="Revisão jurídica automática retornou JSON inválido ou vazio.",
            )

        approved = self._to_bool(payload.get("approved"))
        risk_level = self._normalize_risk_level(str(payload.get("risk_level", "")))
        legal_should_escalate = self._to_bool(payload.get("should_escalate"))
        legal_notes = str(payload.get("legal_notes") or "").strip() or None
        legal_basis = str(payload.get("legal_basis") or "").strip() or None
        final_answer = str(payload.get("final_answer") or "").strip()

        if not approved or legal_should_escalate or risk_level in {"medio", "alto"}:
            return ThemisCrewResult(
                reply=(
                    "Vou encaminhar sua solicitação para um analista de RH. "
                    "A resposta precisa de revisão humana para garantir aderência à legislação trabalhista."
                ),
                should_escalate=True,
                category=specialist_result.category,
                sensitivity=routing.sensitivity,
                specialist=specialist_result.specialist,
                confidence="baixa",
                escalation_reason=legal_notes or "Revisão jurídica automática recomendou escalonamento.",
                legal_reviewed=True,
                legal_risk_level=risk_level,
                legal_notes=legal_notes,
                legal_basis=legal_basis,
            )

        return ThemisCrewResult(
            reply=final_answer or specialist_result.reply,
            should_escalate=False,
            category=specialist_result.category,
            sensitivity=routing.sensitivity,
            specialist=specialist_result.specialist,
            confidence="media" if specialist_result.confidence == "baixa" else specialist_result.confidence,
            escalation_reason=None,
            legal_reviewed=True,
            legal_risk_level=risk_level,
            legal_notes=legal_notes,
            legal_basis=legal_basis,
        )

    def _legal_review_fallback(
        self,
        specialist_result: ThemisCrewResult,
        reason: str,
    ) -> ThemisCrewResult:
        return ThemisCrewResult(
            reply=(
                "Vou encaminhar sua solicitação para um analista de RH. "
                "Não consegui concluir a revisão jurídica automática com segurança."
            ),
            should_escalate=True,
            category=specialist_result.category,
            sensitivity=specialist_result.sensitivity,
            specialist=specialist_result.specialist,
            confidence="baixa",
            escalation_reason=reason,
            legal_reviewed=False,
            legal_risk_level="alto",
            legal_notes=reason,
            legal_basis=None,
        )

    def _kickoff_single_task(self, agent: Agent, task: Task) -> str:
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )
        return str(crew.kickoff())

    def _parse_json(self, raw_output: str) -> dict[str, Any]:
        text = raw_output.strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, flags=re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    pass
        return {}

    def _normalize_area(self, raw_area: str) -> str:
        value = self._slug(raw_area)
        aliases = {
            "ferias": "ferias",
            "ferias_e_licencas": "ferias",
            "remuneracao": "remuneracao",
            "remuneracao_e_beneficios": "remuneracao",
            "jornada": "jornada",
            "jornada_e_frequencia": "jornada",
            "jornada_e_ponto": "jornada",
            "admissao": "admissao",
            "admissao_e_contratos": "admissao",
            "admissao_e_estagio": "admissao",
            "rescisao": "rescisao",
            "rescisao_e_desligamento": "rescisao",
            "assuntos_gerais": "assuntos_gerais",
            "sensivel": "assuntos_gerais",
        }
        return aliases.get(value, "assuntos_gerais")

    def _normalize_sensitivity(self, raw_sensitivity: str) -> str:
        value = self._slug(raw_sensitivity)
        if value in {"alta", "alto", "high"}:
            return "alta"
        if value in {"media", "medio", "moderada", "medium"}:
            return "media"
        return "baixa"

    def _normalize_confidence(self, raw_confidence: str) -> str:
        value = self._slug(raw_confidence)
        if value in {"alta", "alto", "high"}:
            return "alta"
        if value in {"media", "medio", "moderada", "medium"}:
            return "media"
        return "baixa"

    def _normalize_risk_level(self, raw_risk_level: str) -> str:
        value = self._slug(raw_risk_level)
        if value in {"alto", "alta", "high"}:
            return "alto"
        if value in {"medio", "media", "moderado", "moderada", "medium"}:
            return "medio"
        return "baixo"

    def _category_for_area(self, area_key: str) -> str:
        if area_key == "assuntos_gerais":
            return "Assuntos Gerais"
        area = KNOWLEDGE_AREAS.get(area_key)
        return area.category if area else "Assuntos Gerais"

    def _slug(self, text: str) -> str:
        normalized = text.strip().lower()
        replacements = {
            "á": "a",
            "à": "a",
            "ã": "a",
            "â": "a",
            "é": "e",
            "ê": "e",
            "í": "i",
            "ó": "o",
            "ô": "o",
            "õ": "o",
            "ú": "u",
            "ç": "c",
        }
        for source, target in replacements.items():
            normalized = normalized.replace(source, target)
        return re.sub(r"[^a-z0-9]+", "_", normalized).strip("_")

    def _to_bool(self, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        return str(value).strip().lower() in {"true", "sim", "yes", "1"}

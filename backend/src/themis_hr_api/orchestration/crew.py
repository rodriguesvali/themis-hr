import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from crewai import Agent, Crew, Process, Task

from themis_hr_api.core.config import settings
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

    def _build_agent(self, config_key: str) -> Agent:
        return Agent(
            config=self.agent_configs[config_key],
            llm=self.llm,
            verbose=True,
        )

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

        return ThemisCrewResult(
            reply=answer,
            should_escalate=should_escalate,
            category=area.category,
            sensitivity=routing.sensitivity,
            specialist=area.key,
            confidence=confidence,
            escalation_reason=escalation_reason,
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

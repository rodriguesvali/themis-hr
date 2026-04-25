import unittest

from crewai.tools import tool

from themis_hr_api.orchestration.crew import (
    KNOWLEDGE_AREAS,
    RoutingDecision,
    ThemisCrewResult,
    ThemisHRCrew,
)


@tool("Consultar CLT")
def consultar_clt(query: str) -> str:
    """Consulta simulada à CLT para testes do fluxo jurídico."""
    return f"Trecho simulado da CLT para: {query[:40]}"


class LegalReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.crew = ThemisHRCrew()
        self.crew._build_clt_pdf_tool = lambda: consultar_clt
        self.routing = RoutingDecision(
            area_key="ferias",
            category="Férias e Licenças",
            sensitivity="baixa",
            reason="teste",
        )
        self.area = KNOWLEDGE_AREAS["ferias"]
        self.specialist_result = ThemisCrewResult(
            reply="Resposta proposta pelo especialista.",
            should_escalate=False,
            category="Férias e Licenças",
            sensitivity="baixa",
            specialist="ferias",
            confidence="alta",
        )

    def test_approved_legal_review_returns_final_answer(self) -> None:
        self.crew._kickoff_single_task = lambda agent, task: (
            '{"approved": true, "final_answer": "Resposta revisada", '
            '"risk_level": "baixo", "should_escalate": false, '
            '"legal_notes": "Compatível", "legal_basis": "Base simulada"}'
        )

        result = self.crew._review_answer_legally(
            "Pergunta", self.routing, self.area, self.specialist_result
        )

        self.assertFalse(result.should_escalate)
        self.assertTrue(result.legal_reviewed)
        self.assertEqual(result.reply, "Resposta revisada")
        self.assertEqual(result.legal_risk_level, "baixo")
        self.assertEqual(result.legal_basis, "Base simulada")

    def test_medium_legal_risk_escalates(self) -> None:
        self.crew._kickoff_single_task = lambda agent, task: (
            '{"approved": true, "final_answer": "Resposta com ressalva", '
            '"risk_level": "medio", "should_escalate": false, '
            '"legal_notes": "Risco moderado", "legal_basis": "Base simulada"}'
        )

        result = self.crew._review_answer_legally(
            "Pergunta", self.routing, self.area, self.specialist_result
        )

        self.assertTrue(result.should_escalate)
        self.assertEqual(result.confidence, "baixa")
        self.assertEqual(result.legal_risk_level, "medio")
        self.assertEqual(result.escalation_reason, "Risco moderado")

    def test_legal_reviewer_can_rescue_specialist_knowledge_gap(self) -> None:
        outputs = iter(
            [
                (
                    '{"answer": "Encaminhar por falta de base interna.", '
                    '"confidence": "baixa", "should_escalate": true, '
                    '"escalation_reason": "Base interna não cobre interjornada."}'
                ),
                (
                    '{"approved": true, '
                    '"final_answer": "Entre duas jornadas, a CLT prevê descanso mínimo de 11 horas consecutivas.", '
                    '"risk_level": "baixo", "should_escalate": false, '
                    '"legal_notes": "Regra legal objetiva.", '
                    '"legal_basis": "CLT, art. 66"}'
                ),
            ]
        )
        self.crew._kickoff_single_task = lambda agent, task: next(outputs)

        result = self.crew._answer_with_specialist(
            "Qual o intervalo de descanso entre jornadas?",
            self.routing,
            self.area,
        )

        self.assertFalse(result.should_escalate)
        self.assertTrue(result.legal_reviewed)
        self.assertEqual(result.confidence, "media")
        self.assertEqual(result.legal_basis, "CLT, art. 66")
        self.assertIn("11 horas", result.reply)

    def test_invalid_legal_review_json_escalates(self) -> None:
        self.crew._kickoff_single_task = lambda agent, task: "resposta sem json"

        result = self.crew._review_answer_legally(
            "Pergunta", self.routing, self.area, self.specialist_result
        )

        self.assertTrue(result.should_escalate)
        self.assertFalse(result.legal_reviewed)
        self.assertEqual(result.legal_risk_level, "alto")
        self.assertIn("JSON inválido", result.escalation_reason or "")

    def test_clt_tool_failure_escalates(self) -> None:
        self.crew._build_clt_pdf_tool = lambda: (_ for _ in ()).throw(
            FileNotFoundError("sem CLT")
        )

        result = self.crew._review_answer_legally(
            "Pergunta", self.routing, self.area, self.specialist_result
        )

        self.assertTrue(result.should_escalate)
        self.assertFalse(result.legal_reviewed)
        self.assertEqual(result.legal_risk_level, "alto")
        self.assertIn("sem CLT", result.escalation_reason or "")


if __name__ == "__main__":
    unittest.main()

import json
from abc import ABC, abstractmethod
from pathlib import Path
from utils.claude_client import call_claude, StageExecutionError
from config import STAGE_TOKEN_BUDGETS


class BaseStage(ABC):
    stage_key: str = ""

    @abstractmethod
    def build_prompt(self, problem: str, context: dict) -> tuple[str, str]:
        """Return (system_prompt, user_prompt)."""
        ...

    def run(self, problem: str, context: dict) -> dict:
        system, user = self.build_prompt(problem, context)
        max_tokens = STAGE_TOKEN_BUDGETS.get(self.stage_key, 2048)
        result = call_claude(system, user, max_tokens)
        self.validate(result)
        return result

    def validate(self, result: dict) -> None:
        pass

    @staticmethod
    def compress_context(context: dict) -> dict:
        """Return a slimmed context for late-stage prompts to save tokens."""
        slim: dict = {}
        if "laws" in context:
            slim["law_names"] = [l.get("law_name") for l in context["laws"].get("laws", [])]
        if "personas" in context:
            slim["persona_names"] = [p.get("name") for p in context["personas"].get("personas", [])]
            slim["personas_summary"] = [
                {"name": p.get("name"), "goal": p.get("primary_goal"), "frustrations": p.get("frustrations", [])[:2]}
                for p in context["personas"].get("personas", [])
            ]
        if "design_thinking" in context:
            slim["dt_key_insights"] = [
                {"phase": ph.get("phase_name"), "insight_snippet": ph.get("insights", "")[:120]}
                for ph in context["design_thinking"].get("phases", [])
            ]
        if "synthesis" in context:
            slim["hmw_statements"] = context["synthesis"].get("opportunities", [])
            slim["key_themes"] = context["synthesis"].get("key_themes", [])
            slim["critical_insights"] = context["synthesis"].get("critical_insights", [])[:3]
        if "journey" in context:
            slim["journey_stage_names"] = [s.get("stage_name") for s in context["journey"].get("journey_stages", [])]
            slim["journey_pain_points"] = [
                pp for s in context["journey"].get("journey_stages", []) for pp in s.get("pain_points", [])
            ][:8]
        if "rationale" in context:
            slim["decisions_summary"] = [
                {"title": d.get("decision_title"), "chosen": d.get("chosen_approach")}
                for d in context["rationale"].get("decisions", [])
            ]
        if "design_system" in context:
            slim["component_names"] = [
                c.get("component_name")
                for cat in context["design_system"].get("component_categories", [])
                for c in cat.get("components", [])
            ]
        return slim

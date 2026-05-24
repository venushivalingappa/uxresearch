import json
from pipeline.base_stage import BaseStage

SYSTEM = """You are a principal UX designer documenting design rationale for a product.
Every decision must cite specific UX laws and reference named personas.
You consider alternatives seriously before recommending an approach.
Respond ONLY with valid JSON. No markdown fences, no explanation."""

USER_TEMPLATE = """Problem Statement: {problem}

Available UX Laws (cite these in your rationale):
{law_names}

Personas (reference by name):
{persona_names}

Key pain points from the journey map:
{pain_points}

Key design thinking outputs:
{dt_outputs}

Document 6-8 key design decisions for this product. Each decision should address a meaningful design choice
(navigation pattern, onboarding approach, error handling strategy, information architecture, etc.)

Return this exact JSON structure:
{{
  "decisions": [
    {{
      "decision_title": "short title for this design decision",
      "context": "what problem or tension this decision addresses",
      "options_considered": [
        "option A description",
        "option B description",
        "option C description (optional)"
      ],
      "chosen_approach": "the approach selected",
      "rationale": "why this approach was chosen — must cite at least one UX law by exact name and reference at least one persona by name",
      "trade_offs": "what is given up with this choice",
      "success_metric": "how you would measure if this decision was correct"
    }}
  ]
}}

Make decisions varied — cover navigation, content hierarchy, onboarding, error states, feedback mechanisms, accessibility."""


class DesignRationaleStage(BaseStage):
    stage_key = "design_rationale"

    def build_prompt(self, problem: str, context: dict) -> tuple[str, str]:
        slim = self.compress_context(context)

        law_names = "\n".join(f"- {n}" for n in slim.get("law_names", []))
        persona_names = ", ".join(slim.get("persona_names", []))
        pain_points = "\n".join(f"- {pp}" for pp in slim.get("journey_pain_points", [])[:6])
        dt_outputs = "\n".join(
            f"- {item['phase']}: {item['insight_snippet']}"
            for item in slim.get("dt_key_insights", [])
        )

        user = USER_TEMPLATE.format(
            problem=problem,
            law_names=law_names or "Not available",
            persona_names=persona_names or "Not available",
            pain_points=pain_points or "Not available",
            dt_outputs=dt_outputs or "Not available",
        )
        return SYSTEM, user

    def validate(self, result: dict) -> None:
        if "decisions" not in result or len(result["decisions"]) < 4:
            raise ValueError("Expected at least 4 design decisions")

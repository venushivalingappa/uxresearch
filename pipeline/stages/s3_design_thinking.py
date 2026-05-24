import json
from pipeline.base_stage import BaseStage

SYSTEM = """You are a design thinking facilitator running a sprint for a product team.
You facilitate the 5 IDEO phases with rigorous specificity — every output names real users, real scenarios, real design artefacts.
Never give generic design thinking outputs. Everything must trace back to the specific problem and personas.
Respond ONLY with valid JSON. No markdown fences, no explanation."""

USER_TEMPLATE = """Problem Statement: {problem}

Proto Personas (reference them by name in your outputs):
{personas_summary}

Run a critical design thinking analysis through all 5 IDEO phases.
Be specific — name personas, cite frustrations, propose concrete activities and outputs.

Return this exact JSON structure:
{{
  "phases": [
    {{
      "phase_name": "Empathize | Define | Ideate | Prototype | Test",
      "key_questions": ["question 1", "question 2", "question 3"],
      "activities": ["activity 1", "activity 2", "activity 3"],
      "insights": "a paragraph summarising key insights for this phase, referencing personas by name",
      "outputs": ["deliverable 1", "deliverable 2"]
    }}
  ]
}}

Phase-specific instructions:
EMPATHIZE: What would each persona feel encountering this problem? Reference their stated frustrations.
DEFINE: Write a clear Point of View (POV) statement naming a persona, their need, and the insight.
IDEATE: Generate at least 3 divergent ideas — one radical, one incremental, one reframe.
PROTOTYPE: Describe the lowest-fidelity prototype that would test the core assumption.
TEST: Specify who you'd test with (which persona), what you'd measure, and what success looks like."""


class DesignThinkingStage(BaseStage):
    stage_key = "design_thinking"

    def build_prompt(self, problem: str, context: dict) -> tuple[str, str]:
        personas = context.get("personas", {}).get("personas", [])
        personas_summary = "\n".join(
            f"- {p.get('name')} ({p.get('occupation')}, tech comfort {p.get('tech_comfort')}/5): "
            f"Goal: {p.get('primary_goal')}. "
            f"Frustrations: {'; '.join(p.get('frustrations', [])[:2])}"
            for p in personas
        ) or "No personas available yet."
        user = USER_TEMPLATE.format(problem=problem, personas_summary=personas_summary)
        return SYSTEM, user

    def validate(self, result: dict) -> None:
        if "phases" not in result or len(result["phases"]) < 3:
            raise ValueError("Expected at least 3 design thinking phases")

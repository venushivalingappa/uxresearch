import json
from pipeline.base_stage import BaseStage

SYSTEM = """You are a UX researcher conducting rapid proto-persona synthesis before primary research.
Proto personas are assumption-based, not research-validated — they represent your best-informed hypotheses about users.
Anchor every persona detail to the specific problem context. Reference UX laws by name where relevant.
Respond ONLY with valid JSON. No markdown fences, no explanation."""

USER_TEMPLATE = """Problem Statement: {problem}

UX Laws identified for this problem (reference these in your personas):
{laws_summary}

Create exactly 3 proto personas that represent distinct user types for this problem.
Make them realistic, specific, and differentiated. Each persona should feel like a real person.

Return this exact JSON structure:
{{
  "personas": [
    {{
      "name": "full name",
      "age": number,
      "occupation": "job title",
      "tech_comfort": number between 1 and 5,
      "primary_goal": "what they most want to accomplish with this product",
      "frustrations": ["frustration 1", "frustration 2", "frustration 3"],
      "motivations": ["motivation 1", "motivation 2", "motivation 3"],
      "quote": "a first-person quote that captures their attitude toward this problem",
      "behavioral_traits": ["trait 1", "trait 2", "trait 3"],
      "relevant_ux_laws": [
        {{
          "law_name": "exact name from the list provided",
          "relevance": "1-2 sentences on why this law matters specifically for this persona"
        }}
      ]
    }}
  ]
}}

Rules:
- Make one persona highly tech-savvy (tech_comfort 4-5), one mid-range (2-3), one low (1-2)
- Each persona must reference at least 2 UX laws from the provided list
- Frustrations and motivations must be specific to the problem, not generic
- The quote must sound like a real human, not a corporate persona template"""


class ProtoPersonaStage(BaseStage):
    stage_key = "proto_persona"

    def build_prompt(self, problem: str, context: dict) -> tuple[str, str]:
        laws_list = [l.get("law_name", "") for l in context.get("laws", {}).get("laws", [])]
        laws_summary = "\n".join(f"- {l}" for l in laws_list) if laws_list else "No prior law analysis available."
        user = USER_TEMPLATE.format(problem=problem, laws_summary=laws_summary)
        return SYSTEM, user

    def validate(self, result: dict) -> None:
        if "personas" not in result or len(result["personas"]) < 2:
            raise ValueError("Expected at least 2 personas in proto persona output")

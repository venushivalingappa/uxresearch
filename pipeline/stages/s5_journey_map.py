import json
from pipeline.base_stage import BaseStage

SYSTEM = """You are a UX designer mapping the complete user journey for a product.
You document every touchpoint, emotion, and opportunity with precision.
Map the journey from the primary persona's perspective. Opportunities must reference existing HMW statements.
Respond ONLY with valid JSON. No markdown fences, no explanation."""

USER_TEMPLATE = """Problem Statement: {problem}

Primary Persona (map the journey for this person):
Name: {primary_name}
Occupation: {primary_occupation}
Primary Goal: {primary_goal}
Frustrations: {primary_frustrations}

HMW Opportunities to reference in the journey:
{hmw_list}

Map a complete end-to-end user journey for {primary_name} as they try to accomplish their goal.
Identify 5-7 distinct journey stages (e.g. Awareness, Research, Onboarding, First Use, Regular Use, Issue Resolution, Advocacy).

Return this exact JSON structure:
{{
  "persona_used": "{primary_name}",
  "journey_stages": [
    {{
      "stage_name": "stage name",
      "touchpoints": ["touchpoint 1", "touchpoint 2"],
      "user_actions": ["action 1", "action 2", "action 3"],
      "thoughts": "first-person inner monologue for this stage (1-2 sentences as the persona)",
      "emotions": ["emotion label 1", "emotion label 2"],
      "emotion_score": number from -2 to 2 (-2=very negative, 0=neutral, 2=very positive),
      "pain_points": ["pain point 1", "pain point 2"],
      "opportunities": ["exact HMW statement from the provided list that applies here"]
    }}
  ],
  "overall_arc": "one sentence describing the emotional arc of the full journey",
  "moment_of_truth": "the single most critical touchpoint that determines success or failure",
  "biggest_pain_point": "the most impactful pain point across the entire journey"
}}"""


class JourneyMapStage(BaseStage):
    stage_key = "journey_map"

    def build_prompt(self, problem: str, context: dict) -> tuple[str, str]:
        personas = context.get("personas", {}).get("personas", [])
        # Pick primary persona (highest tech comfort = most likely power user for richer journey)
        primary = max(personas, key=lambda p: p.get("tech_comfort", 0)) if personas else {}

        hmw = context.get("synthesis", {}).get("opportunities", [])
        hmw_list = "\n".join(f"- {h}" for h in hmw) if hmw else "- No HMW statements available"

        user = USER_TEMPLATE.format(
            problem=problem,
            primary_name=primary.get("name", "Primary User"),
            primary_occupation=primary.get("occupation", ""),
            primary_goal=primary.get("primary_goal", ""),
            primary_frustrations="; ".join(primary.get("frustrations", [])[:3]),
            hmw_list=hmw_list,
        )
        return SYSTEM, user

    def validate(self, result: dict) -> None:
        if "journey_stages" not in result or len(result["journey_stages"]) < 3:
            raise ValueError("Expected at least 3 journey stages")

import json
from pipeline.base_stage import BaseStage

SYSTEM = """You are a UX designer creating concise low-fidelity wireframe specifications.
Be extremely brief — short field values only. No prose descriptions.
Respond ONLY with valid JSON. No markdown fences, no explanation."""

USER_TEMPLATE = """Problem Statement: {problem}

Journey stages: {journey_stages}
Components available: {component_names}

Create exactly 5 screens for the primary onboarding flow.
Keep ALL field values short (under 10 words each).

Return this exact JSON structure:
{{
  "screens": [
    {{
      "screen_name": "name (3 words max)",
      "purpose": "one short sentence",
      "journey_stage": "stage name",
      "layout_type": "single-column | form | modal | tab-bar",
      "regions": [
        {{
          "region_name": "nav-header | content | tab-bar",
          "height_px": number,
          "background": "white | light-gray | dark",
          "contents": [
            {{
              "element": "component name or primitive (rectangle, text, image-placeholder, divider, spacer)",
              "label": "visible text or placeholder label",
              "width": "full | half | third | auto | Npx",
              "height": "Npx or auto",
              "style": "filled | outlined | text-only",
              "position": "top | center | bottom"
            }}
          ]
        }}
      ],
      "components_used": ["component name"],
      "interactions": [
        {{"trigger": "element", "action": "navigate", "destination": "screen name"}}
      ],
      "annotations": ["one short note"],
      "wireframe_description": "2 sentences max describing layout"
    }}
  ],
  "flow_connections": [
    {{"from_screen": "screen A", "to_screen": "screen B", "trigger": "tap CTA"}}
  ]
}}"""


class WireframesStage(BaseStage):
    stage_key = "wireframes"

    def build_prompt(self, problem: str, context: dict) -> tuple[str, str]:
        slim = self.compress_context(context)

        journey_stages = "\n".join(
            f"- {name}" for name in slim.get("journey_stage_names", [])
        ) or "Not available"

        component_names = "\n".join(
            f"- {name}" for name in slim.get("component_names", [])[:20]
        ) or "Not available"

        user = USER_TEMPLATE.format(
            problem=problem,
            journey_stages=journey_stages,
            component_names=component_names,
        )
        return SYSTEM, user

    def validate(self, result: dict) -> None:
        if "screens" not in result or len(result["screens"]) < 2:
            raise ValueError("Expected at least 2 wireframe screens")

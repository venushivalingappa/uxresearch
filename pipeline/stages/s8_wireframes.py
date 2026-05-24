import json
from pipeline.base_stage import BaseStage

SYSTEM = """You are a UX designer creating low-fidelity wireframe specifications.
Your wireframes are black-and-white, component-based, and described in enough detail that a developer could build them.
Every screen derives from the user journey map and uses components from the design system.
Respond ONLY with valid JSON. No markdown fences, no explanation."""

USER_TEMPLATE = """Problem Statement: {problem}

Journey stages (derive your screen list from these):
{journey_stages}

Available components (use these by exact name):
{component_names}

Create low-fidelity wireframe specifications for the key screens of this product.
Aim for 5-8 screens covering the primary user flow.

Return this exact JSON structure:
{{
  "screens": [
    {{
      "screen_name": "descriptive screen name",
      "screen_purpose": "one sentence on what user task this screen enables",
      "journey_stage": "which journey stage this screen belongs to",
      "layout_type": "single-column | split | modal | tab-bar | list | grid | form",
      "dimensions": {{"width": 375, "height": 812, "platform": "mobile-ios"}},
      "regions": [
        {{
          "region_name": "status-bar | nav-header | content | tab-bar | modal-overlay | bottom-sheet",
          "height_px": number,
          "background": "white | light-gray | dark",
          "contents": [
            {{
              "element": "component name or primitive (rectangle, text, image-placeholder, divider, spacer)",
              "label": "visible text or placeholder label",
              "width": "full | half | third | auto | Npx",
              "height": "Npx or auto",
              "style": "filled | outlined | ghost | text-only",
              "position": "description of position within region"
            }}
          ]
        }}
      ],
      "components_used": ["component names from design system"],
      "interactions": [
        {{
          "trigger": "element that triggers the interaction",
          "action": "what happens",
          "destination": "resulting screen or state"
        }}
      ],
      "annotations": [
        "accessibility note or design clarification"
      ],
      "wireframe_description": "detailed prose description of the complete screen layout — describe every visible element, their relative sizes, vertical stacking order, and placeholder content. Write as if narrating to someone who cannot see the screen."
    }}
  ],
  "flow_connections": [
    {{
      "from_screen": "screen name",
      "to_screen": "screen name",
      "trigger": "what causes navigation"
    }}
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

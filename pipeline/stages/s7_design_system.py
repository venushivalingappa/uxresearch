import json
from pipeline.base_stage import BaseStage

SYSTEM = """You are a design systems architect mapping the component library for a new product.
Derive components directly from the user journey touchpoints and wireframe needs.
Every component must have a clear reason to exist based on the research data.
Respond ONLY with valid JSON. No markdown fences, no explanation."""

USER_TEMPLATE = """Problem Statement: {problem}

Journey touchpoints requiring UI components:
{journey_stages}

Design decisions that imply component needs:
{decisions}

Map the complete design system component inventory for this product.

Be concise — component names and short arrays only. No long descriptions.

Return this exact JSON structure:
{{
  "component_categories": [
    {{
      "name": "Navigation",
      "components": [
        {{
          "component_name": "name",
          "variants": ["v1", "v2"],
          "usage_context": ["journey stage"],
          "ux_principles_applied": ["law name"],
          "priority": "must-have | should-have | nice-to-have",
          "states": ["default", "active", "disabled"]
        }}
      ]
    }}
  ],
  "design_tokens": {{
    "color_roles": ["primary-action", "destructive", "success", "warning", "neutral", "surface", "on-surface"],
    "type_scale": [
      {{"name": "display", "size": "32px", "weight": "700", "usage": "hero headings"}},
      {{"name": "heading-1", "size": "24px", "weight": "600", "usage": "page titles"}},
      {{"name": "body", "size": "16px", "weight": "400", "usage": "body text"}},
      {{"name": "caption", "size": "12px", "weight": "400", "usage": "labels"}}
    ],
    "spacing": {{
      "base_unit": "8px",
      "scale": ["4px", "8px", "16px", "24px", "32px", "48px"]
    }},
    "border_radius": {{"small": "4px", "medium": "8px", "large": "16px", "pill": "999px"}}
  }},
  "hierarchy_notes": "one sentence"
}}

Categories: Navigation, Forms, Feedback, Content, Layout. Max 4 components per category."""


class DesignSystemStage(BaseStage):
    stage_key = "design_system"

    def build_prompt(self, problem: str, context: dict) -> tuple[str, str]:
        slim = self.compress_context(context)

        journey_stages = "\n".join(
            f"- {name}" for name in slim.get("journey_stage_names", [])
        ) or "Not available"

        decisions = "\n".join(
            f"- {d['title']}: chose {d['chosen']}"
            for d in slim.get("decisions_summary", [])
        ) or "Not available"

        user = USER_TEMPLATE.format(
            problem=problem,
            journey_stages=journey_stages,
            decisions=decisions,
        )
        return SYSTEM, user

    def validate(self, result: dict) -> None:
        if "component_categories" not in result:
            raise ValueError("Missing component_categories in design system output")

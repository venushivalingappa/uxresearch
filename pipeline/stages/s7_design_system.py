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

Return this exact JSON structure:
{{
  "component_categories": [
    {{
      "name": "Navigation | Forms | Feedback | Content | Layout | Actions",
      "components": [
        {{
          "component_name": "component name",
          "variants": ["variant 1", "variant 2", "variant 3"],
          "usage_context": ["which journey stages use this component"],
          "ux_principles_applied": ["UX law or principle name"],
          "priority": "must-have | should-have | nice-to-have",
          "states": ["default", "hover", "active", "disabled", "error"]
        }}
      ]
    }}
  ],
  "design_tokens": {{
    "color_roles": ["primary-action", "destructive", "success", "warning", "neutral", "surface", "on-surface"],
    "type_scale": [
      {{"name": "display", "size": "32px", "weight": "700", "usage": "hero headings"}},
      {{"name": "heading-1", "size": "24px", "weight": "600", "usage": "page titles"}},
      {{"name": "heading-2", "size": "20px", "weight": "600", "usage": "section titles"}},
      {{"name": "body", "size": "16px", "weight": "400", "usage": "body text"}},
      {{"name": "body-small", "size": "14px", "weight": "400", "usage": "secondary text"}},
      {{"name": "caption", "size": "12px", "weight": "400", "usage": "labels and captions"}},
      {{"name": "label", "size": "12px", "weight": "600", "usage": "form labels and tags"}}
    ],
    "spacing": {{
      "base_unit": "8px",
      "scale": ["4px", "8px", "12px", "16px", "24px", "32px", "48px", "64px"]
    }},
    "border_radius": {{
      "small": "4px",
      "medium": "8px",
      "large": "16px",
      "pill": "999px"
    }}
  }},
  "hierarchy_notes": "brief note on the component hierarchy and composition patterns"
}}

Cover at minimum: Navigation (tab bar, header, breadcrumb), Forms (input, select, checkbox, radio, button),
Feedback (toast, modal, empty state, loading, error), Content (card, list-item, avatar, badge),
Layout (container, divider, spacer)."""


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

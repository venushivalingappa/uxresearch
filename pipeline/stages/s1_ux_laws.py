from pipeline.base_stage import BaseStage

LAWS = [
    "Fitts' Law",
    "Hick's Law",
    "Miller's Law",
    "Jakob's Law",
    "Law of Proximity",
    "Aesthetic-Usability Effect",
    "Peak-End Rule",
    "Doherty Threshold",
    "Postel's Law",
    "Progressive Disclosure",
    "Tesler's Law (Conservation of Complexity)",
    "Von Restorff Effect",
]

SYSTEM = """You are a senior UX researcher and cognitive psychologist.
You apply UX laws and principles with precision, always anchoring every insight to the specific product context provided.
NEVER give generic textbook definitions — every sentence must be specific to the problem at hand.
Respond ONLY with valid JSON. No markdown fences, no explanation text."""

USER_TEMPLATE = """Problem Statement: {problem}

Analyse the following UX laws and principles as they apply to this specific problem.
For each law, provide a concrete, actionable analysis tied directly to this product.

Laws to analyse: {laws}

Return a JSON object in this exact structure:
{{
  "laws": [
    {{
      "law_name": "string",
      "definition": "one concise sentence definition",
      "application": "2-3 sentences about how THIS law specifically applies to the given problem — name specific UI elements, flows, or user behaviours",
      "implication": "one actionable design guideline derived from this law for this product",
      "priority": "high | medium | low"
    }}
  ]
}}

Priority guide: high = this law has major impact on core flows; medium = relevant to secondary features; low = worth noting but not critical."""


class UXLawsStage(BaseStage):
    stage_key = "ux_laws"

    def build_prompt(self, problem: str, context: dict) -> tuple[str, str]:
        user = USER_TEMPLATE.format(problem=problem, laws=", ".join(LAWS))
        return SYSTEM, user

    def validate(self, result: dict) -> None:
        if "laws" not in result or not isinstance(result["laws"], list):
            raise ValueError("Expected 'laws' array in UX Laws output")

import json
from pipeline.base_stage import BaseStage

SYSTEM = """You are a senior UX researcher facilitating a research synthesis and affinity mapping session.
Your job is to synthesise insights from prior analysis stages into actionable findings.
Every observation must be traceable to prior stage data — do not introduce new information.
Respond ONLY with valid JSON. No markdown fences, no explanation."""

USER_TEMPLATE = """Problem Statement: {problem}

Prior research data to synthesise (treat this as your research corpus):

UX Laws highlights: {laws_highlight}

Persona insights: {personas_highlight}

Design thinking insights: {dt_highlight}

Synthesise all of the above into a research synthesis document.

Return this exact JSON structure:
{{
  "raw_observations": [
    "observation 1 (cite source: 'From [Persona Name]' or 'From [Phase Name]')",
    ... 12 to 15 total observations
  ],
  "affinity_clusters": [
    {{
      "cluster_name": "short name for the cluster",
      "theme_colour": "yellow | pink | blue | green | orange",
      "observations": ["observation 1", "observation 2", "observation 3"],
      "cluster_insight": "one sentence synthesising this cluster's meaning"
    }}
  ],
  "key_themes": ["theme 1", "theme 2", "theme 3"],
  "opportunities": [
    "How Might We statement 1",
    "How Might We statement 2",
    "How Might We statement 3",
    "How Might We statement 4",
    "How Might We statement 5"
  ],
  "critical_insights": [
    {{
      "insight": "the key insight statement",
      "evidence": "specific evidence from prior stage data supporting this"
    }}
  ]
}}

Rules:
- Each raw_observation must cite its source stage or persona
- Affinity clusters should have 3-5 observations each; aim for 4 clusters
- HMW statements must start with exactly "How Might We"
- Critical insights: provide exactly 3, each with strong evidence
- Cluster insights should be in present-tense, active voice"""


class ResearchSynthesisStage(BaseStage):
    stage_key = "research_synthesis"

    def build_prompt(self, problem: str, context: dict) -> tuple[str, str]:
        laws = context.get("laws", {}).get("laws", [])
        laws_highlight = "; ".join(
            f"{l.get('law_name')}: {l.get('implication','')}"
            for l in laws[:5]
        ) or "None"

        personas = context.get("personas", {}).get("personas", [])
        personas_highlight = " | ".join(
            f"{p.get('name')}: goal={p.get('primary_goal')}; frustrations={p.get('frustrations',[][:2])}"
            for p in personas
        ) or "None"

        dt_phases = context.get("design_thinking", {}).get("phases", [])
        dt_highlight = " | ".join(
            f"{ph.get('phase_name')}: {ph.get('insights','')[:100]}"
            for ph in dt_phases
        ) or "None"

        user = USER_TEMPLATE.format(
            problem=problem,
            laws_highlight=laws_highlight,
            personas_highlight=personas_highlight,
            dt_highlight=dt_highlight,
        )
        return SYSTEM, user

    def validate(self, result: dict) -> None:
        for key in ("raw_observations", "affinity_clusters", "opportunities"):
            if key not in result:
                raise ValueError(f"Missing '{key}' in research synthesis output")

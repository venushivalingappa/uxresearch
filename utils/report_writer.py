import json
from pathlib import Path
from datetime import datetime


def _slug(text: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in text.lower())[:40]


def write_report(problem: str, context: dict, output_path: Path) -> None:
    lines = [
        f"# UX Research Report",
        f"",
        f"**Problem Statement:** {problem}",
        f"",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"",
        "---",
        "",
    ]

    # Stage 1: UX Laws
    if "laws" in context and "laws" in context["laws"]:
        lines += ["## Stage 1 — UX Laws & Principles", ""]
        for law in context["laws"]["laws"]:
            lines += [
                f"### {law.get('law_name', 'Unknown Law')}",
                f"**Definition:** {law.get('definition', '')}",
                f"",
                f"**Application:** {law.get('application', '')}",
                f"",
                f"**Design Implication:** {law.get('implication', '')}",
                f"",
                f"**Priority:** `{law.get('priority', 'medium')}`",
                "",
            ]
        lines += ["---", ""]

    # Stage 2: Proto Persona
    if "personas" in context and "personas" in context["personas"]:
        lines += ["## Stage 2 — Proto Personas", ""]
        for p in context["personas"]["personas"]:
            lines += [
                f"### {p.get('name', 'Persona')} — {p.get('occupation', '')}",
                f"**Age:** {p.get('age', '')} | **Tech Comfort:** {p.get('tech_comfort', '')}/5",
                f"",
                f"**Primary Goal:** {p.get('primary_goal', '')}",
                f"",
                f"> *\"{p.get('quote', '')}\"*",
                f"",
                f"**Frustrations:**",
            ]
            for f_ in p.get("frustrations", []):
                lines.append(f"- {f_}")
            lines += ["", "**Motivations:**"]
            for m in p.get("motivations", []):
                lines.append(f"- {m}")
            lines += ["", "**Relevant UX Laws:**"]
            for l_ in p.get("relevant_ux_laws", []):
                if isinstance(l_, dict):
                    lines.append(f"- **{l_.get('law_name','')}**: {l_.get('relevance','')}")
                else:
                    lines.append(f"- {l_}")
            lines += [""]
        lines += ["---", ""]

    # Stage 3: Design Thinking
    if "design_thinking" in context and "phases" in context["design_thinking"]:
        lines += ["## Stage 3 — Critical Design Thinking", ""]
        for phase in context["design_thinking"]["phases"]:
            lines += [f"### {phase.get('phase_name', '')}", ""]
            lines += ["**Key Questions:**"]
            for q in phase.get("key_questions", []):
                lines.append(f"- {q}")
            lines += ["", "**Activities:**"]
            for a in phase.get("activities", []):
                lines.append(f"- {a}")
            lines += ["", f"**Insights:** {phase.get('insights', '')}", ""]
        lines += ["---", ""]

    # Stage 4: Research Synthesis
    if "synthesis" in context:
        s = context["synthesis"]
        lines += ["## Stage 4 — Research Synthesis", ""]
        lines += ["### Affinity Clusters", ""]
        for cluster in s.get("affinity_clusters", []):
            lines += [f"**{cluster.get('cluster_name', '')}**"]
            for obs in cluster.get("observations", []):
                lines.append(f"- {obs}")
            lines += [f"*{cluster.get('cluster_insight', '')}*", ""]
        lines += ["### How Might We Opportunities", ""]
        for hmw in s.get("opportunities", []):
            lines.append(f"- {hmw}")
        lines += ["", "### Critical Insights", ""]
        for ci in s.get("critical_insights", []):
            if isinstance(ci, dict):
                lines += [f"**{ci.get('insight','')}**", f"Evidence: {ci.get('evidence','')}", ""]
            else:
                lines.append(f"- {ci}")
        lines += ["---", ""]

    # Stage 5: Journey Map
    if "journey" in context and "journey_stages" in context["journey"]:
        j = context["journey"]
        lines += [f"## Stage 5 — User Journey Map", f"", f"**Persona:** {j.get('persona_used', '')}", ""]
        for stage in j.get("journey_stages", []):
            score = stage.get('emotion_score', 0)
            emoji = "😊" if score > 0 else "😐" if score == 0 else "😔"
            lines += [
                f"### {stage.get('stage_name', '')} {emoji}",
                f"**Emotion Score:** {score}/2",
                f"**Thoughts:** {stage.get('thoughts', '')}",
                f"",
                f"**Touchpoints:** {', '.join(stage.get('touchpoints', []))}",
                f"**Pain Points:**",
            ]
            for pp in stage.get("pain_points", []):
                lines.append(f"- {pp}")
            lines += ["**Opportunities:**"]
            for op in stage.get("opportunities", []):
                lines.append(f"- {op}")
            lines += [""]
        lines += [f"**Overall Arc:** {j.get('overall_arc', '')}", "", "---", ""]

    # Stage 6: Design Rationale
    if "rationale" in context and "decisions" in context["rationale"]:
        lines += ["## Stage 6 — Design Rationale", ""]
        for dec in context["rationale"]["decisions"]:
            lines += [
                f"### {dec.get('decision_title', '')}",
                f"**Context:** {dec.get('context', '')}",
                f"",
                f"**Options Considered:**",
            ]
            for opt in dec.get("options_considered", []):
                lines.append(f"- {opt}")
            lines += [
                f"",
                f"**Chosen Approach:** {dec.get('chosen_approach', '')}",
                f"",
                f"**Rationale:** {dec.get('rationale', '')}",
                f"",
                f"**Trade-offs:** {dec.get('trade_offs', '')}",
                f"",
                f"**Success Metric:** {dec.get('success_metric', '')}",
                "",
            ]
        lines += ["---", ""]

    # Stage 7: Design System
    if "design_system" in context:
        ds = context["design_system"]
        lines += ["## Stage 7 — Design System Components", ""]
        for cat in ds.get("component_categories", []):
            lines += [f"### {cat.get('name', '')}", ""]
            for comp in cat.get("components", []):
                lines += [
                    f"**{comp.get('component_name', '')}** — Priority: `{comp.get('priority', '')}`",
                    f"Variants: {', '.join(comp.get('variants', []))}",
                    f"Used in: {', '.join(comp.get('usage_context', []))}",
                    f"UX Principles: {', '.join(comp.get('ux_principles_applied', []))}",
                    "",
                ]
        tokens = ds.get("design_tokens", {})
        lines += ["### Design Tokens", f"**Color Roles:** {', '.join(tokens.get('color_roles', []))}",
                  f"**Type Scale:** {', '.join(tokens.get('type_scale', []))}",
                  f"**Spacing:** {tokens.get('spacing', {}).get('base_unit', '')} base unit",
                  "", "---", ""]

    # Stage 8: Wireframes
    if "wireframes" in context and "screens" in context["wireframes"]:
        lines += ["## Stage 8 — Low-fi Wireframes", ""]
        for screen in context["wireframes"]["screens"]:
            lines += [
                f"### {screen.get('screen_name', '')}",
                f"**Purpose:** {screen.get('purpose', screen.get('screen_purpose',''))}",
                f"**Layout:** {screen.get('layout_type', '')}",
                f"",
                f"**Wireframe Description:**",
                f"{screen.get('wireframe_description', '')}",
                f"",
                f"**Components Used:** {', '.join(screen.get('components_used', []))}",
                f"",
                f"**Annotations:** {', '.join(screen.get('annotations', []))}",
                "",
            ]

    output_path.write_text("\n".join(lines), encoding="utf-8")

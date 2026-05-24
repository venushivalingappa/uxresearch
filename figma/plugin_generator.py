"""
Orchestrates the generation of all Figma plugin scripts.
Saves them to output/figma_scripts/ for users to paste into the Figma Dev Console.
"""
import json
from pathlib import Path

from config import FIGMA_SCRIPTS_DIR
from figma.figjam_boards import build_figjam_script
from figma.wireframe_frames import build_wireframe_script, build_component_sheet_script


FIGJAM_BOARDS = [
    ("ux_laws",            "01_ux_laws_reference.js",        "laws"),
    ("proto_persona",      "02_proto_persona_board.js",       "personas"),
    ("design_thinking",    "03_design_thinking_canvas.js",    "design_thinking"),
    ("research_synthesis", "04_research_synthesis_affinity.js", "synthesis"),
    ("journey_map",        "05_user_journey_map.js",          "journey"),
]

FIGMA_DESIGN_FILES = [
    ("wireframes",    "06_low_fi_wireframes.js"),
    ("design_system", "07_design_system_components.js"),
]


def generate_all_scripts(context: dict) -> list[Path]:
    FIGMA_SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    generated: list[Path] = []

    # FigJam boards
    for board_type, filename, ctx_key in FIGJAM_BOARDS:
        data = context.get(ctx_key, {})
        if not data:
            continue
        try:
            script = build_figjam_script(board_type, data)
            path = FIGMA_SCRIPTS_DIR / filename
            path.write_text(script, encoding="utf-8")
            generated.append(path)
        except Exception as e:
            print(f"Warning: Could not generate {filename}: {e}")

    # Wireframe script
    wireframe_data = context.get("wireframes", {})
    design_system_data = context.get("design_system", {})
    if wireframe_data:
        try:
            script = build_wireframe_script(wireframe_data, design_system_data)
            path = FIGMA_SCRIPTS_DIR / "06_low_fi_wireframes.js"
            path.write_text(script, encoding="utf-8")
            generated.append(path)
        except Exception as e:
            print(f"Warning: Could not generate wireframe script: {e}")

    # Component sheet script
    if design_system_data:
        try:
            script = build_component_sheet_script(design_system_data)
            path = FIGMA_SCRIPTS_DIR / "07_design_system_components.js"
            path.write_text(script, encoding="utf-8")
            generated.append(path)
        except Exception as e:
            print(f"Warning: Could not generate component sheet script: {e}")

    # Generate index file
    _write_index(generated)
    return generated


def _write_index(scripts: list[Path]) -> None:
    index_path = FIGMA_SCRIPTS_DIR / "README.txt"
    lines = [
        "UX Research Agent — Figma Scripts",
        "=" * 40,
        "",
        "How to use these scripts:",
        "1. Open Figma or FigJam in your browser or desktop app",
        "2. Go to Plugins → Development → Open Console  (or press Ctrl/Cmd+Alt+I)",
        "3. Paste the content of each script below",
        "4. Press Enter/Run",
        "",
        "Script order (run in order for best results):",
        "",
    ]
    for i, script in enumerate(scripts, 1):
        lines.append(f"  {i}. {script.name}")
        desc = {
            "01_ux_laws_reference.js":          "→ FigJam: UX Laws & Principles reference cards",
            "02_proto_persona_board.js":          "→ FigJam: Proto Persona cards with frustrations/motivations",
            "03_design_thinking_canvas.js":       "→ FigJam: Design Thinking 5-phase canvas",
            "04_research_synthesis_affinity.js":  "→ FigJam: Affinity map + HMW statements",
            "05_user_journey_map.js":             "→ FigJam: Full journey map swimlane diagram",
            "06_low_fi_wireframes.js":            "→ Figma: Black & white wireframes (375×812 mobile)",
            "07_design_system_components.js":     "→ Figma: Design system component reference sheet",
        }.get(script.name, "")
        if desc:
            lines.append(f"     {desc}")
    lines += ["", "Note: FigJam scripts (#1-5) should be run in FigJam files.", "      Figma scripts (#6-7) should be run in Figma design files."]
    index_path.write_text("\n".join(lines), encoding="utf-8")

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
JSON_DIR = OUTPUT_DIR / "json"
REPORTS_DIR = OUTPUT_DIR / "reports"
FIGMA_SCRIPTS_DIR = OUTPUT_DIR / "figma_scripts"

MODEL = "claude-sonnet-4-6"

STAGE_TOKEN_BUDGETS = {
    "ux_laws":            2048,
    "proto_persona":      3000,
    "design_thinking":    3000,
    "research_synthesis": 3000,
    "journey_map":        3500,
    "design_rationale":   3000,
    "design_system":      3500,
    "wireframes":         6000,
}

STAGE_ORDER = [
    "ux_laws",
    "proto_persona",
    "design_thinking",
    "research_synthesis",
    "journey_map",
    "design_rationale",
    "design_system",
    "wireframes",
]

STAGE_LABELS = {
    "ux_laws":            "Stage 1 — UX Laws & Principles",
    "proto_persona":      "Stage 2 — Proto Persona",
    "design_thinking":    "Stage 3 — Critical Design Thinking",
    "research_synthesis": "Stage 4 — Research Synthesis",
    "journey_map":        "Stage 5 — User Journey Map",
    "design_rationale":   "Stage 6 — Design Rationale",
    "design_system":      "Stage 7 — Design System Components",
    "wireframes":         "Stage 8 — Low-fi Wireframes",
}

STAGE_SUMMARIES = {
    "ux_laws":            lambda d: f"{len(d.get('laws', []))} laws mapped",
    "proto_persona":      lambda d: f"{len(d.get('personas', []))} personas created",
    "design_thinking":    lambda d: f"{len(d.get('phases', []))} phases explored",
    "research_synthesis": lambda d: f"{len(d.get('affinity_clusters', []))} clusters, {len(d.get('opportunities', []))} HMW statements",
    "journey_map":        lambda d: f"{len(d.get('journey_stages', []))} journey stages",
    "design_rationale":   lambda d: f"{len(d.get('decisions', []))} design decisions",
    "design_system":      lambda d: f"{sum(len(c.get('components',[])) for c in d.get('component_categories', []))} components mapped",
    "wireframes":         lambda d: f"{len(d.get('screens', []))} screens",
}

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
FIGMA_ACCESS_TOKEN = os.getenv("FIGMA_ACCESS_TOKEN", "")

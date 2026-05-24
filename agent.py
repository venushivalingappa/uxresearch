#!/usr/bin/env python3
"""
UX Research Agent
-----------------
Runs a full UX research pipeline from a single problem statement,
outputting structured JSON, a Markdown report, and Figma/FigJam
plugin scripts for every research artefact.

Usage:
  python agent.py --problem "Design an onboarding flow for a fintech app"
  python agent.py --problem "..." --resume
  python agent.py --problem "..." --skip-figma
  python agent.py --problem "..." --skip-stages ux_laws,proto_persona
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Validate API key before heavy imports
if not os.getenv("ANTHROPIC_API_KEY"):
    print("\n[ERROR] ANTHROPIC_API_KEY environment variable is not set.")
    print("  Set it in your shell or create a .env file — see .env.example\n")
    sys.exit(1)

from config import (
    REPORTS_DIR, FIGMA_SCRIPTS_DIR, JSON_DIR,
    ANTHROPIC_API_KEY, STAGE_LABELS,
)
from pipeline.orchestrator import Orchestrator
from figma.plugin_generator import generate_all_scripts
from utils.report_writer import write_report
from utils import display


def _slug(text: str) -> str:
    return "".join(c if c.isalnum() or c == "_" else "_" for c in text.lower())[:40]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ux-research-agent",
        description="Run a full UX research pipeline and generate Figma/FigJam artefacts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python agent.py --problem "Design an onboarding flow for a fintech mobile app"
  python agent.py --problem "Redesign the checkout flow for an e-commerce site" --resume
  python agent.py --problem "Build a task management app for remote teams" --skip-figma
  python agent.py --list-stages

Stages (run in order):
  ux_laws            — UX Laws & Principles mapping
  proto_persona      — Proto Persona creation (3 personas)
  design_thinking    — Critical Design Thinking (5 IDEO phases)
  research_synthesis — Affinity mapping & HMW statements
  journey_map        — User Journey Map
  design_rationale   — Design Rationale (6-8 decisions)
  design_system      — Design System components mapping
  wireframes         — Low-fidelity wireframe specifications
        """,
    )
    parser.add_argument(
        "--problem", "-p",
        type=str,
        help="The problem statement or design task to research",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from cached stage outputs (skips already-completed stages)",
    )
    parser.add_argument(
        "--skip-figma",
        action="store_true",
        help="Skip generating Figma plugin scripts",
    )
    parser.add_argument(
        "--skip-stages",
        type=str,
        default="",
        help="Comma-separated list of stage keys to skip",
    )
    parser.add_argument(
        "--list-stages",
        action="store_true",
        help="List all available stages and exit",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.list_stages:
        print("\nAvailable stages:")
        for key, label in STAGE_LABELS.items():
            print(f"  {key:<22} {label}")
        print()
        return

    if not args.problem:
        display.print_error(
            "Missing problem statement",
            "Provide a problem statement with --problem \"...\"\n"
            "Example: python agent.py --problem \"Design an onboarding flow for a fintech app\"",
        )
        sys.exit(1)

    problem = args.problem.strip()
    if len(problem) < 10:
        display.print_error("Problem too short", "Please provide a meaningful problem statement (at least 10 chars).")
        sys.exit(1)

    # Ensure output directories exist
    for d in (JSON_DIR, REPORTS_DIR, FIGMA_SCRIPTS_DIR):
        d.mkdir(parents=True, exist_ok=True)

    skip_stages = [s.strip() for s in args.skip_stages.split(",") if s.strip()]

    display.print_banner(problem)

    # ── Run pipeline ──────────────────────────────────────────
    orchestrator = Orchestrator(resume=args.resume, skip_stages=skip_stages)

    try:
        context = orchestrator.run(problem)
    except KeyboardInterrupt:
        display.print_error("Interrupted", "Pipeline was interrupted. Run with --resume to continue.")
        sys.exit(1)

    # ── Write Markdown report ─────────────────────────────────
    slug = _slug(problem)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS_DIR / f"ux_research_{slug}_{timestamp}.md"
    try:
        write_report(problem, context, report_path)
    except Exception as e:
        display.print_error("Report generation failed", str(e))
        report_path = REPORTS_DIR / "report_failed.md"

    # ── Generate Figma scripts ────────────────────────────────
    generated_scripts: list[Path] = []
    if not args.skip_figma:
        try:
            generated_scripts = generate_all_scripts(context)
        except Exception as e:
            display.print_error("Figma script generation failed", str(e))

    # ── Final summary ─────────────────────────────────────────
    display.print_pipeline_complete(
        str(JSON_DIR),
        str(report_path),
        str(FIGMA_SCRIPTS_DIR),
    )

    if generated_scripts and not args.skip_figma:
        display.print_figma_info()

    display.console.print(
        f"\n[dim]Tip: Open [bold]{report_path.name}[/bold] in any Markdown viewer for the full research report.[/dim]\n"
    )


if __name__ == "__main__":
    main()

import json
import sys
from pathlib import Path
from datetime import datetime

from config import STAGE_ORDER, STAGE_LABELS, STAGE_SUMMARIES, JSON_DIR
from utils.claude_client import StageExecutionError
from utils import display

from pipeline.stages.s1_ux_laws import UXLawsStage
from pipeline.stages.s2_proto_persona import ProtoPersonaStage
from pipeline.stages.s3_design_thinking import DesignThinkingStage
from pipeline.stages.s4_research_synthesis import ResearchSynthesisStage
from pipeline.stages.s5_journey_map import JourneyMapStage
from pipeline.stages.s6_design_rationale import DesignRationaleStage
from pipeline.stages.s7_design_system import DesignSystemStage
from pipeline.stages.s8_wireframes import WireframesStage

STAGE_CLASSES = {
    "ux_laws":            UXLawsStage,
    "proto_persona":      ProtoPersonaStage,
    "design_thinking":    DesignThinkingStage,
    "research_synthesis": ResearchSynthesisStage,
    "journey_map":        JourneyMapStage,
    "design_rationale":   DesignRationaleStage,
    "design_system":      DesignSystemStage,
    "wireframes":         WireframesStage,
}

CONTEXT_KEYS = {
    "ux_laws":            "laws",
    "proto_persona":      "personas",
    "design_thinking":    "design_thinking",
    "research_synthesis": "synthesis",
    "journey_map":        "journey",
    "design_rationale":   "rationale",
    "design_system":      "design_system",
    "wireframes":         "wireframes",
}


class Orchestrator:
    def __init__(self, resume: bool = False, skip_stages: list[str] | None = None):
        self.resume = resume
        self.skip_stages = set(skip_stages or [])
        JSON_DIR.mkdir(parents=True, exist_ok=True)

    def _json_path(self, stage_key: str) -> Path:
        return JSON_DIR / f"{stage_key}.json"

    def _load_cached(self, stage_key: str) -> dict | None:
        path = self._json_path(stage_key)
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                return None
        return None

    def _save(self, stage_key: str, data: dict) -> None:
        path = self._json_path(stage_key)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def run(self, problem: str) -> dict:
        context: dict = {}
        errors: list[str] = []

        total = len(STAGE_ORDER)
        with display.make_progress() as progress:
            task = progress.add_task("[cyan]Running UX Research Pipeline...", total=total)

            for stage_key in STAGE_ORDER:
                label = STAGE_LABELS[stage_key]
                ctx_key = CONTEXT_KEYS[stage_key]

                progress.update(task, description=f"[cyan]{label}")
                display.start_stage(label)

                # Resume: use cached result if available
                if self.resume:
                    cached = self._load_cached(stage_key)
                    if cached:
                        context[ctx_key] = cached
                        summary = STAGE_SUMMARIES[stage_key](cached)
                        display.stage_complete(stage_key, label, f"[dim](from cache)[/dim] {summary}")
                        progress.advance(task)
                        continue

                # Skip?
                if stage_key in self.skip_stages:
                    display.stage_complete(stage_key, label, "[dim]skipped[/dim]")
                    progress.advance(task)
                    continue

                try:
                    stage_instance = STAGE_CLASSES[stage_key]()
                    result = stage_instance.run(problem, context)
                    context[ctx_key] = result
                    self._save(stage_key, result)
                    summary = STAGE_SUMMARIES[stage_key](result)
                    display.stage_complete(stage_key, label, summary)
                except StageExecutionError as e:
                    display.stage_error(label, str(e))
                    errors.append(f"{label}: {e}")
                    # Continue pipeline with empty context for this stage
                    context[ctx_key] = {}
                except Exception as e:
                    display.stage_error(label, f"Unexpected error: {e}")
                    errors.append(f"{label}: {e}")
                    context[ctx_key] = {}

                progress.advance(task)

        if errors:
            display.print_section("Pipeline Warnings", "\n".join(f"[yellow]•[/yellow] {e}" for e in errors))

        return context

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.text import Text
from rich import box
from rich.rule import Rule
from rich.columns import Columns
from rich.align import Align

console = Console()


def print_banner(problem: str) -> None:
    console.print()
    console.print(Panel(
        f"[bold white]UX RESEARCH AGENT[/bold white]\n\n"
        f"[dim]Problem Statement:[/dim]\n[italic yellow]{problem}[/italic yellow]",
        border_style="bright_blue",
        padding=(1, 4),
    ))
    console.print()


def make_progress() -> Progress:
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    )


def start_stage(label: str) -> None:
    console.print()
    console.print(Rule(f"[bold cyan]{label}[/bold cyan]", style="cyan"))


def stage_complete(stage_key: str, label: str, summary: str) -> None:
    console.print(f"  [green]✓[/green] [bold]{label}[/bold] — [dim]{summary}[/dim]")


def stage_error(label: str, error: str) -> None:
    console.print(Panel(
        f"[red]{error}[/red]",
        title=f"[bold red]Error in {label}[/bold red]",
        border_style="red",
    ))


def print_pipeline_complete(json_dir: str, report_path: str, figma_scripts_dir: str) -> None:
    console.print()
    console.print(Rule("[bold green]Pipeline Complete[/bold green]", style="green"))
    console.print()

    table = Table(box=box.ROUNDED, border_style="green", show_header=False, padding=(0, 2))
    table.add_column("Item", style="dim")
    table.add_column("Path", style="bright_white")
    table.add_row("Research JSON files", json_dir)
    table.add_row("Markdown report", report_path)
    table.add_row("Figma plugin scripts", figma_scripts_dir)
    console.print(table)
    console.print()
    console.print(
        "[dim]To create Figma files: open Figma/FigJam → Plugins → Development → Open Console → paste each script.[/dim]"
    )
    console.print()


def print_figma_info() -> None:
    console.print(Panel(
        "[yellow]Figma plugin scripts generated.[/yellow]\n"
        "Run each script in [bold]Figma Development Console[/bold] to create the boards and wireframes.\n\n"
        "  [dim]1. Open Figma or FigJam in browser or desktop app[/dim]\n"
        "  [dim]2. Menu → Plugins → Development → Open Console[/dim]\n"
        "  [dim]3. Paste the relevant .js script and press Enter[/dim]",
        title="[bold]Figma Output Instructions[/bold]",
        border_style="yellow",
        padding=(1, 2),
    ))


def print_section(title: str, content: str) -> None:
    console.print(Panel(content, title=f"[bold]{title}[/bold]", border_style="blue", padding=(0, 2)))


def print_error(title: str, message: str) -> None:
    console.print(Panel(f"[red]{message}[/red]", title=f"[bold red]{title}[/bold red]", border_style="red"))

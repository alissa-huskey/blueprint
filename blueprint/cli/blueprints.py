"""Command Line Interface."""

from json import JSONDecodeError

import click
import rich_click as click  # noqa
from rich.console import Console
from rich.table import Table
from rich.traceback import install as rich_tracebacks

from blueprint import BlueprintError
from blueprint.plan import Plan

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.STYLE_OPTION = "bold cyan"
click.rich_click.STYLE_USAGE = "bold green"
click.rich_click.SHOW_METAVARS_COLUMN = True

bp = breakpoint

rich_tracebacks(show_locals=True)
console = Console()
errors = Console(stderr=True)


def error(ex: Exception):
    """Print an error message."""
    if isinstance(ex, BlueprintError):
        ex = ex.message

    errors.print(f"[red]Error[/red] {ex}")


@click.command()
def blueprints():
    """List blueprints."""
    table = Table("OK", "Name", "Title", "Description")

    for tpl in Plan.plans:
        cells = [tpl.id]
        try:
            tpl.specs
        except JSONDecodeError:
            ...
        else:
            cells.append(tpl.specs.get("title", ""))
            cells.append(tpl.specs.get("description", ""))

        if not tpl.ok():
            cells = [f"[dim]{text}" for text in cells]

        table.add_row(("[red]☒", "[green]☑")[tpl.ok()], *cells)

    console.print(table)

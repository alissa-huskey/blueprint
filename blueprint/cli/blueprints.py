"""Command Line Interface."""

import click
import rich_click as click  # noqa
from rich.table import Table

from blueprint import PlanError
from blueprint.cli.app import App
from blueprint.plan import Plan

bp = breakpoint

app = App()


@click.command()
def blueprints():
    """List blueprints."""
    table = Table("OK", "Name", "Title", "Description")

    for tpl in Plan.plans:
        cells = [tpl.id]
        try:
            tpl.specs
        except PlanError:
            ...
        else:
            cells.append(tpl.specs.get("title", ""))
            cells.append(tpl.specs.get("description", ""))

        if not tpl.ok():
            cells = [f"[dim]{text}" for text in cells]

        table.add_row(("[red]☒", "[green]☑")[tpl.ok()], *cells)

    app.console.print(table)

"""Command Line Interface."""

from json import JSONDecodeError

import click
import rich_click as click  # noqa
from rich.console import Console
from rich.table import Table
from rich_click.rich_command import RichCommand

from blueprint import BlueprintError, UserError
#  from blueprint import UserError
#  from blueprint.app import App
#  from blueprint.object import Object
from blueprint.template import Template

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.STYLE_OPTION = "bold cyan"
click.rich_click.STYLE_USAGE = "bold green"
click.rich_click.SHOW_METAVARS_COLUMN = True

bp = breakpoint

console = Console()
errors = Console(stderr=True)


def error(ex: Exception):
    """Print an error message."""
    if isinstance(ex, BlueprintError):
        ex = ex.message

    errors.print(f"[red]Error[/red] {ex}")


@click.group()
def blueprint():
    """Project blueprints."""


@blueprint.command()
def templates():
    """List templates."""
    table = Table("", "Name", "Title", "Description")

    for t in Template.templates:
        cells = [t.id]
        try:
            t.specs
        except JSONDecodeError:
            ...
        else:
            cells.append(t.specs.get("title", ""))
            cells.append(t.specs.get("description", ""))

        if not t.ok:
            cells = [f"[dim]{text}" for text in cells]

        table.add_row(("[red]E", "")[t.ok], *cells)

    console.print(table)


@blueprint.group()
def new():
    """Create a new project."""


# Generate commands from templates
for t in Template.templates:
    if not t.ok:
        continue

    def _():
        print("hello")

    params = []
    for name, spec in t.specs.get("options", {}).items():
        if (choices := spec.pop("choices", None)):
            spec["type"] = click.Choice(choices)
        option = click.Option([f"--{name}"], **spec)
        params.append(option)

    cmd = RichCommand(
        name=t.id,
        callback=_,
        help=t.specs["description"],
        params=params,
    )
    new.add_command(cmd)


def run():
    """Start the command line interface."""
    try:
        blueprint()
    except UserError as e:
        error(e.message)
        exit(e.status)
    # NOTE: This prevents typer from exiting with
    #       non-zero code on argument errors
    #  except SystemExit:
    #      ...


if __name__ == "__main__":
    run()

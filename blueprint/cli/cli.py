"""Command Line Interface."""

import click
import rich_click as click  # noqa
from click import confirm
from rich.console import Console
from rich.traceback import install as rich_tracebacks

from blueprint import BlueprintError, UserError
from blueprint.app import App
from blueprint.cli.blueprints import blueprints
from blueprint.cli.new import new
from blueprint.formatters import ppath

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


def verify(app: App):
    """Ask the user to confirm that they want to proceed."""
    path = ppath(app.project.path)
    prompt = f"Create {app.project.plan.name} project at '{path}'?"
    if not confirm(prompt):
        exit()


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def blueprint(*args, **kwargs):
    """Project blueprints."""


blueprint.add_command(blueprints)
blueprint.add_command(new)


def run():
    """Start the command line interface."""
    try:
        blueprint()
    except UserError as e:
        error(e.message)
        exit(e.status)
    except SystemExit as ex:
        exit(ex.code)


if __name__ == "__main__":
    run()

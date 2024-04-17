"""Command Line Interface."""

from pathlib import Path
from typing import Annotated

from rich.console import Console
from rich.traceback import install as rich_tracebacks
from typer import Argument, Exit, Option, Typer

from blueprint import BlueprintError
from blueprint.app import App

console = Console()
errors = Console(stderr=True)
rich_tracebacks(show_locals=True)
cli = Typer()


def error(self, ex: Exception):
    """Print an error message."""
    if isinstance(ex, BlueprintError):
        ex = ex.message

    self.errors.print(f"[red]Error[/red] {ex}")


def exit(self, status: int):
    """Exit with status code."""
    raise Exit(code=status)


@cli.command()
def init(
    name: Annotated[str, Argument(
        help="Name of project to create.",
    )],
    dest: Annotated[Path, Option(
        show_default=".",
        help="Where to create it.",
        rich_help_panel="Main",
    )] = Path.cwd(),
    python: Annotated[bool, Option(
            "--python",
            help="Create a Python project.",
            rich_help_panel="Main",
    )] = False,
):
    """Demonstrate example command."""
    app = App(name, dest, python=python)
    app.project.make()


def run():
    """Start the command line interface."""
    try:
        cli()
    except BlueprintError as e:
        error(e.message)
        exit(e.status)
    except SystemExit:
        ...


if __name__ == "__main__":
    run()

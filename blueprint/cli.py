"""Command Line Interface."""

from pathlib import Path
from typing import Annotated

from rich.console import Console
from rich.table import Table
from typer import Argument, BadParameter, Context, Exit, Option, Typer, confirm

from blueprint import BlueprintError
from blueprint.app import App

console = Console()
errors = Console(stderr=True)
cli = Typer()
new = Typer()


def error(ex: Exception):
    """Print an error message."""
    if isinstance(ex, BlueprintError):
        ex = ex.message

    errors.print(f"[red]Error[/red] {ex}")


def exit(status: int = 0):
    """Exit with status code."""
    raise Exit(code=status)


def verify(app: App):
    """Ask the user to confirm that they want to proceed."""
    prompt = f"Create {app.project.type} project at '{app.project.path}'?"
    if not confirm(prompt):
        exit()


def dest_exists(path: Path):
    """Callback to confirm the destination directory exists"""
    if not path.is_dir():
        raise BadParameter(f"No such directory: {path}")
    return path


@new.command()
def basic(
    ctx: Context,
    name: Annotated[str, Argument(
        help="Name of project to create.",
        show_default=False,
    )],
    dest: Annotated[Path, Option(
        show_default=".",
        help="Where to create the project.",
        rich_help_panel="Main",
        callback=dest_exists,
    )] = Path.cwd(),
):
    """Create a basic new project."""
    app = App(name, dest)
    verify(app)
    app.project.make()


@new.command()
def python(
    name: Annotated[str, Argument(
        help="Name of project to create.",
        show_default=False,
    )],
    dest: Annotated[Path, Option(
        show_default=".",
        help="Where to create the project.",
        rich_help_panel="Main",
        callback=dest_exists,
    )] = Path.cwd(),
    python_version: Annotated[str, Option(
        "--pyversion", "-P",
        help="Create a Python project.",
        rich_help_panel="Main",
    )] = "3.10.2",
):
    """Create Python project."""
    app = App(name, dest, python_version=python_version, python=True)
    verify(app)
    app.project.make()


cli.add_typer(new, name="new")

@cli.callback()
def default():
    """Create a new project from a blueprint."""


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

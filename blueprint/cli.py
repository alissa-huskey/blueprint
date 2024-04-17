"""Command Line Interface."""

from collections import namedtuple
from pathlib import Path
from sys import exit as sys_exit
from typing import Annotated

from rich.console import Console
from typer import Argument, BadParameter, Context, Option, Typer, confirm

from blueprint import BlueprintError, UserError
from blueprint.app import App
from blueprint.object import Object
from blueprint.python_project import PythonProject

console = Console()
errors = Console(stderr=True)
cli = Typer()
new = Typer()
Opts = Object()
Global = namedtuple("Global", ["name", "param", "default"], defaults=[None])


def exit(status: int = 0):
    """Exit with status code."""
    raise sys_exit(int(status))


def error(ex: Exception):
    """Print an error message."""
    if isinstance(ex, BlueprintError):
        ex = ex.message

    errors.print(f"[red]Error[/red] {ex}")


def verify(app: App):
    """Ask the user to confirm that they want to proceed."""
    prompt = f"Create {app.project.type} project at '{app.project.path}'?"
    if not confirm(prompt):
        exit()


def dest_exists(path: Path):
    """Confirm the destination directory exists."""
    if not path.is_dir():
        raise BadParameter(f"No such directory: {path}")
    return path


# subcommand: new
# =====================================================================================

Opts.name = Global(
    "name",
    Annotated[str, Argument(
        help="Name of project to create.",
        show_default=False,
    )],
)

Opts.dest = Global(
    "dest",
    Annotated[Path, Option(
        "--dest", "-d",
        show_default=".",
        help="Where to create the project.",
        rich_help_panel="Project",
        callback=dest_exists
    )],
    Path.cwd()
)

Opts.summary = Global(
    "summary",
    Annotated[str, Option(
        "--summary", "-s",
        show_default=False,
        help="One line project description.",
        rich_help_panel="Project",
    )],
)


@new.command()
def basic(
    ctx: Context,
    name: Opts.name.param,
    dest: Opts.dest.param = Opts.dest.default,
    summary: Opts.summary.param = Opts.summary.default,
):
    """Create a basic new project."""
    app = App(name, dest, summary=summary)
    verify(app)
    app.project.make()


@new.command()
def python(
    name: Opts.name.param,
    dest: Opts.dest.param = Opts.dest.default,
    summary: Opts.summary.param = Opts.summary.default,
    pyv: Annotated[str, Option(
        "--pyv", "-P",
        help="Python version to use.",
        rich_help_panel="Project",
    )] = PythonProject.DEFAULT_PYV,
    pyv_constraint: Annotated[str, Option(
        "--pyv-constraint", "-C",
        help="Supported Python versions.",
        rich_help_panel="Project",
    )] = PythonProject.DEFAULT_PYV_CONSTRAINT,
):
    """Create Python project."""
    app = App(
        name,
        dest,
        summary=summary,
        pyv=pyv,
        pyv_constraint=pyv_constraint,
        python=True
    )
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
    except UserError as e:
        error(e.message)
        exit(e.status)
    except UserError as e:
        error(e.message)
        exit(e.status)
    except SystemExit:
        ...


if __name__ == "__main__":
    run()

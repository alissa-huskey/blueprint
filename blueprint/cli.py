"""Command Line Interface."""

from json import JSONDecodeError
from pathlib import Path

import click
import rich_click as click  # noqa
from click import confirm
from rich.console import Console
from rich.table import Table
from rich_click import BadParameter
from rich_click.rich_command import RichCommand

from blueprint import BlueprintError, UserError
from blueprint.app import App
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


def shorten_path(path):
    """Replace home with `~` and cwd with `.`."""
    if path.is_relative_to(Path.cwd()):
        path = f"./{path.relative_to(Path.cwd())}"
    elif path.is_relative_to(Path.home()):
        path = f"~/{path.relative_to(Path.home())}"

    return path


def verify(app: App):
    """Ask the user to confirm that they want to proceed."""
    path = shorten_path(app.project.path)
    prompt = f"Create {app.project.template.name} project at '{path}'?"
    if not confirm(prompt):
        exit()


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def blueprint(*args, **kwargs):
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


def dest_exists(ctx, self, path: Path):
    """Confirm the destination directory exists."""
    if not path.is_dir():
        raise BadParameter(f"No such directory: {path}")
    return path


@blueprint.group()
def new():
    """Create a new project."""


def _new_project_cmd(template):
    """Return a callback to create a new project."""
    def _(*args, **kwargs):
        app = App(*args, template=template, **kwargs)
        verify(app)
        app.project.make()
    return _


# Generate commands from templates
for t in Template.templates:
    params = [
        click.Option(
            ["--dest", "-d"],
            help="Where to create the project.",
            type=Path,
            callback=dest_exists,
            default=Path.cwd()
        ),
        click.Option(
            ["--summary", "-s"],
            help="One line project description.",
        ),
        click.Option(
            ["--license", "-l"],
            help="License of the package.",
        ),
    ]
    for name, spec in (t.options or {}).items():
        if (choices := spec.pop("choices", None)):
            spec["type"] = click.Choice(choices)
        option = click.Option([f"--{name}"], **spec)
        params.append(option)

    params.append(
        click.Argument(["name"])
    )

    cmd = RichCommand(
        name=t.id,
        callback=_new_project_cmd(t.id),
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

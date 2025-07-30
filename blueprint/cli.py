"""Command Line Interface."""

from json import JSONDecodeError
from pathlib import Path

import click
import rich_click as click  # noqa
from click import confirm
from rich.console import Console
from rich.table import Table
from rich.traceback import install as rich_tracebacks
from rich_click import BadParameter
from rich_click.rich_command import RichCommand

from blueprint import BlueprintError, UserError
from blueprint.app import App
from blueprint.template import Template

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

    for tpl in Template.templates:
        cells = [tpl.id]
        try:
            tpl.specs
        except JSONDecodeError:
            ...
        else:
            cells.append(tpl.specs.get("title", ""))
            cells.append(tpl.specs.get("description", ""))

        if not tpl.ok:
            cells = [f"[dim]{text}" for text in cells]

        table.add_row(("[red]E", "")[tpl.ok], *cells)

    console.print(table)


def dest_should_exist(ctx, self, path: Path):
    """Confirm the destination directory exists."""
    if not path.is_dir():
        raise BadParameter(f"No such directory: {path}")
    return path


@blueprint.group()
def new():
    """Create a new project."""


new_options = {
    "dest": click.Option(
        ["--dest", "-d"],
        help="Where to create the project.",
        type=Path,
        callback=dest_should_exist,
        default=Path.cwd()
    ),
    "summary": click.Option(
        ["--summary", "-s"],
        help="One line project description.",
    ),
    "license": click.Option(
        ["--license", "-l"],
        default="MIT",
        help="License of the package.",
    ),
}


def _new_project_cmd(template):
    """Return a callback to create a new project."""
    def _(*args, **kwargs):
        app = App(*args, template=template, **kwargs)
        if app.project.path.is_dir():
            raise BadParameter(
                f"Project directory already exists: {app.project.path}",
                param=new_options["dest"],
            )
        verify(app)
        app.project.make()
    return _


# Generate commands from templates
for tpl in Template.templates:
    # generate options
    params = list(new_options.values())
    for name, spec in (tpl.options or {}).items():
        if (choices := spec.pop("choices", None)):
            spec["type"] = click.Choice(choices)
        option = click.Option([f"--{name}"], **spec)
        params.append(option)

    # generate arguments
    arguments = {"name": {}}
    if tpl.arguments:
        if "name" in tpl.arguments:
            arguments.pop("name", None)
        arguments.update(tpl.arguments)

    for name, spec in arguments.items():
        params.append(
            click.Argument([name], **spec)
        )

    # create command
    cmd = RichCommand(
        name=tpl.id,
        callback=_new_project_cmd(tpl.id),
        help=tpl.specs["description"],
        params=params,
    )

    # add subcommand to new
    new.add_command(cmd)


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

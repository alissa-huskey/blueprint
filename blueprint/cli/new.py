"""Command Line Interface."""

from pathlib import Path

import click
import rich_click as click  # noqa
from click import confirm
from rich.console import Console
from rich.traceback import install as rich_tracebacks
from rich_click import BadParameter
from rich_click.rich_command import RichCommand

from blueprint.app import App
from blueprint.formatters import ppath
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


def verify(app: App):
    """Ask the user to confirm that they want to proceed."""
    path = ppath(app.project.path)
    prompt = f"Create {app.project.plan.name} project at '{path}'?"
    if not confirm(prompt):
        exit()


def dest_should_exist(ctx, self, path: Path):
    """Confirm the destination directory exists."""
    if not path.is_dir():
        path = ppath(path)
        raise BadParameter(f"No such directory: {path}")
    return path


@click.group()
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


def _new_project_cmd(plan):
    """Return a callback to create a new project."""
    def _(*args, **kwargs):
        app = App(*args, plan=plan, **kwargs)
        if app.project.path.is_dir():
            path = ppath(app.project.path)
            raise BadParameter(
                f"Project directory already exists: {path}",
                param=new_options["dest"],
            )
        verify(app)
        app.project.make()
    return _


# Generate commands from plans
for tpl in Plan.plans:
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

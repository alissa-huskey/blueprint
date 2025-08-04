"""Overall application logic."""

import click
import rich_click as click  # noqa
from click import confirm
from rich.console import Console

from blueprint import BlueprintError
from blueprint.attr import attr, hasattrs
from blueprint.cli import tracebacks  # noqa
from blueprint.object import Object
from blueprint.project import Project

bp = breakpoint

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.STYLE_OPTION = "bold cyan"
click.rich_click.STYLE_USAGE = "bold green"
click.rich_click.SHOW_METAVARS_COLUMN = True


@hasattrs
class App(Object):
    """Application controller."""

    def __init__(self, **kwargs):
        """Create object."""
        self.name = kwargs.pop("name", None)
        self.plan = kwargs.pop("plan", None)

        self.kwargs = kwargs

        self.project = self.name

        self.console = Console()
        self.stderr = Console(stderr=True)

        super().__init__(**kwargs)

    @attr(method="setter")
    def project(self, project: str | Project) -> Project:
        """Set the project."""
        if not project:
            return
        if isinstance(project, str):
            project = Project(self.plan, self.name, **self.kwargs)
        self._project = project

    def error(self, ex: Exception):
        """Print an error message."""
        if isinstance(ex, BlueprintError):
            ex = ex.message

        self.stderr.print(f"[red]Error[/red] {ex}")

    def prompt(self, message: str):
        """Ask the user to confirm that they want to proceed."""
        if not confirm(message):
            exit()

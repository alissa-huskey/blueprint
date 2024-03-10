"""Overall application logic."""

from sys import exit

from rich.console import Console

from new_project import NewProjectError
from new_project.object import Object


class App(Object):
    """Application controller."""

    NAME = "new-project"

    console = Console()
    errors = Console(stderr=True)

    def __init__(self, name=None, **kwargs):
        """."""
        self.name = name or self.NAME
        super().__init__(**kwargs)

    def error(self, ex):
        """."""
        if isinstance(ex, NewProjectError):
            ex = ex.message

        self.errors.print(f"[red]Error[/red] {ex}")

    def exit(self, status):
        """."""
        exit(int(status))

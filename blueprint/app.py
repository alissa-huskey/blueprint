"""Overall application logic."""

from sys import exit

from rich.console import Console

from blueprint import BlueprintError
from blueprint.object import Object


class App(Object):
    """Application controller."""

    NAME = "blueprint"

    console = Console()
    errors = Console(stderr=True)

    def __init__(self, name=None, **kwargs):
        """."""
        self.name = name or self.NAME
        super().__init__(**kwargs)

    def error(self, ex):
        """."""
        if isinstance(ex, BlueprintError):
            ex = ex.message

        self.errors.print(f"[red]Error[/red] {ex}")

    def exit(self, status):
        """."""
        exit(int(status))

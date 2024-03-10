"""Module for a new project."""

from pathlib import Path

from new_project import AccessError
from new_project.attr import attr
from new_project.object import Object


class Project(Object):
    """A new project."""

    def __init__(self, name=None, dest=None):
        """Create a new project object."""
        self.name = name
        self.dest = dest

    def _dest_setter(self, value):
        """Validate and set dest."""
        if not value:
            return

        dest = Path(value)
        if not dest.is_dir():
            raise AccessError(f"Cannot create project in: '{dest}'")

        self._dest = dest
    dest = attr("dest", setter=_dest_setter)

    @property
    def path(self):
        """Path to the project directory."""
        return self.dest / self.name

    def create(self):
        """Create the project."""
        self.path.mkdir(exist_ok=True)

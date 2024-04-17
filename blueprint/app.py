"""Overall application logic."""

from functools import cached_property

from blueprint.object import Object
from blueprint.project import Project
from blueprint.project_factory import ProjectFactory


class App(Object):
    """Application controller."""

    NAME = "blueprint"

    def __init__(self, name=None, dest=None, **kwargs):
        """Create object."""
        self.kwargs = kwargs
        self.name = name or self.NAME
        self.dest = dest
        super().__init__(**kwargs)

    @cached_property
    def project(self) -> Project:
        """Project that is being created."""
        return ProjectFactory(self.name, self.dest, **self.kwargs)

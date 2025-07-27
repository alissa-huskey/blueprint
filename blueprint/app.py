"""Overall application logic."""

from functools import cached_property

from blueprint.object import Object
from blueprint.project import Project


class App(Object):
    """Application controller."""

    NAME = "blueprint"

    def __init__(self, **kwargs):
        """Create object."""
        super().__init__(**kwargs)
        self.name = kwargs.get("name") or self.NAME

    @cached_property
    def project(self) -> Project:
        """Project that is being created."""
        return Project(self.template, self.name, self.dest, **self.kwargs)

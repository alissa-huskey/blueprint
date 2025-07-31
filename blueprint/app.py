"""Overall application logic."""

from functools import cached_property

from blueprint.object import Object
from blueprint.project import Project

bp = breakpoint


class App(Object):
    """Application controller."""

    def __init__(self, name: str = None, **kwargs):
        """Create object."""
        self.name = name
        self.kwargs = kwargs
        super().__init__(**kwargs)

    @cached_property
    def project(self) -> Project:
        """Project that is being created."""
        self.kwargs.pop("plan", None)
        return Project(self.plan, self.name, **self.kwargs)

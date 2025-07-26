"""Blueprint tests."""

from contextlib import contextmanager

from blueprint.project_type import ProjectType

bp = breakpoint


@contextmanager
def set_types_root(root):
    """Temporarily modify the TYPES_ROOT directory of a Project class."""
    orig = ProjectType.TYPES_ROOT
    ProjectType.TYPES_ROOT = root
    yield
    ProjectType.TYPES_ROOT = orig

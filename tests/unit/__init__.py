"""Blueprint tests."""

from contextlib import contextmanager

from blueprint.config import Config
from blueprint.plan import Plan
from blueprint.schema import Schema

bp = breakpoint


@contextmanager
def set_plans_root(root):
    """Temporarily modify the Plan.ROOT directory of a Project class."""
    orig = Plan.ROOT
    Plan.ROOT = root
    yield
    Plan.ROOT = orig


@contextmanager
def set_schemas_root(root):
    """Temporarily modify the Schema.ROOT path."""
    orig = Schema.ROOT
    Schema.ROOT = root
    yield
    Schema.ROOT = orig


@contextmanager
def set_config_base(base):
    """Temporarily modify the BASE directory of a Project class."""
    orig = Config.BASE
    Config.BASE = base
    yield
    Config.BASE = orig

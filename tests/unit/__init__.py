"""Blueprint tests."""

from contextlib import contextmanager

from blueprint.config import Config
from blueprint.schema import Schema
from blueprint.template import Template

bp = breakpoint


@contextmanager
def set_templates_root(root):
    """Temporarily modify the TEMPLATES_ROOT directory of a Project class."""
    orig = Template.TEMPLATES_ROOT
    Template.TEMPLATES_ROOT = root
    yield
    Template.TEMPLATES_ROOT = orig


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

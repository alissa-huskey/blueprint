"""Blueprint tests."""

from contextlib import contextmanager

from blueprint.template import Template

bp = breakpoint


@contextmanager
def set_templates_root(root):
    """Temporarily modify the TEMPLATES_ROOT directory of a Project class."""
    orig = Template.TEMPLATES_ROOT
    Template.TEMPLATES_ROOT = root
    yield
    Template.TEMPLATES_ROOT = orig

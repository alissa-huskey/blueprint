"""Jinja template rendering."""

from jinja2 import Environment

from blueprint.attr import attr, hasattrs
from blueprint.formatters import (to_camel_case, to_kebab_case, to_pascal_case,
                                  to_smooshed_case, to_snake_case,
                                  to_title_case)
from blueprint.object import Object

bp = breakpoint


@hasattrs
class Template(Object):
    """Template object."""

    FILTERS = {
        "to_camel_case": to_camel_case,
        "to_kebab_case": to_kebab_case,
        "to_pascal_case": to_pascal_case,
        "to_smooshed_case": to_smooshed_case,
        "to_snake_case": to_snake_case,
        "to_title_case": to_title_case,
    }

    def __init__(self, text: str = "", **variables):
        """Initialize object."""
        self.text = text
        self.variables = variables

    @attr
    def _jinja(self) -> Environment:
        """Return a Jinja Environment object with filters added."""
        if not self._jinja_:
            self._jinja_ = Environment()
            self._jinja_.filters.update(self.FILTERS)
        return self._jinja_

    def render(self) -> str:
        """Render the template."""
        tpl = self._jinja.from_string(self.text)
        return tpl.render(**self.variables)

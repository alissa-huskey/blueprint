"""Jinja template engine."""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from jinja2 import Template as JinjaTemplate

from blueprint.attr import attr, hasattrs
from blueprint.formatters import (to_camel_case, to_kebab_case, to_pascal_case,
                                  to_smooshed_case, to_snake_case,
                                  to_title_case)
from blueprint.object import Object

bp = breakpoint


@hasattrs
class Jinja(Object):
    """Jinja template engine."""

    FILTERS = {
        "to_camel_case": to_camel_case,
        "to_kebab_case": to_kebab_case,
        "to_pascal_case": to_pascal_case,
        "to_smooshed_case": to_smooshed_case,
        "to_snake_case": to_snake_case,
        "to_title_case": to_title_case,
    }

    def __init__(self, paths: list | str | Path = None):
        """Initialize."""
        self.paths = paths

    @attr(method="setter")
    def paths(self, paths: list | str):
        """Access paths."""
        if not paths:
            return
        if isinstance(paths, str):
            paths = [paths]
        self._paths = paths

    @attr
    def fs(self) -> FileSystemLoader:
        """Access fs."""
        if not self._fs:
            if not self.paths:
                return

            self._fs = FileSystemLoader(self.paths)
        return self._fs

    @attr
    def env(self) -> Environment:
        """Return a Jinja Environment object."""
        if not self._env:
            self._env = Environment()
            if self.fs:
                self._env.loader = self.fs
            self._env.filters.update(self.FILTERS)
        return self._env

    def template(self, filename: str) -> JinjaTemplate:
        """Get a template file."""
        return self.env.get_template(filename)

    def render(self, text: str = None, file: str | JinjaTemplate = None, **variables):
        """Render a template."""
        if text:
            tpl = self.env.from_string(text)
        elif file:
            tpl = self.template(file)
        else:
            raise ValueError(
                "Template .render(): one of text or file argument required"
            )
        return tpl.render(**variables)

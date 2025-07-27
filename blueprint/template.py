"""Module logic related to reading and executing a blueprint.json file."""

import json
from json import JSONDecodeError
from pathlib import Path

from jsonschema import ValidationError, validate

from blueprint import ROOT
from blueprint.attr import attr, hasattrs
from blueprint.object import Object

bp = breakpoint


@hasattrs
class Template(Object):
    """A blueprint.json file."""

    TEMPLATES_ROOT = ROOT / "templates"

    def __init__(self, template_id=None, **kwargs):
        """Create a new project object."""
        self.id = template_id

        super().__init__(**kwargs)

    @classmethod
    @property
    def templates(cls):
        """Return a list of templates."""
        return [
            cls(path.name)
            for path in cls.TEMPLATES_ROOT.iterdir()
            if (path / "blueprint.json").is_file()
        ]

    @property
    def root(self) -> Path:
        """Return the path to the source files for this template."""
        return self.TEMPLATES_ROOT / self.id

    @property
    def skeleton(self) -> Path:
        """Return the path to the source files for this template."""
        return self.root / "skeleton"

    @attr(method="getter")
    def specs(self) -> dict:
        """Return the parsed blueprint.json file."""
        if not self._specs:
            with open(self.root / "blueprint.json") as fp:
                self._specs = json.load(fp)
        return self._specs

    @property
    def ok(self):
        """Return True if the Template is valid."""
        if not (self.root / "blueprint.json").is_file():
            return False

        try:
            self.specs
        except JSONDecodeError:
            return False

        schema = ROOT / "docs" / "blueprint.schema.json"

        with open(schema) as fp:
            schema = json.load(fp)

        try:
            validate(
                schema=schema,
                instance=self.specs,
            )
        except ValidationError:
            return False

        return True

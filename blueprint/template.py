"""Module logic related to reading and executing a blueprint.json file."""

import json
from json import JSONDecodeError
from pathlib import Path

from jsonschema import ValidationError, validate

from blueprint import ROOT, TemplateError
from blueprint.attr import attr, hasattrs
from blueprint.config import Config
from blueprint.dict import Dict
from blueprint.object import Object

bp = breakpoint


@hasattrs
class Template(Object):
    """A blueprint.json file."""

    SCHEMA_FILE = ROOT / "docs" / "blueprint.schema.json"

    SCHEMA = json.loads(SCHEMA_FILE.read_text())

    TEMPLATES_ROOT = ROOT / "templates"

    _ok = True

    def __init__(self, template_id: str = None, **kwargs):
        """Initialize object."""
        self.id = template_id

        super().__init__(**kwargs)

        for key, spec in self.SCHEMA.get("properties", {}).items():
            try:
                value = (self.specs or {}).get(key)
                setattr(self, key.replace("-", "_"), value)
            except TemplateError:
                self._ok = False

    def __eq__(self, other):
        """Equality."""
        return self.id == other.id

    @classmethod
    @property
    def templates(cls):
        """Return a list of templates."""
        return [
            cls(path.name)
            for path in cls.TEMPLATES_ROOT.iterdir()
            if (path / "blueprint.json").is_file()
        ]

    def _process_exe(self, exe) -> dict:
        """Process an #Executable from json.

        Convert "script" and "argument" keys to a command.
        """
        if (script := exe.pop("script", None)):
            path = self.root / "scripts" / script
            if not path.is_file():
                raise TemplateError(f"No such script: {path}")
            exe["cmd"] = [str(path), *exe.pop("arguments", [])]
        return exe

    @property
    def root(self) -> Path:
        """Return the path to the source files for this template."""
        return self.TEMPLATES_ROOT / self.id

    @property
    def blueprint(self) -> Path:
        """Path to the blueprint.json file."""
        return self.root / "blueprint.json"

    @property
    def skeleton(self) -> Path:
        """Return the path to the source files for this template."""
        return self.root / "skeleton"

    @attr
    def specs(self) -> dict:
        """Return the parsed blueprint.json file."""
        if not (self.id and self.blueprint.is_file()):
            return

        if not self._specs:
            with open(self.blueprint) as fp:
                self._specs = Dict(json.load(fp))
        return self._specs

    @attr(method="setter")
    def setup(self, value) -> list:
        """Set setup."""
        self._setup = [self._process_exe(step) for step in (value or [])]

    @attr(method="setter")
    def after(self, value) -> list:
        """Set after."""
        self._after = [self._process_exe(step) for step in (value or [])]

    @attr(method="setter")
    def variables(self, value) -> list:
        """Set variables."""
        self._variables = {
            k: self._process_exe(step) for k, step in (value or {}).items()
        }

    @property
    def ok(self):
        """Return True if the Template is valid."""
        if self._ok is False:
            return False

        if not self.blueprint.is_file():
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

    @attr
    def config(self) -> Config:
        """Return the Config object for this template."""
        if not self._config:
            self._config = Config(self.id)
        return self._config

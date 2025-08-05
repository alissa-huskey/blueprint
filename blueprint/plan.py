"""Module logic related to reading and executing a blueprint.json file."""

import json
from json import JSONDecodeError
from pathlib import Path
from shutil import which

from blueprint import ROOT, PlanError
from blueprint.attr import attr, hasattrs
from blueprint.config import Config
from blueprint.dict import Dict
from blueprint.jinja import Jinja
from blueprint.object import Object
from blueprint.schema import Schema

bp = breakpoint


@hasattrs
class Plan(Object):
    """A blueprint.json file."""

    _NO_REPR = ["_specs"]

    ROOT = ROOT / "plans"

    _ok = True
    _parent = None

    error: str = None

    def __init__(self, plan_id: str = None, read: bool = False, **kwargs):
        """Initialize object."""
        self.id = plan_id

        if self.schema and self.schema.properties:
            for key, spec in self.schema.properties.items():
                if key not in ["options", "arguments"]:
                    try:
                        value = (self.specs or {}).get(key)
                        setattr(self, key.replace("-", "_"), value)
                    except PlanError:
                        self._ok = False

        super().__init__(**kwargs)

    def __eq__(self, other):
        """Equality."""
        return isinstance(other, Plan) and self.id == other.id

    @classmethod
    @property
    def plans(cls):
        """Return a list of plans."""
        plans = []
        for path in cls.ROOT.iterdir():
            try:
                plans.append(cls(path.name))
            except PlanError:
                plan = cls()
                plan.id = path.name
                plans.append(plan)
        return plans

    @attr
    def schema(self):
        """Return the data parsed from the schema JSON."""
        if not self._schema:
            try:
                if self.specs and (name := self.specs.get("type")):
                    self._schema = Schema(name)
            except PlanError as ex:
                self.error = ex.message
                self._ok = False
                return
        return self._schema

    def _process_exe(self, exe) -> dict:
        """Process an #Executable from json.

        Convert "script" and "argument" keys to a command.
        """
        if (script := exe.pop("script", None)):
            path = self.root / "scripts" / script
            if not path.is_file():
                ids = ""
                if self.schema:
                    ids = f"{self.schema.id}, "
                ids += self.id
                raise PlanError(f"[{ids}] No such script: {path}")
            exe["cmd"] = [str(path), *exe.pop("arguments", [])]
        return exe

    @property
    def root(self) -> Path:
        """Return the path to the source files for this plan."""
        return self.ROOT / self.id

    @property
    def blueprint(self) -> Path:
        """Path to the blueprint.json file."""
        return self.root / "blueprint.json"

    @property
    def skeleton(self) -> Path:
        """Return the path to the source files for this plan."""
        return self.root / "skeleton"

    @attr
    def specs(self) -> dict:
        """Return the parsed blueprint.json file."""
        if not (self.id and self.blueprint.is_file()):
            return Dict()

        if not self._specs:
            try:
                with open(self.blueprint) as fp:
                    self._specs = Dict(json.load(fp))
            except JSONDecodeError as ex:
                msg = f"[{self.id}:{ex.lineno},{ex.colno}] JSON parse error: {ex.msg}"
                raise PlanError(msg)

        return self._specs

    @property
    def parent(self) -> "Plan":
        """Set the parent plan value."""
        if not self._parent and self.specs and self.specs.get("parent"):
            self._parent = Plan(self.specs.parent)
        return self._parent

    @parent.setter
    def parent(self, value):
        """Set the parent plan value."""
        if isinstance(value, str):
            value = Plan(value)
        self._parent = value

    @attr
    def options(self) -> Dict:
        """Return the plan options, recursive for parents."""
        if not self._options:
            self._options = Dict()
            if self.parent and self.parent.options:
                self._options.update(self.parent.options)
            if self.specs:
                self._options.update(self.specs.get("options", {}))
        return self._options

    @attr
    def arguments(self) -> Dict:
        """Return the plan arguments, recursive for parents."""
        if not self._arguments:
            self._arguments = Dict()
            if self.parent and self.parent.arguments:
                self._arguments.update(self.parent.arguments)
            if self.specs:
                self._arguments.update(self.specs.get("arguments", {}))
        return self._arguments

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

    def ok(self):
        """Return True if the Plan is valid."""
        if self._ok is False:
            return False

        ids = ""
        if self.schema:
            ids = f"{self.schema.id}, "
        ids += self.id
        prefix = f"[{ids}]"

        self.error = None

        if not self.blueprint.is_file():
            self.error = f"{prefix} No such blueprint file: {self.blueprint}"
            return False

        try:
            self.specs
        except PlanError as ex:
            self.error = f"{prefix} {ex.message}"
            return False

        is_valid = self.schema.validate(self.specs)
        if not is_valid:
            self.error = self.schema.error
            return False

        requirements = self.specs.get("requirements", [])
        for required in requirements:
            if not which(required):
                self.error = f"{prefix} missing requirement: '{required}'"
                return False

        return True

    @attr
    def jinja(self) -> Jinja:
        """Return a Jinja templating engine."""
        if not self._jinja:
            paths = [
                self.root / "after",
                self.root / "optional",
                self.root / "skeleton",
                self.root / "templates",
            ]
            self._jinja = Jinja(paths)
        return self._jinja

    @attr
    def config(self) -> Config:
        """Return the Config object for this plan."""
        if not self._config:
            self._config = Config(self.id)
        return self._config

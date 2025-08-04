"""JSON Schema files."""

import json
from copy import deepcopy
from json import JSONDecodeError
from pathlib import Path

from jsonschema.exceptions import UnknownType
from jsonschema.exceptions import _Error as JsonschemaError
from jsonschema.validators import validator_for
from referencing import Registry, Resource

from blueprint import ROOT, SchemaError
from blueprint.attr import attr, hasattrs
from blueprint.dict import Dict
from blueprint.object import Object

bp = breakpoint


@hasattrs
class Schema(Object):
    """JSON Schema files."""

    _NO_REPR = ["_data_raw", "_data", "_properties", "_path"]

    ROOT = ROOT / "schemas"

    _registry = None

    error = None
    _loaded = False
    _base = None
    _data_raw = None

    def __init__(self, id: str = None, load: bool = False, **kwargs):
        """Initialize the object."""
        self.id = id

        if load:
            self.load()

    @classmethod
    def retrieve(cls, id: str) -> Resource:
        """Return the Resource object for this $id."""
        path = cls.ROOT / id
        return Resource.from_contents(json.loads(path.read_text()))

    @classmethod
    @property
    def registry(cls) -> Registry:
        """Return a Resource registry for resolving $refs."""
        if not cls._registry:
            cls._registry = Registry(retrieve=cls.retrieve)
        return cls._registry

    @attr
    def _validator_class(self):
        """Return an a jsonschema validator class for this $schema."""
        if not self.data:
            return

        if not self._validator_class_:
            self._validator_class_ = validator_for(self._data_raw)
        return self._validator_class_

    @attr
    def _validator(self):
        """Return an instance of the jsonschema validator class for this $schema."""
        if not (self.ok and self.data):
            return

        if not self._validator_:
            Validator = self._validator_class
            self._validator_ = Validator(self._data_raw, registry=self.registry)
        return self._validator_

    def validate(self, data):
        """Validate an data as an instance of this schema.

        Return True if valid, otherwise the error message.
        """
        if not self._validator:
            return
        prefix = f"[{self.id}, {data.get('name', '')}]"
        try:
            self._validator.validate(data)
        except UnknownType as ex:
            message = f"{prefix} unknown type: {ex.type} (in {ex.instance})"
            self.error = message
            return False
        except (JsonschemaError) as ex:
            self.error = f"{prefix} {ex.message}"
            return False
        return True

    @attr(method="setter")
    def id(self, value) -> str:
        """Set the id of this schema.

        The value stored in the $id keyword, ie "base.schema.json".
        """
        if not value:
            return
        value = value.replace(".schema.json", "")
        self._id = f"{value}.schema.json"

    @property
    def name(self) -> str:
        """Return the name of this schema.

        ie "language-toolstack".
        """
        if not self.id:
            return
        return self.id.replace(".schema.json", "")

    @property
    def base(self) -> "Schema":
        """Return the schema that is referenced by the $ref keyword."""
        if not self._base and self.data.get("$ref"):
            self._base = Schema(self.data["$ref"])
        return self._base

    @attr
    def path(self) -> Path:
        """Return the path to the schema file."""
        if not self.id:
            return

        if not self._path:
            self._path = self.ROOT / self.id
            if not self._path.is_file():
                raise SchemaError(f"No such schema file: {self._path}")

        return self._path

    def ok(self):
        """Return True if the schema file and its base are valid."""
        try:
            self.load()
        except SchemaError as ex:
            self.error = ex.message
            return False

        try:
            self._validator_class.check_schema(self._data_raw)
        except JsonschemaError as ex:
            self.error = f"Schema error: {ex.json_path}: {ex.message}"
            return False
        return True

    def load(self):
        """Load the data from file."""
        self.data
        if not self._loaded and self.base:
            self._merge(self.base)
            self._loaded = True

    def _merge(self, parent: dict) -> dict:
        """Merge the data of this schema with its parent schemas."""
        self.data  # ensure derived data is loaded from file
        self._data = Dict(deepcopy(parent.data.to_dict()))

        properties = self._data.pop("properties", {})
        properties.update(self._data_raw.get("properties", {}))

        self._data.update(self._data_raw)
        self._data.properties = properties

    @attr
    def data(self) -> Dict:
        """Return the parsed JSON."""
        if not self._data:
            if not self.path:
                return
            try:
                with open(self.path) as fp:
                    # save a backup/reference of the raw data as
                    # self._data is merged with parent schema data
                    self._data_raw = json.load(fp)
                    self._data = Dict(deepcopy(self._data_raw))
            except JSONDecodeError as ex:
                raise SchemaError(
                    f"JSON parse error, schema: {self.path.name}, error: {ex.msg}"
                )
        return self._data

    @attr
    def properties(self) -> Path:
        """Return a dictionary of properties and values."""
        self.load()
        if not self._properties and self.data:
            self._properties = self.data.get("properties", {})
        return self._properties

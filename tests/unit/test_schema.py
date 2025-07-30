import json

import pytest  # noqa
from jsonschema.validators import Draft202012Validator
from referencing import Registry, Resource
from referencing._core import Retrieved

from blueprint.schema import Schema
from tests.unit import set_schemas_root

bp = breakpoint


def test_schema():
    schema = Schema()

    assert schema


def test_schema_id():
    """
    GIVEN: A Schema object
    WHEN: The .id setter is used
    THEN: The id should be set to VALUE.schema.json
    """
    schema = Schema()

    for value in ["generic", "generic.schema.json"]:
        schema.id = value

        assert schema.id == "generic.schema.json", f"When set to: {value}"


def test_schema_name():
    """
    GIVEN: A Schema object with an .id value
    WHEN: .name is accessed
    THEN: it should return the .id prefix (before .schema.json)
    """
    schema = Schema("generic")

    assert schema.name == "generic"


def test_schema_path():
    """
    GIVEN: A Schema object with a .id value
    AND:   a Schema.ROOT path
    WHEN: .path is accessed
    THEN: it should return the path to that schema
    """
    schema = Schema("generic")

    assert schema.path == schema.ROOT / "generic.schema.json"


def test_schema_base():
    """
    GIVEN: A Schema object with a $ref value
    WHEN: .base is called
    THEN: it should return the Schema object for the $ref target
    """
    schema = Schema("generic")

    assert schema.base == Schema("base")


def test_schema_data():
    """
    GIVEN:A schema object with a .id value
    AND:  a valid JSON file at schema.path
    WHEN: .data is accessed
    THEN: it should return the data parsed from JSON
    AND:  it should set ._data_raw to a ba a backup of ._data
    """
    schema = Schema("generic")

    assert isinstance(schema.data, dict)
    assert schema.data.title == "Blueprint generic schema."
    assert schema._data_raw == schema._data


def test_schema__merge():
    """
    GIVEN: A Schema object with a .id value
    AND:   a valid JSON file at .path
    AND:   another schema object with a .id value
           (used for the .base schema, but could be any)
    AND:   a valid JSON file at other.path
    WHEN:  ._merge() is called with another schema object
    THEN:  it should merge the two schema's property dictionaries,
           with other taking precedence
    AND:   it should merge the two schema's data dictionaries,
           with other taking precedence
    """
    schema = Schema("generic")
    schema._merge(Schema("base"))

    assert schema.data.title == "Blueprint generic schema."
    assert schema.data.get("version") == "0.1.0"
    assert schema._data_raw.get("version") is None
    assert schema.data.properties.get("name")


def test_schema_properties():
    """
    GIVEN: A Schema object with a .id value
    AND:   a valid JSON file at .path
    AND:   a .base schema
    WHEN:  .properties is accessed
    THEN:  it should call .load()
    AND:   it should return the merged properties dictionary
    """
    schema = Schema("language-toolstack")

    keys = [
        "after",
        "arguments",
        "dependency-commands",
        "description",
        "name",
        "options",
        "parent",
        "project-dir",
        "requirements",
        "setup",
        "stack",
        "title",
        "type",
        "variables",
        "version",
    ]

    schema.properties
    assert isinstance(schema.properties, dict)
    assert sorted(schema.properties.keys()) == keys


def test_schema_ok(tmp_path):
    """
    GIVEN: A Schema object and a valid JSON file
    WHEN: .ok() is called
    THEN: it should return True if the schema and its base are valid
    """
    base_path = tmp_path / "base.schema.json"
    base_content = """
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "base.schema.json",
            "title": "Blueprint base schema",
            "description": "Blueprint template definition.",
            "version": "0.1.0",
            "type": "object"
        }
    """
    base_path.write_text(base_content)

    with set_schemas_root(tmp_path):
        schema = Schema("base")
        assert schema.ok() is True


def test_schema_not_ok_missing_file(tmp_path):
    """
    GIVEN: A Schema object with a path
    AND:   No file at that path
    WHEN:  .ok() is called
    THEN:  it should return False
    """
    with set_schemas_root(tmp_path):
        schema = Schema("base")
        assert schema.ok() is False
        assert schema.error == f"No such schema file: {schema.path}"


def test_schema_not_ok_parse_error(tmp_path):
    """
    GIVEN: A Schema object with a path
    AND:   A JSON file at that path that is invalid JSON
    WHEN:  .ok() is called
    THEN:  it should return False
    """
    base_path = tmp_path / "base.schema.json"

    # Note trailing comma
    base_content = """
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "base.schema.json",
            "title": "Blueprint base schema",
            "description": "Blueprint template definition.",
            "version": "0.1.0",
            "type": "object",
        }
    """
    base_path.write_text(base_content)

    with set_schemas_root(tmp_path):
        schema = Schema("base")
        err = "Expecting property name enclosed in double quotes"
        assert schema.ok() is False
        assert schema.error == \
            f"JSON parse error, schema: base.schema.json, error: {err}"


def test_schema_not_ok_jsonschema_schema_error(tmp_path):
    """
    GIVEN: A Schema object with a path
    AND:   A JSON schema file at that path that has a schema error
    WHEN:  .ok() is called
    THEN:  it should return False
    """
    base_path = tmp_path / "base.schema.json"

    # Note trailing comma
    base_content = """
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "base.schema.json",
            "title": "Blueprint base schema",
            "description": "Blueprint template definition.",
            "version": "0.1.0",
            "properties": 1
        }
    """
    base_path.write_text(base_content)

    with set_schemas_root(tmp_path):
        schema = Schema("base")
        assert schema.ok() is False
        assert schema.error == \
            "Schema error: $.properties: 1 is not of type 'object'"


def test_schema_retrieve(tmp_path):
    """
    GIVEN: A JSON file located in the Schema.ROOT directory
    WHEN:  Schema.retrieve() is called with the filename
    THEN:  A Resource object should be returned for that schema
    """
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "base.json.schema",
    }

    path = (tmp_path / "base.schema.json")
    path.write_text(json.dumps(schema))

    with set_schemas_root(tmp_path):
        resource = Schema.retrieve("base.schema.json")
        assert isinstance(resource, Resource)
        assert resource.contents == schema


def test_schema_registry(tmp_path):
    """
    GIVEN: Valid json files in the Schema.ROOT directory
    WHEN:  Schema.registry is accessed
    THEN:  It should return a Registry object that can retrieve Retrieved
           objects from schema $ids.
    """
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "base.json.schema",
    }

    path = (tmp_path / "base.schema.json")
    path.write_text(json.dumps(schema))

    with set_schemas_root(tmp_path):
        registry = Schema.registry

        assert isinstance(registry, Registry)

        retrieved = registry.get_or_retrieve("base.schema.json")

        assert isinstance(retrieved, Retrieved)
        assert retrieved.value.contents == schema


def test_schema__validator(tmp_path):
    """
    GIVEN: A Schema object that points to a valid JSON file
    AND:   That file has a valid $schema value set
    WHEN:  .validator is accessed
    THEN:  it should return an instance of one of the jsonschema validator
           classes (usually Draft202012Validator)
    AND:   the validator._registry should be the Schema.registry object
    """
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "base.json.schema",
    }

    path = (tmp_path / "base.schema.json")
    path.write_text(json.dumps(schema))

    with set_schemas_root(tmp_path):
        schema = Schema("base")
        validator = schema._validator

        assert isinstance(validator, Draft202012Validator)
        assert isinstance(validator._registry, Registry)
        assert validator._registry == Schema.registry


@pytest.mark.parametrize(["desc", "data", "expected", "error"], [
    ["A valid dict", {"title": "A project"}, True, None],
    ["An invalid dict", {"name": "A project"}, False, "'title' is a required property"],
])
def test_schema_validate(tmp_path, desc, data, expected, error):
    """
    GIVEN: A Schema object with a ._validator value
    WHEN:  .validate() is called
    THEN:  it should return True if the JSON is a valid instance of the schema
    OR:    it should return False otherwise
    """
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "base.json.schema",
        "type": "object",
        "required": ["title"],
        "properties": {
            "title": {
                "type": "string"
            },
        },
    }

    path = (tmp_path / "base.schema.json")
    path.write_text(json.dumps(schema))

    with set_schemas_root(tmp_path):
        schema = Schema("base")
        is_valid = schema.validate(data)

        assert is_valid is expected, desc
        assert schema.error == error


def test_schema_x():
    """
    GIVEN: ...
    WHEN:  ...
    THEN:  ...
    """

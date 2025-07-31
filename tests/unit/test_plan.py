import json

import pytest

from blueprint.config import Config
from blueprint.plan import Plan
from blueprint.schema import Schema
from tests.unit import set_plans_root

bp = breakpoint


@pytest.fixture
def blueprint_json():
    """Return the contents of a barebones blueprint.json file."""
    return """
        {
            "name": "plan",
            "title": "Project Plan",
            "description": "A project plan.",
            "version": "0.1.0",
            "type": "generic"
        }
    """


def test_plan():
    plan = Plan()

    assert plan


def test_plan_plans(tmp_path):
    """
    GIVEN: A ROOT directory
    AND: subdirectories that contain `blueprint.json` files
    WHEN: Plan.plans is accessed
    THEN: it should return a list of Plan objects for each of those
          subdirectories
    """
    plans_root = tmp_path

    abc = tmp_path / "abc"
    xyz = tmp_path / "xyz"

    for d in [abc, xyz]:
        d.mkdir(parents=True)
        (d / "blueprint.json").write_text("{}")

    with set_plans_root(plans_root):
        plans = Plan.plans

    assert plans == [Plan("abc"), Plan("xyz")]


def test_plan_root(root):
    plan = Plan("basic")
    plan_root = root / "plans" / "basic"

    assert plan.root == plan_root


def test_plan_skeleton(root):
    plan = Plan("basic")

    assert plan.skeleton == root / "plans" / "basic" / "skeleton"


def test_plan_specs(root):
    """
    GIVEN: a blueprint.json file
    WHEN: specs is accessed
    THEN: it should return the data parsed from the json file
    """
    plan = Plan("basic")

    assert isinstance(plan.specs, dict)
    assert plan.specs.get("name") == "Basic"


def test_plan_parent():
    """
    GIVEN: A Plan with a parent defined in the spec
    WHEN: .parent is accessed
    THEN: it should return the Plan for that variable
    """
    plan = Plan("python-poetry")
    assert plan.parent == Plan("basic")


def test_plan_has_requirements():
    ...


def test_plan_ok_true(tmp_path, blueprint_json):
    plandir = tmp_path / "project"
    plandir.mkdir()

    bp_json = plandir / "blueprint.json"
    bp_json.write_text(blueprint_json)

    with set_plans_root(tmp_path):
        plan = Plan("project")

        assert plan.ok() is True


def test_plan_not_ok_missing_file(tmp_path):
    plandir = tmp_path / "project"
    plandir.mkdir()

    with set_plans_root(tmp_path):
        plan = Plan("project")

        assert plan.ok() is False
        assert plan.error == f"No such blueprint file: {plan.blueprint}"


def test_plan_not_ok_invalid_file(tmp_path, blueprint_json):
    plandir = tmp_path / "project"
    plandir.mkdir()

    bp_json = plandir / "blueprint.json"
    bp_json.write_text("""
        {
            "name": "plan",
            "title": "Project Plan",
            "version": "0.1.0",
            "type": "language-toolstack"
        }
    """)

    with set_plans_root(tmp_path):
        plan = Plan("project")

        assert plan.ok() is False
        assert plan.error == "'description' is a required property"


def test_plan_config():
    ...


def test_plan_setup(fixtures_path):
    """
    GIVEN: A Plan object
    WHEN: `.setup =` is called
    THEN: Each step should be run through ._process_exe()
    """
    with set_plans_root(fixtures_path):
        plan = Plan()
        plan.id = "toolstack"
        plan.setup = [
            {
                "script": "do-thing",
                "arguments": ["--a", "--b", "--c"],
            }
        ]

        cmd = {
            "cmd": [str(plan.root / "scripts" / "do-thing"), "--a", "--b", "--c"],
        }

        assert plan.setup == [cmd]


def test_plan_after(fixtures_path):
    """
    GIVEN: A Plan object
    WHEN: `.after =` is called
    THEN: Each step should be run through ._process_exe()
    """
    with set_plans_root(fixtures_path):
        plan = Plan()
        plan.id = "toolstack"
        plan.after = [
            {
                "script": "do-thing",
                "arguments": ["--a", "--b", "--c"],
            }
        ]

        cmd = {
            "cmd": [str(plan.root / "scripts" / "do-thing"), "--a", "--b", "--c"],
        }

        assert plan.after == [cmd]


def test_plan_variables(fixtures_path):
    """
    GIVEN: A Plan object
    WHEN: `.variables =` is called
    THEN: Each step should be run through ._process_exe()
    """
    with set_plans_root(fixtures_path):
        plan = Plan()
        plan.id = "toolstack"
        plan.variables = {
            "VARIABLE": {
                "script": "do-thing",
                "arguments": ["--a", "--b", "--c"],
            }
        }

        cmd = {
            "cmd": [str(plan.root / "scripts" / "do-thing"), "--a", "--b", "--c"],
        }

        assert plan.variables == {"VARIABLE": cmd}


def test_plan_process_exe(fixtures_path):
    """
    GIVEN: A Plan object
    AND: A spec that includes variables, steps, or after keys defined with
        a script and optionally arguments
    WHEN: Those keys are accessed
    THEN: They should be converted into a single command
    """
    with set_plans_root(fixtures_path):
        plan = Plan()
        plan.id = "toolstack"
        result = plan._process_exe({
            "script": "do-thing",
            "arguments": ["--a", "--b", "--c"],
        })

        cmd = {
            "cmd": [str(plan.root / "scripts" / "do-thing"), "--a", "--b", "--c"],
        }

        assert result == cmd


def test_plan_spec_attrs(fixtures_path):
    """
    GIVEN: A Plan object
    AND: a blueprint.json file
    WHEN: a key defined in the properties of blueprint.schema.json is accessed
    THEN: it should return the attrdict for that key in the blueprint.json file

    """
    keys = [
        "name",
        "title",
        "description",
        "version",
        "type",
        "parent",
        "requirements",
        "stack",
        "config",
        "variables",
        "setup",
        "after",
    ]

    with set_plans_root(fixtures_path):
        plan = Plan("toolstack")

        for key in keys:
            assert hasattr(plan, key), f"The {key} attr should be set."

        assert plan.name == "python-poetry"
        assert plan.title == "Python: Poetry"
        assert plan.description == "Python project managed by poetry."
        assert plan.version == "0.1.0"
        assert plan.type == "language-toolstack"
        assert plan.parent == Plan("basic")


def test_plan_config():
    plan = Plan("basic")

    assert isinstance(plan.config, Config)
    assert plan.config.path == Config.BASE / "basic.yml"


def test_plan_arguments(tmp_path, blueprint_json):
    specs = json.loads(blueprint_json)
    specs["arguments"] = {"a": {}}
    (tmp_path / "basic").mkdir()
    (tmp_path / "basic" / "blueprint.json").write_text(json.dumps(specs))

    with set_plans_root(tmp_path):
        plan = Plan("basic")

        assert plan.arguments == {"a": {}}


def test_plan_arguments_parents(tmp_path, blueprint_json):
    plans = {
        "base": {
            "arguments": {
                "a": {"help": "base a option"},
                "b": {"help": "base b option"},
                "c": {"help": "base c option"},
            },
        },
        "php": {
            "parent": "base",
            "arguments": {
                "b": {"help": "php b option"},
                "c": {"help": "php c option"},
            },
        },
        "phpbb-ext": {
            "parent": "php",
            "arguments": {
                "c": {"help": "phpbb-ext c option"},
                "d": {"help": "phpbb-ext d option"},
            },
        },
    }
    specs = json.loads(blueprint_json)

    for name, cfg in plans.items():
        tpl_specs = specs.copy()
        tpl_specs["arguments"] = cfg["arguments"]
        tpl_specs["parent"] = cfg.get("parent")
        (tmp_path / name).mkdir()
        (tmp_path / name / "blueprint.json").write_text(json.dumps(tpl_specs))

    arguments = {
        "a": plans["base"]["arguments"]["a"],
        "b": plans["php"]["arguments"]["b"],
        "c": plans["phpbb-ext"]["arguments"]["c"],
        "d": plans["phpbb-ext"]["arguments"]["d"],
    }

    with set_plans_root(tmp_path):
        plan = Plan("phpbb-ext")
        plan.arguments
        assert plan.arguments == arguments


def test_plan_options(tmp_path, blueprint_json):
    specs = json.loads(blueprint_json)
    specs["options"] = {"a": {}}
    (tmp_path / "basic").mkdir()
    (tmp_path / "basic" / "blueprint.json").write_text(json.dumps(specs))

    with set_plans_root(tmp_path):
        plan = Plan("basic")

        assert plan.options == {"a": {}}


def test_plan_options_parents(tmp_path, blueprint_json):
    plans = {
        "base": {
            "options": {
                "a": {"help": "base a option"},
                "b": {"help": "base b option"},
                "c": {"help": "base c option"},
            },
        },
        "php": {
            "parent": "base",
            "options": {
                "b": {"help": "php b option"},
                "c": {"help": "php c option"},
            },
        },
        "phpbb-ext": {
            "parent": "php",
            "options": {
                "c": {"help": "phpbb-ext c option"},
                "d": {"help": "phpbb-ext d option"},
            },
        },
    }
    specs = json.loads(blueprint_json)

    for name, cfg in plans.items():
        tpl_specs = specs.copy()
        tpl_specs["options"] = cfg["options"]
        tpl_specs["parent"] = cfg.get("parent")
        (tmp_path / name).mkdir()
        (tmp_path / name / "blueprint.json").write_text(json.dumps(tpl_specs))

    options = {
        "a": plans["base"]["options"]["a"],
        "b": plans["php"]["options"]["b"],
        "c": plans["phpbb-ext"]["options"]["c"],
        "d": plans["phpbb-ext"]["options"]["d"],
    }

    with set_plans_root(tmp_path):
        plan = Plan("phpbb-ext")
        plan.options
        assert plan.options == options


def test_plan_schema():
    plan = Plan("basic")
    schema = plan.schema

    assert isinstance(schema, Schema)
    assert schema.id == "generic.schema.json"


def test_plan_x():
    ...

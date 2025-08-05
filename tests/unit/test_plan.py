from blueprint.config import Config
from blueprint.jinja import Jinja
from blueprint.plan import Plan
from blueprint.schema import Schema
from tests.unit import make_blueprint, set_plans_root

bp = breakpoint


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
    make_blueprint(tmp_path, "abc", {})
    make_blueprint(tmp_path, "xyz", {})

    with set_plans_root(tmp_path):
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


def test_plan_ok_true(tmp_path, blueprint_json):
    make_blueprint(tmp_path, "project", blueprint_json)

    with set_plans_root(tmp_path):
        plan = Plan("project")

        assert plan.ok() is True


def test_plan_not_ok_missing_file(tmp_path):
    make_blueprint(tmp_path, "project", False)

    with set_plans_root(tmp_path):
        plan = Plan("project")

        assert plan.ok() is False
        assert plan.error == f"[project] No such blueprint file: {plan.blueprint}"


def test_plan_not_ok_parse_error(tmp_path):
    contents = """
        {
            "name": "project",
            "title": "Project Plan",
            "version": "0.1.0",
            "type": "language-toolstack",
        }
    """
    make_blueprint(tmp_path, "project", contents)

    with set_plans_root(tmp_path):
        plan = Plan("project")

        assert plan.ok() is False
        assert plan.error == (
            "[project:7,9] "
            "JSON parse error: Expecting property name enclosed in double quotes"
        )


def test_plan_not_ok_invalid_file(tmp_path):
    # invalid because it's missing "type" key
    contents = """
        {
            "name": "plan",
            "title": "Project Plan",
            "version": "0.1.0",
            "type": "language-toolstack"
        }
    """
    make_blueprint(tmp_path, "project", contents)

    with set_plans_root(tmp_path):
        plan = Plan("project")

        assert plan.ok() is False
        assert plan.error == (
            "[language-toolstack.schema.json, plan] "
            "'description' is a required property"
        )


def test_plan_not_ok_missing_requirements(tmp_path, blueprint_json):
    # invalid because it's missing "type" key
    blueprint_json["requirements"] = ["xxx"]
    make_blueprint(tmp_path, "project", blueprint_json)

    with set_plans_root(tmp_path):
        plan = Plan("project")

        assert plan.ok() is False
        assert plan.error == (
            "[generic.schema.json, project] "
            "missing requirement: 'xxx'"
        )


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
    blueprint_json["arguments"] = {"a": {}}

    make_blueprint(tmp_path, "basic", blueprint_json)

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
    for name, cfg in plans.items():
        specs = blueprint_json.copy()
        specs["arguments"] = cfg["arguments"]
        specs["parent"] = cfg.get("parent")
        make_blueprint(tmp_path, name, specs)

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
    blueprint_json["options"] = {"a": {}}
    make_blueprint(tmp_path, "basic", blueprint_json)

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
    for name, cfg in plans.items():
        specs = blueprint_json.copy()
        specs["options"] = cfg["options"]
        specs["parent"] = cfg.get("parent")
        make_blueprint(tmp_path, name, specs)

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


def test_plan_jinja():
    plan = Plan("basic")

    searchpaths = [
        str(plan.root / "after"),
        str(plan.root / "optional"),
        str(plan.root / "skeleton"),
        str(plan.root / "templates"),
    ]

    engine = plan.jinja

    assert isinstance(engine, Jinja)
    assert engine.fs and engine.fs.searchpath == searchpaths


def test_plan_():
    ...

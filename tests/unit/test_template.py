import pytest

from blueprint.config import Config
from blueprint.template import Template
from tests.unit import set_templates_root

bp = breakpoint


@pytest.fixture
def blueprint_json():
    """Return the contents of a barebones blueprint.json file."""
    return """
        {
            "name": "template",
            "title": "Project Template",
            "description": "A project template.",
            "version": "0.1.0",
            "type": "language-toolstack"
        }
    """


def test_template():
    template = Template()

    assert template


def test_template_templates(tmp_path):
    """
    GIVEN: A TEMPLATES_ROOT directory
    AND: subdirectories that contain `blueprint.json` files
    WHEN: Template.templates is accessed
    THEN: it should return a list of Template objects for each of those
          subdirectories
    """
    templates_root = tmp_path

    abc = tmp_path / "abc"
    xyz = tmp_path / "xyz"

    for d in [abc, xyz]:
        d.mkdir(parents=True)
        (d / "blueprint.json").write_text("{}")

    with set_templates_root(templates_root):
        templates = Template.templates

    assert templates == [Template("abc"), Template("xyz")]


def test_template_root(root):
    template = Template("basic")
    template_root = root / "templates" / "basic"

    assert template.root == template_root


def test_template_skeleton(root):
    template = Template("basic")

    assert template.skeleton == root / "templates" / "basic" / "skeleton"


def test_template_specs(root):
    """
    GIVEN: a blueprint.json file
    WHEN: specs is accessed
    THEN: it should return the data parsed from the json file
    """
    template = Template("basic")

    assert isinstance(template.specs, dict)
    assert template.specs.get("name") == "Basic"


def test_template_parent():
    """
    GIVEN: A Template with a parent defined in the spec
    WHEN: .parent is accessed
    THEN: it should return the Template for that variable
    """


def test_template_has_requirements():
    ...


def test_template_ok_true(tmp_path, blueprint_json):
    templatedir = tmp_path / "project"
    templatedir.mkdir()

    bp_json = templatedir / "blueprint.json"
    bp_json.write_text(blueprint_json)

    with set_templates_root(tmp_path):
        template = Template("project")

        assert template.ok


def test_template_ok_false_missing_file(tmp_path):
    templatedir = tmp_path / "project"
    templatedir.mkdir()

    with set_templates_root(tmp_path):
        template = Template("project")

        assert not template.ok


def test_template_ok_false_invalid_file(tmp_path, blueprint_json):
    templatedir = tmp_path / "project"
    templatedir.mkdir()

    bp_json = templatedir / "blueprint.json"
    bp_json.write_text("""
        {
            "name": "template",
            "title": "Project Template",
            "version": "0.1.0",
            "type": "language-toolstack"
        }
    """)

    with set_templates_root(tmp_path):
        template = Template("project")

        assert not template.ok


def test_template_config():
    ...


def test_template_setup(fixtures_path):
    """
    GIVEN: A Template object
    WHEN: `.setup =` is called
    THEN: Each step should be run through ._process_exe()
    """
    with set_templates_root(fixtures_path):
        template = Template()
        template.id = "toolstack"
        template.setup = [
            {
                "script": "do-thing",
                "arguments": ["--a", "--b", "--c"],
            }
        ]

        cmd = {
            "cmd": [str(template.root / "scripts" / "do-thing"), "--a", "--b", "--c"],
        }

        assert template.setup == [cmd]


def test_template_after(fixtures_path):
    """
    GIVEN: A Template object
    WHEN: `.after =` is called
    THEN: Each step should be run through ._process_exe()
    """
    with set_templates_root(fixtures_path):
        template = Template()
        template.id = "toolstack"
        template.after = [
            {
                "script": "do-thing",
                "arguments": ["--a", "--b", "--c"],
            }
        ]

        cmd = {
            "cmd": [str(template.root / "scripts" / "do-thing"), "--a", "--b", "--c"],
        }

        assert template.after == [cmd]


def test_template_variables(fixtures_path):
    """
    GIVEN: A Template object
    WHEN: `.variables =` is called
    THEN: Each step should be run through ._process_exe()
    """
    with set_templates_root(fixtures_path):
        template = Template()
        template.id = "toolstack"
        template.variables = {
            "VARIABLE": {
                "script": "do-thing",
                "arguments": ["--a", "--b", "--c"],
            }
        }

        cmd = {
            "cmd": [str(template.root / "scripts" / "do-thing"), "--a", "--b", "--c"],
        }

        assert template.variables == {"VARIABLE": cmd}


def test_template_process_exe(fixtures_path):
    """
    GIVEN: A Template object
    AND: A spec that includes variables, steps, or after keys defined with
        a script and optionally arguments
    WHEN: Those keys are accessed
    THEN: They should be converted into a single command
    """
    with set_templates_root(fixtures_path):
        template = Template()
        template.id = "toolstack"
        result = template._process_exe({
            "script": "do-thing",
            "arguments": ["--a", "--b", "--c"],
        })

        cmd = {
            "cmd": [str(template.root / "scripts" / "do-thing"), "--a", "--b", "--c"],
        }

        assert result == cmd


def test_template_x():
    ...


def test_template_spec_attrs(fixtures_path):
    """
    GIVEN: A Template object
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
        "options",
        "setup",
        "after",
    ]

    with set_templates_root(fixtures_path):
        template = Template("toolstack")

        for key in keys:
            assert hasattr(template, key), f"The {key} attr should be set."

        assert template.name == "python-poetry"
        assert template.title == "Python: Poetry"
        assert template.description == "Python project managed by poetry."
        assert template.version == "0.1.0"
        assert template.type == "language-toolstack"
        assert template.parent == "basic"


def test_template_config():
    template = Template("basic")

    assert isinstance(template.config, Config)
    assert template.config.path == Config.BASE / "basic.yml"

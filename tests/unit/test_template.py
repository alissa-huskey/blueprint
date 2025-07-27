import pytest

#  from blueprint import AccessError
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
        (d / "blueprint.json").touch()

    with set_templates_root(templates_root):
        templates = Template.templates

    assert templates == [Template("abc"), Template("xyz")]


def test_template_root(root):
    project = Template("basic")
    template_root = root / "templates" / "basic"

    assert project.root == template_root


def test_template_skeleton(root):
    project = Template("basic")

    assert project.skeleton == root / "templates" / "basic" / "skeleton"


def test_template_specs(root):
    """
    GIVEN: a blueprint.json file
    WHEN: project.specs is accessed
    THEN: it should return the data parsed from the json file
    """
    project = Template("basic")

    assert isinstance(project.specs, dict)
    assert project.specs.get("name") == "Basic"


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
        project = Template("project")

        assert project.ok


def test_template_ok_false_missing_file(tmp_path):
    templatedir = tmp_path / "project"
    templatedir.mkdir()

    with set_templates_root(tmp_path):
        project = Template("project")

        assert not project.ok


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
        project = Template("project")

        assert not project.ok


def test_template_config():
    ...


def test_template_variables():
    ...


def test_template_x():
    ...

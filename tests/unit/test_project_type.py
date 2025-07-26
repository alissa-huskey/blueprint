import pytest

#  from blueprint import AccessError
from blueprint.project_type import ProjectType
from tests.unit import set_types_root

bp = breakpoint


@pytest.fixture
def blueprint_json():
    """Return the contents of a barebones blueprint.json file."""
    return """
        {
        "name": "project-type",
        "title": "Project Type",
        "description": "A type of project.",
        "version": "0.1.0",
        "type": "language-toolstack"
        }
    """


def test_project_type_type():
    project_type = ProjectType()

    assert project_type


def test_project_type_types(tmp_path):
    """
    GIVEN: A TYPES_ROOT directory
    AND: subdirectories that contain `blueprint.json` files
    WHEN: ProjectType.types is accessed
    THEN: it should return a list of ProjectType objects for each of those
          subdirectories
    """
    types_root = tmp_path

    abc = tmp_path / "abc"
    xyz = tmp_path / "xyz"

    for d in [abc, xyz]:
        d.mkdir(parents=True)
        (d / "blueprint.json").touch()

    with set_types_root(types_root):
        types = ProjectType.types

    assert types == [ProjectType("abc"), ProjectType("xyz")]


def test_project_type_root(root):
    project = ProjectType("basic")
    type_root = root / "types" / "basic"

    assert project.root == type_root


def test_project_type_skeleton(root):
    project = ProjectType("basic")

    assert project.skeleton == root / "types" / "basic" / "skeleton"


def test_project_type_specs(root):
    """
    GIVEN: a blueprint.json file
    WHEN: project.specs is accessed
    THEN: it should return the data parsed from the json file
    """
    project = ProjectType("basic")

    assert isinstance(project.specs, dict)
    assert project.specs.get("name") == "Basic"


def test_project_type_json_validate():
    ...


def test_project_type_meta_validate():
    ...


def test_project_type_parent():
    ...


def test_project_type_cmd():
    ...


def test_project_type_cmd_args():
    ...


def test_project_type_cmd_out():
    ...


def test_project_type_cmd_extra():
    ...


def test_project_type_cmd_substitutions():
    ...


def test_project_type_script():
    ...


def test_project_type_script_args():
    ...


def test_project_type_script_out():
    ...


def test_project_type_script_substitutions():
    ...


def test_project_type_x():
    ...


def test_project_type_has_requirements():
    ...


def test_project_type_ok_true(tmp_path, blueprint_json):
    typedir = tmp_path / "project"
    typedir.mkdir()

    bp_json = typedir / "blueprint.json"
    bp_json.write_text(blueprint_json)

    with set_types_root(tmp_path):
        project = ProjectType("project")

        assert project.ok


def test_project_type_ok_false_missing_file(tmp_path):
    typedir = tmp_path / "project"
    typedir.mkdir()

    with set_types_root(tmp_path):
        project = ProjectType("project")

        assert not project.ok


def test_project_type_ok_false_invalid_file(tmp_path, blueprint_json):
    typedir = tmp_path / "project"
    typedir.mkdir()

    bp_json = typedir / "blueprint.json"
    bp_json.write_text("""
        {
        "name": "project-type",
        "title": "Project Type",
        "version": "0.1.0",
        "type": "language-toolstack"
        }
    """)

    with set_types_root(tmp_path):
        project = ProjectType("project")

        assert not project.ok


def test_project_type_options():
    ...


def test_project_type_config():
    ...


def test_project_type_variables():
    ...


def test_project_type_setup():
    ...


def test_project_type_x():
    ...

import pytest

from blueprint import AccessError
from blueprint.project import Project
from blueprint.template import Template
from tests.unit import set_templates_root

bp = breakpoint


def test_project():
    project = Project()
    assert project


def test_project_path_invalid():
    with pytest.raises(AccessError):
        project = Project()
        project.dest = "invalid_directory"


def test_project_dest_valid(tmp_path):
    project = Project()
    project.dest = tmp_path
    assert project.dest == tmp_path


def test_project_template():
    project = Project("basic")

    assert project.template == Template("basic")


def test_project_path(tmp_path):
    project = Project(name="some-project")
    project.dest = tmp_path
    assert project.path == tmp_path/"some-project"


def test_project_substitute():
    project = Project(name="my-project")
    text = project.substitute("${SMOOSHED_NAME}")

    assert text == "myproject"


def test_project_create(tmp_path):
    """
    WHEN: project.create is called
    THEN: A new project is created
    """
    project = Project("basic", "myproject", dest=tmp_path)
    project.create()

    assert (tmp_path/"myproject").is_dir()


def test_project_dash_name():
    """
    WHEN: project.dash_name is accessed
    THEN: it should return the dash version of that name
    """
    project = Project(name="my_project")

    assert project.dash_name == "my-project"


def test_project_smooshed_name():
    """
    WHEN: project.snake_name is accessed
    THEN: it should return the snake tail version of that name
    """
    project = Project(name="my-project")

    assert project.smooshed_name == "myproject"


def test_project_snake_name():
    """
    WHEN: project.snake_name is accessed
    THEN: it should return the snake tail version of that name
    """
    project = Project(name="my-project")

    assert project.snake_name == "my_project"


def test_project_pascal_name():
    """
    WHEN: project.pascal_name is accessed
    THEN: it should return the pascal tail version of that name
    """
    project = Project(name="my-project")

    assert project.pascal_name == "MyProject"


def test_project_title_name():
    """
    WHEN: project.pascal_name is accessed
    THEN: it should return the pascal tail version of that name
    """
    project = Project(name="my-project")

    assert project.title_name == "My Project"


def test_project_install(tmp_path):
    """
    GIVEN: a project object where create() has been called
    WHEN: project.install() is called with a valid filename from the sources
          directory
    THEN: The file should exist in the new project
    """
    project = Project("basic", "myproject", dest=tmp_path)
    project.create()
    project.install("README.md")

    assert (project.path / "README.md").is_file()


def test_project_install_is_dir(tmp_path):
    """
    GIVEN: a project object where create() has been called
    WHEN: project.install(DIRNAME, is_dir=True) is called with a valid source directory
    THEN: a matching direcory should be created in the new project
    """
    proj_path = tmp_path / "project"
    proj_path.mkdir()

    templates_root = tmp_path / "templates"
    some_dir = templates_root / "a_template" / "skeleton" / "some_dir"
    some_dir.mkdir(parents=True)

    with set_templates_root(templates_root):
        project = Project("a_template", "myproject", dest=proj_path)
        project.create()
        project.install("some_dir")

    assert some_dir.is_dir()


def test_project_install_path_substitues(tmp_path):
    """
    GIVEN: a Project object where create() has been called
    AND: a file or directory exists with a template variable
    WHEN: project.install() is called with that filename
    THEN: The variable name should be replaced with the right value
    """
    proj_path = tmp_path / "project"
    proj_path.mkdir()

    templates_root = tmp_path / "sources"
    some_dir = templates_root / "a_template" / "skeleton" / "${SNAKE_NAME}"
    some_dir.mkdir(parents=True)

    with set_templates_root(templates_root):
        project = Project("a_template", "my-project", dest=tmp_path)
        project.create()
        project.install("${SNAKE_NAME}")

    assert (project.path / "my_project").is_dir()


def test_project_install_file_subs(tmp_path):
    """
    GIVEN: a Project object where create() has been called
    AND: a file exists in the skeleton directory that contains variables
    WHEN: project.install() is called with that filename
    THEN: The file should exist in the project
    AND: The variables in the file should have been replaced
    """
    project = Project("basic", "my-project", dest=tmp_path)
    project.create()
    project.install("README.md")

    dest_file = project.path / "README.md"
    dest_contents = dest_file.read_text()

    assert "My Project" in dest_contents


def test_project_install_all(tmp_path):
    """
    GIVEN: a Project object where create() has been called
    WHEN: project.install_all() is called
    THEN: The files should exist in the new project
    """
    project = Project("basic", "myproject", dest=tmp_path)
    project.create()
    project.install_all()

    assert (project.path / "README.md").is_file()
    assert (project.path / ".todo").is_dir()


def test_project_setup(tmp_path):
    """
    GIVEN: a project object where create() has been called
    WHEN: project.setup() is called
    THEN: the project should be git init'd
    """
    project = Project("basic", "myproject", dest=tmp_path)
    project.create()
    project.setup()

    assert (project.path / ".git").is_dir()


def test_project_cmd():
    ...


def test_project_cmd_args():
    ...


def test_project_cmd_out():
    ...


def test_project_cmd_extra():
    ...


def test_project_cmd_substitutions():
    ...


def test_project_script():
    ...


def test_project_script_args():
    ...


def test_project_script_out():
    ...


def test_project_script_substitutions():
    ...

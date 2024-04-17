import pytest

from blueprint import AccessError
from blueprint.project import Project


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


def test_project_path(tmp_path):
    project = Project("some-project")
    project.dest = tmp_path
    assert project.path == tmp_path/"some-project"


def test_project_create(tmp_path):
    """
    WHEN: project.create is called
    THEN: A new project is created
    """
    project = Project("myproject", dest=tmp_path)
    project.create()

    assert (tmp_path/"myproject").is_dir()


def test_project_snake_name():
    """
    WHEN: project.snake_name is accessed
    THEN: it should return the snake tail version of that name
    """
    project = Project("my-project")

    assert project.snake_name == "my_project"


def test_project_pascal_name():
    """
    WHEN: project.pascal_name is accessed
    THEN: it should return the pascal tail version of that name
    """
    project = Project("my-project")

    assert project.pascal_name == "MyProject"


def test_project_title_name():
    """
    WHEN: project.pascal_name is accessed
    THEN: it should return the pascal tail version of that name
    """
    project = Project("my-project")

    assert project.title_name == "My Project"


def test_project_install(tmp_path):
    """
    GIVEN: a roject object where create() has been called
    WHEN: project.install() is called with a valid filename from the sources
          directory
    THEN: The file should exist in the new project
    """
    project = Project("myproject", dest=tmp_path)
    project.create()
    project.install("README.md")

    assert (project.path / "README.md").is_file()


@pytest.mark.skip("how to test this with no sources/bare/SNAKE_CASE?")
def test_project_install_path_subs(tmp_path):
    """
    GIVEN: a Project object where create() has been called
    WHEN: project.install() is called with a valid filename from the sources
          directory
    THEN: The file should exist in the new project
    """
    project = Project("my-project", dest=tmp_path)
    project.create()
    project.install("SNAKE_NAME/__init__.py")

    assert (project.path / "my_project" / "__init__.py").is_file()


def test_project_install_file_subs(tmp_path):
    """
    GIVEN: a Project object where create() has been called
    AND: a file exists with a template variable
    WHEN: project.install() is called with that filename
    THEN: The variable name should be replaced with the right value
    """
    project = Project("my-project", dest=tmp_path)
    project.create()
    project.install("README.md")

    dest_file = project.path / "README.md"
    dest_contents = dest_file.read_text()

    assert "My Project" in dest_contents

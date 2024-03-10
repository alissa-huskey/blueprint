import pytest

from new_project.python_project import PythonProject


def test_python_project():
    project = PythonProject()
    assert project


def test_python_project_create(tmp_path):
    """
    WHEN: project.create is called
    THEN: A new project directory is created
    AND: The pyproject.toml file exists
    """
    project = PythonProject("myproject", dest=tmp_path)
    project.create()

    assert project.path.is_dir()
    assert (project.path / "pyproject.toml").is_file()


def test_python_project_toml(tmp_path):
    """
    WHEN: project.create is called
    THEN: A new project directory is created
    AND: The pyproject.toml file exists
    """
    project = PythonProject("myproject", dest=tmp_path)
    project.create()
    project.update_pyproject()

    toml_contents = project.pyproject.read_text()

    assert 'python = ">=3.10"' in toml_contents
    assert 'tool.black' in toml_contents


def test_python_project_install(tmp_path):
    """
    GIVEN: a PythonProject object where create() has been called
    WHEN: project.install() is called with a valid filename from the sources
          directory
    THEN: The file should exist in the new project
    """
    project = PythonProject("myproject", dest=tmp_path)
    project.create()
    project.install(".env")

    assert (project.path / ".env").is_file()


def test_python_project_install_dotfiles(tmp_path):
    """
    GIVEN: a PythonProject object where create() has been called
    WHEN: project.install_dotfiles() is called
    THEN: The dotfiles should exist in the new project
    """
    project = PythonProject("myproject", dest=tmp_path)
    project.create()
    project.install_dotfiles()

    assert (project.path / ".env").is_file()
    assert (project.path / ".flake8").is_file()
    assert (project.path / ".python-version").is_file()

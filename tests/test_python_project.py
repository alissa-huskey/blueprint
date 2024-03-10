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

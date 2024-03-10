from re import search as re_search
from subprocess import run

import pytest

from new_project import python_project
from new_project.object import Object
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
    assert '0.0.1' in toml_contents


def test_python_project_install_all(tmp_path):
    """
    GIVEN: a PythonProject object where create() has been called
    WHEN: project.install_all() is called
    THEN: The files should exist in the new project
    """
    project = PythonProject("myproject", dest=tmp_path)
    project.create()
    project.install_all()

    assert (project.path / ".env").is_file()
    assert (project.path / ".flake8").is_file()


def test_python_project_install_dot_python_version(tmp_path):
    """
    GIVEN: a PythonProject object where create() has been called
    WHEN: project.dot_python_version() is called
    THEN: the files should exist
    AND: it should contain the full python version
    """
    project = PythonProject("myproject", dest=tmp_path)
    project.create()
    project.install_dot_python_version()

    dotfile = project.path / ".python-version"
    contents = dotfile.read_text()

    assert dotfile.is_file()
    assert project.PYTHON_FULL_VERSION in contents


def test_python_project_with_subs(tmp_path):
    """
    GIVEN: a PythonProject object where create() has been called
    AND: SNAKE_NAME directory exists
    WHEN: project.install() is called with that directory
    THEN: the file will be created in the correct place
    """
    project = PythonProject("my-project", dest=tmp_path)
    project.create()
    project.install("${SNAKE_NAME}/__init__.py")

    assert (project.path / "my_project" / "__init__.py").is_file()


def test_python_project_python_where(monkeypatch):
    """
    WHEN: project.python_where is accessed
    THEN: the path to the python executable from asdf is returned
    """
    project = PythonProject()
    cmd_res = Object(stdout="~/.asdf/installs/python/3.10.2")

    with monkeypatch.context() as m:
        m.setattr(python_project, "run", lambda *args, **kwargs: cmd_res)
        assert project.python_where == f"{cmd_res.stdout}/bin/python"


def test_python_project_poetry_use(tmp_path):
    """
    WHEN: project.poetry_use is accessed
    THEN: the virtual env should be created in the correct place

    NOTE: This one uses the real filesystem, so it's slow.'
    """
    project = PythonProject("my-project", dest=tmp_path)
    project.create()
    cmd_res = project.poetry_use()

    verify = run(
        ["poetry", "env", "info"],
        cwd=project.path,
        capture_output=True,
        text=True
    )

    assert cmd_res.returncode == 0
    assert "Creating virtualenv" in cmd_res.stdout
    assert re_search(
        rf'Virtualenv\nPython:\s+{project.PYTHON_FULL_VERSION}',
        verify.stdout
    )

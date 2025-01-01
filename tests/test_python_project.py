from pathlib import Path
from re import search as re_search
from subprocess import run

import pytest
import toml

from blueprint.python_project import PythonProject

bp = breakpoint


@pytest.fixture(scope="session")
def poetry_cachedir():
    """Return the hardcoded default Poetry cache path on macOS."""
    return Path.home() / "Library" / "Caches" / "pypoetry" / "virtualenvs"


@pytest.fixture
def project(tmp_path):
    """Prepare and cleanup logic."""
    def make_project(*args, **kwargs):
        """Create and cleanup a project."""
        project = PythonProject(*args, **kwargs)
        yield project
        if project.env_path.exists():
            project.env_path.unlink()


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


def test_python_pyproject_toml(tmp_path):
    """
    WHEN: project.create is called
    THEN: A new project directory is created
    AND: The pyproject.toml file exists
    """
    project = PythonProject(
        "my_pytest_project",
        dest=tmp_path,
        pyv="3.10.2",
        summary="My pytest project.",
        license="MIT",
    )
    project.create()
    project.setup_poetry_init()
    project.setup_pyproject()

    with open(project.path/"pyproject.toml") as f:
        specs = toml.load(f)
        poetry = specs["tool"]["poetry"]

    assert project.pyproject.is_file()
    assert poetry["name"] == "my-pytest-project"
    assert poetry["description"] == "My pytest project."
    assert poetry["license"] == "MIT"
    assert poetry["dependencies"]["python"] == ">=3.10.2"
    assert specs["tool"]["pytest"]["ini_options"]["testpaths"] == ["tests"]
    assert specs["tool"]["pytest"]["ini_options"]["addopts"] == "-vvx"
    assert specs["tool"]["black"]["line-length"] == "88"


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
    assert (project.path / "setup.cfg").is_file()


def test_python_project_setup_dot_python_version(tmp_path):
    """
    GIVEN: a PythonProject object where create() has been called
    WHEN: project.dot_python_version() is called
    THEN: the files should exist
    AND: it should contain the full python version
    """
    project = PythonProject("myproject", dest=tmp_path, pyv="3.10.2")
    project.create()
    project.setup_dot_python_version()

    dotfile = project.path / ".python-version"
    contents = dotfile.read_text()

    assert dotfile.is_file()
    assert "3.10.2" in contents


def test_python_project_with_subs(tmp_path):
    """
    GIVEN: a PythonProject object where create() has been called
    AND: SNAKE_NAME directory exists
    WHEN: project.install() is called with that directory
    THEN: the file will be created in the correct place
    """
    project = PythonProject("my-pytest-project", dest=tmp_path)
    project.create()
    project.install("${SNAKE_NAME}/__init__.py")

    assert (project.path / "my_pytest_project" / "__init__.py").is_file()


@pytest.mark.skip(
    "Poetry does not return the correct venv "
    "if you're in a poetry shell for another project."
)
def test_python_project_venv_path(tmp_path, poetry_cachedir):
    """
    WHEN: project.venv_path is accessed
    THEN: the path to the virtual env should be returned

    NOTE: This one uses the real filesystem, so it's slow.
    """
    project = PythonProject("my-pytest-project", dest=tmp_path)
    project.create()
    project.setup_poetry_install()
    project.venv_path

    assert project.venv_path.name.startswith("my-pytest-project-")
    assert str(project.venv_path).startswith(str(poetry_cachedir))


def test_python_project_setup_poetry_use(tmp_path):
    """
    WHEN: project.poetry_use is accessed
    THEN: the virtual env should be created in the correct place

    NOTE: This one uses the real filesystem, so it's slow.'
    """
    project = PythonProject("my-pytest-project", dest=tmp_path)
    project.create()
    cmd_res = project.setup_poetry_use()

    verify = run(
        ["poetry", "env", "info"],
        cwd=project.path,
        capture_output=True,
        text=True
    )

    assert cmd_res.returncode == 0

    # sometimes poetry uses a leftover venv when a new project is created
    # so it may say "Using virtualenv" instead of "Creating virtual env"
    # perhaps all venvs should be cleared out before tests run as part of setup
    # or teardown
    # or perhaps the project.create() should clear out the venv if it exists
    # for now, this is the simplest solution
    assert (
        ("Creating virtualenv" in cmd_res.stdout) or
        ("Using virtualenv" in cmd_res.stdout)
    )

    assert re_search(
        rf'Virtualenv\nPython:\s+{project.DEFAULT_PYV}',
        verify.stdout
    )


def test_python_project_poetry_init(tmp_path):
    """
    GIVEN: a PythonProject object where create() has been called
    WHEN: project.setup_poetry_init() is called
    THEN: the pyproject.toml should be good
    """
    project = PythonProject(
        "my_pytest_project",
        dest=tmp_path,
        pyv="3.10.2",
        summary="My pytest project.",
        license="MIT",
    )
    project.create()
    res = project.setup_poetry_init()

    with open(project.path/"pyproject.toml") as f:
        specs = toml.load(f)
        poetry = specs["tool"]["poetry"]

    assert res.returncode == 0
    assert project.pyproject.is_file()
    assert poetry["name"] == "my-pytest-project"
    assert poetry["description"] == "My pytest project."
    assert poetry["license"] == "MIT"
    assert poetry["dependencies"]["python"] == ">=3.10.2"

from re import search as re_search
from subprocess import run

from blueprint.python_project import PythonProject


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
    project.setup_pyproject()

    toml_contents = project.pyproject.read_text()

    assert '0.0.1' in toml_contents
    assert 'tool.pytest.ini_options' in toml_contents


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
    project = PythonProject("my-project", dest=tmp_path)
    project.create()
    project.install("${SNAKE_NAME}/__init__.py")

    assert (project.path / "my_project" / "__init__.py").is_file()


def test_python_project_setup_poetry_use(tmp_path):
    """
    WHEN: project.poetry_use is accessed
    THEN: the virtual env should be created in the correct place

    NOTE: This one uses the real filesystem, so it's slow.'
    """
    project = PythonProject("my-project", dest=tmp_path)
    project.create()
    cmd_res = project.setup_poetry_use()

    verify = run(
        ["poetry", "env", "info"],
        cwd=project.path,
        capture_output=True,
        text=True
    )

    assert cmd_res.returncode == 0
    assert "Creating virtualenv" in cmd_res.stdout
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
    project = PythonProject("my_project", dest=tmp_path, pyv="3.10.2")
    project.create()
    project.setup_poetry_init()

    toml_contents = project.pyproject.read_text()

    assert 'name = "my-project"' in toml_contents
    assert 'python = ">=3.10.2"' in toml_contents

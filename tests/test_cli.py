import toml
from typer.testing import CliRunner

from blueprint.cli import new

bp = breakpoint
runner = CliRunner()


def test_new_help():
    """bp new --help"""

    result = runner.invoke(new, ["--help"])
    assert result.exit_code == 0
    assert "basic" in result.stdout
    assert "python" in result.stdout


def test_new_basic_help():
    """bp new basic --help"""

    result = runner.invoke(new, ["basic", "--help"])
    assert result.exit_code == 0


def test_new_basic(tmp_path):
    """
    WHEN: `bp new basic 'my project'`
    THEN: a project directory should be created
    AND: a README.md should be created
    AND: the project should be initialized in git
    AND: a .todo directory should be created
    """

    path = tmp_path / "my-project"
    readme = path / "README.md"

    result = runner.invoke(new, [
        "basic",
        "--dest", str(tmp_path),
        "--summary", "My new project.",
        "my project",
    ], input="y")

    assert result.exit_code == 0
    assert path.is_dir()
    assert (path / ".git").is_dir()
    assert (path / ".todo").is_dir()
    assert readme.is_file()

    lines = readme.read_text().splitlines()

    assert lines[0] == "# My Project"
    assert lines[2] == "> My new project."


def test_new_python(tmp_path):
    """
    WHEN: `bp new python 'my-project'`
    THEN: a project directory should be created
    AND: directories should be created:
         - project-name
         - tests
    AND: file should created:
         - .env
         - .python-version
         - README.md
         - pyproject.toml
         - setup.cfg
         - project_name/__init__.py
         - tests/__init__.py
         - tests/test_project_name.py
    AND: default dev dependencies should be installed
    AND: the project should use the python version specified by --pyv
    AND: the pyproject.toml should have the python version specified by
         --pyv-constraint
    AND: the license specified by --license should be used
    """

    path = tmp_path / "my-project"

    dirs = (
        "my_project",
        "tests",
    )

    files = (
        ".env",
        ".python-version",
        "README.md",
        "pyproject.toml",
        "setup.cfg",
        "my_project/__init__.py",
        "tests/__init__.py",
        "tests/test_my_project.py",
    )

    deps = (
        "black",
        "flake8",
        "flake8-black",
        "flake8-docstrings",
        "flake8-isort",
        "ipython",
        "isort",
        "pdbpp",
        "pycodestyle",
        "pylama",
        "pynvim",
        "pylint",
    )

    result = runner.invoke(new, [
        "python",
        "--dest", str(tmp_path),
        "--summary", "My new project.",
        "--pyv", "3.10.2",
        "--pyv-constraint", ">=3.10.2",
        "my project",
    ], input="y")

    assert result.exit_code == 0

    for d in dirs:
        assert (path / d).is_dir(), f"{d}/ should be created"

    for f in files:
        assert (path / f).is_file(), f"{f}/ should be created"

    lines = (path / "README.md").read_text().splitlines()

    assert lines[0] == "# My Project"
    assert lines[2] == "> My new project."

    with open(path/"pyproject.toml") as f:
        data = toml.load(f)
        specs = data["tool"]["poetry"]

    assert specs["name"] == "my-project"
    assert specs["description"] == "My new project."
    assert specs["license"] == "MIT"
    assert specs["dependencies"]["python"] == ">=3.10.2"

    for d in deps:
        assert d in specs["group"]["dev"]["dependencies"]

    assert (path / ".python-version").read_text().strip() == "3.10.2"

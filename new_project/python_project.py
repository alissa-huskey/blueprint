"""Module for a new python project."""

from subprocess import run

from new_project import ROOT
from new_project.project import Project


class PythonProject(Project):
    """A new python project."""

    POETRY_PYTHON_VERSION = "3.9"
    PYTHON_VERSION = "3.10"
    PYTHON_FULL_VERSION = "3.10.2"
    POETRY_PROJECT_VERSION = "0.1.0"
    SOURCES = ROOT / "sources" / "python"

    def create(self):
        """Create the project using poetry."""
        command = ["poetry", "new", f"--name={self.name}", str(self.path)]
        run(command)

    def install_dot_python_version(self):
        """Install the python version to .python-version file."""
        dotfile = self.path / ".python-version"
        dotfile.write_text(f"{self.PYTHON_FULL_VERSION}\n")

    @property
    def python_where(self):
        """Return the location to the correct python executable."""
        command = [
            "asdf",
            "where",
            "python",
            self.PYTHON_FULL_VERSION
        ]
        res = run(command, capture_output=True, text=True)
        pyroot = res.stdout.strip()
        return f"{pyroot}/bin/python"

    def poetry_use(self):
        """Tell poetry which python executable to use."""
        command = ["poetry", "env", "use", self.python_where]
        return run(command, capture_output=True, text=True, cwd=self.path)

    @property
    def pyproject(self):
        """Path to the pyproject.toml file."""
        return self.path / "pyproject.toml"

    def install_all(self):
        """Install all dotfiles from sources into the new project directory."""
        self.install(".env")
        self.install(".flake8")
        self.install("${SNAKE_NAME}/__init__.py")
        self.install("tests/test_${SNAKE_NAME}.py")

    def update_pyproject(self):
        """Change the version and add more options to pyproject.toml."""
        contents = self.pyproject.read_text()
        contents = contents.replace(
            f'python = "^{self.POETRY_PYTHON_VERSION}"',
            f'python = ">={self.PYTHON_VERSION}"'
        )

        contents = contents.replace(
            f'version = "{self.POETRY_PROJECT_VERSION}"',
            f'version = "{self.PROJECT_VERSION}"'
        )

        addons_file = self.SOURCES / "_pyproject.toml"
        addon_contents = addons_file.read_text()

        contents = contents.replace(
            "\n[build-system]\n",
            addon_contents,
        )

        self.pyproject.write_text(contents)

"""Module for a new python project."""

from shutil import copy
from subprocess import run

from new_project import ROOT
from new_project.project import Project


class PythonProject(Project):
    """A new python project."""

    POETRY_PYTHON_VERSION = "^3.9"
    PYTHON_VERSION = ">=3.10"
    SOURCES = ROOT / "sources" / "python"

    def create(self):
        """Create the project using poetry."""
        command = ["poetry", "new", f"--name={self.name}", str(self.path)]
        run(command)

    @property
    def pyproject(self):
        """Path to the pyproject.toml file."""
        return self.path / "pyproject.toml"

    def install(self, file):
        """Copy a file from the source to the dest."""
        copy(self.SOURCES / file, self.path / file)

    def install_dotfiles(self):
        """Install all dotfiles from sources into the new project directory."""
        self.install(".env")
        self.install(".flake8")
        self.install(".python-version")

    def update_pyproject(self):
        """Change the version and add more options to pyproject.toml."""
        contents = self.pyproject.read_text()
        toml = contents.replace(
            f'python = "{self.POETRY_PYTHON_VERSION}"',
            f'python = "{self.PYTHON_VERSION}"'
        )

        addons_file = self.SOURCES / "_pyproject.toml"
        addon_contents = addons_file.read_text()

        toml = toml.replace(
            "\n[build-system]\n",
            addon_contents,
        )

        self.pyproject.write_text(toml)

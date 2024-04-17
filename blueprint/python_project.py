"""Module for a new python project."""

from blueprint import ROOT, AccessError
from blueprint.project import Project


class PythonProject(Project):
    """A new python project."""

    POETRY_PROJECT_VERSION = "0.1.0"
    SOURCES = ROOT / "sources" / "python"
    DEFAULT_PYV = "3.10.2"
    DEFAULT_PYV_CONSTRAINT = ">=3.10.2"

    type: str = "python"

    DEV_DEPENDENCIES = [
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
        "pytest",
    ]

    def __init__(self, name=None, dest=None,
                 pyv=None, pyv_constraint=None, **kwargs):
        """Create object."""
        self.pyv = pyv or self.DEFAULT_PYV
        self.pyv_constraint = pyv_constraint or self.DEFAULT_PYV_CONSTRAINT
        super().__init__(name, dest, **kwargs)

    def create(self):
        """Create the project using poetry."""
        if self.path.exists():
            raise AccessError(f"Directory already exists: {self.path}")
        command = ["poetry", "new", f"--name={self.name}", str(self.path)]
        return self.run(command, cwd=None)

    def setup_dot_python_version(self):
        """Install the python version to .python-version file."""
        if not self.pyv:
            return

        dotfile = self.path / ".python-version"
        dotfile.write_text(f"{self.pyv}\n")

    @property
    def python_where(self):
        """Return the location to the correct python executable."""
        if not self.pyv:
            return
        command = [
            "asdf",
            "where",
            "python",
            self.pyv,
        ]
        res = self.run(command)
        pyroot = res.stdout.strip()
        return f"{pyroot}/bin/python"

    def setup_poetry_use(self):
        """Tell poetry which python executable to use."""
        if not self.python_where:
            return
        command = ["poetry", "env", "use", self.python_where]
        return self.run(command)

    def setup_poetry_install(self):
        """Install project and dependencies in venv."""
        command = ["poetry", "install"]
        return self.run(command)

    def setup_dev_dependencies(self):
        """Install poetry dev dependencies."""
        command = [
            "poetry", "add", "--group", "dev",
            *self.DEV_DEPENDENCIES,
        ]
        return self.run(command)

    @property
    def pyproject(self):
        """Path to the pyproject.toml file."""
        return self.path / "pyproject.toml"

    def install_all(self):
        """Install all dotfiles from sources into the new project directory."""
        self.install(".env")
        self.install("setup.cfg")
        self.install("${SNAKE_NAME}/__init__.py")
        self.install("${SNAKE_NAME}/object.py")
        self.install("${SNAKE_NAME}/attr.py")
        self.install("tests/test_${SNAKE_NAME}.py")
        super().install_all()

    def setup_poetry_init(self):
        """Generate initial pyproject.toml file."""
        command = [
            "poetry",
            "init",
            f"--name={self.name}",
            f"--python={self.pyv_constraint}",
            "--no-interaction",
        ]

        if self.summary:
            command.append(f"--description={self.summary}")

        if self.license:
            command.append(f"--license={self.license}")

        if self.pyproject.is_file():
            self.pyproject.unlink()

        self.run(command)

    def setup(self):
        """Set up Python project."""
        super().setup()
        self.setup_dot_python_version()
        self.setup_poetry_init()
        self.setup_pyproject()
        self.setup_dev_dependencies()
        self.setup_poetry_use()
        self.setup_poetry_install()

    def setup_pyproject(self):
        """Add more config info to pyproject.toml."""
        contents = self.pyproject.read_text()

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

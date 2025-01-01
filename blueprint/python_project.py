"""Module for a new python project."""

from pathlib import Path
from shutil import which

import toml

from blueprint import ROOT, AccessError
from blueprint.project import Project

bp = breakpoint


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

    @classmethod
    @property
    def poetry_exe(cls):
        """Return the path to the poetry executable."""
        return which("poetry")

    def create(self):
        """Create the project using poetry."""
        if self.path.exists():
            raise AccessError(f"Directory already exists: {self.path}")
        command = [
            "poetry",
            "--directory",
            str(self.dest),
            "new",
            f"--name={self.dash_name}",
            str(self.path)
        ]
        return self.run(command, cwd=self.dest)

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

        command = [
            "poetry",
            "--directory",
            str(self.path),
            "env",
            "use",
            self.python_where,
        ]
        return self.run(command)

    def setup_poetry_install(self):
        """Install project and dependencies in venv."""
        command = ["poetry", "--directory", str(self.path), "install"]
        return self.run(command)

    def setup_dev_dependencies(self):
        """Install poetry dev dependencies."""
        command = [
            "poetry",
            "--directory",
            str(self.path),
            "add",
            "--group",
            "dev",
            *self.DEV_DEPENDENCIES,
        ]
        return self.run(command)

    @property
    def pyproject(self):
        """Path to the pyproject.toml file."""
        return self.path / "pyproject.toml"

    @property
    def venv_path(self) -> Path:
        """Return the path to this projects virtual environment."""
        command = [
            "poetry",
            "--directory",
            str(self.path),
            "env",
            "info",
            "--path"
        ]
        res = self.run(command)
        return Path(res.stdout.strip())

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
            "--directory",
            str(self.path),
            "init",
            f"--name={self.dash_name}",
            f"--python={self.pyv_constraint}",
            "--no-interaction",
        ]

        if self.summary:
            command.append(f"--description={self.summary}")

        if self.license:
            command.append(f"--license={self.license}")

        if self.pyproject.is_file():
            self.pyproject.unlink()

        return self.run(command)

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
        with open(self.pyproject) as f:
            specs = toml.load(f)

        # add/modify toml contents
        specs["tool"]["poetry"]["version"] = self.PROJECT_VERSION
        specs["tool"]["pytest"] = {}
        specs["tool"]["black"] = {}
        specs["tool"]["pytest"]["ini_options"] = {
            "testpaths": ["tests"],
            "addopts": "-vvx",
        }
        specs["tool"]["black"]["line-length"] = "88"

        # put the sections in the correct order
        order = [{"tool": {x: specs["tool"][x]}} for x in ("poetry", "pytest", "black")]
        order.append({"build-system": specs["build-system"]})

        # convert sections to toml then join them together
        sections = [toml.dumps(x) for x in order]
        text = "\n".join(sections)

        # save the pyproject.toml file
        self.pyproject.write_text(text)

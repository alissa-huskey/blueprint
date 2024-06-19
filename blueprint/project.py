"""Module for a new project."""

from pathlib import Path
from re import compile as re_compile
from string import Template
from subprocess import run

from git import Repo

from blueprint import ROOT, AccessError, ProgramError
from blueprint.attr import attr
from blueprint.object import Object

bp = breakpoint


class Project(Object):
    """A new project."""

    pascal_replacer = re_compile(r'[-]([a-z])')
    SOURCES = ROOT / "sources" / "bare"
    PROJECT_VERSION = "0.0.1"

    type: str = "basic"

    def __init__(self, name=None, dest=None, summary="", license="", **kwargs):
        """Create a new project object."""
        self.name = name
        self.dest = dest
        self.summary = summary
        self.license = license

        super().__init__(**kwargs)

    def _dest_setter(self, value):
        """Validate and set dest."""
        if not value:
            return

        dest = Path(value)
        if not dest.is_dir():
            raise AccessError(f"Cannot create project in: '{dest}'")

        self._dest = dest
    dest = attr("dest", setter=_dest_setter)

    @property
    def path(self):
        """Path to the project directory."""
        return self.dest / self.dash_name

    def create(self):
        """Create the project."""
        self.path.mkdir(exist_ok=True)

    @property
    def pascal_name(self):
        """Return the pascal version of the project name.

        Example: MyProject
        """
        return self.title_name.replace(" ", "")

    @property
    def dash_name(self):
        """Return the dash version of the project name.

        Example: my-project
        """
        return self.name.lower().translate(str.maketrans("_ ", "--"))

    @property
    def snake_name(self):
        """Return the snake tail version of the project name.

        Example: my_project
        """
        return self.name.lower().translate(str.maketrans("- ", "__"))

    @property
    def title_name(self):
        """Return the title case version of the project name.

        Example: My Project
        """
        return self.name.translate(str.maketrans("-_", "  ")).title()

    def source_path(self, file):
        """Return the path to a source file."""
        for klass in self.__class__.mro():
            if not issubclass(klass, Project):
                break

            path = klass.SOURCES / file
            if path.exists():
                return path

        klass = self.__class__.__name__
        raise ProgramError(f"Could not find source file: {file} in class: {klass}")

    def install(self, file):
        """Copy a file or create an empty directory from the source to the dest."""
        src = self.source_path(file)
        dest_filename = Template(file).safe_substitute(self.substitutions)
        dest = self.path / dest_filename

        if src.is_dir():
            dest.mkdir(parents=True)
            return

        src_text = src.read_text()
        text = Template(src_text).safe_substitute(**self.substitutions)
        dest.write_text(text)

    @property
    def substitutions(self):
        """Return a mapping of the file substitutions for installing files."""
        return {
            "DASH_NAME": self.dash_name,
            "TITLE_NAME": self.title_name,
            "SNAKE_NAME": self.snake_name,
            "PASCAL_NAME": self.pascal_name,
            "VERSION": self.PROJECT_VERSION,
            "SUMMARY": self.summary,
        }

    def install_all(self):
        """Install all dotfiles from sources into the new project directory."""
        self.install("README.md")
        self.install(".todo")

    def run(self, command: list, capture_output=True, text=True, **kwargs):
        """Run a CLI command."""
        cwd = kwargs.pop("cwd", self.path)

        params = dict(
            capture_output=capture_output,
            text=text,
        )

        if cwd:
            params["cwd"] = cwd

        params.update(kwargs)

        # if keyword arg shell=True is passed to run()
        # the command must be a simple string
        if params.get("shell"):
            command = " ".join(command)

        res = run(command, **params)

        if res.returncode:
            cmd = " ".join(command)
            err = ""
            if hasattr(res, "stderr"):
                err = res.stderr
            raise ProgramError(
                f"Failed CLI command [{res.returncode}] {cmd!r}: {err!r}"
            )

        return res

    def make(self):
        """Make the project end-to-end."""
        self.create()
        self.setup()
        self.install_all()

    def setup(self):
        """Take setup steps."""
        Repo.init(self.path)

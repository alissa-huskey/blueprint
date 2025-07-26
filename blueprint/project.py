"""Module for a Project."""

from pathlib import Path
from re import compile as re_compile
from string import Template
from subprocess import run

from blueprint import ROOT, AccessError, ProgramError
from blueprint.attr import attr
from blueprint.object import Object
from blueprint.project_type import ProjectType

bp = breakpoint


class Project(Object):
    """A new project."""

    pascal_replacer = re_compile(r'[-]([a-z])')
    PROJECT_VERSION = "0.0.1"

    def __init__(self,
                 kind=None,
                 name=None,
                 dest=None,
                 summary="",
                 license="",
                 **kwargs):
        """Create a new project object."""
        self.type = kind
        self.name = name
        self.dest = dest
        self.summary = summary
        self.license = license

        super().__init__(**kwargs)

    @attr(method="setter")
    def type(self, value):
        """Set the project type."""
        if not isinstance(value, ProjectType):
            value = ProjectType(value)
        self._type = value

    def _dest_setter(self, value):
        """Define self.dest property.

        Validates and sets dest.
        """
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

    def install(self, path):
        """Copy a file or create an empty directory from the source to the dest."""
        if isinstance(path, str):
            path = self.type.skeleton / path

        dest_filename = Template(path.name).safe_substitute(self.substitutions)
        dest = self.path / dest_filename

        if path.is_dir():
            dest.mkdir(parents=True)
            return

        src_text = path.read_text()
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
        for path in self.type.skeleton.iterdir():
            self.install(path)

    def run(self, command: list, capture_output=True, text=True, **kwargs):
        """Run a CLI command."""
        cwd = kwargs.pop("cwd", self.path)

        if kwargs.get("stdout"):
            capture_output = False

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
        """Execute setup steps."""
        for step in self.type.specs.get("setup", []):
            outfile = step.get("out")
            if outfile:
                path = self.path / outfile
                with open(path, "w") as fp:
                    self.run(step["cmd"], stdout=fp)
            else:
                self.run(step["cmd"])

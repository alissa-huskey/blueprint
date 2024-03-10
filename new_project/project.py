"""Module for a new project."""

from pathlib import Path
from re import compile as re_compile
#  from shutil import copy
from string import Template

from new_project import ROOT, AccessError
from new_project.attr import attr
from new_project.object import Object


class Project(Object):
    """A new project."""

    pascal_replacer = re_compile(r'[-]([a-z])')
    SOURCES = ROOT / "sources" / "bare"
    PROJECT_VERSION = "0.0.1"

    def __init__(self, name=None, dest=None):
        """Create a new project object."""
        self.name = name
        self.dest = dest

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
        return self.dest / self.name

    def create(self):
        """Create the project."""
        self.path.mkdir(exist_ok=True)

    @property
    def pascal_name(self):
        """Return the snake tail version of the project name."""
        name = self.name.capitalize()
        name = self.pascal_replacer.sub(
            lambda m: m.group(1).upper(), name
        )
        return name

    @property
    def snake_name(self):
        """Return the snake tail version of the project name."""
        return self.name.replace("-", "_")

    @property
    def title_name(self):
        """Return the title case version of the project name."""
        return self.name.replace("-", " ").title()

    def install(self, file):
        """Copy a file from the source to the dest."""
        dest_file = Template(file).safe_substitute(self.substitutions)

        src = self.SOURCES / file
        dest = self.path / dest_file

        src_text = src.read_text()


        text = Template(src_text).safe_substitute(**self.substitutions)

        dest.write_text(text)

    @property
    def substitutions(self):
        """Return a mapping of the file substitutions for installing files."""
        return {
            "TITLE_NAME": self.title_name,
            "SNAKE_NAME": self.snake_name,
            "PASCAL_NAME": self.pascal_name,
            "VERSION": self.PROJECT_VERSION,
        }

"""Config files."""

import yaml
from xdg_base_dirs import xdg_config_home

from blueprint.object import Object

bp = breakpoint


class Config(Object):
    """Config files."""

    BASE = xdg_config_home() / "blueprint"

    data = {}

    def __init__(self, template: str = None, read: bool = False, **kwargs):
        """Initialize object."""
        self.template = template

        if read:
            self.read()

    @property
    def path(self):
        """Path to this template's config file."""
        return self.BASE / f"{self.template}.yml"

    def exists(self):
        """Return True if config file exists."""
        return self.path.is_file()

    def read(self) -> bool:
        """Read the config file."""
        if not (self.template and self.path.is_file()):
            return False

        with open(self.path) as fp:
            self.data = yaml.load(fp, yaml.FullLoader)

            for key, value in self.data.items():
                setattr(self, key, value)

            return True

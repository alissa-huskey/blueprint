"""Config files."""

import yaml
from xdg_base_dirs import xdg_config_home

from blueprint.object import Object


class Config(Object):
    """Config files."""

    BASE = xdg_config_home() / "blueprint"

    def __init__(self, template: str = None, read: bool = False, **kwargs):
        """Initialize object."""
        self.template = template

        if read:
            self.read()

    @property
    def path(self):
        """Path to this template's config file."""
        return self.BASE / f"{self.template}.yml"

    def read(self):
        """Read the config file."""
        if not (self.template and self.path.is_file()):
            return

        with open(self.path) as fp:
            self.data = yaml.load(fp, yaml.FullLoader)

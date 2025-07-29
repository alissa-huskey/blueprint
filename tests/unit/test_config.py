from contextlib import contextmanager
from pathlib import Path

import pytest  # noqa

from blueprint.config import Config

bp = breakpoint


@contextmanager
def set_config_base(base):
    """Temporarily modify the BASE directory of a Project class."""
    orig = Config.BASE
    Config.BASE = base
    yield
    Config.BASE = orig


def test_config():
    cfg = Config()
    assert cfg


def test_config_path():
    cfg = Config("python-poetry")
    assert cfg.path == (Path.home() / ".config/blueprint/python-poetry.yml")


def test_config_read(tmp_path):
    with set_config_base(tmp_path):
        cfg = Config("python-poetry")

        cfg.path.write_text("""
dev-dependencies:
  - a
  - b
  - c
        """)

        cfg.read()

        data = {
            "dev-dependencies": ["a", "b", "c"]
        }

        assert cfg.data == data

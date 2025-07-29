from pathlib import Path

import pytest  # noqa

from blueprint.config import Config
from tests.unit import set_config_base

bp = breakpoint


def test_config():
    cfg = Config()
    assert cfg


def test_config_path():
    cfg = Config("python-poetry")
    assert cfg.path == (Path.home() / ".config/blueprint/python-poetry.yml")


def test_config_read(tmp_path, config_yml):
    with set_config_base(tmp_path):
        cfg = Config("python-poetry")

        cfg.path.write_text(config_yml)
        cfg.read()

        data = {
            "dependencies": {"dev": ["pytest", "pynvim", "pylama", "black"]}
        }

        assert cfg.data == data

"""Blueprint global pytest configuration and fixtures."""

from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import Mock

import pytest

from blueprint import shell_command

bp = breakpoint


@pytest.fixture
def root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent.parent


@pytest.fixture
def fixtures_path(root) -> Path:
    """Return the path to the fixtures directory."""
    return root / "tests" / "fixtures"


@pytest.fixture
def subprocess_run_mock(monkeypatch):
    """Mock subprocess.run in Project."""
    subprocess_run = Mock(return_value=CompletedProcess([], 0))

    with monkeypatch.context() as m:
        m.setattr(shell_command, "run", subprocess_run)
        yield subprocess_run


@pytest.fixture
def config_yml() -> str:
    """Return example config.yaml contents."""
    return """
dependencies:
  dev:
    - pytest
    - pynvim
    - pylama
    - black
"""


@pytest.fixture
def blueprint_json():
    """Return the contents of a barebones blueprint.json file."""
    return {
        "name": "plan",
        "title": "Project Plan",
        "description": "A project plan.",
        "version": "0.1.0",
        "type": "generic"
    }

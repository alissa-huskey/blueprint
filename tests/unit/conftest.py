"""Blueprint global pytest configuration and fixtures."""

from pathlib import Path

import pytest


@pytest.fixture
def root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent.parent


@pytest.fixture
def fixtures_path(root) -> Path:
    """Return the path to the fixtures directory."""
    return root / "tests" / "fixtures"

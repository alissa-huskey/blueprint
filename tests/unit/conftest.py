"""Blueprint global pytest configuration and fixtures."""

from pathlib import Path

import pytest


@pytest.fixture
def root():
    """Return the project root directory."""
    return Path(__file__).parent.parent.parent

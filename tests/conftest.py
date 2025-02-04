"""Test configuration and shared fixtures."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import pytest


def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line("markers", "asyncio: mark test as asyncio")


@dataclass
class SampleData:
    """Sample dataclass for testing."""

    id: int
    name: str
    created_at: datetime
    active: bool
    _hidden: str = "hidden"


@pytest.fixture
def sample_data() -> SampleData:
    """Provide a sample dataclass instance."""
    return SampleData(
        id=1,
        name="Test Item",
        created_at=datetime(2024, 1, 1),
        active=True,
    )

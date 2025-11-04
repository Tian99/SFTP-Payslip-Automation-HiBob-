"""
Shared pytest fixtures for Payslip Automation.
Provides reusable TestClient instance for CLI or API-level testing.
"""

import os
import sys
import pytest

# ensure project root is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.cache import Cache


@pytest.fixture(scope="session")
def cache():
    """Returns a clean in-memory Cache instance."""
    c = Cache(None)
    yield c
    c.flush()
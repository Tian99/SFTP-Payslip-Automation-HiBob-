"""
Unit tests for core.cache module.
"""

from core.cache import Cache


def test_cache_set_get_inmem():
    """Ensure in-memory cache stores and retrieves values."""
    c = Cache(None)
    c.set("foo", "bar")
    assert c.get("foo") == "bar"


def test_cache_incr():
    """Ensure incr() increments properly."""
    c = Cache(None)
    c.incr("counter")
    assert c.get("counter") == 1 or c.get("counter") == "1"
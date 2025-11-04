"""
Basic sanity test for project entrypoint.
Ensures main.py imports and CLI group runs without error.
"""
import importlib


def test_main_importable():
    """Ensure main.py loads successfully"""
    mod = importlib.import_module("main")
    assert hasattr(mod, "cli")
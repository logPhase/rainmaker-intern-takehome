"""Graphiti imports cleanly. This passes before you write anything; if it fails, run `uv sync`."""


def test_graphiti_imports():
    import graphiti_core  # noqa: F401
    from graphiti_core.driver.falkordb_driver import FalkorDriver  # noqa: F401

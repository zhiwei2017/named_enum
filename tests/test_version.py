import importlib.metadata


def test_version():
    assert isinstance(importlib.metadata.version("named_enum"), str)

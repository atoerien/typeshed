"""Serialization and deserialization."""

from functools import singledispatch

@singledispatch
def to_json(obj: object) -> object:
    """Convert obj to a JSON serializable form."""
    ...

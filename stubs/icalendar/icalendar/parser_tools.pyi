from typing import Any, Final, TypeAlias, TypeVar, overload

_T = TypeVar("_T")

__all__ = ["DEFAULT_ENCODING", "SEQUENCE_TYPES", "ICAL_TYPE", "data_encode", "from_unicode", "to_unicode"]

SEQUENCE_TYPES: Final[tuple[type[Any], ...]]
DEFAULT_ENCODING: str
ICAL_TYPE: TypeAlias = str | bytes

def from_unicode(value: ICAL_TYPE, encoding: str = "utf-8") -> bytes:
    """
    Converts a value to bytes, even if it already is bytes
    :param value: The value to convert
    :param encoding: The encoding to use in the conversion
    :return: The bytes representation of the value
    """
    ...
def to_unicode(value: ICAL_TYPE, encoding: str = "utf-8-sig") -> str:
    """Converts a value to unicode, even if it is already a unicode string."""
    ...
@overload
def data_encode(data: ICAL_TYPE, encoding: str = "utf-8") -> bytes:
    """
    Encode all datastructures to the given encoding.
    Currently unicode strings, dicts and lists are supported.
    """
    ...
@overload
def data_encode(data: dict[Any, Any], encoding: str = "utf-8") -> dict[Any, Any]:
    """
    Encode all datastructures to the given encoding.
    Currently unicode strings, dicts and lists are supported.
    """
    ...
@overload
def data_encode(data: list[Any] | tuple[Any, ...], encoding: str = "utf-8") -> list[Any]:
    """
    Encode all datastructures to the given encoding.
    Currently unicode strings, dicts and lists are supported.
    """
    ...
@overload
def data_encode(data: _T, encoding: str = "utf-8") -> _T:
    """
    Encode all datastructures to the given encoding.
    Currently unicode strings, dicts and lists are supported.
    """
    ...

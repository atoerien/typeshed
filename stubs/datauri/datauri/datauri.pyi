from collections.abc import Generator
from re import Pattern
from typing import Final

RE_DATA_URI: Final[Pattern[str]]  # undocumented

class DataURIError(ValueError):
    """
    Exception raised when parsing fails.

    This class subclasses the built-in ``ValueError``.
    """
    ...

class ParsedDataURI:
    """
    Container for parsed data URIs.

    Do not instantiate directly; use ``parse()`` instead.
    """
    media_type: str | None
    data: bytes
    uri: str

    def __init__(self, media_type: str | None, data: bytes, uri: str) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

def parse(uri: str) -> ParsedDataURI:
    """
    Parse a 'data:' URI.

    Returns a ParsedDataURI instance.
    """
    ...
def discover(s: str) -> Generator[ParsedDataURI]:
    """
    Discover 'data:' URIs in a string.

    This returns a generator that yields data URIs found in the string.
    """
    ...

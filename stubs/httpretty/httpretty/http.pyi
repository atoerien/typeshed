from _typeshed import SupportsLenAndGetItem
from typing import Final, Literal, TypeAlias
from typing_extensions import TypeVar

_T = TypeVar("_T", str, bytes)
_HTTPMethod: TypeAlias = Literal["GET", "PUT", "POST", "DELETE", "HEAD", "PATCH", "OPTIONS", "CONNECT"]

STATUSES: dict[int, str]

class HttpBaseClass:
    GET: Final = "GET"
    PUT: Final = "PUT"
    POST: Final = "POST"
    DELETE: Final = "DELETE"
    HEAD: Final = "HEAD"
    PATCH: Final = "PATCH"
    OPTIONS: Final = "OPTIONS"
    CONNECT: Final = "CONNECT"
    METHODS: tuple[_HTTPMethod, ...]

def parse_requestline(s: str) -> tuple[str, str, str]:
    """
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html#sec5

    >>> parse_requestline('GET / HTTP/1.0')
    ('GET', '/', '1.0')
    >>> parse_requestline('post /testurl htTP/1.1')
    ('POST', '/testurl', '1.1')
    >>> parse_requestline('Im not a RequestLine')
    Traceback (most recent call last):
        ...
    ValueError: Not a Request-Line
    """
    ...
def last_requestline(sent_data: SupportsLenAndGetItem[_T]) -> _T | None:
    """Find the last line in sent_data that can be parsed with parse_requestline"""
    ...

from _typeshed import Incomplete
from collections.abc import Callable
from re import Match
from typing import Any, Literal

class JSONDecoder:
    """
    Simple JSON <http://json.org> decoder

    Performs the following translations in decoding by default:

    +---------------+-------------------+
    | JSON          | Python            |
    +===============+===================+
    | object        | dict              |
    +---------------+-------------------+
    | array         | list              |
    +---------------+-------------------+
    | string        | str, unicode      |
    +---------------+-------------------+
    | number (int)  | int, long         |
    +---------------+-------------------+
    | number (real) | float             |
    +---------------+-------------------+
    | true          | True              |
    +---------------+-------------------+
    | false         | False             |
    +---------------+-------------------+
    | null          | None              |
    +---------------+-------------------+

    When allow_nan=True, it also understands
    ``NaN``, ``Infinity``, and ``-Infinity`` as
    their corresponding ``float`` values, which is outside the JSON spec.
    """
    encoding: str
    object_hook: Callable[[dict[Any, Any]], Any] | None
    # transforms a list of (key, json_value) pairs to an arbitrary value
    object_pairs_hook: Callable[[list[tuple[str, Any]]], Any] | None
    parse_float: Callable[[str], Any] | None
    parse_int: Callable[[str], Any] | None
    parse_constant: Callable[[str], Any] | None
    strict: bool
    array_hook: Callable[[list[Any]], Any] | None  # transforms a JSON value to an arbitrary value
    # They have many parameters, it might be better to use Protocol:
    parse_object: Callable[..., tuple[Incomplete, int]]
    parse_array: Callable[..., tuple[Incomplete, int]]
    parse_string: Callable[..., tuple[Incomplete, int]]
    memo: dict[Any, Any]
    scan_once: Callable[[str, int], tuple[bool, int]]

    def __init__(
        self,
        encoding: str | None = None,
        object_hook: Callable[[dict[Any, Any]], Any] | None = None,
        parse_float: Callable[[str], Any] | None = None,
        parse_int: Callable[[str], Any] | None = None,
        parse_constant: Callable[[str], Any] | None = None,
        strict: bool = True,
        object_pairs_hook: Callable[[list[tuple[Any, Any]]], Any] | None = None,
        allow_nan: bool = False,
        array_hook: Callable[[list[Any]], Any] | None = None,  # transforms a JSON value to an arbitrary value
    ) -> None: ...
    def decode(self, s: str, _w: Callable[[str, int], Match[str]] = ..., _PY3: Literal[True] = True) -> Any: ...
    def raw_decode(
        self, s: str, idx: int = 0, _w: Callable[[str, int], Match[str]] = ..., _PY3: Literal[True] = True
    ) -> tuple[Any, int]:
        """
        Decode a JSON document from ``s`` (a ``str`` or ``unicode``
        beginning with a JSON document) and return a 2-tuple of the Python
        representation and the index in ``s`` where the document ended.
        Optionally, ``idx`` can be used to specify an offset in ``s`` where
        the JSON document begins.

        This can be used to decode a JSON document from a string that may
        have extraneous data at the end.
        """
        ...

__all__ = ["JSONDecoder"]

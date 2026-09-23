import re
from collections.abc import Iterable, Iterator
from typing import Any, ClassVar, TypeAlias, overload
from typing_extensions import Self, deprecated

from .connections import Connection

RE_INSERT_VALUES: re.Pattern[str]
_Args: TypeAlias = list[Any] | tuple[Any, ...] | dict[str, Any]

class Cursor:
    """
    This is the object used to interact with the database.

    Do not create an instance of a Cursor yourself. Call
    connections.Connection.cursor().

    See `Cursor <https://www.python.org/dev/peps/pep-0249/#cursor-objects>`_ in
    the specification.
    """
    max_stmt_length: ClassVar[int]
    connection: Connection[Any]
    description: tuple[str, ...]
    rownumber: int
    rowcount: int
    arraysize: int
    messages: Any
    errorhandler: Any
    lastrowid: int
    warning_count: int
    def __init__(self, connection: Connection[Any]) -> None: ...
    def close(self) -> None:
        """Closing a cursor just exhausts all remaining data."""
        ...
    def setinputsizes(self, *args) -> None:
        """Does nothing, required by DB API."""
        ...
    def setoutputsizes(self, *args) -> None:
        """Does nothing, required by DB API."""
        ...
    def nextset(self) -> bool | None: ...

    @overload
    def mogrify(self, query: str, args: _Args | None = None) -> str: ...
    @overload
    @deprecated("single argument is deprecated and will be removed in the next version.")
    def mogrify(self, query: str, args: object) -> str: ...

    @overload
    def execute(self, query: str, args: _Args | None = None) -> int: ...
    @overload
    @deprecated("single argument is deprecated and will be removed in the next version.")
    def execute(self, query: str, args: object) -> int: ...

    def executemany(self, query: str, args: Iterable[object]) -> int | None: ...
    def callproc(self, procname: str, args: Iterable[Any] = ()) -> Any: ...
    def scroll(self, value: int, mode: str = "relative") -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, *exc_info: object) -> None: ...
    # Methods returning result tuples are below.
    def fetchone(self) -> tuple[Any, ...] | None:
        """Fetch the next row."""
        ...
    def fetchmany(self, size: int | None = None) -> tuple[tuple[Any, ...], ...]:
        """Fetch several rows."""
        ...
    def fetchall(self) -> tuple[tuple[Any, ...], ...]:
        """Fetch all the rows."""
        ...
    def __iter__(self) -> Iterator[tuple[Any, ...]]: ...
    def __next__(self): ...

class DictCursorMixin:
    dict_type: Any  # TODO: add support if someone needs this
    def fetchone(self) -> dict[str, Any] | None: ...
    def fetchmany(self, size: int | None = ...) -> tuple[dict[str, Any], ...]: ...
    def fetchall(self) -> tuple[dict[str, Any], ...]: ...
    def __iter__(self) -> Iterator[dict[str, Any]]: ...

class SSCursor(Cursor):
    """
    Unbuffered Cursor, mainly useful for queries that return a lot of data,
    or for connections to remote servers over a slow network.

    Instead of copying every row of data into a buffer, this will fetch
    rows as needed. The upside of this is the client uses much less memory,
    and rows are returned much faster when traveling over a slow network
    or if the result set is very big.

    There are limitations, though. The MySQL protocol doesn't support
    returning the total number of rows, so the only way to tell how many rows
    there are is to iterate over every row returned. Also, it currently isn't
    possible to scroll backwards, as only the current row is held in memory.
    """
    def __del__(self) -> None: ...
    def read_next(self) -> tuple[Any, ...] | None:
        """Read next row."""
        ...
    def fetchall(self) -> list[tuple[Any, ...]]:
        """
        Fetch all, as per MySQLdb. Pretty useless for large queries, as
        it is buffered. See fetchall_unbuffered(), if you want an unbuffered
        generator version of this method.
        """
        ...
    def fetchall_unbuffered(self) -> Iterator[tuple[Any, ...]]:
        """
        Fetch all, implemented as a generator, which isn't to standard,
        however, it doesn't make sense to return everything in a list, as that
        would use ridiculous memory for large result sets.
        """
        ...
    def scroll(self, value: int, mode: str = "relative") -> None: ...

class DictCursor(DictCursorMixin, Cursor):
    """A cursor which returns results as a dictionary"""
    ...

class SSDictCursor(DictCursorMixin, SSCursor):  # type: ignore[misc]  # pyrefly: ignore [inconsistent-inheritance]
    """An unbuffered cursor, which returns results as a dictionary"""
    def fetchall_unbuffered(self) -> Iterator[dict[str, Any]]:
        """
        Fetch all, implemented as a generator, which isn't to standard,
        however, it doesn't make sense to return everything in a list, as that
        would use ridiculous memory for large result sets.
        """
        ...
    def read_next(self) -> dict[str, Any] | None:
        """Read next row."""
        ...

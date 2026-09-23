"""
This module implements connections for MySQLdb. Presently there is
only one class: Connection. Others are unlikely. However, you might
want to make your own subclasses. In most cases, you will probably
override Connection.default_cursor with a non-standard Cursor class.
"""

from _typeshed import Incomplete
from re import Pattern
from types import TracebackType
from typing import Any, Literal, TypeAlias
from typing_extensions import LiteralString, Self

from . import _mysql, cursors
from ._exceptions import (
    DatabaseError as DatabaseError,
    DataError as DataError,
    Error as Error,
    IntegrityError as IntegrityError,
    InterfaceError as InterfaceError,
    InternalError as InternalError,
    NotSupportedError as NotSupportedError,
    OperationalError as OperationalError,
    ProgrammingError as ProgrammingError,
    Warning as Warning,
)

# Any kind of object that can be passed to Connection.literal().
# The allowed types depend on the defined encoders, but the following
# types are always allowed.
_Literal: TypeAlias = str | bytearray | bytes | tuple[_Literal, ...] | list[_Literal] | Any

re_numeric_part: Pattern[str]

def numeric_part(s):
    """
    Returns the leading numeric part of a string.

    >>> numeric_part("20-alpha")
    20
    >>> numeric_part("foo")
    >>> numeric_part("16b")
    16
    """
    ...

class Connection(_mysql.connection):
    """MySQL Database Connection Object"""
    default_cursor: type[cursors.Cursor]
    executemany_fallback: Literal["loop", "multi"]
    cursorclass: type[cursors.BaseCursor]
    encoders: Incomplete
    encoding: str
    messages: Incomplete
    def __init__(self, *args, executemany_fallback: Literal["loop", "multi"] = ..., **kwargs) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> None: ...
    def autocommit(self, on: bool) -> None: ...
    def cursor(self, cursorclass: type[cursors.BaseCursor] | None = None):
        """
        Create a cursor on which queries may be performed. The
        optional cursorclass parameter is used to create the
        Cursor. By default, self.cursorclass=cursors.Cursor is
        used.
        """
        ...
    def query(self, query) -> None: ...
    def literal(self, o: _Literal) -> bytes:
        """
        If o is a single object, returns an SQL literal as a string.
        If o is a non-string sequence, the items of the sequence are
        converted and returned as a sequence.

        Non-standard. For internal use; do not use this in your
        applications.
        """
        ...
    def begin(self) -> None:
        """
        Explicitly begin a connection.

        This method is not used when autocommit=False (default).
        """
        ...
    def warning_count(self):
        """
        Returns the number of warnings generated during execution
        of the previous SQL statement.

        Non-standard.
        """
        ...
    def set_character_set(self, charset: LiteralString, collation: LiteralString | None = None) -> None:
        """Set the connection character set to charset."""
        ...
    def set_sql_mode(self, sql_mode) -> None:
        """
        Set the connection sql_mode. See MySQL documentation for
        legal values.
        """
        ...
    def show_warnings(self):
        """
        Return detailed information about warnings as a
        sequence of tuples of (Level, Code, Message). This
        is only supported in MySQL-4.1 and up. If your server
        is an earlier version, an empty sequence is returned.
        """
        ...
    Warning: type[BaseException]
    Error: type[BaseException]
    InterfaceError: type[BaseException]
    DatabaseError: type[BaseException]
    DataError: type[BaseException]
    OperationalError: type[BaseException]
    IntegrityError: type[BaseException]
    InternalError: type[BaseException]
    ProgrammingError: type[BaseException]
    NotSupportedError: type[BaseException]

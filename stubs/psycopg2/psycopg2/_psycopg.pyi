"""psycopg2 PostgreSQL driver"""

import datetime as dt
from _typeshed import ConvertibleToInt, Incomplete, SupportsRead, SupportsReadline, SupportsWrite, Unused
from collections.abc import Callable, Iterable, Mapping, Sequence
from types import TracebackType
from typing import Any, Literal, NoReturn, Protocol, TextIO, TypeAlias, TypeVar, overload, type_check_only
from typing_extensions import Self, disjoint_base

from psycopg2.extras import ReplicationCursor as extras_ReplicationCursor
from psycopg2.sql import Composable

_Vars: TypeAlias = Sequence[Any] | Mapping[str, Any] | None

@type_check_only
class _type:
    # The class doesn't exist at runtime but following attributes have type "psycopg2._psycopg.type"
    name: str
    values: tuple[int, ...]
    def __call__(self, value: str | bytes | None, cur: cursor | None, /) -> Any: ...

BINARY: _type
BINARYARRAY: _type
BOOLEAN: _type
BOOLEANARRAY: _type
BYTES: _type
BYTESARRAY: _type
CIDRARRAY: _type
DATE: _type
DATEARRAY: _type
DATETIME: _type
DATETIMEARRAY: _type
DATETIMETZ: _type
DATETIMETZARRAY: _type
DECIMAL: _type
DECIMALARRAY: _type
FLOAT: _type
FLOATARRAY: _type
INETARRAY: _type
INTEGER: _type
INTEGERARRAY: _type
INTERVAL: _type
INTERVALARRAY: _type
LONGINTEGER: _type
LONGINTEGERARRAY: _type
MACADDRARRAY: _type
NUMBER: _type
PYDATE: _type
PYDATEARRAY: _type
PYDATETIME: _type
PYDATETIMEARRAY: _type
PYDATETIMETZ: _type
PYDATETIMETZARRAY: _type
PYINTERVAL: _type
PYINTERVALARRAY: _type
PYTIME: _type
PYTIMEARRAY: _type
ROWID: _type
ROWIDARRAY: _type
STRING: _type
STRINGARRAY: _type
TIME: _type
TIMEARRAY: _type
UNICODE: _type
UNICODEARRAY: _type
UNKNOWN: _type

REPLICATION_LOGICAL: int
REPLICATION_PHYSICAL: int

@type_check_only
class _ISQLQuoteProto(Protocol):
    # Objects conforming this protocol should implement a getquoted() and optionally a prepare() method.
    # The real ISQLQuote class is implemented below with more stuff.
    def getquoted(self) -> bytes: ...
    # def prepare(self, __conn: connection) -> None: ...  # optional

adapters: dict[tuple[type[Any], type[ISQLQuote]], Callable[[Any], _ISQLQuoteProto]]
apilevel: str
binary_types: dict[Any, Any]
encodings: dict[str, str]
paramstyle: str
sqlstate_errors: dict[str, type[Error]]
string_types: dict[int, _type]
threadsafety: int

__libpq_version__: int

_T_co = TypeVar("_T_co", covariant=True)

@type_check_only
class _SupportsReadAndReadline(SupportsRead[_T_co], SupportsReadline[_T_co], Protocol[_T_co]): ...

@disjoint_base
class cursor:
    """A database cursor."""
    arraysize: int
    binary_types: Incomplete | None
    connection: _Connection
    itersize: int
    row_factory: Incomplete | None
    scrollable: bool | None
    string_types: Incomplete | None
    tzinfo_factory: Callable[..., dt.tzinfo]
    withhold: bool
    def __init__(self, conn: _Connection, name: str | bytes | None = None) -> None: ...
    @property
    def closed(self) -> bool:
        """True if cursor is closed, False if cursor is open"""
        ...
    @property
    def lastrowid(self) -> int:
        """The ``oid`` of the last row inserted by the cursor."""
        ...
    @property
    def name(self) -> Incomplete | None: ...
    @property
    def query(self) -> bytes | None:
        """The last query text sent to the backend."""
        ...
    @property
    def description(self) -> tuple[Column, ...] | None:
        """Cursor description as defined in DBAPI-2.0."""
        ...
    @property
    def rowcount(self) -> int:
        """Number of rows read from the backend in the last command."""
        ...
    @property
    def rownumber(self) -> int:
        """The current row position."""
        ...
    @property
    def typecaster(self) -> Incomplete | None: ...
    @property
    def statusmessage(self) -> str | None:
        """The return message of the last command."""
        ...
    @property
    def pgresult_ptr(self) -> int | None:
        """pgresult_ptr -- Get the PGresult structure pointer."""
        ...
    def callproc(self, procname: str | bytes, parameters: _Vars = None, /) -> None:
        """callproc(procname, parameters=None) -- Execute stored procedure."""
        ...
    def cast(self, oid: int, s: str | bytes, /) -> Any:
        """
        cast(oid, s) -> value

        Convert the string s to a Python object according to its oid.

        Look for a typecaster first in the cursor, then in its connection,then in the global register. If no suitable typecaster is found,leave the value as a string.
        """
        ...
    def close(self) -> None:
        """close() -- Close the cursor."""
        ...
    def copy_expert(
        self,
        sql: str | bytes | Composable,
        file: _SupportsReadAndReadline[bytes] | SupportsWrite[bytes] | TextIO,
        size: int = 8192,
    ) -> None:
        """
        copy_expert(sql, file, size=8192) -- Submit a user-composed COPY statement.
        `file` must be an open, readable file for COPY FROM or an open, writable
        file for COPY TO. The optional `size` argument, when specified for a COPY
        FROM statement, will be passed to file's read method to control the read
        buffer size.
        """
        ...
    def copy_from(
        self,
        file: _SupportsReadAndReadline[bytes] | _SupportsReadAndReadline[str],
        table: str,
        sep: str = "\t",
        null: str = "\\N",
        size: int = 8192,
        columns: Iterable[str] | None = None,
    ) -> None:
        r"""copy_from(file, table, sep='\t', null='\\N', size=8192, columns=None) -- Copy table from file."""
        ...
    def copy_to(
        self,
        file: SupportsWrite[bytes] | TextIO,
        table: str,
        sep: str = "\t",
        null: str = "\\N",
        columns: Iterable[str] | None = None,
    ) -> None:
        r"""copy_to(file, table, sep='\t', null='\\N', columns=None) -- Copy table to file."""
        ...
    def execute(self, query: str | bytes | Composable, vars: _Vars = None) -> None:
        """execute(query, vars=None) -- Execute query with bound vars."""
        ...
    def executemany(self, query: str | bytes | Composable, vars_list: Iterable[_Vars]) -> None:
        """executemany(query, vars_list) -- Execute many queries with bound vars."""
        ...
    def fetchall(self) -> list[tuple[Any, ...]]:
        """
        fetchall() -> list of tuple

        Return all the remaining rows of a query result set.

        Rows are returned in the form of a list of tuples (by default) or using
        the sequence factory previously set in the `row_factory` attribute.
        Return `!None` when no more data is available.
        """
        ...
    def fetchmany(self, size: int | None = None) -> list[tuple[Any, ...]]:
        """
        fetchmany(size=self.arraysize) -> list of tuple

        Return the next `size` rows of a query result set in the form of a list
        of tuples (by default) or using the sequence factory previously set in
        the `row_factory` attribute.

        Return an empty list when no more data is available.
        """
        ...
    def fetchone(self) -> tuple[Any, ...] | None:
        """
        fetchone() -> tuple or None

        Return the next row of a query result set in the form of a tuple (by
        default) or using the sequence factory previously set in the
        `row_factory` attribute. Return `!None` when no more data is available.
        """
        ...
    def mogrify(self, query: str | bytes | Composable, vars: _Vars | None = None) -> bytes:
        """mogrify(query, vars=None) -> str -- Return query after vars binding."""
        ...
    def nextset(self) -> NoReturn:
        """
        nextset() -- Skip to next set of data.

        This method is not supported (PostgreSQL does not have multiple data 
        sets) and will raise a NotSupportedError exception.
        """
        ...
    def scroll(self, value: int, mode: Literal["absolute", "relative"] = "relative") -> None:
        """scroll(value, mode='relative') -- Scroll to new position according to mode."""
        ...
    def setinputsizes(self, sizes: Unused) -> None:
        """
        setinputsizes(sizes) -- Set memory areas before execute.

        This method currently does nothing but it is safe to call it.
        """
        ...
    def setoutputsize(self, size: int, column: int = ..., /) -> None:
        """
        setoutputsize(size, column=None) -- Set column buffer size.

        This method currently does nothing but it is safe to call it.
        """
        ...
    def __enter__(self) -> Self:
        """__enter__ -> self"""
        ...
    def __exit__(
        self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        """__exit__ -- close the cursor"""
        ...
    def __iter__(self) -> Self:
        """Implement iter(self)."""
        ...
    def __next__(self) -> tuple[Any, ...]:
        """Implement next(self)."""
        ...

_Cursor: TypeAlias = cursor

@disjoint_base
class AsIs:
    """AsIs(str) -> new AsIs adapter object"""
    def __init__(self, obj: object, /, **kwargs: Unused) -> None: ...
    @property
    def adapted(self) -> Any: ...
    def getquoted(self) -> bytes:
        """getquoted() -> wrapped object value as SQL-quoted string"""
        ...
    def __conform__(self, proto, /) -> Self | None: ...

@disjoint_base
class Binary:
    """Binary(buffer) -> new binary object"""
    def __init__(self, str: object, /, **kwargs: Unused) -> None: ...
    @property
    def adapted(self) -> Any: ...
    @property
    def buffer(self) -> Any: ...
    def getquoted(self) -> bytes:
        """getquoted() -> wrapped object value as SQL-quoted binary string"""
        ...
    def prepare(self, conn: connection, /) -> None:
        """prepare(conn) -> prepare for binary encoding using conn"""
        ...
    def __conform__(self, proto, /) -> Self | None: ...

@disjoint_base
class Boolean:
    """Boolean(str) -> new Boolean adapter object"""
    def __init__(self, obj: object, /, **kwargs: Unused) -> None: ...
    @property
    def adapted(self) -> Any: ...
    def getquoted(self) -> bytes:
        """getquoted() -> wrapped object value as SQL-quoted string"""
        ...
    def __conform__(self, proto, /) -> Self | None: ...

@disjoint_base
class Column:
    """
    Description of a column returned by a query.

    The DBAPI demands this object to be a 7-items sequence. This object
    respects this interface, but adds names for the exposed attributes
    and adds attribute not requested by the DBAPI.
    """
    display_size: Any
    internal_size: Any
    name: Any
    null_ok: Any
    precision: Any
    scale: Any
    table_column: Any
    table_oid: Any
    type_code: Any
    def __init__(self, *args, **kwargs) -> None: ...
    def __eq__(self, other, /):
        """Return self==value."""
        ...
    def __ge__(self, other, /):
        """Return self>=value."""
        ...
    def __getitem__(self, index, /):
        """Return self[key]."""
        ...
    def __getstate__(self): ...
    def __gt__(self, other, /):
        """Return self>value."""
        ...
    def __le__(self, other, /):
        """Return self<=value."""
        ...
    def __len__(self) -> int:
        """Return len(self)."""
        ...
    def __lt__(self, other, /):
        """Return self<value."""
        ...
    def __ne__(self, other, /):
        """Return self!=value."""
        ...
    def __setstate__(self, state, /): ...

@disjoint_base
class ConnectionInfo:
    """
    Details about the native PostgreSQL database connection.

    This class exposes several `informative functions`__ about the status
    of the libpq connection.

    Objects of this class are exposed as the `connection.info` attribute.

    .. __: https://www.postgresql.org/docs/current/static/libpq-status.html
    """
    # Note: the following properties can be None if their corresponding libpq function
    # returns NULL. They're not annotated as such, because this is very unlikely in
    # practice---the psycopg2 docs [1] don't even mention this as a possibility!
    #
    # - db_name
    # - user
    # - password
    # - host
    # - port
    # - options
    #
    # (To prove this, one needs to inspect the psycopg2 source code [2], plus the
    # documentation [3] and source code [4] of the corresponding libpq calls.)
    #
    # [1]: https://www.psycopg.org/docs/extensions.html#psycopg2.extensions.ConnectionInfo
    # [2]: https://github.com/psycopg/psycopg2/blob/1d3a89a0bba621dc1cc9b32db6d241bd2da85ad1/psycopg/conninfo_type.c#L52 and below
    # [3]: https://www.postgresql.org/docs/current/libpq-status.html
    # [4]: https://github.com/postgres/postgres/blob/b39838889e76274b107935fa8e8951baf0e8b31b/src/interfaces/libpq/fe-connect.c#L6754 and below  # noqa: E501
    @property
    def backend_pid(self) -> int:
        """
        The process ID (PID) of the backend process you connected to.

        :type: `!int`

        .. seealso:: libpq docs for `PQbackendPID()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQBACKENDPID
        """
        ...
    @property
    def dbname(self) -> str:
        """
        The database name of the connection.

        .. seealso:: libpq docs for `PQdb()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQDB
        """
        ...
    @property
    def dsn_parameters(self) -> dict[str, str]:
        """
        The effective connection parameters.

        :type: `!dict`

        The results include values which weren't explicitly set by the connection
        string, such as defaults, environment variables, etc.
        The *password* parameter is removed from the results.

        .. seealso:: libpq docs for `PQconninfo()`__ for details.
        .. __: https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PQCONNINFO
        """
        ...
    @property
    def error_message(self) -> str | None:
        """
        The error message most recently generated by an operation on the connection.

        `!None` if there is no current message.

        .. seealso:: libpq docs for `PQerrorMessage()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQERRORMESSAGE
        """
        ...
    @property
    def host(self) -> str:
        """
        The server host name of the connection.

        This can be a host name, an IP address, or a directory path if the
        connection is via Unix socket. (The path case can be distinguished
        because it will always be an absolute path, beginning with ``/``.)

        .. seealso:: libpq docs for `PQhost()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQHOST
        """
        ...
    @property
    def needs_password(self) -> bool:
        """
        The connection authentication method required a password, but none was available.

        :type: `!bool`

        .. seealso:: libpq docs for `PQconnectionNeedsPassword()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQCONNECTIONNEEDSPASSWORD
        """
        ...
    @property
    def options(self) -> str:
        """
        The command-line options passed in the connection request.

        .. seealso:: libpq docs for `PQoptions()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQOPTIONS
        """
        ...
    @property
    def password(self) -> str:
        """
        The password of the connection.

        .. seealso:: libpq docs for `PQpass()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQPASS
        """
        ...
    @property
    def port(self) -> int:
        """
        The port of the connection.

        :type: `!int`

        .. seealso:: libpq docs for `PQport()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQPORT
        """
        ...
    @property
    def protocol_version(self) -> int:
        """
        The frontend/backend protocol being used.

        :type: `!int`

        .. seealso:: libpq docs for `PQprotocolVersion()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQPROTOCOLVERSION
        """
        ...
    @property
    def server_version(self) -> int:
        """
        Returns an integer representing the server version.

        :type: `!int`

        .. seealso:: libpq docs for `PQserverVersion()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQSERVERVERSION
        """
        ...
    @property
    def socket(self) -> int:
        """
        The file descriptor number of the connection socket to the server.

        :type: `!int`

        .. seealso:: libpq docs for `PQsocket()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQSOCKET
        """
        ...
    @property
    def ssl_attribute_names(self) -> list[str]:
        """
        The list of the SSL attribute names available.

        :type: `!list` of `!str`

        Only available if psycopg was built with libpq >= 9.5; raise
        `~psycopg2.NotSupportedError` otherwise.

        .. seealso:: libpq docs for `PQsslAttributeNames()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQSSLATTRIBUTENAMES
        """
        ...
    @property
    def ssl_in_use(self) -> bool:
        """
        `!True` if the connection uses SSL, `!False` if not.

        Only available if psycopg was built with libpq >= 9.5; raise
        `~psycopg2.NotSupportedError` otherwise.

        :type: `!bool`

        .. seealso:: libpq docs for `PQsslInUse()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQSSLINUSE
        """
        ...
    @property
    def status(self) -> int:
        """
        The status of the connection.

        :type: `!int`

        .. seealso:: libpq docs for `PQstatus()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQSTATUS
        """
        ...
    @property
    def transaction_status(self) -> int:
        """
        The current in-transaction status of the connection.

        Symbolic constants for the values are defined in the module
        `psycopg2.extensions`: see :ref:`transaction-status-constants` for the
        available values.

        :type: `!int`

        .. seealso:: libpq docs for `PQtransactionStatus()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQTRANSACTIONSTATUS
        """
        ...
    @property
    def used_password(self) -> bool:
        """
        The connection authentication method used a password.

        :type: `!bool`

        .. seealso:: libpq docs for `PQconnectionUsedPassword()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQCONNECTIONUSEDPASSWORD
        """
        ...
    @property
    def user(self) -> str:
        """
        The user name of the connection.

        .. seealso:: libpq docs for `PQuser()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQUSER
        """
        ...
    def __init__(self, *args, **kwargs) -> None: ...
    def parameter_status(self, name: str) -> str | None:
        """
        Looks up a current parameter setting of the server.

        :param name: The name of the parameter to return.
        :type name: `!str`
        :return: The parameter value, `!None` if the parameter is unknown.
        :rtype: `!str`

        .. seealso:: libpq docs for `PQparameterStatus()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQPARAMETERSTATUS
        """
        ...
    def ssl_attribute(self, name: str) -> str | None:
        """
        Returns SSL-related information about the connection.

        :param name: The name of the attribute to return.
        :type name: `!str`
        :return: The attribute value, `!None` if unknown.
        :rtype: `!str`

        Only available if psycopg was built with libpq >= 9.5; raise
        `~psycopg2.NotSupportedError` otherwise.

        Valid names are available in `ssl_attribute_names`.

        .. seealso:: libpq docs for `PQsslAttribute()`__ for details.
        .. __: https://www.postgresql.org/docs/current/static/libpq-status.html#LIBPQ-PQSSLATTRIBUTE
        """
        ...

@disjoint_base
class Error(Exception):
    """Base class for error exceptions."""
    cursor: _Cursor | None
    diag: Diagnostics
    pgcode: str | None
    pgerror: str | None
    def __init__(self, *args, **kwargs) -> None: ...
    def __reduce__(self): ...
    def __setstate__(self, state, /): ...

class DatabaseError(Error):
    """Error related to the database engine."""
    ...
class DataError(DatabaseError):
    """Error related to problems with the processed data."""
    ...
class IntegrityError(DatabaseError):
    """Error related to database integrity."""
    ...
class InternalError(DatabaseError):
    """The database encountered an internal error."""
    ...
class NotSupportedError(DatabaseError):
    """A method or database API was used which is not supported by the database."""
    ...
class OperationalError(DatabaseError):
    """Error related to database operation (disconnect, memory allocation etc)."""
    ...
class ProgrammingError(DatabaseError):
    """Error related to database programming (SQL error, table not found etc)."""
    ...
class QueryCanceledError(OperationalError):
    """Error related to SQL query cancellation."""
    ...
class TransactionRollbackError(OperationalError):
    """Error causing transaction rollback (deadlocks, serialization failures, etc)."""
    ...
class InterfaceError(Error):
    """Error related to the database interface."""
    ...
class Warning(Exception):
    """A database warning."""
    ...

@disjoint_base
class ISQLQuote:
    """
    Abstract ISQLQuote protocol

    An object conform to this protocol should expose a ``getquoted()`` method
    returning the SQL representation of the object.
    """
    _wrapped: Any
    def __init__(self, wrapped: object, /, **kwargs) -> None: ...
    def getbinary(self):
        """getbinary() -- return SQL-quoted binary representation of this object"""
        ...
    def getbuffer(self):
        """getbuffer() -- return this object"""
        ...
    def getquoted(self) -> bytes:
        """getquoted() -- return SQL-quoted representation of this object"""
        ...

@disjoint_base
class Decimal:
    """Decimal(str) -> new Decimal adapter object"""
    def __init__(self, value: object, /, **kwargs: Unused) -> None: ...
    @property
    def adapted(self) -> Any: ...
    def getquoted(self) -> bytes:
        """getquoted() -> wrapped object value as SQL-quoted string"""
        ...
    def __conform__(self, proto, /) -> Self | None: ...

@disjoint_base
class Diagnostics:
    """
    Details from a database error report.

    The object is returned by the `~psycopg2.Error.diag` attribute of the
    `!Error` object.
    All the information available from the |PQresultErrorField|_ function
    are exposed as attributes by the object, e.g. the `!severity` attribute
    returns the `!PG_DIAG_SEVERITY` code. Please refer to the `PostgreSQL documentation`__ for the meaning of all the attributes.

    .. |PQresultErrorField| replace:: `!PQresultErrorField()`
    .. _PQresultErrorField: https://www.postgresql.org/docs/current/static/libpq-exec.html#LIBPQ-PQRESULTERRORFIELD
    .. __: PQresultErrorField_
    """
    column_name: str | None
    constraint_name: str | None
    context: str | None
    datatype_name: str | None
    internal_position: str | None
    internal_query: str | None
    message_detail: str | None
    message_hint: str | None
    message_primary: str | None
    schema_name: str | None
    severity: str | None
    severity_nonlocalized: str | None
    source_file: str | None
    source_function: str | None
    source_line: str | None
    sqlstate: str | None
    statement_position: str | None
    table_name: str | None
    def __init__(self, err: Error, /) -> None: ...

@disjoint_base
class Float:
    """Float(str) -> new Float adapter object"""
    def __init__(self, value: float, /, **kwargs: Unused) -> None: ...
    @property
    def adapted(self) -> float: ...
    def getquoted(self) -> bytes:
        """getquoted() -> wrapped object value as SQL-quoted string"""
        ...
    def __conform__(self, proto, /) -> Self | None: ...

@disjoint_base
class Int:
    """Int(str) -> new Int adapter object"""
    def __init__(self, value: ConvertibleToInt, /, **kwargs: Unused) -> None: ...
    @property
    def adapted(self) -> Any: ...
    def getquoted(self) -> bytes:
        """getquoted() -> wrapped object value as SQL-quoted string"""
        ...
    def __conform__(self, proto, /) -> Self | None: ...

@disjoint_base
class List:
    """List(list) -> new list wrapper object"""
    def __init__(self, objs: list[object], /, **kwargs: Unused) -> None: ...
    @property
    def adapted(self) -> list[Any]: ...
    def getquoted(self) -> bytes:
        """getquoted() -> wrapped object value as SQL date/time"""
        ...
    def prepare(self, conn: connection, /) -> None:
        """prepare(conn) -> set encoding to conn->encoding"""
        ...
    def __conform__(self, proto, /) -> Self | None: ...

@disjoint_base
class Notify:
    """
    A notification received from the backend.

    `!Notify` instances are made available upon reception on the
    `~connection.notifies` member of the listening connection. The object
    can be also accessed as a 2 items tuple returning the members
    :samp:`({pid},{channel})` for backward compatibility.

    See :ref:`async-notify` for details.
    """
    channel: Any
    payload: Any
    pid: Any
    def __init__(self, *args, **kwargs) -> None: ...
    def __eq__(self, other, /):
        """Return self==value."""
        ...
    def __ge__(self, other, /):
        """Return self>=value."""
        ...
    def __getitem__(self, index, /):
        """Return self[key]."""
        ...
    def __gt__(self, other, /):
        """Return self>value."""
        ...
    def __hash__(self) -> int:
        """Return hash(self)."""
        ...
    def __le__(self, other, /):
        """Return self<=value."""
        ...
    def __len__(self) -> int:
        """Return len(self)."""
        ...
    def __lt__(self, other, /):
        """Return self<value."""
        ...
    def __ne__(self, other, /):
        """Return self!=value."""
        ...

@disjoint_base
class QuotedString:
    """QuotedString(str) -> new quoted object"""
    encoding: str
    def __init__(self, str: object, /, **kwargs: Unused) -> None: ...
    @property
    def adapted(self) -> Any: ...
    @property
    def buffer(self) -> Any: ...
    def getquoted(self) -> bytes:
        """getquoted() -> wrapped object value as SQL-quoted string"""
        ...
    def prepare(self, conn: connection, /) -> None:
        """prepare(conn) -> set encoding to conn->encoding and store conn"""
        ...
    def __conform__(self, proto, /) -> Self | None: ...

@disjoint_base
class ReplicationCursor(cursor):
    """A database replication cursor."""
    feedback_timestamp: Any
    io_timestamp: Any
    wal_end: Any
    def __init__(self, *args, **kwargs) -> None: ...
    def consume_stream(self, consumer, keepalive_interval=...):
        """consume_stream(consumer, keepalive_interval=None) -- Consume replication stream."""
        ...
    def read_message(self) -> Incomplete | None:
        """read_message() -- Try reading a replication message from the server (non-blocking)."""
        ...
    def send_feedback(self, write_lsn=..., flush_lsn=..., apply_lsn=..., reply=..., force=...):
        """send_feedback(write_lsn=0, flush_lsn=0, apply_lsn=0, reply=False, force=False) -- Update a replication feedback, optionally request a reply or force sending a feedback message regardless of the timeout."""
        ...
    def start_replication_expert(self, command, decode=..., status_interval=...):
        """start_replication_expert(command, decode=False, status_interval=10) -- Start replication with a given command."""
        ...

@disjoint_base
class ReplicationMessage:
    """A replication protocol message."""
    cursor: Any
    data_size: Any
    data_start: Any
    payload: Any
    send_time: Any
    wal_end: Any
    def __init__(self, *args, **kwargs) -> None: ...

@disjoint_base
class Xid:
    """
    A transaction identifier used for two-phase commit.

    Usually returned by the connection methods `~connection.xid()` and
    `~connection.tpc_recover()`.
    `!Xid` instances can be unpacked as a 3-item tuples containing the items
    :samp:`({format_id},{gtrid},{bqual})`.
    The `!str()` of the object returns the *transaction ID* used
    in the commands sent to the server.

    See :ref:`tpc` for an introduction.
    """
    bqual: Any
    database: Any
    format_id: Any
    gtrid: Any
    owner: Any
    prepared: Any
    def __init__(self, *args, **kwargs) -> None: ...
    def from_string(self, *args, **kwargs):
        """
        Create a `!Xid` object from a string representation. Static method.

        If *s* is a PostgreSQL transaction ID produced by a XA transaction,
        the returned object will have `format_id`, `gtrid`, `bqual` set to
        the values of the preparing XA id.
        Otherwise only the `!gtrid` is populated with the unparsed string.
        The operation is the inverse of the one performed by `!str(xid)`.
        """
        ...
    def __getitem__(self, index, /):
        """Return self[key]."""
        ...
    def __len__(self) -> int:
        """Return len(self)."""
        ...

_T_cur = TypeVar("_T_cur", bound=cursor)
_Lobject: TypeAlias = lobject

@disjoint_base
class connection:
    """
    connection(dsn, ...) -> new connection object

    :Groups:
      * `DBAPI-2.0 errors`: Error, Warning, InterfaceError,
        DatabaseError, InternalError, OperationalError,
        ProgrammingError, IntegrityError, DataError, NotSupportedError
    """
    DataError: type[DataError]
    DatabaseError: type[DatabaseError]
    Error: type[Error]
    IntegrityError: type[IntegrityError]
    InterfaceError: type[InterfaceError]
    InternalError: type[InternalError]
    NotSupportedError: type[NotSupportedError]
    OperationalError: type[OperationalError]
    ProgrammingError: type[ProgrammingError]
    Warning: type[Warning]
    @property
    def async_(self) -> int:
        """True if the connection is asynchronous."""
        ...
    autocommit: bool
    @property
    def binary_types(self) -> dict[Incomplete, Incomplete]:
        """A set of typecasters to convert binary values."""
        ...
    @property
    def closed(self) -> int: ...
    cursor_factory: Callable[[connection, str | bytes | None], _Cursor]
    @property
    def dsn(self) -> str:
        """The current connection string."""
        ...
    @property
    def encoding(self) -> str:
        """The current client encoding."""
        ...
    @property
    def info(self) -> ConnectionInfo:
        """info -- Get connection info."""
        ...

    @property
    def isolation_level(self) -> int | None:
        """Set or return the connection transaction isolation level."""
        ...
    @isolation_level.setter
    def isolation_level(self, value: str | bytes | int | None, /) -> None:
        """Set or return the connection transaction isolation level."""
        ...

    notices: list[str]
    notifies: list[Notify]
    @property
    def pgconn_ptr(self) -> int | None:
        """pgconn_ptr -- Get the PGconn structure pointer."""
        ...
    @property
    def protocol_version(self) -> int:
        """Protocol version used for this connection. Currently always 3."""
        ...

    @property
    def deferrable(self) -> bool | None:
        """Set or return the connection deferrable status."""
        ...
    @deferrable.setter
    def deferrable(self, value: Literal["default"] | bool | None, /) -> None:
        """Set or return the connection deferrable status."""
        ...

    @property
    def readonly(self) -> bool | None:
        """Set or return the connection read-only status."""
        ...
    @readonly.setter
    def readonly(self, value: Literal["default"] | bool | None, /) -> None:
        """Set or return the connection read-only status."""
        ...

    @property
    def server_version(self) -> int:
        """Server version."""
        ...
    @property
    def status(self) -> int:
        """The current transaction status."""
        ...
    @property
    def string_types(self) -> dict[Incomplete, Incomplete]:
        """A set of typecasters to convert textual values."""
        ...
    # Really it's dsn: str, async: int = 0, async_: int = 0, but
    # that would be a syntax error.
    def __init__(self, dsn: str, *, async_: int = 0) -> None: ...
    def cancel(self) -> None:
        """cancel() -- cancel the current operation"""
        ...
    def close(self) -> None:
        """close() -- Close the connection."""
        ...
    def commit(self) -> None:
        """commit() -- Commit all changes to database."""
        ...

    @overload
    def cursor(
        self, name: str | bytes | None = None, cursor_factory: None = None, withhold: bool = False, scrollable: bool | None = None
    ) -> _Cursor: ...
    @overload
    def cursor(
        self,
        name: str | bytes | None = None,
        *,
        cursor_factory: Callable[[connection, str | bytes | None], _T_cur],
        withhold: bool = False,
        scrollable: bool | None = None,
    ) -> _T_cur:
        """
        cursor(name=None, cursor_factory=extensions.cursor, withhold=False) -- new cursor

        Return a new cursor.

        The ``cursor_factory`` argument can be used to
        create non-standard cursors by passing a class different from the
        default. Note that the new class *should* be a sub-class of
        `extensions.cursor`.

        :rtype: `extensions.cursor`
        """
        ...
    @overload
    def cursor(
        self,
        name: str | bytes | None,
        cursor_factory: Callable[[connection, str | bytes | None], _T_cur],
        withhold: bool = False,
        scrollable: bool | None = None,
    ) -> _T_cur:
        """
        cursor(name=None, cursor_factory=extensions.cursor, withhold=False) -- new cursor

        Return a new cursor.

        The ``cursor_factory`` argument can be used to
        create non-standard cursors by passing a class different from the
        default. Note that the new class *should* be a sub-class of
        `extensions.cursor`.

        :rtype: `extensions.cursor`
        """
        ...

    def fileno(self) -> int:
        """fileno() -> int -- Return file descriptor associated to database connection."""
        ...
    def get_backend_pid(self) -> int:
        """get_backend_pid() -- Get backend process id."""
        ...
    def get_dsn_parameters(self) -> dict[str, str]:
        """get_dsn_parameters() -- Get effective connection parameters."""
        ...
    def get_native_connection(self):
        """get_native_connection() -- Return the internal PGconn* as a Python Capsule."""
        ...
    def get_parameter_status(self, parameter: str) -> str | None:
        """
        get_parameter_status(parameter) -- Get backend parameter status.

        Potential values for ``parameter``:
          server_version, server_encoding, client_encoding, is_superuser,
          session_authorization, DateStyle, TimeZone, integer_datetimes,
          and standard_conforming_strings
        If server did not report requested parameter, None is returned.

        See libpq docs for PQparameterStatus() for further details.
        """
        ...
    def get_transaction_status(self) -> int:
        """get_transaction_status() -- Get backend transaction status."""
        ...
    def isexecuting(self) -> bool:
        """isexecuting() -> bool -- Return True if the connection is executing an asynchronous operation."""
        ...
    def lobject(
        self,
        oid: int = ...,
        mode: str | None = ...,
        new_oid: int = ...,
        new_file: str | None = ...,
        lobject_factory: type[_Lobject] = ...,
    ) -> _Lobject: ...
    def poll(self) -> int: ...
    def reset(self) -> None: ...
    def rollback(self) -> None: ...
    def set_client_encoding(self, encoding: str) -> None: ...
    def set_isolation_level(self, level: int | None) -> None: ...
    def set_session(
        self,
        isolation_level: str | bytes | int | None = ...,
        readonly: bool | Literal["default", b"default"] | None = ...,
        deferrable: bool | Literal["default", b"default"] | None = ...,
        autocommit: bool = ...,
    ) -> None:
        """
        set_session(...) -- Set one or more parameters for the next transactions.

        Accepted arguments are 'isolation_level', 'readonly', 'deferrable', 'autocommit'.
        """
        ...
    def tpc_begin(self, xid: str | bytes | Xid) -> None:
        """tpc_begin(xid) -- begin a TPC transaction with given transaction ID xid."""
        ...
    def tpc_commit(self, xid: str | bytes | Xid = ..., /) -> None:
        """tpc_commit([xid]) -- commit a transaction previously prepared."""
        ...
    def tpc_prepare(self) -> None:
        """tpc_prepare() -- perform the first phase of a two-phase transaction."""
        ...
    def tpc_recover(self) -> list[Xid]:
        """tpc_recover() -- returns a list of pending transaction IDs."""
        ...
    def tpc_rollback(self, xid: str | bytes | Xid = ..., /) -> None:
        """tpc_rollback([xid]) -- abort a transaction previously prepared."""
        ...
    def xid(self, format_id, gtrid, bqual) -> Xid:
        """xid(format_id, gtrid, bqual) -- create a transaction identifier."""
        ...
    def __enter__(self) -> Self:
        """__enter__ -> self"""
        ...
    def __exit__(self, type: type[BaseException] | None, name: BaseException | None, tb: TracebackType | None, /) -> None:
        """__exit__ -- commit if no exception, else roll back"""
        ...

_Connection: TypeAlias = connection

@disjoint_base
class ReplicationConnection(connection):
    """A replication connection."""
    autocommit: Any
    isolation_level: Any
    replication_type: Any
    reset: Any
    set_isolation_level: Any
    set_session: Any
    def __init__(self, *args, **kwargs) -> None: ...

    # https://github.com/python/typeshed/issues/11282
    # The return type should be exactly extras.ReplicationCursor (not _psycopg.ReplicationCursor)
    # See the C code: replicationConnection_init(), psyco_conn_cursor()
    @overload
    def cursor(
        self, name: str | bytes | None = None, cursor_factory: None = None, withhold: bool = False, scrollable: bool | None = None
    ) -> extras_ReplicationCursor:
        """
        cursor(name=None, cursor_factory=extensions.cursor, withhold=False) -- new cursor

        Return a new cursor.

        The ``cursor_factory`` argument can be used to
        create non-standard cursors by passing a class different from the
        default. Note that the new class *should* be a sub-class of
        `extensions.cursor`.

        :rtype: `extensions.cursor`
        """
        ...
    @overload
    def cursor(
        self,
        name: str | bytes | None = None,
        *,
        cursor_factory: Callable[[connection, str | bytes | None], _T_cur],
        withhold: bool = False,
        scrollable: bool | None = None,
    ) -> _T_cur:
        """
        cursor(name=None, cursor_factory=extensions.cursor, withhold=False) -- new cursor

        Return a new cursor.

        The ``cursor_factory`` argument can be used to
        create non-standard cursors by passing a class different from the
        default. Note that the new class *should* be a sub-class of
        `extensions.cursor`.

        :rtype: `extensions.cursor`
        """
        ...
    @overload
    def cursor(
        self,
        name: str | bytes | None,
        cursor_factory: Callable[[connection, str | bytes | None], _T_cur],
        withhold: bool = False,
        scrollable: bool | None = None,
    ) -> _T_cur:
        """
        cursor(name=None, cursor_factory=extensions.cursor, withhold=False) -- new cursor

        Return a new cursor.

        The ``cursor_factory`` argument can be used to
        create non-standard cursors by passing a class different from the
        default. Note that the new class *should* be a sub-class of
        `extensions.cursor`.

        :rtype: `extensions.cursor`
        """
        ...

@disjoint_base
class lobject:
    """A database large object."""
    closed: Any
    mode: Any
    oid: Any
    def __init__(self, *args, **kwargs) -> None: ...
    def close(self):
        """close() -- Close the lobject."""
        ...
    def export(self, filename):
        """export(filename) -- Export large object to given file."""
        ...
    def read(self, size=...):
        """read(size=-1) -- Read at most size bytes or to the end of the large object."""
        ...
    def seek(self, offset, whence=...):
        """seek(offset, whence=0) -- Set the lobject's current position."""
        ...
    def tell(self):
        """tell() -- Return the lobject's current position."""
        ...
    def truncate(self, len=...):
        """truncate(len=0) -- Truncate large object to given size."""
        ...
    def unlink(self):
        """unlink() -- Close and then remove the lobject."""
        ...
    def write(self, str):
        """write(str | bytes) -- Write a string or bytes to the large object."""
        ...

@type_check_only
class _datetime:
    # The class doesn't exist at runtime but functions below return "psycopg2._psycopg.datetime" objects
    # XXX: This and other classes that implement the `ISQLQuote` protocol could be made generic
    # in the return type of their `adapted` property if someone asks for it.
    def __init__(self, obj: object, type: int = -1, /, **kwargs: Unused) -> None: ...
    @property
    def adapted(self) -> Any: ...
    @property
    def type(self) -> int: ...
    def getquoted(self) -> bytes: ...
    def __conform__(self, proto, /) -> Self | None: ...

def Date(year: int, month: int, day: int, /) -> _datetime:
    """
    Date(year, month, day) -> new date

    Build an object holding a date value.
    """
    ...
def DateFromPy(date: dt.date, /) -> _datetime:
    """DateFromPy(datetime.date) -> new wrapper"""
    ...
def DateFromTicks(ticks: float, /) -> _datetime:
    """
    DateFromTicks(ticks) -> new date

    Build an object holding a date value from the given ticks value.

    Ticks are the number of seconds since the epoch; see the documentation of the standard Python time module for details).
    """
    ...
def IntervalFromPy(interval: dt.timedelta, /) -> _datetime:
    """IntervalFromPy(datetime.timedelta) -> new wrapper"""
    ...
def Time(hour: int, minutes: int, seconds: float, tzinfo: dt.tzinfo | None = None, /) -> _datetime:
    """
    Time(hour, minutes, seconds, tzinfo=None) -> new time

    Build an object holding a time value.
    """
    ...
def TimeFromPy(time: dt.time, /) -> _datetime:
    """TimeFromPy(datetime.time) -> new wrapper"""
    ...
def TimeFromTicks(ticks: float, /) -> _datetime:
    """
    TimeFromTicks(ticks) -> new time

    Build an object holding a time value from the given ticks value.

    Ticks are the number of seconds since the epoch; see the documentation of the standard Python time module for details).
    """
    ...
def Timestamp(
    year: int, month: int, day: int, hour: int = 0, minutes: int = 0, seconds: float = 0, tzinfo: dt.tzinfo | None = None, /
) -> _datetime:
    """
    Timestamp(year, month, day, hour, minutes, seconds, tzinfo=None) -> new timestamp

    Build an object holding a timestamp value.
    """
    ...
def TimestampFromPy(datetime: dt.datetime, /) -> _datetime:
    """TimestampFromPy(datetime.datetime) -> new wrapper"""
    ...
def TimestampFromTicks(ticks: float, /) -> _datetime:
    """
    TimestampFromTicks(ticks) -> new timestamp

    Build an object holding a timestamp value from the given ticks value.

    Ticks are the number of seconds since the epoch; see the documentation of the standard Python time module for details).
    """
    ...
def _connect(*args, **kwargs):
    """_connect(dsn, [connection_factory], [async]) -- New database connection."""
    ...
def adapt(obj: object, protocol=..., alternate=..., /) -> Any:
    """adapt(obj, protocol, alternate) -> object -- adapt obj to given protocol"""
    ...
def encrypt_password(
    password: str | bytes, user: str | bytes, scope: connection | cursor | None = None, algorithm: str | None = None
) -> str:
    """encrypt_password(password, user, [scope], [algorithm]) -- Prepares the encrypted form of a PostgreSQL password."""
    ...
def get_wait_callback() -> Incomplete | None:
    """
    Return the currently registered wait callback.

    Return `!None` if no callback is currently registered.
    """
    ...
def libpq_version() -> int:
    """Query actual libpq version loaded."""
    ...
def new_array_type(values: tuple[int, ...], name: str, baseobj: _type) -> _type:
    """
    new_array_type(oids, name, baseobj) -> new type object

    Create a new binding object to parse an array.

    The object can be used with `register_type()`.

    :Parameters:
      * `oids`: Tuple of ``oid`` of the PostgreSQL types to convert.
      * `name`: Name for the new type
      * `baseobj`: Adapter to perform type conversion of a single array item.
    """
    ...
def new_type(
    values: tuple[int, ...], name: str, castobj: Callable[[str | bytes | None, cursor], Any] | None = None, baseobj=None
) -> _type:
    """
    new_type(oids, name, castobj) -> new type object

    Create a new binding object. The object can be used with the
    `register_type()` function to bind PostgreSQL objects to python objects.

    :Parameters:
      * `oids`: Tuple of ``oid`` of the PostgreSQL types to convert.
      * `name`: Name for the new type
      * `adapter`: Callable to perform type conversion.
        It must have the signature ``fun(value, cur)`` where ``value`` is
        the string representation returned by PostgreSQL (`!None` if ``NULL``)
        and ``cur`` is the cursor from which data are read.
    """
    ...
def parse_dsn(dsn: str | bytes) -> dict[str, Any]:
    """parse_dsn(dsn) -> dict -- parse a connection string into parameters"""
    ...
def quote_ident(ident: str | bytes, scope) -> str:
    """
    quote_ident(str, conn_or_curs) -> str -- wrapper around PQescapeIdentifier

    :Parameters:
      * `str`: A bytes or unicode object
      * `conn_or_curs`: A connection or cursor, required
    """
    ...
def register_type(obj: _type, conn_or_curs: connection | cursor | None = None, /) -> None:
    """
    register_type(obj, conn_or_curs) -> None -- register obj with psycopg type system

    :Parameters:
      * `obj`: A type adapter created by `new_type()`
      * `conn_or_curs`: A connection, cursor or None
    """
    ...
def set_wait_callback(none: Callable[..., Incomplete] | None, /) -> None:
    """
    Register a callback function to block waiting for data.

    The callback should have signature :samp:`fun({conn})` and
    is called to wait for data available whenever a blocking function from the
    libpq is called.  Use `!set_wait_callback(None)` to revert to the
    original behaviour (i.e. using blocking libpq functions).

    The function is an hook to allow coroutine-based libraries (such as
    Eventlet_ or gevent_) to switch when Psycopg is blocked, allowing
    other coroutines to run concurrently.

    See `~psycopg2.extras.wait_select()` for an example of a wait callback
    implementation.

    .. _Eventlet: https://eventlet.net/
    .. _gevent: http://www.gevent.org/
    """
    ...

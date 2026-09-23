"""
an adaptation of the MySQL C API (mostly)

You probably are better off using MySQLdb instead of using this
module directly.

In general, renaming goes from mysql_* to _mysql.*. _mysql.connect()
returns a connection object (MYSQL). Functions which expect MYSQL * as
an argument are now methods of the connection object. A number of things
return result objects (MYSQL_RES). Functions which expect MYSQL_RES * as
an argument are now methods of the result object. Deprecated functions
(as of 3.23) are NOT implemented.
"""

import builtins
from _typeshed import Incomplete
from typing import overload
from typing_extensions import deprecated, disjoint_base

import MySQLdb._exceptions

version_info: tuple[Incomplete, ...]

class DataError(MySQLdb._exceptions.DatabaseError):
    """
    Exception raised for errors that are due to problems with the
    processed data like division by zero, numeric value out of range,
    etc.
    """
    ...
class DatabaseError(MySQLdb._exceptions.Error):
    """
    Exception raised for errors that are related to the
    database.
    """
    ...
class Error(MySQLdb._exceptions.MySQLError):
    """
    Exception that is the base class of all other error exceptions
    (not Warning).
    """
    ...
class IntegrityError(MySQLdb._exceptions.DatabaseError):
    """
    Exception raised when the relational integrity of the database
    is affected, e.g. a foreign key check fails, duplicate key,
    etc.
    """
    ...
class InterfaceError(MySQLdb._exceptions.Error):
    """
    Exception raised for errors that are related to the database
    interface rather than the database itself.
    """
    ...
class InternalError(MySQLdb._exceptions.DatabaseError):
    """
    Exception raised when the database encounters an internal
    error, e.g. the cursor is not valid anymore, the transaction is
    out of sync, etc.
    """
    ...
class MySQLError(Exception):
    """Exception related to operation with MySQL."""
    ...
class NotSupportedError(MySQLdb._exceptions.DatabaseError):
    """
    Exception raised in case a method or database API was used
    which is not supported by the database, e.g. requesting a
    .rollback() on a connection that does not support transaction or
    has transactions turned off.
    """
    ...
class OperationalError(MySQLdb._exceptions.DatabaseError):
    """
    Exception raised for errors that are related to the database's
    operation and not necessarily under the control of the programmer,
    e.g. an unexpected disconnect occurs, the data source name is not
    found, a transaction could not be processed, a memory allocation
    error occurred during processing, etc.
    """
    ...
class ProgrammingError(MySQLdb._exceptions.DatabaseError):
    """
    Exception raised for programming errors, e.g. table not found
    or already exists, syntax error in the SQL statement, wrong number
    of parameters specified, etc.
    """
    ...
class Warning(builtins.Warning, MySQLdb._exceptions.MySQLError):
    """
    Exception raised for important warnings like data truncations
    while inserting, etc.
    """
    ...

@disjoint_base
class connection:
    """
    Returns a MYSQL connection object. Exclusive use of
    keyword parameters strongly recommended. Consult the
    MySQL C API documentation for more details.

    host
      string, host to connect

    user
      string, user to connect as

    password
      string, password to use

    database
      string, database to use

    port
      integer, TCP/IP port to connect to

    unix_socket
      string, location of unix_socket (UNIX-ish only)

    conv
      mapping, maps MySQL FIELD_TYPE.* to Python functions which
      convert a string to the appropriate Python type

    connect_timeout
      number of seconds to wait before the connection
      attempt fails.

    compress
      if set, gzip compression is enabled

    named_pipe
      if set, connect to server via named pipe (Windows only)

    init_command
      command which is run once the connection is created

    read_default_file
      see the MySQL documentation for mysql_options()

    read_default_group
      see the MySQL documentation for mysql_options()

    client_flag
      client flags from MySQLdb.constants.CLIENT

    load_infile
      int, non-zero enables LOAD LOCAL INFILE, zero disables
    """
    client_flag: Incomplete
    converter: Incomplete
    open: Incomplete
    port: Incomplete
    server_capabilities: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def _get_native_connection(self): ...
    def affected_rows(self): ...
    def autocommit(self, on): ...
    def change_user(self, *args, **kwargs): ...
    def character_set_name(self): ...
    def close(self): ...
    def commit(self): ...
    def dump_debug_info(self): ...
    def errno(self): ...
    def error(self): ...
    def escape(self, obj, dict): ...
    def escape_string(self, s): ...
    def field_count(self): ...
    def fileno(self): ...
    def get_autocommit(self): ...
    def get_character_set_info(self): ...
    def get_host_info(self): ...
    def get_proto_info(self): ...
    def get_server_info(self): ...
    def info(self): ...
    def insert_id(self): ...
    def kill(self, *args, **kwargs): ...
    def more_results(self) -> bool: ...
    def next_result(self): ...

    @overload
    @deprecated("The reconnect parameter of ping() is deprecated.")
    def ping(self, reconnect: bool) -> None: ...
    @overload
    def ping(self) -> None: ...

    def query(self, query): ...
    def read_query_result(self): ...
    def rollback(self): ...
    def select_db(self, *args, **kwargs): ...
    def send_query(self, *args, **kwargs): ...
    def set_character_set(self, charset: str) -> None: ...
    def set_server_option(self, option): ...
    def shutdown(self): ...
    def sqlstate(self): ...
    def stat(self): ...
    def store_result(self): ...
    def string_literal(self, obj, /) -> str: ...
    def thread_id(self): ...
    def use_result(self): ...
    def discard_result(self) -> None: ...
    def warning_count(self): ...
    def __delattr__(self, name: str, /) -> None: ...
    def __setattr__(self, name: str, value, /) -> None: ...

@disjoint_base
class result:
    """
    result(connection, use=0, converter={}) -- Result set from a query.

    Creating instances of this class directly is an excellent way to
    shoot yourself in the foot. If using _mysql.connection directly,
    use connection.store_result() or connection.use_result() instead.
    If using MySQLdb.Connection, this is done by the cursor class.
    Just forget you ever saw this. Forget... FOR-GET...
    """
    converter: Incomplete
    has_next: Incomplete
    def __init__(self, *args, **kwargs) -> None: ...
    def data_seek(self, n):
        """data_seek(n) -- seek to row n of result set"""
        ...
    def describe(self):
        """
        Returns the sequence of 7-tuples required by the DB-API for
        the Cursor.description attribute.
        """
        ...
    def fetch_row(self, *args, **kwargs):
        """
        fetch_row([maxrows, how]) -- Fetches up to maxrows as a tuple.
        The rows are formatted according to how:

            0 -- tuples (default)
            1 -- dictionaries, key=column or table.column if duplicated
            2 -- dictionaries, key=table.column
        """
        ...
    def discard(self) -> None:
        """discard() -- Discard remaining rows in the resultset."""
        ...
    def field_flags(self):
        """Returns a tuple of field flags, one for each column in the result."""
        ...
    def num_fields(self):
        """Returns the number of fields (column) in the result."""
        ...
    def num_rows(self):
        """
        Returns the number of rows in the result set. Note that if
        use=1, this will not return a valid value until the entire result
        set has been read.
        """
        ...
    def __delattr__(self, name: str, /) -> None:
        """Implement delattr(self, name)."""
        ...
    def __setattr__(self, name: str, value, /) -> None:
        """Implement setattr(self, name, value)."""
        ...

def connect(*args, **kwargs):
    """
    Returns a MYSQL connection object. Exclusive use of
    keyword parameters strongly recommended. Consult the
    MySQL C API documentation for more details.

    host
      string, host to connect

    user
      string, user to connect as

    password
      string, password to use

    database
      string, database to use

    port
      integer, TCP/IP port to connect to

    unix_socket
      string, location of unix_socket (UNIX-ish only)

    conv
      mapping, maps MySQL FIELD_TYPE.* to Python functions which
      convert a string to the appropriate Python type

    connect_timeout
      number of seconds to wait before the connection
      attempt fails.

    compress
      if set, gzip compression is enabled

    named_pipe
      if set, connect to server via named pipe (Windows only)

    init_command
      command which is run once the connection is created

    read_default_file
      see the MySQL documentation for mysql_options()

    read_default_group
      see the MySQL documentation for mysql_options()

    client_flag
      client flags from MySQLdb.constants.CLIENT

    load_infile
      int, non-zero enables LOAD LOCAL INFILE, zero disables
    """
    ...
def debug(*args, **kwargs):
    """
    Does a DBUG_PUSH with the given string.
    mysql_debug() uses the Fred Fish debug library.
    To use this function, you must compile the client library to
    support debugging.
    """
    ...
def escape(obj, dict):
    """
    escape(obj, dict) -- escape any special characters in object obj
    using mapping dict to provide quoting functions for each type.
    Returns a SQL literal string.
    """
    ...
def escape_string(s):
    """
    escape_string(s) -- quote any SQL-interpreted characters in string s.

    Use connection.escape_string(s), if you use it at all.
    _mysql.escape_string(s) cannot handle character sets. You are
    probably better off using connection.escape(o) instead, since
    it will escape entire sequences as well as strings.
    """
    ...
def get_client_info():
    """
    get_client_info() -- Returns a string that represents
    the client library version.
    """
    ...
def string_literal(obj, /) -> str:
    """
    string_literal(obj) -- converts object obj into a SQL string literal.
    This means, any special SQL characters are escaped, and it is enclosed
    within single quotes. In other words, it performs:

    "'%s'" % escape_string(str(obj))

    Use connection.string_literal(obj), if you use it at all.
    _mysql.string_literal(obj) cannot handle character sets.
    """
    ...

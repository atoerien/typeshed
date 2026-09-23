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
    def _get_native_connection(self):
        """
        Return the internal MYSQL* wrapped in a PyCapsule object.
        NOTE: this is a private API introduced ONLY for XTA integration,
              don't use it for different use cases.
              This method is supported only for XTA integration and support must
              be asked to LIXA project: http://www.tiian.org/lixa/
              Please DO NOT ask support to PyMySQL/mysqlclient-python project.
        """
        ...
    def affected_rows(self):
        """
        Return number of rows affected by the last query.
        Non-standard. Use Cursor.rowcount.
        """
        ...
    def autocommit(self, on):
        """Set the autocommit mode. True values enable; False value disable."""
        ...
    def change_user(self, *args, **kwargs):
        """
        Changes the user and causes the database specified by db to
        become the default (current) database on the connection
        specified by mysql. In subsequent queries, this database is
        the default for table references that do not include an
        explicit database specifier.

        This function was introduced in MySQL Version 3.23.3.

        Fails unless the connected user can be authenticated or if he
        doesn't have permission to use the database. In this case the
        user and database are not changed.

        The db parameter may be set to None if you don't want to have
        a default database.
        """
        ...
    def character_set_name(self):
        """
        Returns the default character set for the current connection.
        Non-standard.
        """
        ...
    def close(self):
        """Close the connection. No further activity possible."""
        ...
    def commit(self):
        """Commits the current transaction"""
        ...
    def dump_debug_info(self):
        """
        Instructs the server to write some debug information to the
        log. The connected user must have the process privilege for
        this to work. Non-standard.
        """
        ...
    def errno(self):
        """
        Returns the error code for the most recently invoked API function
        that can succeed or fail. A return value of zero means that no error
        occurred.
        """
        ...
    def error(self):
        """
        Returns the error message for the most recently invoked API function
        that can succeed or fail. An empty string () is returned if no error
        occurred.
        """
        ...
    def escape(self, obj, dict):
        """
        escape(obj, dict) -- escape any special characters in object obj
        using mapping dict to provide quoting functions for each type.
        Returns a SQL literal string.
        """
        ...
    def escape_string(self, s):
        """
        escape_string(s) -- quote any SQL-interpreted characters in string s.

        Use connection.escape_string(s), if you use it at all.
        _mysql.escape_string(s) cannot handle character sets. You are
        probably better off using connection.escape(o) instead, since
        it will escape entire sequences as well as strings.
        """
        ...
    def field_count(self):
        """
        Returns the number of columns for the most recent query on the
        connection. Non-standard. Will probably give you bogus results
        on most cursor classes. Use Cursor.rowcount.
        """
        ...
    def fileno(self):
        """
        Return file descriptor of the underlying libmysqlclient connection.
        This provides raw access to the underlying network connection.
        """
        ...
    def get_autocommit(self):
        """Get the autocommit mode. True when enable; False when disable."""
        ...
    def get_character_set_info(self):
        """
        Returns a dict with information about the current character set:

        collation
            collation name
        name
            character set name
        comment
            comment or descriptive name
        dir
            character set directory
        mbminlen
            min. length for multibyte string
        mbmaxlen
            max. length for multibyte string

        Not all keys may be present, particularly dir.

        Non-standard.
        """
        ...
    def get_host_info(self):
        """
        Returns a string that represents the MySQL client library
        version. Non-standard.
        """
        ...
    def get_proto_info(self):
        """
        Returns an unsigned integer representing the protocol version
        used by the current connection. Non-standard.
        """
        ...
    def get_server_info(self):
        """
        Returns a string that represents the server version number.
        Non-standard.
        """
        ...
    def info(self):
        """
        Retrieves a string providing information about the most
        recently executed query. Non-standard. Use messages or
        Cursor.messages.
        """
        ...
    def insert_id(self):
        """
        Returns the ID generated for an AUTO_INCREMENT column by the previous
        query. Use this function after you have performed an INSERT query into a
        table that contains an AUTO_INCREMENT field.

        Note that this returns 0 if the previous query does not
        generate an AUTO_INCREMENT value. If you need to save the value for
        later, be sure to call this immediately after the query
        that generates the value.

        The ID is updated after INSERT and UPDATE statements that generate
        an AUTO_INCREMENT value or that set a column value to
        LAST_INSERT_ID(expr). See section 6.3.5.2 Miscellaneous Functions
        in the MySQL documentation.

        Also note that the value of the SQL LAST_INSERT_ID() function always
        contains the most recently generated AUTO_INCREMENT value, and is not
        reset between queries because the value of that function is maintained
        in the server.
        """
        ...
    def kill(self, *args, **kwargs):
        """
        Asks the server to kill the thread specified by pid.
        Non-standard. Deprecated.
        """
        ...
    def more_results(self) -> bool:
        """
        Returns True if one or more results follow the current result of a
        multi-statement query. This check does not advance to the next result.

        Non-standard.
        """
        ...
    def next_result(self):
        """
        If more query results exist, next_result() reads the next query
        results and returns the status back to application.

        After calling next_result() the state of the connection is as if
        you had called query() for the next query. This means that you can
        now call store_result(), warning_count(), affected_rows()
        , and so forth. 

        Returns 0 if there are more results; -1 if there are no more results

        Non-standard.
        """
        ...

    @overload
    @deprecated("The reconnect parameter of ping() is deprecated.")
    def ping(self, reconnect: bool) -> None:
        """
        Checks whether or not the connection to the server is working.

        This function can be used by clients that remain idle for a
        long while, to check whether or not the server has closed the
        connection.

        DEPRECATED: Accepts an optional `reconnect` parameter. If True,
        then the client will attempt reconnection. Note that this setting
        is persistent. By default, this is on in MySQL<5.0.3, and off
        thereafter.
        MySQL 8.0.33 deprecated the MYSQL_OPT_RECONNECT option so reconnect
        parameter is also deprecated in mysqlclient 2.2.1.

        Non-standard. You should assume that ping() performs an
        implicit rollback; use only when starting a new transaction.
        You have been warned.
        """
        ...
    @overload
    def ping(self) -> None:
        """
        Checks whether or not the connection to the server is working.

        This function can be used by clients that remain idle for a
        long while, to check whether or not the server has closed the
        connection.

        DEPRECATED: Accepts an optional `reconnect` parameter. If True,
        then the client will attempt reconnection. Note that this setting
        is persistent. By default, this is on in MySQL<5.0.3, and off
        thereafter.
        MySQL 8.0.33 deprecated the MYSQL_OPT_RECONNECT option so reconnect
        parameter is also deprecated in mysqlclient 2.2.1.

        Non-standard. You should assume that ping() performs an
        implicit rollback; use only when starting a new transaction.
        You have been warned.
        """
        ...

    def query(self, query):
        """
        Execute a query. store_result() or use_result() will get the
        result set, if any. Non-standard. Use cursor() to create a cursor,
        then cursor.execute().
        """
        ...
    def read_query_result(self):
        """Read result of query sent by send_query()."""
        ...
    def rollback(self):
        """Rolls back the current transaction"""
        ...
    def select_db(self, *args, **kwargs):
        """
        Causes the database specified by db to become the default
        (current) database on the connection specified by mysql. In subsequent
        queries, this database is the default for table references that do not
        include an explicit database specifier.

        Fails unless the connected user can be authenticated as having
        permission to use the database.

        Non-standard.
        """
        ...
    def send_query(self, *args, **kwargs):
        """
        Send a query. Same to query() except not wait response.

        Use read_query_result() before calling store_result() or use_result()
        """
        ...
    def set_character_set(self, charset: str) -> None:
        """
        Sets the default character set for the current connection.
        Non-standard.
        """
        ...
    def set_server_option(self, option):
        """
        set_server_option(option) -- Enables or disables an option
        for the connection.

        Non-standard.
        """
        ...
    def shutdown(self):
        """
        Asks the database server to shut down. The connected user must
        have shutdown privileges. Non-standard. Deprecated.
        """
        ...
    def sqlstate(self):
        """
        Returns a string containing the SQLSTATE error code
        for the last error. The error code consists of five characters.
        '00000' means "no error." The values are specified by ANSI SQL
        and ODBC. For a list of possible values, see section 23
        Error Handling in MySQL in the MySQL Manual.

        Note that not all MySQL errors are yet mapped to SQLSTATE's.
        The value 'HY000' (general error) is used for unmapped errors.

        Non-standard.
        """
        ...
    def stat(self):
        """
        Returns a character string containing information similar to
        that provided by the mysqladmin status command. This includes
        uptime in seconds and the number of running threads,
        questions, reloads, and open tables. Non-standard.
        """
        ...
    def store_result(self):
        """
        Returns a result object acquired by mysql_store_result
        (results stored in the client). If no results are available,
        None is returned. Non-standard.
        """
        ...
    def string_literal(self, obj, /) -> str:
        """
        string_literal(obj) -- converts object obj into a SQL string literal.
        This means, any special SQL characters are escaped, and it is enclosed
        within single quotes. In other words, it performs:

        "'%s'" % escape_string(str(obj))

        Use connection.string_literal(obj), if you use it at all.
        _mysql.string_literal(obj) cannot handle character sets.
        """
        ...
    def thread_id(self):
        """
        Returns the thread ID of the current connection. This value
        can be used as an argument to kill() to kill the thread.

        If the connection is lost and you reconnect with ping(), the
        thread ID will change. This means you should not get the
        thread ID and store it for later. You should get it when you
        need it.

        Non-standard.
        """
        ...
    def use_result(self):
        """
        Returns a result object acquired by mysql_use_result
        (results stored in the server). If no results are available,
        None is returned. Non-standard.
        """
        ...
    def discard_result(self) -> None:
        """
        Discard current result set.

        This function can be called instead of use_result() or store_result(). Non-standard.
        """
        ...
    def warning_count(self):
        """
        Returns the number of warnings generated during execution
        of the previous SQL statement.

        Non-standard.
        """
        ...
    def __delattr__(self, name: str, /) -> None:
        """Implement delattr(self, name)."""
        ...
    def __setattr__(self, name: str, value, /) -> None:
        """Implement setattr(self, name, value)."""
        ...

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

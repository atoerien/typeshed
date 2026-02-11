"""
This module implements connections for MySQLdb. Presently there is
only one class: Connection. Others are unlikely. However, you might
want to make your own subclasses. In most cases, you will probably
override Connection.default_cursor with a non-standard Cursor class.
"""

from _typeshed import Incomplete
from re import Pattern
from types import TracebackType
from typing import Any
from typing_extensions import LiteralString, Self, TypeAlias

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
    cursorclass: type[cursors.BaseCursor]
    encoders: Incomplete
    encoding: str
    messages: Incomplete
    def __init__(self, *args, **kwargs) -> None:
        """
        Create a connection to the database. It is strongly recommended
        that you only use keyword parameters. Consult the MySQL C API
        documentation for more information.

        :param str host:        host to connect
        :param str user:        user to connect as
        :param str password:    password to use
        :param str passwd:      alias of password (deprecated)
        :param str database:    database to use
        :param str db:          alias of database (deprecated)
        :param int port:        TCP/IP port to connect to
        :param str unix_socket: location of unix_socket to use
        :param dict conv:       conversion dictionary, see MySQLdb.converters
        :param int connect_timeout:
            number of seconds to wait before the connection attempt fails.

        :param bool compress:   if set, compression is enabled
        :param str named_pipe:  if set, a named pipe is used to connect (Windows only)
        :param str init_command:
            command which is run once the connection is created

        :param str read_default_file:
            file from which default client values are read

        :param str read_default_group:
            configuration group to use from the default file

        :param type cursorclass:
            class object, used to create cursors (keyword only)

        :param bool use_unicode:
            If True, text-like columns are returned as unicode objects
            using the connection's character set. Otherwise, text-like
            columns are returned as bytes. Unicode objects will always
            be encoded to the connection's character set regardless of
            this setting.
            Default to True.

        :param str charset:
            If supplied, the connection character set will be changed
            to this character set.

        :param str collation:
            If ``charset`` and ``collation`` are both supplied, the
            character set and collation for the current connection
            will be set.

            If omitted, empty string, or None, the default collation
            for the ``charset`` is implied.

        :param str auth_plugin:
            If supplied, the connection default authentication plugin will be
            changed to this value. Example values:
            `mysql_native_password` or `caching_sha2_password`

        :param str sql_mode:
            If supplied, the session SQL mode will be changed to this
            setting.
            For more details and legal values, see the MySQL documentation.

        :param int client_flag:
            flags to use or 0 (see MySQL docs or constants/CLIENTS.py)

        :param bool multi_statements:
            If True, enable multi statements for clients >= 4.1.
            Defaults to True.

        :param str ssl_mode:
            specify the security settings for connection to the server;
            see the MySQL documentation for more details
            (mysql_option(), MYSQL_OPT_SSL_MODE).
            Only one of 'DISABLED', 'PREFERRED', 'REQUIRED',
            'VERIFY_CA', 'VERIFY_IDENTITY' can be specified.

        :param dict ssl:
            dictionary or mapping contains SSL connection parameters;
            see the MySQL documentation for more details
            (mysql_ssl_set()).  If this is set, and the client does not
            support SSL, NotSupportedError will be raised.
            Since mysqlclient 2.2.4, ssl=True is alias of ssl_mode=REQUIRED
            for better compatibility with PyMySQL and MariaDB.

        :param str server_public_key_path:
            specify the path to a file RSA public key file for caching_sha2_password.
            See https://dev.mysql.com/doc/refman/9.0/en/caching-sha2-pluggable-authentication.html

        :param bool local_infile:
            sets ``MYSQL_OPT_LOCAL_INFILE`` in ``mysql_options()`` enabling LOAD LOCAL INFILE from any path; zero disables;
    
        :param str local_infile_dir:
            sets ``MYSQL_OPT_LOAD_DATA_LOCAL_DIR`` in ``mysql_options()`` enabling LOAD LOCAL INFILE from any path; 
            if ``local_infile`` is set to ``True`` then this is ignored;
    
            supported for mysql version >= 8.0.21

        :param bool autocommit:
            If False (default), autocommit is disabled.
            If True, autocommit is enabled.
            If None, autocommit isn't set and server default is used.

        :param bool binary_prefix:
            If set, the '_binary' prefix will be used for raw byte query
            arguments (e.g. Binary). This is disabled by default.

        There are a number of undocumented, non-standard methods. See the
        documentation for the MySQL C API for some hints on what they do.
        """
        ...
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

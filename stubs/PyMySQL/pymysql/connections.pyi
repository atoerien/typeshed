from _typeshed import FileDescriptorOrPath, Incomplete, Unused
from collections.abc import Callable, Mapping
from socket import _Address, socket as _socket
from ssl import SSLContext, _PasswordType
from typing import Any, AnyStr, Generic, overload
from typing_extensions import Self, TypeVar, deprecated

from .charset import charset_by_id as charset_by_id, charset_by_name as charset_by_name
from .constants import CLIENT as CLIENT, COMMAND as COMMAND, FIELD_TYPE as FIELD_TYPE, SERVER_STATUS as SERVER_STATUS
from .cursors import Cursor
from .err import (
    DatabaseError,
    DataError,
    Error,
    IntegrityError,
    InterfaceError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
    Warning,
)

_C = TypeVar("_C", bound=Cursor, default=Cursor)
_C2 = TypeVar("_C2", bound=Cursor)

SSL_ENABLED: bool
DEFAULT_USER: str | None
DEBUG: bool
DEFAULT_CHARSET: str
TEXT_TYPES: set[int]
MAX_PACKET_LEN: int

def dump_packet(data): ...
def _lenenc_int(i: int) -> bytes: ...

class Connection(Generic[_C]):
    """
    Representation of a socket with a mysql server.

    The proper way to get an instance of this class is to call
    connect().

    Establish a connection to the MySQL database. Accepts several
    arguments:

    :param host: Host where the database server is located.
    :param user: Username to log in as.
    :param password: Password to use.
    :param database: Database to use, None to not use a particular one.
    :param port: MySQL port to use, default is usually OK. (default: 3306)
    :param bind_address: When the client has multiple network interfaces, specify
        the interface from which to connect to the host. Argument can be
        a hostname or an IP address.
    :param unix_socket: Use a unix socket rather than TCP/IP.
    :param read_timeout: The timeout for reading from the connection in seconds.
        (default: None - no timeout)
    :param write_timeout: The timeout for writing to the connection in seconds.
        (default: None - no timeout)
    :param str charset: Charset to use.
    :param str collation: Collation name to use.
    :param sql_mode: Default SQL_MODE to use.
    :param read_default_file:
        Specifies  my.cnf file to read these parameters from under the [client] section.
    :param conv:
        Conversion dictionary to use instead of the default one.
        This is used to provide custom marshalling and unmarshalling of types.
        See converters.
    :param use_unicode:
        Whether or not to default to unicode strings.
        This option defaults to true.
    :param client_flag: Custom flags to send to MySQL. Find potential values in constants.CLIENT.
    :param cursorclass: Custom cursor class to use.
    :param init_command: Initial SQL statement to run when connection is established.
    :param connect_timeout: The timeout for connecting to the database in seconds.
        (default: 10, min: 1, max: 31536000)
    :param ssl: A dict of arguments similar to mysql_ssl_set()'s parameters or an ssl.SSLContext.
    :param ssl_ca: Path to the file that contains a PEM-formatted CA certificate.
    :param ssl_cert: Path to the file that contains a PEM-formatted client certificate.
    :param ssl_disabled: A boolean value that disables usage of TLS.
    :param ssl_key: Path to the file that contains a PEM-formatted private key for
        the client certificate.
    :param ssl_key_password: The password for the client certificate private key.
    :param ssl_verify_cert: Set to true to check the server certificate's validity.
    :param ssl_verify_identity: Set to true to check the server's identity.
    :param read_default_group: Group to read from in the configuration file.
    :param autocommit: Autocommit mode. None means use server default. (default: False)
    :param local_infile: Boolean to enable the use of LOAD DATA LOCAL command. (default: False)
    :param max_allowed_packet: Max size of packet sent to server in bytes. (default: 16MB)
        Only used to limit size of "LOAD LOCAL INFILE" data packet smaller than default (16KB).
    :param defer_connect: Don't explicitly connect on construction - wait for connect call.
        (default: False)
    :param auth_plugin_map: A dict of plugin names to a class that processes that plugin.
        The class will take the Connection object as the argument to the constructor.
        The class needs an authenticate method taking an authentication packet as
        an argument.  For the dialog plugin, a prompt(echo, prompt) method can be used
        (if no authenticate method) for returning a string from the user. (experimental)
    :param server_public_key: SHA256 authentication plugin public key value. (default: None)
    :param binary_prefix: Add _binary prefix on bytes and bytearray. (default: False)
    :param compress: Not supported.
    :param named_pipe: Not supported.
    :param db: **DEPRECATED** Alias for database.
    :param passwd: **DEPRECATED** Alias for password.

    See `Connection <https://www.python.org/dev/peps/pep-0249/#connection-objects>`_ in the
    specification.
    """
    ssl: bool
    host: str
    port: int
    user: str | bytes | None
    password: bytes
    db: str | bytes | None
    unix_socket: _Address | None
    charset: str
    collation: str | None
    bind_address: str | None
    use_unicode: bool
    client_flag: int
    cursorclass: type[_C]
    connect_timeout: float | None
    host_info: str
    sql_mode: str | None
    init_command: str | None
    max_allowed_packet: int
    server_public_key: bytes | None
    encoding: str
    autocommit_mode: bool | None
    encoders: dict[type[Any], Callable[[Any], str]]  # argument type depends on the key
    decoders: dict[int, Callable[[str], Any]]  # return type depends on the key

    @overload
    def __init__(
        self,
        *,
        user: str | bytes | None = None,
        password: str | bytes = "",
        host: str | None = None,
        database: str | bytes | None = None,
        unix_socket: _Address | None = None,
        port: int = 0,
        charset: str = "",
        collation: str | None = None,
        sql_mode: str | None = None,
        read_default_file: str | None = None,
        conv: dict[int | type[Any], Callable[[Any], str] | Callable[[str], Any]] | None = None,
        use_unicode: bool = True,
        client_flag: int = 0,
        cursorclass: type[_C] = ...,
        init_command: str | None = None,
        connect_timeout: float = 10,
        read_default_group: str | None = None,
        autocommit: bool | None = False,
        local_infile: bool = False,
        max_allowed_packet: int = 16_777_216,
        defer_connect: bool = False,
        auth_plugin_map: dict[str, Callable[[Connection[Any]], Any]] | None = None,
        read_timeout: float | None = None,
        write_timeout: float | None = None,
        bind_address: str | None = None,
        binary_prefix: bool = False,
        program_name: str | None = None,
        server_public_key: bytes | None = None,
        ssl: dict[str, Incomplete] | SSLContext | None = None,
        ssl_ca: str | None = None,
        ssl_cert: str | None = None,
        ssl_disabled: bool | None = None,
        ssl_key: str | None = None,
        ssl_key_password: _PasswordType | None = None,
        ssl_verify_cert: bool | None = None,
        ssl_verify_identity: bool | None = None,
        compress: Unused = None,
        named_pipe: Unused = None,
        # different between overloads:
        passwd: None = None,  # deprecated
        db: None = None,  # deprecated
    ) -> None: ...
    @overload
    @deprecated("'passwd' and 'db' arguments are deprecated. Use 'password' and 'database' instead.")
    def __init__(
        self,
        *,
        user: str | bytes | None = None,
        password: str | bytes = "",
        host: str | None = None,
        database: str | bytes | None = None,
        unix_socket: _Address | None = None,
        port: int = 0,
        charset: str = "",
        collation: str | None = None,
        sql_mode: str | None = None,
        read_default_file: str | None = None,
        conv: dict[int | type[Any], Callable[[Any], str] | Callable[[str], Any]] | None = None,
        use_unicode: bool = True,
        client_flag: int = 0,
        cursorclass: type[_C] = ...,
        init_command: str | None = None,
        connect_timeout: float = 10,
        read_default_group: str | None = None,
        autocommit: bool | None = False,
        local_infile: bool = False,
        max_allowed_packet: int = 16_777_216,
        defer_connect: bool = False,
        auth_plugin_map: dict[str, Callable[[Connection[Any]], Any]] | None = None,
        read_timeout: float | None = None,
        write_timeout: float | None = None,
        bind_address: str | None = None,
        binary_prefix: bool = False,
        program_name: str | None = None,
        server_public_key: bytes | None = None,
        ssl: dict[str, Incomplete] | SSLContext | None = None,
        ssl_ca: str | None = None,
        ssl_cert: str | None = None,
        ssl_disabled: bool | None = None,
        ssl_key: str | None = None,
        ssl_key_password: _PasswordType | None = None,
        ssl_verify_cert: bool | None = None,
        ssl_verify_identity: bool | None = None,
        compress: Unused = None,
        named_pipe: Unused = None,
        # different between overloads:
        passwd: str | bytes | None = None,  # deprecated
        db: str | bytes | None = None,  # deprecated
    ) -> None: ...

    def close(self) -> None: ...
    @property
    def open(self) -> bool:
        """Return True if the connection is open."""
        ...
    def __del__(self) -> None:
        """Close connection without QUIT message."""
        ...
    def autocommit(self, value) -> None: ...
    def get_autocommit(self) -> bool: ...
    def commit(self) -> None:
        """
        Commit changes to stable storage.

        See `Connection.commit() <https://www.python.org/dev/peps/pep-0249/#commit>`_
        in the specification.
        """
        ...
    def begin(self) -> None:
        """Begin transaction."""
        ...
    def rollback(self) -> None:
        """
        Roll back the current transaction.

        See `Connection.rollback() <https://www.python.org/dev/peps/pep-0249/#rollback>`_
        in the specification.
        """
        ...
    def select_db(self, db) -> None:
        """
        Set current db.

        :param db: The name of the db.
        """
        ...
    def escape(self, obj, mapping: Mapping[str, Incomplete] | None = None):
        """
        Escape whatever value is passed.

        Non-standard, for internal use; do not use this in your applications.
        """
        ...
    def literal(self, obj):
        """
        Alias for escape().

        Non-standard, for internal use; do not use this in your applications.
        """
        ...
    def escape_string(self, s: AnyStr) -> AnyStr: ...

    @overload
    def cursor(self, cursor: None = None) -> _C:
        """
        Create a new cursor to execute queries with.

        :param cursor: The type of cursor to create. None means use Cursor.
        :type cursor: :py:class:`Cursor`, :py:class:`SSCursor`, :py:class:`DictCursor`,
            or :py:class:`SSDictCursor`.
        """
        ...
    @overload
    def cursor(self, cursor: type[_C2]) -> _C2: ...

    def query(self, sql, unbuffered: bool = False) -> int: ...
    def next_result(self, unbuffered: bool = False) -> int: ...
    def affected_rows(self): ...
    def kill(self, thread_id): ...
    def ping(self, reconnect: bool = True) -> None:
        """
        Check if the server is alive.

        :param reconnect: If the connection is closed, reconnect.
        :type reconnect: boolean

        :raise Error: If the connection is closed and reconnect=False.
        """
        ...
    @deprecated("Method is deprecated. Use set_character_set() instead.")
    def set_charset(self, charset: str) -> None:
        """Deprecated. Use set_character_set() instead."""
        ...
    def set_character_set(self, charset: str, collation: str | None = None) -> None:
        """
        Set charaset (and collation)

        Send "SET NAMES charset [COLLATE collation]" query.
        Update Connection.encoding based on charset.
        """
        ...
    def connect(self, sock: _socket | None = None) -> None: ...
    def write_packet(self, payload) -> None:
        """
        Writes an entire "mysql packet" in its entirety to the network
        adding its length and sequence number.
        """
        ...
    def _read_packet(self, packet_type=...):
        """
        Read an entire "mysql packet" in its entirety from the network
        and return a MysqlPacket type that represents the results.

        :raise OperationalError: If the connection to the MySQL server is lost.
        :raise InternalError: If the packet sequence number is wrong.
        """
        ...
    def insert_id(self): ...
    def thread_id(self): ...
    def character_set_name(self): ...
    def get_host_info(self) -> str: ...
    def get_proto_info(self): ...
    def get_server_info(self): ...
    def show_warnings(self):
        """Send the "SHOW WARNINGS" SQL command."""
        ...
    def __enter__(self) -> Self: ...
    def __exit__(self, *exc_info: object) -> None: ...
    Warning: type[Warning]
    Error: type[Error]
    InterfaceError: type[InterfaceError]
    DatabaseError: type[DatabaseError]
    DataError: type[DataError]
    OperationalError: type[OperationalError]
    IntegrityError: type[IntegrityError]
    InternalError: type[InternalError]
    ProgrammingError: type[ProgrammingError]
    NotSupportedError: type[NotSupportedError]

class MySQLResult:
    connection: Connection[Any] | None
    affected_rows: int | None
    insert_id: int | None
    server_status: int | None
    warning_count: int
    message: str | None
    field_count: int
    description: Incomplete
    rows: Incomplete
    has_next: bool | None
    unbuffered_active: bool
    def __init__(self, connection: Connection[Any]) -> None:
        """:type connection: Connection"""
        ...
    def __del__(self) -> None: ...
    first_packet: Incomplete
    def read(self) -> None: ...
    def init_unbuffered_query(self) -> None:
        """
        :raise OperationalError: If the connection to the MySQL server is lost.
        :raise InternalError:
        """
        ...

class LoadLocalFile:
    filename: FileDescriptorOrPath
    connection: Connection[Any]
    def __init__(self, filename: FileDescriptorOrPath, connection: Connection[Any]) -> None: ...
    def send_data(self) -> None:
        """Send data packets from the local file to the server"""
        ...

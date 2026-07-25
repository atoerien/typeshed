"""Core connection objects"""

import abc
import ssl
from _typeshed import Incomplete
from collections.abc import Callable
from logging import Logger
from typing import Final, Literal
from typing_extensions import Self

from .callback import CallbackManager
from .channel import Channel
from .compat import AbstractBase
from .credentials import PlainCredentials, _Credentials
from .frame import Method
from .spec import Connection as SpecConnection

PRODUCT: Final = "Pika Python Client Library"
LOGGER: Logger

class Parameters:
    """
    Base connection parameters class definition

    
    """
    __slots__ = (
        "_blocked_connection_timeout",
        "_channel_max",
        "_client_properties",
        "_connection_attempts",
        "_credentials",
        "_frame_max",
        "_heartbeat",
        "_host",
        "_locale",
        "_port",
        "_retry_delay",
        "_socket_timeout",
        "_stack_timeout",
        "_ssl_options",
        "_virtual_host",
        "_tcp_options",
    )
    DEFAULT_USERNAME: Final = "guest"
    DEFAULT_PASSWORD: Final = "guest"
    DEFAULT_BLOCKED_CONNECTION_TIMEOUT: Final = None
    DEFAULT_CHANNEL_MAX: Final = 65535
    DEFAULT_CLIENT_PROPERTIES: Final = None
    DEFAULT_CREDENTIALS: Final[PlainCredentials]
    DEFAULT_CONNECTION_ATTEMPTS: Final = 1
    DEFAULT_FRAME_MAX: Final = 131072
    DEFAULT_HEARTBEAT_TIMEOUT: None
    DEFAULT_HOST: Final = "localhost"
    DEFAULT_LOCALE: Final = "en_US"
    DEFAULT_PORT: Final = 5672
    DEFAULT_RETRY_DELAY: Final = 2.0
    DEFAULT_SOCKET_TIMEOUT: Final = 10.0
    DEFAULT_STACK_TIMEOUT: Final = 15.0
    DEFAULT_SSL: Final = False
    DEFAULT_SSL_OPTIONS: Final = None
    DEFAULT_SSL_PORT: Final = 5671
    DEFAULT_VIRTUAL_HOST: Final = "/"
    DEFAULT_TCP_OPTIONS: Final = None
    def __init__(self) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

    @property
    def blocked_connection_timeout(self) -> float | None:
        """
        :returns: blocked connection timeout. Defaults to
            `DEFAULT_BLOCKED_CONNECTION_TIMEOUT`.
        :rtype: float|None
        """
        ...
    @blocked_connection_timeout.setter
    def blocked_connection_timeout(self, value: float | None) -> None:
        """
        :returns: blocked connection timeout. Defaults to
            `DEFAULT_BLOCKED_CONNECTION_TIMEOUT`.
        :rtype: float|None
        """
        ...

    @property
    def channel_max(self) -> int:
        """
        :returns: max preferred number of channels. Defaults to
            `DEFAULT_CHANNEL_MAX`.
        :rtype: int
        """
        ...
    @channel_max.setter
    def channel_max(self, value: int) -> None:
        """
        :returns: max preferred number of channels. Defaults to
            `DEFAULT_CHANNEL_MAX`.
        :rtype: int
        """
        ...

    @property
    def client_properties(self) -> dict[Incomplete, Incomplete] | None:
        """
        :returns: client properties used to override the fields in the default
            client properties reported  to RabbitMQ via `Connection.StartOk`
            method. Defaults to `DEFAULT_CLIENT_PROPERTIES`.
        :rtype: dict|None
        """
        ...
    @client_properties.setter
    def client_properties(self, value: dict[Incomplete, Incomplete] | None) -> None:
        """
        :returns: client properties used to override the fields in the default
            client properties reported  to RabbitMQ via `Connection.StartOk`
            method. Defaults to `DEFAULT_CLIENT_PROPERTIES`.
        :rtype: dict|None
        """
        ...

    @property
    def connection_attempts(self) -> int:
        """
        :returns: number of socket connection attempts. Defaults to
            `DEFAULT_CONNECTION_ATTEMPTS`. See also `retry_delay`.
        :rtype: int
        """
        ...
    @connection_attempts.setter
    def connection_attempts(self, value: int) -> None:
        """
        :returns: number of socket connection attempts. Defaults to
            `DEFAULT_CONNECTION_ATTEMPTS`. See also `retry_delay`.
        :rtype: int
        """
        ...

    @property
    def credentials(self) -> _Credentials:
        """
        :rtype: one of the classes from `pika.credentials.VALID_TYPES`. Defaults
            to `DEFAULT_CREDENTIALS`.
        """
        ...
    @credentials.setter
    def credentials(self, value: _Credentials) -> None:
        """
        :rtype: one of the classes from `pika.credentials.VALID_TYPES`. Defaults
            to `DEFAULT_CREDENTIALS`.
        """
        ...

    @property
    def frame_max(self) -> int:
        """
        :returns: desired maximum AMQP frame size to use. Defaults to
            `DEFAULT_FRAME_MAX`.
        :rtype: int
        """
        ...
    @frame_max.setter
    def frame_max(self, value: int) -> None:
        """
        :returns: desired maximum AMQP frame size to use. Defaults to
            `DEFAULT_FRAME_MAX`.
        :rtype: int
        """
        ...

    @property
    def heartbeat(self) -> int | Callable[[Connection, int], int] | None:
        """
        :returns: AMQP connection heartbeat timeout value for negotiation during
            connection tuning or callable which is invoked during connection tuning.
            None to accept broker's value. 0 turns heartbeat off. Defaults to
            `DEFAULT_HEARTBEAT_TIMEOUT`.
        :rtype: int|callable|None
        """
        ...
    @heartbeat.setter
    def heartbeat(self, value: int | Callable[[Connection, int], int] | None) -> None:
        """
        :returns: AMQP connection heartbeat timeout value for negotiation during
            connection tuning or callable which is invoked during connection tuning.
            None to accept broker's value. 0 turns heartbeat off. Defaults to
            `DEFAULT_HEARTBEAT_TIMEOUT`.
        :rtype: int|callable|None
        """
        ...

    @property
    def host(self) -> str:
        """
        :returns: hostname or ip address of broker. Defaults to `DEFAULT_HOST`.
        :rtype: str
        """
        ...
    @host.setter
    def host(self, value: str) -> None:
        """
        :returns: hostname or ip address of broker. Defaults to `DEFAULT_HOST`.
        :rtype: str
        """
        ...

    @property
    def locale(self) -> str:
        """
        :returns: locale value to pass to broker; e.g., 'en_US'. Defaults to
            `DEFAULT_LOCALE`.
        :rtype: str
        """
        ...
    @locale.setter
    def locale(self, value: str) -> None:
        """
        :returns: locale value to pass to broker; e.g., 'en_US'. Defaults to
            `DEFAULT_LOCALE`.
        :rtype: str
        """
        ...

    @property
    def port(self) -> int:
        """
        :returns: port number of broker's listening socket. Defaults to
            `DEFAULT_PORT`.
        :rtype: int
        """
        ...
    @port.setter
    def port(self, value: int | str) -> None:
        """
        :returns: port number of broker's listening socket. Defaults to
            `DEFAULT_PORT`.
        :rtype: int
        """
        ...

    @property
    def retry_delay(self) -> int | float:
        """
        :returns: interval between socket connection attempts; see also
            `connection_attempts`. Defaults to `DEFAULT_RETRY_DELAY`.
        :rtype: float
        """
        ...
    @retry_delay.setter
    def retry_delay(self, value: float) -> None:
        """
        :returns: interval between socket connection attempts; see also
            `connection_attempts`. Defaults to `DEFAULT_RETRY_DELAY`.
        :rtype: float
        """
        ...

    @property
    def socket_timeout(self) -> float | None:
        """
        :returns: socket connect timeout in seconds. Defaults to
            `DEFAULT_SOCKET_TIMEOUT`. The value None disables this timeout.
        :rtype: float|None
        """
        ...
    @socket_timeout.setter
    def socket_timeout(self, value: float | None) -> None:
        """
        :returns: socket connect timeout in seconds. Defaults to
            `DEFAULT_SOCKET_TIMEOUT`. The value None disables this timeout.
        :rtype: float|None
        """
        ...

    @property
    def stack_timeout(self) -> float | None:
        """
        :returns: full protocol stack TCP/[SSL]/AMQP bring-up timeout in
            seconds. Defaults to `DEFAULT_STACK_TIMEOUT`. The value None
            disables this timeout.
        :rtype: float
        """
        ...
    @stack_timeout.setter
    def stack_timeout(self, value: float | None) -> None:
        """
        :returns: full protocol stack TCP/[SSL]/AMQP bring-up timeout in
            seconds. Defaults to `DEFAULT_STACK_TIMEOUT`. The value None
            disables this timeout.
        :rtype: float
        """
        ...

    @property
    def ssl_options(self) -> SSLOptions | None:
        """
        :returns: None for plaintext or `pika.SSLOptions` instance for SSL/TLS.
        :rtype: `pika.SSLOptions`|None
        """
        ...
    @ssl_options.setter
    def ssl_options(self, value: SSLOptions | None) -> None:
        """
        :returns: None for plaintext or `pika.SSLOptions` instance for SSL/TLS.
        :rtype: `pika.SSLOptions`|None
        """
        ...

    @property
    def virtual_host(self) -> str:
        """
        :returns: rabbitmq virtual host name. Defaults to
            `DEFAULT_VIRTUAL_HOST`.
        :rtype: str
        """
        ...
    @virtual_host.setter
    def virtual_host(self, value: str) -> None:
        """
        :returns: rabbitmq virtual host name. Defaults to
            `DEFAULT_VIRTUAL_HOST`.
        :rtype: str
        """
        ...

    @property
    def tcp_options(self) -> dict[str, Incomplete] | None: ...
    @tcp_options.setter
    def tcp_options(self, value: dict[str, Incomplete] | None) -> None: ...

class ConnectionParameters(Parameters):
    """
    Connection parameters object that is passed into the connection adapter
    upon construction.
    """
    __slots__ = ()
    def __init__(
        self,
        host: str = ...,
        port: int = ...,
        virtual_host: str = ...,
        credentials: _Credentials = ...,
        channel_max: int = ...,
        frame_max: int = ...,
        heartbeat: int | Callable[[Connection, int], int] | None = ...,
        ssl_options: SSLOptions | None = ...,
        connection_attempts: int = ...,
        retry_delay: float = ...,
        socket_timeout: float | None = ...,
        stack_timeout: float | None = ...,
        locale: str = ...,
        blocked_connection_timeout: float | None = ...,
        client_properties: dict[str, Incomplete] | None = ...,
        tcp_options: dict[str, Incomplete] | None = ...,
    ) -> None: ...

class URLParameters(Parameters):
    """
    Connect to RabbitMQ via an AMQP URL in the format::

         amqp://username:password@host:port/<virtual_host>[?query-string]

    Ensure that the virtual host is URI encoded when specified. For example if
    you are using the default "/" virtual host, the value should be `%2f`.

    See `Parameters` for default values.

    Valid query string values are:

        - channel_max:
            Override the default maximum channel count value
        - client_properties:
            dict of client properties used to override the fields in the default
            client properties reported to RabbitMQ via `Connection.StartOk`
            method
        - connection_attempts:
            Specify how many times pika should try and reconnect before it gives up
        - frame_max:
            Override the default maximum frame size for communication
        - heartbeat:
            Desired connection heartbeat timeout for negotiation. If not present
            the broker's value is accepted. 0 turns heartbeat off.
        - locale:
            Override the default `en_US` locale value
        - ssl_options:
            None for plaintext; for SSL: dict of public ssl context-related
            arguments that may be passed to :meth:`ssl.SSLSocket` as kwargs,
            except `sock`, `server_side`,`do_handshake_on_connect`, `family`,
            `type`, `proto`, `fileno`.
        - retry_delay:
            The number of seconds to sleep before attempting to connect on
            connection failure.
        - socket_timeout:
            Socket connect timeout value in seconds (float or int)
        - stack_timeout:
            Positive full protocol stack (TCP/[SSL]/AMQP) bring-up timeout in
            seconds. It's recommended to set this value higher than
            `socket_timeout`.
        - blocked_connection_timeout:
            Set the timeout, in seconds, that the connection may remain blocked
            (triggered by Connection.Blocked from broker); if the timeout
            expires before connection becomes unblocked, the connection will be
            torn down, triggering the connection's on_close_callback
        - tcp_options:
            Set the tcp options for the underlying socket.

    :param str url: The AMQP URL to connect to
    """
    __slots__ = ("_all_url_query_values",)
    def __init__(self, url: str) -> None:
        """
        Create a new URLParameters instance.

        :param str url: The URL value
        """
        ...

class SSLOptions:
    """
    Class used to provide parameters for optional fine grained control of SSL
    socket wrapping.
    """
    __slots__ = ("context", "server_hostname")
    context: ssl.SSLContext
    server_hostname: str | None
    def __init__(self, context: ssl.SSLContext, server_hostname: str | None = None) -> None:
        """
        :param ssl.SSLContext context: SSLContext instance
        :param str|None server_hostname: SSLContext.wrap_socket, used to enable
            SNI
        """
        ...

class Connection(AbstractBase, metaclass=abc.ABCMeta):
    ON_CONNECTION_CLOSED: Final = "_on_connection_closed"
    ON_CONNECTION_ERROR: Final = "_on_connection_error"
    ON_CONNECTION_OPEN_OK: Final = "_on_connection_open_ok"
    CONNECTION_CLOSED: Final = 0
    CONNECTION_INIT: Final = 1
    CONNECTION_PROTOCOL: Final = 2
    CONNECTION_START: Final = 3
    CONNECTION_TUNE: Final = 4
    CONNECTION_OPEN: Final = 5
    CONNECTION_CLOSING: Final = 6
    connection_state: Literal[0, 1, 2, 3, 4, 5, 6]  # one of the constants above
    params: Parameters
    callbacks: CallbackManager
    server_capabilities: dict[str, bool] | None
    server_properties: dict[str, Incomplete] | None
    known_hosts: str | None
    def __init__(
        self,
        parameters: Parameters | None = None,
        on_open_callback: Callable[[Self], object] | None = None,
        on_open_error_callback: Callable[[Self, BaseException], object] | None = None,
        on_close_callback: Callable[[Self, BaseException], object] | None = None,
        internal_connection_workflow: bool = True,
    ) -> None:
        """
        Connection initialization expects an object that has implemented the
         Parameters class and a callback function to notify when we have
         successfully connected to the AMQP Broker.

        Available Parameters classes are the ConnectionParameters class and
        URLParameters class.

        :param pika.connection.Parameters parameters: Read-only connection
            parameters.
        :param callable on_open_callback: Called when the connection is opened:
            on_open_callback(connection)
        :param None | method on_open_error_callback: Called if the connection
            can't be established or connection establishment is interrupted by
            `Connection.close()`: on_open_error_callback(Connection, exception).
        :param None | method on_close_callback: Called when a previously fully
            open connection is closed:
            `on_close_callback(Connection, exception)`, where `exception` is
            either an instance of `exceptions.ConnectionClosed` if closed by
            user or broker or exception of another type that describes the cause
            of connection failure.
        :param bool internal_connection_workflow: True for autonomous connection
            establishment which is default; False for externally-managed
            connection workflow via the `create_connection()` factory.
        """
        ...
    def add_on_close_callback(self, callback: Callable[[Self, BaseException], object]) -> None:
        """
        Add a callback notification when the connection has closed. The
        callback will be passed the connection and an exception instance. The
        exception will either be an instance of `exceptions.ConnectionClosed` if
        a fully-open connection was closed by user or broker or exception of
        another type that describes the cause of connection closure/failure.

        :param callable callback: Callback to call on close, having the signature:
            callback(pika.connection.Connection, exception)
        """
        ...
    def add_on_connection_blocked_callback(self, callback: Callable[[Self, Method[SpecConnection.Blocked]], object]) -> None:
        """
        RabbitMQ AMQP extension - Add a callback to be notified when the
        connection gets blocked (`Connection.Blocked` received from RabbitMQ)
        due to the broker running low on resources (memory or disk). In this
        state RabbitMQ suspends processing incoming data until the connection
        is unblocked, so it's a good idea for publishers receiving this
        notification to suspend publishing until the connection becomes
        unblocked.

        See also `Connection.add_on_connection_unblocked_callback()`

        See also `ConnectionParameters.blocked_connection_timeout`.

        :param callable callback: Callback to call on `Connection.Blocked`,
            having the signature `callback(connection, pika.frame.Method)`,
            where the method frame's `method` member is of type
            `pika.spec.Connection.Blocked`
        """
        ...
    def add_on_connection_unblocked_callback(
        self, callback: Callable[[Self, Method[SpecConnection.Unblocked]], object]
    ) -> None:
        """
        RabbitMQ AMQP extension - Add a callback to be notified when the
        connection gets unblocked (`Connection.Unblocked` frame is received from
        RabbitMQ) letting publishers know it's ok to start publishing again.

        :param callable callback: Callback to call on
            `Connection.Unblocked`, having the signature
            `callback(connection, pika.frame.Method)`, where the method frame's
            `method` member is of type `pika.spec.Connection.Unblocked`
        """
        ...
    def add_on_open_callback(self, callback: Callable[[Self], object]) -> None:
        """
        Add a callback notification when the connection has opened. The
        callback will be passed the connection instance as its only arg.

        :param callable callback: Callback to call when open
        """
        ...
    def add_on_open_error_callback(
        self, callback: Callable[[Self, BaseException], object], remove_default: bool = True
    ) -> None:
        """
        Add a callback notification when the connection can not be opened.

        The callback method should accept the connection instance that could not
        connect, and either a string or an exception as its second arg.

        :param callable callback: Callback to call when can't connect, having
            the signature _(Connection, Exception)
        :param bool remove_default: Remove default exception raising callback
        """
        ...
    def channel(
        self, channel_number: int | None = None, on_open_callback: Callable[[Channel], object] | None = None
    ) -> Channel: ...
    def update_secret(
        self,
        new_secret: str | bytes,
        reason: str | bytes,
        callback: Callable[[Method[SpecConnection.UpdateSecretOk]], object] | None = None,
    ) -> None: ...
    def close(self, reply_code: int = 200, reply_text: str = "Normal shutdown") -> None: ...
    @property
    def is_closed(self) -> bool:
        """Returns a boolean reporting the current connection state."""
        ...
    @property
    def is_closing(self) -> bool:
        """
        Returns True if connection is in the process of closing due to
        client-initiated `close` request, but closing is not yet complete.
        """
        ...
    @property
    def is_open(self) -> bool:
        """Returns a boolean reporting the current connection state."""
        ...
    @property
    def basic_nack(self) -> bool:
        """
        Specifies if the server supports basic.nack on the active connection.

        :rtype: bool
        """
        ...
    @property
    def consumer_cancel_notify(self) -> bool:
        """
        Specifies if the server supports consumer cancel notification on the
        active connection.

        :rtype: bool
        """
        ...
    @property
    def exchange_exchange_bindings(self) -> bool:
        """
        Specifies if the active connection supports exchange to exchange
        bindings.

        :rtype: bool
        """
        ...
    @property
    def publisher_confirms(self) -> bool:
        """
        Specifies if the active connection can use publisher confirmations.

        :rtype: bool
        """
        ...

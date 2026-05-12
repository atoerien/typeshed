import socket
import threading
from _typeshed import FileDescriptorLike
from _typeshed.wsgi import WSGIEnvironment
from collections.abc import Callable
from selectors import SelectorKey
from ssl import SSLContext
from typing import Any, Protocol, type_check_only

from wsproto import ConnectionType, WSConnection
from wsproto.events import Request
from wsproto.frame_protocol import CloseReason

@type_check_only
class _ThreadClassProtocol(Protocol):
    name: str
    # this accepts any callable as the target, like `threading.Thread`
    def __init__(self, target: Callable[..., Any]) -> None: ...
    def start(self) -> None: ...

@type_check_only
class _EventClassProtocol(Protocol):
    def clear(self) -> None: ...
    def set(self) -> None: ...
    def wait(self, timeout: float | None = None) -> bool: ...

@type_check_only
class _SelectorClassProtocol(Protocol):
    # the signature of `register` here is the same as `selectors._BaseSelectorImpl` from the stdlib
    def register(self, fileobj: FileDescriptorLike, events: int, data: Any = None) -> SelectorKey: ...
    # the signature of `select` here is the same as `selectors.DefaultSelector` from the stdlib
    def select(self, timeout: float | None = None) -> list[tuple[SelectorKey, int]]: ...
    def close(self) -> None: ...

class Base:
    subprotocol: str | None
    sock: socket.socket | None
    receive_bytes: int
    ping_interval: float | None
    max_message_size: int | None
    pong_received: bool
    input_buffer: list[bytes | str]
    incoming_message: bytes | str | None
    incoming_message_len: int
    connected: bool
    is_server: bool
    close_reason: CloseReason
    close_message: str | None
    selector_class: type[_SelectorClassProtocol]
    event: _EventClassProtocol | threading.Event
    ws: WSConnection
    thread: _ThreadClassProtocol | threading.Thread
    def __init__(
        self,
        sock: socket.socket | None = None,
        connection_type: ConnectionType | None = None,
        receive_bytes: int = 4096,
        ping_interval: float | None = None,
        max_message_size: int | None = None,
        thread_class: type[_ThreadClassProtocol] | None = None,
        event_class: type[_EventClassProtocol] | None = None,
        selector_class: type[_SelectorClassProtocol] | None = None,
    ) -> None: ...
    def handshake(self) -> None: ...
    # data can be antyhing. a special case is made for `bytes`, anything else is converted to `str`.
    def send(self, data: bytes | Any) -> None:
        """
        Send data over the WebSocket connection.

        :param data: The data to send. If ``data`` is of type ``bytes``, then
                     a binary message is sent. Else, the message is sent in
                     text format.
        """
        ...
    def receive(self, timeout: float | None = None) -> bytes | str | None:
        """
        Receive data over the WebSocket connection.

        :param timeout: Amount of time to wait for the data, in seconds. Set
                        to ``None`` (the default) to wait indefinitely. Set
                        to 0 to read without blocking.

        The data received is returned, as ``bytes`` or ``str``, depending on
        the type of the incoming message.
        """
        ...
    def close(self, reason: CloseReason | None = None, message: str | None = None) -> None:
        """
        Close the WebSocket connection.

        :param reason: A numeric status code indicating the reason of the
                       closure, as defined by the WebSocket specification. The
                       default is 1000 (normal closure).
        :param message: A text message to be sent to the other side.
        """
        ...
    def choose_subprotocol(self, request: Request) -> str | None: ...

class Server(Base):
    """
    This class implements a WebSocket server.

    Instead of creating an instance of this class directly, use the
    ``accept()`` class method to create individual instances of the server,
    each bound to a client request.
    """
    environ: WSGIEnvironment
    subprotocols: list[str]
    mode: str
    connected: bool
    def __init__(
        self,
        environ: WSGIEnvironment,
        subprotocols: list[str] | None = None,
        receive_bytes: int = 4096,
        ping_interval: float | None = None,
        max_message_size: int | None = None,
        thread_class: type[_ThreadClassProtocol] | None = None,
        event_class: type[_EventClassProtocol] | None = None,
        selector_class: type[_SelectorClassProtocol] | None = None,
    ) -> None: ...
    @classmethod
    def accept(
        cls,
        environ: WSGIEnvironment,
        subprotocols: list[str] | None = None,
        receive_bytes: int = 4096,
        ping_interval: float | None = None,
        max_message_size: int | None = None,
        thread_class: type[_ThreadClassProtocol] | None = None,
        event_class: type[_EventClassProtocol] | None = None,
        selector_class: type[_SelectorClassProtocol] | None = None,
    ) -> Server:
        """
        Accept a WebSocket connection from a client.

        :param environ: A WSGI ``environ`` dictionary with the request details.
                        Among other things, this class expects to find the
                        low-level network socket for the connection somewhere
                        in this dictionary. Since the WSGI specification does
                        not cover where or how to store this socket, each web
                        server does this in its own different way. Werkzeug,
                        Gunicorn, Eventlet and Gevent are the only web servers
                        that are currently supported.
        :param subprotocols: A list of supported subprotocols, or ``None`` (the
                             default) to disable subprotocol negotiation.
        :param receive_bytes: The size of the receive buffer, in bytes. The
                              default is 4096.
        :param ping_interval: Send ping packets to clients at the requested
                              interval in seconds. Set to ``None`` (the
                              default) to disable ping/pong logic. Enable to
                              prevent disconnections when the line is idle for
                              a certain amount of time, or to detect
                              unresponsive clients and disconnect them. A
                              recommended interval is 25 seconds.
        :param max_message_size: The maximum size allowed for a message, in
                                 bytes, or ``None`` for no limit. The default
                                 is ``None``.
        :param thread_class: The ``Thread`` class to use when creating
                             background threads. The default is the
                             ``threading.Thread`` class from the Python
                             standard library.
        :param event_class: The ``Event`` class to use when creating event
                            objects. The default is the `threading.Event``
                            class from the Python standard library.
        :param selector_class: The ``Selector`` class to use when creating
                               selectors. The default is the
                               ``selectors.DefaultSelector`` class from the
                               Python standard library.
        """
        ...
    def handshake(self) -> None: ...
    def choose_subprotocol(self, request: Request) -> str | None:
        """
        Choose a subprotocol to use for the WebSocket connection.

        The default implementation selects the first protocol requested by the
        client that is accepted by the server. Subclasses can override this
        method to implement a different subprotocol negotiation algorithm.

        :param request: A ``Request`` object.

        The method should return the subprotocol to use, or ``None`` if no
        subprotocol is chosen.
        """
        ...

class Client(Base):
    """
    This class implements a WebSocket client.

    Instead of creating an instance of this class directly, use the
    ``connect()`` class method to create an instance that is connected to a
    server.
    """
    host: str
    port: int
    path: str
    subprotocols: list[str]
    extra_headeers: list[tuple[bytes, bytes]]
    subprotocol: str | None
    connected: bool
    def __init__(
        self,
        url: str,
        subprotocols: list[str] | None = None,
        headers: dict[bytes, bytes] | list[tuple[bytes, bytes]] | None = None,
        receive_bytes: int = 4096,
        ping_interval: float | None = None,
        max_message_size: int | None = None,
        ssl_context: SSLContext | None = None,
        thread_class: type[_ThreadClassProtocol] | None = None,
        event_class: type[_EventClassProtocol] | None = None,
    ) -> None: ...
    @classmethod
    def connect(
        cls,
        url: str,
        subprotocols: list[str] | None = None,
        headers: dict[bytes, bytes] | list[tuple[bytes, bytes]] | None = None,
        receive_bytes: int = 4096,
        ping_interval: float | None = None,
        max_message_size: int | None = None,
        ssl_context: SSLContext | None = None,
        thread_class: type[_ThreadClassProtocol] | None = None,
        event_class: type[_EventClassProtocol] | None = None,
    ) -> Client:
        """
        Returns a WebSocket client connection.

        :param url: The connection URL. Both ``ws://`` and ``wss://`` URLs are
                    accepted.
        :param subprotocols: The name of the subprotocol to use, or a list of
                             subprotocol names in order of preference. Set to
                             ``None`` (the default) to not use a subprotocol.
        :param headers: A dictionary or list of tuples with additional HTTP
                        headers to send with the connection request. Note that
                        custom headers are not supported by the WebSocket
                        protocol, so the use of this parameter is not
                        recommended.
        :param receive_bytes: The size of the receive buffer, in bytes. The
                              default is 4096.
        :param ping_interval: Send ping packets to the server at the requested
                              interval in seconds. Set to ``None`` (the
                              default) to disable ping/pong logic. Enable to
                              prevent disconnections when the line is idle for
                              a certain amount of time, or to detect an
                              unresponsive server and disconnect. A recommended
                              interval is 25 seconds. In general it is
                              preferred to enable ping/pong on the server, and
                              let the client respond with pong (which it does
                              regardless of this setting).
        :param max_message_size: The maximum size allowed for a message, in
                                 bytes, or ``None`` for no limit. The default
                                 is ``None``.
        :param ssl_context: An ``SSLContext`` instance, if a default SSL
                            context isn't sufficient.
        :param thread_class: The ``Thread`` class to use when creating
                             background threads. The default is the
                             ``threading.Thread`` class from the Python
                             standard library.
        :param event_class: The ``Event`` class to use when creating event
                            objects. The default is the `threading.Event``
                            class from the Python standard library.
        """
        ...
    def handshake(self) -> None: ...
    def close(self, reason: CloseReason | None = None, message: str | None = None) -> None: ...

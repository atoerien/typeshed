"""
Utilities for implementing `nbio_interface.AbstractIOServices` for
pika connection adapters.
"""

import abc
from collections.abc import Callable
from socket import socket
from ssl import SSLContext, SSLSocket
from typing import Any

from pika.adapters.utils.nbio_interface import (
    AbstractFileDescriptorServices,
    AbstractIOReference,
    AbstractIOServices,
    AbstractStreamProtocol,
    AbstractStreamTransport,
)
from pika.adapters.utils.selector_ioloop_adapter import _SupportsCancel

def check_callback_arg(callback: Callable[..., Any], name: str) -> None:
    """
    Raise TypeError if callback is not callable

    :param callback: callback to check
    :param name: Name to include in exception text
    :raises TypeError:
    """
    ...
def check_fd_arg(fd: int) -> None:
    """
    Raise TypeError if file descriptor is not an integer

    :param fd: file descriptor
    :raises TypeError:
    """
    ...

class SocketConnectionMixin:
    """
    Implements
    `pika.adapters.utils.nbio_interface.AbstractIOServices.connect_socket()`
    on top of
    `pika.adapters.utils.nbio_interface.AbstractFileDescriptorServices` and
    basic `pika.adapters.utils.nbio_interface.AbstractIOServices`.
    """
    def connect_socket(
        self, sock: socket, resolved_addr: tuple[str, int], on_done: Callable[[BaseException | None], None]
    ) -> _AsyncServiceAsyncHandle:
        """
        Implement
        :py:meth:`.nbio_interface.AbstractIOServices.connect_socket()`.
        """
        ...

class StreamingConnectionMixin:
    """
    Implements
    `.nbio_interface.AbstractIOServices.create_streaming_connection()` on
    top of `.nbio_interface.AbstractFileDescriptorServices` and basic
    `nbio_interface.AbstractIOServices` services.
    """
    def create_streaming_connection(
        self,
        protocol_factory: Callable[[], AbstractStreamProtocol],
        sock: socket,
        on_done: Callable[[tuple[AbstractStreamTransport, AbstractStreamProtocol] | BaseException], None],
        ssl_context: SSLContext | None = None,
        server_hostname: str | None = None,
    ) -> AbstractIOReference:
        """
        Implement
        :py:meth:`.nbio_interface.AbstractIOServices.create_streaming_connection()`.
        """
        ...

class _AsyncServiceAsyncHandle(AbstractIOReference):
    """
    This module's adaptation of `.nbio_interface.AbstractIOReference`

    
    """
    def __init__(self, subject: _SupportsCancel) -> None:
        """:param subject: subject of the reference containing a `cancel()` method"""
        ...
    def cancel(self) -> bool:
        """
        Cancel pending operation

        :returns: False if was already done or cancelled; True otherwise
        :rtype: bool
        """
        ...

class _AsyncSocketConnector:
    """
    Connects the given non-blocking socket asynchronously using
    `.nbio_interface.AbstractFileDescriptorServices` and basic
    `.nbio_interface.AbstractIOServices`. Used for implementing
    `.nbio_interface.AbstractIOServices.connect_socket()`.
    """
    def __init__(
        self,
        nbio: AbstractIOServices | AbstractFileDescriptorServices,
        sock: socket,
        resolved_addr: tuple[str, int],
        on_done: Callable[[BaseException | None], None],
    ) -> None:
        """
        :param AbstractIOServices | AbstractFileDescriptorServices nbio:
        :param socket.socket sock: non-blocking socket that needs to be
            connected via `socket.socket.connect()`
        :param tuple resolved_addr: resolved destination address/port two-tuple
            which is compatible with the given's socket's address family
        :param callable on_done: user callback that takes None upon successful
            completion or exception upon error (check for `BaseException`) as
            its only arg. It will not be called if the operation was cancelled.
        :raises ValueError: if host portion of `resolved_addr` is not an IP
            address or is inconsistent with the socket's address family as
            validated via `socket.inet_pton()`
        """
        ...
    def start(self) -> AbstractIOReference:
        """
        Start asynchronous connection establishment.

        :rtype: AbstractIOReference
        """
        ...
    def cancel(self) -> bool:
        """
        Cancel pending connection request without calling user's completion
        callback.

        :returns: False if was already done or cancelled; True otherwise
        :rtype: bool
        """
        ...

class _AsyncStreamConnector:
    """
    Performs asynchronous SSL session establishment, if requested, on the
    already-connected socket and links the streaming transport to protocol.
    Used for implementing
    `.nbio_interface.AbstractIOServices.create_streaming_connection()`.
    """
    def __init__(
        self,
        nbio: AbstractIOServices | AbstractFileDescriptorServices,
        protocol_factory: Callable[[], AbstractStreamProtocol],
        sock: socket,
        ssl_context: SSLContext,
        server_hostname: str | None,
        on_done: Callable[[tuple[AbstractStreamTransport, AbstractStreamProtocol] | BaseException], None],
    ) -> None:
        """
        NOTE: We take ownership of the given socket upon successful completion
        of the constructor.

        See `AbstractIOServices.create_streaming_connection()` for detailed
        documentation of the corresponding args.

        :param AbstractIOServices | AbstractFileDescriptorServices nbio:
        :param callable protocol_factory:
        :param socket.socket sock:
        :param ssl.SSLContext | None ssl_context:
        :param str | None server_hostname:
        :param callable on_done:
        """
        ...
    def start(self) -> AbstractIOReference:
        """
        Kick off the workflow

        :rtype: AbstractIOReference
        """
        ...
    def cancel(self) -> bool:
        """
        Cancel pending connection request without calling user's completion
        callback.

        :returns: False if was already done or cancelled; True otherwise
        :rtype: bool
        """
        ...

class _AsyncTransportBase(AbstractStreamTransport, metaclass=abc.ABCMeta):
    """
    Base class for `_AsyncPlaintextTransport` and `_AsyncSSLTransport`.

    
    """
    class RxEndOfFile(OSError):
        """
        We raise this internally when EOF (empty read) is detected on input.

        
        """
        def __init__(self) -> None: ...

    def __init__(
        self,
        sock: socket | SSLSocket,
        protocol: AbstractStreamProtocol,
        nbio: AbstractIOServices | AbstractFileDescriptorServices,
    ) -> None:
        """
        :param socket.socket | ssl.SSLSocket sock: connected socket
        :param pika.adapters.utils.nbio_interface.AbstractStreamProtocol protocol:
            corresponding protocol in this transport/protocol pairing; the
            protocol already had its `connection_made()` method called.
        :param AbstractIOServices | AbstractFileDescriptorServices nbio:
        """
        ...
    def abort(self) -> None:
        """
        Close connection abruptly without waiting for pending I/O to
        complete. Will invoke the corresponding protocol's `connection_lost()`
        method asynchronously (not in context of the abort() call).

        :raises Exception: Exception-based exception on error
        """
        ...
    def get_protocol(self) -> AbstractStreamProtocol:
        """
        Return the protocol linked to this transport.

        :rtype: pika.adapters.utils.nbio_interface.AbstractStreamProtocol
        """
        ...
    def get_write_buffer_size(self) -> int:
        """
        :returns: Current size of output data buffered by the transport
        :rtype: int
        """
        ...

class _AsyncPlaintextTransport(_AsyncTransportBase):
    """
    Implementation of `nbio_interface.AbstractStreamTransport` for a
    plaintext connection.
    """
    def __init__(
        self,
        sock: socket | SSLSocket,
        protocol: AbstractStreamProtocol,
        nbio: AbstractIOServices | AbstractFileDescriptorServices,
    ) -> None:
        """
        :param socket.socket sock: non-blocking connected socket
        :param pika.adapters.utils.nbio_interface.AbstractStreamProtocol protocol:
            corresponding protocol in this transport/protocol pairing; the
            protocol already had its `connection_made()` method called.
        :param AbstractIOServices | AbstractFileDescriptorServices nbio:
        """
        ...
    def write(self, data: bytes) -> None:
        """
        Buffer the given data until it can be sent asynchronously.

        :param bytes data:
        :raises ValueError: if called with empty data
        """
        ...

class _AsyncSSLTransport(_AsyncTransportBase):
    """
    Implementation of `.nbio_interface.AbstractStreamTransport` for an SSL
    connection.
    """
    def __init__(
        self, sock: SSLSocket, protocol: AbstractStreamProtocol, nbio: AbstractIOServices | AbstractFileDescriptorServices
    ) -> None:
        """
        :param ssl.SSLSocket sock: non-blocking connected socket
        :param pika.adapters.utils.nbio_interface.AbstractStreamProtocol protocol:
            corresponding protocol in this transport/protocol pairing; the
            protocol already had its `connection_made()` method called.
        :param AbstractIOServices | AbstractFileDescriptorServices nbio:
        """
        ...
    def write(self, data: bytes) -> None:
        """
        Buffer the given data until it can be sent asynchronously.

        :param bytes data:
        :raises ValueError: if called with empty data
        """
        ...

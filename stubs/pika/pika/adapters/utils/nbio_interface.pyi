"""
Non-blocking I/O interface for pika connection adapters.

I/O interface expected by `pika.adapters.base_connection.BaseConnection`

NOTE: This API is modeled after asyncio in python3 for a couple of reasons
    1. It's a sensible API
    2. To make it easy to implement at least on top of the built-in asyncio

Furthermore, the API caters to the needs of pika core and lack of generalization
is intentional for the sake of reducing complexity of the implementation and
testing and lessening the maintenance burden.
"""

import abc
from collections.abc import Callable
from socket import socket
from ssl import SSLContext

import pika.compat

class AbstractIOServices(pika.compat.AbstractBase, metaclass=abc.ABCMeta):
    """
    Interface to I/O services required by `pika.adapters.BaseConnection` and
    related utilities.

    NOTE: This is not a public API. Pika users should rely on the native I/O
    loop APIs (e.g., asyncio event loop, tornado ioloop, twisted reactor, etc.)
    that corresponds to the chosen Connection adapter.
    """
    @abc.abstractmethod
    def get_native_ioloop(self) -> object: ...
    @abc.abstractmethod
    def close(self) -> None: ...
    @abc.abstractmethod
    def run(self) -> None: ...
    @abc.abstractmethod
    def stop(self) -> None: ...
    @abc.abstractmethod
    def add_callback_threadsafe(self, callback: Callable[..., None]) -> None: ...
    @abc.abstractmethod
    def call_later(self, delay: float, callback: Callable[..., None]) -> AbstractTimerReference: ...
    @abc.abstractmethod
    def getaddrinfo(
        self,
        host: str | bytes | None,
        port: str | bytes | int | None,
        on_done: Callable[  # list is result of socket.getaddrinfo
            [list[tuple[int, int, int, str, tuple[str, int] | tuple[str, int, int, int] | tuple[int, bytes]]] | BaseException],
            None,
        ],
        family: int = 0,
        socktype: int = 0,
        proto: int = 0,
        flags: int = 0,
    ) -> AbstractIOReference: ...
    @abc.abstractmethod
    def connect_socket(
        self, sock: socket, resolved_addr: tuple[str, int], on_done: Callable[[BaseException | None], None]
    ) -> AbstractIOReference: ...
    @abc.abstractmethod
    def create_streaming_connection(
        self,
        protocol_factory: Callable[[], AbstractStreamProtocol],
        sock: socket,
        on_done: Callable[[tuple[AbstractStreamTransport, AbstractStreamProtocol] | BaseException], None],
        ssl_context: SSLContext | None = None,
        server_hostname: str | None = None,
    ) -> AbstractIOReference: ...

class AbstractFileDescriptorServices(pika.compat.AbstractBase):
    @abc.abstractmethod
    def set_reader(self, fd: int, on_readable: Callable[[], None]) -> None: ...
    @abc.abstractmethod
    def remove_reader(self, fd: int) -> bool: ...
    @abc.abstractmethod
    def set_writer(self, fd: int, on_writable: Callable[[], None]) -> None: ...
    @abc.abstractmethod
    def remove_writer(self, fd: int) -> bool: ...

class AbstractTimerReference(pika.compat.AbstractBase):
    @abc.abstractmethod
    def cancel(self) -> None: ...

class AbstractIOReference(pika.compat.AbstractBase):
    @abc.abstractmethod
    def cancel(self) -> bool: ...

class AbstractStreamProtocol(pika.compat.AbstractBase):
    @abc.abstractmethod
    def connection_made(self, transport: AbstractStreamTransport) -> None: ...
    @abc.abstractmethod
    def connection_lost(self, error: BaseException | None) -> None: ...
    @abc.abstractmethod
    def eof_received(self) -> bool | None: ...
    @abc.abstractmethod
    def data_received(self, data: bytes) -> None: ...

class AbstractStreamTransport(pika.compat.AbstractBase):
    @abc.abstractmethod
    def abort(self) -> None: ...
    @abc.abstractmethod
    def get_protocol(self) -> AbstractStreamProtocol: ...
    @abc.abstractmethod
    def write(self, data: bytes) -> None: ...
    @abc.abstractmethod
    def get_write_buffer_size(self) -> int: ...

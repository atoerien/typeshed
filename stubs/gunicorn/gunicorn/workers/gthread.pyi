import socket
from _typeshed import Unused
from collections import deque
from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor
from selectors import DefaultSelector
from types import FrameType
from typing import Final

from gunicorn.config import Config
from gunicorn.glogging import Logger as GLogger
from gunicorn.http import Request, RequestParser
from gunicorn.http2.connection import HTTP2ServerConnection
from gunicorn.uwsgi.parser import UWSGIParser

from .._types import _AddressType
from . import base

DEFAULT_WORKER_DATA_TIMEOUT: Final = 5.0

class TConn:
    cfg: Config
    sock: socket.socket
    client: _AddressType
    server: _AddressType
    timeout: float | None
    parser: HTTP2ServerConnection | UWSGIParser | RequestParser | None
    initialized: bool
    is_http2: bool
    data_ready: bool

    def __init__(self, cfg: Config, sock: socket.socket, client: _AddressType, server: _AddressType) -> None: ...
    def init(self) -> None: ...
    def set_timeout(self) -> None: ...
    def wait_for_data(self, timeout: float | None) -> bool: ...
    def close(self) -> None: ...

class PollableMethodQueue:
    """
    Thread-safe queue that can wake up a selector.

    Uses a pipe to allow worker threads to signal the main thread
    when work is ready, enabling lock-free coordination.

    This approach is compatible with all POSIX systems including
    Linux, macOS, FreeBSD, OpenBSD, and NetBSD. The pipe is set to
    non-blocking mode to prevent worker threads from blocking if
    the pipe buffer fills up under extreme load.
    """
    def __init__(self) -> None: ...
    def init(self) -> None:
        """Initialize the pipe and queue."""
        ...
    def close(self) -> None:
        """Close the pipe file descriptors."""
        ...
    def fileno(self) -> int | None:
        """Return the readable file descriptor for selector registration."""
        ...
    # Actually, `*args` are expected to match the parameter types of `callback`.
    # Ideally this would be typed using ParamSpec as:
    # def defer(self, callback: Callable[_P, object], *args: _P.args) -> None
    def defer(self, callback: Callable[..., object], *args: object) -> None:
        """
        Queue a callback to be run on the main thread.

        The callback is added to the queue first, then a wake-up byte
        is written to the pipe. If the pipe write fails (buffer full),
        it's safe to ignore because the main thread will eventually
        drain the queue when it reads other wake-up bytes.
        """
        ...
    def run_callbacks(self, _fileobj: Unused, max_callbacks: int = 50) -> None:
        """
        Run queued callbacks. Called when the pipe is readable.

        Drains all available wake-up bytes and runs corresponding callbacks.
        The max_callbacks limit prevents starvation of other event sources.
        """
        ...

class ThreadWorker(base.Worker):
    worker_connections: int
    max_keepalived: int
    tpool: ThreadPoolExecutor
    poller: DefaultSelector
    method_queue: PollableMethodQueue
    keepalived_conns: deque[TConn]
    pending_conns: deque[TConn]
    nr_conns: int
    alive: bool

    @classmethod
    def check_config(cls, cfg: Config, log: GLogger) -> None: ...
    def init_process(self) -> None: ...
    def get_thread_pool(self) -> ThreadPoolExecutor: ...
    def handle_exit(self, sig: int, frame: FrameType | None) -> None: ...
    def handle_quit(self, sig: int, frame: FrameType | None) -> None: ...
    def set_accept_enabled(self, enabled: bool | None) -> None: ...
    def enqueue_req(self, conn: TConn) -> None: ...
    def accept(self, listener: socket.socket) -> None: ...
    def on_client_socket_readable(self, conn: TConn, client: socket.socket) -> None: ...
    def on_pending_socket_readable(self, conn: TConn, client: socket.socket) -> None: ...
    def murder_keepalived(self) -> None: ...
    def murder_pending(self) -> None: ...
    def is_parent_alive(self) -> bool: ...
    def wait_for_and_dispatch_events(self, timeout: float | None) -> None:
        """Wait for events and dispatch callbacks."""
        ...
    def run(self) -> None: ...
    def finish_request(self, conn: TConn, fs: Future[bool]) -> None:
        """Handle completion of a request (called via method_queue on main thread)."""
        ...
    def handle(self, conn: TConn) -> bool:
        """Handle a request on a connection. Runs in a worker thread."""
        ...
    def handle_http2(self, conn: TConn) -> bool:
        """
        Handle an HTTP/2 connection. Runs in a worker thread.

        HTTP/2 connections are persistent and multiplex multiple streams.
        We handle all streams until the connection is closed.

        Returns:
            False (HTTP/2 connections don't use keepalive polling)
        """
        ...
    def handle_http2_request(self, req: Request, conn: TConn, h2_conn: HTTP2ServerConnection) -> None:
        """Handle a single HTTP/2 request/stream."""
        ...
    def handle_request(self, req: Request, conn: TConn) -> bool: ...

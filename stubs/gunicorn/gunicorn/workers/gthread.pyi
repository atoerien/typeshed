import socket
from _typeshed import Unused
from collections import deque
from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor
from selectors import DefaultSelector
from types import FrameType

from gunicorn.config import Config
from gunicorn.glogging import Logger as GLogger
from gunicorn.http import Request, RequestParser
from gunicorn.http2.connection import HTTP2ServerConnection
from gunicorn.uwsgi.parser import UWSGIParser

from .._types import _AddressType
from . import base

class TConn:
    cfg: Config
    sock: socket.socket
    client: _AddressType
    server: _AddressType
    timeout: float | None
    parser: HTTP2ServerConnection | UWSGIParser | RequestParser | None
    initialized: bool
    is_http2: bool

    def __init__(self, cfg: Config, sock: socket.socket, client: _AddressType, server: _AddressType) -> None: ...
    def init(self) -> None: ...
    def set_timeout(self) -> None: ...
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
    nr_conns: int
    alive: bool

    @classmethod
    def check_config(cls, cfg: Config, log: GLogger) -> None: ...
    def init_process(self) -> None: ...
    def get_thread_pool(self) -> ThreadPoolExecutor:
        """Override this method to customize how the thread pool is created"""
        ...
    def handle_exit(self, sig: int, frame: FrameType | None) -> None:
        """Handle SIGTERM - begin graceful shutdown."""
        ...
    def handle_quit(self, sig: int, frame: FrameType | None) -> None:
        """Handle SIGQUIT - immediate shutdown."""
        ...
    def set_accept_enabled(self, enabled: bool | None) -> None:
        """Enable or disable accepting new connections."""
        ...
    def enqueue_req(self, conn: TConn) -> None:
        """Submit connection to thread pool for processing."""
        ...
    def accept(self, listener: socket.socket) -> None:
        """Accept a new connection from a listener socket."""
        ...
    def on_client_socket_readable(self, conn: TConn, client: socket.socket) -> None:
        """Handle a keepalive connection becoming readable."""
        ...
    def murder_keepalived(self) -> None:
        """Close expired keepalive connections."""
        ...
    def is_parent_alive(self) -> bool: ...
    def wait_for_and_dispatch_events(self, timeout: float | None) -> None:
        """Wait for events and dispatch callbacks."""
        ...
    def run(self) -> None: ...
    def finish_request(self, conn: TConn, fs: Future[bool]) -> None: ...
    def handle(self, conn: TConn) -> bool: ...
    def handle_http2(self, conn: TConn) -> bool: ...
    def handle_http2_request(self, req: Request, conn: TConn, h2_conn: HTTP2ServerConnection) -> None: ...
    def handle_request(self, req: Request, conn: TConn) -> bool: ...

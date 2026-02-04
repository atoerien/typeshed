"""
ASGI worker for gunicorn.

Provides native asyncio-based ASGI support using gunicorn's own
HTTP parsing infrastructure.
"""

from _typeshed import Incomplete
from asyncio.base_events import Server
from asyncio.events import AbstractEventLoop
from typing import NoReturn

from gunicorn.asgi.lifespan import LifespanManager
from gunicorn.config import Config
from gunicorn.glogging import Logger as GLogger
from gunicorn.workers import base

from .._types import _ASGIAppType

class ASGIWorker(base.Worker):
    """
    ASGI worker using asyncio event loop.

    Supports:
    - HTTP/1.1 with keepalive
    - WebSocket connections
    - Lifespan protocol (startup/shutdown hooks)
    - Optional uvloop for improved performance
    """
    worker_connections: int
    loop: AbstractEventLoop | None
    servers: list[Server]
    nr_conns: int
    lifespan: LifespanManager | None
    state: dict[Incomplete, Incomplete]
    asgi: _ASGIAppType

    @classmethod
    def check_config(cls, cfg: Config, log: GLogger) -> None:
        """Validate configuration for ASGI worker."""
        ...
    def init_process(self) -> None:
        """Initialize the worker process."""
        ...
    def load_wsgi(self) -> None:
        """Load the ASGI application."""
        ...
    def init_signals(self) -> None:
        """Initialize signal handlers for asyncio."""
        ...
    def handle_quit_signal(self) -> None:
        """Handle SIGQUIT/SIGINT - immediate shutdown."""
        ...
    def handle_exit_signal(self) -> None:
        """Handle SIGTERM - graceful shutdown."""
        ...
    def handle_usr1_signal(self) -> None:
        """Handle SIGUSR1 - reopen log files."""
        ...
    def handle_winch_signal(self) -> None:
        """Handle SIGWINCH - ignored in worker."""
        ...
    def handle_abort_signal(self) -> NoReturn:
        """Handle SIGABRT - abort."""
        ...
    def run(self) -> None:
        """Main entry point for the worker."""
        ...

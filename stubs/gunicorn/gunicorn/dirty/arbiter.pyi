"""
Dirty Arbiter Process

Asyncio-based arbiter that manages the dirty worker pool and routes
requests from HTTP workers to available dirty workers.
"""

import asyncio
from _typeshed import Incomplete
from asyncio import StreamReader, StreamWriter
from signal import Signals
from typing import ClassVar

from gunicorn.config import Config
from gunicorn.dirty.worker import DirtyWorker
from gunicorn.glogging import Logger as GLogger

class DirtyArbiter:
    """
    Dirty arbiter that manages the dirty worker pool.

    The arbiter runs an asyncio event loop and handles:
    - Spawning and managing dirty worker processes
    - Accepting connections from HTTP workers
    - Routing requests to available dirty workers
    - Monitoring worker health via heartbeat
    """
    SIGNALS: ClassVar[list[Signals]]
    WORKER_BOOT_ERROR: ClassVar[int]
    cfg: Config
    log: GLogger
    pid: int | None
    ppid: int
    pidfile: str | None
    tmpdir: str
    socket_path: str
    workers: dict[int, DirtyWorker]
    worker_sockets: dict[int, str]
    worker_connections: dict[int, tuple[Incomplete, Incomplete]]
    worker_queues: dict[int, asyncio.Queue[Incomplete]]
    worker_consumers: dict[int, asyncio.Task[None]]
    worker_age: int
    alive: bool
    app_specs: dict[str, dict[Incomplete, Incomplete]]
    app_worker_map: dict[str, set[Incomplete]]
    worker_app_map: dict[int, list[Incomplete]]

    def __init__(self, cfg: Config, log: GLogger, socket_path: str | None = None, pidfile: str | None = None) -> None:
        """
        Initialize the dirty arbiter.

        Args:
            cfg: Gunicorn config
            log: Logger
            socket_path: Path to the arbiter's Unix socket
            pidfile: Well-known PID file location for orphan detection
        """
        ...
    def run(self) -> None:
        """Run the dirty arbiter (blocking call)."""
        ...
    def init_signals(self) -> None:
        """Set up signal handlers."""
        ...
    async def handle_client(self, reader: StreamReader, writer: StreamWriter) -> None:
        """
        Handle a connection from an HTTP worker.

        Routes requests to available dirty workers and returns responses.
        Supports both regular responses and streaming (chunk-based) responses.
        """
        ...
    async def route_request(self, request: dict[str, Incomplete], client_writer: StreamWriter) -> None:
        """
        Route a request to an available dirty worker via queue.

        Each worker has a dedicated queue and consumer task. Requests are
        submitted to the queue and processed sequentially by the consumer.

        For streaming responses, messages (chunks) are forwarded directly
        to the client_writer as they arrive from the worker.

        Args:
            request: Request message dict
            client_writer: StreamWriter to send responses to client
        """
        ...
    async def manage_workers(self) -> None:
        """Maintain the number of dirty workers."""
        ...
    def spawn_worker(self) -> int | None:
        """
        Spawn a new dirty worker.

        Worker app assignment follows these priorities:
        1. If there are pending respawns (from dead workers), use those apps
        2. Otherwise, determine apps for a new worker based on allocation

        Returns:
            Worker PID in parent process, or None if no apps need workers
        """
        ...
    def kill_worker(self, pid: int, sig: int) -> None:
        """Kill a worker by PID."""
        ...
    async def murder_workers(self) -> None:
        """Kill workers that have timed out."""
        ...
    def reap_workers(self) -> None:
        """Reap dead worker processes."""
        ...
    async def reload(self) -> None:
        """Reload workers (SIGHUP handling)."""
        ...
    async def stop(self, graceful: bool = True) -> None:
        """Stop all workers."""
        ...

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
    num_workers: int
    app_specs: dict[str, dict[Incomplete, Incomplete]]
    app_worker_map: dict[str, set[Incomplete]]
    worker_app_map: dict[int, list[Incomplete]]
    stash_tables: dict[str, dict[Incomplete, Incomplete]]

    def __init__(self, cfg: Config, log: GLogger, socket_path: str | None = None, pidfile: str | None = None) -> None: ...
    def run(self) -> None: ...
    def init_signals(self) -> None: ...
    async def handle_client(self, reader: StreamReader, writer: StreamWriter) -> None: ...
    async def route_request(self, request: dict[str, Incomplete], client_writer: StreamWriter) -> None: ...
    async def handle_status_request(self, message: dict[str, Incomplete], client_writer: StreamWriter) -> None: ...
    async def handle_manage_request(self, message: dict[str, Incomplete], client_writer: StreamWriter) -> None: ...
    async def handle_stash_request(self, message: dict[str, Incomplete], client_writer: StreamWriter) -> None: ...
    async def manage_workers(self) -> None: ...
    def spawn_worker(self, force_all_apps: bool = False) -> int | None: ...
    def kill_worker(self, pid: int, sig: int) -> None: ...
    async def murder_workers(self) -> None: ...
    def reap_workers(self) -> None: ...
    async def reload(self) -> None: ...
    async def stop(self, graceful: bool = True) -> None: ...

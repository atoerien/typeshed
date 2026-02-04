from queue import SimpleQueue
from types import FrameType
from typing import ClassVar

from gunicorn.app.base import BaseApplication
from gunicorn.config import Config
from gunicorn.dirty import DirtyArbiter
from gunicorn.glogging import Logger as GLogger
from gunicorn.sock import BaseSocket
from gunicorn.workers.base import Worker

from ._types import _AddressType
from .pidfile import Pidfile

class Arbiter:
    """
    Arbiter maintain the workers processes alive. It launches or
    kills them if needed. It also manages application reloading
    via SIGHUP/USR2.
    """
    WORKER_BOOT_ERROR: ClassVar[int]
    APP_LOAD_ERROR: ClassVar[int]
    START_CTX: ClassVar[dict[int | str, str | list[str]]]
    LISTENERS: ClassVar[list[BaseSocket]]
    WORKERS: ClassVar[dict[int, Worker]]
    WAKEUP_REQUEST: ClassVar[int]
    SIGNALS: ClassVar[list[int]]
    SIG_NAMES: ClassVar[dict[int, str]]
    log: GLogger | None
    SIG_QUEUE: SimpleQueue[int]
    pidfile: Pidfile | None
    systemd: bool
    worker_age: int
    reexec_pid: int
    master_pid: int
    master_name: str
    dirty_arbiter_pid: int
    dirty_arbiter: DirtyArbiter | None
    dirty_pidfile: str | None
    pid: int
    app: BaseApplication
    cfg: Config
    worker_class: type[Worker]
    address: list[_AddressType]
    timeout: int
    proc_name: str
    num_workers: int

    def __init__(self, app: BaseApplication) -> None: ...
    def setup(self, app: BaseApplication) -> None: ...
    def start(self) -> None:
        """
        Initialize the arbiter. Start listening and set pidfile if needed.
        
        """
        ...
    def init_signals(self) -> None:
        """
        Initialize master signal handling. Most of the signals
        are queued. Child signals only wake up the master.
        """
        ...
    def signal(self, sig: int, frame: FrameType | None) -> None:
        """Signal handler - NO LOGGING, just queue the signal."""
        ...
    def run(self) -> None:
        """Main master loop."""
        ...
    def signal_chld(self, sig: int, frame: FrameType | None) -> None:
        """SIGCHLD signal handler - NO LOGGING, just queue the signal."""
        ...
    def handle_chld(self) -> None:
        """SIGCHLD handling - called from main loop, safe to log."""
        ...
    handle_cld = handle_chld
    def handle_hup(self) -> None:
        """
        HUP handling.
        - Reload configuration
        - Start the new worker processes with a new configuration
        - Gracefully shutdown the old worker processes
        """
        ...
    def handle_term(self) -> None:
        """SIGTERM handling"""
        ...
    def handle_int(self) -> None:
        """SIGINT handling"""
        ...
    def handle_quit(self) -> None:
        """SIGQUIT handling"""
        ...
    def handle_ttin(self) -> None:
        """
        SIGTTIN handling.
        Increases the number of workers by one.
        """
        ...
    def handle_ttou(self) -> None:
        """
        SIGTTOU handling.
        Decreases the number of workers by one.
        """
        ...
    def handle_usr1(self) -> None:
        """
        SIGUSR1 handling.
        Kill all workers by sending them a SIGUSR1
        """
        ...
    def handle_usr2(self) -> None:
        """
        SIGUSR2 handling.
        Creates a new arbiter/worker set as a fork of the current
        arbiter without affecting old workers. Use this to do live
        deployment with the ability to backout a change.
        """
        ...
    def handle_winch(self) -> None:
        """SIGWINCH handling"""
        ...
    def maybe_promote_master(self) -> None: ...
    def wakeup(self) -> None:
        """Wake up the arbiter's main loop."""
        ...
    def halt(self, reason: str | None = None, exit_status: int = 0) -> None:
        """halt arbiter """
        ...
    def wait_for_signals(self, timeout: float | None = 1.0) -> list[int]:
        """
        Wait for signals with timeout.
        Returns a list of signals that were received.
        """
        ...
    def stop(self, graceful: bool = True) -> None:
        """
        Stop workers

        :attr graceful: boolean, If True (the default) workers will be
        killed gracefully  (ie. trying to wait for the current connection)
        """
        ...
    def reexec(self) -> None:
        """
        Relaunch the master and workers.
        
        """
        ...
    def reload(self) -> None: ...
    def murder_workers(self) -> None:
        """
        Kill unused/idle workers
        
        """
        ...
    def reap_workers(self) -> None:
        """
        Reap workers to avoid zombie processes
        
        """
        ...
    def manage_workers(self) -> None:
        """
        Maintain the number of workers by spawning or killing
        as required.
        """
        ...
    def spawn_worker(self) -> int: ...
    def spawn_workers(self) -> None:
        """
        Spawn new workers as needed.

        This is where a worker process leaves the main loop
        of the master process.
        """
        ...
    def kill_workers(self, sig: int) -> None:
        """
        Kill all workers with the signal `sig`
        :attr sig: `signal.SIG*` value
        """
        ...
    def kill_worker(self, pid: int, sig: int) -> None:
        """
        Kill a worker

        :attr pid: int, worker pid
        :attr sig: `signal.SIG*` value
 
        """
        ...
    def spawn_dirty_arbiter(self) -> int | None:
        """
        Spawn the dirty arbiter process.

        The dirty arbiter manages a separate pool of workers for
        long-running, blocking operations.
        """
        ...
    def kill_dirty_arbiter(self, sig: int) -> None:
        """
        Send a signal to the dirty arbiter.

        :attr sig: `signal.SIG*` value
        """
        ...
    def reap_dirty_arbiter(self) -> None:
        """
        Reap the dirty arbiter process if it has exited.
        
        """
        ...
    def manage_dirty_arbiter(self) -> None:
        """
        Maintain the dirty arbiter process by respawning if needed.
        
        """
        ...

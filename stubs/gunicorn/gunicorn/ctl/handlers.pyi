"""
Control Interface Command Handlers

Provides handlers for all control commands with access to arbiter state.
"""

from _typeshed import Incomplete
from typing import Literal, TypedDict, type_check_only
from typing_extensions import NotRequired

from gunicorn.arbiter import Arbiter

@type_check_only
class _Worker(TypedDict):
    pid: int
    age: int
    booted: bool
    last_heartbeat: float
    aborted: NotRequired[bool]
    apps: NotRequired[list[str]]

@type_check_only
class _ShowWorkersReturnType(TypedDict):
    workers: list[_Worker]
    count: int

@type_check_only
class _App(TypedDict):
    import_path: str
    worker_count: int | None
    current_workers: int
    worker_pids: list[int]

@type_check_only
class _ShowDirtyReturnType(TypedDict):
    enabled: bool
    pid: int | None
    workers: list[_Worker]
    apps: list[_App]

@type_check_only
class _ShowStatsReturnType(TypedDict):
    uptime: float | None
    pid: int
    workers_current: int
    workers_target: int
    workers_spawned: int
    workers_killed: int
    reloads: int
    dirty_arbiter_pid: int | None

@type_check_only
class _ListenerInfo(TypedDict):
    address: str
    fd: int
    type: Literal["unix", "tcp", "tcp6", "unknown"]

@type_check_only
class _ShowListenersReturnType(TypedDict):
    listeners: list[_ListenerInfo]
    count: int

@type_check_only
class _WorkerAddReturnType(TypedDict):
    added: int
    previous: int
    total: int

@type_check_only
class _WorkerRemovedReturnType(TypedDict):
    removed: int
    previous: int
    total: int

@type_check_only
class _WorkerKillSucessReturnType(TypedDict):
    success: Literal[True]
    killed: int

@type_check_only
class _WorkerKillFailedReturnType(TypedDict):
    success: Literal[False]
    error: str

@type_check_only
class _ReloadReturnType(TypedDict):
    status: Literal["reloading"]

@type_check_only
class _ReopenReturnType(TypedDict):
    status: Literal["reopening"]

@type_check_only
class _ShutdownReturnType(TypedDict):
    status: Literal["shutting_down"]
    mode: str

@type_check_only
class _HelpReturnType(TypedDict):
    commands: dict[str, str]

class CommandHandlers:
    """
    Command handlers with access to arbiter state.

    All handler methods return dictionaries that will be sent
    as the response data.
    """
    arbiter: Arbiter
    def __init__(self, arbiter: Arbiter) -> None:
        """
        Initialize handlers with arbiter reference.

        Args:
            arbiter: The Gunicorn arbiter instance
        """
        ...
    def show_workers(self) -> _ShowWorkersReturnType:
        """
        Return list of HTTP workers.

        Returns:
            Dictionary with workers list containing:
            - pid: Worker process ID
            - age: Worker age (spawn order)
            - requests: Number of requests handled (if available)
            - booted: Whether worker has finished booting
            - last_heartbeat: Seconds since last heartbeat
        """
        ...
    def show_dirty(self) -> _ShowDirtyReturnType:
        """
        Return dirty workers and apps information.

        Returns:
            Dictionary with:
            - enabled: Whether dirty arbiter is running
            - pid: Dirty arbiter PID
            - workers: List of dirty worker info
            - apps: List of dirty app specs
        """
        ...
    def show_config(self) -> dict[str, Incomplete]:
        """
        Return current effective configuration.

        Returns:
            Dictionary of configuration values
        """
        ...
    def show_stats(self) -> _ShowStatsReturnType:
        """
        Return server statistics.

        Returns:
            Dictionary with:
            - uptime: Seconds since arbiter started
            - pid: Arbiter PID
            - workers_current: Current number of workers
            - workers_spawned: Total workers spawned
            - workers_killed: Total workers killed (if tracked)
            - reloads: Number of reloads (if tracked)
        """
        ...
    def show_listeners(self) -> _ShowListenersReturnType:
        """
        Return bound socket information.

        Returns:
            Dictionary with listeners list
        """
        ...
    def worker_add(self, count: int = 1) -> _WorkerAddReturnType:
        """
        Increase worker count.

        Args:
            count: Number of workers to add (default 1)

        Returns:
            Dictionary with added count and new total
        """
        ...
    def worker_remove(self, count: int = 1) -> _WorkerRemovedReturnType:
        """
        Decrease worker count.

        Args:
            count: Number of workers to remove (default 1)

        Returns:
            Dictionary with removed count and new total
        """
        ...
    def worker_kill(self, pid: int) -> _WorkerKillSucessReturnType | _WorkerKillFailedReturnType:
        """
        Gracefully terminate a specific worker.

        Args:
            pid: Worker process ID

        Returns:
            Dictionary with killed PID or error
        """
        ...
    def dirty_add(self, count: int = 1) -> dict[str, Incomplete]:
        """
        Spawn additional dirty workers.

        Sends a MANAGE message to the dirty arbiter to spawn workers.

        Args:
            count: Number of dirty workers to add (default 1)

        Returns:
            Dictionary with added count or error
        """
        ...
    def dirty_remove(self, count: int = 1) -> dict[str, Incomplete]:
        """
        Remove dirty workers.

        Sends a MANAGE message to the dirty arbiter to remove workers.

        Args:
            count: Number of dirty workers to remove (default 1)

        Returns:
            Dictionary with removed count or error
        """
        ...
    def reload(self) -> _ReloadReturnType:
        """
        Trigger graceful reload (equivalent to SIGHUP).

        Returns:
            Dictionary with status
        """
        ...
    def reopen(self) -> _ReopenReturnType:
        """
        Reopen log files (equivalent to SIGUSR1).

        Returns:
            Dictionary with status
        """
        ...
    def shutdown(self, mode: str = "graceful") -> _ShutdownReturnType:
        """
        Initiate shutdown.

        Args:
            mode: "graceful" (SIGTERM) or "quick" (SIGINT)

        Returns:
            Dictionary with status
        """
        ...
    def show_all(self) -> dict[str, Incomplete]:
        """
        Return overview of all processes (arbiter, web workers, dirty arbiter, dirty workers).

        Returns:
            Dictionary with complete process hierarchy
        """
        ...
    def help(self) -> _HelpReturnType:
        """
        Return list of available commands.

        Returns:
            Dictionary with commands and descriptions
        """
        ...

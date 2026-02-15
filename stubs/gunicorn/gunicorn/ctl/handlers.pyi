"""
Control Interface Command Handlers

Provides handlers for all control commands with access to arbiter state.
"""

from _typeshed import Incomplete

from gunicorn.arbiter import Arbiter

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
    # TODO: Use TypedDict for next return types
    def show_workers(self) -> dict[str, Incomplete]:
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
    def show_dirty(self) -> dict[str, Incomplete]:
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
    def show_stats(self) -> dict[str, Incomplete]:
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
    def show_listeners(self) -> dict[str, Incomplete]:
        """
        Return bound socket information.

        Returns:
            Dictionary with listeners list
        """
        ...
    def worker_add(self, count: int = 1) -> dict[str, Incomplete]:
        """
        Increase worker count.

        Args:
            count: Number of workers to add (default 1)

        Returns:
            Dictionary with added count and new total
        """
        ...
    def worker_remove(self, count: int = 1) -> dict[str, Incomplete]:
        """
        Decrease worker count.

        Args:
            count: Number of workers to remove (default 1)

        Returns:
            Dictionary with removed count and new total
        """
        ...
    def worker_kill(self, pid: int) -> dict[str, Incomplete]:
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
    def reload(self) -> dict[str, Incomplete]:
        """
        Trigger graceful reload (equivalent to SIGHUP).

        Returns:
            Dictionary with status
        """
        ...
    def reopen(self) -> dict[str, Incomplete]:
        """
        Reopen log files (equivalent to SIGUSR1).

        Returns:
            Dictionary with status
        """
        ...
    def shutdown(self, mode: str = "graceful") -> dict[str, Incomplete]:
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
    def help(self) -> dict[str, Incomplete]:
        """
        Return list of available commands.

        Returns:
            Dictionary with commands and descriptions
        """
        ...

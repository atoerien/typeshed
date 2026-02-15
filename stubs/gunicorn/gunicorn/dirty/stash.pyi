"""
Stash - Global Shared State for Dirty Workers

Provides simple key-value tables stored in the arbiter process.
All workers can read and write to the same tables.

Usage::

    from gunicorn.dirty import stash

    # Basic operations - table is auto-created on first access
    stash.put("sessions", "user:1", {"name": "Alice", "role": "admin"})
    user = stash.get("sessions", "user:1")
    stash.delete("sessions", "user:1")

    # Dict-like interface
    sessions = stash.table("sessions")
    sessions["user:1"] = {"name": "Alice"}
    user = sessions["user:1"]
    del sessions["user:1"]

    # Query operations
    keys = stash.keys("sessions")
    keys = stash.keys("sessions", pattern="user:*")

    # Table management
    stash.ensure("cache")           # Explicit creation (idempotent)
    stash.clear("sessions")         # Delete all entries
    stash.delete_table("sessions")  # Delete the table itself
    tables = stash.tables()         # List all tables

Declarative usage in DirtyApp::

    class MyApp(DirtyApp):
        stashes = ["sessions", "cache"]  # Auto-created on arbiter start

        def __call__(self, action, *args, **kwargs):
            # Tables are ready to use
            stash.put("sessions", "key", "value")

Note: Tables are stored in the arbiter process and are ephemeral.
If the arbiter restarts, all data is lost.
"""

from _typeshed import Incomplete
from collections.abc import Iterator
from types import TracebackType
from typing_extensions import Self

from .errors import DirtyError

class StashError(DirtyError):
    """Base exception for stash operations."""
    ...

class StashTableNotFoundError(StashError):
    """Raised when a table does not exist."""
    table_name: str

    def __init__(self, table_name: str) -> None: ...

class StashKeyNotFoundError(StashError):
    """Raised when a key does not exist in a table."""
    table_name: str
    key: str

    def __init__(self, table_name: str, key: str) -> None: ...

class StashClient:
    """
    Client for stash operations.

    Communicates with the arbiter which stores all tables in memory.
    """
    socket_path: str
    timeout: float

    def __init__(self, socket_path: str, timeout: float = 30.0) -> None:
        """
        Initialize the stash client.

        Args:
            socket_path: Path to the dirty arbiter's Unix socket
            timeout: Default timeout for operations in seconds
        """
        ...
    def put(self, table: str, key: str, value) -> None:
        """
        Store a value in a table.

        The table is automatically created if it doesn't exist.

        Args:
            table: Table name
            key: Key to store under
            value: Value to store (must be serializable)
        """
        ...
    def get(self, table: str, key: str, default=None):
        """
        Retrieve a value from a table.

        Args:
            table: Table name
            key: Key to retrieve
            default: Default value if key not found

        Returns:
            The stored value, or default if not found
        """
        ...
    def delete(self, table: str, key: str) -> bool:
        """
        Delete a key from a table.

        Args:
            table: Table name
            key: Key to delete

        Returns:
            True if key was deleted, False if it didn't exist
        """
        ...
    def keys(self, table: str, pattern: str | None = None) -> list[str]:
        """
        Get all keys in a table, optionally filtered by pattern.

        Args:
            table: Table name
            pattern: Optional glob pattern (e.g., "user:*")

        Returns:
            List of keys
        """
        ...
    def clear(self, table: str) -> None:
        """
        Delete all entries in a table.

        Args:
            table: Table name
        """
        ...
    def info(self, table: str) -> dict[str, Incomplete]:
        """
        Get information about a table.

        Args:
            table: Table name

        Returns:
            Dict with table info (size, etc.)
        """
        ...
    def ensure(self, table: str) -> None:
        """
        Ensure a table exists (create if not exists).

        This is idempotent - calling it multiple times is safe.

        Args:
            table: Table name
        """
        ...
    def exists(self, table: str, key=None) -> bool:
        """
        Check if a table or key exists.

        Args:
            table: Table name
            key: Optional key to check within the table

        Returns:
            True if exists, False otherwise
        """
        ...
    def delete_table(self, table: str) -> None:
        """
        Delete an entire table.

        Args:
            table: Table name
        """
        ...
    def tables(self) -> list[str]:
        """
        List all tables.

        Returns:
            List of table names
        """
        ...
    def table(self, name: str) -> StashTable:
        """
        Get a dict-like interface to a table.

        Args:
            name: Table name

        Returns:
            StashTable instance
        """
        ...
    def close(self) -> None:
        """Close the client connection."""
        ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...

class StashTable:
    """
    Dict-like interface to a stash table.

    Example::

        sessions = stash.table("sessions")
        sessions["user:1"] = {"name": "Alice"}
        user = sessions["user:1"]
        del sessions["user:1"]

        # Iteration
        for key in sessions:
            print(key, sessions[key])
    """
    def __init__(self, client: StashClient, name: str) -> None: ...
    @property
    def name(self) -> str:
        """Table name."""
        ...
    def __getitem__(self, key: str): ...
    def __setitem__(self, key: str, value) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __contains__(self, key: str) -> bool: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def get(self, key: str, default=None):
        """Get value with default."""
        ...
    def keys(self, pattern: str | None = None) -> list[str]:
        """Get all keys, optionally filtered by pattern."""
        ...
    def clear(self) -> None:
        """Delete all entries."""
        ...
    def items(self) -> Iterator[tuple[Incomplete, Incomplete]]:
        """Iterate over (key, value) pairs."""
        ...
    def values(self) -> Iterator[Incomplete]:
        """Iterate over values."""
        ...

def set_stash_socket_path(path: str) -> None:
    """Set the global stash socket path (called during initialization)."""
    ...
def get_stash_socket_path() -> str:
    """Get the stash socket path."""
    ...
def put(table: str, key: str, value) -> None:
    """Store a value in a table."""
    ...
def get(table: str, key: str, default=None):
    """Retrieve a value from a table."""
    ...
def delete(table: str, key: str) -> bool:
    """Delete a key from a table."""
    ...
def keys(table: str, pattern: str | None = None) -> list[str]:
    """Get all keys in a table."""
    ...
def clear(table: str) -> None:
    """Delete all entries in a table."""
    ...
def info(table: str) -> dict[str, Incomplete]:
    """Get information about a table."""
    ...
def ensure(table: str) -> None:
    """Ensure a table exists."""
    ...
def exists(table: str, key: str | None = None) -> bool:
    """Check if a table or key exists."""
    ...
def delete_table(table: str) -> None:
    """Delete an entire table."""
    ...
def tables() -> list[str]:
    """List all tables."""
    ...
def table(name: str) -> StashTable:
    """Get a dict-like interface to a table."""
    ...

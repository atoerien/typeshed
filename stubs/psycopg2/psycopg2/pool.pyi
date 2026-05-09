"""
Connection pooling for psycopg2

This module implements thread-safe (and not) connection pools.
"""

from _typeshed import ConvertibleToInt
from collections.abc import Hashable

import psycopg2
from psycopg2.extensions import connection

class PoolError(psycopg2.Error): ...

class AbstractConnectionPool:
    """Generic key-based pooling code."""
    minconn: int
    maxconn: int
    closed: bool
    def __init__(self, minconn: ConvertibleToInt, maxconn: ConvertibleToInt, *args, **kwargs) -> None:
        """
        Initialize the connection pool.

        New 'minconn' connections are created immediately calling 'connfunc'
        with given parameters. The connection pool will support a maximum of
        about 'maxconn' connections.
        """
        ...
    # getconn, putconn and closeall are officially documented as methods of the
    # abstract base class, but in reality, they only exist on the children classes
    def getconn(self, key: Hashable | None = None) -> connection: ...
    def putconn(self, conn: connection, key: Hashable | None = None, close: bool = False) -> None: ...
    def closeall(self) -> None: ...

class SimpleConnectionPool(AbstractConnectionPool):
    """A connection pool that can't be shared across different threads."""
    ...

class ThreadedConnectionPool(AbstractConnectionPool):
    """A connection pool that works with the threading module."""
    # This subclass has a default value for conn which doesn't exist
    # in the SimpleConnectionPool class, nor in the documentation
    def putconn(self, conn: connection | None = None, key: Hashable | None = None, close: bool = False) -> None:
        """Put away an unused connection."""
        ...

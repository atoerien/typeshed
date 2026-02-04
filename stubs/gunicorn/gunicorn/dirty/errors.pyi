"""
Dirty Arbiters Error Classes

Exception hierarchy for dirty worker pool operations.
"""

from _typeshed import Incomplete
from typing import TypedDict, type_check_only

@type_check_only
class _DirtyErrorDict(TypedDict):
    error_type: str
    message: str
    details: dict[str, Incomplete]

class DirtyError(Exception):
    """Base exception for all dirty arbiter errors."""
    message: str
    details: dict[str, Incomplete]

    def __init__(self, message: str, details: dict[str, Incomplete] | None = None) -> None: ...
    def to_dict(self) -> _DirtyErrorDict:
        """Serialize error for protocol transmission."""
        ...
    @classmethod
    def from_dict(cls, data: dict[str, Incomplete]) -> DirtyError:
        """
        Deserialize error from protocol transmission.

        Creates an error instance from a serialized dict. The returned
        error will be an instance of the appropriate subclass based on
        the error_type field, but constructed using the base DirtyError
        __init__ to preserve all details.
        """
        ...

class DirtyTimeoutError(DirtyError):
    """Raised when a dirty operation times out."""
    timeout: float | None

    def __init__(self, message: str = "Operation timed out", timeout: float | None = None) -> None: ...

class DirtyConnectionError(DirtyError):
    """Raised when connection to dirty arbiter fails."""
    socket_path: str | None

    def __init__(self, message: str = "Connection failed", socket_path: str | None = None) -> None: ...

class DirtyWorkerError(DirtyError):
    """Raised when a dirty worker encounters an error."""
    worker_id: int | None
    traceback: str | None

    def __init__(self, message: str, worker_id: int | None = None, traceback: str | None = None) -> None: ...

class DirtyAppError(DirtyError):
    """Raised when a dirty app encounters an error during execution."""
    app_path: str | None
    action: str | None
    traceback: str | None

    def __init__(
        self, message: str, app_path: str | None = None, action: str | None = None, traceback: str | None = None
    ) -> None: ...

class DirtyAppNotFoundError(DirtyAppError):
    """Raised when a dirty app is not found."""
    app_path: str

    def __init__(self, app_path: str) -> None: ...

class DirtyNoWorkersAvailableError(DirtyError):
    """
    Raised when no workers are available for the requested app.

    This exception is raised when a request targets an app that has
    worker limits configured, and no workers with that app are currently
    available (e.g., all workers for that app crashed and haven't been
    respawned yet).

    Web applications can catch this exception to provide graceful
    degradation, such as queuing requests for retry or showing a
    maintenance page.

    Example::

        from gunicorn.dirty import get_dirty_client
        from gunicorn.dirty.errors import DirtyNoWorkersAvailableError

        def my_view(request):
            client = get_dirty_client()
            try:
                result = client.execute("myapp.ml:HeavyModel", "predict", data)
            except DirtyNoWorkersAvailableError as e:
                return {"error": "Service temporarily unavailable",
                        "app": e.app_path}
    """
    app_path: str

    def __init__(self, app_path: str, message: str | None = None) -> None: ...

class DirtyProtocolError(DirtyError):
    """Raised when there is a protocol-level error."""
    def __init__(self, message: str = "Protocol error", raw_data: str | bytes | None = None) -> None: ...

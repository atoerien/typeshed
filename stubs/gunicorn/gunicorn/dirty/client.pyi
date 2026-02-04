"""
Dirty Client

Client for HTTP workers to communicate with the dirty worker pool.
Provides both sync and async APIs.
"""

from _typeshed import Incomplete
from types import TracebackType
from typing import Any, ClassVar
from typing_extensions import Self

class DirtyClient:
    """
    Client for calling dirty workers from HTTP workers.

    Provides both sync and async APIs. The sync API is for traditional
    sync workers (sync, gthread), while the async API is for async
    workers (asgi, gevent, eventlet).
    """
    socket_path: str
    timeout: float

    def __init__(self, socket_path: str, timeout: float = 30.0) -> None:
        """
        Initialize the dirty client.

        Args:
            socket_path: Path to the dirty arbiter's Unix socket
            timeout: Default timeout for operations in seconds
        """
        ...
    def connect(self) -> None:
        """
        Establish sync socket connection to arbiter.

        Raises:
            DirtyConnectionError: If connection fails
        """
        ...
    # Arguments and result depend on app path and method name passed to action
    def execute(self, app_path: str, action: str, *args: Any, **kwargs: Any) -> Any:
        """
        Execute an action on a dirty app (sync/blocking).

        Args:
            app_path: Import path of the dirty app (e.g., 'myapp.ml:MLApp')
            action: Action to call on the app
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Result from the dirty app action

        Raises:
            DirtyConnectionError: If connection fails
            DirtyTimeoutError: If operation times out
            DirtyError: If execution fails
        """
        ...
    def stream(self, app_path: str, action: str, *args: Any, **kwargs: Any) -> DirtyStreamIterator:
        """
        Stream results from a dirty app action (sync).

        This method returns an iterator that yields chunks from a streaming
        response. Use this for actions that return generators.

        Args:
            app_path: Import path of the dirty app (e.g., 'myapp.ml:MLApp')
            action: Action to call on the app
            *args: Positional arguments
            **kwargs: Keyword arguments

        Yields:
            Chunks of data from the streaming response

        Raises:
            DirtyConnectionError: If connection fails
            DirtyTimeoutError: If operation times out
            DirtyError: If execution fails

        Example::

            for chunk in client.stream("myapp.llm:LLMApp", "generate", prompt):
                print(chunk, end="", flush=True)
        """
        ...
    def close(self) -> None:
        """Close the sync connection."""
        ...
    async def connect_async(self) -> None:
        """
        Establish async connection to arbiter.

        Raises:
            DirtyConnectionError: If connection fails
        """
        ...
    async def execute_async(self, app_path: str, action: str, *args: Any, **kwargs: Any) -> Any:
        """
        Execute an action on a dirty app (async/non-blocking).

        Args:
            app_path: Import path of the dirty app
            action: Action to call on the app
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Result from the dirty app action

        Raises:
            DirtyConnectionError: If connection fails
            DirtyTimeoutError: If operation times out
            DirtyError: If execution fails
        """
        ...
    def stream_async(self, app_path: str, action: str, *args: Any, **kwargs: Any) -> DirtyAsyncStreamIterator:
        """
        Stream results from a dirty app action (async).

        This method returns an async iterator that yields chunks from a
        streaming response. Use this for actions that return generators.

        Args:
            app_path: Import path of the dirty app (e.g., 'myapp.ml:MLApp')
            action: Action to call on the app
            *args: Positional arguments
            **kwargs: Keyword arguments

        Yields:
            Chunks of data from the streaming response

        Raises:
            DirtyConnectionError: If connection fails
            DirtyTimeoutError: If operation times out
            DirtyError: If execution fails

        Example::

            async for chunk in client.stream_async("myapp.llm:LLMApp", "generate", prompt):
                await response.write(chunk)
        """
        ...
    async def close_async(self) -> None:
        """Close the async connection."""
        ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...
    async def __aenter__(self) -> Self: ...
    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...

class DirtyStreamIterator:
    """
    Iterator for streaming responses from dirty workers (sync).

    This class is returned by `DirtyClient.stream()` and yields chunks
    from a streaming response until the end message is received.

    Uses a deadline-based timeout approach:
    - Total stream timeout: limits entire stream duration
    - Idle timeout: limits gap between chunks (defaults to total timeout)
    """
    DEFAULT_IDLE_TIMEOUT: ClassVar[float]
    client: DirtyClient
    app_path: str
    action: str
    args: tuple[Incomplete, ...]
    kwargs: dict[str, Incomplete]

    def __init__(
        self,
        client: DirtyClient,
        app_path: str,
        action: str,
        args: tuple[Incomplete, ...],
        kwargs: dict[str, Incomplete],
        idle_timeout: float | None = None,
    ) -> None: ...
    def __iter__(self) -> Self: ...
    def __next__(self) -> Incomplete | None: ...

class DirtyAsyncStreamIterator:
    """
    Async iterator for streaming responses from dirty workers.

    This class is returned by `DirtyClient.stream_async()` and yields chunks
    from a streaming response until the end message is received.

    Uses a deadline-based timeout approach for efficiency:
    - Total stream timeout: limits entire stream duration
    - Idle timeout: limits gap between chunks (defaults to total timeout)

    This avoids the overhead of asyncio.wait_for() on every chunk read.
    """
    DEFAULT_IDLE_TIMEOUT: ClassVar[float]
    client: DirtyClient
    app_path: str
    action: str
    args: tuple[Incomplete, ...]
    kwargs: dict[str, Incomplete]

    def __init__(
        self,
        client: DirtyClient,
        app_path: str,
        action: str,
        args: tuple[Incomplete, ...],
        kwargs: dict[str, Incomplete],
        idle_timeout: float | None = None,
    ) -> None: ...
    def __aiter__(self) -> Self: ...
    async def __anext__(self) -> Incomplete | None: ...

def set_dirty_socket_path(path: str) -> None:
    """Set the global dirty socket path (called during initialization)."""
    ...
def get_dirty_socket_path() -> str:
    """Get the dirty socket path."""
    ...
def get_dirty_client(timeout: float = 30.0) -> DirtyClient:
    """
    Get or create a thread-local sync client.

    This is the recommended way to get a client in sync HTTP workers.

    Args:
        timeout: Timeout for operations in seconds

    Returns:
        DirtyClient: Thread-local client instance

    Example::

        from gunicorn.dirty import get_dirty_client

        def my_view(request):
            client = get_dirty_client()
            result = client.execute("myapp.ml:MLApp", "inference", data)
            return result
    """
    ...
async def get_dirty_client_async(timeout: float = 30.0) -> DirtyClient:
    """
    Get or create a context-local async client.

    This is the recommended way to get a client in async HTTP workers.

    Args:
        timeout: Timeout for operations in seconds

    Returns:
        DirtyClient: Context-local client instance

    Example::

        from gunicorn.dirty import get_dirty_client_async

        async def my_view(request):
            client = await get_dirty_client_async()
            result = await client.execute_async("myapp.ml:MLApp", "inference", data)
            return result
    """
    ...
def close_dirty_client() -> None:
    """Close the thread-local client (call on worker exit)."""
    ...
async def close_dirty_client_async() -> None:
    """Close the context-local async client."""
    ...

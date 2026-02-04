"""
Dirty Worker Process

Asyncio-based worker that loads dirty apps and handles requests
from the DirtyArbiter.

Threading Model
---------------
Each dirty worker runs an asyncio event loop in the main thread for:
- Handling connections from the arbiter
- Managing heartbeat updates
- Coordinating task execution

Actual app execution runs in a ThreadPoolExecutor (separate threads):
- The number of threads is controlled by ``dirty_threads`` config (default: 1)
- Each thread can execute one app action at a time
- The asyncio event loop is NOT blocked by task execution

State and Global Objects
------------------------
Apps can maintain persistent state because:

1. Apps are loaded ONCE when the worker starts (in ``load_apps()``)
2. The same app instances are reused for ALL requests
3. App state (instance variables, loaded models, etc.) persists

Example::

    class MLApp(DirtyApp):
        def init(self):
            self.model = load_heavy_model()  # Loaded once, reused
            self.cache = {}                   # Persistent cache

        def predict(self, data):
            return self.model.predict(data)  # Uses loaded model

Thread Safety:
- With ``dirty_threads=1`` (default): No concurrent access, thread-safe by design
- With ``dirty_threads > 1``: Multiple threads share the same app instances,
  apps MUST be thread-safe (use locks, thread-local storage, etc.)

Heartbeat and Liveness
----------------------
The worker sends heartbeat updates to prove it's alive:

1. A dedicated asyncio task (``_heartbeat_loop``) runs independently
2. It updates the heartbeat file every ``dirty_timeout / 2`` seconds
3. Since tasks run in executor threads, they do NOT block heartbeats
4. The arbiter kills workers that miss heartbeat updates

Timeout Control
---------------
Execution timeout is enforced at two levels:

1. **Worker level**: Each task execution has a timeout (``dirty_timeout``).
   If exceeded, the worker returns a timeout error but the thread may
   continue running (Python threads cannot be cancelled).

2. **Arbiter level**: The arbiter also enforces timeout when waiting
   for worker response. Workers that don't respond are killed via SIGABRT.

Note: Since Python threads cannot be forcibly cancelled, a truly stuck
operation will continue until the worker is killed by the arbiter.
"""

from _typeshed import Incomplete
from asyncio import StreamReader, StreamWriter
from collections.abc import Iterable, Mapping
from signal import Signals
from typing import Any, ClassVar, Literal

from gunicorn.config import Config
from gunicorn.glogging import Logger as GLogger
from gunicorn.workers.workertmp import WorkerTmp

class DirtyWorker:
    """
    Dirty worker process that loads dirty apps and handles requests.

    Each worker runs its own asyncio event loop and listens on a
    worker-specific Unix socket for requests from the DirtyArbiter.
    """
    SIGNALS: ClassVar[list[Signals]]
    age: int
    pid: int | Literal["[booting]"]
    ppid: int
    app_paths: list[str]
    cfg: Config
    log: GLogger
    socket_path: str
    booted: bool
    aborted: bool
    alive: bool
    tmp: WorkerTmp
    apps: dict[str, Incomplete]

    def __init__(self, age: int, ppid: int, app_paths: list[str], cfg: Config, log: GLogger, socket_path: str) -> None:
        """
        Initialize a dirty worker.

        Args:
            age: Worker age (for identifying workers)
            ppid: Parent process ID
            app_paths: List of dirty app import paths
            cfg: Gunicorn config
            log: Logger
            socket_path: Path to this worker's Unix socket
        """
        ...
    def notify(self) -> None:
        """Update heartbeat timestamp."""
        ...
    def init_process(self) -> None:
        """
        Initialize the worker process after fork.

        This is called in the child process after fork. It sets up
        the environment, loads apps, and starts the main run loop.
        """
        ...
    def init_signals(self) -> None:
        """Set up signal handlers."""
        ...
    def load_apps(self) -> None:
        """Load all configured dirty apps."""
        ...
    def run(self) -> None:
        """Run the main asyncio event loop."""
        ...
    async def handle_connection(self, reader: StreamReader, writer: StreamWriter) -> None:
        """
        Handle a connection from the arbiter.

        Each connection can send multiple requests.
        """
        ...
    async def handle_request(self, message: dict[str, Incomplete], writer: StreamWriter) -> None:
        """
        Handle a single request message.

        Supports both regular (non-streaming) and streaming responses.
        For streaming, detects if the result is a generator and sends
        chunk messages followed by an end message.

        Args:
            message: Request dict from protocol
            writer: StreamWriter for sending responses
        """
        ...
    async def execute(
        self, app_path: str, action: str, args: Iterable[Any], kwargs: Mapping[str, Any]
    ) -> Any:
        """
        Execute an action on a dirty app.

        The action runs in a thread pool executor to avoid blocking the
        asyncio event loop. Execution timeout is enforced using
        ``dirty_timeout`` config.

        Args:
            app_path: Import path of the dirty app
            action: Action name to execute
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Result from the app action

        Raises:
            DirtyAppNotFoundError: If app is not loaded
            DirtyTimeoutError: If execution exceeds timeout
            DirtyAppError: If execution fails
        """
        ...

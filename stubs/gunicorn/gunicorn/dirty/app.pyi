"""
Dirty Application Base Class

Provides the DirtyApp base class that all dirty applications must inherit from,
and utilities for loading dirty apps from import paths.
"""

from _typeshed import Incomplete
from collections.abc import Iterable
from typing import Any

class DirtyApp:
    """
    Base class for dirty applications.

    Dirty applications are loaded once when the dirty worker starts and
    persist in memory for the lifetime of the worker. They are designed
    for stateful resources like ML models, connection pools, etc.

    Lifecycle
    ---------
    1. ``__init__()``: Called when the app is instantiated (once per worker)
    2. ``init()``: Called after instantiation to initialize resources
    3. ``__call__()``: Called for each request from HTTP workers
    4. ``close()``: Called when the worker shuts down

    State Persistence
    -----------------
    Instance variables persist across requests. This is the key feature
    that enables loading heavy resources once and reusing them::

        class MLApp(DirtyApp):
            def init(self):
                self.model = load_model()  # Loaded once, reused forever

            def predict(self, data):
                return self.model.predict(data)  # Same model for all requests

    Thread Safety
    -------------
    With ``dirty_threads=1`` (default): Only one request runs at a time,
    so no thread safety concerns.

    With ``dirty_threads > 1``: Multiple requests may run concurrently
    in the same worker. Your app MUST be thread-safe. Options:

    - Use locks: ``threading.Lock()`` for shared state
    - Use thread-local: ``threading.local()`` for per-thread state
    - Use read-only state: Load models once in init(), never mutate

    Example::

        import threading

        class ThreadSafeMLApp(DirtyApp):
            def __init__(self):
                self.models = {}
                self._lock = threading.Lock()

            def init(self):
                self.models['default'] = load_model('base-model')

            def load_model(self, name):
                with self._lock:
                    if name not in self.models:
                        self.models[name] = load_model(name)
                return {"loaded": True, "name": name}

    Worker Allocation
    -----------------
    By default, all dirty workers load all apps. For apps that consume
    significant memory (like large ML models), you can limit how many
    workers load the app by setting the ``workers`` class attribute::

        class HeavyModelApp(DirtyApp):
            workers = 2  # Only 2 workers will load this app

            def init(self):
                self.model = load_10gb_model()

    Subclasses should implement:
        - init(): Called once at worker startup to initialize resources
        - __call__(action, *args, **kwargs): Handle requests from HTTP workers
        - close(): Called at worker shutdown to cleanup resources
    """
    workers: Incomplete | None

    def init(self) -> None:
        """
        Initialize the application.

        Called once when the dirty worker starts, after the app instance
        is created. Use this for expensive initialization like loading
        ML models, establishing database connections, etc.

        This method is called in the child process after fork, so it's
        safe to initialize non-fork-safe resources here.
        """
        ...
    def __call__(
        self, action: str, *args: Any, **kwargs: Any
    ) -> Any:
        """
        Handle a request from an HTTP worker.

        Args:
            action: The action/method name to execute
            *args: Positional arguments for the action
            **kwargs: Keyword arguments for the action

        Returns:
            The result of the action (must be JSON-serializable)

        Raises:
            ValueError: If the action is unknown
            Any exception: Will be caught and returned as DirtyAppError
        """
        ...
    def close(self) -> None:
        """
        Cleanup resources.

        Called when the dirty worker is shutting down. Use this to
        release resources like database connections, unload models, etc.
        """
        ...

def parse_dirty_app_spec(spec: str) -> tuple[str, int | None]:
    """
    Parse a dirty app specification.

    Supports two formats:
    - ``"module:Class"`` - standard format, all workers load the app
    - ``"module:Class:N"`` - worker-limited format, only N workers load the app

    Args:
        spec: The app specification string

    Returns:
        tuple: (import_path, worker_count)
            - import_path: The "module:Class" part for importing
            - worker_count: Integer limit or None for all workers

    Raises:
        DirtyAppError: If the spec format is invalid or worker_count is < 1

    Examples::

        >>> parse_dirty_app_spec("myapp:App")
        ("myapp:App", None)

        >>> parse_dirty_app_spec("myapp:App:2")
        ("myapp:App", 2)

        >>> parse_dirty_app_spec("myapp.sub:App:1")
        ("myapp.sub:App", 1)
    """
    ...
def load_dirty_app(import_path: str):
    """
    Load a dirty app class from an import path.

    Args:
        import_path: String in format 'module.path:ClassName'

    Returns:
        An instance of the dirty app class

    Raises:
        DirtyAppNotFoundError: If the module or class cannot be found
        DirtyAppError: If the class is not a valid DirtyApp subclass
    """
    ...
def load_dirty_apps(import_paths: Iterable[str]) -> dict[str, Incomplete]:
    """
    Load multiple dirty apps from a list of import paths.

    Args:
        import_paths: List of import path strings

    Returns:
        dict: Mapping of import path to app instance

    Raises:
        DirtyAppError: If any app fails to load
    """
    ...
def get_app_workers_attribute(import_path: str) -> int | None:
    """
    Get the workers class attribute from a dirty app without instantiating it.

    This is used by the arbiter to determine how many workers should load
    an app based on the class attribute, without needing to actually load
    the app.

    Args:
        import_path: String in format 'module.path:ClassName'

    Returns:
        The workers class attribute value (int or None)

    Raises:
        DirtyAppNotFoundError: If the module or class cannot be found
        DirtyAppError: If the import path format is invalid
    """
    ...

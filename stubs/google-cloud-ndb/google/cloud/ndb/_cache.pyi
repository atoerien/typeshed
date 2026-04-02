from _typeshed import Incomplete

from google.cloud.ndb import tasklets as tasklets

class ContextCache:
    """
    A per-context in-memory entity cache.

    This cache verifies the fetched entity has the correct key before
    returning a result, in order to handle cases where the entity's key was
    modified but the cache's key was not updated.
    """
    def get_and_validate(self, key):
        """
        Verify that the entity's key has not changed since it was added
        to the cache. If it has changed, consider this a cache miss.
        See issue 13.  http://goo.gl/jxjOP
        """
        ...

class _GlobalCacheBatch:
    """Abstract base for classes used to batch operations for the global cache."""
    def full(self):
        """
        Indicates whether more work can be added to this batch.

        Returns:
            boolean: `False`, always.
        """
        ...
    def idle_callback(self) -> None:
        """
        Call the cache operation.

        Also, schedule a callback for the completed operation.
        """
        ...
    def done_callback(self, cache_call) -> None:
        """
        Process results of call to global cache.

        If there is an exception for the cache call, distribute that to waiting
        futures, otherwise set the result for all waiting futures to ``None``.
        """
        ...
    def make_call(self) -> None:
        """Make the actual call to the global cache. To be overridden."""
        ...
    def future_info(self, key) -> None:
        """Generate info string for Future. To be overridden."""
        ...

global_get: Incomplete

class _GlobalCacheGetBatch(_GlobalCacheBatch):
    """
    Batch for global cache get requests.

    Attributes:
        todo (Dict[bytes, List[Future]]): Mapping of keys to futures that are
            waiting on them.

    Arguments:
        ignore_options (Any): Ignored.
    """
    todo: Incomplete
    keys: Incomplete
    def __init__(self, ignore_options) -> None: ...
    def add(self, key):
        """
        Add a key to get from the cache.

        Arguments:
            key (bytes): The key to get from the cache.

        Returns:
            tasklets.Future: Eventual result will be the entity retrieved from
                the cache (``bytes``) or ``None``.
        """
        ...
    def done_callback(self, cache_call) -> None:
        """
        Process results of call to global cache.

        If there is an exception for the cache call, distribute that to waiting
        futures, otherwise distribute cache hits or misses to their respective
        waiting futures.
        """
        ...
    def make_call(self):
        """Call :method:`GlobalCache.get`."""
        ...
    def future_info(self, key):
        """Generate info string for Future."""
        ...

def global_set(key, value, expires: Incomplete | None = ..., read: bool = ...):
    """
    Store entity in the global cache.

    Args:
        key (bytes): The key to save.
        value (bytes): The entity to save.
        expires (Optional[float]): Number of seconds until value expires.
        read (bool): Indicates if being set in a read (lookup) context.

    Returns:
        tasklets.Future: Eventual result will be ``None``.
    """
    ...

class _GlobalCacheSetBatch(_GlobalCacheBatch):
    """Batch for global cache set requests."""
    expires: Incomplete
    todo: object
    futures: object
    def __init__(self, options) -> None: ...
    def done_callback(self, cache_call) -> None: ...
    def add(self, key, value): ...
    def make_call(self): ...
    def future_info(self, key, value): ...  # type: ignore[override]

class _GlobalCacheSetIfNotExistsBatch(_GlobalCacheSetBatch):
    def add(self, key, value): ...
    def make_call(self): ...
    def future_info(self, key, value): ...  # type: ignore[override]

global_delete: Incomplete

class _GlobalCacheDeleteBatch(_GlobalCacheBatch):
    """Batch for global cache delete requests."""
    keys: Incomplete
    futures: Incomplete
    def __init__(self, ignore_options) -> None: ...
    def add(self, key):
        """
        Add a key to delete from the cache.

        Arguments:
            key (bytes): The key to delete.

        Returns:
            tasklets.Future: Eventual result will be ``None``.
        """
        ...
    def make_call(self):
        """Call :method:`GlobalCache.delete`."""
        ...
    def future_info(self, key):
        """Generate info string for Future."""
        ...

global_watch: Incomplete

class _GlobalCacheWatchBatch(_GlobalCacheDeleteBatch):
    def make_call(self): ...
    def future_info(self, key, value): ...  # type: ignore[override]

def global_unwatch(key):
    """
    End optimistic transaction with global cache.

    Indicates that value for the key wasn't found in the database, so there will not be
    a future call to :func:`global_compare_and_swap`, and we no longer need to watch
    this key.

    Args:
        key (bytes): The key to unwatch.

    Returns:
        tasklets.Future: Eventual result will be ``None``.
    """
    ...

class _GlobalCacheUnwatchBatch(_GlobalCacheDeleteBatch):
    """Batch for global cache unwatch requests."""
    def make_call(self):
        """Call :method:`GlobalCache.unwatch`."""
        ...
    def future_info(self, key):
        """Generate info string for Future."""
        ...

global_compare_and_swap: Incomplete

class _GlobalCacheCompareAndSwapBatch(_GlobalCacheSetBatch):
    def make_call(self): ...
    def future_info(self, key, value): ...  # type: ignore[override]

def is_locked_value(value):
    """
    Check if the given value is the special reserved value for key lock.

    Returns:
        bool: Whether the value is the special reserved value for key lock.
    """
    ...
def global_cache_key(key):
    """
    Convert Datastore key to ``bytes`` to use for global cache key.

    Args:
        key (datastore.Key): The Datastore key.

    Returns:
        bytes: The cache key.
    """
    ...

"""GlobalCache interface and its implementations."""

import abc
from _typeshed import Incomplete
from typing_extensions import Self

ConnectionError: Incomplete

class GlobalCache(metaclass=abc.ABCMeta):
    """
    Abstract base class for a global entity cache.

    A global entity cache is shared across contexts, sessions, and possibly
    even servers. A concrete implementation is available which uses Redis.

    Essentially, this class models a simple key/value store where keys and
    values are arbitrary ``bytes`` instances. "Compare and swap", aka
    "optimistic transactions" should also be supported.

    Concrete implementations can either by synchronous or asynchronous.
    Asynchronous implementations should return
    :class:`~google.cloud.ndb.tasklets.Future` instances whose eventual results
    match the return value described for each method. Because coordinating with
    the single threaded event model used by ``NDB`` can be tricky with remote
    services, it's not recommended that casual users write asynchronous
    implementations, as some specialized knowledge is required.

    Attributes:
        strict_read (bool): If :data:`False`, transient errors that occur as part of a
            entity lookup operation will be logged as warnings but not raised to the
            application layer. If :data:`True`, in the event of transient errors, cache
            operations will be retried a number of times before eventually raising the
            transient error to the application layer, if it does not resolve after
            retrying. Setting this to :data:`True` will cause NDB operations to take
            longer to complete if there are transient errors in the cache layer.
        strict_write (bool): If :data:`False`, transient errors that occur as part of
            a put or delete operation will be logged as warnings, but not raised to the
            application layer. If :data:`True`, in the event of transient errors, cache
            operations will be retried a number of times before eventually raising the
            transient error to the application layer if it does not resolve after
            retrying. Setting this to :data:`False` somewhat increases the risk
            that other clients might read stale data from the cache. Setting this to
            :data:`True` will cause NDB operations to take longer to complete if there
            are transient errors in the cache layer.
    """
    __metaclass__: Incomplete
    transient_errors: Incomplete
    strict_read: bool
    strict_write: bool
    @abc.abstractmethod
    def get(self, keys):
        """
        Retrieve entities from the cache.

        Arguments:
            keys (List[bytes]): The keys to get.

        Returns:
            List[Union[bytes, None]]]: Serialized entities, or :data:`None`,
                for each key.
        """
        ...
    @abc.abstractmethod
    def set(self, items, expires=None): ...
    @abc.abstractmethod
    def delete(self, keys):
        """
        Remove entities from the cache.

        Arguments:
            keys (List[bytes]): The keys to remove.
        """
        ...
    @abc.abstractmethod
    def watch(self, items):
        """
        Begin an optimistic transaction for the given items.

        A future call to :meth:`compare_and_swap` will only set values for keys
        whose values haven't changed since the call to this method. Values are used to
        check that the watched value matches the expected value for a given key.

        Arguments:
            items (Dict[bytes, bytes]): The items to watch.
        """
        ...
    @abc.abstractmethod
    def unwatch(self, keys):
        """
        End an optimistic transaction for the given keys.

        Indicates that value for the key wasn't found in the database, so there will not
        be a future call to :meth:`compare_and_swap`, and we no longer need to watch
        this key.

        Arguments:
            keys (List[bytes]): The keys to watch.
        """
        ...
    @abc.abstractmethod
    def compare_and_swap(self, items, expires=None): ...
    @abc.abstractmethod
    def clear(self):
        """
        Clear all keys from global cache.

        Will be called if there previously was a connection error, to prevent clients
        from reading potentially stale data from the cache.
        """
        ...

class _InProcessGlobalCache(GlobalCache):
    """
    Reference implementation of :class:`GlobalCache`.

    Not intended for production use. Uses a single process wide dictionary to
    keep an in memory cache. For use in testing and to have an easily grokkable
    reference implementation. Thread safety is potentially a little sketchy.
    """
    cache: Incomplete
    def __init__(self) -> None: ...
    def get(self, keys): ...
    def set(self, items, expires=None) -> None: ...
    def delete(self, keys) -> None: ...
    def watch(self, items) -> None: ...
    def unwatch(self, keys) -> None: ...
    def compare_and_swap(self, items, expires=None): ...
    def clear(self) -> None: ...

class RedisCache(GlobalCache):
    """
    Redis implementation of the :class:`GlobalCache`.

    This is a synchronous implementation. The idea is that calls to Redis
    should be fast enough not to warrant the added complexity of an
    asynchronous implementation.

    Args:
        redis (redis.Redis): Instance of Redis client to use.
        strict_read (bool): If :data:`False`, connection errors during read operations
            will be logged with a warning and treated as cache misses, but will not
            raise an exception in the application, with connection errors during reads
            being treated as cache misses. If :data:`True`, in the event of connection
            errors, cache operations will be retried a number of times before eventually
            raising the connection error to the application layer, if it does not
            resolve after retrying. Setting this to :data:`True` will cause NDB
            operations to take longer to complete if there are transient errors in the
            cache layer. Default: :data:`False`.
        strict_write (bool): If :data:`False`, connection errors during write
            operations will be logged with a warning, but will not raise an exception in
            the application. If :data:`True`, connection errors during write will be
            raised as exceptions in the application. Because write operations involve
            cache invalidation, setting this to :data:`False` may allow other clients to
            retrieve stale data from the cache. If :data:`True`, in the event of
            connection errors, cache operations will be retried a number of times before
            eventually raising the connection error to the application layer, if it does
            not resolve after retrying. Setting this to :data:`True` will cause NDB
            operations to take longer to complete if there are transient errors in the
            cache layer. Default: :data:`True`.
    """
    transient_errors: Incomplete
    @classmethod
    def from_environment(cls, strict_read: bool = False, strict_write: bool = True) -> Self: ...
    redis: Incomplete
    strict_read: Incomplete
    strict_write: Incomplete
    def __init__(self, redis, strict_read: bool = False, strict_write: bool = True) -> None: ...
    @property
    def pipes(self): ...
    def get(self, keys): ...
    def set(self, items, expires=None) -> None: ...
    def delete(self, keys) -> None: ...
    def watch(self, items) -> None: ...
    def unwatch(self, keys) -> None: ...
    def compare_and_swap(self, items, expires=None): ...
    def clear(self) -> None: ...

class MemcacheCache(GlobalCache):
    """
    Memcache implementation of the :class:`GlobalCache`.

    This is a synchronous implementation. The idea is that calls to Memcache
    should be fast enough not to warrant the added complexity of an
    asynchronous implementation.

    Args:
        client (pymemcache.Client): Instance of Memcache client to use.
        strict_read (bool): If :data:`False`, connection errors during read
            operations will be logged with a warning and treated as cache misses,
            but will not raise an exception in the application, with connection
            errors during reads being treated as cache misses. If :data:`True`, in
            the event of connection errors, cache operations will be retried a
            number of times before eventually raising the connection error to the
            application layer, if it does not resolve after retrying. Setting this
            to :data:`True` will cause NDB operations to take longer to complete if
            there are transient errors in the cache layer. Default: :data:`False`.
        strict_write (bool): If :data:`False`, connection errors during write
            operations will be logged with a warning, but will not raise an
            exception in the application. If :data:`True`, connection errors during
            write will be raised as exceptions in the application. Because write
            operations involve cache invalidation, setting this to :data:`False` may
            allow other clients to retrieve stale data from the cache. If :data:`True`,
            in the event of connection errors, cache operations will be retried a number
            of times before eventually raising the connection error to the application
            layer, if it does not resolve after retrying.  Setting this to :data:`True`
            will cause NDB operations to take longer to complete if there are transient
            errors in the cache layer. Default: :data:`True`.
    """
    class KeyNotSet(Exception):
        key: Incomplete
        def __init__(self, key) -> None: ...
        def __eq__(self, other): ...

    transient_errors: Incomplete
    @classmethod
    def from_environment(cls, max_pool_size: int = 4, strict_read: bool = False, strict_write: bool = True) -> Self: ...
    client: Incomplete
    strict_read: Incomplete
    strict_write: Incomplete
    def __init__(self, client, strict_read: bool = False, strict_write: bool = True) -> None: ...
    @property
    def caskeys(self): ...
    def get(self, keys): ...
    def set(self, items, expires=None): ...
    def delete(self, keys) -> None: ...
    def watch(self, items) -> None: ...
    def unwatch(self, keys) -> None: ...
    def compare_and_swap(self, items, expires=None): ...
    def clear(self) -> None: ...

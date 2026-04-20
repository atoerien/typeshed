from collections.abc import Callable

class _DummyLock:
    acquire: Callable[..., None]
    release: Callable[..., None]
    locked: Callable[..., None]

def allocate_lock() -> _DummyLock:
    """
    allocate_lock() -> lock object
    (allocate() is an obsolete synonym)

    Create a new lock object. See help(type(threading.Lock())) for
    information about locks.
    """
    ...

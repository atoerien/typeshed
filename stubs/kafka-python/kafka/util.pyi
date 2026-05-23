from _typeshed import Incomplete
from collections.abc import Callable
from typing import ParamSpec, TypeVar

_P = ParamSpec("_P")
_T = TypeVar("_T")

MAX_INT: Incomplete
TO_SIGNED: Incomplete

def crc32(data): ...

class Timer:
    def __init__(self, timeout_ms, error_message=None, start_at=None) -> None: ...
    @property
    def expired(self): ...
    @property
    def timeout_ms(self): ...
    @property
    def elapsed_ms(self): ...
    def maybe_raise(self) -> None: ...

TOPIC_MAX_LENGTH: int
TOPIC_LEGAL_CHARS: Incomplete

def ensure_valid_topic_name(topic) -> None:
    """Ensures that the topic name is valid according to the kafka source. """
    ...

class WeakMethod:
    """
    Callable that weakly references a method and the object it is bound to. It
    is based on https://stackoverflow.com/a/24287465.

    Arguments:

        object_dot_method: A bound instance method (i.e. 'object.method').
    """
    target: Incomplete
    method: Incomplete
    def __init__(self, object_dot_method) -> None: ...
    def __call__(self, *args, **kwargs):
        """Calls the method on target with args and kwargs."""
        ...
    def __hash__(self): ...
    def __eq__(self, other): ...

class Dict(dict[Incomplete, Incomplete]):
    """
    Utility class to support passing weakrefs to dicts

    See: https://docs.python.org/2/library/weakref.html
    """
    ...

def synchronized(func: Callable[_P, _T]) -> Callable[_P, _T]: ...

"""
Selectors module.

This module allows high-level and efficient I/O multiplexing, built upon the
`select` module primitives.
"""

import sys
from _typeshed import FileDescriptor, FileDescriptorLike, Unused
from abc import ABCMeta, abstractmethod
from collections.abc import Mapping
from typing import Any, Final, NamedTuple
from typing_extensions import Self

EVENT_READ: Final = 1
EVENT_WRITE: Final = 2

class SelectorKey(NamedTuple):
    """
    SelectorKey(fileobj, fd, events, data)

    Object used to associate a file object to its backing
    file descriptor, selected event mask, and attached data.
    """
    fileobj: FileDescriptorLike
    fd: FileDescriptor
    events: int
    data: Any

class BaseSelector(metaclass=ABCMeta):
    """
    Selector abstract base class.

    A selector supports registering file objects to be monitored for specific
    I/O events.

    A file object is a file descriptor or any object with a `fileno()` method.
    An arbitrary object can be attached to the file object, which can be used
    for example to store context information, a callback, etc.

    A selector can use various implementations (select(), poll(), epoll()...)
    depending on the platform. The default `Selector` class uses the most
    efficient implementation on the current platform.
    """
    @abstractmethod
    def register(self, fileobj: FileDescriptorLike, events: int, data: Any = None) -> SelectorKey: ...
    @abstractmethod
    def unregister(self, fileobj: FileDescriptorLike) -> SelectorKey: ...
    def modify(self, fileobj: FileDescriptorLike, events: int, data: Any = None) -> SelectorKey: ...
    @abstractmethod
    def select(self, timeout: float | None = None) -> list[tuple[SelectorKey, int]]: ...
    def close(self) -> None: ...
    def get_key(self, fileobj: FileDescriptorLike) -> SelectorKey: ...
    @abstractmethod
    def get_map(self) -> Mapping[FileDescriptorLike, SelectorKey]:
        """Return a mapping of file objects to selector keys."""
        ...
    def __enter__(self) -> Self: ...
    def __exit__(self, *args: Unused) -> None: ...

class _BaseSelectorImpl(BaseSelector, metaclass=ABCMeta):
    def register(self, fileobj: FileDescriptorLike, events: int, data: Any = None) -> SelectorKey: ...
    def unregister(self, fileobj: FileDescriptorLike) -> SelectorKey: ...
    def modify(self, fileobj: FileDescriptorLike, events: int, data: Any = None) -> SelectorKey: ...
    def get_map(self) -> Mapping[FileDescriptorLike, SelectorKey]: ...

class SelectSelector(_BaseSelectorImpl):
    def select(self, timeout: float | None = None) -> list[tuple[SelectorKey, int]]: ...

class _PollLikeSelector(_BaseSelectorImpl):
    def select(self, timeout: float | None = None) -> list[tuple[SelectorKey, int]]: ...

if sys.platform != "win32":
    class PollSelector(_PollLikeSelector):
        """Poll-based selector."""
        ...

if sys.platform == "linux":
    class EpollSelector(_PollLikeSelector):
        def fileno(self) -> int: ...

if sys.platform != "linux" and sys.platform != "darwin" and sys.platform != "win32":
    # Solaris only
    class DevpollSelector(_PollLikeSelector):
        def fileno(self) -> int: ...

if sys.platform != "win32" and sys.platform != "linux":
    class KqueueSelector(_BaseSelectorImpl):
        """Kqueue-based selector."""
        def fileno(self) -> int: ...
        def select(self, timeout: float | None = None) -> list[tuple[SelectorKey, int]]: ...

# Not a real class at runtime, it is just a conditional alias to other real selectors.
# The runtime logic is more fine-grained than a `sys.platform` check;
# not really expressible in the stubs
class DefaultSelector(_BaseSelectorImpl):
    def select(self, timeout: float | None = None) -> list[tuple[SelectorKey, int]]: ...
    if sys.platform != "win32":
        def fileno(self) -> int: ...

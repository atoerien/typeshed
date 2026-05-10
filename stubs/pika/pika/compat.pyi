import socket
import sys
from abc import ABCMeta
from re import Pattern
from typing import Final, SupportsIndex

RE_NUM: Final[Pattern[str]]
ON_LINUX: Final[bool]
ON_OSX: Final[bool]
ON_WINDOWS: Final[bool]

class AbstractBase(metaclass=ABCMeta): ...

SOCKET_ERROR = OSError
SOL_TCP: Final[int]
HAVE_SIGNAL: Final[bool]
str_or_bytes: Final[tuple[type[str], type[bytes]]]

def time_now() -> float: ...
def byte(*args: SupportsIndex) -> bytes: ...

    dict.keys returns a view that works like .keys in Python 2
    *except* any modifications in the dictionary will be visible
    (and will cause errors if the view is being iterated over while
    it is modified).
    """
    ...
def dictvalues(dct: Mapping[Any, _VT_co]) -> list[_VT_co]:
    """
    Returns a list of values of a dictionary

def as_bytes(value: str | bytes) -> bytes: ...
def to_digit(value: str) -> int: ...
def get_linux_version(release_str: str) -> tuple[int, int, int]: ...

if sys.platform == "linux":
    LINUX_VERSION: Final[tuple[int, int, int]]
else:
    LINUX_VERSION: Final[None]

def nonblocking_socketpair(
    family: int = socket.AF_INET, socket_type: int = socket.SOCK_STREAM, proto: int = 0
) -> tuple[socket.socket, socket.socket]: ...

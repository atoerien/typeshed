"""The compat module provides various compatibility functions"""

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

def time_now() -> float:
    """Returns monotonic time"""
    ...
def byte(*args: SupportsIndex) -> bytes:
    """
    Returns a single byte `bytes` for the given int argument (we
    optimize it a bit here by passing the positional argument tuple
    directly to the bytes constructor.
    """
    ...

class long(int):
    """
    A marker class that signifies that the integer value should be
    serialized as `l` instead of `I`
    """
    ...

def as_bytes(value: str | bytes) -> bytes:
    """Returns value as bytes"""
    ...
def to_digit(value: str) -> int:
    """Returns value as in integer"""
    ...
def get_linux_version(release_str: str) -> tuple[int, int, int]:
    """Gets linux version"""
    ...

if sys.platform == "linux":
    LINUX_VERSION: Final[tuple[int, int, int]]
else:
    LINUX_VERSION: Final[None]

def nonblocking_socketpair(
    family: int = socket.AF_INET, socket_type: int = socket.SOCK_STREAM, proto: int = 0
) -> tuple[socket.socket, socket.socket]:
    """
    Returns a pair of sockets in the manner of socketpair with the additional
    feature that they will be non-blocking. Prior to Python 3.5, socketpair
    did not exist on Windows at all.
    """
    ...

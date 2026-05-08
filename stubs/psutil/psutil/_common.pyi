"""
Common objects shared by __init__.py and _ps*.py modules.

Note: this module is imported by setup.py, so it should not import
psutil or third-party modules.
"""

import enum
import io
import sys
import threading
from _typeshed import ConvertibleToFloat, FileDescriptorOrPath, Incomplete, StrOrBytesPath, SupportsWrite
from collections import defaultdict
from collections.abc import Callable
from socket import AF_INET6 as AF_INET6, AddressFamily, SocketKind
from typing import BinaryIO, Final, ParamSpec, SupportsIndex, TypeVar, overload

from . import _ntuples as ntp

POSIX: Final[bool]
WINDOWS: Final[bool]
LINUX: Final[bool]
MACOS: Final[bool]
OSX: Final[bool]
FREEBSD: Final[bool]
OPENBSD: Final[bool]
NETBSD: Final[bool]
BSD: Final[bool]
SUNOS: Final[bool]
AIX: Final[bool]

STATUS_RUNNING: Final = "running"
STATUS_SLEEPING: Final = "sleeping"
STATUS_DISK_SLEEP: Final = "disk-sleep"
STATUS_STOPPED: Final = "stopped"
STATUS_TRACING_STOP: Final = "tracing-stop"
STATUS_ZOMBIE: Final = "zombie"
STATUS_DEAD: Final = "dead"
STATUS_WAKE_KILL: Final = "wake-kill"
STATUS_WAKING: Final = "waking"
STATUS_IDLE: Final = "idle"
STATUS_LOCKED: Final = "locked"
STATUS_WAITING: Final = "waiting"
STATUS_SUSPENDED: Final = "suspended"
STATUS_PARKED: Final = "parked"

CONN_ESTABLISHED: Final = "ESTABLISHED"
CONN_SYN_SENT: Final = "SYN_SENT"
CONN_SYN_RECV: Final = "SYN_RECV"
CONN_FIN_WAIT1: Final = "FIN_WAIT1"
CONN_FIN_WAIT2: Final = "FIN_WAIT2"
CONN_TIME_WAIT: Final = "TIME_WAIT"
CONN_CLOSE: Final = "CLOSE"
CONN_CLOSE_WAIT: Final = "CLOSE_WAIT"
CONN_LAST_ACK: Final = "LAST_ACK"
CONN_LISTEN: Final = "LISTEN"
CONN_CLOSING: Final = "CLOSING"
CONN_NONE: Final = "NONE"

class NicDuplex(enum.IntEnum):
    """An enumeration."""
    NIC_DUPLEX_FULL = 2
    NIC_DUPLEX_HALF = 1
    NIC_DUPLEX_UNKNOWN = 0

NIC_DUPLEX_FULL: Final = NicDuplex.NIC_DUPLEX_FULL
NIC_DUPLEX_HALF: Final = NicDuplex.NIC_DUPLEX_HALF
NIC_DUPLEX_UNKNOWN: Final = NicDuplex.NIC_DUPLEX_UNKNOWN

class BatteryTime(enum.IntEnum):
    """An enumeration."""
    POWER_TIME_UNKNOWN = -1
    POWER_TIME_UNLIMITED = -2

POWER_TIME_UNKNOWN: Final = BatteryTime.POWER_TIME_UNKNOWN
POWER_TIME_UNLIMITED: Final = BatteryTime.POWER_TIME_UNLIMITED

ENCODING: Final[str]
ENCODING_ERRS: Final[str]

conn_tmap: dict[str, tuple[list[AddressFamily], list[SocketKind]]]

class Error(Exception):
    """
    Base exception class. All other psutil exceptions inherit
    from this one.
    """
    ...

class NoSuchProcess(Error):
    """
    Exception raised when a process with a certain PID doesn't
    or no longer exists.
    """
    pid: int
    name: str | None
    msg: str
    def __init__(self, pid: int, name: str | None = None, msg: str | None = None) -> None: ...

class ZombieProcess(NoSuchProcess):
    """
    Exception raised when querying a zombie process. This is
    raised on macOS, BSD and Solaris only, and not always: depending
    on the query the OS may be able to succeed anyway.
    On Linux all zombie processes are querable (hence this is never
    raised). Windows doesn't have zombie processes.
    """
    ppid: int | None
    def __init__(self, pid: int, name: str | None = None, ppid: int | None = None, msg: str | None = None) -> None: ...

class AccessDenied(Error):
    """Exception raised when permission to perform an action is denied."""
    pid: int | None
    name: str | None
    msg: str
    def __init__(self, pid: int | None = None, name: str | None = None, msg: str | None = None) -> None: ...

class TimeoutExpired(Error):
    """
    Raised on Process.wait(timeout) if timeout expires and process
    is still alive.
    """
    seconds: float
    pid: int | None
    name: str | None
    msg: str
    def __init__(self, seconds: float, pid: int | None = None, name: str | None = None) -> None: ...

_P = ParamSpec("_P")
_R = TypeVar("_R")
_T = TypeVar("_T")

def usage_percent(used: ConvertibleToFloat, total: float, round_: SupportsIndex | None = None) -> float:
    """Calculate percentage usage of 'used' against 'total'."""
    ...

# returned function has `cache_clear()` attribute:
def memoize(fun: Callable[_P, _R]) -> Callable[_P, _R]:
    """
    A simple memoize decorator for functions supporting (hashable)
    positional arguments.
    It also provides a cache_clear() function for clearing the cache:

    >>> @memoize
    ... def foo()
    ...     return 1
        ...
    >>> foo()
    1
    >>> foo.cache_clear()
    >>>

    It supports:
     - functions
     - classes (acts as a @singleton)
     - staticmethods
     - classmethods

    It does NOT support:
     - methods
    """
    ...

# returned function has `cache_activate(proc)` and `cache_deactivate(proc)` attributes:
def memoize_when_activated(fun: Callable[_P, _R]) -> Callable[_P, _R]:
    """
    A memoize decorator which is disabled by default. It can be
    activated and deactivated on request.
    For efficiency reasons it can be used only against class methods
    accepting no arguments.

    >>> class Foo:
    ...     @memoize
    ...     def foo()
    ...         print(1)
    ...
    >>> f = Foo()
    >>> # deactivated (default)
    >>> foo()
    1
    >>> foo()
    1
    >>>
    >>> # activated
    >>> foo.cache_activate(self)
    >>> foo()
    1
    >>> foo()
    >>> foo()
    >>>
    """
    ...
def isfile_strict(path: StrOrBytesPath) -> bool:
    """
    Same as os.path.isfile() but does not swallow EACCES / EPERM
    exceptions, see:
    http://mail.python.org/pipermail/python-dev/2012-June/120787.html.
    """
    ...
def path_exists_strict(path: StrOrBytesPath) -> bool:
    """
    Same as os.path.exists() but does not swallow EACCES / EPERM
    exceptions. See:
    http://mail.python.org/pipermail/python-dev/2012-June/120787.html.
    """
    ...
def supports_ipv6() -> bool:
    """Return True if IPv6 is supported on this platform."""
    ...
def parse_environ_block(data: str) -> dict[str, str]:
    """Parse a C environ block of environment variables into a dictionary."""
    ...
def sockfam_to_enum(num: int) -> AddressFamily:
    """
    Convert a numeric socket family value to an IntEnum member.
    If it's not a known member, return the numeric value itself.
    """
    ...
def socktype_to_enum(num: int) -> SocketKind:
    """
    Convert a numeric socket type value to an IntEnum member.
    If it's not a known member, return the numeric value itself.
    """
    ...
@overload
def conn_to_ntuple(
    fd: int,
    fam: int,
    type_: int,
    laddr: ntp.addr | tuple[str, int] | tuple[()],
    raddr: ntp.addr | tuple[str, int] | tuple[()],
    status: int | str,
    status_map: dict[int, str] | dict[str, str],
    pid: int,
) -> ntp.sconn:
    """Convert a raw connection tuple to a proper ntuple."""
    ...
@overload
def conn_to_ntuple(
    fd: int,
    fam: int,
    type_: int,
    laddr: ntp.addr | tuple[str, int] | tuple[()],
    raddr: ntp.addr | tuple[str, int] | tuple[()],
    status: int | str,
    status_map: dict[int, str] | dict[str, str],
    pid: None = None,
) -> ntp.pconn:
    """Convert a raw connection tuple to a proper ntuple."""
    ...
def deprecated_method(replacement: str) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
    """
    A decorator which can be used to mark a method as deprecated
    'replcement' is the method name which will be called instead.
    """
    ...

class _WrapNumbers:
    """
    Watches numbers so that they don't overflow and wrap
    (reset to zero).
    """
    lock: threading.Lock
    cache: dict[str, dict[str, tuple[int, ...]]]
    reminders: dict[str, defaultdict[Incomplete, int]]
    reminder_keys: dict[str, defaultdict[Incomplete, set[Incomplete]]]
    def __init__(self) -> None: ...
    def run(self, input_dict: dict[str, tuple[int, ...]], name: str) -> dict[str, tuple[int, ...]]:
        """
        Cache dict and sum numbers which overflow and wrap.
        Return an updated copy of `input_dict`.
        """
        ...
    def cache_clear(self, name: str | None = None) -> None:
        """Clear the internal cache, optionally only for function 'name'."""
        ...
    def cache_info(
        self,
    ) -> tuple[
        dict[str, dict[str, tuple[int, ...]]],
        dict[str, defaultdict[Incomplete, int]],
        dict[str, defaultdict[Incomplete, set[Incomplete]]],
    ]:
        """Return internal cache dicts as a tuple of 3 elements."""
        ...

def wrap_numbers(input_dict: dict[str, tuple[int, ...]], name: str) -> dict[str, tuple[int, ...]]:
    """
    Given an `input_dict` and a function `name`, adjust the numbers
    which "wrap" (restart from zero) across different calls by adding
    "old value" to "new value" and return an updated dict.
    """
    ...
def open_binary(fname: FileDescriptorOrPath) -> BinaryIO: ...
def open_text(fname: FileDescriptorOrPath) -> io.TextIOWrapper:
    """
    Open a file in text mode by using the proper FS encoding and
    en/decoding error handlers.
    """
    ...
@overload
def cat(fname: FileDescriptorOrPath, _open: Callable[[FileDescriptorOrPath], io.TextIOWrapper] = ...) -> str:
    """
    Read entire file content and return it as a string. File is
    opened in text mode. If specified, `fallback` is the value
    returned in case of error, either if the file does not exist or
    it can't be read().
    """
    ...
@overload
def cat(
    fname: FileDescriptorOrPath, fallback: _T = ..., _open: Callable[[FileDescriptorOrPath], io.TextIOWrapper] = ...
) -> str | _T:
    """
    Read entire file content and return it as a string. File is
    opened in text mode. If specified, `fallback` is the value
    returned in case of error, either if the file does not exist or
    it can't be read().
    """
    ...
@overload
def bcat(fname: FileDescriptorOrPath) -> str:
    """Same as above but opens file in binary mode."""
    ...
@overload
def bcat(fname: FileDescriptorOrPath, fallback: _T = ...) -> str | _T:
    """Same as above but opens file in binary mode."""
    ...
def bytes2human(n: int, format: str = "%(value).1f%(symbol)s") -> str:
    """
    Used by various scripts. See: https://code.activestate.com/recipes/578019-bytes-to-human-human-to-bytes-converter/?in=user-4178764.

    >>> bytes2human(10000)
    '9.8K'
    >>> bytes2human(100001221)
    '95.4M'
    """
    ...
def get_procfs_path() -> str:
    """Return updated psutil.PROCFS_PATH constant."""
    ...
def decode(s: bytes) -> str: ...
def term_supports_colors(file: SupportsWrite[str] = sys.stdout) -> bool: ...
def hilite(s: str, color: str | None = None, bold: bool = False) -> str:
    """Return an highlighted version of 'string'."""
    ...
def print_color(s: str, color: str | None = None, bold: bool = False, file: SupportsWrite[str] = sys.stdout) -> None:
    """Print a colorized version of string."""
    ...
def debug(msg: str | Exception) -> None:
    """If PSUTIL_DEBUG env var is set, print a debug message to stderr."""
    ...

__all__ = [
    # OS constants
    "FREEBSD",
    "BSD",
    "LINUX",
    "NETBSD",
    "OPENBSD",
    "MACOS",
    "OSX",
    "POSIX",
    "SUNOS",
    "WINDOWS",
    # connection constants
    "CONN_CLOSE",
    "CONN_CLOSE_WAIT",
    "CONN_CLOSING",
    "CONN_ESTABLISHED",
    "CONN_FIN_WAIT1",
    "CONN_FIN_WAIT2",
    "CONN_LAST_ACK",
    "CONN_LISTEN",
    "CONN_NONE",
    "CONN_SYN_RECV",
    "CONN_SYN_SENT",
    "CONN_TIME_WAIT",
    # net constants
    "NIC_DUPLEX_FULL",
    "NIC_DUPLEX_HALF",
    "NIC_DUPLEX_UNKNOWN",
    # process status constants
    "STATUS_DEAD",
    "STATUS_DISK_SLEEP",
    "STATUS_IDLE",
    "STATUS_LOCKED",
    "STATUS_RUNNING",
    "STATUS_SLEEPING",
    "STATUS_STOPPED",
    "STATUS_SUSPENDED",
    "STATUS_TRACING_STOP",
    "STATUS_WAITING",
    "STATUS_WAKE_KILL",
    "STATUS_WAKING",
    "STATUS_ZOMBIE",
    "STATUS_PARKED",
    # other constants
    "ENCODING",
    "ENCODING_ERRS",
    "AF_INET6",
    # utility functions
    "conn_tmap",
    "deprecated_method",
    "isfile_strict",
    "memoize",
    "parse_environ_block",
    "path_exists_strict",
    "usage_percent",
    "supports_ipv6",
    "sockfam_to_enum",
    "socktype_to_enum",
    "wrap_numbers",
    "open_text",
    "open_binary",
    "cat",
    "bcat",
    "bytes2human",
    "conn_to_ntuple",
    "debug",
    # shell utils
    "hilite",
    "term_supports_colors",
    "print_color",
]

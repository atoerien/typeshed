"""
distutils.util

Miscellaneous utility functions -- anything that doesn't fit into
one of the other *util.py modules.
"""

from _typeshed import GenericPath, StrPath, Unused
from collections.abc import Callable, Iterable, Mapping
from typing import AnyStr, Literal
from typing_extensions import TypeVarTuple, Unpack

_Ts = TypeVarTuple("_Ts")

def get_host_platform() -> str:
    """
    Return a string that identifies the current platform. Use this
    function to distinguish platform-specific build directories and
    platform-specific built distributions.
    """
    ...
def get_platform() -> str: ...
def get_macosx_target_ver_from_syscfg():
    """
    Get the version of macOS latched in the Python interpreter configuration.
    Returns the version as a string or None if can't obtain one. Cached.
    """
    ...
def get_macosx_target_ver():
    """
    Return the version of macOS for which we are building.

    The target version defaults to the version in sysconfig latched at time
    the Python interpreter was built, unless overridden by an environment
    variable. If neither source has a value, then None is returned
    """
    ...
def split_version(s: str) -> list[int]:
    """Convert a dot-separated string into a list of numbers for comparisons"""
    ...
def convert_path(pathname: StrPath) -> str:
    r"""
    Allow for pathlib.Path inputs, coax to a native path string.

    If None is passed, will just pass it through as
    Setuptools relies on this behavior.

    >>> convert_path(None) is None
    True

    Removes empty paths.

    >>> convert_path('foo/./bar').replace('\\', '/')
    'foo/bar'
    """
    ...
def change_root(new_root: GenericPath[AnyStr], pathname: GenericPath[AnyStr]) -> AnyStr:
    """
    Return 'pathname' with 'new_root' prepended.  If 'pathname' is
    relative, this is equivalent to "os.path.join(new_root,pathname)".
    Otherwise, it requires making 'pathname' relative and then joining the
    two, which is tricky on DOS/Windows and Mac OS.
    """
    ...
def check_environ() -> None:
    """
    Ensure that 'os.environ' has all the environment variables we
    guarantee that users can use in config files, command-line options,
    etc.  Currently this includes:
      HOME - user's home directory (Unix only)
      PLAT - description of the current platform, including hardware
             and OS (see 'get_platform()')
    """
    ...
def subst_vars(s: str, local_vars: Mapping[str, object]) -> str:
    """
    Perform variable substitution on 'string'.
    Variables are indicated by format-style braces ("{var}").
    Variable is substituted by the value found in the 'local_vars'
    dictionary or in 'os.environ' if it's not in 'local_vars'.
    'os.environ' is first checked/augmented to guarantee that it contains
    certain values: see 'check_environ()'.  Raise ValueError for any
    variables not found in either 'local_vars' or 'os.environ'.
    """
    ...
def grok_environment_error(exc: object, prefix: str = "error: ") -> str: ...
def split_quoted(s: str) -> list[str]:
    """
    Split a string up according to Unix shell-like rules for quotes and
    backslashes.  In short: words are delimited by spaces, as long as those
    spaces are not escaped by a backslash, or inside a quoted string.
    Single and double quotes are equivalent, and the quote characters can
    be backslash-escaped.  The backslash is stripped from any two-character
    escape sequence, leaving only the escaped character.  The quote
    characters are stripped from any quoted string.  Returns a list of
    words.
    """
    ...
def execute(
    func: Callable[[Unpack[_Ts]], Unused], args: tuple[Unpack[_Ts]], msg: str | None = None, verbose: bool = False
) -> None:
    """
    Perform some action that affects the outside world (e.g. by
    writing to the filesystem). Was previously used to deal with
    "dry run" operations, but now runs unconditionally.
    """
    ...
def strtobool(val: str) -> Literal[0, 1]:
    """
    Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    ...
def byte_compile(
    py_files: Iterable[str],
    optimize: int = 0,
    force: bool = False,
    prefix: str | None = None,
    base_dir: str | None = None,
    verbose: bool = True,
    direct: bool | None = None,
) -> None: ...
def rfc822_escape(header: str) -> str: ...
def is_mingw() -> bool: ...
def is_freethreaded() -> bool: ...

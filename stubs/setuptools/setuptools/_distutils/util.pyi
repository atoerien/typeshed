from _typeshed import StrPath, Unused
from collections.abc import Callable, Iterable, Mapping
from typing import Literal
from typing_extensions import TypeVarTuple, Unpack

from .compilers.platform import detect, macos

_Ts = TypeVarTuple("_Ts")

get_host_platform = detect.get_host_platform
get_platform = detect.get_platform
is_mingw = detect.is_mingw
MACOSX_VERSION_VAR = macos.VERSION_VAR
get_macosx_target_ver = macos.target_ver
get_macosx_target_ver_from_syscfg = macos._target_ver_from_syscfg

def split_version(s: str) -> list[int]: ...
def convert_path(pathname: StrPath) -> str: ...
def change_root(new_root: StrPath, pathname: StrPath) -> str: ...
def check_environ() -> None: ...
def subst_vars(s: str, local_vars: Mapping[str, object]) -> str: ...
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
def is_freethreaded() -> bool: ...

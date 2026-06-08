"""General helpers required for `tqdm.std`."""

from _typeshed import Incomplete
from collections.abc import Callable, Mapping
from re import Pattern
from typing import ParamSpec, Protocol, TypeVar, type_check_only

CUR_OS: str
IS_WIN: bool
IS_NIX: bool
RE_ANSI: Pattern[str]

class FormatReplace:
    """
    >>> a = FormatReplace('something')
    >>> f"{a:5d}"
    'something'
    """
    replace: str
    format_called: int
    def __init__(self, replace: str = "") -> None: ...
    def __format__(self, _) -> str: ...

@type_check_only
class _Has__Comparable(Protocol):
    _comparable: Incomplete

class Comparable:
    """Assumes child has self._comparable attr/@property"""
    _comparable: Incomplete
    def __lt__(self, other: _Has__Comparable) -> bool: ...
    def __le__(self, other: _Has__Comparable) -> bool: ...
    def __eq__(self, other: _Has__Comparable) -> bool: ...  # type: ignore[override]
    def __ne__(self, other: _Has__Comparable) -> bool: ...  # type: ignore[override]
    def __gt__(self, other: _Has__Comparable) -> bool: ...
    def __ge__(self, other: _Has__Comparable) -> bool: ...

class ObjectWrapper:
    def __getattr__(self, name: str): ...
    def __setattr__(self, name: str, value) -> None: ...
    def wrapper_getattr(self, name):
        """Actual `self.getattr` rather than self._wrapped.getattr"""
        ...
    def wrapper_setattr(self, name, value):
        """Actual `self.setattr` rather than self._wrapped.setattr"""
        ...
    def __init__(self, wrapped) -> None:
        """Thin wrapper around a given object"""
        ...

class SimpleTextIOWrapper(ObjectWrapper):
    """
    Change only `.write()` of the wrapped object by encoding the passed
    value and passing the result to the wrapped object's `.write()` method.
    """
    def __init__(self, wrapped, encoding) -> None: ...
    def write(self, s: str):
        """Encode `s` and pass to the wrapped object's `.write()` method."""
        ...
    def __eq__(self, other: object) -> bool: ...

_P = ParamSpec("_P")
_R = TypeVar("_R")

class DisableOnWriteError(ObjectWrapper):
    """Disable the given `tqdm_instance` upon `write()` or `flush()` errors."""
    @staticmethod
    def disable_on_exception(tqdm_instance, func: Callable[_P, _R]) -> Callable[_P, _R]:
        """Quietly set `tqdm_instance.miniters=inf` if `func` raises `errno=5`."""
        ...
    def __init__(self, wrapped, tqdm_instance) -> None: ...
    def __eq__(self, other: object) -> bool: ...

class CallbackIOWrapper(ObjectWrapper):
    def __init__(self, callback: Callable[[int], object], stream, method: str = "read") -> None:
        """
        Wrap a given `file`-like object's `read()` or `write()` to report
        lengths to the given `callback`
        """
        ...

def disp_len(data: str) -> int:
    """
    Returns the real on-screen length of a string which may contain
    ANSI control codes and wide chars.
    """
    ...
def disp_trim(data: str, length: int) -> str:
    """Trim a string which may contain ANSI control characters."""
    ...
def envwrap(
    name: str, app: str = "", types: Mapping[str, Callable[[Incomplete], Incomplete]] | None = None, is_method: bool = False
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
    """
    Function decorator overriding default arguments.

    Precedence (descending):
    - call (`func(a=3)`)
    - environment (`NAME_APP_FUNC_A=2`, `NAME_FUNC_A=2`, `NAME_APP_A=2`, `NAME_A=2`)
        - `UPPER_CASE` env vars -> `lower_case` param names
        - other cases aren't supported because Windows ignores case
    - config file:
        - ./`{name}.{toml,yaml,yml,json,ini,cfg}::{app.func.a,func.a,app.a,a}`
        - platformdirs.{user,site}_config_path(name, False)/
            - `{app}.{toml,yaml,yml,json,ini,cfg}::{func.a,a}`
            - `{name}.{toml,yaml,yml,json,ini,cfg}::{app.func.a,func.a,app.a,a}`
        - ./`pyproject.toml::tool.name.{app.func.a,func.a,app.a,a}`
    - signature (`def foo(a=1)`)

    Parameters
    ----------
    name:
        Configuration name.
    app:
        Application name.
    types:
        Fallback mappings `{'param_name': type, ...}` if types cannot be
        inferred from function signature.
        Consider using `types=collections.defaultdict(lambda: ast.literal_eval)`.
    is_method:
        Whether to use `functools.partialmethod`. If (default: False) use `functools.partial`.

    Examples
    --------
    >>> os.environ.update(dict(FOO_A="7", FOO_TEST_A="42", FOO_C="1337"))
    >>> from envwrap import envwrap
    >>> @envwrap("FOO")
    >>> def test(a=1, b=2, c=3):
    ...     print(f"received: a={a}, b={b}, c={c}")
    ...
    >>> test(c=99)
    received: a=42, b=2, c=99
    """
    ...

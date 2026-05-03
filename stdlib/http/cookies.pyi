from _typeshed import MaybeNone, SupportsItems, SupportsKeysAndGetItem
from collections.abc import Container, Iterable
from types import GenericAlias
from typing import Any, Generic, TypeVar, overload

__all__ = ["CookieError", "BaseCookie", "SimpleCookie"]

_T = TypeVar("_T")

@overload
def _quote(str: None) -> None:
    r"""
    Quote a string for use in a cookie header.

    If the string does not need to be double-quoted, then just return the
    string.  Otherwise, surround the string in doublequotes and quote
    (with a \) special characters.
    """
    ...
@overload
def _quote(str: str) -> str:
    r"""
    Quote a string for use in a cookie header.

    If the string does not need to be double-quoted, then just return the
    string.  Otherwise, surround the string in doublequotes and quote
    (with a \) special characters.
    """
    ...
@overload
def _unquote(str: None) -> None: ...
@overload
def _unquote(str: str) -> str: ...

class CookieError(Exception): ...

class Morsel(dict[str, Any], Generic[_T]):
    """
    A class to hold ONE (key, value) pair.

    In a cookie, each such pair may have several attributes, so this class is
    used to keep the attributes associated with the appropriate key,value pair.
    This class also includes a coded_value attribute, which is used to hold
    the network representation of the value.
    """
    @property
    def value(self) -> str | MaybeNone: ...
    @property
    def coded_value(self) -> _T | MaybeNone: ...
    @property
    def key(self) -> str | MaybeNone: ...
    def __init__(self) -> None: ...
    def set(self, key: str, val: str, coded_val: _T) -> None: ...
    def setdefault(self, key: str, val: str | None = None) -> str: ...
    # The dict update can also get a keywords argument so this is incompatible
    def update(self, values: Iterable[tuple[str, str]] | SupportsKeysAndGetItem[str, str]) -> None: ...  # type: ignore[override]
    def isReservedKey(self, K: str) -> bool: ...
    def output(self, attrs: Container[str] | None = None, header: str = "Set-Cookie:") -> str: ...
    __str__ = output
    def js_output(self, attrs: Container[str] | None = None) -> str: ...
    def OutputString(self, attrs: Container[str] | None = None) -> str: ...
    def __eq__(self, morsel: object) -> bool: ...
    def __setitem__(self, K: str, V: Any) -> None: ...
    def __class_getitem__(cls, item: Any, /) -> GenericAlias:
        """
        Represent a PEP 585 generic type

        E.g. for t = list[int], t.__origin__ is list and t.__args__ is (int,).
        """
        ...

class BaseCookie(dict[str, Morsel[_T]], Generic[_T]):
    def __init__(self, input: str | SupportsItems[str, str | Morsel[Any]] | None = None) -> None: ...
    def value_decode(self, val: str) -> tuple[_T, str]: ...
    def value_encode(self, val: _T) -> tuple[str, str]: ...
    def output(self, attrs: Container[str] | None = None, header: str = "Set-Cookie:", sep: str = "\r\n") -> str: ...
    __str__ = output
    def js_output(self, attrs: Container[str] | None = None) -> str: ...
    def load(self, rawdata: str | SupportsItems[str, str | Morsel[Any]]) -> None: ...
    def __setitem__(self, key: str, value: str | Morsel[_T]) -> None: ...

class SimpleCookie(BaseCookie[str]):
    """
    SimpleCookie supports strings as cookie values.  When setting
    the value using the dictionary assignment notation, SimpleCookie
    calls the builtin str() to convert the value to a string.  Values
    received from HTTP are kept as strings.
    """
    ...

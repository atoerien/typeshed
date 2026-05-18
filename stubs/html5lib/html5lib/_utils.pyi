import xml.etree.ElementTree as default_etree
from _typeshed import Incomplete, Unused
from collections.abc import Iterable, Mapping, Sequence
from typing import Final, TypeVar, overload

__all__ = [
    "default_etree",
    "MethodDispatcher",
    "isSurrogatePair",
    "surrogatePairToCodepoint",
    "moduleFactoryFactory",
    "supports_lone_surrogates",
]

supports_lone_surrogates: Final[bool]

_K = TypeVar("_K")
_V = TypeVar("_V")

class MethodDispatcher(dict[_K, _V]):
    """
    Dict with 2 special properties:

    On initiation, keys that are lists, sets or tuples are converted to
    multiple keys so accessing any one of the items in the original
    list-like object returns the matching value

    md = MethodDispatcher({("foo", "bar"):"baz"})
    md["foo"] == "baz"

    A default value which can be set through the default attribute.
    """
    default: _V | None

    @overload  # to solve `reportInvalidTypeVarUse`
    def __init__(self) -> None: ...
    @overload
    def __init__(self, items: Iterable[tuple[_K | Iterable[_K], _V]]) -> None: ...

    def __getitem__(self, key: _K) -> _V | None: ...  # type: ignore[override]
    def __get__(self, instance, owner: Unused = None) -> BoundMethodDispatcher: ...

class BoundMethodDispatcher(Mapping[Incomplete, Incomplete]):
    """Wraps a MethodDispatcher, binding its return values to `instance`"""
    instance: Incomplete
    dispatcher: Incomplete
    def __init__(self, instance, dispatcher) -> None: ...
    def __getitem__(self, key): ...
    def get(self, key, default): ...  # type: ignore[override]
    def __iter__(self): ...
    def __len__(self) -> int: ...
    def __contains__(self, key) -> bool: ...

def isSurrogatePair(data: Sequence[str | bytes | bytearray]) -> bool: ...
def surrogatePairToCodepoint(data: Sequence[str | bytes | bytearray]) -> int: ...
def moduleFactoryFactory(factory): ...

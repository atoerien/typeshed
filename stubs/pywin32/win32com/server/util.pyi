"""General Server side utilities"""

from _typeshed import Incomplete
from collections.abc import Iterable
from typing import Literal

import _win32typing

def wrap(
    ob, iid=None, usePolicy: type[Incomplete] | None = None, useDispatcher: type[Incomplete] | bool | Literal[0, 1] | None = None
):
    """
    Wraps an object in a PyGDispatch gateway.

    Returns a client side PyI{iid} interface.

    Interface and gateway support must exist for the specified IID, as
    the QueryInterface() method is used.
    """
    ...
def unwrap(ob):
    """
    Unwraps an interface.

    Given an interface which wraps up a Gateway, return the object behind
    the gateway.
    """
    ...

class ListEnumerator:
    """
    A class to expose a Python sequence as an EnumVARIANT.

    Create an instance of this class passing a sequence (list, tuple, or
    any sequence protocol supporting object) and it will automatically
    support the EnumVARIANT interface for the object.

    See also the @NewEnum@ function, which can be used to turn the
    instance into an actual COM server.
    """
    index: int
    def __init__(self, data, index: int = 0, iid=...) -> None: ...
    def Next(self, count: int): ...
    def Skip(self, count: int) -> None: ...
    def Reset(self) -> None: ...
    def Clone(self): ...

class ListEnumeratorGateway(ListEnumerator):
    """
    A List Enumerator which wraps a sequence's items in gateways.

    If a sequence contains items (objects) that have not been wrapped for
    return through the COM layers, then a ListEnumeratorGateway can be
    used to wrap those items before returning them (from the Next() method).

    See also the @ListEnumerator@ class and the @NewEnum@ function.
    """
    def Next(self, count: int) -> Iterable[Incomplete]: ...

def NewEnum(
    seq,
    cls=...,
    iid=...,
    usePolicy: type[Incomplete] | None = None,
    useDispatcher: type[Incomplete] | bool | Literal[0, 1] | None = None,
):
    """
    Creates a new enumerator COM server.

    This function creates a new COM Server that implements the
    IID_IEnumVARIANT interface.

    A COM server that can enumerate the passed in sequence will be
    created, then wrapped up for return through the COM framework.
    Optionally, a custom COM server for enumeration can be passed
    (the default is @ListEnumerator@), and the specific IEnum
    interface can be specified.
    """
    ...

class Collection:
    """A collection of VARIANT values."""
    data: Incomplete
    def __init__(self, data=None, readOnly: bool | Literal[0, 1] = 0) -> None: ...
    def Item(self, *args): ...
    def Count(self): ...
    def Add(self, value) -> None: ...
    def Remove(self, index) -> None: ...
    def Insert(self, index, value) -> None: ...

def NewCollection(seq, cls=...) -> _win32typing.PyIUnknown:
    """
    Creates a new COM collection object

    This function creates a new COM Server that implements the
    common collection protocols, including enumeration. (_NewEnum)

    A COM server that can enumerate the passed in sequence will be
    created, then wrapped up for return through the COM framework.
    Optionally, a custom COM server for enumeration can be passed
    (the default is @Collection@).
    """
    ...

class FileStream:
    file: Incomplete
    def __init__(self, file: _win32typing.Pymmapfile) -> None: ...
    def Read(self, amount): ...
    def Write(self, data) -> int: ...
    def Clone(self): ...
    def CopyTo(self, dest, cb) -> tuple[int, int]: ...
    def Seek(self, offset: int, origin: int) -> int: ...

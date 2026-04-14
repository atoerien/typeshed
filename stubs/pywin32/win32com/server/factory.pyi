from _typeshed import Unused
from collections.abc import Iterable

from _win32typing import PyIClassFactory, PyIID

def RegisterClassFactories(
    clsids: Iterable[PyIID], flags: int | None = None, clsctx: int | None = None
) -> list[tuple[PyIClassFactory, int]]:
    """
    Given a list of CLSID, create and register class factories.

    Returns a list, which should be passed to RevokeClassFactories
    """
    ...
def RevokeClassFactories(infos: Iterable[tuple[Unused, int]]) -> None: ...

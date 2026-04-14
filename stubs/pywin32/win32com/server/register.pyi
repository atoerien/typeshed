"""
Utilities for registering objects.

This module contains utility functions to register Python objects as
valid COM Servers.  The RegisterServer function provides all information
necessary to allow the COM framework to respond to a request for a COM object,
construct the necessary Python object, and dispatch COM events.
"""

from collections.abc import Callable, Iterable, Mapping
from typing import Final, Literal, Protocol, TypedDict, TypeVar, type_check_only
from typing_extensions import Unpack

from _win32typing import PyHKEY, PyIID

_T = TypeVar("_T", PyHKEY, int)

@type_check_only
class _RegisterClass(Protocol):
    _reg_clsid_: PyIID

@type_check_only
class _RegisterFlag(TypedDict, total=False):
    quiet: bool
    debug: bool
    finalize_register: Callable[[], None]

@type_check_only
class _UnregisterFlag(TypedDict, total=False):
    quiet: bool
    finalize_unregister: Callable[[], None]

@type_check_only
class _ElevatedFlag(TypedDict, total=False):
    quiet: bool
    unattended: bool
    hwnd: int

@type_check_only
class _CommandFlag(_RegisterFlag, _UnregisterFlag, _ElevatedFlag):  # type: ignore[misc]
    ...

CATID_PythonCOMServer: Final = "{B3EF80D0-68E2-11D0-A689-00C04FD658FF}"

def recurse_delete_key(path: str | None, base: PyHKEY | int = -2147483648) -> None:
    """
    Recursively delete registry keys.

    This is needed since you can't blast a key when subkeys exist.
    """
    ...
def RegisterServer(
    clsid: PyIID,
    pythonInstString: str | None = None,
    desc: str | None = None,
    progID: str | None = None,
    verProgID: str | None = None,
    defIcon: str | None = None,
    threadingModel: Literal["apartment", "both", "free", "neutral"] = "both",
    policy: str | None = None,
    catids: list[PyIID] = [],
    other: Mapping[str, str] = {},
    addPyComCat: bool | None = None,
    dispatcher: str | None = None,
    clsctx: int | None = None,
    addnPath: str | None = None,
) -> None:
    """
    Registers a Python object as a COM Server.  This enters almost all necessary
    information in the system registry, allowing COM to use the object.

    clsid -- The (unique) CLSID of the server.
    pythonInstString -- A string holding the instance name that will be created
                  whenever COM requests a new object.
    desc -- The description of the COM object.
    progID -- The user name of this object (eg, Word.Document)
    verProgId -- The user name of this version's implementation (eg Word.6.Document)
    defIcon -- The default icon for the object.
    threadingModel -- The threading model this object supports.
    policy -- The policy to use when creating this object.
    catids -- A list of category ID's this object belongs in.
    other -- A dictionary of extra items to be registered.
    addPyComCat -- A flag indicating if the object should be added to the list
             of Python servers installed on the machine.  If None (the default)
             then it will be registered when running from python source, but
             not registered if running in a frozen environment.
    dispatcher -- The dispatcher to use when creating this object.
    clsctx -- One of the CLSCTX_* constants.
    addnPath -- An additional path the COM framework will add to sys.path
                before attempting to create the object.
    """
    ...
def GetUnregisterServerKeys(
    clsid: PyIID, progID: str | None = None, verProgID: str | None = None, customKeys: Iterable[tuple[str, _T]] | None = None
) -> list[tuple[str, _T | int]]:
    """
    Given a server, return a list of of ("key", root), which are keys recursively
    and uncondtionally deleted at unregister or uninstall time.
    """
    ...
def UnregisterServer(
    clsid: PyIID,
    progID: str | None = None,
    verProgID: str | None = None,
    customKeys: Iterable[tuple[str, PyHKEY | int]] | None = None,
) -> None:
    """Unregisters a Python COM server."""
    ...
def GetRegisteredServerOption(clsid: PyIID, optionName: str) -> str | None:
    """Given a CLSID for a server and option name, return the option value"""
    ...
def RegisterClasses(*classes: type[_RegisterClass], **flags: Unpack[_RegisterFlag]) -> None: ...
def UnregisterClasses(*classes: type[_RegisterClass], **flags: Unpack[_UnregisterFlag]) -> None: ...
def UnregisterInfoClasses(*classes: type[_RegisterClass]) -> list[tuple[str, PyHKEY | int]]: ...
def ReExecuteElevated(flags: _ElevatedFlag) -> None: ...
def UseCommandLine(*classes: type[_RegisterClass], **flags: Unpack[_CommandFlag]) -> list[tuple[str, PyHKEY | int]] | None: ...
def RegisterPyComCategory() -> None:
    """Register the Python COM Server component category."""
    ...

"""A module that exposes the Windows Networking API."""

from _typeshed import Incomplete

import _win32typing
from win32.lib.pywintypes import error as error

def NCBBuffer(size, /):
    """Creates a memory buffer"""
    ...
def Netbios(ncb: _win32typing.NCB, /):
    """Calls the windows Netbios function"""
    ...
def WNetAddConnection2(
    NetResource: _win32typing.PyNETRESOURCE,
    Password: Incomplete | None = ...,
    UserName: Incomplete | None = ...,
    Flags: int = ...,
) -> None:
    """WNetAddConnection2(NetResource, Password, UserName, Flags)"""
    ...
def WNetAddConnection3(
    HwndOwner: int | _win32typing.PyHANDLE,
    NetResource: _win32typing.PyNETRESOURCE,
    Password: Incomplete | None = ...,
    UserName: Incomplete | None = ...,
    Flags: int = ...,
) -> None:
    """WNetAddConnection3(HwndParent, NetResource, Password, UserName, Flags)"""
    ...
def WNetCancelConnection2(name: str, flags, force, /) -> None:
    """localname,dwflags,bforce"""
    ...
def WNetOpenEnum(scope, _type, usage, resource: _win32typing.PyNETRESOURCE, /) -> _win32typing.PyHANDLE:
    """dwScope,dwType,dwUsage,NETRESOURCE - returns PyHANDLE"""
    ...
def WNetCloseEnum(handle: _win32typing.PyHANDLE, /) -> None:
    """PyHANDLE from WNetOpenEnum()"""
    ...
def WNetEnumResource(handle: _win32typing.PyHANDLE, maxExtries: int = ..., /) -> list[_win32typing.PyNETRESOURCE]:
    """Enum"""
    ...
def WNetGetUser(connection: str | None = ..., /) -> str:
    """connectionName=None"""
    ...
def WNetGetUniversalName(localPath: str, infoLevel, /) -> str:
    """localPath, infoLevel=UNIVERSAL_NAME_INFO_LEVEL"""
    ...
def WNetGetResourceInformation(NetResource: _win32typing.PyNETRESOURCE, /) -> tuple[_win32typing.PyNETRESOURCE, Incomplete]:
    """Finds the type and provider of a network resource"""
    ...
def WNetGetLastError() -> tuple[Incomplete, Incomplete, Incomplete]:
    """Retrieves extended error information set by a network provider when one of the WNet* functions fails"""
    ...
def WNetGetResourceParent(NetResource: _win32typing.PyNETRESOURCE, /) -> _win32typing.PyNETRESOURCE:
    """Finds the parent resource of a network resource"""
    ...
def WNetGetConnection(connection: str | None = ..., /) -> str:
    """Retrieves the name of the network resource associated with a local device"""
    ...

NETRESOURCE = _win32typing.PyNETRESOURCE
NCB = _win32typing.PyNCB
# old "deprecated" names, before types could create instances.
NETRESOURCEType = _win32typing.PyNETRESOURCE
NCBType = _win32typing.PyNCB

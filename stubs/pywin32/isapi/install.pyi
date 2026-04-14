"""Installation utilities for Python ISAPI filters and extensions."""

from _typeshed import Incomplete, StrOrBytesPath, StrPath, SupportsGetItem, Unused
from collections.abc import Callable, Iterable, Mapping
from optparse import OptionParser
from typing import Final, Literal

this_dir: str

class FilterParameters:
    Name: Incomplete
    Description: Incomplete
    Path: Incomplete
    Server: Incomplete
    AddExtensionFile: bool
    AddExtensionFile_Enabled: bool
    AddExtensionFile_GroupID: Incomplete
    AddExtensionFile_CanDelete: bool
    AddExtensionFile_Description: Incomplete
    def __init__(self, **kw) -> None: ...

class VirtualDirParameters:
    Name: Incomplete
    Description: Incomplete
    AppProtection: Incomplete
    Headers: Incomplete
    Path: Incomplete
    Type: Incomplete
    AccessExecute: Incomplete
    AccessRead: Incomplete
    AccessWrite: Incomplete
    AccessScript: Incomplete
    ContentIndexed: Incomplete
    EnableDirBrowsing: Incomplete
    EnableDefaultDoc: Incomplete
    DefaultDoc: Incomplete
    ScriptMaps: list[ScriptMapParams]
    ScriptMapUpdate: str
    Server: Incomplete
    def __init__(self, **kw) -> None: ...
    def is_root(self) -> bool:
        """This virtual directory is a root directory if parent and name are blank"""
        ...
    def split_path(self) -> list[str]: ...

class ScriptMapParams:
    Extension: Incomplete
    Module: Incomplete
    Flags: int
    Verbs: str
    AddExtensionFile: bool
    AddExtensionFile_Enabled: bool
    AddExtensionFile_GroupID: Incomplete
    AddExtensionFile_CanDelete: bool
    AddExtensionFile_Description: Incomplete
    def __init__(self, **kw) -> None: ...

class ISAPIParameters:
    ServerName: Incomplete
    Filters: list[FilterParameters]
    VirtualDirs: list[VirtualDirParameters]
    def __init__(self, **kw) -> None: ...

verbose: int

def log(level: int, what: object) -> None: ...

class InstallationError(Exception): ...
class ItemNotFound(InstallationError): ...
class ConfigurationError(InstallationError): ...

def FindPath(options, server: str | bytes | bytearray, name: str) -> str: ...
def LocateWebServerPath(description: str):
    """
    Find an IIS web server whose name or comment matches the provided
    description (case-insensitive).

    >>> LocateWebServerPath('Default Web Site') # doctest: +SKIP

    or

    >>> LocateWebServerPath('1') #doctest: +SKIP
    """
    ...
def GetWebServer(description: str | None = None):
    """
    Load the web server instance (COM object) for a given instance
    or description.
    If None is specified, the default website is retrieved (indicated
    by the identifier 1.
    """
    ...
def LoadWebServer(path): ...
def FindWebServer(options, server_desc: str | bytes | bytearray | None) -> str:
    """
    Legacy function to allow options to define a .server property
    to override the other parameter.  Use GetWebServer instead.
    """
    ...
def split_path(path: str) -> list[str]:
    """
    Get the parent path and basename.

    >>> split_path('/')
    ['', '']

    >>> split_path('')
    ['', '']

    >>> split_path('foo')
    ['', 'foo']

    >>> split_path('/foo')
    ['', 'foo']

    >>> split_path('/foo/bar')
    ['/foo', 'bar']

    >>> split_path('foo/bar')
    ['/foo', 'bar']
    """
    ...
def CreateDirectory(params, options): ...
def AssignScriptMaps(script_maps: Iterable[ScriptMapParams], target, update: str = "replace") -> None:
    """
    Updates IIS with the supplied script map information.

    script_maps is a list of ScriptMapParameter objects

    target is an IIS Virtual Directory to assign the script maps to

    update is a string indicating how to update the maps, one of  ('start',
    'end', or 'replace')
    """
    ...
def get_unique_items(sequence, reference):
    """Return items in sequence that can't be found in reference."""
    ...
def CreateISAPIFilter(filterParams, options): ...
def DeleteISAPIFilter(filterParams, options) -> None: ...
def AddExtensionFiles(params, options) -> None:
    """
    Register the modules used by the filters/extensions as a trusted
    'extension module' - required by the default IIS6 security settings.
    """
    ...
def DeleteExtensionFileRecords(params, options) -> None: ...
def CheckLoaderModule(dll_name: StrOrBytesPath) -> None: ...
def Install(params, options) -> None: ...
def RemoveDirectory(params, options) -> None: ...
def RemoveScriptMaps(vd_params, options) -> None:
    """Remove script maps from the already installed virtual directory"""
    ...
def Uninstall(params, options) -> None: ...
def GetLoaderModuleName(mod_name: StrPath, check_module: bool | None = None) -> str: ...
def InstallModule(conf_module_name: StrPath, params, options, log: Callable[[int, str], Unused] = ...) -> None:
    """Install the extension"""
    ...
def UninstallModule(conf_module_name: StrPath, params, options, log: Callable[[int, str], Unused] = ...) -> None:
    """Remove the extension"""
    ...

standard_arguments: Final[dict[Literal["install", "remove"], Callable[..., Incomplete]]]

def build_usage(handler_map: Mapping[str, object]) -> str: ...
def MergeStandardOptions(options, params) -> None:
    """
    Take an options object generated by the command line and merge
    the values into the IISParameters object.
    """
    ...
def HandleCommandLine(
    params,
    argv: SupportsGetItem[int, str] | None = None,
    conf_module_name: str | None = None,
    default_arg: str = "install",
    opt_parser: OptionParser | None = None,
    custom_arg_handlers: Mapping[str, object] = {},
) -> None:
    """
    Perform installation or removal of an ISAPI filter or extension.

    This module handles standard command-line options and configuration
    information, and installs, removes or updates the configuration of an
    ISAPI filter or extension.

    You must pass your configuration information in params - all other
    arguments are optional, and allow you to configure the installation
    process.
    """
    ...

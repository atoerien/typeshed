"""
Manages the cache of generated Python code.

Description
  This file manages the cache of generated Python code.  When run from the
  command line, it also provides a number of options for managing that cache.

Implementation
  Each typelib is generated into a filename of format "{guid}x{lcid}x{major}x{minor}.py"

  An external persistant dictionary maps from all known IIDs in all known type libraries
  to the type library itself.

  Thus, whenever Python code knows the IID of an object, it can find the IID, LCID and version of
  the type library which supports it.  Given this information, it can find the Python module
  with the support.

  If necessary, this support can be generated on the fly.

Hacks, to do, etc
  Currently just uses a pickled dictionary, but should used some sort of indexed file.
  Maybe an OLE2 compound file, or a bsddb file?
"""

from _typeshed import Incomplete, Unused
from collections.abc import Generator
from contextlib import contextmanager
from types import ModuleType
from typing import Literal, NoReturn

from win32.lib.pywintypes import IIDType
from win32com.client import dynamic

bForDemandDefault: int
clsidToTypelib: dict[str, tuple[str, int, int, int]]
versionRedirectMap: dict[tuple[str, int, int, int], ModuleType | None]
is_readonly: bool
is_zip: bool
demandGeneratedTypeLibraries: dict[tuple[str, int, int, int], Incomplete]

def __init__() -> None: ...

pickleVersion: int

@contextmanager
def ModuleMutex(module_name: str) -> Generator[None]:
    """
    Given the output of GetGeneratedFilename, acquire a named mutex for that module

    This is required so that writes (generation) don't interfere with each other and with reads (import)
    """
    ...
def GetGeneratedFileName(clsid, lcid, major, minor) -> str:
    """
    Given the clsid, lcid, major and  minor for a type lib, return
    the file name (no extension) providing this support.
    """
    ...
def SplitGeneratedFileName(fname: str) -> tuple[str, ...]:
    """Reverse of GetGeneratedFileName()"""
    ...
def GetGeneratePath() -> str:
    """
    Returns the name of the path to generate to.
    Checks the directory is OK.
    """
    ...
def GetClassForProgID(progid: str) -> type | None:
    """
    Get a Python class for a Program ID

    Given a Program ID, return a Python class which wraps the COM object

    Returns the Python class, or None if no module is available.

    Params
    progid -- A COM ProgramID or IID (eg, "Word.Application")
    """
    ...
def GetClassForCLSID(clsid) -> type | None:
    """
    Get a Python class for a CLSID

    Given a CLSID, return a Python class which wraps the COM object

    Returns the Python class, or None if no module is available.

    Params
    clsid -- A COM CLSID (or string repr of one)
    """
    ...
def GetModuleForProgID(progid: str) -> ModuleType | None:
    """
    Get a Python module for a Program ID

    Given a Program ID, return a Python module which contains the
    class which wraps the COM object.

    Returns the Python module, or None if no module is available.

    Params
    progid -- A COM ProgramID or IID (eg, "Word.Application")
    """
    ...
def GetModuleForCLSID(clsid) -> ModuleType | None:
    """
    Get a Python module for a CLSID

    Given a CLSID, return a Python module which contains the
    class which wraps the COM object.

    Returns the Python module, or None if no module is available.

    Params
    progid -- A COM CLSID (ie, not the description)
    """
    ...
def GetModuleForTypelib(typelibCLSID, lcid, major, minor) -> ModuleType:
    """
    Get a Python module for a type library ID

    Given the CLSID of a typelibrary, return an imported Python module,
    else None

    Params
    typelibCLSID -- IID of the type library.
    major -- Integer major version.
    minor -- Integer minor version
    lcid -- Integer LCID for the library.
    """
    ...
def MakeModuleForTypelib(
    typelibCLSID,
    lcid,
    major,
    minor,
    progressInstance=None,
    bForDemand: bool | Literal[0, 1] = ...,
    bBuildHidden: bool | Literal[0, 1] = 1,
) -> ModuleType:
    """
    Generate support for a type library.

    Given the IID, LCID and version information for a type library, generate
    and import the necessary support files.

    Returns the Python module.  No exceptions are caught.

    Params
    typelibCLSID -- IID of the type library.
    major -- Integer major version.
    minor -- Integer minor version.
    lcid -- Integer LCID for the library.
    progressInstance -- Instance to use as progress indicator, or None to
                        use the GUI progress bar.
    """
    ...
def MakeModuleForTypelibInterface(
    typelib_ob, progressInstance=None, bForDemand: bool | Literal[0, 1] = ..., bBuildHidden: bool | Literal[0, 1] = 1
) -> ModuleType | None:
    """
    Generate support for a type library.

    Given a PyITypeLib interface generate and import the necessary support files.  This is useful
    for getting makepy support for a typelibrary that is not registered - the caller can locate
    and load the type library itself, rather than relying on COM to find it.

    Returns the Python module.

    Params
    typelib_ob -- The type library itself
    progressInstance -- Instance to use as progress indicator, or None to
                        use the GUI progress bar.
    """
    ...
def EnsureModuleForTypelibInterface(
    typelib_ob, progressInstance=None, bForDemand: bool | Literal[0, 1] = ..., bBuildHidden: bool | Literal[0, 1] = 1
) -> ModuleType | None:
    """
    Check we have support for a type library, generating if not.

    Given a PyITypeLib interface generate and import the necessary
    support files if necessary. This is useful for getting makepy support
    for a typelibrary that is not registered - the caller can locate and
    load the type library itself, rather than relying on COM to find it.

    Returns the Python module.

    Params
    typelib_ob -- The type library itself
    progressInstance -- Instance to use as progress indicator, or None to
                        use the GUI progress bar.
    """
    ...
def ForgetAboutTypelibInterface(typelib_ob) -> None:
    """Drop any references to a typelib previously added with EnsureModuleForTypelibInterface and forDemand"""
    ...
def EnsureModule(
    typelibCLSID,
    lcid,
    major,
    minor,
    progressInstance=None,
    bValidateFile: bool | Literal[0, 1] = ...,
    bForDemand: bool | Literal[0, 1] = ...,
    bBuildHidden: bool | Literal[0, 1] = 1,
) -> ModuleType | None:
    """
    Ensure Python support is loaded for a type library, generating if necessary.

    Given the IID, LCID and version information for a type library, check and if
    necessary (re)generate, then import the necessary support files. If we regenerate the file, there
    is no way to totally snuff out all instances of the old module in Python, and thus we will regenerate the file more than necessary,
    unless makepy/genpy is modified accordingly.


    Returns the Python module.  No exceptions are caught during the generate process.

    Params
    typelibCLSID -- IID of the type library.
    major -- Integer major version.
    minor -- Integer minor version
    lcid -- Integer LCID for the library.
    progressInstance -- Instance to use as progress indicator, or None to
                        use the GUI progress bar.
    bValidateFile -- Whether or not to perform cache validation or not
    bForDemand -- Should a complete generation happen now, or on demand?
    bBuildHidden -- Should hidden members/attributes etc be generated?
    """
    ...
def EnsureDispatch(
    prog_id: str | dynamic.PyIDispatchType | IIDType | dynamic.PyIUnknownType, bForDemand: bool | Literal[0, 1] = 1
) -> dynamic.CDispatch:
    """Given a COM prog_id, return an object that is using makepy support, building if necessary"""
    ...
def AddModuleToCache(typelibclsid, lcid, major, minor, verbose: Unused = 1, bFlushNow: bool | Literal[0, 1] = ...) -> None:
    """Add a newly generated file to the cache dictionary."""
    ...
def GetGeneratedInfos() -> list[tuple[Incomplete, Incomplete, Incomplete, Incomplete]]: ...
def Rebuild(verbose: bool | Literal[0, 1] = 1) -> None:
    """Rebuild the cache indexes from the file system."""
    ...
def usage() -> NoReturn: ...

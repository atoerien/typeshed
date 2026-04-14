from _typeshed import Incomplete

CLSIDPyFile: str
RegistryIDPyFile: str
RegistryIDPycFile: str

def BuildDefaultPythonKey():
    """
    Builds a string containing the path to the current registry key.

    The Python registry key contains the Python version.  This function
    uses the version of the DLL used by the current process to get the
    registry key currently in use.
    """
    ...
def GetRootKey():
    """Retrieves the Registry root in use by Python."""
    ...
def GetRegistryDefaultValue(subkey, rootkey: Incomplete | None = ...):
    """A helper to return the default value for a key in the registry."""
    ...
def SetRegistryDefaultValue(subKey, value, rootkey: Incomplete | None = ...) -> None:
    """A helper to set the default value for a key in the registry"""
    ...
def GetAppPathsKey(): ...
def RegisterPythonExe(exeFullPath, exeAlias: Incomplete | None = ..., exeAppPath: Incomplete | None = ...) -> None:
    """
    Register a .exe file that uses Python.

    Registers the .exe with the OS.  This allows the specified .exe to
    be run from the command-line or start button without using the full path,
    and also to setup application specific path (ie, os.environ['PATH']).

    Currently the exeAppPath is not supported, so this function is general
    purpose, and not specific to Python at all.  Later, exeAppPath may provide
    a reasonable default that is used.

    exeFullPath -- The full path to the .exe
    exeAlias = None -- An alias for the exe - if none, the base portion
              of the filename is used.
    exeAppPath -- Not supported.
    """
    ...
def GetRegisteredExe(exeAlias):
    """Get a registered .exe"""
    ...
def UnregisterPythonExe(exeAlias) -> None:
    """Unregister a .exe file that uses Python."""
    ...
def RegisterNamedPath(name, path) -> None:
    """Register a named path - ie, a named PythonPath entry."""
    ...
def UnregisterNamedPath(name) -> None:
    """Unregister a named path - ie, a named PythonPath entry."""
    ...
def GetRegisteredNamedPath(name):
    """Get a registered named path, or None if it doesn't exist."""
    ...
def RegisterModule(modName, modPath) -> None:
    """
    Register an explicit module in the registry.  This forces the Python import
    mechanism to locate this module directly, without a sys.path search.  Thus
    a registered module need not appear in sys.path at all.

    modName -- The name of the module, as used by import.
    modPath -- The full path and file name of the module.
    """
    ...
def UnregisterModule(modName) -> None:
    """
    Unregister an explicit module in the registry.

    modName -- The name of the module, as used by import.
    """
    ...
def GetRegisteredHelpFile(helpDesc):
    """Given a description, return the registered entry."""
    ...
def RegisterHelpFile(helpFile, helpPath, helpDesc: Incomplete | None = ..., bCheckFile: int = ...) -> None:
    """
    Register a help file in the registry.

      Note that this used to support writing to the Windows Help
      key, however this is no longer done, as it seems to be incompatible.

    helpFile -- the base name of the help file.
    helpPath -- the path to the help file
    helpDesc -- A description for the help file.  If None, the helpFile param is used.
    bCheckFile -- A flag indicating if the file existence should be checked.
    """
    ...
def UnregisterHelpFile(helpFile, helpDesc: Incomplete | None = ...) -> None:
    """
    Unregister a help file in the registry.

    helpFile -- the base name of the help file.
    helpDesc -- A description for the help file.  If None, the helpFile param is used.
    """
    ...
def RegisterCoreDLL(coredllName: Incomplete | None = ...) -> None:
    """
    Registers the core DLL in the registry.

    If no params are passed, the name of the Python DLL used in
    the current process is used and registered.
    """
    ...
def RegisterFileExtensions(defPyIcon, defPycIcon, runCommand) -> None:
    """
    Register the core Python file extensions.

    defPyIcon -- The default icon to use for .py files, in 'fname,offset' format.
    defPycIcon -- The default icon to use for .pyc files, in 'fname,offset' format.
    runCommand -- The command line to use for running .py files
    """
    ...
def RegisterShellCommand(shellCommand, exeCommand, shellUserCommand: Incomplete | None = ...) -> None: ...
def RegisterDDECommand(shellCommand, ddeApp, ddeTopic, ddeCommand) -> None: ...

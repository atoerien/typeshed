from _typeshed import Incomplete

from win32comext.axdebug import gateways
from win32comext.axdebug.codecontainer import SourceCodeContainer

debuggingTrace: int

def trace(*args) -> None:
    """A function used instead of "print" for debugging output."""
    ...

class DebugManager:
    scriptEngine: Incomplete
    adb: Incomplete
    rootNode: Incomplete
    debugApplication: Incomplete
    ccProvider: Incomplete
    scriptSiteDebug: Incomplete
    activeScriptDebug: Incomplete
    codeContainers: Incomplete
    def __init__(self, scriptEngine) -> None: ...
    def Close(self) -> None: ...
    def IsAnyHost(self):
        """Do we have _any_ debugging interfaces installed?"""
        ...
    def IsSimpleHost(self): ...
    def HandleRuntimeError(self):
        """
        Called by the engine when a runtime error occurs.  If we have a debugger,
        we let it know.

        The result is a boolean which indicates if the error handler should call
        IActiveScriptSite::OnScriptError()
        """
        ...
    def OnEnterScript(self) -> None: ...
    def OnLeaveScript(self) -> None: ...
    def AddScriptBlock(self, codeBlock) -> None: ...

class DebugCodeBlockContainer(SourceCodeContainer):
    codeBlock: Incomplete
    def __init__(self, codeBlock, site) -> None: ...
    def GetName(self, dnt): ...

class EnumDebugCodeContexts(gateways.EnumDebugCodeContexts): ...

class ActiveScriptDebug:
    """
    The class which implements the IActiveScriptDebug interface for the Active Script engine.

    Only ever used by smart hosts.
    """
    debugMgr: Incomplete
    scriptSiteDebug: Incomplete
    codeContainers: Incomplete
    def __init__(self, debugMgr, codeContainers) -> None: ...
    def GetScriptTextAttributes(self, code, delim, flags): ...
    def GetScriptletTextAttributes(self, code, delim, flags): ...
    def EnumCodeContextsOfPosition(self, context, charOffset, numChars): ...

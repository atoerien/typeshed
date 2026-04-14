"""
Exception and error handling.

This contains the core exceptions that the implementations should raise
as well as the IActiveScriptError interface code.
"""

from types import TracebackType

from win32com.server.exception import COMException
from win32comext.axscript.client.debug import DebugManager
from win32comext.axscript.client.framework import AXScriptCodeBlock, COMScript
from win32comext.axscript.server.axsite import AXSite

debugging: int

def FormatForAX(text: str) -> str:
    """Format a string suitable for an AX Host"""
    ...
def ExpandTabs(text: str) -> str: ...
def AddCR(text: str) -> str: ...

class IActiveScriptError:
    """
    An implementation of IActiveScriptError

    The ActiveX Scripting host calls this client whenever we report
    an exception to it.  This interface provides the exception details
    for the host to report to the user.
    """
    def GetSourceLineText(self) -> str | None: ...
    def GetSourcePosition(self) -> tuple[int, int, int]: ...
    def GetExceptionInfo(self) -> AXScriptException: ...

class AXScriptException(COMException):
    """
    A class used as a COM exception.

    Note this has attributes which conform to the standard attributes
    for COM exceptions, plus a few others specific to our IActiveScriptError
    object.
    """
    sourceContext: int
    startLineNo: int
    linetext: str
    def __init__(
        self,
        site: COMScript,
        codeBlock: AXScriptCodeBlock | None,
        exc_type: None = None,
        exc_value: BaseException | None = None,
        exc_traceback: None = None,
    ) -> None: ...
    def ExtractTracebackInfo(self, tb: TracebackType, site: COMScript) -> tuple[str, int, str, str | None]: ...

def ProcessAXScriptException(
    scriptingSite: AXSite, debugManager: DebugManager, exceptionInstance: AXScriptException
) -> None | COMException | AXScriptException:
    """
    General function to handle any exception in AX code

    This function creates an instance of our IActiveScriptError interface, and
    gives it to the host, along with out exception class.  The host will
    likely call back on the IActiveScriptError interface to get the source text
    and other information not normally in COM exceptions.
    """
    ...

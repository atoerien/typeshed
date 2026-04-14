from _typeshed import Incomplete

from win32com.server.util import ListEnumeratorGateway

class EnumDebugCodeContexts(ListEnumeratorGateway):
    """
    A class to expose a Python sequence as an EnumDebugCodeContexts

    Create an instance of this class passing a sequence (list, tuple, or
    any sequence protocol supporting object) and it will automatically
    support the EnumDebugCodeContexts interface for the object.
    """
    ...
class EnumDebugStackFrames(ListEnumeratorGateway):
    """
    A class to expose a Python sequence as an EnumDebugStackFrames

    Create an instance of this class passing a sequence (list, tuple, or
    any sequence protocol supporting object) and it will automatically
    support the EnumDebugStackFrames interface for the object.
    """
    ...
class EnumDebugApplicationNodes(ListEnumeratorGateway):
    """
    A class to expose a Python sequence as an EnumDebugStackFrames

    Create an instance of this class passing a sequence (list, tuple, or
    any sequence protocol supporting object) and it will automatically
    support the EnumDebugApplicationNodes interface for the object.
    """
    ...
class EnumRemoteDebugApplications(ListEnumeratorGateway): ...
class EnumRemoteDebugApplicationThreads(ListEnumeratorGateway): ...

class DebugDocumentInfo:
    def GetName(self, dnt) -> None:
        """
        Get the one of the name of the document
        dnt -- int DOCUMENTNAMETYPE
        """
        ...
    def GetDocumentClassId(self) -> None:
        """Result must be an IID object (or string representing one)."""
        ...

class DebugDocumentProvider(DebugDocumentInfo):
    def GetDocument(self) -> None: ...

class DebugApplicationNode(DebugDocumentProvider):
    """Provides the functionality of IDebugDocumentProvider, plus a context within a project tree."""
    def EnumChildren(self) -> None: ...
    def GetParent(self) -> None: ...
    def SetDocumentProvider(self, pddp) -> None: ...
    def Close(self) -> None: ...
    def Attach(self, parent) -> None: ...
    def Detach(self) -> None: ...

class DebugApplicationNodeEvents:
    """Event interface for DebugApplicationNode object."""
    def onAddChild(self, child) -> None: ...
    def onRemoveChild(self, child) -> None: ...
    def onDetach(self) -> None: ...
    def onAttach(self, parent) -> None: ...

class DebugDocument(DebugDocumentInfo):
    """The base interface to all debug documents."""
    ...

class DebugDocumentText(DebugDocument):
    """The interface to a text only debug document."""
    def GetDocumentAttributes(self) -> None: ...
    def GetSize(self) -> None: ...
    def GetPositionOfLine(self, cLineNumber) -> None: ...
    def GetLineOfPosition(self, charPos) -> None: ...
    def GetText(self, charPos, maxChars, wantAttr) -> None:
        """
        Params
        charPos -- integer
        maxChars -- integer
        wantAttr -- Should the function compute attributes.

        Return value must be (string, attribtues).  attributes may be
        None if(not wantAttr)
        """
        ...
    def GetPositionOfContext(self, debugDocumentContext) -> None:
        """
        Params
        debugDocumentContext -- a PyIDebugDocumentContext object.

        Return value must be (charPos, numChars)
        """
        ...
    def GetContextOfPosition(self, charPos, maxChars) -> None:
        """
        Params are integers.
        Return value must be PyIDebugDocumentContext object
        """
        ...

class DebugDocumentTextExternalAuthor:
    """Allow external editors to edit file-based debugger documents, and to notify the document when the source file has been changed."""
    def GetPathName(self) -> None:
        """
        Return the full path (including file name) to the document's source file.

        Result must be (filename, fIsOriginal), where
        - if fIsOriginalPath is TRUE if the path refers to the original file for the document.
        - if fIsOriginalPath is FALSE if the path refers to a newly created temporary file.

        raise COMException(winerror.E_FAIL) if no source file can be created/determined.
        """
        ...
    def GetFileName(self) -> None:
        """
        Return just the name of the document, with no path information.  (Used for "Save As...")

        Result is a string
        """
        ...
    def NotifyChanged(self) -> None:
        """
        Notify the host that the document's source file has been saved and
        that its contents should be refreshed.
        """
        ...

class DebugDocumentTextEvents:
    def onDestroy(self) -> None: ...
    def onInsertText(self, cCharacterPosition, cNumToInsert) -> None: ...
    def onRemoveText(self, cCharacterPosition, cNumToRemove) -> None: ...
    def onReplaceText(self, cCharacterPosition, cNumToReplace) -> None: ...
    def onUpdateTextAttributes(self, cCharacterPosition, cNumToUpdate) -> None: ...
    def onUpdateDocumentAttributes(self, textdocattr) -> None: ...

class DebugDocumentContext:
    def GetDocument(self) -> None:
        """Return value must be a PyIDebugDocument object"""
        ...
    def EnumCodeContexts(self) -> None:
        """Return value must be a PyIEnumDebugCodeContexts object"""
        ...

class DebugCodeContext:
    def GetDocumentContext(self) -> None:
        """Return value must be a PyIDebugDocumentContext object"""
        ...
    def SetBreakPoint(self, bps) -> None:
        """bps -- an integer with flags."""
        ...

class DebugStackFrame:
    """Abstraction representing a logical stack frame on the stack of a thread."""
    def GetCodeContext(self) -> None:
        """
        Returns the current code context associated with the stack frame.

        Return value must be a IDebugCodeContext object
        """
        ...
    def GetDescriptionString(self, fLong) -> None:
        """
        Returns a textual description of the stack frame.

        fLong -- A flag indicating if the long name is requested.
        """
        ...
    def GetLanguageString(self) -> None:
        """
        Returns a short or long textual description of the language.

        fLong -- A flag indicating if the long name is requested.
        """
        ...
    def GetThread(self) -> None:
        """
        Returns the thread associated with this stack frame.

        Result must be a IDebugApplicationThread
        """
        ...
    def GetDebugProperty(self) -> None: ...

class DebugDocumentHost:
    """
    The interface from the IDebugDocumentHelper back to
    the smart host or language engine.  This interface
    exposes host specific functionality such as syntax coloring.
    """
    def GetDeferredText(self, dwTextStartCookie, maxChars, bWantAttr) -> None: ...
    def GetScriptTextAttributes(self, codeText, delimterText, flags) -> None: ...
    def OnCreateDocumentContext(self) -> None: ...
    def GetPathName(self) -> None: ...
    def GetFileName(self) -> None: ...
    def NotifyChanged(self) -> None: ...

class DebugDocumentTextConnectServer:
    cookieNo: int
    connections: Incomplete
    def EnumConnections(self) -> None: ...
    def GetConnectionInterface(self) -> None: ...
    def GetConnectionPointContainer(self): ...
    def Advise(self, pUnk): ...
    def Unadvise(self, cookie): ...
    def EnumConnectionPoints(self) -> None: ...
    def FindConnectionPoint(self, iid): ...

class RemoteDebugApplicationEvents:
    def OnConnectDebugger(self, appDebugger) -> None:
        """appDebugger -- a PyIApplicationDebugger"""
        ...
    def OnDisconnectDebugger(self) -> None: ...
    def OnSetName(self, name) -> None: ...
    def OnDebugOutput(self, string) -> None: ...
    def OnClose(self) -> None: ...
    def OnEnterBreakPoint(self, rdat) -> None:
        """rdat -- PyIRemoteDebugApplicationThread"""
        ...
    def OnLeaveBreakPoint(self, rdat) -> None:
        """rdat -- PyIRemoteDebugApplicationThread"""
        ...
    def OnCreateThread(self, rdat) -> None:
        """rdat -- PyIRemoteDebugApplicationThread"""
        ...
    def OnDestroyThread(self, rdat) -> None:
        """rdat -- PyIRemoteDebugApplicationThread"""
        ...
    def OnBreakFlagChange(self, abf, rdat) -> None:
        """
        abf -- int - one of the axdebug.APPBREAKFLAGS constants
        rdat -- PyIRemoteDebugApplicationThread
        RaiseNotImpl("OnBreakFlagChange")
        """
        ...

class DebugExpressionContext:
    def ParseLanguageText(self, code, radix, delim, flags) -> None:
        """result is IDebugExpression"""
        ...
    def GetLanguageInfo(self) -> None:
        """result is (string langName, iid langId)"""
        ...

class DebugExpression:
    def Start(self, callback) -> None:
        """
        callback -- an IDebugExpressionCallback

        result - void
        """
        ...
    def Abort(self) -> None:
        """
        no params
        result -- void
        """
        ...
    def QueryIsComplete(self) -> None:
        """
        no params
        result -- void
        """
        ...
    def GetResultAsString(self) -> None: ...
    def GetResultAsDebugProperty(self) -> None: ...

class ProvideExpressionContexts:
    def EnumExpressionContexts(self) -> None: ...

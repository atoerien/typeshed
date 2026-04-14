"""
Exception Handling

Exceptions

    To better support COM exceptions, the framework allows for an instance to be
    raised.  This instance may have a certain number of known attributes, which are
    translated into COM exception details.

    This means, for example, that Python could raise a COM exception that includes details
    on a Help file and location, and a description for the user.

    This module provides a class which provides the necessary attributes.
"""

import pythoncom

class COMException(pythoncom.com_error):
    """
    An Exception object that is understood by the framework.

    If the framework is presented with an exception of type class,
    it looks for certain known attributes on this class to provide rich
    error information to the caller.

    It should be noted that the framework supports providing this error
    information via COM Exceptions, or via the ISupportErrorInfo interface.

    By using this class, you automatically provide rich error information to the
    server.
    """
    scode: int
    description: str
    source: str | None
    helpfile: str | None
    helpcontext: int | None
    def __init__(
        self,
        description: str | None = None,
        scode: int | None = None,
        source: str | None = None,
        helpfile: str | None = None,
        helpContext: int | None = None,
        desc: str | None = None,
        hresult: int | None = None,
    ) -> None:
        """
        Initialize an exception
        **Params**

        description -- A string description for the exception.
        scode -- An integer scode to be returned to the server, if necessary.
        The pythoncom framework defaults this to be DISP_E_EXCEPTION if not specified otherwise.
        source -- A string which identifies the source of the error.
        helpfile -- A string which points to a help file which contains details on the error.
        helpContext -- An integer context in the help file.
        desc -- A short-cut for description.
        hresult -- A short-cut for scode.
        """
        ...

def IsCOMException(t: type[BaseException] | None = None) -> bool: ...
def IsCOMServerException(t: type[BaseException] | None = None) -> bool: ...

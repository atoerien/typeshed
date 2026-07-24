from typing_extensions import Never
from xml.sax.xmlreader import Locator

class SAXException(Exception):
    def __init__(self, msg: str, exception: Exception | None = None) -> None: ...
    def getMessage(self) -> str: ...
    def getException(self) -> Exception | None: ...
    def __getitem__(self, ix: object) -> Never: ...

class SAXParseException(SAXException):
    """
    Encapsulate an XML parse error or warning.

    This exception will include information for locating the error in
    the original XML document. Note that although the application will
    receive a SAXParseException as the argument to the handlers in the
    ErrorHandler interface, the application is not actually required
    to raise the exception; instead, it can simply read the
    information in it and take a different action.

    Since this exception is a subclass of SAXException, it inherits
    the ability to wrap another exception.
    """
    def __init__(self, msg: str, exception: Exception | None, locator: Locator) -> None:
        """Creates the exception. The exception parameter is allowed to be None."""
        ...
    def getColumnNumber(self) -> int | None:
        """
        The column number of the end of the text where the exception
        occurred.
        """
        ...
    def getLineNumber(self) -> int | None:
        """The line number of the end of the text where the exception occurred."""
        ...
    def getPublicId(self) -> str | None:
        """Get the public identifier of the entity where the exception occurred."""
        ...
    def getSystemId(self) -> str | None:
        """Get the system identifier of the entity where the exception occurred."""
        ...

class SAXNotRecognizedException(SAXException):
    """
    Exception class for an unrecognized identifier.

    An XMLReader will raise this exception when it is confronted with an
    unrecognized feature or property. SAX applications and extensions may
    use this class for similar purposes.
    """
    ...
class SAXNotSupportedException(SAXException):
    """
    Exception class for an unsupported operation.

    An XMLReader will raise this exception when a service it cannot
    perform is requested (specifically setting a state or value). SAX
    applications and extensions may use this class for similar
    purposes.
    """
    ...
class SAXReaderNotAvailable(SAXNotSupportedException):
    """
    Exception class for a missing driver.

    An XMLReader module (driver) should raise this exception when it
    is first imported, e.g. when a support module cannot be imported.
    It also may be raised during parsing, e.g. if executing an external
    program is not permitted.
    """
    ...

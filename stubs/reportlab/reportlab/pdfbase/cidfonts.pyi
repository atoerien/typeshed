"""
CID (Asian multi-byte) font support.

This defines classes to represent CID fonts.  They know how to calculate
their own width and how to write themselves into PDF files.
"""

from _typeshed import Incomplete
from typing import Final, Literal

from reportlab.pdfbase import pdfmetrics

__version__: Final[str]
DISABLE_CMAP: bool

def findCMapFile(name: str) -> str: ...
def structToPDF(structure): ...

class CIDEncoding(pdfmetrics.Encoding):
    """
    Multi-byte encoding.  These are loaded from CMAP files.

    A CMAP file is like a mini-codec.  It defines the correspondence
    between code points in the (multi-byte) input data and Character
    IDs. 
    """
    name: Incomplete
    source: str | None
    def __init__(self, name, useCache: bool | Literal[0, 1] = 1) -> None: ...
    def parseCMAPFile(self, name) -> None: ...
    def translate(self, text) -> list[Incomplete]: ...
    def fastSave(self, directory) -> None: ...
    def fastLoad(self, directory) -> None: ...
    def getData(self) -> dict[str, Incomplete]: ...

class CIDTypeFace(pdfmetrics.TypeFace):
    """
    Multi-byte type face.

    Conceptually similar to a single byte typeface,
    but the glyphs are identified by a numeric Character
    ID (CID) and not a glyph name. 
    """
    def __init__(self, name) -> None:
        """
        Initialised from one of the canned dictionaries in allowedEncodings

        Or rather, it will be shortly...
        """
        ...
    def getCharWidth(self, characterId): ...

class CIDFont(pdfmetrics.Font):
    """Represents a built-in multi-byte font"""
    faceName: Incomplete
    face: CIDTypeFace
    encodingName: Incomplete
    encoding: CIDEncoding
    fontName: Incomplete
    name: Incomplete
    isVertical: bool
    substitutionFonts: list[Incomplete]
    def __init__(self, face, encoding) -> None: ...
    def formatForPdf(self, text) -> str: ...
    def stringWidth(self, text, size, encoding=None) -> float: ...
    def addObjects(self, doc) -> None: ...

class UnicodeCIDFont(CIDFont):
    language: str
    name: Incomplete
    fontName: Incomplete
    vertical: bool
    isHalfWidth: bool
    unicodeWidths: Incomplete
    def __init__(self, face: str, isVertical: bool = False, isHalfWidth: bool = False) -> None: ...
    def formatForPdf(self, text) -> str: ...
    def stringWidth(self, text, size, encoding=None) -> float: ...

def precalculate(cmapdir) -> None: ...
def test() -> None: ...

"""
This provides a database of font metric information and
efines Font, Encoding and TypeFace classes aimed at end users.

There are counterparts to some of these in pdfbase/pdfdoc.py, but
the latter focus on constructing the right PDF objects.  These
classes are declarative and focus on letting the user construct
and query font objects.

The module maintains a registry of font objects at run time.

It is independent of the canvas or any particular context.  It keeps
a registry of Font, TypeFace and Encoding objects.  Ideally these
would be pre-loaded, but due to a nasty circularity problem we
trap attempts to access them and do it on first access.
"""

from _typeshed import Incomplete, StrOrBytesPath
from typing import Final, Literal

from reportlab.lib.rl_accel import unicode2T1 as unicode2T1
from reportlab.pdfbase.pdfdoc import PDFDictionary

__version__: Final[str]
standardFonts: Incomplete
standardEncodings: Incomplete

class FontError(Exception): ...
class FontNotFoundError(Exception): ...

def parseAFMFile(afmFileName: StrOrBytesPath) -> tuple[dict[Incomplete, Incomplete], list[Incomplete]]:
    """
    Quick and dirty - gives back a top-level dictionary
    with top-level items, and a 'widths' key containing
    a dictionary of glyph names and widths.  Just enough
    needed for embedding.  A better parser would accept
    options for what data you wwanted, and preserve the
    order.
    """
    ...

class TypeFace:
    name: Incomplete
    glyphNames: Incomplete
    glyphWidths: Incomplete
    ascent: int
    descent: int
    familyName: Incomplete
    bold: int
    italic: int
    requiredEncoding: str
    builtIn: int
    def __init__(self, name) -> None: ...
    def getFontFiles(self) -> list[Incomplete]: ...
    def findT1File(self, ext: str = ".pfb") -> str | None: ...

def bruteForceSearchForFile(fn, searchPath=None): ...
def bruteForceSearchForAFM(faceName) -> str | None: ...

class Encoding:
    """Object to help you create and refer to encodings."""
    name: Incomplete
    frozen: Literal[0, 1]
    baseEncodingName: Incomplete
    vector: tuple[Incomplete, ...]
    def __init__(self, name, base=None) -> None: ...
    def __getitem__(self, index):
        """Return glyph name for that code point, or None"""
        ...
    def __setitem__(self, index, value) -> None: ...
    def freeze(self) -> None: ...
    def isEqual(self, other) -> bool: ...
    def modifyRange(self, base, newNames) -> None: ...
    def getDifferences(self, otherEnc) -> list[Incomplete]: ...
    def makePDFObject(self) -> PDFDictionary | str: ...

standardT1SubstitutionFonts: Incomplete

class Font:
    """
    Represents a font (i.e combination of face and encoding).

    Defines suitable machinery for single byte fonts.  This is
    a concrete class which can handle the basic built-in fonts;
    not clear yet if embedded ones need a new font class or
    just a new typeface class (which would do the job through
    composition)
    """
    fontName: Incomplete
    encoding: Incomplete
    encName: Incomplete
    substitutionFonts: Incomplete
    shapable: bool
    def __init__(self, name, faceName, encName, substitutionFonts=None) -> None: ...
    def stringWidth(self, text: str | bytes, size: float, encoding: str = "utf8") -> float: ...
    widths: list[int]
    def addObjects(self, doc) -> None: ...

PFB_MARKER: Final[str]
PFB_ASCII: Final[str]
PFB_BINARY: Final[str]
PFB_EOF: Final[str]

class EmbeddedType1Face(TypeFace):
    """
    A Type 1 font other than one of the basic 14.

    Its glyph data will be embedded in the PDF file.
    """
    afmFileName: Incomplete
    pfbFileName: Incomplete
    requiredEncoding: Incomplete
    def __init__(self, afmFileName, pfbFileName) -> None: ...
    def getFontFiles(self) -> list[Incomplete]: ...
    def addObjects(self, doc): ...

def registerTypeFace(face) -> None: ...
def registerEncoding(enc) -> None: ...
def registerFontFamily(family, normal=None, bold=None, italic=None, boldItalic=None) -> None: ...
def registerFont(font) -> None: ...
def getTypeFace(faceName) -> TypeFace: ...
def getEncoding(encName) -> Encoding: ...
def findFontAndRegister(fontName: str) -> Font: ...
def getFont(fontName: str) -> Font: ...
def getAscentDescent(fontName: str, fontSize: float | None = None) -> tuple[float, float]: ...
def getAscent(fontName: str, fontSize: float | None = None) -> float: ...
def getDescent(fontName: str, fontSize: float | None = None) -> float: ...
def getRegisteredFontNames() -> list[Incomplete]: ...
def stringWidth(text: str | bytes, fontName: str, fontSize: float, encoding: str = "utf8") -> float: ...
def dumpFontData() -> None: ...
def test3widths(texts) -> None: ...
def testStringWidthAlgorithms() -> None: ...
def test() -> None: ...

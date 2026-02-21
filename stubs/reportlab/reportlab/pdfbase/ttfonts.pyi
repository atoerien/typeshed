"""
TrueType font support

This defines classes to represent TrueType fonts.  They know how to calculate
their own width and how to write themselves into PDF files.  They support
subsetting and embedding and can represent all 16-bit Unicode characters.

Note on dynamic fonts
---------------------

Usually a Font in ReportLab corresponds to a fixed set of PDF objects (Font,
FontDescriptor, Encoding).  But with dynamic font subsetting a single TTFont
will result in a number of Font/FontDescriptor/Encoding object sets, and the
contents of those will depend on the actual characters used for printing.

To support dynamic font subsetting a concept of "dynamic font" was introduced.
Dynamic Fonts have a _dynamicFont attribute set to 1.

Dynamic fonts have the following additional functions::

    def splitString(self, text, doc):
        '''Splits text into a number of chunks, each of which belongs to a
        single subset.  Returns a list of tuples (subset, string).  Use
        subset numbers with getSubsetInternalName.  Doc is used to identify
        a document so that different documents may have different dynamically
        constructed subsets.'''

    def getSubsetInternalName(self, subset, doc):
        '''Returns the name of a PDF Font object corresponding to a given
        subset of this dynamic font.  Use this function instead of
        PDFDocument.getInternalFontName.'''

You must never call PDFDocument.getInternalFontName for dynamic fonts.

If you have a traditional static font, mapping to PDF text output operators
is simple::

   '%s 14 Tf (%s) Tj' % (getInternalFontName(psfontname), text)

If you have a dynamic font, use this instead::

   for subset, chunk in font.splitString(text, doc):
       '%s 14 Tf (%s) Tj' % (font.getSubsetInternalName(subset, doc), chunk)

(Tf is a font setting operator and Tj is a text ouput operator.  You should
also escape invalid characters in Tj argument, see TextObject._formatText.
Oh, and that 14 up there is font size.)

Canvas and TextObject have special support for dynamic fonts.
"""

from _typeshed import Incomplete, ReadableBuffer, StrOrBytesPath
from collections.abc import Sequence
from typing import Final, Literal, NamedTuple
from typing_extensions import Self
from weakref import WeakKeyDictionary

from reportlab.pdfbase import pdfdoc, pdfmetrics

__version__: Final[str]

class TTFError(pdfdoc.PDFError):
    """TrueType font exception"""
    ...

def SUBSETN(n, table: ReadableBuffer | None = ...) -> bytes: ...
def makeToUnicodeCMap(fontname: str, subset) -> str:
    """
    Creates a ToUnicode CMap for a given subset.  See Adobe
    _PDF_Reference (ISBN 0-201-75839-3) for more information.
    """
    ...
def splice(stream, offset, value):
    """
    Splices the given value into stream at the given offset and
    returns the resulting stream (the original is unchanged)
    """
    ...

GF_ARG_1_AND_2_ARE_WORDS: Final = 1
GF_ARGS_ARE_XY_VALUES: Final = 2
GF_ROUND_XY_TO_GRID: Final = 4
GF_WE_HAVE_A_SCALE: Final = 8
GF_RESERVED: Final = 16
GF_MORE_COMPONENTS: Final = 32
GF_WE_HAVE_AN_X_AND_Y_SCALE: Final = 64
GF_WE_HAVE_A_TWO_BY_TWO: Final = 128
GF_WE_HAVE_INSTRUCTIONS: Final = 256
GF_USE_MY_METRICS: Final = 512
GF_OVERLAP_COMPOUND: Final = 1024
GF_SCALED_COMPONENT_OFFSET: Final = 2048
GF_UNSCALED_COMPONENT_OFFSET: Final = 4096

def TTFOpenFile(fn: StrOrBytesPath) -> tuple[StrOrBytesPath,]:
    """
    Opens a TTF file possibly after searching TTFSearchPath
    returns (filename,file)
    """
    ...

class TTFontParser:
    ttfVersions: tuple[int, ...]
    ttcVersions: tuple[int, ...]
    fileKind: str
    validate: bool | Literal[0, 1]
    subfontNameX: bytes
    def __init__(self, file, validate: bool | Literal[0, 1] = 0, subfontIndex: int = 0) -> None: ...
    ttcVersion: int
    numSubfonts: int
    subfontOffsets: list[int]
    def readTTCHeader(self) -> None: ...
    def getSubfont(self, subfontIndex: int) -> None: ...
    numTables: int
    searchRange: int
    entrySelector: int
    rangeShift: int
    table: dict[Incomplete, Incomplete]
    tables: list[Incomplete]
    def readTableDirectory(self) -> None: ...
    version: int
    def readHeader(self) -> bool: ...
    filename: Incomplete
    def readFile(self, f) -> None: ...
    def checksumTables(self) -> None: ...
    def checksumFile(self) -> None: ...
    def get_table_pos(self, tag) -> tuple[Incomplete, Incomplete]: ...
    def seek(self, pos: int) -> None: ...
    def skip(self, delta: int) -> None: ...
    def seek_table(self, tag, offset_in_table: int = 0) -> int: ...
    def read_tag(self) -> str: ...
    def get_chunk(self, pos: int, length: int) -> bytes: ...
    def read_uint8(self) -> int: ...
    def read_ushort(self) -> int: ...
    def read_ulong(self) -> int: ...
    def read_short(self) -> int: ...
    def get_ushort(self, pos: int) -> int: ...
    def get_ulong(self, pos: int) -> int: ...
    def get_table(self, tag): ...

class TTFontMaker:
    tables: dict[Incomplete, Incomplete]
    def __init__(self) -> None: ...
    def add(self, tag, data) -> None: ...
    def makeStream(self) -> bytes: ...

class CMapFmt2SubHeader(NamedTuple):
    firstCode: int
    entryCount: int
    idDelta: int
    idRangeOffset: int

class TTFNameBytes(bytes):
    """class used to return named strings"""
    ustr: Incomplete
    def __new__(cls, b, enc: str = "utf8") -> Self: ...

class TTFontFile(TTFontParser):
    def __init__(
        self, file, charInfo: bool | Literal[0, 1] = 1, validate: bool | Literal[0, 1] = 0, subfontIndex: int | str | bytes = 0
    ) -> None: ...
    name: Incomplete
    familyName: Incomplete
    styleName: Incomplete
    fullName: Incomplete
    uniqueFontID: Incomplete
    fontRevision: Incomplete
    unitsPerEm: Incomplete
    bbox: Incomplete
    ascent: Incomplete
    descent: Incomplete
    capHeight: Incomplete
    stemV: Incomplete
    italicAngle: Incomplete
    underlinePosition: Incomplete
    underlineThickness: Incomplete
    flags: Incomplete
    numGlyphs: Incomplete
    charToGlyph: Incomplete
    defaultWidth: Incomplete
    charWidths: Incomplete
    hmetrics: Incomplete
    glyphPos: Incomplete
    def extractInfo(self, charInfo: bool | Literal[0, 1] = 1) -> None: ...
    def makeSubset(self, subset: Sequence[Incomplete]) -> bytes: ...

FF_FIXED: Final = 1
FF_SERIF: Final = 2
FF_SYMBOLIC: Final = 4
FF_SCRIPT: Final = 8
FF_NONSYMBOLIC: Final = 32
FF_ITALIC: Final = 64
FF_ALLCAP: Final = 65536
FF_SMALLCAP: Final = 131072
FF_FORCEBOLD: Final = 262144

class TTFontFace(TTFontFile, pdfmetrics.TypeFace):
    def __init__(self, filename, validate: bool | Literal[0, 1] = 0, subfontIndex: int | str | bytes = 0) -> None: ...
    def getCharWidth(self, code): ...
    def addSubsetObjects(self, doc, fontname, subset): ...

class TTEncoding:
    """
    Encoding for TrueType fonts (always UTF-8).

    TTEncoding does not directly participate in PDF object creation, since
    we need a number of different 8-bit encodings for every generated font
    subset.  TTFont itself cares about that.
    """
    name: str
    def __init__(self) -> None: ...

class TTFont:
    """
    Represents a TrueType font.

    Its encoding is always UTF-8.

    Note: you cannot use the same TTFont object for different documents
    at the same time.

    Example of usage:

        font = ttfonts.TTFont('PostScriptFontName', '/path/to/font.ttf')
        pdfmetrics.registerFont(font)

        canvas.setFont('PostScriptFontName', size)
        canvas.drawString(x, y, "Some text encoded in UTF-8")
    """
    class State:
        namePrefix: str
        nextCode: int
        internalName: Incomplete
        frozen: bool | Literal[0, 1]
        subsets: Incomplete
        def __init__(self, asciiReadable: bool | Literal[0, 1] | None = None, ttf=None) -> None: ...

    fontName: str
    face: TTFontFace
    encoding: TTEncoding
    state: WeakKeyDictionary[Incomplete, State]
    def __init__(
        self,
        name: str,
        filename,
        validate: bool | Literal[0, 1] = 0,
        subfontIndex: int | str | bytes = 0,
        asciiReadable: bool | Literal[0, 1] | None = None,
        shapable: bool = True,
    ) -> None: ...
    def stringWidth(self, text, size, encoding: str = "utf8") -> float: ...
    def splitString(self, text, doc, encoding: str = "utf-8") -> list[tuple[int, bytes]]: ...
    def getSubsetInternalName(self, subset, doc) -> str: ...
    def addObjects(self, doc) -> None: ...
    @property
    def hbFace(self) -> Incomplete | None:
        """return uharbuzz.Face"""
        ...
    def hbFont(self, fontSize: float = 10):
        """return uharfbuzz Font"""
        ...
    @property
    def shapable(self) -> bool: ...
    @shapable.setter
    def shapable(self, v) -> None: ...
    def pdfScale(self, v): ...
    def unregister(self) -> None: ...

class ShapedFragWord(list[Incomplete]):
    """list class to distinguish frag words that have been shaped"""
    ...

class ShapeData(NamedTuple):
    cluster: int
    x_advance: float
    y_advance: float
    x_offset: float
    y_offset: float
    width: float

class ShapedStr(str):
    def __new__(cls, s, shapeData: ShapeData | None = None) -> Self: ...
    def __add__(self, other) -> ShapedStr: ...
    def __radd__(self, other) -> ShapedStr: ...

def shapeStr(s: str, fontName: str, fontSize: float, force: bool = False): ...
def freshTTFont(ttfn, ttfpath, **kwds) -> TTFont:
    """return a new instance corrsponding to a ttf path"""
    ...
def makeShapedFragWord(w, K: list[Incomplete] = [], V: list[Incomplete] = []) -> type[ShapedFragWord]: ...
def shapeFragWord(w, features=None, force: bool = False): ...

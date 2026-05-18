import re
from _io import BytesIO, StringIO
from _typeshed import Incomplete, ReadableBuffer, SupportsRead
from collections.abc import Callable, Iterable
from typing import Any, AnyStr, Generic, Literal, TypeAlias, TypeVar, overload
from typing_extensions import Self

from webencodings import Encoding

_UnicodeInputStream: TypeAlias = str | SupportsRead[str]
_BinaryInputStream: TypeAlias = bytes | SupportsRead[bytes]
_InputStream: TypeAlias = _UnicodeInputStream | _BinaryInputStream  # noqa: Y047  # used in other files
_SupportsReadT = TypeVar("_SupportsReadT", bound=SupportsRead[Any])
_SupportsReadBytesT = TypeVar("_SupportsReadBytesT", bound=SupportsRead[bytes])

spaceCharactersBytes: frozenset[bytes]
asciiLettersBytes: frozenset[bytes]
asciiUppercaseBytes: frozenset[bytes]
spacesAngleBrackets: frozenset[bytes]
invalid_unicode_no_surrogate: str
invalid_unicode_re: re.Pattern[str]
non_bmp_invalid_codepoints: set[int]
ascii_punctuation_re: re.Pattern[str]
charsUntilRegEx: dict[tuple[Iterable[str | bytes | bytearray], bool], re.Pattern[str]]

class BufferedStream(Generic[AnyStr]):
    """
    Buffering for streams that do not have buffering of their own

    The buffer is implemented as a list of chunks on the assumption that
    joining many strings will be slow since it is O(n**2)
    """
    stream: SupportsRead[AnyStr]
    buffer: list[AnyStr]
    position: list[int]
    def __init__(self, stream: SupportsRead[AnyStr]) -> None: ...
    def tell(self) -> int: ...
    def seek(self, pos: int) -> None: ...
    def read(self, bytes: int) -> AnyStr: ...

@overload
def HTMLInputStream(source: _UnicodeInputStream) -> HTMLUnicodeInputStream: ...
@overload
def HTMLInputStream(
    source: _BinaryInputStream,
    *,
    override_encoding: str | bytes | None = None,
    transport_encoding: str | bytes | None = None,
    same_origin_parent_encoding: str | bytes | None = None,
    likely_encoding: str | bytes | None = None,
    default_encoding: str = "windows-1252",
    useChardet: bool = True,
) -> HTMLBinaryInputStream: ...

class HTMLUnicodeInputStream:
    """
    Provides a unicode stream of characters to the HTMLTokenizer.

    This class takes care of character encoding and removing or replacing
    incorrect byte-sequences and also provides column and line tracking.
    """
    reportCharacterErrors: Callable[[str], None]
    newLines: list[int]
    charEncoding: tuple[Encoding, str]
    dataStream: Incomplete
    def __init__(self, source: _UnicodeInputStream) -> None:
        """
        Initialises the HTMLInputStream.

        HTMLInputStream(source, [encoding]) -> Normalized stream from source
        for use by html5lib.

        source can be either a file-object, local filename or a string.

        The optional encoding parameter must be a string that indicates
        the encoding.  If specified, that encoding will be used,
        regardless of any BOM or later declaration (such as in a meta
        element)
        """
        ...
    chunk: str
    chunkSize: int
    chunkOffset: int
    errors: list[str]
    prevNumLines: int
    prevNumCols: int
    def reset(self) -> None: ...

    @overload
    def openStream(self, source: _SupportsReadT) -> _SupportsReadT:
        """
        Produces a file object from source.

        source can be either a file object, local filename or a string.
        """
        ...
    @overload
    def openStream(self, source: str | None) -> StringIO: ...

    def position(self) -> tuple[int, int]: ...
    def char(self) -> str | None: ...
    def readChunk(self, chunkSize: int | None = None) -> bool: ...
    def characterErrorsUCS4(self, data: str) -> None: ...
    def characterErrorsUCS2(self, data: str) -> None: ...
    def charsUntil(self, characters: Iterable[str | bytes | bytearray], opposite: bool = False) -> str:
        """
        Returns a string of characters from the stream up to but not
        including any character in 'characters' or EOF. 'characters' must be
        a container that supports the 'in' method and iteration over its
        characters.
        """
        ...
    def unget(self, char: str | None) -> None: ...

class HTMLBinaryInputStream(HTMLUnicodeInputStream):
    """
    Provides a unicode stream of characters to the HTMLTokenizer.

    This class takes care of character encoding and removing or replacing
    incorrect byte-sequences and also provides column and line tracking.
    """
    rawStream: Incomplete
    numBytesMeta: int
    numBytesChardet: int
    override_encoding: Incomplete
    transport_encoding: Incomplete
    same_origin_parent_encoding: Incomplete
    likely_encoding: Incomplete
    default_encoding: str
    charEncoding: tuple[Encoding, str]
    def __init__(
        self,
        source: _BinaryInputStream,
        override_encoding: str | bytes | None = None,
        transport_encoding: str | bytes | None = None,
        same_origin_parent_encoding: str | bytes | None = None,
        likely_encoding: str | bytes | None = None,
        default_encoding: str = "windows-1252",
        useChardet: bool = True,
    ) -> None:
        """
        Initialises the HTMLInputStream.

        HTMLInputStream(source, [encoding]) -> Normalized stream from source
        for use by html5lib.

        source can be either a file-object, local filename or a string.

        The optional encoding parameter must be a string that indicates
        the encoding.  If specified, that encoding will be used,
        regardless of any BOM or later declaration (such as in a meta
        element)
        """
        ...
    dataStream: Incomplete
    def reset(self) -> None: ...

    @overload  # type: ignore[override]
    def openStream(self, source: _SupportsReadBytesT) -> _SupportsReadBytesT:
        """
        Produces a file object from source.

        source can be either a file object, local filename or a string.
        """
        ...
    @overload  # type: ignore[override]
    def openStream(self, source: ReadableBuffer) -> BytesIO: ...

    def determineEncoding(self, chardet: bool = True): ...
    def changeEncoding(self, newEncoding: str | bytes | None) -> None: ...
    def detectBOM(self) -> Encoding | None:
        """
        Attempts to detect at BOM at the start of the stream. If
        an encoding can be determined from the BOM return the name of the
        encoding otherwise return None
        """
        ...
    def detectEncodingMeta(self) -> Encoding | None:
        """
        Report the encoding declared by the meta element
        
        """
        ...

class EncodingBytes(bytes):
    """
    String-like object with an associated position and various extra methods
    If the position is ever greater than the string length then an exception is
    raised
    """
    def __new__(self, value: bytes) -> Self: ...
    def __init__(self, value: bytes) -> None: ...
    def __iter__(self) -> Self: ...  # type: ignore[override]
    def __next__(self) -> bytes: ...
    def next(self) -> bytes: ...
    def previous(self) -> bytes: ...
    def setPosition(self, position: int) -> None: ...
    def getPosition(self) -> int | None: ...

    @property
    def position(self) -> int | None: ...
    @position.setter
    def position(self, position: int) -> None: ...

    def getCurrentByte(self) -> bytes: ...
    @property
    def currentByte(self) -> bytes: ...
    def skip(self, chars: bytes | bytearray | Iterable[bytes] = ...) -> bytes | None:
        """Skip past a list of characters"""
        ...
    def skipUntil(self, chars: bytes | bytearray | Iterable[bytes]) -> bytes | None: ...
    def matchBytes(self, bytes: bytes | bytearray) -> bool:
        """
        Look for a sequence of bytes at the start of a string. If the bytes
        are found return True and advance the position to the byte after the
        match. Otherwise return False and leave the position alone
        """
        ...
    def jumpTo(self, bytes: bytes | bytearray) -> Literal[True]:
        """
        Look for the next sequence of bytes matching a given sequence. If
        a match is found advance the position to the last byte of the match
        """
        ...

class EncodingParser:
    """Mini parser for detecting character encoding from meta elements"""
    data: EncodingBytes
    encoding: Encoding | None
    def __init__(self, data: bytes) -> None:
        """string - the data to work on for encoding detection"""
        ...
    def getEncoding(self) -> Encoding | None: ...
    def handleComment(self) -> bool:
        """Skip over comments"""
        ...
    def handleMeta(self) -> bool: ...
    def handlePossibleStartTag(self) -> bool: ...
    def handlePossibleEndTag(self) -> bool: ...
    def handlePossibleTag(self, endTag: bool | None) -> bool: ...
    def handleOther(self) -> bool: ...
    def getAttribute(self) -> tuple[bytes, bytes] | None:
        """
        Return a name,value pair for the next attribute in the stream,
        if one is found, or None
        """
        ...

class ContentAttrParser:
    data: EncodingBytes
    def __init__(self, data: EncodingBytes) -> None: ...
    def parse(self) -> bytes | None: ...

def lookupEncoding(encoding: str | bytes | None) -> Encoding | None:
    """
    Return the python codec name corresponding to an encoding or None if the
    string doesn't correspond to a valid encoding.
    """
    ...

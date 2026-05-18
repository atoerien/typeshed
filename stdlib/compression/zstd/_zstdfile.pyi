from _typeshed import ReadableBuffer, StrOrBytesPath, SupportsWrite, WriteableBuffer
from collections.abc import Mapping
from compression._common import _streams
from compression.zstd import ZstdDict
from io import TextIOWrapper, _WrappedBuffer
from typing import Literal, Protocol, TypeAlias, overload, type_check_only

from _zstd import ZstdCompressor, _ZstdCompressorFlushBlock, _ZstdCompressorFlushFrame

__all__ = ("ZstdFile", "open")

_ReadBinaryMode: TypeAlias = Literal["r", "rb"]
_WriteBinaryMode: TypeAlias = Literal["w", "wb", "x", "xb", "a", "ab"]
_ReadTextMode: TypeAlias = Literal["rt"]
_WriteTextMode: TypeAlias = Literal["wt", "xt", "at"]

@type_check_only
class _FileBinaryRead(_streams._Reader, Protocol):
    def close(self) -> None: ...

@type_check_only
class _FileBinaryWrite(SupportsWrite[bytes], Protocol):
    def close(self) -> None: ...

class ZstdFile(_streams.BaseStream):
    """
    A file-like object providing transparent Zstandard (de)compression.

    A ZstdFile can act as a wrapper for an existing file object, or refer
    directly to a named file on disk.

    ZstdFile provides a *binary* file interface. Data is read and returned as
    bytes, and may only be written to objects that support the Buffer Protocol.
    """
    FLUSH_BLOCK = ZstdCompressor.FLUSH_BLOCK
    FLUSH_FRAME = ZstdCompressor.FLUSH_FRAME

    @overload
    def __init__(
        self,
        file: StrOrBytesPath | _FileBinaryRead,
        /,
        mode: _ReadBinaryMode = "r",
        *,
        level: None = None,
        options: Mapping[int, int] | None = None,
        zstd_dict: ZstdDict | tuple[ZstdDict, int] | None = None,
    ) -> None:
        """
        Open a Zstandard compressed file in binary mode.

        *file* can be either an file-like object, or a file name to open.

        *mode* can be 'r' for reading (default), 'w' for (over)writing, 'x' for
        creating exclusively, or 'a' for appending. These can equivalently be
        given as 'rb', 'wb', 'xb' and 'ab' respectively.

        *level* is an optional int specifying the compression level to use,
        or COMPRESSION_LEVEL_DEFAULT if not given.

        *options* is an optional dict for advanced compression parameters.
        See CompressionParameter and DecompressionParameter for the possible
        options.

        *zstd_dict* is an optional ZstdDict object, a pre-trained Zstandard
        dictionary. See train_dict() to train ZstdDict on sample data.
        """
        ...
    @overload
    def __init__(
        self,
        file: StrOrBytesPath | _FileBinaryWrite,
        /,
        mode: _WriteBinaryMode,
        *,
        level: int | None = None,
        options: Mapping[int, int] | None = None,
        zstd_dict: ZstdDict | tuple[ZstdDict, int] | None = None,
    ) -> None: ...

    def write(self, data: ReadableBuffer, /) -> int: ...
    def flush(self, mode: _ZstdCompressorFlushBlock | _ZstdCompressorFlushFrame = 1) -> bytes: ...  # type: ignore[override]
    def read(self, size: int | None = -1) -> bytes: ...
    def read1(self, size: int | None = -1) -> bytes: ...
    def readinto(self, b: WriteableBuffer) -> int: ...
    def readinto1(self, b: WriteableBuffer) -> int: ...
    def readline(self, size: int | None = -1) -> bytes: ...
    def seek(self, offset: int, whence: int = 0) -> int: ...
    def peek(self, size: int = -1) -> bytes: ...
    @property
    def name(self) -> str | bytes: ...
    @property
    def mode(self) -> Literal["rb", "wb"]: ...

@overload
def open(
    file: StrOrBytesPath | _FileBinaryRead,
    /,
    mode: _ReadBinaryMode = "rb",
    *,
    level: None = None,
    options: Mapping[int, int] | None = None,
    zstd_dict: ZstdDict | tuple[ZstdDict, int] | None = None,
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = None,
) -> ZstdFile:
    """
    Open a Zstandard compressed file in binary or text mode.

    file can be either a file name (given as a str, bytes, or PathLike object),
    in which case the named file is opened, or it can be an existing file object
    to read from or write to.

    The mode parameter can be 'r', 'rb' (default), 'w', 'wb', 'x', 'xb', 'a',
    'ab' for binary mode, or 'rt', 'wt', 'xt', 'at' for text mode.

    The level, options, and zstd_dict parameters specify the settings the same
    as ZstdFile.

    When using read mode (decompression), the options parameter is a dict
    representing advanced decompression options. The level parameter is not
    supported in this case. When using write mode (compression), only one of
    level, an int representing the compression level, or options, a dict
    representing advanced compression options, may be passed. In both modes,
    zstd_dict is a ZstdDict instance containing a trained Zstandard dictionary.

    For binary mode, this function is equivalent to the ZstdFile constructor:
    ZstdFile(filename, mode, ...). In this case, the encoding, errors and
    newline parameters must not be provided.

    For text mode, an ZstdFile object is created, and wrapped in an
    io.TextIOWrapper instance with the specified encoding, error handling
    behavior, and line ending(s).
    """
    ...
@overload
def open(
    file: StrOrBytesPath | _FileBinaryWrite,
    /,
    mode: _WriteBinaryMode,
    *,
    level: int | None = None,
    options: Mapping[int, int] | None = None,
    zstd_dict: ZstdDict | tuple[ZstdDict, int] | None = None,
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = None,
) -> ZstdFile:
    """
    Open a Zstandard compressed file in binary or text mode.

    file can be either a file name (given as a str, bytes, or PathLike object),
    in which case the named file is opened, or it can be an existing file object
    to read from or write to.

    The mode parameter can be 'r', 'rb' (default), 'w', 'wb', 'x', 'xb', 'a',
    'ab' for binary mode, or 'rt', 'wt', 'xt', 'at' for text mode.

    The level, options, and zstd_dict parameters specify the settings the same
    as ZstdFile.

    When using read mode (decompression), the options parameter is a dict
    representing advanced decompression options. The level parameter is not
    supported in this case. When using write mode (compression), only one of
    level, an int representing the compression level, or options, a dict
    representing advanced compression options, may be passed. In both modes,
    zstd_dict is a ZstdDict instance containing a trained Zstandard dictionary.

    For binary mode, this function is equivalent to the ZstdFile constructor:
    ZstdFile(filename, mode, ...). In this case, the encoding, errors and
    newline parameters must not be provided.

    For text mode, an ZstdFile object is created, and wrapped in an
    io.TextIOWrapper instance with the specified encoding, error handling
    behavior, and line ending(s).
    """
    ...
@overload
def open(
    file: StrOrBytesPath | _WrappedBuffer,
    /,
    mode: _ReadTextMode,
    *,
    level: None = None,
    options: Mapping[int, int] | None = None,
    zstd_dict: ZstdDict | tuple[ZstdDict, int] | None = None,
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = None,
) -> TextIOWrapper:
    """
    Open a Zstandard compressed file in binary or text mode.

    file can be either a file name (given as a str, bytes, or PathLike object),
    in which case the named file is opened, or it can be an existing file object
    to read from or write to.

    The mode parameter can be 'r', 'rb' (default), 'w', 'wb', 'x', 'xb', 'a',
    'ab' for binary mode, or 'rt', 'wt', 'xt', 'at' for text mode.

    The level, options, and zstd_dict parameters specify the settings the same
    as ZstdFile.

    When using read mode (decompression), the options parameter is a dict
    representing advanced decompression options. The level parameter is not
    supported in this case. When using write mode (compression), only one of
    level, an int representing the compression level, or options, a dict
    representing advanced compression options, may be passed. In both modes,
    zstd_dict is a ZstdDict instance containing a trained Zstandard dictionary.

    For binary mode, this function is equivalent to the ZstdFile constructor:
    ZstdFile(filename, mode, ...). In this case, the encoding, errors and
    newline parameters must not be provided.

    For text mode, an ZstdFile object is created, and wrapped in an
    io.TextIOWrapper instance with the specified encoding, error handling
    behavior, and line ending(s).
    """
    ...
@overload
def open(
    file: StrOrBytesPath | _WrappedBuffer,
    /,
    mode: _WriteTextMode,
    *,
    level: int | None = None,
    options: Mapping[int, int] | None = None,
    zstd_dict: ZstdDict | tuple[ZstdDict, int] | None = None,
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = None,
) -> TextIOWrapper:
    """
    Open a Zstandard compressed file in binary or text mode.

    file can be either a file name (given as a str, bytes, or PathLike object),
    in which case the named file is opened, or it can be an existing file object
    to read from or write to.

    The mode parameter can be 'r', 'rb' (default), 'w', 'wb', 'x', 'xb', 'a',
    'ab' for binary mode, or 'rt', 'wt', 'xt', 'at' for text mode.

    The level, options, and zstd_dict parameters specify the settings the same
    as ZstdFile.

    When using read mode (decompression), the options parameter is a dict
    representing advanced decompression options. The level parameter is not
    supported in this case. When using write mode (compression), only one of
    level, an int representing the compression level, or options, a dict
    representing advanced compression options, may be passed. In both modes,
    zstd_dict is a ZstdDict instance containing a trained Zstandard dictionary.

    For binary mode, this function is equivalent to the ZstdFile constructor:
    ZstdFile(filename, mode, ...). In this case, the encoding, errors and
    newline parameters must not be provided.

    For text mode, an ZstdFile object is created, and wrapped in an
    io.TextIOWrapper instance with the specified encoding, error handling
    behavior, and line ending(s).
    """
    ...

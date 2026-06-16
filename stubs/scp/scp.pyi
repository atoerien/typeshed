"""Utilities for sending files over ssh using the scp1 protocol."""

from collections.abc import Callable, Iterable
from pathlib import PurePath
from types import TracebackType
from typing import Final, Literal, Protocol, TypeAlias, type_check_only
from typing_extensions import Self

from paramiko.channel import Channel
from paramiko.transport import Transport

__version__: Final[str]

SCP_COMMAND: Final = b"scp"
PATH_TYPES: Final[tuple[type[str], type[bytes], type[PurePath]]]
bytes_sep: Final[bytes]

PathTypes: TypeAlias = str | bytes | PurePath

@type_check_only
class _PutFOReader(Protocol):
    def read(self, size: int, /) -> str | bytes | bytearray: ...
    def tell(self) -> int: ...
    def seek(self, offset: int, whence: Literal[0, 2], /) -> object: ...

def asbytes(s: PathTypes) -> bytes:
    """
    Turns unicode into bytes, if needed.

    Assumes UTF-8.
    """
    ...
def asunicode(s: bytes | str) -> str:
    """
    Turns bytes into unicode, if needed.

    Uses UTF-8.
    """
    ...
def asunicode_win(s: bytes | str) -> str:
    """
    Turns bytes into unicode, if needed.
    
    """
    ...

class SCPClient:
    """
    An scp1 implementation, compatible with openssh scp.
    Raises SCPException for all transport related errors. Local filesystem
    and OS errors pass through.

    Main public methods are .put and .get
    The get method is controlled by the remote scp instance, and behaves
    accordingly. This means that symlinks are resolved, and the transfer is
    halted after too many levels of symlinks are detected.
    The put method uses os.walk for recursion, and sends files accordingly.
    Since scp doesn't support symlinks, we send file symlinks as the file
    (matching scp behaviour), but we make no attempt at symlinked directories.
    """
    transport: Transport
    buff_size: int
    socket_timeout: float | None
    channel: Channel | None
    preserve_times: bool
    sanitize: Callable[[bytes], bytes]
    peername: tuple[str, int]
    scp_command: bytes
    def __init__(
        self,
        transport: Transport,
        buff_size: int = 16384,
        socket_timeout: float | None = 10.0,
        progress: Callable[[str | bytes, int, int], None] | None = None,
        progress4: Callable[[str | bytes, int, int, tuple[str, int]], None] | None = None,
        sanitize: Callable[[bytes], bytes] | Literal[False] = ...,
        limit_bw: int | None = None,
    ) -> None:
        """
        Create an scp1 client.

        @param transport: an existing paramiko L{Transport}
        @type transport: L{Transport}
        @param buff_size: size of the scp send buffer.
        @type buff_size: int
        @param socket_timeout: channel socket timeout in seconds
        @type socket_timeout: float
        @param progress: callback - called with (filename, size, sent) during
            transfers
        @param progress4: callback - called with (filename, size, sent, peername)
            during transfers. peername is a tuple contains (IP, PORT)
        @param sanitize: function - called with filename, should return
            safe or escaped string. Uses _sh_quote by default. Set to ``False``
            to disable.
        @type progress: function(string, int, int, tuple)
        @limit_bw: limits the bandwidth used on the connection in Kbps. Must be integer positive.
            the default value None does not limit the bandwidth.
        @type limit_bw: Optional[int]
        """
        ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None
    ) -> None: ...
    def put(
        self,
        files: PathTypes | Iterable[PathTypes],
        remote_path: PathTypes = b".",
        recursive: bool = False,
        preserve_times: bool = False,
    ) -> None:
        """
        Transfer files and directories to remote host.

        @param files: A single path, or a list of paths to be transferred.
            recursive must be True to transfer directories.
        @type files: string OR list of strings
        @param remote_path: path in which to receive the files on the remote
            host. defaults to '.'
        @type remote_path: str
        @param recursive: transfer files and directories recursively
        @type recursive: bool
        @param preserve_times: preserve mtime and atime of transferred files
            and directories.
        @type preserve_times: bool
        """
        ...
    def putfo(self, fl: _PutFOReader, remote_path: PathTypes, mode: str | bytes = "0644", size: int | None = None) -> None:
        """
        Transfer file-like object to remote host.

        @param fl: opened file or file-like object to copy
        @type fl: file-like object
        @param remote_path: full destination path
        @type remote_path: str
        @param mode: permissions (posix-style) for the uploaded file
        @type mode: str
        @param size: size of the file in bytes. If ``None``, the size will be
            computed using `seek()` and `tell()`.
        """
        ...
    def get(
        self,
        remote_path: PathTypes | Iterable[PathTypes],
        local_path: PathTypes = "",
        recursive: bool = False,
        preserve_times: bool = False,
    ) -> None:
        """
        Transfer files and directories from remote host to localhost.

        @param remote_path: path to retrieve from remote host. Note that
            wildcards will be escaped unless you changed the `sanitize`
            function.
        @type remote_path: str
        @param local_path: path in which to receive files locally
        @type local_path: str
        @param recursive: transfer files and directories recursively
        @type recursive: bool
        @param preserve_times: preserve mtime and atime of transferred files
            and directories.
        @type preserve_times: bool
        """
        ...
    def close(self) -> None:
        """close scp channel"""
        ...

class SCPException(Exception):
    """SCP exception class"""
    ...

def put(
    transport: Transport,
    files: PathTypes | Iterable[PathTypes],
    remote_path: PathTypes = b".",
    recursive: bool = False,
    preserve_times: bool = False,
) -> None:
    """
    Transfer files and directories to remote host.

    This is a convenience function that creates a SCPClient from the given
    transport and closes it at the end, useful for one-off transfers.

    @param files: A single path, or a list of paths to be transferred.
        recursive must be True to transfer directories.
    @type files: string OR list of strings
    @param remote_path: path in which to receive the files on the remote host.
        defaults to '.'
    @type remote_path: str
    @param recursive: transfer files and directories recursively
    @type recursive: bool
    @param preserve_times: preserve mtime and atime of transferred files and
        directories.
    @type preserve_times: bool
    """
    ...
def get(
    transport: Transport,
    remote_path: PathTypes | Iterable[PathTypes],
    local_path: PathTypes = "",
    recursive: bool = False,
    preserve_times: bool = False,
) -> None:
    """
    Transfer files and directories from remote host to localhost.

    This is a convenience function that creates a SCPClient from the given
    transport and closes it at the end, useful for one-off transfers.

    @param transport: an paramiko L{Transport}
    @type transport: L{Transport}
    @param remote_path: path to retrieve from remote host. Note that wildcards
        will be escaped unless you changed the `sanitize` function.
    @type remote_path: str
    @param local_path: path in which to receive files locally
    @type local_path: str
    @param recursive: transfer files and directories recursively
    @type recursive: bool
    @param preserve_times: preserve mtime and atime of transferred files
        and directories.
    @type preserve_times: bool
    """
    ...

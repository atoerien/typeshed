from _typeshed import StrOrBytesPath
from collections.abc import Callable, Iterator
from logging import Logger
from typing import IO, TypeAlias
from typing_extensions import Self

from paramiko.channel import Channel
from paramiko.sftp import BaseSFTP
from paramiko.sftp_attr import SFTPAttributes
from paramiko.sftp_file import SFTPFile
from paramiko.transport import Transport
from paramiko.util import ClosingContextManager

_Callback: TypeAlias = Callable[[int, int], object]

b_slash: bytes

class SFTPClient(BaseSFTP, ClosingContextManager):
    """
    SFTP client object.

    Used to open an SFTP session across an open SSH `.Transport` and perform
    remote file operations.

    Instances of this class may be used as context managers.
    """
    sock: Channel
    ultra_debug: bool
    request_number: int
    logger: Logger
    def __init__(self, sock: Channel) -> None:
        """
        Create an SFTP client from an existing `.Channel`.  The channel
        should already have requested the ``"sftp"`` subsystem.

        An alternate way to create an SFTP client context is by using
        `from_transport`.

        :param .Channel sock: an open `.Channel` using the ``"sftp"`` subsystem

        :raises:
            `.SSHException` -- if there's an exception while negotiating sftp
        """
        ...
    @classmethod
    def from_transport(cls, t: Transport, window_size: int | None = None, max_packet_size: int | None = None) -> Self | None:
        """
        Create an SFTP client channel from an open `.Transport`.

        Setting the window and packet sizes might affect the transfer speed.
        The default settings in the `.Transport` class are the same as in
        OpenSSH and should work adequately for both files transfers and
        interactive sessions.

        :param .Transport t: an open `.Transport` which is already
            authenticated
        :param int window_size:
            optional window size for the `.SFTPClient` session.
        :param int max_packet_size:
            optional max packet size for the `.SFTPClient` session..

        :return:
            a new `.SFTPClient` object, referring to an sftp session (channel)
            across the transport

        .. versionchanged:: 1.15
            Added the ``window_size`` and ``max_packet_size`` arguments.
        """
        ...
    def close(self) -> None:
        """
        Close the SFTP session and its underlying channel.

        .. versionadded:: 1.4
        """
        ...
    def get_channel(self) -> Channel | None:
        """
        Return the underlying `.Channel` object for this SFTP session.  This
        might be useful for doing things like setting a timeout on the channel.

        .. versionadded:: 1.7.1
        """
        ...
    def listdir(self, path: str = ".") -> list[str]:
        """
        Return a list containing the names of the entries in the given
        ``path``.

        The list is in arbitrary order.  It does not include the special
        entries ``'.'`` and ``'..'`` even if they are present in the folder.
        This method is meant to mirror ``os.listdir`` as closely as possible.
        For a list of full `.SFTPAttributes` objects, see `listdir_attr`.

        :param str path: path to list (defaults to ``'.'``)
        """
        ...
    def listdir_attr(self, path: str = ".") -> list[SFTPAttributes]:
        """
        Return a list containing `.SFTPAttributes` objects corresponding to
        files in the given ``path``.  The list is in arbitrary order.  It does
        not include the special entries ``'.'`` and ``'..'`` even if they are
        present in the folder.

        The returned `.SFTPAttributes` objects will each have an additional
        field: ``longname``, which may contain a formatted string of the file's
        attributes, in unix format.  The content of this string will probably
        depend on the SFTP server implementation.

        :param str path: path to list (defaults to ``'.'``)
        :return: list of `.SFTPAttributes` objects

        .. versionadded:: 1.2
        """
        ...
    def listdir_iter(self, path: bytes | str = ".", read_aheads: int = 50) -> Iterator[SFTPAttributes]:
        """
        Generator version of `.listdir_attr`.

        See the API docs for `.listdir_attr` for overall details.

        This function adds one more kwarg on top of `.listdir_attr`:
        ``read_aheads``, an integer controlling how many
        ``SSH_FXP_READDIR`` requests are made to the server. The default of 50
        should suffice for most file listings as each request/response cycle
        may contain multiple files (dependent on server implementation.)

        .. versionadded:: 1.15
        """
        ...
    def open(self, filename: bytes | str, mode: str = "r", bufsize: int = -1) -> SFTPFile:
        """
        Open a file on the remote server.  The arguments are the same as for
        Python's built-in `python:file` (aka `python:open`).  A file-like
        object is returned, which closely mimics the behavior of a normal
        Python file object, including the ability to be used as a context
        manager.

        The mode indicates how the file is to be opened: ``'r'`` for reading,
        ``'w'`` for writing (truncating an existing file), ``'a'`` for
        appending, ``'r+'`` for reading/writing, ``'w+'`` for reading/writing
        (truncating an existing file), ``'a+'`` for reading/appending.  The
        Python ``'b'`` flag is ignored, since SSH treats all files as binary.
        The ``'U'`` flag is supported in a compatible way.

        Since 1.5.2, an ``'x'`` flag indicates that the operation should only
        succeed if the file was created and did not previously exist.  This has
        no direct mapping to Python's file flags, but is commonly known as the
        ``O_EXCL`` flag in posix.

        The file will be buffered in standard Python style by default, but
        can be altered with the ``bufsize`` parameter.  ``<=0`` turns off
        buffering, ``1`` uses line buffering, and any number greater than 1
        (``>1``) uses that specific buffer size.

        :param str filename: name of the file to open
        :param str mode: mode (Python-style) to open in
        :param int bufsize: desired buffering (default: ``-1``)
        :return: an `.SFTPFile` object representing the open file

        :raises: ``IOError`` -- if the file could not be opened.
        """
        ...
    file = open
    def remove(self, path: bytes | str) -> None:
        """
        Remove the file at the given path.  This only works on files; for
        removing folders (directories), use `rmdir`.

        :param str path: path (absolute or relative) of the file to remove

        :raises: ``IOError`` -- if the path refers to a folder (directory)
        """
        ...
    unlink = remove
    def rename(self, oldpath: bytes | str, newpath: bytes | str) -> None: ...
    def posix_rename(self, oldpath: bytes | str, newpath: bytes | str) -> None: ...
    def mkdir(self, path: bytes | str, mode: int = 511) -> None: ...
    def rmdir(self, path: bytes | str) -> None: ...
    def stat(self, path: bytes | str) -> SFTPAttributes: ...
    def lstat(self, path: bytes | str) -> SFTPAttributes: ...
    def symlink(self, source: bytes | str, dest: bytes | str) -> None: ...
    def chmod(self, path: bytes | str, mode: int) -> None: ...
    def chown(self, path: bytes | str, uid: int, gid: int) -> None: ...
    def utime(self, path: bytes | str, times: tuple[float, float] | None) -> None: ...
    def truncate(self, path: bytes | str, size: int) -> None: ...
    def readlink(self, path: bytes | str) -> str | None: ...
    def normalize(self, path: bytes | str) -> str: ...
    def chdir(self, path: bytes | str | None = None) -> None: ...
    def getcwd(self) -> str | None: ...
    def putfo(
        self, fl: IO[bytes], remotepath: bytes | str, file_size: int = 0, callback: _Callback | None = None, confirm: bool = True
    ) -> SFTPAttributes:
        """
        Copy the contents of an open file object (``fl``) to the SFTP server as
        ``remotepath``. Any exception raised by operations will be passed
        through.

        The SFTP operations use pipelining for speed.

        :param fl: opened file or file-like object to copy
        :param str remotepath: the destination path on the SFTP server
        :param int file_size:
            optional size parameter passed to callback. If none is specified,
            size defaults to 0
        :param callable callback:
            optional callback function (form: ``func(int, int)``) that accepts
            the bytes transferred so far and the total bytes to be transferred
            (since 1.7.4)
        :param bool confirm:
            whether to do a stat() on the file afterwards to confirm the file
            size (since 1.7.7)

        :return:
            an `.SFTPAttributes` object containing attributes about the given
            file.

        .. versionadded:: 1.10
        """
        ...
    def put(
        self, localpath: StrOrBytesPath, remotepath: bytes | str, callback: _Callback | None = None, confirm: bool = True
    ) -> SFTPAttributes:
        """
        Copy a local file (``localpath``) to the SFTP server as ``remotepath``.
        Any exception raised by operations will be passed through.  This
        method is primarily provided as a convenience.

        The SFTP operations use pipelining for speed.

        :param str localpath: the local file to copy
        :param str remotepath: the destination path on the SFTP server. Note
            that the filename should be included. Only specifying a directory
            may result in an error.
        :param callable callback:
            optional callback function (form: ``func(int, int)``) that accepts
            the bytes transferred so far and the total bytes to be transferred
        :param bool confirm:
            whether to do a stat() on the file afterwards to confirm the file
            size

        :return: an `.SFTPAttributes` object containing attributes about the
            given file

        .. versionadded:: 1.4
        .. versionchanged:: 1.7.4
            ``callback`` and rich attribute return value added.
        .. versionchanged:: 1.7.7
            ``confirm`` param added.
        """
        ...
    def getfo(
        self,
        remotepath: bytes | str,
        fl: IO[bytes],
        callback: _Callback | None = None,
        prefetch: bool = True,
        max_concurrent_prefetch_requests: int | None = None,
    ) -> int:
        """
        Copy a remote file (``remotepath``) from the SFTP server and write to
        an open file or file-like object, ``fl``.  Any exception raised by
        operations will be passed through.  This method is primarily provided
        as a convenience.

        :param object remotepath: opened file or file-like object to copy to
        :param str fl:
            the destination path on the local host or open file object
        :param callable callback:
            optional callback function (form: ``func(int, int)``) that accepts
            the bytes transferred so far and the total bytes to be transferred
        :param bool prefetch:
            controls whether prefetching is performed (default: True)
        :param int max_concurrent_prefetch_requests:
            The maximum number of concurrent read requests to prefetch. See
            `.SFTPClient.get` (its ``max_concurrent_prefetch_requests`` param)
            for details.
        :return: the `number <int>` of bytes written to the opened file object

        .. versionadded:: 1.10
        .. versionchanged:: 2.8
            Added the ``prefetch`` keyword argument.
        .. versionchanged:: 3.3
            Added ``max_concurrent_prefetch_requests``.
        """
        ...
    def get(
        self,
        remotepath: bytes | str,
        localpath: StrOrBytesPath,
        callback: _Callback | None = None,
        prefetch: bool = True,
        max_concurrent_prefetch_requests: int | None = None,
    ) -> None:
        """
        Copy a remote file (``remotepath``) from the SFTP server to the local
        host as ``localpath``.  Any exception raised by operations will be
        passed through.  This method is primarily provided as a convenience.

        :param str remotepath: the remote file to copy
        :param str localpath: the destination path on the local host
        :param callable callback:
            optional callback function (form: ``func(int, int)``) that accepts
            the bytes transferred so far and the total bytes to be transferred
        :param bool prefetch:
            controls whether prefetching is performed (default: True)
        :param int max_concurrent_prefetch_requests:
            The maximum number of concurrent read requests to prefetch.
            When this is ``None`` (the default), do not limit the number of
            concurrent prefetch requests. Note: OpenSSH's sftp internally
            imposes a limit of 64 concurrent requests, while Paramiko imposes
            no limit by default; consider setting a limit if a file can be
            successfully received with sftp but hangs with Paramiko.

        .. versionadded:: 1.4
        .. versionchanged:: 1.7.4
            Added the ``callback`` param
        .. versionchanged:: 2.8
            Added the ``prefetch`` keyword argument.
        .. versionchanged:: 3.3
            Added ``max_concurrent_prefetch_requests``.
        """
        ...

class SFTP(SFTPClient):
    """An alias for `.SFTPClient` for backwards compatibility."""
    ...

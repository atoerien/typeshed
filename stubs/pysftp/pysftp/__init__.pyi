"""A friendly Python SFTP interface."""

from collections.abc import Callable, Sequence
from contextlib import AbstractContextManager
from stat import S_IMODE as S_IMODE
from types import TracebackType
from typing import IO, Literal
from typing_extensions import Self, TypeAlias

import paramiko
from paramiko import AuthenticationException as AuthenticationException
from pysftp.exceptions import (
    ConnectionException as ConnectionException,
    CredentialException as CredentialException,
    HostKeysException as HostKeysException,
)
from pysftp.helpers import (
    WTCallbacks as WTCallbacks,
    _PathCallback,
    cd as cd,
    known_hosts as known_hosts,
    path_advance as path_advance,
    path_retreat as path_retreat,
    reparent as reparent,
    st_mode_to_int as st_mode_to_int,
    walktree as walktree,
)

class CnOpts:
    """
    additional connection options beyond authentication

    :ivar bool|str log: initial value: False -
        log connection/handshake details? If set to True,
        pysftp creates a temporary file and logs to that.  If set to a valid
        path and filename, pysftp logs to that.  The name of the logfile can
        be found at  ``.logfile``
    :ivar bool compression: initial value: False - Enables compression on the
        transport, if set to True.
    :ivar list|None ciphers: initial value: None -
        List of ciphers to use in order.
    :ivar paramiko.hostkeys.HostKeys|None hostkeys: HostKeys object to use for
        host key checking.
    :param filepath|None knownhosts: initial value: None - file to load
        hostkeys. If not specified, uses ~/.ssh/known_hosts
    :returns: (obj) CnOpts - A connection options object, used for passing
        extended options to the Connection
    :raises HostKeysException:
    """
    log: bool | str
    compression: bool
    ciphers: Sequence[str] | None
    hostkeys: paramiko.HostKeys | None
    def __init__(self, knownhosts: str | None = None) -> None: ...
    def get_hostkey(self, host: str) -> paramiko.PKey:
        """
        return the matching hostkey to use for verification for the host
        indicated or raise an SSHException
        """
        ...

_Callback: TypeAlias = Callable[[int, int], object]
_Path: TypeAlias = str | bytes

class Connection:
    """
    Connects and logs into the specified hostname.
    Arguments that are not given are guessed from the environment.

    :param str host:
        The Hostname or IP of the remote machine.
    :param str|None username: *Default: None* -
        Your username at the remote machine.
    :param str|obj|None private_key: *Default: None* -
        path to private key file(str) or paramiko.AgentKey
    :param str|None password: *Default: None* -
        Your password at the remote machine.
    :param int port: *Default: 22* -
        The SSH port of the remote machine.
    :param str|None private_key_pass: *Default: None* -
        password to use, if private_key is encrypted.
    :param list|None ciphers: *Deprecated* -
        see ``pysftp.CnOpts`` and ``cnopts`` parameter
    :param bool|str log: *Deprecated* -
        see ``pysftp.CnOpts`` and ``cnopts`` parameter
    :param None|CnOpts cnopts: *Default: None* - extra connection options
        set in a CnOpts object.
    :param str|None default_path: *Default: None* -
        set a default path upon connection.
    :returns: (obj) connection to the requested host
    :raises ConnectionException:
    :raises CredentialException:
    :raises SSHException:
    :raises AuthenticationException:
    :raises PasswordRequiredException:
    :raises HostKeysException:
    """
    def __init__(
        self,
        host: str,
        username: str | None = None,
        private_key: str | paramiko.RSAKey | paramiko.AgentKey | None = None,
        password: str | None = None,
        port: int = 22,
        private_key_pass: str | None = None,
        ciphers: Sequence[str] | None = None,
        log: bool | str = False,
        cnopts: CnOpts | None = None,
        default_path: _Path | None = None,
    ) -> None: ...
    @property
    def pwd(self) -> str:
        """
        return the current working directory

        :returns: (str) current working directory
        """
        ...
    def get(
        self, remotepath: _Path, localpath: _Path | None = None, callback: _Callback | None = None, preserve_mtime: bool = False
    ) -> None:
        """
        Copies a file between the remote host and the local host.

        :param str remotepath: the remote path and filename, source
        :param str localpath:
            the local path and filename to copy, destination. If not specified,
            file is copied to local current working directory
        :param callable callback:
            optional callback function (form: ``func(int, int)``) that accepts
            the bytes transferred so far and the total bytes to be transferred.
        :param bool preserve_mtime:
            *Default: False* - make the modification time(st_mtime) on the
            local file match the time on the remote. (st_atime can differ
            because stat'ing the localfile can/does update it's st_atime)

        :returns: None

        :raises: IOError
        """
        ...
    def get_d(self, remotedir: _Path, localdir: _Path, preserve_mtime: bool = False) -> None:
        """
        get the contents of remotedir and write to locadir. (non-recursive)

        :param str remotedir: the remote directory to copy from (source)
        :param str localdir: the local directory to copy to (target)
        :param bool preserve_mtime: *Default: False* -
            preserve modification time on files

        :returns: None

        :raises:
        """
        ...
    def get_r(self, remotedir: _Path, localdir: _Path, preserve_mtime: bool = False) -> None:
        """
        recursively copy remotedir structure to localdir

        :param str remotedir: the remote directory to copy from
        :param str localdir: the local directory to copy to
        :param bool preserve_mtime: *Default: False* -
            preserve modification time on files

        :returns: None

        :raises:
        """
        ...
    def getfo(self, remotepath: _Path, flo: IO[bytes], callback: _Callback | None = None) -> int:
        """
        Copy a remote file (remotepath) to a file-like object, flo.

        :param str remotepath: the remote path and filename, source
        :param flo: open file like object to write, destination.
        :param callable callback:
            optional callback function (form: ``func(int, int``)) that accepts
            the bytes transferred so far and the total bytes to be transferred.

        :returns: (int) the number of bytes written to the opened file object

        :raises: Any exception raised by operations will be passed through.
        """
        ...
    def put(
        self,
        localpath: _Path,
        remotepath: _Path | None = None,
        callback: _Callback | None = None,
        confirm: bool = True,
        preserve_mtime: bool = False,
    ) -> paramiko.SFTPAttributes:
        """
        Copies a file between the local host and the remote host.

        :param str localpath: the local path and filename
        :param str remotepath:
            the remote path, else the remote :attr:`.pwd` and filename is used.
        :param callable callback:
            optional callback function (form: ``func(int, int``)) that accepts
            the bytes transferred so far and the total bytes to be transferred.
        :param bool confirm:
            whether to do a stat() on the file afterwards to confirm the file
            size
        :param bool preserve_mtime:
            *Default: False* - make the modification time(st_mtime) on the
            remote file match the time on the local. (st_atime can differ
            because stat'ing the localfile can/does update it's st_atime)

        :returns:
            (obj) SFTPAttributes containing attributes about the given file

        :raises IOError: if remotepath doesn't exist
        :raises OSError: if localpath doesn't exist
        """
        ...
    def put_d(self, localpath: _Path, remotepath: _Path, confirm: bool = True, preserve_mtime: bool = False) -> None:
        """
        Copies a local directory's contents to a remotepath

        :param str localpath: the local path to copy (source)
        :param str remotepath:
            the remote path to copy to (target)
        :param bool confirm:
            whether to do a stat() on the file afterwards to confirm the file
            size
        :param bool preserve_mtime:
            *Default: False* - make the modification time(st_mtime) on the
            remote file match the time on the local. (st_atime can differ
            because stat'ing the localfile can/does update it's st_atime)

        :returns: None

        :raises IOError: if remotepath doesn't exist
        :raises OSError: if localpath doesn't exist
        """
        ...
    def put_r(self, localpath: _Path, remotepath: _Path, confirm: bool = True, preserve_mtime: bool = False) -> None:
        """
        Recursively copies a local directory's contents to a remotepath

        :param str localpath: the local path to copy (source)
        :param str remotepath:
            the remote path to copy to (target)
        :param bool confirm:
            whether to do a stat() on the file afterwards to confirm the file
            size
        :param bool preserve_mtime:
            *Default: False* - make the modification time(st_mtime) on the
            remote file match the time on the local. (st_atime can differ
            because stat'ing the localfile can/does update it's st_atime)

        :returns: None

        :raises IOError: if remotepath doesn't exist
        :raises OSError: if localpath doesn't exist
        """
        ...
    def putfo(
        self,
        flo: IO[bytes],
        remotepath: _Path | None = None,
        file_size: int = 0,
        callback: _Callback | None = None,
        confirm: bool = True,
    ) -> paramiko.SFTPAttributes: ...
    def execute(self, command: str) -> list[str]: ...
    def cd(self, remotepath: _Path | None = None) -> AbstractContextManager[None]: ...
    def chdir(self, remotepath: _Path) -> None: ...
    def cwd(self, remotepath: _Path) -> None: ...
    def chmod(self, remotepath: _Path, mode: int = 777) -> None: ...
    def chown(self, remotepath: _Path, uid: int | None = None, gid: int | None = None) -> None: ...
    def getcwd(self) -> str: ...
    def listdir(self, remotepath: _Path = ".") -> list[str]: ...
    def listdir_attr(self, remotepath: _Path = ".") -> list[paramiko.SFTPAttributes]: ...
    def mkdir(self, remotepath: _Path, mode: int = 777) -> None: ...
    def normalize(self, remotepath: _Path) -> str: ...
    def isdir(self, remotepath: _Path) -> bool: ...
    def isfile(self, remotepath: _Path) -> bool: ...
    def makedirs(self, remotedir: _Path, mode: int = 777) -> None: ...
    def readlink(self, remotelink: _Path) -> str: ...
    def remove(self, remotefile: _Path) -> None: ...
    def unlink(self, remotefile: _Path) -> None: ...
    def rmdir(self, remotepath: _Path) -> None: ...
    def rename(self, remote_src: _Path, remote_dest: _Path) -> None: ...
    def stat(self, remotepath: _Path) -> paramiko.SFTPAttributes: ...
    def lstat(self, remotepath: _Path) -> paramiko.SFTPAttributes: ...
    def close(self) -> None: ...
    def open(self, remote_file: _Path, mode: str = "r", bufsize: int = -1) -> paramiko.SFTPFile: ...
    def exists(self, remotepath: _Path) -> bool: ...
    def lexists(self, remotepath: _Path) -> bool: ...
    def symlink(self, remote_src: _Path, remote_dest: _Path) -> None: ...
    def truncate(self, remotepath: _Path, size: int) -> int: ...
    def walktree(
        self,
        remotepath: _Path,
        fcallback: _PathCallback,
        dcallback: _PathCallback,
        ucallback: _PathCallback,
        recurse: bool = True,
    ) -> None:
        """
        recursively descend, depth first, the directory tree rooted at
        remotepath, calling discreet callback functions for each regular file,
        directory and unknown file type.

        :param str remotepath:
            root of remote directory to descend, use '.' to start at
            :attr:`.pwd`
        :param callable fcallback:
            callback function to invoke for a regular file.
            (form: ``func(str)``)
        :param callable dcallback:
            callback function to invoke for a directory. (form: ``func(str)``)
        :param callable ucallback:
            callback function to invoke for an unknown file type.
            (form: ``func(str)``)
        :param bool recurse: *Default: True* - should it recurse

        :returns: None

        :raises:
        """
        ...
    @property
    def sftp_client(self) -> paramiko.SFTPClient:
        """
        give access to the underlying, connected paramiko SFTPClient object

        see http://paramiko-docs.readthedocs.org/en/latest/api/sftp.html

        :params: None

        :returns: (obj) the active SFTPClient object
        """
        ...
    @property
    def active_ciphers(self) -> tuple[str, str]:
        """
        Get tuple of currently used local and remote ciphers.

        :returns:
            (tuple of  str) currently used ciphers (local_cipher,
            remote_cipher)
        """
        ...
    @property
    def active_compression(self) -> tuple[str, str]:
        """
        Get tuple of currently used local and remote compression.

        :returns:
            (tuple of  str) currently used compression (local_compression,
            remote_compression)
        """
        ...
    @property
    def security_options(self) -> paramiko.SecurityOptions:
        """
        return the available security options recognized by paramiko.

        :returns:
            (obj) security preferences of the ssh transport. These are tuples
            of acceptable `.ciphers`, `.digests`, `.key_types`, and key
            exchange algorithms `.kex`, listed in order of preference.
        """
        ...
    @property
    def logfile(self) -> str | Literal[False]:
        """
        return the name of the file used for logging or False it not logging

        :returns: (str)logfile or (bool) False
        """
        ...
    @property
    def timeout(self) -> float | None:
        """
        (float|None) *Default: None* -
            get or set the underlying socket timeout for pending read/write
            ops.

        :returns:
            (float|None) seconds to wait for a pending read/write operation
            before raising socket.timeout, or None for no timeout
        """
        ...
    @timeout.setter
    def timeout(self, val: float | None) -> None:
        """
        (float|None) *Default: None* -
            get or set the underlying socket timeout for pending read/write
            ops.

        :returns:
            (float|None) seconds to wait for a pending read/write operation
            before raising socket.timeout, or None for no timeout
        """
        ...
    @property
    def remote_server_key(self) -> paramiko.PKey:
        """return the remote server's key"""
        ...
    def __del__(self) -> None:
        """Attempt to clean up if not explicitly closed."""
        ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, etype: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None
    ) -> None: ...

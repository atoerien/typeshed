from _io import _BufferedReaderStream
from _typeshed import Incomplete
from socket import SocketIO
from typing import Literal, overload

from docker.transport.sshconn import SSHSocket
from docker.types.daemon import CancellableStream

class ExecApiMixin:
    def exec_create(
        self,
        container,
        cmd,
        stdout: bool = True,
        stderr: bool = True,
        stdin: bool = False,
        tty: bool = False,
        privileged: bool = False,
        user: str = "",
        environment: dict[str, str] | list[str] | None = None,
        workdir: str | None = None,
        detach_keys: str | None = None,
    ) -> dict[str, Incomplete]: ...
    def exec_inspect(self, exec_id: str) -> dict[str, Incomplete]: ...
    def exec_resize(self, exec_id: str, height: int | None = None, width: int | None = None) -> None: ...

    @overload
    def exec_start(
        self,
        exec_id: str,
        detach: Literal[True],
        tty: bool = False,
        stream: bool = False,
        socket: bool = False,
        demux: bool = False,
    ) -> bytes:
        """
        Start a previously set up exec instance.

        Args:
            exec_id (str): ID of the exec instance
            detach (bool): If true, detach from the exec command.
                Default: False
            tty (bool): Allocate a pseudo-TTY. Default: False
            stream (bool): Return response data progressively as an iterator
                of strings, rather than a single string.
            socket (bool): Return the connection socket to allow custom
                read/write operations. Must be closed by the caller when done.
            demux (bool): Return stdout and stderr separately

        Returns:

            (generator or str or tuple): If ``stream=True``, a generator
            yielding response chunks. If ``socket=True``, a socket object for
            the connection. A string containing response data otherwise. If
            ``demux=True``, a tuple with two elements of type byte: stdout and
            stderr.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    @overload
    def exec_start(
        self, exec_id: str, detach: Literal[False], tty: bool, stream: bool, socket: Literal[True], demux: bool = False
    ) -> SocketIO | _BufferedReaderStream | SSHSocket:
        """
        Start a previously set up exec instance.

        Args:
            exec_id (str): ID of the exec instance
            detach (bool): If true, detach from the exec command.
                Default: False
            tty (bool): Allocate a pseudo-TTY. Default: False
            stream (bool): Return response data progressively as an iterator
                of strings, rather than a single string.
            socket (bool): Return the connection socket to allow custom
                read/write operations. Must be closed by the caller when done.
            demux (bool): Return stdout and stderr separately

        Returns:

            (generator or str or tuple): If ``stream=True``, a generator
            yielding response chunks. If ``socket=True``, a socket object for
            the connection. A string containing response data otherwise. If
            ``demux=True``, a tuple with two elements of type byte: stdout and
            stderr.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    @overload
    def exec_start(
        self,
        exec_id: str,
        detach: Literal[False] = False,
        tty: bool = False,
        stream: bool = False,
        *,
        socket: Literal[True],
        demux: bool = False,
    ) -> SocketIO | _BufferedReaderStream | SSHSocket:
        """
        Start a previously set up exec instance.

        Args:
            exec_id (str): ID of the exec instance
            detach (bool): If true, detach from the exec command.
                Default: False
            tty (bool): Allocate a pseudo-TTY. Default: False
            stream (bool): Return response data progressively as an iterator
                of strings, rather than a single string.
            socket (bool): Return the connection socket to allow custom
                read/write operations. Must be closed by the caller when done.
            demux (bool): Return stdout and stderr separately

        Returns:

            (generator or str or tuple): If ``stream=True``, a generator
            yielding response chunks. If ``socket=True``, a socket object for
            the connection. A string containing response data otherwise. If
            ``demux=True``, a tuple with two elements of type byte: stdout and
            stderr.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    @overload
    def exec_start(
        self, exec_id: str, detach: Literal[False], tty: bool, stream: Literal[True], socket: Literal[False], demux: Literal[True]
    ) -> CancellableStream[tuple[bytes | None, bytes | None]]:
        """
        Start a previously set up exec instance.

        Args:
            exec_id (str): ID of the exec instance
            detach (bool): If true, detach from the exec command.
                Default: False
            tty (bool): Allocate a pseudo-TTY. Default: False
            stream (bool): Return response data progressively as an iterator
                of strings, rather than a single string.
            socket (bool): Return the connection socket to allow custom
                read/write operations. Must be closed by the caller when done.
            demux (bool): Return stdout and stderr separately

        Returns:

            (generator or str or tuple): If ``stream=True``, a generator
            yielding response chunks. If ``socket=True``, a socket object for
            the connection. A string containing response data otherwise. If
            ``demux=True``, a tuple with two elements of type byte: stdout and
            stderr.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    @overload
    def exec_start(
        self,
        exec_id: str,
        detach: Literal[False] = False,
        tty: bool = False,
        socket: Literal[False] = False,
        *,
        stream: Literal[True],
        demux: Literal[True],
    ) -> CancellableStream[tuple[bytes | None, bytes | None]]:
        """
        Start a previously set up exec instance.

        Args:
            exec_id (str): ID of the exec instance
            detach (bool): If true, detach from the exec command.
                Default: False
            tty (bool): Allocate a pseudo-TTY. Default: False
            stream (bool): Return response data progressively as an iterator
                of strings, rather than a single string.
            socket (bool): Return the connection socket to allow custom
                read/write operations. Must be closed by the caller when done.
            demux (bool): Return stdout and stderr separately

        Returns:

            (generator or str or tuple): If ``stream=True``, a generator
            yielding response chunks. If ``socket=True``, a socket object for
            the connection. A string containing response data otherwise. If
            ``demux=True``, a tuple with two elements of type byte: stdout and
            stderr.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    @overload
    def exec_start(
        self,
        exec_id: str,
        detach: Literal[False],
        tty: bool,
        stream: Literal[True],
        socket: Literal[False],
        demux: Literal[False],
    ) -> CancellableStream[bytes]:
        """
        Start a previously set up exec instance.

        Args:
            exec_id (str): ID of the exec instance
            detach (bool): If true, detach from the exec command.
                Default: False
            tty (bool): Allocate a pseudo-TTY. Default: False
            stream (bool): Return response data progressively as an iterator
                of strings, rather than a single string.
            socket (bool): Return the connection socket to allow custom
                read/write operations. Must be closed by the caller when done.
            demux (bool): Return stdout and stderr separately

        Returns:

            (generator or str or tuple): If ``stream=True``, a generator
            yielding response chunks. If ``socket=True``, a socket object for
            the connection. A string containing response data otherwise. If
            ``demux=True``, a tuple with two elements of type byte: stdout and
            stderr.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    @overload
    def exec_start(
        self,
        exec_id: str,
        detach: Literal[False] = False,
        tty: bool = False,
        *,
        stream: Literal[True],
        socket: Literal[False] = False,
        demux: Literal[False] = False,
    ) -> CancellableStream[bytes]:
        """
        Start a previously set up exec instance.

        Args:
            exec_id (str): ID of the exec instance
            detach (bool): If true, detach from the exec command.
                Default: False
            tty (bool): Allocate a pseudo-TTY. Default: False
            stream (bool): Return response data progressively as an iterator
                of strings, rather than a single string.
            socket (bool): Return the connection socket to allow custom
                read/write operations. Must be closed by the caller when done.
            demux (bool): Return stdout and stderr separately

        Returns:

            (generator or str or tuple): If ``stream=True``, a generator
            yielding response chunks. If ``socket=True``, a socket object for
            the connection. A string containing response data otherwise. If
            ``demux=True``, a tuple with two elements of type byte: stdout and
            stderr.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    @overload
    def exec_start(
        self,
        exec_id: str,
        detach: Literal[False],
        tty: bool,
        stream: Literal[False],
        socket: Literal[False],
        demux: Literal[True],
    ) -> tuple[bytes | None, bytes | None]:
        """
        Start a previously set up exec instance.

        Args:
            exec_id (str): ID of the exec instance
            detach (bool): If true, detach from the exec command.
                Default: False
            tty (bool): Allocate a pseudo-TTY. Default: False
            stream (bool): Return response data progressively as an iterator
                of strings, rather than a single string.
            socket (bool): Return the connection socket to allow custom
                read/write operations. Must be closed by the caller when done.
            demux (bool): Return stdout and stderr separately

        Returns:

            (generator or str or tuple): If ``stream=True``, a generator
            yielding response chunks. If ``socket=True``, a socket object for
            the connection. A string containing response data otherwise. If
            ``demux=True``, a tuple with two elements of type byte: stdout and
            stderr.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    @overload
    def exec_start(
        self,
        exec_id: str,
        detach: Literal[False] = False,
        tty: bool = False,
        stream: Literal[False] = False,
        socket: Literal[False] = False,
        *,
        demux: Literal[True],
    ) -> tuple[bytes | None, bytes | None]:
        """
        Start a previously set up exec instance.

        Args:
            exec_id (str): ID of the exec instance
            detach (bool): If true, detach from the exec command.
                Default: False
            tty (bool): Allocate a pseudo-TTY. Default: False
            stream (bool): Return response data progressively as an iterator
                of strings, rather than a single string.
            socket (bool): Return the connection socket to allow custom
                read/write operations. Must be closed by the caller when done.
            demux (bool): Return stdout and stderr separately

        Returns:

            (generator or str or tuple): If ``stream=True``, a generator
            yielding response chunks. If ``socket=True``, a socket object for
            the connection. A string containing response data otherwise. If
            ``demux=True``, a tuple with two elements of type byte: stdout and
            stderr.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    @overload
    def exec_start(
        self,
        exec_id: str,
        detach: Literal[False] = False,
        tty: bool = False,
        stream: Literal[False] = False,
        socket: Literal[False] = False,
        demux: Literal[False] = False,
    ) -> bytes:
        """
        Start a previously set up exec instance.

        Args:
            exec_id (str): ID of the exec instance
            detach (bool): If true, detach from the exec command.
                Default: False
            tty (bool): Allocate a pseudo-TTY. Default: False
            stream (bool): Return response data progressively as an iterator
                of strings, rather than a single string.
            socket (bool): Return the connection socket to allow custom
                read/write operations. Must be closed by the caller when done.
            demux (bool): Return stdout and stderr separately

        Returns:

            (generator or str or tuple): If ``stream=True``, a generator
            yielding response chunks. If ``socket=True``, a socket object for
            the connection. A string containing response data otherwise. If
            ``demux=True``, a tuple with two elements of type byte: stdout and
            stderr.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    @overload
    def exec_start(
        self,
        exec_id: str,
        detach: bool = False,
        tty: bool = False,
        stream: bool = False,
        socket: bool = False,
        demux: bool = False,
    ) -> (
        str
        | SocketIO
        | _BufferedReaderStream
        | SSHSocket
        | CancellableStream[bytes]
        | CancellableStream[tuple[bytes | None, bytes | None]]
        | tuple[bytes | None, bytes | None]
        | bytes
    ):
        """
        Start a previously set up exec instance.

        Args:
            exec_id (str): ID of the exec instance
            detach (bool): If true, detach from the exec command.
                Default: False
            tty (bool): Allocate a pseudo-TTY. Default: False
            stream (bool): Return response data progressively as an iterator
                of strings, rather than a single string.
            socket (bool): Return the connection socket to allow custom
                read/write operations. Must be closed by the caller when done.
            demux (bool): Return stdout and stderr separately

        Returns:

            (generator or str or tuple): If ``stream=True``, a generator
            yielding response chunks. If ``socket=True``, a socket object for
            the connection. A string containing response data otherwise. If
            ``demux=True``, a tuple with two elements of type byte: stdout and
            stderr.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...

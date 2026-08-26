import io
import socket
from _typeshed import ReadableBuffer
from collections.abc import Iterable, Iterator

class Unreader:
    buf: io.BytesIO

    def __init__(self) -> None: ...
    def chunk(self) -> bytes: ...
    def take_buffered(self) -> bytes:
        """
        Return read-ahead already held, without touching the source.

        read() blocks on the source when the buffer is empty, which is wrong
        for a caller that only wants the bytes it has: an Upgrade: h2c
        handshake needs whatever the client pipelined behind the request,
        and must not wait for more.
        """
        ...
    def read(self, size: int | None = None) -> bytes: ...
    def unread(self, data: ReadableBuffer) -> None: ...

class SocketUnreader(Unreader):
    sock: socket.socket
    mxchunk: int

    def __init__(self, sock: socket.socket, max_chunk: int = 8192) -> None: ...
    def chunk(self) -> bytes: ...

class IterUnreader(Unreader):
    iter: Iterator[bytes] | None

    def __init__(self, iterable: Iterable[bytes]) -> None: ...
    def chunk(self) -> bytes: ...

"""
Dirty Arbiters Protocol

Length-prefixed JSON message framing over Unix sockets.
Provides both async (primary) and sync (for HTTP workers) APIs.

Message Format:
+----------------+------------------+
| 4-byte length  | JSON payload     |
+----------------+------------------+

The length field is a 4-byte unsigned integer in network byte order (big-endian).
"""

import asyncio
import socket
from _typeshed import Incomplete
from typing import ClassVar

class DirtyProtocol:
    """Length-prefixed JSON messages over Unix sockets."""
    HEADER_FORMAT: ClassVar[str]
    HEADER_SIZE: ClassVar[int]
    MAX_MESSAGE_SIZE: ClassVar[int]
    MSG_TYPE_REQUEST: ClassVar[str]
    MSG_TYPE_RESPONSE: ClassVar[str]
    MSG_TYPE_ERROR: ClassVar[str]
    MSG_TYPE_CHUNK: ClassVar[str]
    MSG_TYPE_END: ClassVar[str]

    @staticmethod
    def encode(message: dict[Incomplete, Incomplete]) -> bytes:
        """
        Encode a message dict to length-prefixed bytes.

        Args:
            message: Dictionary to encode as JSON

        Returns:
            bytes: Length-prefixed encoded message

        Raises:
            DirtyProtocolError: If encoding fails
        """
        ...
    @staticmethod
    def decode(data: bytes) -> dict[Incomplete, Incomplete]:
        """
        Decode bytes (without length prefix) to message dict.

        Args:
            data: JSON bytes to decode

        Returns:
            dict: Decoded message

        Raises:
            DirtyProtocolError: If decoding fails
        """
        ...
    @staticmethod
    async def read_message_async(reader: asyncio.StreamReader) -> dict[Incomplete, Incomplete]:
        """
        Read a complete message from async stream.

        Args:
            reader: asyncio StreamReader

        Returns:
            dict: Decoded message

        Raises:
            DirtyProtocolError: If read fails or message is malformed
            asyncio.IncompleteReadError: If connection closed mid-read
        """
        ...
    @staticmethod
    async def write_message_async(writer: asyncio.StreamWriter, message: dict[Incomplete, Incomplete]) -> None:
        """
        Write a message to async stream.

        Args:
            writer: asyncio StreamWriter
            message: Dictionary to send

        Raises:
            DirtyProtocolError: If encoding fails
            ConnectionError: If write fails
        """
        ...
    @staticmethod
    def read_message(sock: socket.socket) -> dict[Incomplete, Incomplete]:
        """
        Read a complete message from socket (sync).

        Args:
            sock: Socket to read from

        Returns:
            dict: Decoded message

        Raises:
            DirtyProtocolError: If read fails or message is malformed
        """
        ...
    @staticmethod
    def write_message(sock: socket.socket, message: dict[Incomplete, Incomplete]) -> None:
        """
        Write a message to socket (sync).

        Args:
            sock: Socket to write to
            message: Dictionary to send

        Raises:
            DirtyProtocolError: If encoding fails
            OSError: If write fails
        """
        ...

# TODO: Use TypedDict for results
def make_request(
    request_id: str,
    app_path: str,
    action: str,
    args: tuple[Incomplete, ...] | None = None,
    kwargs: dict[str, Incomplete] | None = None,
) -> dict[str, Incomplete]:
    """
    Build a request message.

    Args:
        request_id: Unique request identifier
        app_path: Import path of the dirty app (e.g., 'myapp.ml:MLApp')
        action: Action to call on the app
        args: Positional arguments
        kwargs: Keyword arguments

    Returns:
        dict: Request message
    """
    ...
def make_response(request_id: str, result) -> dict[str, Incomplete]:
    """
    Build a success response message.

    Args:
        request_id: Request identifier this responds to
        result: Result value (must be JSON-serializable)

    Returns:
        dict: Response message
    """
    ...
def make_error_response(request_id: str, error) -> dict[str, Incomplete]:
    """
    Build an error response message.

    Args:
        request_id: Request identifier this responds to
        error: DirtyError instance or dict with error info

    Returns:
        dict: Error response message
    """
    ...
def make_chunk_message(request_id: str, data) -> dict[str, Incomplete]:
    """
    Build a chunk message for streaming responses.

    Args:
        request_id: Request identifier this chunk belongs to
        data: Chunk data (must be JSON-serializable)

    Returns:
        dict: Chunk message
    """
    ...
def make_end_message(request_id: str) -> dict[str, Incomplete]:
    """
    Build an end-of-stream message.

    Args:
        request_id: Request identifier this ends

    Returns:
        dict: End message
    """
    ...

"""
Control Socket Protocol

JSON-based protocol with length-prefixed framing for the control interface.

Message Format:
    +----------------+------------------+
    | Length (4B BE) |  JSON Payload    |
    +----------------+------------------+

Request Format:
    {"id": 1, "command": "show", "args": ["workers"]}

Response Format:
    {"id": 1, "status": "ok", "data": {...}}
    {"id": 1, "status": "error", "error": "message"}
"""

from _typeshed import Incomplete
from asyncio import StreamReader, StreamWriter
from socket import socket
from typing import ClassVar

class ProtocolError(Exception):
    """Protocol-level error."""
    ...

class ControlProtocol:
    """
    Protocol implementation for control socket communication.

    Uses 4-byte big-endian length prefix followed by JSON payload.
    """
    MAX_MESSAGE_SIZE: ClassVar[int]
    @staticmethod
    def encode_message(data: dict[Incomplete, Incomplete]) -> bytes:
        """
        Encode a message for transmission.

        Args:
            data: Dictionary to encode

        Returns:
            Length-prefixed JSON bytes
        """
        ...
    @staticmethod
    def decode_message(data: bytes) -> dict[Incomplete, Incomplete]:
        """
        Decode a message from bytes.

        Args:
            data: Raw bytes (length prefix + JSON payload)

        Returns:
            Decoded dictionary
        """
        ...
    @staticmethod
    def read_message(sock: socket) -> dict[Incomplete, Incomplete]:
        """
        Read one message from a socket.

        Args:
            sock: Socket to read from

        Returns:
            Decoded message dictionary

        Raises:
            ProtocolError: If message is malformed
            ConnectionError: If connection is closed
        """
        ...
    @staticmethod
    def write_message(sock: socket, data: dict[Incomplete, Incomplete]) -> None:
        """
        Write one message to a socket.

        Args:
            sock: Socket to write to
            data: Message dictionary to send
        """
        ...
    @staticmethod
    async def read_message_async(reader: StreamReader) -> dict[Incomplete, Incomplete]:
        """
        Read one message from an async reader.

        Args:
            reader: asyncio StreamReader

        Returns:
            Decoded message dictionary
        """
        ...
    @staticmethod
    async def write_message_async(writer: StreamWriter, data: dict[Incomplete, Incomplete]) -> None:
        """
        Write one message to an async writer.

        Args:
            writer: asyncio StreamWriter
            data: Message dictionary to send
        """
        ...

# TODO: Use TypedDict for next return types
def make_request(request_id: int, command: str, args: list[str] | None = None) -> dict[str, Incomplete]:
    """
    Create a request message.

    Args:
        request_id: Unique request identifier
        command: Command name (e.g., "show workers")
        args: Optional list of arguments

    Returns:
        Request dictionary
    """
    ...
def make_response(request_id: int, data: dict[Incomplete, Incomplete] | None = None) -> dict[str, Incomplete]:
    """
    Create a success response message.

    Args:
        request_id: Request identifier being responded to
        data: Response data

    Returns:
        Response dictionary
    """
    ...
def make_error_response(request_id: int, error: str) -> dict[str, Incomplete]:
    """
    Create an error response message.

    Args:
        request_id: Request identifier being responded to
        error: Error message

    Returns:
        Error response dictionary
    """
    ...

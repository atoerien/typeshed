"""
Dirty Worker Binary Protocol

Binary message framing over Unix sockets, inspired by OpenBSD msgctl/msgsnd.
Replaces JSON protocol for efficient binary data transfer.

Header Format (16 bytes):
+--------+--------+--------+--------+--------+--------+--------+--------+
|  Magic (2B)     | Ver(1) | MType  |        Payload Length (4B)        |
+--------+--------+--------+--------+--------+--------+--------+--------+
|                       Request ID (8 bytes)                            |
+--------+--------+--------+--------+--------+--------+--------+--------+

- Magic: 0x47 0x44 ("GD" for Gunicorn Dirty)
- Version: 0x01
- MType: Message type (REQUEST, RESPONSE, ERROR, CHUNK, END)
- Length: Payload size (big-endian uint32, max 64MB)
- Request ID: uint64 (replaces UUID string)

Payload is TLV-encoded (see tlv.py).
"""

import asyncio
import socket
from _typeshed import Incomplete
from typing import ClassVar, Final

MAGIC: Final = b"GD"
VERSION: Final = 0x01
MSG_TYPE_REQUEST: Final = 0x01
MSG_TYPE_RESPONSE: Final = 0x02
MSG_TYPE_ERROR: Final = 0x03
MSG_TYPE_CHUNK: Final = 0x04
MSG_TYPE_END: Final = 0x05
MSG_TYPE_STASH: Final = 0x10
MSG_TYPE_STATUS: Final = 0x11
MSG_TYPE_MANAGE: Final = 0x12
MSG_TYPE_REQUEST_STR: Final = "request"
MSG_TYPE_RESPONSE_STR: Final = "response"
MSG_TYPE_ERROR_STR: Final = "error"
MSG_TYPE_CHUNK_STR: Final = "chunk"
MSG_TYPE_END_STR: Final = "end"
MSG_TYPE_STASH_STR: Final = "stash"
MSG_TYPE_STATUS_STR: Final = "status"
MSG_TYPE_MANAGE_STR: Final = "manage"
MSG_TYPE_TO_STR: Final[dict[int, str]]
MSG_TYPE_FROM_STR: Final[dict[str, int]]
STASH_OP_PUT: Final = 1
STASH_OP_GET: Final = 2
STASH_OP_DELETE: Final = 3
STASH_OP_KEYS: Final = 4
STASH_OP_CLEAR: Final = 5
STASH_OP_INFO: Final = 6
STASH_OP_ENSURE: Final = 7
STASH_OP_DELETE_TABLE: Final = 8
STASH_OP_TABLES: Final = 9
STASH_OP_EXISTS: Final = 10
MANAGE_OP_ADD: Final = 1
MANAGE_OP_REMOVE: Final = 2
HEADER_FORMAT: Final = ">2sBBIQ"
HEADER_SIZE: Final[int]
MAX_MESSAGE_SIZE: Final = 67108864

class BinaryProtocol:
    """Binary message protocol for dirty worker IPC."""
    HEADER_SIZE: ClassVar[int]
    MAX_MESSAGE_SIZE: ClassVar[int]
    MSG_TYPE_REQUEST: ClassVar[str]
    MSG_TYPE_RESPONSE: ClassVar[str]
    MSG_TYPE_ERROR: ClassVar[str]
    MSG_TYPE_CHUNK: ClassVar[str]
    MSG_TYPE_END: ClassVar[str]
    MSG_TYPE_STASH: ClassVar[str]
    MSG_TYPE_STATUS: ClassVar[str]
    MSG_TYPE_MANAGE: ClassVar[str]

    @staticmethod
    def encode_header(msg_type: int, request_id: int, payload_length: int) -> bytes:
        """
        Encode the 16-byte message header.

        Args:
            msg_type: Message type (MSG_TYPE_REQUEST, etc.)
            request_id: Unique request identifier (uint64)
            payload_length: Length of the TLV-encoded payload

        Returns:
            bytes: 16-byte header
        """
        ...
    @staticmethod
    def decode_header(data: bytes) -> tuple[int, int, int]:
        """
        Decode the 16-byte message header.

        Args:
            data: 16 bytes of header data

        Returns:
            tuple: (msg_type, request_id, payload_length)

        Raises:
            DirtyProtocolError: If header is invalid
        """
        ...
    @staticmethod
    def encode_request(
        request_id: int,
        app_path: str,
        action: str,
        args: tuple[Incomplete, ...] | None = None,
        kwargs: dict[str, Incomplete] | None = None,
    ) -> bytes:
        """
        Encode a request message.

        Args:
            request_id: Unique request identifier (uint64)
            app_path: Import path of the dirty app
            action: Action to call on the app
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            bytes: Complete message (header + payload)
        """
        ...
    @staticmethod
    def encode_response(request_id: int, result) -> bytes:
        """
        Encode a success response message.

        Args:
            request_id: Request identifier this responds to
            result: Result value (must be TLV-serializable)

        Returns:
            bytes: Complete message (header + payload)
        """
        ...
    @staticmethod
    def encode_error(request_id: int, error: BaseException | dict[str, Incomplete]) -> bytes:
        """
        Encode an error response message.

        Args:
            request_id: Request identifier this responds to
            error: DirtyError instance, dict, or Exception

        Returns:
            bytes: Complete message (header + payload)
        """
        ...
    @staticmethod
    def encode_chunk(request_id: int, data) -> bytes:
        """
        Encode a chunk message for streaming responses.

        Args:
            request_id: Request identifier this chunk belongs to
            data: Chunk data (must be TLV-serializable)

        Returns:
            bytes: Complete message (header + payload)
        """
        ...
    @staticmethod
    def encode_end(request_id: int) -> bytes:
        """
        Encode an end-of-stream message.

        Args:
            request_id: Request identifier this ends

        Returns:
            bytes: Complete message (header + empty payload)
        """
        ...
    @staticmethod
    def encode_status(request_id: int) -> bytes:
        """
        Encode a status query message.

        Args:
            request_id: Request identifier

        Returns:
            bytes: Complete message (header + empty payload)
        """
        ...
    @staticmethod
    def encode_manage(request_id: int, op: int, count: int = 1) -> bytes:
        """
        Encode a worker management message.

        Args:
            request_id: Request identifier
            op: Management operation (MANAGE_OP_ADD or MANAGE_OP_REMOVE)
            count: Number of workers to add/remove

        Returns:
            bytes: Complete message (header + payload)
        """
        ...
    @staticmethod
    def encode_stash(request_id: int, op: int, table: str, key=None, value=None, pattern=None) -> bytes:
        """
        Encode a stash operation message.

        Args:
            request_id: Unique request identifier (uint64)
            op: Stash operation code (STASH_OP_*)
            table: Table name
            key: Optional key for put/get/delete operations
            value: Optional value for put operation
            pattern: Optional pattern for keys operation

        Returns:
            bytes: Complete message (header + payload)
        """
        ...
    @staticmethod
    def decode_message(data: bytes) -> tuple[str, int, Incomplete]:
        """
        Decode a complete message (header + payload).

        Args:
            data: Complete message bytes

        Returns:
            tuple: (msg_type_str, request_id, payload_dict)
                   msg_type_str is the string name (e.g., "request")
                   payload_dict is the decoded TLV payload as a dict

        Raises:
            DirtyProtocolError: If message is malformed
        """
        ...
    @staticmethod
    async def read_message_async(reader: asyncio.StreamReader) -> dict[str, Incomplete]:
        """
        Read a complete binary message from async stream.

        Args:
            reader: asyncio StreamReader

        Returns:
            dict: Message dict with 'type', 'id', and payload fields

        Raises:
            DirtyProtocolError: If read fails or message is malformed
            asyncio.IncompleteReadError: If connection closed mid-read
        """
        ...
    @staticmethod
    async def write_message_async(writer: asyncio.StreamWriter, message: dict[str, Incomplete]) -> None:
        """
        Write a message to async stream.

        Accepts dict format for backwards compatibility.

        Args:
            writer: asyncio StreamWriter
            message: Message dict with 'type', 'id', and payload fields

        Raises:
            DirtyProtocolError: If encoding fails
            ConnectionError: If write fails
        """
        ...
    @staticmethod
    def _recv_exactly(sock: socket.socket, n: int) -> bytes:
        """
        Receive exactly n bytes from a socket.

        Args:
            sock: Socket to read from
            n: Number of bytes to read

        Returns:
            bytes: Received data

        Raises:
            DirtyProtocolError: If read fails or connection closed
        """
        ...
    @staticmethod
    def read_message(sock: socket.socket) -> dict[str, Incomplete]:
        """
        Read a complete message from socket (sync).

        Args:
            sock: Socket to read from

        Returns:
            dict: Message dict with 'type', 'id', and payload fields

        Raises:
            DirtyProtocolError: If read fails or message is malformed
        """
        ...
    @staticmethod
    def write_message(sock: socket.socket, message: dict[str, Incomplete]) -> None:
        """
        Write a message to socket (sync).

        Args:
            sock: Socket to write to
            message: Message dict with 'type', 'id', and payload fields

        Raises:
            DirtyProtocolError: If encoding fails
            OSError: If write fails
        """
        ...
    @staticmethod
    def _encode_from_dict(message: dict[str, Incomplete]) -> bytes:
        """
        Encode a message dict to binary format.

        Supports the old dict-based API for backwards compatibility.

        Args:
            message: Message dict with 'type', 'id', and payload fields

        Returns:
            bytes: Complete encoded message
        """
        ...

DirtyProtocol = BinaryProtocol

# TODO: Use TypedDict for results
def make_request(
    request_id: int | str,
    app_path: str,
    action: str,
    args: tuple[Incomplete, ...] | None = None,
    kwargs: dict[str, Incomplete] | None = None,
) -> dict[str, Incomplete]:
    """
    Build a request message dict.

    Args:
        request_id: Unique request identifier (int or str)
        app_path: Import path of the dirty app (e.g., 'myapp.ml:MLApp')
        action: Action to call on the app
        args: Positional arguments
        kwargs: Keyword arguments

    Returns:
        dict: Request message dict
    """
    ...
def make_response(request_id: int | str, result) -> dict[str, Incomplete]:
    """
    Build a success response message dict.

    Args:
        request_id: Request identifier this responds to
        result: Result value

    Returns:
        dict: Response message dict
    """
    ...
def make_error_response(request_id: int | str, error) -> dict[str, Incomplete]:
    """
    Build an error response message dict.

    Args:
        request_id: Request identifier this responds to
        error: DirtyError instance or dict with error info

    Returns:
        dict: Error response message dict
    """
    ...
def make_chunk_message(request_id: int | str, data) -> dict[str, Incomplete]:
    """
    Build a chunk message dict for streaming responses.

    Args:
        request_id: Request identifier this chunk belongs to
        data: Chunk data

    Returns:
        dict: Chunk message dict
    """
    ...
def make_end_message(request_id: int | str) -> dict[str, Incomplete]:
    """
    Build an end-of-stream message dict.

    Args:
        request_id: Request identifier this ends

    Returns:
        dict: End message dict
    """
    ...
def make_stash_message(
    request_id: int | str, op: int, table: str, key=None, value=None, pattern=None
) -> dict[str, Incomplete]:
    """
    Build a stash operation message dict.

    Args:
        request_id: Unique request identifier (int or str)
        op: Stash operation code (STASH_OP_*)
        table: Table name
        key: Optional key for put/get/delete operations
        value: Optional value for put operation
        pattern: Optional pattern for keys operation

    Returns:
        dict: Stash message dict
    """
    ...
def make_manage_message(request_id: int | str, op: int, count: int = 1) -> dict[str, Incomplete]:
    """
    Build a worker management message dict.

    Args:
        request_id: Unique request identifier (int or str)
        op: Management operation (MANAGE_OP_ADD or MANAGE_OP_REMOVE)
        count: Number of workers to add/remove

    Returns:
        dict: Manage message dict
    """
    ...

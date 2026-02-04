"""
HTTP/2 stream state management.

Each HTTP/2 stream represents a single request/response exchange.
"""

from _typeshed import Incomplete, ReadableBuffer
from collections.abc import Iterable
from enum import Enum
from io import BytesIO

from gunicorn.http2.connection import HTTP2ServerConnection

class StreamState(Enum):
    """HTTP/2 stream states as defined in RFC 7540 Section 5.1."""
    IDLE = 1
    RESERVED_LOCAL = 2
    RESERVED_REMOTE = 3
    OPEN = 4
    HALF_CLOSED_LOCAL = 5
    HALF_CLOSED_REMOTE = 6
    CLOSED = 7

class HTTP2Stream:
    """
    Represents a single HTTP/2 stream.

    Manages stream state, headers, and body data for a single
    request/response exchange within an HTTP/2 connection.
    """
    stream_id: int
    connection: HTTP2ServerConnection
    state: StreamState
    request_headers: list[tuple[str, Incomplete]]
    request_body: BytesIO
    request_complete: bool
    response_started: bool
    response_headers_sent: bool
    response_complete: bool
    window_size: int
    trailers: list[tuple[str, Incomplete]] | None
    response_trailers: list[tuple[str, Incomplete]] | None
    priority_weight: int
    priority_depends_on: int
    priority_exclusive: bool

    def __init__(self, stream_id: int, connection: HTTP2ServerConnection) -> None:
        """
        Initialize an HTTP/2 stream.

        Args:
            stream_id: The unique stream identifier (odd for client-initiated)
            connection: The parent HTTP2ServerConnection
        """
        ...
    @property
    def is_client_stream(self) -> bool:
        """Check if this is a client-initiated stream (odd stream ID)."""
        ...
    @property
    def is_server_stream(self) -> bool:
        """Check if this is a server-initiated stream (even stream ID)."""
        ...
    @property
    def can_receive(self) -> bool:
        """Check if this stream can receive data."""
        ...
    @property
    def can_send(self) -> bool:
        """Check if this stream can send data."""
        ...
    def receive_headers(self, headers: Iterable[tuple[str, Incomplete]], end_stream: bool | None = False) -> None:
        """
        Process received HEADERS frame.

        Args:
            headers: List of (name, value) tuples
            end_stream: True if END_STREAM flag is set

        Raises:
            HTTP2StreamError: If headers received in invalid state
        """
        ...
    def receive_data(self, data: ReadableBuffer, end_stream: bool | None = False) -> None:
        """
        Process received DATA frame.

        Args:
            data: Bytes received
            end_stream: True if END_STREAM flag is set

        Raises:
            HTTP2StreamError: If data received in invalid state
        """
        ...
    def receive_trailers(self, trailers: list[tuple[str, Incomplete]]) -> None:
        """
        Process received trailing headers.

        Args:
            trailers: List of (name, value) tuples
        """
        ...
    def send_headers(self, headers: Iterable[tuple[str, Incomplete]], end_stream: bool | None = False) -> None:
        """
        Mark headers as sent.

        Args:
            headers: List of (name, value) tuples to send
            end_stream: True if this completes the response

        Raises:
            HTTP2StreamError: If headers cannot be sent in current state
        """
        ...
    def send_data(self, data: ReadableBuffer, end_stream: bool | None = False) -> None:
        """
        Mark data as sent.

        Args:
            data: Bytes to send
            end_stream: True if this completes the response

        Raises:
            HTTP2StreamError: If data cannot be sent in current state
        """
        ...
    def send_trailers(self, trailers: list[tuple[str, Incomplete]]) -> None:
        """
        Mark trailers as sent and close the stream.

        Args:
            trailers: List of (name, value) trailer tuples

        Raises:
            HTTP2StreamError: If trailers cannot be sent in current state
        """
        ...
    def reset(self, error_code: int = 0x8) -> None:
        """
        Reset this stream with RST_STREAM.

        Args:
            error_code: HTTP/2 error code (default: CANCEL)
        """
        ...
    def close(self) -> None:
        """Close this stream normally."""
        ...
    def update_priority(
        self, weight: int | None = None, depends_on: int | None = None, exclusive: bool | None = None
    ) -> None:
        """
        Update stream priority from PRIORITY frame.

        Args:
            weight: Priority weight (1-256), higher = more resources
            depends_on: Stream ID this stream depends on
            exclusive: Whether this is an exclusive dependency
        """
        ...
    def get_request_body(self) -> bytes:
        """
        Get the complete request body.

        Returns:
            bytes: The request body data
        """
        ...
    def get_pseudo_headers(self) -> dict[str, Incomplete]:
        """
        Extract HTTP/2 pseudo-headers from request headers.

        Returns:
            dict: Mapping of pseudo-header names to values
                  (e.g., {':method': 'GET', ':path': '/'})
        """
        ...
    def get_regular_headers(self) -> list[tuple[str, Incomplete]]:
        """
        Get regular (non-pseudo) headers from request.

        Returns:
            list: List of (name, value) tuples for regular headers
        """
        ...

__all__ = ["HTTP2Stream", "StreamState"]

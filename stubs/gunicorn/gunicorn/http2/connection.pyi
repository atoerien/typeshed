"""
HTTP/2 server connection implementation.

Uses the hyper-h2 library for HTTP/2 protocol handling.
"""

from _typeshed import Incomplete
from collections.abc import Iterable
from ssl import SSLSocket
from typing import Any, ClassVar
from typing_extensions import TypeAlias

from gunicorn.config import Config
from gunicorn.http2.request import HTTP2Request
from gunicorn.http2.stream import HTTP2Stream

from .._types import _AddressType

_H2Connection: TypeAlias = Any  # h2.connection.H2Connection class

class HTTP2ServerConnection:
    """
    HTTP/2 server-side connection handler.

    Manages the HTTP/2 connection state and multiplexed streams.
    This class wraps the h2 library and provides a higher-level
    interface for gunicorn workers.
    """
    READ_BUFFER_SIZE: ClassVar[int]
    cfg: Config
    sock: SSLSocket
    client_addr: _AddressType
    streams: dict[int, HTTP2Stream]
    initial_window_size: int
    max_concurrent_streams: int
    max_frame_size: int
    max_header_list_size: int
    h2_conn: _H2Connection

    def __init__(self, cfg: Config, sock: SSLSocket, client_addr: _AddressType) -> None:
        """
        Initialize an HTTP/2 server connection.

        Args:
            cfg: Gunicorn configuration object
            sock: SSL socket with completed handshake
            client_addr: Client address tuple (host, port)

        Raises:
            HTTP2NotAvailable: If h2 library is not installed
        """
        ...
    def initiate_connection(self) -> None:
        """
        Send initial HTTP/2 settings to client.

        Should be called after the SSL handshake completes and
        before processing any data.
        """
        ...
    def receive_data(self, data: bytes | None = None) -> list[HTTP2Request]:
        """
        Process received data and return completed requests.

        Args:
            data: Optional bytes to process. If None, reads from socket.

        Returns:
            list: List of HTTP2Request objects for completed requests

        Raises:
            HTTP2ConnectionError: On protocol or connection errors
        """
        ...
    def send_informational(self, stream_id: int, status: int, headers: Iterable[tuple[str, Incomplete]]) -> None:
        """
        Send an informational response (1xx) on a stream.

        This is used for 103 Early Hints and other 1xx responses.
        Informational responses are sent before the final response
        and do not end the stream.

        Args:
            stream_id: The stream ID
            status: HTTP status code (100-199)
            headers: List of (name, value) header tuples

        Raises:
            HTTP2Error: If status is not in 1xx range
        """
        ...
    def send_response(
        self, stream_id: int, status: int, headers: Iterable[tuple[str, Incomplete]], body: bytes | None = None
    ) -> bool:
        """
        Send a response on a stream.

        Args:
            stream_id: The stream ID to respond on
            status: HTTP status code (int)
            headers: List of (name, value) header tuples
            body: Optional response body bytes

        Raises:
            HTTP2Error: If stream not found or in invalid state

        Returns:
            bool: True if response sent, False if stream was already closed
        """
        ...
    def send_data(self, stream_id: int, data: bytes, end_stream: bool = False) -> bool:
        """
        Send data on a stream.

        Args:
            stream_id: The stream ID
            data: Body data bytes
            end_stream: Whether this ends the stream

        Returns:
            bool: True if data sent, False if stream was already closed
        """
        ...
    def send_trailers(self, stream_id: int, trailers: Iterable[tuple[str, Incomplete]]) -> bool:
        """
        Send trailing headers on a stream.

        Trailers are headers sent after the response body, commonly used
        for gRPC status codes, checksums, and timing information.

        Args:
            stream_id: The stream ID
            trailers: List of (name, value) trailer tuples

        Raises:
            HTTP2Error: If stream not found, headers not sent, or pseudo-headers used

        Returns:
            bool: True if trailers sent, False if stream was already closed
        """
        ...
    def send_error(self, stream_id: int, status_code: int, message: str | None = None) -> None:
        """
        Send an error response on a stream.

        Args:
            stream_id: The stream ID
            status_code: HTTP status code
            message: Optional error message body
        """
        ...
    def reset_stream(self, stream_id: int, error_code: int = 0x8) -> None:
        """
        Reset a stream with RST_STREAM.

        Args:
            stream_id: The stream ID to reset
            error_code: HTTP/2 error code (default: CANCEL)
        """
        ...
    def close(self, error_code: int = 0x0, last_stream_id: int | None = None) -> None:
        """
        Close the connection gracefully with GOAWAY.

        Args:
            error_code: HTTP/2 error code (default: NO_ERROR)
            last_stream_id: Last processed stream ID (default: highest)
        """
        ...
    @property
    def is_closed(self) -> bool:
        """Check if connection is closed."""
        ...
    def cleanup_stream(self, stream_id: int) -> None:
        """
        Remove a stream after processing is complete.

        Args:
            stream_id: The stream ID to clean up
        """
        ...

__all__ = ["HTTP2ServerConnection"]

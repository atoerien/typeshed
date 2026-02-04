"""
HTTP/2 request wrapper.

Provides a Request-compatible interface for HTTP/2 streams.
"""

from _typeshed import Incomplete, ReadableBuffer
from collections.abc import Iterator
from typing import Literal

from gunicorn.config import Config
from gunicorn.http2.stream import HTTP2Stream

from .._types import _AddressType

class HTTP2Body:
    """
    Body wrapper for HTTP/2 request data.

    Provides a file-like interface to the request body,
    compatible with gunicorn's Body class expectations.
    """
    def __init__(self, data: ReadableBuffer) -> None:
        """
        Initialize with body data.

        Args:
            data: bytes containing the request body
        """
        ...
    def read(self, size: int | None = None) -> bytes:
        """
        Read data from the body.

        Args:
            size: Number of bytes to read, or None for all remaining

        Returns:
            bytes: The requested data
        """
        ...
    def readline(self, size: int | None = None) -> bytes:
        """
        Read a line from the body.

        Args:
            size: Maximum bytes to read

        Returns:
            bytes: A line of data
        """
        ...
    def readlines(self, hint: int | None = None) -> list[bytes]:
        """
        Read all lines from the body.

        Args:
            hint: Approximate byte count hint

        Returns:
            list: List of lines
        """
        ...
    def __iter__(self) -> Iterator[bytes]:
        """Iterate over lines in the body."""
        ...
    def __len__(self) -> int:
        """Return the content length."""
        ...
    def close(self) -> None:
        """Close the body stream."""
        ...

class HTTP2Request:
    """
    HTTP/2 request wrapper compatible with gunicorn Request interface.

    Wraps an HTTP2Stream to provide the same interface as the HTTP/1.x
    Request class, allowing workers to handle HTTP/2 requests using
    existing code paths.
    """
    stream: HTTP2Stream
    cfg: Config
    peer_addr: _AddressType
    remote_addr: _AddressType
    version: tuple[int, int]
    method: str
    scheme: Literal["https", "http"]
    uri: str
    path: str
    query: str
    fragment: str
    headers: list[tuple[str, str]]
    trailers: list[tuple[str, Incomplete]]
    body: HTTP2Body
    must_close: bool
    req_number: int
    proxy_protocol_info: dict[str, str | int | None] | None  # TODO: Use TypedDict
    priority_weight: int
    priority_depends_on: int

    def __init__(self, stream: HTTP2Stream, cfg: Config, peer_addr: _AddressType) -> None:
        """
        Initialize from an HTTP/2 stream.

        Args:
            stream: HTTP2Stream instance with received headers/body
            cfg: Gunicorn configuration object
            peer_addr: Client address tuple (host, port)
        """
        ...
    def force_close(self) -> None:
        """Force the connection to close after this request."""
        ...
    def should_close(self) -> bool:
        """
        Check if connection should close after this request.

        HTTP/2 connections are persistent by design, but we may still
        need to close if explicitly requested.

        Returns:
            bool: True if connection should close
        """
        ...
    def get_header(self, name: str) -> str | None:
        """
        Get a header value by name.

        Args:
            name: Header name (case-insensitive)

        Returns:
            str: Header value, or None if not found
        """
        ...
    @property
    def content_length(self) -> int | None:
        """
        Get the Content-Length header value.

        Returns:
            int: Content length, or None if not set
        """
        ...
    @property
    def content_type(self) -> str | None:
        """
        Get the Content-Type header value.

        Returns:
            str: Content type, or None if not set
        """
        ...

__all__ = ["HTTP2Request", "HTTP2Body"]

"""
HTTP/2 support for Gunicorn.

This module provides HTTP/2 protocol support using the hyper-h2 library.
HTTP/2 requires TLS with ALPN negotiation.
"""

from typing import Final

from .async_connection import AsyncHTTP2Connection
from .connection import HTTP2ServerConnection

H2_MIN_VERSION: Final[tuple[int, int, int]]

def is_http2_available() -> bool:
    """
    Check if HTTP/2 support is available.

    Returns:
        bool: True if the h2 library is installed with minimum required version.
    """
    ...
def get_h2_version() -> tuple[int, int, int]:
    """
    Get the installed h2 library version.

    Returns:
        tuple: Version tuple (major, minor, patch) or None if not installed.
    """
    ...
def get_http2_connection_class() -> type[HTTP2ServerConnection]:
    """
    Get the HTTP2ServerConnection class if h2 is available.

    Returns:
        HTTP2ServerConnection class, or raises HTTP2NotAvailable
    """
    ...
def get_async_http2_connection_class() -> type[AsyncHTTP2Connection]:
    """
    Get the AsyncHTTP2Connection class if h2 is available.

    Returns:
        AsyncHTTP2Connection class, or raises HTTP2NotAvailable
    """
    ...

__all__ = [
    "is_http2_available",
    "get_h2_version",
    "get_http2_connection_class",
    "get_async_http2_connection_class",
    "H2_MIN_VERSION",
]

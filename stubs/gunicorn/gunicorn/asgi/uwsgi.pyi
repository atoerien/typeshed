"""
Async uWSGI protocol parser for ASGI workers.

Reuses the parsing logic from gunicorn/uwsgi/message.py, only async I/O differs.
"""

from typing import Literal
from typing_extensions import Self

from gunicorn.asgi.unreader import AsyncUnreader
from gunicorn.config import Config
from gunicorn.uwsgi.message import UWSGIRequest

from .._types import _AddressType

class AsyncUWSGIRequest(UWSGIRequest):
    """
    Async version of UWSGIRequest.

    Reuses all parsing logic from the sync version, only async I/O differs.
    The following methods are reused from the parent class:
    - _parse_vars() - pure parsing, no I/O
    - _extract_request_info() - pure transformation
    - _check_allowed_ip() - no I/O
    - should_close() - simple logic
    """
    cfg: Config
    unreader: AsyncUnreader  # type: ignore[assignment]
    peer_addr: _AddressType
    remote_addr: _AddressType
    req_number: int
    method: str | None
    uri: str | None
    path: str | None
    query: str | None
    fragment: str | None
    version: tuple[int, int]
    headers: list[tuple[str, str]]
    trailers: list[tuple[str, str]]
    scheme: Literal["https", "http"]
    must_close: bool
    uwsgi_vars: dict[str, str]
    modifier1: int
    modifier2: int
    proxy_protocol_info: dict[str, str | int | None] | None  # TODO: Use TypedDict
    content_length: int
    chunked: bool

    def __init__(self, cfg: Config, unreader: AsyncUnreader, peer_addr: _AddressType, req_number: int = 1) -> None: ...
    @classmethod
    async def parse(cls, cfg: Config, unreader: AsyncUnreader, peer_addr: _AddressType, req_number: int = 1) -> Self:
        """
        Parse a uWSGI request asynchronously.

        Args:
            cfg: gunicorn config object
            unreader: AsyncUnreader instance
            peer_addr: client address tuple
            req_number: request number on this connection (for keepalive)

        Returns:
            AsyncUWSGIRequest: Parsed request object

        Raises:
            InvalidUWSGIHeader: If the uWSGI header is malformed
            UnsupportedModifier: If modifier1 is not 0
            ForbiddenUWSGIRequest: If source IP is not allowed
        """
        ...
    async def read_body(self, size: int = 8192) -> bytes:
        """
        Read body chunk asynchronously.

        Args:
            size: Maximum bytes to read

        Returns:
            bytes: Body data, empty bytes when body is exhausted
        """
        ...
    async def drain_body(self) -> None:
        """
        Drain unread body data.

        Should be called before reusing connection for keepalive.
        """
        ...
    def get_header(self, name: str) -> str | None:
        """
        Get header by name (case-insensitive).

        Args:
            name: Header name to look up

        Returns:
            Header value if found, None otherwise
        """
        ...

"""
HTTP parser for ASGI workers.

Provides callback-based parsing using either the fast C parser (gunicorn_h1c)
or the pure Python PythonProtocol fallback.
"""

from collections.abc import Callable, Iterable
from enum import IntEnum
from typing import Any, Final, Literal, SupportsIndex, TypedDict, type_check_only
from typing_extensions import Self, TypeAlias

_H1CProtocol: TypeAlias = Any  # gunicorn_h1c H1CProtocol class

class ParseError(Exception): ...
class InvalidProxyLine(ParseError): ...
class InvalidProxyHeader(ParseError): ...

PP_V2_SIGNATURE: Final[bytes]

class PPCommand(IntEnum):
    LOCAL = 0x0
    PROXY = 0x1

class PPFamily(IntEnum):
    UNSPEC = 0x0
    INET = 0x1
    INET6 = 0x2
    UNIX = 0x3

class PPProtocol(IntEnum):
    UNSPEC = 0x0
    STREAM = 0x1
    DGRAM = 0x2

class LimitRequestLine(ParseError): ...
class InvalidRequestLine(ParseError): ...
class LimitRequestHeaders(ParseError): ...
class InvalidRequestMethod(ParseError): ...
class InvalidHTTPVersion(ParseError): ...
class InvalidHeaderName(ParseError): ...
class InvalidHeader(ParseError): ...
class UnsupportedTransferCoding(ParseError): ...
class InvalidChunkSize(ParseError): ...
class InvalidChunkExtension(ParseError): ...

@type_check_only
class _ProxyProtocolInfo(TypedDict):
    proxy_protocol: Literal["TCP4", "TCP6", "UDP4", "UDP6"]
    client_addr: str
    client_port: int
    proxy_addr: str
    proxy_port: int

@type_check_only
class _ProxyProtocolInfoUnknown(TypedDict):
    proxy_protocol: Literal["UNKNOWN", "LOCAL", "UNSPEC"]
    client_addr: None
    client_port: None
    proxy_addr: None
    proxy_port: None

class PythonProtocol:
    """
    Callback-based HTTP/1.1 parser (pure Python fallback).

    Mirrors H1CProtocol interface for seamless switching between
    the C extension and pure Python implementations.

    Callbacks:
        on_message_begin: () -> None - Called when request starts
        on_url: (url: bytes) -> None - Called with request URL/path
        on_header: (name: bytes, value: bytes) -> None - Called for each header
        on_headers_complete: () -> bool - Called when headers done (return True to skip body)
        on_body: (chunk: bytes) -> None - Called with body data chunks
        on_message_complete: () -> None - Called when request is complete
    """
    __slots__ = (
        "_on_message_begin",
        "_on_url",
        "_on_header",
        "_on_headers_complete",
        "_on_body",
        "_on_message_complete",
        "_state",
        "_buffer",
        "_headers_list",
        "method",
        "path",
        "http_version",
        "headers",
        "content_length",
        "is_chunked",
        "should_keep_alive",
        "is_complete",
        "_body_remaining",
        "_skip_body",
        "_chunk_state",
        "_chunk_size",
        "_chunk_remaining",
        "_limit_request_line",
        "_limit_request_fields",
        "_limit_request_field_size",
        "_permit_unconventional_http_method",
        "_permit_unconventional_http_version",
        "_header_count",
        "_proxy_protocol",
        "_proxy_protocol_info",
        "_proxy_protocol_done",
    )
    method: bytes | None
    path: bytes | None
    http_version: tuple[int, int] | None
    headers: list[tuple[bytes, bytes]]
    content_length: int | None
    is_chunked: bool
    should_keep_alive: bool
    is_complete: bool

    def __init__(
        self,
        on_message_begin: Callable[[], object] | None = None,
        on_url: Callable[[bytes], object] | None = None,
        on_header: Callable[[bytes, bytes], object] | None = None,
        on_headers_complete: Callable[[], bool] | None = None,
        on_body: Callable[[bytes], object] | None = None,
        on_message_complete: Callable[[], object] | None = None,
        limit_request_line: int = 8190,
        limit_request_fields: int = 100,
        limit_request_field_size: int = 8190,
        permit_unconventional_http_method: bool = False,
        permit_unconventional_http_version: bool = False,
        proxy_protocol: Literal["off", "v1", "v2", "auto"] = "off",
    ) -> None: ...
    def feed(self, data: Iterable[SupportsIndex]) -> None: ...
    @property
    def proxy_protocol_info(self) -> _ProxyProtocolInfo | _ProxyProtocolInfoUnknown | None: ...
    def reset(self) -> None: ...
    def finish(self) -> None: ...

class CallbackRequest:
    """
    Request object built from callback parser state.

    Works with both H1CProtocol (C extension) and PythonProtocol.
    """
    __slots__ = (
        "method",
        "uri",
        "path",
        "query",
        "fragment",
        "version",
        "headers",
        "headers_bytes",
        "scheme",
        "raw_path",
        "content_length",
        "chunked",
        "must_close",
        "proxy_protocol_info",
        "_expect_100_continue",
    )
    method: str | None
    uri: str | None
    path: str | None
    query: str | None
    fragment: str | None
    version: tuple[int, int] | None
    headers: list[tuple[str, str]]
    headers_bytes: list[tuple[bytes, bytes]]
    scheme: Literal["https", "http"]
    raw_path: bytes
    content_length: int
    chunked: bool
    must_close: bool
    proxy_protocol_info: dict[str, str | int | None] | None  # TODO: Use TypedDict

    def __init__(self) -> None: ...
    @classmethod
    def from_parser(cls, parser: _H1CProtocol | PythonProtocol, is_ssl: bool = False) -> Self:
        """
        Build request from callback parser state.

        Args:
            parser: H1CProtocol or PythonProtocol instance
            is_ssl: Whether connection is SSL/TLS

        Returns:
            CallbackRequest instance
        """
        ...
    def should_close(self) -> bool:
        """Check if connection should be closed after this request."""
        ...
    def get_header(self, name: str) -> str | None:
        """Get a header value by name (case-insensitive)."""
        ...

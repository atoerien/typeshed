from typing import Final, Literal

from gunicorn.config import Config
from gunicorn.http.body import Body
from gunicorn.http.unreader import Unreader

from .._types import _AddressType
from ..asgi.parser import _ProxyProtocolInfo, _ProxyProtocolInfoUnknown

MAX_UWSGI_VARS: Final = 1000

class UWSGIRequest:
    """
    uWSGI protocol request parser.

    The uWSGI protocol uses a 4-byte binary header:
    - Byte 0: modifier1 (packet type, 0 = WSGI request)
    - Bytes 1-2: datasize (16-bit little-endian, size of vars block)
    - Byte 3: modifier2 (additional flags, typically 0)

    After the header:
    1. Vars block (datasize bytes): Key-value pairs containing WSGI environ
       - Each pair: 2-byte key_size (LE) + key + 2-byte val_size (LE) + value
    2. Request body (determined by CONTENT_LENGTH in vars)
    """
    cfg: Config
    unreader: Unreader
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
    body: Body | None
    scheme: Literal["https", "http"]
    must_close: bool
    uwsgi_vars: dict[str, str]
    modifier1: int
    modifier2: int
    proxy_protocol_info: _ProxyProtocolInfo | _ProxyProtocolInfoUnknown | None

    def __init__(self, cfg: Config, unreader: Unreader, peer_addr: _AddressType, req_number: int = 1) -> None: ...
    def force_close(self) -> None:
        """Force the connection to close after this request."""
        ...
    def parse(self, unreader: Unreader) -> bytes:
        """Parse uWSGI packet header and vars block."""
        ...
    def set_body_reader(self) -> None:
        """Set up the body reader based on CONTENT_LENGTH."""
        ...
    def should_close(self) -> bool:
        """Determine if the connection should be closed after this request."""
        ...

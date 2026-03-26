"""
WebSocket protocol handler for ASGI.

Implements RFC 6455 WebSocket protocol for ASGI applications.
"""

import asyncio
from typing import Final

from gunicorn.glogging import Logger as GLogger

from .._types import _ASGIAppType, _ScopeType

OPCODE_CONTINUATION: Final = 0x0
OPCODE_TEXT: Final = 0x1
OPCODE_BINARY: Final = 0x2
OPCODE_CLOSE: Final = 0x8
OPCODE_PING: Final = 0x9
OPCODE_PONG: Final = 0xA
CLOSE_NORMAL: Final = 1000
CLOSE_GOING_AWAY: Final = 1001
CLOSE_PROTOCOL_ERROR: Final = 1002
CLOSE_UNSUPPORTED: Final = 1003
CLOSE_NO_STATUS: Final = 1005
CLOSE_ABNORMAL: Final = 1006
CLOSE_INVALID_DATA: Final = 1007
CLOSE_POLICY_VIOLATION: Final = 1008
CLOSE_MESSAGE_TOO_BIG: Final = 1009
CLOSE_MANDATORY_EXT: Final = 1010
CLOSE_INTERNAL_ERROR: Final = 1011
WS_GUID: Final = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

class WebSocketProtocol:
    """
    WebSocket connection handler for ASGI applications.

    Uses callback-based data feeding instead of StreamReader for efficiency.
    Data is fed via feed_data() from the parent protocol's data_received().
    """
    transport: asyncio.Transport
    scope: _ScopeType
    app: _ASGIAppType
    log: GLogger
    accepted: bool
    closed: bool
    close_code: int | None
    close_reason: str | None

    def __init__(self, transport: asyncio.Transport, scope: _ScopeType, app: _ASGIAppType, log: GLogger) -> None:
        """
        Initialize WebSocket protocol handler.

        Args:
            transport: asyncio transport for writing
            scope: ASGI WebSocket scope dict
            app: ASGI application callable
            log: Logger instance
        """
        ...
    def feed_data(self, data: bytes) -> None:
        """
        Feed incoming data from the parent protocol's data_received().

        Args:
            data: bytes received on the connection
        """
        ...
    def feed_eof(self) -> None:
        """Signal that the connection has been closed."""
        ...
    async def run(self) -> None:
        """Run the WebSocket ASGI application."""
        ...

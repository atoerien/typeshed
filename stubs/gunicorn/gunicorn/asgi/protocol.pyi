"""
ASGI protocol handler for gunicorn.

Implements asyncio.Protocol to handle HTTP/1.x and HTTP/2 connections
and dispatch to ASGI applications.
"""

import asyncio
from collections.abc import Iterable
from typing import Final, Literal, TypedDict, type_check_only
from typing_extensions import NotRequired

from gunicorn.asgi.parser import CallbackRequest
from gunicorn.config import Config
from gunicorn.glogging import Logger as GLogger
from gunicorn.workers.gasgi import ASGIWorker

from .._types import _ASGIAppType

HIGH_WATER_LIMIT: Final = 65536

class FlowControl:
    """
    Manage transport-level write flow control.

    Blocks send() when transport buffer exceeds high water mark,
    preventing memory issues with large streaming responses.
    """
    __slots__ = ("_transport", "read_paused", "write_paused", "_is_writable_event")
    read_paused: bool
    write_paused: bool

    def __init__(self, transport: asyncio.BaseTransport) -> None: ...
    async def drain(self) -> None:
        """Wait until transport is writable."""
        ...
    def pause_reading(self) -> None: ...
    def resume_reading(self) -> None: ...
    def pause_writing(self) -> None: ...
    def resume_writing(self) -> None: ...

class ASGIResponseInfo:
    """Simple container for ASGI response info for access logging."""
    status: str | int
    sent: int
    headers: list[tuple[str, str]]

    def __init__(self, status: str | int, headers: Iterable[tuple[str | bytes, str | bytes]], sent: int) -> None: ...

@type_check_only
class _BodyReceieverReceiveReturnType(TypedDict):
    type: Literal["http.disconnect", "http.request"]
    body: NotRequired[bytes]
    more_body: NotRequired[bool]

class BodyReceiver:
    """
    Body receiver for callback-based parsers.

    Body chunks are fed directly via the feed() method from parser callbacks.
    Uses Future-based waiting for efficient async receive().
    """
    __slots__ = ("_chunks", "_complete", "_body_finished", "_closed", "_waiter", "request", "protocol")
    request: CallbackRequest
    protocol: ASGIProtocol

    def __init__(self, request: CallbackRequest, protocol: ASGIProtocol) -> None: ...
    def feed(self, chunk: bytes) -> None:
        """Feed a body chunk directly (called by parser callback)."""
        ...
    def set_complete(self) -> None:
        """Mark body as complete (called when message ends)."""
        ...
    def signal_disconnect(self) -> None:
        """Signal that connection has been lost."""
        ...
    async def receive(self) -> _BodyReceieverReceiveReturnType:
        """ASGI receive callable - returns body chunks or disconnect."""
        ...

class ASGIProtocol(asyncio.Protocol):
    """
    HTTP/1.1 protocol handler for ASGI applications.

    Handles connection lifecycle, request parsing, and ASGI app invocation.
    Uses callback-based parsing (H1CProtocol/PythonProtocol) for efficient
    incremental parsing in data_received().
    """
    worker: ASGIWorker
    cfg: Config
    log: GLogger
    app: _ASGIAppType
    transport: asyncio.BaseTransport | None
    reader: asyncio.StreamReader | None
    writer: asyncio.BaseTransport | None
    req_count: int

    def __init__(self, worker: ASGIWorker) -> None: ...

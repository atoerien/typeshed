"""
ASGI protocol handler for gunicorn.

Implements asyncio.Protocol to handle HTTP/1.x and HTTP/2 connections
and dispatch to ASGI applications.
"""

import asyncio
from _typeshed import Incomplete
from collections.abc import Iterable
from typing import Final

from gunicorn.asgi.parser import CallbackRequest
from gunicorn.config import Config
from gunicorn.glogging import Logger as GLogger
from gunicorn.workers.gasgi import ASGIWorker

from .._types import _ASGIAppType

HIGH_WATER_LIMIT: Final = 65536

class FlowControl:
    __slots__ = ("_transport", "read_paused", "write_paused", "_is_writable_event")
    read_paused: bool
    write_paused: bool

    def __init__(self, transport: asyncio.BaseTransport) -> None: ...
    async def drain(self) -> None: ...
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

class BodyReceiver:
    __slots__ = ("_chunks", "_complete", "_body_finished", "_closed", "_waiter", "request", "protocol")
    request: CallbackRequest
    protocol: ASGIProtocol

    def __init__(self, request: CallbackRequest, protocol: ASGIProtocol) -> None: ...
    def feed(self, chunk: bytes) -> None: ...
    def set_complete(self) -> None: ...
    def signal_disconnect(self) -> None: ...
    async def receive(self) -> dict[str, Incomplete]: ...  # TODO: Use TypedDict

class ASGIProtocol(asyncio.Protocol):
    """
    HTTP/1.1 protocol handler for ASGI applications.

    Handles connection lifecycle, request parsing, and ASGI app invocation.
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

"""
ASGI protocol handler for gunicorn.

Implements asyncio.Protocol to handle HTTP/1.x and HTTP/2 connections
and dispatch to ASGI applications.
"""

import asyncio
from collections.abc import Iterable

from gunicorn.config import Config
from gunicorn.glogging import Logger as GLogger
from gunicorn.workers.gasgi import ASGIWorker

from .._types import _ASGIAppType

class ASGIResponseInfo:
    """Simple container for ASGI response info for access logging."""
    status: str | int
    sent: int
    headers: list[tuple[str, str]]

    def __init__(self, status: str | int, headers: Iterable[tuple[str | bytes, str | bytes]], sent: int) -> None: ...

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

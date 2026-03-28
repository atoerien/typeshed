"""
ASGI support for gunicorn.

This module provides native ASGI worker support, using gunicorn's own
HTTP parsing infrastructure adapted for async I/O.

Components:
- AsyncUnreader: Async socket reading with pushback buffer
- ASGIProtocol: asyncio.Protocol implementation for HTTP handling
- WebSocketProtocol: WebSocket protocol handler (RFC 6455)
- LifespanManager: ASGI lifespan protocol support

Usage:
    gunicorn -k asgi myapp:app
"""

from gunicorn.asgi.lifespan import LifespanManager as LifespanManager
from gunicorn.asgi.unreader import AsyncUnreader as AsyncUnreader

__all__ = ["AsyncUnreader", "LifespanManager"]

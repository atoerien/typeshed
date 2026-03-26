"""
Async version of gunicorn/http/unreader.py for ASGI workers.

Provides async reading with pushback buffer support.
"""

import asyncio
import io
from _typeshed import ReadableBuffer

class AsyncUnreader:
    """
    Async socket reader with pushback buffer support.

    This class wraps an asyncio StreamReader and provides the ability
    to "unread" data back into a buffer for re-parsing.

    Performance optimization: Reuses BytesIO buffer with truncate/seek
    instead of creating new objects to reduce GC pressure.
    """
    reader: asyncio.StreamReader
    buf: io.BytesIO
    max_chunk: int

    def __init__(self, reader: asyncio.StreamReader, max_chunk: int = 8192) -> None:
        """
        Initialize the async unreader.

        Args:
            reader: asyncio.StreamReader instance
            max_chunk: Maximum bytes to read at once
        """
        ...
    async def read(self, size: int | None = None) -> bytes:
        """
        Read data from the stream, using buffered data first.

        Args:
            size: Number of bytes to read. If None, returns all buffered
                  data or reads a single chunk.

        Returns:
            bytes: Data read from buffer or stream
        """
        ...
    def unread(self, data: ReadableBuffer) -> None:
        """
        Push data back into the buffer for re-reading.

        Args:
            data: bytes to push back

        Note: This prepends data to the buffer so it will be read first.
        """
        ...
    def has_buffered_data(self) -> bool:
        """Check if there's data in the pushback buffer."""
        ...

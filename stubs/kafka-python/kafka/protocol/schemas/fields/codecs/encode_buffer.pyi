from _typeshed import Incomplete, ReadableBuffer, Unused
from collections.abc import Iterable
from typing import SupportsIndex

class EncodeBuffer:
    """
    Growable byte buffer for the ``encode_into`` fast path.

    The encoders write primitives directly into ``buf`` at offset ``pos``
    rather than building and joining intermediate ``bytes`` objects. The
    buffer starts at a fixed size and grows on demand via :meth:`ensure`.

    Capacity contract
    -----------------
    Writing past the end of ``buf`` does not grow it automatically:

      * single-byte index writes (``buf[pos] = x``) raise ``IndexError``,
      * ``pack_into`` raises ``struct.error``,
      * slice assignment (``buf[pos:pos+n] = data``) silently *resizes* the
        bytearray, defeating the preallocation.

    Therefore **every writer must call** ``ensure(n)`` to reserve ``n`` bytes
    before writing ``n`` bytes at ``pos`` (where ``n`` is the maximum the write
    can consume - e.g. ``5`` for a varint32, a fixed field's ``size``, or
    ``len(payload)`` for variable data). See the codecs in ``types.py`` for the
    pattern, and ``CodegenContext.emit_reserve`` for the compiled equivalent.

    Reallocation note
    -----------------
    ``ensure`` may replace ``buf`` with a larger bytearray. Any caller (or
    generated code) that caches ``buf`` in a local **must re-read** ``self.buf``
    after a call that can grow it - including indirect growth through a nested
    ``encode_into`` / ``ensure``. Forgetting to re-read leaves writes targeting
    the old, discarded buffer (silent data loss) or raises out of range.
    """
    __slots__ = ("buf", "pos")
    buf: bytearray
    pos: int
    def __init__(self, size: Iterable[SupportsIndex] | SupportsIndex | ReadableBuffer = 65536) -> None: ...
    def reset(self) -> None:
        """Reset position to 0 for reuse. The buffer retains its current size."""
        ...
    def ensure(self, needed: int) -> None:
        """
        Guarantee at least ``needed`` writable bytes remain at ``pos``.

        Call this *before* writing ``needed`` bytes at ``self.pos``. If the
        current buffer cannot hold them it is grown (at least doubled) and the
        existing ``[:pos]`` content is preserved.

        WARNING: this may rebind ``self.buf`` to a new bytearray, so re-read
        ``self.buf`` afterwards if you hold a local reference to it (see the
        class docstring).
        """
        ...
    def result(self) -> bytearray:
        """Return the encoded bytes written so far (``buf[:pos]``)."""
        ...

class EncodeBufferPool:
    """
    Thread-local pool of reusable EncodeBuffer objects.

    Each thread gets its own buffer that grows to match the largest message
    encoded on that thread and stays that size - avoiding repeated allocation
    of large bytearrays.

    Usage:
        with EncodeBufferPool.acquire() as out:
            fast_encode(item, out)
            return out.result()
    """
    @classmethod
    def acquire(cls) -> _PooledBuffer:
        """Return a context manager that provides a reset EncodeBuffer."""
        ...

class _PooledBuffer:
    """Context manager for EncodeBufferPool.acquire()."""
    __slots__ = ("_pool", "_buf")
    def __init__(self, pool: EncodeBufferPool) -> None: ...
    def __enter__(self) -> EncodeBuffer | Incomplete: ...
    def __exit__(self, *exc: Unused): ...

import socket
from collections.abc import Callable, Iterable, Iterator
from typing import ClassVar

from gunicorn.config import Config
from gunicorn.http.message import Request
from gunicorn.http.unreader import Unreader

from .._types import _AddressType

class Parser:
    # TODO: Use Protocol instead of Request class
    mesg_class: ClassVar[type[Request] | None]
    cfg: Config
    unreader: Unreader
    mesg: Request | None
    source_addr: _AddressType
    req_count: int

    def __init__(self, cfg: Config, source: socket.socket | Iterable[bytes], source_addr: _AddressType) -> None: ...
    def __iter__(self) -> Iterator[Request]: ...
    def finish_body(self, deadline: float | None = None, max_bytes: int | None = None) -> None:
        """
        Discard any unread body of the current message.

        Called before returning a keepalive connection to the poller so the
        socket does not appear readable due to leftover body bytes.

        ``deadline`` is an absolute ``time.monotonic()`` value; when set the
        socket read timeout is bounded by the remaining time before each read.
        ``max_bytes`` caps the total drained bytes; when a deadline is given
        and ``max_bytes`` is left at the default, ``_DRAIN_MAX_BYTES`` applies
        to defend against a slow client that keeps trickling under it.  When
        called without a deadline (the default invocation from ``__next__``),
        no byte cap is applied so the prior unbounded drain semantics are
        preserved for callers that don't know how to react to a partial drain.

        Returns ``True`` when the body was fully drained, ``False`` when the
        drain was abandoned (deadline, byte cap, or socket timeout).  Callers
        that observe ``False`` MUST close the connection rather than serve
        another request on it.
        """
        ...
    def __next__(self) -> Request: ...

    next: Callable[[Parser], Request]

class RequestParser(Parser):
    mesg_class: ClassVar[type[Request]]

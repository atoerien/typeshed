"""
Asyncio integration for ``pycurl.CurlMulti``.

Drives :py:class:`pycurl.CurlMulti` transfers from an asyncio event loop
using libcurl's multi-socket API. No threads, no busy-polling. A
selector-style event loop is required (on Windows install
``WindowsSelectorEventLoopPolicy``).

Example::

    async with pycurl.AsyncCurlMulti() as multi:
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, "https://example.com")
        await multi.perform(curl)
        print(curl.getinfo(pycurl.RESPONSE_CODE))
"""

import asyncio
from collections.abc import Iterable
from types import TracebackType
from typing import Any
from typing_extensions import Self

from pycurl._pycurl import Curl

class AsyncCurlMulti:
    """
    AsyncCurlMulti(close_handles=False) -> AsyncCurlMulti object

    An asyncio-driven wrapper around :py:class:`pycurl.CurlMulti`. Each
    :py:class:`pycurl.Curl` transfer is represented by an
    :py:class:`asyncio.Future` that resolves to the same ``Curl`` object on
    success or raises :py:class:`pycurl.error` on failure.

    The constructor does not require a running event loop; the loop is
    captured on the first call to :py:meth:`add_handle` and the instance
    is bound to that loop for its lifetime.

    A selector-style asyncio event loop is required. On a non-selector
    loop (e.g., Windows ``ProactorEventLoop``) :py:meth:`add_handle`
    raises :py:exc:`RuntimeError` with guidance on switching policy.

    Always call :py:meth:`aclose` (or use ``async with``) to release the
    underlying multi handle promptly.

    *close_handles* is forwarded to :py:class:`pycurl.CurlMulti`. When
    ``True``, any easy handle still attached to the multi when
    :py:meth:`aclose` runs is also closed by libcurl.

    Example::

        async with pycurl.AsyncCurlMulti() as multi:
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, "https://example.com")
            await multi.perform(curl)
            print(curl.getinfo(pycurl.RESPONSE_CODE))

    Batch example::

        async with pycurl.AsyncCurlMulti() as multi:
            for url in urls:
                curl = pycurl.Curl()
                curl.setopt(pycurl.URL, url)
                multi.add_handle(curl)
            results = await asyncio.gather(*multi.futures())
    """
    def __init__(self, close_handles: bool = False) -> None: ...
    def setopt(self, option: int, value: Any) -> None:
        """
        setopt(option, value) -> None

        Sets a multi-handle option. Equivalent to
        :py:meth:`pycurl.CurlMulti.setopt`, except that
        ``M_SOCKETFUNCTION``, ``M_TIMERFUNCTION``, and (on libcurl 8.17.0+)
        ``M_NOTIFYFUNCTION`` are owned by ``AsyncCurlMulti`` and raise
        :py:exc:`ValueError` if set externally.

        *option* is a ``pycurl.M_*`` constant identifying which option to
        set. *value* is the new option value; different options accept
        values of different types (see :py:meth:`pycurl.CurlMulti.setopt`).
        """
        ...
    def add_handle(self, curl: Curl) -> asyncio.Future[Curl]:
        """
        add_handle(curl) -> asyncio.Future

        Schedules *curl* for transfer and returns an
        :py:class:`asyncio.Future` that resolves to *curl* on success or
        raises :py:class:`pycurl.error` on failure. Cancelling the future
        removes the handle; cleanup runs on the next event-loop tick.

        *curl* is a :py:class:`pycurl.Curl` easy handle.

        The first call captures the running event loop and binds this
        instance to it. Raises :py:exc:`RuntimeError` if called outside
        a running loop, after :py:meth:`aclose`, or if *curl* is already
        registered.
        """
        ...
    def remove_handle(self, curl: Curl) -> None:
        """
        remove_handle(curl) -> None

        Removes *curl* from this multi handle and cancels its future
        (if not already done). Synchronous; if you need to observe the
        cancellation propagate, await the future returned from the
        original :py:meth:`add_handle` call.

        *curl* is a :py:class:`pycurl.Curl` easy handle. Raises
        :py:exc:`RuntimeError` if *curl* is not registered or after
        :py:meth:`aclose`. Raises :py:class:`pycurl.error` if libcurl
        rejects the removal.
        """
        ...
    async def perform(self, curl: Curl) -> Curl:
        """
        perform(curl) -> Curl object

        Coroutine equivalent to ``await self.add_handle(curl)``. Schedules
        *curl* for transfer and returns it once the transfer completes.
        Raises :py:class:`pycurl.error` on failure.

        *curl* is a :py:class:`pycurl.Curl` easy handle.
        """
        ...
    def futures(self, curls: Iterable[Curl] | None = None) -> tuple[asyncio.Future[Curl], ...]:
        """
        futures(curls=None) -> tuple of asyncio.Future

        Returns a snapshot of futures for transfers currently registered
        with this multi handle.

        *curls* is either ``None`` (the default) or an iterable of
        :py:class:`pycurl.Curl` easy handles. When ``None``, the result
        contains every pending future in the order in which the handles
        were added via :py:meth:`add_handle`. When an iterable is given,
        the result contains the corresponding futures in input order and
        length (so duplicates yield duplicate references to the same
        future).

        Completed or cancelled transfers are not included in later
        snapshots.

        Raises :py:exc:`KeyError` if any handle in *curls* is not
        currently registered.
        """
        ...
    @property
    def closed(self) -> bool:
        """Whether the underlying :py:class:`pycurl.CurlMulti` handle is closed."""
        ...
    async def aclose(self) -> None:
        """
        aclose() -> None

        Coroutine. Cancels the pending timer, removes all in-flight
        handles, unregisters socket watchers, and closes the underlying
        multi handle. Pending futures are cancelled. Idempotent.
        """
        ...
    async def __aenter__(self) -> Self: ...
    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, tb: TracebackType | None
    ) -> None: ...

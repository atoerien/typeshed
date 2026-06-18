"""
This module implements an interface to the cURL library.

Types:

Curl() -> New object.  Create a new curl object.
CurlMulti() -> New object.  Create a new curl multi object.
CurlShare() -> New object.  Create a new curl share object.

Functions:

global_init(option) -> None.  Initialize curl environment.
global_cleanup() -> None.  Cleanup curl environment.
version_info() -> tuple.  Return version information.
"""

import sys
from _typeshed import ReadableBuffer, WriteableBuffer
from collections.abc import Callable
from datetime import datetime
from types import TracebackType
from typing import Any, Final, Literal, NamedTuple
from typing_extensions import Self, disjoint_base

version: str

def global_init(option: int) -> None:
    """
    global_init(option) -> None

    Initialize curl environment.

    *option* is one of the constants pycurl.GLOBAL_SSL, pycurl.GLOBAL_WIN32,
    pycurl.GLOBAL_ALL, pycurl.GLOBAL_NOTHING, pycurl.GLOBAL_DEFAULT.

    Corresponds to `curl_global_init`_ in libcurl.

    .. _curl_global_init: https://curl.haxx.se/libcurl/c/curl_global_init.html
    """
    ...
def global_cleanup() -> None:
    """
    global_cleanup() -> None

    Cleanup curl environment.

    Corresponds to `curl_global_cleanup`_ in libcurl.

    .. _curl_global_cleanup: https://curl.haxx.se/libcurl/c/curl_global_cleanup.html
    """
    ...
def version_info(
    stamp: int = ...,
) -> tuple[int, str, int, str, int, str, int, str, tuple[str, ...], str | None, int, str | None]: ...

class error(Exception):
    # libcurl protocol errors raise (code, message); arg-parse errors raise (message,).
    args: tuple[int, str] | tuple[str]

class WsFrame(NamedTuple):
    """WsFrame(age, flags, offset, bytesleft, len)"""
    age: int
    flags: int
    offset: int
    bytesleft: int
    len: int

class HstsEntry(NamedTuple):
    """HstsEntry(host, expire, include_subdomains)"""
    host: bytes
    expire: datetime | None
    include_subdomains: bool

class HstsIndex(NamedTuple):
    """HstsIndex(index, total)"""
    index: int  # type: ignore[assignment]
    total: int

class KhKey(NamedTuple):
    """KhKey(key, keytype)"""
    key: bytes
    keytype: int

class CurlSockAddr(NamedTuple):
    """CurlSockAddr(family, socktype, protocol, addr)"""
    family: int
    socktype: int
    protocol: int
    addr: tuple[str, int] | tuple[str, int, int, int] | bytes

@disjoint_base
class Curl:
    """
    Curl() -> New Curl object

    Creates a new :ref:`curlobject` which corresponds to a
    ``CURL`` handle in libcurl. Curl objects automatically set
    CURLOPT_VERBOSE to 0, CURLOPT_NOPROGRESS to 1, provide a default
    CURLOPT_USERAGENT and setup CURLOPT_ERRORBUFFER to point to a
    private error buffer.

    Implicitly calls :py:func:`pycurl.global_init` if the latter has not yet been called.

    The ``Curl`` object can be used as a context manager. Exiting the
    context calls ``close()``.

    Example::

        with pycurl.Curl() as c:
            # perform operations
    """
    USERPWD: int
    def close(self) -> None: ...
    def closed(self) -> bool: ...
    # For `setopt()` the exact `value` type depends on the passed `option`; `None` used to unassign:
    # http://pycurl.io/docs/latest/curlobject.html#pycurl.Curl.setopt
    def setopt(self, option: int, value: Any | None) -> None: ...
    def setopt_string(self, option: int, value: str) -> None: ...
    def perform(self) -> None: ...
    def perform_rb(self) -> bytes: ...
    def perform_rs(self) -> str: ...
    # For getinfo and getinfo_raw, the exact return type depends on the passed value:
    # http://pycurl.io/docs/latest/curlobject.html#pycurl.Curl.getinfo
    def getinfo(self, info: int) -> Any:
        """
        getinfo(option) -> Result

        Extract and return information from a curl session,
        decoding string data in Python's default encoding at the time of the call.
        Corresponds to `curl_easy_getinfo`_ in libcurl.
        The ``getinfo`` method should not be called unless
        ``perform`` has been called and finished.

        *option* is a constant corresponding to one of the
        ``CURLINFO_*`` constants in libcurl. Most option constant names match
        the respective ``CURLINFO_*`` constant names with the ``CURLINFO_`` prefix
        removed, for example ``CURLINFO_CONTENT_TYPE`` is accessible as
        ``pycurl.CONTENT_TYPE``. Exceptions to this rule are as follows:

        - ``CURLINFO_FILETIME`` is mapped as ``pycurl.INFO_FILETIME``
        - ``CURLINFO_COOKIELIST`` is mapped as ``pycurl.INFO_COOKIELIST``
        - ``CURLINFO_CERTINFO`` is mapped as ``pycurl.INFO_CERTINFO``
        - ``CURLINFO_RTSP_CLIENT_CSEQ`` is mapped as ``pycurl.INFO_RTSP_CLIENT_CSEQ``
        - ``CURLINFO_RTSP_CSEQ_RECV`` is mapped as ``pycurl.INFO_RTSP_CSEQ_RECV``
        - ``CURLINFO_RTSP_SERVER_CSEQ`` is mapped as ``pycurl.INFO_RTSP_SERVER_CSEQ``
        - ``CURLINFO_RTSP_SESSION_ID`` is mapped as ``pycurl.INFO_RTSP_SESSION_ID``

        The type of return value depends on the option, as follows:

        - Options documented by libcurl to return an integer value return a
          Python ``int``.
        - Options documented by libcurl to return a floating point value
          return a Python ``float``.
        - Options documented by libcurl to return a string value
          return a Python ``str``.
          The data returned by libcurl is decoded using the
          default string encoding at the time of the call.
          If the data cannot be decoded using the default encoding, ``UnicodeDecodeError``
          is raised. Use :ref:`getinfo_raw <getinfo_raw>`
          to retrieve the data as ``bytes`` in these
          cases.
        - ``SSL_ENGINES`` and ``INFO_COOKIELIST`` return a list of strings.
          The same encoding caveats apply; use :ref:`getinfo_raw <getinfo_raw>`
          to retrieve the
          data as a list of byte strings.
        - ``INFO_CERTINFO`` returns a list with one element
          per certificate in the chain, starting with the leaf; each element is a
          sequence of *(key, value)* tuples where both ``key`` and ``value`` are
          strings. String encoding caveats apply; use :ref:`getinfo_raw <getinfo_raw>`
          to retrieve
          certificate data as byte strings.
        - For libcurl versions >= 7.45.0, ``CURLINFO_LASTSOCKET`` is aliased to
          ``CURLINFO_ACTIVESOCKET`` to avoid unreliable results on some platforms.

        Example usage::

            import pycurl
            c = pycurl.Curl()
            c.setopt(pycurl.OPT_CERTINFO, 1)
            c.setopt(pycurl.URL, "https://python.org")
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.perform()
            print(c.getinfo(pycurl.HTTP_CODE))
            # --> 200
            print(c.getinfo(pycurl.EFFECTIVE_URL))
            # --> "https://www.python.org/"
            certinfo = c.getinfo(pycurl.INFO_CERTINFO)
            print(certinfo)
            # --> [(('Subject', 'C = AU, ST = Some-State, O = PycURL test suite,
                     CN = localhost'), ('Issuer', 'C = AU, ST = Some-State,
                     O = PycURL test suite, OU = localhost, CN = localhost'),
                    ('Version', '0'), ...)]


        Raises pycurl.error exception upon failure.

        .. _curl_easy_getinfo:
            https://curl.haxx.se/libcurl/c/curl_easy_getinfo.html
        """
        ...
    def getinfo_raw(self, info: int) -> Any:
        """
        getinfo_raw(option) -> Result

        Extract and return information from a curl session,
        returning string data as byte strings.
        Corresponds to `curl_easy_getinfo`_ in libcurl.
        The ``getinfo_raw`` method should not be called unless
        ``perform`` has been called and finished.

        *option* is a constant corresponding to one of the
        ``CURLINFO_*`` constants in libcurl. Most option constant names match
        the respective ``CURLINFO_*`` constant names with the ``CURLINFO_`` prefix
        removed, for example ``CURLINFO_CONTENT_TYPE`` is accessible as
        ``pycurl.CONTENT_TYPE``. Exceptions to this rule are as follows:

        - ``CURLINFO_FILETIME`` is mapped as ``pycurl.INFO_FILETIME``
        - ``CURLINFO_COOKIELIST`` is mapped as ``pycurl.INFO_COOKIELIST``
        - ``CURLINFO_CERTINFO`` is mapped as ``pycurl.INFO_CERTINFO``
        - ``CURLINFO_RTSP_CLIENT_CSEQ`` is mapped as ``pycurl.INFO_RTSP_CLIENT_CSEQ``
        - ``CURLINFO_RTSP_CSEQ_RECV`` is mapped as ``pycurl.INFO_RTSP_CSEQ_RECV``
        - ``CURLINFO_RTSP_SERVER_CSEQ`` is mapped as ``pycurl.INFO_RTSP_SERVER_CSEQ``
        - ``CURLINFO_RTSP_SESSION_ID`` is mapped as ``pycurl.INFO_RTSP_SESSION_ID``

        The type of return value depends on the option, as follows:

        - Options documented by libcurl to return an integer value return a
          Python ``int``.
        - Options documented by libcurl to return a floating point value
          return a Python ``float``.
        - Options documented by libcurl to return a string value
          return a Python ``bytes`` instance.
          The string contains whatever data libcurl returned.
          Use :ref:`getinfo <getinfo>` to retrieve this data as a Unicode string.
        - ``SSL_ENGINES`` and ``INFO_COOKIELIST`` return a list of byte strings.
          The same encoding caveats apply; use :ref:`getinfo <getinfo>` to retrieve the
          data as a list of potentially Unicode strings.
        - ``INFO_CERTINFO`` returns a list with one element
          per certificate in the chain, starting with the leaf; each element is a
          sequence of *(key, value)* tuples where both ``key`` and ``value`` are
          byte strings. String encoding caveats apply; use :ref:`getinfo <getinfo>`
          to retrieve
          certificate data as potentially Unicode strings.

        Example usage::

            import pycurl
            c = pycurl.Curl()
            c.setopt(pycurl.OPT_CERTINFO, 1)
            c.setopt(pycurl.URL, "https://python.org")
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.perform()
            print(c.getinfo_raw(pycurl.HTTP_CODE))
            # --> 200
            print(c.getinfo_raw(pycurl.EFFECTIVE_URL))
            # --> b"https://www.python.org/"
            certinfo = c.getinfo_raw(pycurl.INFO_CERTINFO)
            print(certinfo)
            # --> [((b'Subject', b'C = AU, ST = Some-State, O = PycURL test suite,
                     CN = localhost'), (b'Issuer', b'C = AU, ST = Some-State,
                     O = PycURL test suite, OU = localhost, CN = localhost'),
                    (b'Version', b'0'), ...)]


        Raises pycurl.error exception upon failure.

        *Added in version 7.43.0.2.*

        .. _curl_easy_getinfo:
            https://curl.haxx.se/libcurl/c/curl_easy_getinfo.html
        """
        ...
    def reset(self) -> None:
        """
        reset() -> None

        Reset all options set on curl handle to default values, but preserves
        live connections, session ID cache, DNS cache, cookies, and shares.

        Corresponds to `curl_easy_reset`_ in libcurl.

        .. _curl_easy_reset: https://curl.haxx.se/libcurl/c/curl_easy_reset.html
        """
        ...
    def unsetopt(self, option: int) -> None:
        """
        unsetopt(option) -> None

        Reset curl session option to its default value.

        Only some curl options may be reset via this method.

        libcurl does not provide a general way to reset a single option to its default value;
        :py:meth:`pycurl.Curl.reset` resets all options to their default values,
        otherwise :py:meth:`pycurl.Curl.setopt` must be called with whatever value
        is the default. For convenience, PycURL provides this unsetopt method
        to reset some of the options to their default values.

        Raises pycurl.error exception on failure.

        ``c.unsetopt(option)`` is equivalent to ``c.setopt(option, None)``.
        """
        ...
    def pause(self, bitmask: int = ...) -> None:
        """
        pause(bitmask=PAUSE_ALL) -> None

        Pause or unpause a curl handle. ``bitmask`` defaults to ``PAUSE_ALL``.
        Pass a value such as ``PAUSE_RECV``, ``PAUSE_SEND``, or ``PAUSE_CONT`` to
        override.

        Corresponds to `curl_easy_pause`_ in libcurl. The argument should be
        derived from the ``PAUSE_RECV``, ``PAUSE_SEND``, ``PAUSE_ALL`` and
        ``PAUSE_CONT`` constants.

        Raises pycurl.error exception upon failure.

        .. _curl_easy_pause: https://curl.haxx.se/libcurl/c/curl_easy_pause.html
        """
        ...
    def unpause(self) -> None:
        """
        unpause() -> None

        Unpause a curl handle.

        Equivalent to ``pause(PAUSE_CONT)``.

        Corresponds to `curl_easy_pause`_ in libcurl.

        Raises pycurl.error exception upon failure.

        .. _curl_easy_pause: https://curl.haxx.se/libcurl/c/curl_easy_pause.html
        """
        ...
    def errstr(self) -> str:
        """
        errstr() -> string

        Return the internal libcurl error buffer of this handle as a string.

        Return value is a ``str`` instance. Error buffer data is decoded using
        Python's default encoding at the time of the call. If this decoding fails,
        ``UnicodeDecodeError`` is raised. Use :ref:`errstr_raw <errstr_raw>` to
        retrieve the error buffer as a byte string in this case.
        """
        ...
    def duphandle(self) -> Self:
        """
        duphandle() -> Curl

        Clone a curl handle. This function will return a new curl handle,
        a duplicate, using all the options previously set in the input curl handle.
        Both handles can subsequently be used independently.

        The new handle will not inherit any state information, no connections,
        no SSL sessions and no cookies. It also will not inherit any share object
        states or options (it will be made as if SHARE was unset).

        When ``MIMEPOST`` includes parts configured with ``CurlMimePart.data_cb()``,
        libcurl duplicates callback userdata pointers into the duplicated handle.
        Design callback state (especially any ``free`` hook side effects) so that
        multiple handle instances can release it safely.
        See also `curl_mime_data_cb`_ in libcurl.

        Corresponds to `curl_easy_duphandle`_ in libcurl.

        Example usage::

            import pycurl
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, "https://python.org")
            dup = curl.duphandle()
            curl.perform()
            dup.perform()

        .. _curl_easy_duphandle:
            https://curl.se/libcurl/c/curl_easy_duphandle.html

        .. _curl_mime_data_cb:
            https://curl.se/libcurl/c/curl_mime_data_cb.html
        """
        ...
    def errstr_raw(self) -> bytes:
        """
        errstr_raw() -> byte string

        Return the internal libcurl error buffer of this handle as a byte string.

        Return value is a ``bytes`` instance. Unlike :ref:`errstr <errstr>`,
        ``errstr_raw`` allows reading libcurl error buffer when its contents is not
        valid in Python's default encoding.

        *Added in version 7.43.0.2.*
        """
        ...
    def multi(self) -> CurlMulti | None:
        """
        multi() -> CurlMulti | None

        Return the ``CurlMulti`` object this ``Curl`` handle currently belongs to,
        or ``None`` if it is not part of any ``CurlMulti``.
        """
        ...
    def share(self) -> CurlShare | None:
        """
        share() -> CurlShare | None

        Return the ``CurlShare`` object that this ``Curl`` handle is currently
        associated with, or ``None`` if it is not part of any ``CurlShare``.
        """
        ...
    def recv(self, buffersize: int, /) -> bytes:
        """
        recv(buffersize) -> data

        Receive data from a connection established with ``CONNECT_ONLY``.

        Receive up to *buffersize* bytes and return them as a ``bytes`` object.
        A returned empty ``bytes`` object indicates that the peer has closed the
        connection.

        Raises ``ValueError`` if *buffersize* is negative.

        Corresponds to `curl_easy_recv`_ in libcurl.

        Because the underlying socket is used in non-blocking mode internally,
        this method raises ``BlockingIOError`` with ``errno`` set to ``EAGAIN``
        when libcurl returns ``CURLE_AGAIN``.

        Raises pycurl.error exception upon failures other than ``CURLE_AGAIN``.

        .. _curl_easy_recv: https://curl.se/libcurl/c/curl_easy_recv.html
        """
        ...
    def recv_into(self, buffer: WriteableBuffer, nbytes: int = 0) -> int:
        """
        recv_into(buffer[, nbytes]) -> nbytes

        Receive data from a connection established with ``CONNECT_ONLY`` into
        *buffer*.

        *buffer* must be a writable bytes-like object.

        If *nbytes* is ``0`` (the default), receive up to ``len(buffer)`` bytes.
        Otherwise, receive up to *nbytes* bytes. Returns the number of bytes
        received.

        Raises ``ValueError`` if *nbytes* is negative or larger than ``len(buffer)``.

        Corresponds to `curl_easy_recv`_ in libcurl.

        Because the underlying socket is used in non-blocking mode internally,
        this method raises ``BlockingIOError`` with ``errno`` set to ``EAGAIN``
        when libcurl returns ``CURLE_AGAIN``.

        Raises pycurl.error exception upon failures other than ``CURLE_AGAIN``.

        .. _curl_easy_recv: https://curl.se/libcurl/c/curl_easy_recv.html
        """
        ...
    def send(self, data: ReadableBuffer, /) -> int:
        """
        send(bytes) -> count

        Send data over a connection established with ``CONNECT_ONLY``.

        *data* may be any bytes-like object.

        Returns the number of bytes sent. If fewer than ``len(data)`` bytes are sent,
        the remaining data should be sent in a subsequent call.

        Corresponds to `curl_easy_send`_ in libcurl.

        Because the underlying socket is used in non-blocking mode internally,
        this method raises ``BlockingIOError`` with ``errno`` set to ``EAGAIN``
        when libcurl returns ``CURLE_AGAIN``.

        Raises pycurl.error exception upon failures other than ``CURLE_AGAIN``.

        .. _curl_easy_send: https://curl.se/libcurl/c/curl_easy_send.html
        """
        ...
    def ws_send(
        self, data: ReadableBuffer | str, flags: int | None = None, fragsize: int = 0, encoding: str = "utf-8"
    ) -> int:
        """
        ws_send(data, flags=None, fragsize=0, encoding='utf-8') -> count

        Send a WebSocket frame. In detached mode this requires ``CONNECT_ONLY=2``;
        inside an active ``WRITEFUNCTION`` callback it may also be used to send
        a blocking reply.

        *data* may be a ``str`` or any bytes-like object. ``str`` is encoded
        with *encoding* (UTF-8 by default); characters that are not
        representable in *encoding* raise ``UnicodeEncodeError``. Passing
        ``None`` raises ``TypeError`` — use ``b""`` for an empty payload.

        *flags* is a bitmask built from the frame-type constants ``WS_TEXT``,
        ``WS_BINARY``, ``WS_CONT``, ``WS_CLOSE``, ``WS_PING``, ``WS_PONG``. When
        ``flags`` is omitted (``None``), the frame type is inferred: ``str`` ->
        ``WS_TEXT``, bytes-like -> ``WS_BINARY``. Explicit flags win. ``str`` +
        ``WS_BINARY`` and ``str`` + ``WS_CLOSE`` raise ``TypeError`` (use
        :py:meth:`ws_close` for close frames, or pass bytes-like data).

        *fragsize* maps to ``curl_ws_send``'s ``fragsize`` parameter; ``0``
        means "whole message". ``WS_OFFSET`` is the companion flag for
        multi-call fragmented sends; see the libcurl docs for the rules.

        Returns the number of bytes accepted by libcurl.

        Raises ``BlockingIOError`` (``errno=EAGAIN``) in detached mode when
        libcurl returns ``CURLE_AGAIN``. Inside a ``WRITEFUNCTION`` callback
        libcurl treats the call as blocking and returns only once the frame has
        been fully sent; ``BlockingIOError`` does not apply. Calls from other
        threads while ``perform()`` is running are rejected.

        Corresponds to `curl_ws_send`_ in libcurl. Requires libcurl 7.86.0 or
        later. Raises ``pycurl.error`` for libcurl failures other than
        ``CURLE_AGAIN``.

        .. _curl_ws_send: https://curl.se/libcurl/c/curl_ws_send.html
        """
        ...
    def ws_recv(self, buffersize: int, /) -> tuple[bytes, WsFrame]:
        """
        ws_recv(buffersize) -> (data, meta)

        Receive a WebSocket frame chunk on a connection established with
        ``CONNECT_ONLY=2``.

        Receive up to *buffersize* bytes. Returns a 2-tuple ``(data, meta)``
        where *data* is a ``bytes`` object containing the received payload chunk
        and *meta* is a ``WsFrame`` namedtuple carrying the per-frame metadata
        returned by libcurl for this call (``age``, ``flags``, ``offset``,
        ``bytesleft``, ``len``).

        A single call may return only part of a frame's payload: check
        ``meta.bytesleft`` to decide whether to loop. Reassembly of fragmented
        messages is the caller's responsibility.

        A *buffersize* of ``0`` performs a zero-length ``curl_ws_recv`` call.
        This returns ``(b"", meta)`` so callers can inspect frame metadata
        without consuming payload bytes. Frames with empty payload are consumed
        by this action.

        Raises ``ValueError`` if *buffersize* is negative.

        Corresponds to `curl_ws_recv`_ in libcurl. Requires libcurl 7.86.0 or
        later.

        Because the underlying socket is used in non-blocking mode internally,
        this method raises ``BlockingIOError`` with ``errno`` set to ``EAGAIN``
        when libcurl returns ``CURLE_AGAIN``.

        Raises pycurl.error exception upon failures other than ``CURLE_AGAIN``.

        .. _curl_ws_recv: https://curl.se/libcurl/c/curl_ws_recv.html
        """
        ...
    def ws_recv_into(self, buffer: WriteableBuffer, nbytes: int = 0) -> tuple[int, WsFrame]:
        """
        ws_recv_into(buffer[, nbytes]) -> (nbytes, meta)

        Receive a WebSocket frame chunk on a connection established with
        ``CONNECT_ONLY=2`` into a caller-owned writable *buffer*.

        *buffer* must be a writable bytes-like object (e.g. ``bytearray``,
        ``memoryview``, ``array.array``).

        If *nbytes* is ``0`` (the default), receive up to ``len(buffer)`` bytes.
        Otherwise, receive up to *nbytes* bytes.

        Returns a 2-tuple ``(nbytes, meta)`` where *nbytes* is the number of
        bytes written into *buffer* and *meta* is a ``WsFrame`` namedtuple with
        the per-frame metadata returned by libcurl for this call.

        Raises ``ValueError`` if *nbytes* is negative or larger than
        ``len(buffer)``.

        If *buffer* has length ``0``, this performs a zero-length
        ``curl_ws_recv`` call and returns ``(0, meta)`` so callers can inspect
        frame metadata without consuming payload bytes. Frames with empty
        payload are consumed by this action.

        Corresponds to `curl_ws_recv`_ in libcurl. Requires libcurl 7.86.0 or
        later.

        Because the underlying socket is used in non-blocking mode internally,
        this method raises ``BlockingIOError`` with ``errno`` set to ``EAGAIN``
        when libcurl returns ``CURLE_AGAIN``.

        Raises pycurl.error exception upon failures other than ``CURLE_AGAIN``.

        .. _curl_ws_recv: https://curl.se/libcurl/c/curl_ws_recv.html
        """
        ...
    def ws_meta(self) -> WsFrame | None:
        """
        ws_meta() -> WsFrame or None

        Return a snapshot of the current WebSocket frame's metadata.

        This is a callback-context helper. It is intended to be called from
        inside an active ``WRITEFUNCTION`` callback on a WebSocket transfer,
        where it returns a ``WsFrame`` namedtuple with the metadata of the
        chunk currently being delivered.

        Outside that context — including when used in detached mode
        (``CONNECT_ONLY=2``), after ``perform()`` has returned, or on a
        non-WebSocket transfer — libcurl's ``curl_ws_meta()`` returns ``NULL``
        and PycURL maps that ``NULL`` to Python ``None``. No exception is
        raised; callers can use ``if c.ws_meta() is None`` to probe context
        validity.

        In detached mode, prefer the metadata returned directly by
        ``ws_recv()`` / ``ws_recv_into()`` rather than a separate ``ws_meta()``
        call.

        Corresponds to `curl_ws_meta`_ in libcurl. Requires libcurl 7.86.0 or
        later.

        .. _curl_ws_meta: https://curl.se/libcurl/c/curl_ws_meta.html
        """
        ...
    def ws_close(self, code: int | None = None, reason: ReadableBuffer | str | None = None, encoding: str = "utf-8") -> int:
        """
        ws_close(code=None, reason=None, encoding='utf-8') -> count

        Send a WebSocket close frame. In detached mode this requires
        ``CONNECT_ONLY=2``; inside an active ``WRITEFUNCTION`` callback it may
        also be used to send a blocking reply.

        Builds an RFC 6455 §5.5.1 close payload — an optional 2-byte big-endian
        status *code* followed by an optional UTF-8 *reason* — and sends it as
        a ``WS_CLOSE`` control frame. Prefer this over
        ``ws_send(bytes, WS_CLOSE)``: the payload format is non-obvious.

        *code* is the WebSocket close status code. Omitted (``None``) sends an
        empty close payload. When specified, must be a valid wire code per RFC
        6455 §7.4.1: ``1000`` (normal), ``1001`` (going away), ``1002``, ``1003``,
        ``1007``-``1014``, or a private-use value in ``3000..4999``. Codes
        ``1004``, ``1005``, ``1006``, ``1015`` are RFC-forbidden to send and
        rejected.

        *reason* may be a ``str`` or any bytes-like object. ``str`` is encoded
        with *encoding* (UTF-8 by default). The resulting bytes must be valid
        UTF-8 on the wire; invalid UTF-8 raises ``UnicodeDecodeError``,
        non-encodable input raises ``UnicodeEncodeError``. ``reason`` without
        ``code`` raises ``ValueError``. The combined payload (2-byte code +
        reason) must not exceed 125 bytes (RFC 6455 §5.5).

        Returns the number of bytes accepted by libcurl.

        Same blocking / non-blocking semantics as :py:meth:`ws_send`. Calls
        from other threads while ``perform()`` is running are rejected.

        Corresponds to `curl_ws_send`_ with ``CURLWS_CLOSE``. Requires libcurl
        7.86.0 or later. Raises ``pycurl.error`` for libcurl failures other
        than ``CURLE_AGAIN``.

        .. _curl_ws_send: https://curl.se/libcurl/c/curl_ws_send.html
        """
        ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None, /
    ) -> None: ...
    if sys.platform == "linux" or sys.platform == "darwin":
        def set_ca_certs(self, value: str | bytes, /) -> None: ...

@disjoint_base
class CurlMulti:
    def close(self) -> None: ...
    def closed(self) -> bool: ...
    def add_handle(self, obj: Curl) -> None: ...
    def remove_handle(self, obj: Curl) -> None: ...
    def setopt(
        self,
        option: int,
        value: (
            bool
            | int
            | list[str | bytes]
            | tuple[str | bytes, ...]
            | Callable[[int], Literal[-1, 0] | None]
            | Callable[[int, int, Self, Any | None], Literal[-1, 0] | None]  # See `assign()` below for `Any | None`
            | None
        ),
    ) -> None: ...
    def perform(self) -> tuple[int, int]: ...
    def fdset(self) -> tuple[list[int], list[int], list[int]]: ...
    def select(self, timeout: float) -> int: ...
    def info_read(self, max_objects: int = ...) -> tuple[int, list[Curl], list[tuple[Curl, int, str]]]: ...
    def socket_action(self, sockfd: int, ev_bitmask: int) -> tuple[int, int]: ...
    # `assign()` accepts literally any object, it's only passed to callbacks and not processed; `None` used to unassign
    def assign(self, sockfd: int, obj: Any | None, /) -> None: ...
    def unassign(self, sock_fd: int, /) -> None: ...
    def socket_all(self) -> tuple[int, int]: ...
    def timeout(self) -> int: ...
    def __contains__(self, key: Curl, /) -> bool: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None, /
    ) -> None: ...

@disjoint_base
class CurlShare:
    def close(self) -> None: ...
    def closed(self) -> bool: ...
    # Currently this `setopt()` is very limited; `None` to unset is also not accepted:
    # http://pycurl.io/docs/latest/curlshareobject.html#pycurl.CurlShare.setopt
    def setopt(self, option: int, value: int) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None, /
    ) -> None: ...

@disjoint_base
class CurlMime:
    """Python wrapper for libcurl MIME API."""
    def __new__(cls, curl: Curl) -> Self: ...
    def add(
        self,
        name: str | bytes | None = None,
        data: ReadableBuffer | str | None = None,
        file: str | bytes | None = None,
        filename: str | bytes | None = None,
        content_type: str | bytes | None = None,
        headers: list[str | bytes] | tuple[str | bytes, ...] | None = None,
        encoder: str | bytes | None = None,
    ) -> CurlMimePart:
        """Add a part using a keyword-oriented builder API."""
        ...
    def add_field(
        self,
        name: str | bytes,
        value: str | bytes,
        content_type: str | bytes | None = None,
        encoder: str | bytes | None = None,
        headers: list[str | bytes] | tuple[str | bytes, ...] | None = None,
    ) -> CurlMimePart:
        """Add a simple form field part."""
        ...
    def add_file(
        self,
        name: str | bytes,
        path: str | bytes,
        filename: str | bytes | None = None,
        content_type: str | bytes | None = None,
        headers: list[str | bytes] | tuple[str | bytes, ...] | None = None,
        encoder: str | bytes | None = None,
    ) -> CurlMimePart:
        """Add a file upload part."""
        ...
    def add_multipart(self, name: str | bytes | None = None, subtype: str | bytes | None = None) -> CurlMime:
        """Add and attach a nested multipart CurlMime."""
        ...
    def addpart(self) -> CurlMimePart:
        """Create and return a new MIME part."""
        ...
    def close(self) -> None:
        """Release the underlying curl_mime handle."""
        ...
    def closed(self) -> bool:
        """Return whether this CurlMime object is closed."""
        ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None, /
    ) -> None: ...

@disjoint_base
class CurlMimePart:
    """A MIME part belonging to a CurlMime object."""
    def name(self, name: str | bytes, /) -> None:
        """Set the name of this MIME part."""
        ...
    def data(self, data: ReadableBuffer | str, /) -> None:
        """Set in-memory data for this MIME part."""
        ...
    def data_cb(
        self,
        datasize: int | None,
        read: Callable[[Any, int], ReadableBuffer | str | int],
        seek: Callable[[Any, int, int], int | None] | None = None,
        free: Callable[[Any], object] | None = None,
        userdata: Any = None,
    ) -> None:
        """Set callback-based data for this MIME part."""
        ...
    def filedata(self, path: str | bytes, /) -> None:
        """Set on-disk file data for this MIME part."""
        ...
    def filename(self, name: str | bytes, /) -> None:
        """Set the remote filename for this MIME part."""
        ...
    def type(self, content_type: str | bytes, /) -> None:
        """Set content type for this MIME part."""
        ...
    def encoder(self, name: str | bytes, /) -> None:
        """Set content transfer encoding for this MIME part."""
        ...
    def headers(self, headers: list[str | bytes] | tuple[str | bytes, ...] | None, /) -> None:
        """Set custom headers for this MIME part."""
        ...
    def subparts(self, mime: CurlMime, /) -> None:
        """Attach a child CurlMime object as multipart data."""
        ...

APPCONNECT_TIME_T: Final[int] = ...
CONNECT_TIME_T: Final[int] = ...
CONTENT_LENGTH_DOWNLOAD_T: Final[int] = ...
CONTENT_LENGTH_UPLOAD_T: Final[int] = ...
EARLYDATA_SENT_T: Final[int] = ...
FILETIME_T: Final[int] = ...
NAMELOOKUP_TIME_T: Final[int] = ...
POSTTRANSFER_TIME_T: Final[int] = ...
PRETRANSFER_TIME_T: Final[int] = ...
QUEUE_TIME_T: Final[int] = ...
REDIRECT_TIME_T: Final[int] = ...
SIZE_DOWNLOAD_T: Final[int] = ...
SIZE_UPLOAD_T: Final[int] = ...
SPEED_DOWNLOAD_T: Final[int] = ...
SPEED_UPLOAD_T: Final[int] = ...
STARTTRANSFER_TIME_T: Final[int] = ...
TOTAL_TIME_T: Final[int] = ...

ACCEPTTIMEOUT_MS: Final = 212
ACCEPT_ENCODING: Final = 10102
ACTIVESOCKET: Final[int]
ADDRESS_SCOPE: Final = 171
APPCONNECT_TIME: Final = 3145761
APPEND: Final = 50
AUTOREFERER: Final = 58
AWS_SIGV4: Final = 10305
BUFFERSIZE: Final = 98
CAINFO: Final = 10065
CAINFO_BLOB: Final = 40309
CAPATH: Final = 10097
CLOSESOCKETFUNCTION: Final = 20208
COMPILE_LIBCURL_VERSION_NUM: Final[int]
COMPILE_PY_VERSION_HEX: Final[int]
COMPILE_SSL_LIB: Final[str]
CONDITION_UNMET: Final = 2097187
CONNECTTIMEOUT: Final = 78
CONNECTTIMEOUT_MS: Final = 156
CONNECT_ONLY: Final = 141
CONNECT_TIME: Final = 3145733
CONNECT_TO: Final = 10243
CONTENT_LENGTH_DOWNLOAD: Final = 3145743
CONTENT_LENGTH_UPLOAD: Final = 3145744
CONTENT_TYPE: Final = 1048594
COOKIE: Final = 10022
COOKIEFILE: Final = 10031
COOKIEJAR: Final = 10082
COOKIELIST: Final = 10135
COOKIESESSION: Final = 96
COPYPOSTFIELDS: Final = 10165
CRLF: Final = 27
CRLFILE: Final = 10169
CSELECT_ERR: Final = 4
CSELECT_IN: Final = 1
CSELECT_OUT: Final = 2
CURLHSTS_ENABLE: Final[int]
CURLHSTS_READONLYFILE: Final[int]
CURLSTS_DONE: Final[int]
CURLSTS_FAIL: Final[int]
CURLSTS_OK: Final[int]
CURL_HTTP_VERSION_1_0: Final = 1
CURL_HTTP_VERSION_1_1: Final = 2
CURL_HTTP_VERSION_2: Final = 3
CURL_HTTP_VERSION_2TLS: Final = 4
CURL_HTTP_VERSION_2_0: Final = 3
CURL_HTTP_VERSION_2_PRIOR_KNOWLEDGE: Final = 5
CURL_HTTP_VERSION_3: Final = 30
CURL_HTTP_VERSION_3ONLY: Final = 31
CURL_HTTP_VERSION_LAST: Final = 32
CURL_HTTP_VERSION_NONE: Final = 0
CURL_VERSION_ALTSVC: Final = 16777216
CURL_VERSION_BROTLI: Final = 8388608
CURL_VERSION_GSASL: Final = 536870912
CURL_VERSION_HSTS: Final = 268435456
CURL_VERSION_HTTP3: Final = 33554432
CURL_VERSION_HTTPS_PROXY: Final = 2097152
CURL_VERSION_MULTI_SSL: Final = 4194304
CURL_VERSION_UNICODE: Final = 134217728
CURL_VERSION_ZSTD: Final = 67108864
CUSTOMREQUEST: Final = 10036
DEBUGFUNCTION: Final = 20094
DEFAULT_PROTOCOL: Final = 10238
DIRLISTONLY: Final = 48
DNS_CACHE_TIMEOUT: Final = 92
DNS_SERVERS: Final = 10211
DNS_USE_GLOBAL_CACHE: Final = 91
DOH_URL: Final = 10279
EFFECTIVE_URL: Final = 1048577
EFFECTIVE_METHOD: Final = 1048634
EGDSOCKET: Final = 10077
ENCODING: Final = 10102
EXPECT_100_TIMEOUT_MS: Final = 227
E_ABORTED_BY_CALLBACK: Final = 42
E_AGAIN: Final = 81
E_ALREADY_COMPLETE: Final = 99999
E_BAD_CALLING_ORDER: Final = 44
E_BAD_CONTENT_ENCODING: Final = 61
E_BAD_DOWNLOAD_RESUME: Final = 36
E_BAD_FUNCTION_ARGUMENT: Final = 43
E_BAD_PASSWORD_ENTERED: Final = 46
E_CALL_MULTI_PERFORM: Final = -1
E_CHUNK_FAILED: Final = 88
E_CONV_FAILED: Final = 75
E_CONV_REQD: Final = 76
E_COULDNT_CONNECT: Final = 7
E_COULDNT_RESOLVE_HOST: Final = 6
E_COULDNT_RESOLVE_PROXY: Final = 5
E_FAILED_INIT: Final = 2
E_FILESIZE_EXCEEDED: Final = 63
E_FILE_COULDNT_READ_FILE: Final = 37
E_FTP_ACCEPT_FAILED: Final = 10
E_FTP_ACCEPT_TIMEOUT: Final = 12
E_FTP_ACCESS_DENIED: Final = 9
E_FTP_BAD_DOWNLOAD_RESUME: Final = 36
E_FTP_BAD_FILE_LIST: Final = 87
E_FTP_CANT_GET_HOST: Final = 15
E_FTP_CANT_RECONNECT: Final = 16
E_FTP_COULDNT_GET_SIZE: Final = 32
E_FTP_COULDNT_RETR_FILE: Final = 19
E_FTP_COULDNT_SET_ASCII: Final = 29
E_FTP_COULDNT_SET_BINARY: Final = 17
E_FTP_COULDNT_SET_TYPE: Final = 17
E_FTP_COULDNT_STOR_FILE: Final = 25
E_FTP_COULDNT_USE_REST: Final = 31
E_FTP_PARTIAL_FILE: Final = 18
E_FTP_PORT_FAILED: Final = 30
E_FTP_PRET_FAILED: Final = 84
E_FTP_QUOTE_ERROR: Final = 21
E_FTP_SSL_FAILED: Final = 64
E_FTP_USER_PASSWORD_INCORRECT: Final = 10
E_FTP_WEIRD_227_FORMAT: Final = 14
E_FTP_WEIRD_PASS_REPLY: Final = 11
E_FTP_WEIRD_PASV_REPLY: Final = 13
E_FTP_WEIRD_SERVER_REPLY: Final = 8
E_FTP_WEIRD_USER_REPLY: Final = 12
E_FTP_WRITE_ERROR: Final = 20
E_FUNCTION_NOT_FOUND: Final = 41
E_GOT_NOTHING: Final = 52
E_HTTP2: Final = 16
E_HTTP_NOT_FOUND: Final = 22
E_HTTP_PORT_FAILED: Final = 45
E_HTTP_POST_ERROR: Final = 34
E_HTTP_RANGE_ERROR: Final = 33
E_HTTP_RETURNED_ERROR: Final = 22
E_INTERFACE_FAILED: Final = 45
E_LDAP_CANNOT_BIND: Final = 38
E_LDAP_INVALID_URL: Final = 62
E_LDAP_SEARCH_FAILED: Final = 39
E_LIBRARY_NOT_FOUND: Final = 40
E_LOGIN_DENIED: Final = 67
E_MALFORMAT_USER: Final = 24
E_MULTI_ADDED_ALREADY: Final = 7
E_MULTI_BAD_EASY_HANDLE: Final = 2
E_MULTI_BAD_HANDLE: Final = 1
E_MULTI_BAD_SOCKET: Final = 5
E_MULTI_CALL_MULTI_PERFORM: Final = -1
E_MULTI_CALL_MULTI_SOCKET: Final = -1
E_MULTI_INTERNAL_ERROR: Final = 4
E_MULTI_OK: Final = 0
E_MULTI_OUT_OF_MEMORY: Final = 3
E_MULTI_UNKNOWN_OPTION: Final = 6
E_NOT_BUILT_IN: Final = 4
E_NO_CONNECTION_AVAILABLE: Final = 89
E_OK: Final = 0
E_OPERATION_TIMEDOUT: Final = 28
E_OPERATION_TIMEOUTED: Final = 28
E_OUT_OF_MEMORY: Final = 27
E_PARTIAL_FILE: Final = 18
E_PEER_FAILED_VERIFICATION: Final = 60
E_QUOTE_ERROR: Final = 21
E_RANGE_ERROR: Final = 33
E_READ_ERROR: Final = 26
E_RECV_ERROR: Final = 56
E_REMOTE_ACCESS_DENIED: Final = 9
E_REMOTE_DISK_FULL: Final = 70
E_REMOTE_FILE_EXISTS: Final = 73
E_REMOTE_FILE_NOT_FOUND: Final = 78
E_RTSP_CSEQ_ERROR: Final = 85
E_RTSP_SESSION_ERROR: Final = 86
E_SEND_ERROR: Final = 55
E_SEND_FAIL_REWIND: Final = 65
E_SHARE_IN_USE: Final = 57
E_SSH: Final = 79
E_SSL_CACERT: Final = 60
E_SSL_CACERT_BADFILE: Final = 77
E_SSL_CERTPROBLEM: Final = 58
E_SSL_CIPHER: Final = 59
E_SSL_CONNECT_ERROR: Final = 35
E_SSL_CRL_BADFILE: Final = 82
E_SSL_ENGINE_INITFAILED: Final = 66
E_SSL_ENGINE_NOTFOUND: Final = 53
E_SSL_ENGINE_SETFAILED: Final = 54
E_SSL_INVALIDCERTSTATUS: Final = 91
E_SSL_ISSUER_ERROR: Final = 83
E_SSL_PEER_CERTIFICATE: Final = 60
E_SSL_PINNEDPUBKEYNOTMATCH: Final = 90
E_SSL_SHUTDOWN_FAILED: Final = 80
E_TELNET_OPTION_SYNTAX: Final = 49
E_TFTP_DISKFULL: Final = 70
E_TFTP_EXISTS: Final = 73
E_TFTP_ILLEGAL: Final = 71
E_TFTP_NOSUCHUSER: Final = 74
E_TFTP_NOTFOUND: Final = 68
E_TFTP_PERM: Final = 69
E_TFTP_UNKNOWNID: Final = 72
E_TOO_MANY_REDIRECTS: Final = 47
E_UNKNOWN_OPTION: Final = 48
E_UNKNOWN_TELNET_OPTION: Final = 48
E_UNSUPPORTED_PROTOCOL: Final = 1
E_UPLOAD_FAILED: Final = 25
E_URL_MALFORMAT: Final = 3
E_URL_MALFORMAT_USER: Final = 4
E_USE_SSL_FAILED: Final = 64
E_WRITE_ERROR: Final = 23
FAILONERROR: Final = 45
FILE: Final = 10001
FNMATCHFUNC_FAIL: Final[int]
FNMATCHFUNC_MATCH: Final[int]
FNMATCHFUNC_NOMATCH: Final[int]
FNMATCH_DATA: Final[int]
FNMATCH_FUNCTION: Final[int]
FOLLOWLOCATION: Final = 52
FORBID_REUSE: Final = 75
FORM_BUFFER: Final = 11
FORM_BUFFERPTR: Final = 12
FORM_CONTENTS: Final = 4
FORM_CONTENTTYPE: Final = 14
FORM_FILE: Final = 10
FORM_FILENAME: Final = 16
FRESH_CONNECT: Final = 74
FTPAPPEND: Final = 50
FTPAUTH_DEFAULT: Final = 0
FTPAUTH_SSL: Final = 1
FTPAUTH_TLS: Final = 2
FTPLISTONLY: Final = 48
FTPMETHOD_DEFAULT: Final = 0
FTPMETHOD_MULTICWD: Final = 1
FTPMETHOD_NOCWD: Final = 2
FTPMETHOD_SINGLECWD: Final = 3
FTPPORT: Final = 10017
FTPSSLAUTH: Final = 129
FTPSSL_ALL: Final = 3
FTPSSL_CONTROL: Final = 2
FTPSSL_NONE: Final = 0
FTPSSL_TRY: Final = 1
FTP_ACCOUNT: Final = 10134
FTP_ALTERNATIVE_TO_USER: Final = 10147
FTP_CREATE_MISSING_DIRS: Final = 110
FTP_ENTRY_PATH: Final = 1048606
FTP_FILEMETHOD: Final = 138
FTP_RESPONSE_TIMEOUT: Final = 112
FTP_SKIP_PASV_IP: Final = 137
FTP_SSL: Final = 119
FTP_SSL_CCC: Final = 154
FTP_USE_EPRT: Final = 106
FTP_USE_EPSV: Final = 85
FTP_USE_PRET: Final = 188
GLOBAL_ACK_EINTR: Final = 4
GLOBAL_ALL: Final = 3
GLOBAL_DEFAULT: Final = 3
GLOBAL_NOTHING: Final = 0
GLOBAL_SSL: Final = 1
GLOBAL_WIN32: Final = 2
GSSAPI_DELEGATION: Final = 210
GSSAPI_DELEGATION_FLAG: Final = 2
GSSAPI_DELEGATION_NONE: Final = 0
GSSAPI_DELEGATION_POLICY_FLAG: Final = 1
HAPROXYPROTOCOL: Final = 274
HAPROXY_CLIENT_IP: Final = 10323
ECH: Final = 10325
HEADER: Final = 42
HEADERFUNCTION: Final = 20079
HEADEROPT: Final = 229
HEADER_SEPARATE: Final = 1
HEADER_SIZE: Final = 2097163
HEADER_UNIFIED: Final = 0
HSTS: Final[int]
HSTSREADDATA: Final[int]
HSTSREADFUNCTION: Final[int]
HSTSWRITEDATA: Final[int]
HSTSWRITEFUNCTION: Final[int]
HSTS_CTRL: Final[int]
HTTP09_ALLOWED: Final = 285
HTTP200ALIASES: Final = 10104
HTTPAUTH: Final = 107
HTTPAUTH_ANY: Final[int]
HTTPAUTH_ANYSAFE: Final[int]
HTTPAUTH_AVAIL: Final = 2097175
HTTPAUTH_BASIC: Final = 1
HTTPAUTH_DIGEST: Final = 2
HTTPAUTH_DIGEST_IE: Final = 16
HTTPAUTH_GSSNEGOTIATE: Final = 4
HTTPAUTH_NEGOTIATE: Final = 4
HTTPAUTH_NONE: Final = 0
HTTPAUTH_NTLM: Final = 8
HTTPAUTH_NTLM_WB: Final = 32
HTTPAUTH_ONLY: Final[int]
HTTPGET: Final = 80
HTTPHEADER: Final = 10023
HTTPPOST: Final = 10024
HTTPPROXYTUNNEL: Final = 61
HTTP_CODE: Final = 2097154
HTTP_CONNECTCODE: Final = 2097174
HTTP_CONTENT_DECODING: Final = 158
HTTP_TRANSFER_DECODING: Final = 157
HTTP_VERSION: Final = 84
IGNORE_CONTENT_LENGTH: Final = 136
INFILE: Final = 10009
INFILESIZE: Final = 30115
INFILESIZE_LARGE: Final = 30115
INFOTYPE_DATA_IN: Final = 3
INFOTYPE_DATA_OUT: Final = 4
INFOTYPE_HEADER_IN: Final = 1
INFOTYPE_HEADER_OUT: Final = 2
INFOTYPE_SSL_DATA_IN: Final = 5
INFOTYPE_SSL_DATA_OUT: Final = 6
INFOTYPE_TEXT: Final = 0
INFO_CERTINFO: Final = 4194338
INFO_COOKIELIST: Final = 4194332
INFO_FILETIME: Final = 2097166
INFO_HTTP_VERSION: Final = 2097198
INFO_RTSP_CLIENT_CSEQ: Final = 2097189
INFO_RTSP_CSEQ_RECV: Final = 2097191
INFO_RTSP_SERVER_CSEQ: Final = 2097190
INFO_RTSP_SESSION_ID: Final = 1048612
INTERFACE: Final = 10062
IOCMD_NOP: Final = 0
IOCMD_RESTARTREAD: Final = 1
IOCTLFUNCTION: Final = 20130
IOE_FAILRESTART: Final = 2
IOE_OK: Final = 0
IOE_UNKNOWNCMD: Final = 1
IPRESOLVE: Final = 113
IPRESOLVE_V4: Final = 1
IPRESOLVE_V6: Final = 2
IPRESOLVE_WHATEVER: Final = 0
ISSUERCERT: Final = 10170
ISSUERCERT_BLOB: Final = 40295
KEYPASSWD: Final = 10026
KHMATCH_MISMATCH: Final = 1
KHMATCH_MISSING: Final = 2
KHMATCH_OK: Final = 0
KHSTAT_DEFER: Final = 3
KHSTAT_FINE: Final = 1
KHSTAT_FINE_ADD_TO_FILE: Final = 0
KHSTAT_REJECT: Final = 2
KHTYPE_DSS: Final = 3
KHTYPE_RSA: Final = 2
KHTYPE_RSA1: Final = 1
KHTYPE_UNKNOWN: Final = 0
KRB4LEVEL: Final = 10063
KRBLEVEL: Final = 10063
LASTSOCKET: Final = 2097181
LOCALPORT: Final = 139
LOCALPORTRANGE: Final = 140
LOCAL_IP: Final = 1048617
LOCAL_PORT: Final = 2097194
LOCK_DATA_CONNECT: Final = 5
LOCK_DATA_COOKIE: Final = 2
LOCK_DATA_DNS: Final = 3
LOCK_DATA_PSL: Final = 6
LOCK_DATA_SSL_SESSION: Final = 4
LOGIN_OPTIONS: Final = 10224
LOW_SPEED_LIMIT: Final = 19
LOW_SPEED_TIME: Final = 20
MAIL_AUTH: Final = 10217
MAIL_FROM: Final = 10186
MAIL_RCPT: Final = 10187
MAXAGE_CONN: Final = 288
MAXCONNECTS: Final = 71
MAXFILESIZE: Final = 30117
MAXFILESIZE_LARGE: Final = 30117
MAXLIFETIME_CONN: Final = 314
PREREQFUNCTION: Final = 20312
PREREQFUNC_OK: Final = 0
PREREQFUNC_ABORT: Final = 1
MAXREDIRS: Final = 68
MAX_RECV_SPEED_LARGE: Final = 30146
MAX_SEND_SPEED_LARGE: Final = 30145
MIMEPOST: Final[int]
M_CHUNK_LENGTH_PENALTY_SIZE: Final = 30010
M_CONTENT_LENGTH_PENALTY_SIZE: Final = 30009
M_MAXCONNECTS: Final = 6
M_MAX_CONCURRENT_STREAMS: Final = 16
M_MAX_HOST_CONNECTIONS: Final = 7
M_MAX_PIPELINE_LENGTH: Final = 8
M_MAX_TOTAL_CONNECTIONS: Final = 13
M_PIPELINING: Final = 3
M_PIPELINING_SERVER_BL: Final = 10012
M_PIPELINING_SITE_BL: Final = 10011
M_SOCKETFUNCTION: Final = 20001
M_TIMERFUNCTION: Final = 20004
NAMELOOKUP_TIME: Final = 3145732
NETRC: Final = 51
NETRC_FILE: Final = 10118
NETRC_IGNORED: Final = 0
NETRC_OPTIONAL: Final = 1
NETRC_REQUIRED: Final = 2
NEW_DIRECTORY_PERMS: Final = 160
NEW_FILE_PERMS: Final = 159
NOBODY: Final = 44
NOPROGRESS: Final = 43
NOPROXY: Final = 10177
NOSIGNAL: Final = 99
NUM_CONNECTS: Final = 2097178
OPENSOCKETFUNCTION: Final = 20163
OPT_CERTINFO: Final = 172
OPT_COOKIELIST: Final = 10135
OPT_FILETIME: Final = 69
OPT_RTSP_CLIENT_CSEQ: Final = 193
OPT_RTSP_REQUEST: Final = 189
OPT_RTSP_SERVER_CSEQ: Final = 194
OPT_RTSP_SESSION_ID: Final = 10190
OPT_RTSP_STREAM_URI: Final = 10191
OPT_RTSP_TRANSPORT: Final = 10192
OS_ERRNO: Final = 2097177
PASSWORD: Final = 10174
PATH_AS_IS: Final = 234
PAUSE_ALL: Final = 5
PAUSE_CONT: Final = 0
PAUSE_RECV: Final = 1
PAUSE_SEND: Final = 4
PINNEDPUBLICKEY: Final = 10230
PIPEWAIT: Final = 237
PIPE_HTTP1: Final = 1
PIPE_MULTIPLEX: Final = 2
PIPE_NOTHING: Final = 0
POLL_IN: Final = 1
POLL_INOUT: Final = 3
POLL_NONE: Final = 0
POLL_OUT: Final = 2
POLL_REMOVE: Final = 4
PORT: Final = 3
POST: Final = 47
POST301: Final = 161
POSTFIELDS: Final = 10015
POSTFIELDSIZE: Final = 30120
POSTFIELDSIZE_LARGE: Final = 30120
POSTQUOTE: Final = 10039
POSTREDIR: Final = 161
PREQUOTE: Final = 10093
PRETRANSFER_TIME: Final = 3145734
PRE_PROXY: Final = 10262
PRIMARY_IP: Final = 1048608
PRIMARY_PORT: Final = 2097192
PROGRESSFUNCTION: Final = 20056
PROTOCOLS: Final = 181
PROTO_ALL: Final[int]
PROTO_DICT: Final = 512
PROTO_FILE: Final = 1024
PROTO_FTP: Final = 4
PROTO_FTPS: Final = 8
PROTO_GOPHER: Final = 33554432
PROTO_HTTP: Final = 1
PROTO_HTTPS: Final = 2
PROTO_IMAP: Final = 4096
PROTO_IMAPS: Final = 8192
PROTO_LDAP: Final = 128
PROTO_LDAPS: Final = 256
PROTO_POP3: Final = 16384
PROTO_POP3S: Final = 32768
PROTO_RTMP: Final = 524288
PROTO_RTMPE: Final = 2097152
PROTO_RTMPS: Final = 8388608
PROTO_RTMPT: Final = 1048576
PROTO_RTMPTE: Final = 4194304
PROTO_RTMPTS: Final = 16777216
PROTO_RTSP: Final = 262144
PROTO_SCP: Final = 16
PROTO_SFTP: Final = 32
PROTO_SMB: Final = 67108864
PROTO_SMBS: Final = 134217728
PROTO_SMTP: Final = 65536
PROTO_SMTPS: Final = 131072
PROTO_TELNET: Final = 64
PROTO_TFTP: Final = 2048
PROXY: Final = 10004
PROXYAUTH: Final = 111
PROXYAUTH_AVAIL: Final = 2097176
PROXYHEADER: Final = 10228
PROXYPASSWORD: Final = 10176
PROXYPORT: Final = 59
PROXYTYPE: Final = 101
PROXYTYPE_HTTP: Final = 0
PROXYTYPE_HTTP_1_0: Final = 1
PROXYTYPE_SOCKS4: Final = 4
PROXYTYPE_SOCKS4A: Final = 6
PROXYTYPE_SOCKS5: Final = 5
PROXYTYPE_SOCKS5_HOSTNAME: Final = 7
PROXYUSERNAME: Final = 10175
PROXYUSERPWD: Final = 10006
PROXY_CAINFO: Final = 10246
PROXY_CAINFO_BLOB: Final = 40310
PROXY_CAPATH: Final = 10247
PROXY_CRLFILE: Final = 10260
PROXY_ISSUERCERT: Final = 10296
PROXY_ISSUERCERT_BLOB: Final = 40297
PROXY_KEYPASSWD: Final = 10258
PROXY_PINNEDPUBLICKEY: Final = 10263
PROXY_SERVICE_NAME: Final = 10235
PROXY_SSLCERT: Final = 10254
PROXY_SSLCERTTYPE: Final = 10255
PROXY_SSLCERT_BLOB: Final = 40293
PROXY_SSLKEY: Final = 10256
PROXY_SSLKEYTYPE: Final = 10257
PROXY_SSLKEY_BLOB: Final = 40294
PROXY_SSLVERSION: Final = 250
PROXY_SSL_CIPHER_LIST: Final = 10259
PROXY_SSL_OPTIONS: Final = 261
PROXY_SSL_VERIFYHOST: Final = 249
PROXY_SSL_VERIFYPEER: Final = 248
PROXY_TLS13_CIPHERS: Final = 10277
PROXY_TLSAUTH_PASSWORD: Final = 10252
PROXY_TLSAUTH_TYPE: Final = 10253
PROXY_TLSAUTH_USERNAME: Final = 10251
PROXY_TRANSFER_MODE: Final = 166
PUT: Final = 54
QUOTE: Final = 10028
RANDOM_FILE: Final = 10076
RANGE: Final = 10007
READDATA: Final = 10009
READFUNCTION: Final = 20012
READFUNC_ABORT: Final = 268435456
READFUNC_PAUSE: Final = 268435457
REDIRECT_COUNT: Final = 2097172
REDIRECT_TIME: Final = 3145747
REDIRECT_URL: Final = 1048607
REDIR_POST_301: Final = 1
REDIR_POST_302: Final = 2
REDIR_POST_303: Final = 4
REDIR_POST_ALL: Final = 7
REDIR_PROTOCOLS: Final = 182
REFERER: Final = 10016
REQUEST_SIZE: Final = 2097164
REQUEST_TARGET: Final = 10266
RESOLVE: Final = 10203
RESOLVER_START_DATA: Final[int]
RESOLVER_START_FUNCTION: Final[int]
RESPONSE_CODE: Final = 2097154
RESUME_FROM: Final = 30116
RESUME_FROM_LARGE: Final = 30116
RTSPREQ_ANNOUNCE: Final = 3
RTSPREQ_DESCRIBE: Final = 2
RTSPREQ_GET_PARAMETER: Final = 8
RTSPREQ_LAST: Final = 12
RTSPREQ_NONE: Final = 0
RTSPREQ_OPTIONS: Final = 1
RTSPREQ_PAUSE: Final = 6
RTSPREQ_PLAY: Final = 5
RTSPREQ_RECEIVE: Final = 11
RTSPREQ_RECORD: Final = 10
RTSPREQ_SETUP: Final = 4
RTSPREQ_SET_PARAMETER: Final = 9
RTSPREQ_TEARDOWN: Final = 7
SASL_IR: Final = 218
SEEKFUNCTION: Final = 20167
SEEKFUNC_CANTSEEK: Final = 2
SEEKFUNC_FAIL: Final = 1
SEEKFUNC_OK: Final = 0
SERVICE_NAME: Final = 10236
SHARE: Final = 10100
SH_SHARE: Final = 1
SH_UNSHARE: Final = 2
SIZE_DOWNLOAD: Final = 3145736
SIZE_UPLOAD: Final = 3145735
SOCKET_BAD: Final = -1
SOCKET_TIMEOUT: Final = -1
SOCKOPTFUNCTION: Final = 20148
SOCKOPT_ALREADY_CONNECTED: Final = 2
SOCKOPT_ERROR: Final = 1
SOCKOPT_OK: Final = 0
SOCKS5_GSSAPI_NEC: Final = 180
SOCKS5_GSSAPI_SERVICE: Final = 10179
SOCKTYPE_ACCEPT: Final = 1
SOCKTYPE_IPCXN: Final = 0
SPEED_DOWNLOAD: Final = 3145737
SPEED_UPLOAD: Final = 3145738
SSH_AUTH_AGENT: Final = 16
SSH_AUTH_ANY: Final[int]
SSH_AUTH_DEFAULT: Final[int]
SSH_AUTH_HOST: Final = 4
SSH_AUTH_KEYBOARD: Final = 8
SSH_AUTH_NONE: Final = 0
SSH_AUTH_PASSWORD: Final = 2
SSH_AUTH_PUBLICKEY: Final = 1
SSH_AUTH_TYPES: Final = 151
SSH_HOST_PUBLIC_KEY_MD5: Final = 10162
SSH_KEYFUNCTION: Final = 20184
SSH_KNOWNHOSTS: Final = 10183
SSH_PRIVATE_KEYFILE: Final = 10153
SSH_PUBLIC_KEYFILE: Final = 10152
SSLCERT: Final = 10025
SSLCERTPASSWD: Final = 10026
SSLCERTTYPE: Final = 10086
SSLCERT_BLOB: Final = 40291
SSLENGINE: Final = 10089
SSLENGINE_DEFAULT: Final = 90
SSLKEY: Final = 10087
SSLKEYPASSWD: Final = 10026
SSLKEYTYPE: Final = 10088
SSLKEY_BLOB: Final = 40292
SSLOPT_ALLOW_BEAST: Final = 1
SSLOPT_NO_REVOKE: Final = 2
SSLVERSION: Final = 32
SSLVERSION_DEFAULT: Final = 0
SSLVERSION_MAX_DEFAULT: Final = 65536
SSLVERSION_MAX_TLSv1_0: Final = 262144
SSLVERSION_MAX_TLSv1_1: Final = 327680
SSLVERSION_MAX_TLSv1_2: Final = 393216
SSLVERSION_MAX_TLSv1_3: Final = 458752
SSLVERSION_SSLv2: Final = 2
SSLVERSION_SSLv3: Final = 3
SSLVERSION_TLSv1: Final = 1
SSLVERSION_TLSv1_0: Final = 4
SSLVERSION_TLSv1_1: Final = 5
SSLVERSION_TLSv1_2: Final = 6
SSLVERSION_TLSv1_3: Final = 7
SSL_CIPHER_LIST: Final = 10083
SSL_ENABLE_ALPN: Final = 226
SSL_ENABLE_NPN: Final = 225
SSL_ENGINES: Final = 4194331
SSL_FALSESTART: Final = 233
SSL_OPTIONS: Final = 216
SSL_SESSIONID_CACHE: Final = 150
SSL_VERIFYHOST: Final = 81
SSL_VERIFYPEER: Final = 64
SSL_VERIFYRESULT: Final = 2097165
SSL_VERIFYSTATUS: Final = 232
STARTTRANSFER_TIME: Final = 3145745
STDERR: Final = 10037
TCP_FASTOPEN: Final = 244
TCP_KEEPALIVE: Final = 213
TCP_KEEPIDLE: Final = 214
TCP_KEEPINTVL: Final = 215
TCP_NODELAY: Final = 121
TELNETOPTIONS: Final = 10070
TFTP_BLKSIZE: Final = 178
TIMECONDITION: Final = 33
TIMECONDITION_IFMODSINCE: Final = 1
TIMECONDITION_IFUNMODSINCE: Final = 2
TIMECONDITION_LASTMOD: Final = 3
TIMECONDITION_NONE: Final = 0
TIMEOUT: Final = 13
TIMEOUT_MS: Final = 155
TIMEVALUE: Final = 34
TLS13_CIPHERS: Final = 10276
TLSAUTH_PASSWORD: Final = 10205
TLSAUTH_TYPE: Final = 10206
TLSAUTH_USERNAME: Final = 10204
TOTAL_TIME: Final = 3145731
TRAILERDATA: Final[int]
TRAILERFUNCTION: Final[int]
TRAILERFUNC_ABORT: Final[int]
TRAILERFUNC_OK: Final[int]
TRANSFERTEXT: Final = 53
TRANSFER_ENCODING: Final = 207
UNIX_SOCKET_PATH: Final = 10231
UNRESTRICTED_AUTH: Final = 105
UPLOAD: Final = 46
UPLOAD_BUFFERSIZE: Final = 280
URL: Final = 10002
USERAGENT: Final = 10018
USERNAME: Final = 10173
USERPWD: Final = 10005
USESSL_ALL: Final = 3
USESSL_CONTROL: Final = 2
USESSL_NONE: Final = 0
USESSL_TRY: Final = 1
USE_SSL: Final = 119
VERBOSE: Final = 41
VERSION_ALTSVC: Final = 16777216
VERSION_ASYNCHDNS: Final = 128
VERSION_BROTLI: Final = 8388608
VERSION_CONV: Final = 4096
VERSION_CURLDEBUG: Final = 8192
VERSION_DEBUG: Final = 64
VERSION_GSASL: Final = 536870912
VERSION_GSSAPI: Final = 131072
VERSION_GSSNEGOTIATE: Final = 32
VERSION_HSTS: Final = 268435456
VERSION_HTTP2: Final = 65536
VERSION_HTTP3: Final = 33554432
VERSION_HTTPS_PROXY: Final = 2097152
VERSION_IDN: Final = 1024
VERSION_IPV6: Final = 1
VERSION_KERBEROS4: Final = 2
VERSION_KERBEROS5: Final = 262144
VERSION_LARGEFILE: Final = 512
VERSION_LIBZ: Final = 8
VERSION_MULTI_SSL: Final = 4194304
VERSION_NTLM: Final = 16
VERSION_NTLM_WB: Final = 32768
VERSION_PSL: Final = 1048576
VERSION_SPNEGO: Final = 256
VERSION_SSL: Final = 4
VERSION_SSPI: Final = 2048
VERSION_TLSAUTH_SRP: Final = 16384
VERSION_UNICODE: Final = 134217728
VERSION_UNIX_SOCKETS: Final = 524288
VERSION_ZSTD: Final = 67108864
WILDCARDMATCH: Final = 197
WRITEDATA: Final = 10001
WRITEFUNCTION: Final = 20011
WRITEFUNC_PAUSE: Final = 268435457
WRITEHEADER: Final = 10029
WS_BINARY: Final[int]
WS_CLOSE: Final[int]
WS_CONT: Final[int]
WS_NOAUTOPONG: Final[int]
WS_OFFSET: Final[int]
WS_OPTIONS: Final[int]
WS_PING: Final[int]
WS_PONG: Final[int]
WS_RAW_MODE: Final[int]
WS_TEXT: Final[int]
XFERINFOFUNCTION: Final = 20219
XOAUTH2_BEARER: Final = 10220

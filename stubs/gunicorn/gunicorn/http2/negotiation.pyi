"""
Cleartext HTTP/2 (h2c) negotiation, shared by every worker.

The I/O differs per worker: gthread and gevent read from a socket, the ASGI
worker is handed bytes by asyncio. The decisions do not. Keeping the pure,
I/O-free part here stops the blocking and push-based paths from drifting apart.
"""

import socket
from typing import Final, Literal, Protocol, type_check_only

from gunicorn.config import Config

from .._types import _AddressType

@type_check_only
class _HasHeaders(Protocol):
    headers: list[tuple[str, str]]

H2C_PREFACE: Final = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
H2C_PREFACE_TIMEOUT: Final = 1.0
MATCH: Final = "match"
PARTIAL: Final = "partial"
MISMATCH: Final = "mismatch"

def preface_match(buf: bytes) -> Literal["match", "mismatch", "partial"]:
    """
    Compare buffered bytes against the connection preface.

    Returns ``MATCH`` when the whole preface is present, ``PARTIAL`` when the
    bytes so far are a prefix of it and more could still arrive, and
    ``MISMATCH`` as soon as a byte diverges. Never blocks and never reads.
    """
    ...
def peer_trusted_for_h2c(cfg: Config, peer_addr: _AddressType) -> bool:
    """
    Whether this peer may negotiate cleartext HTTP/2.

    Reuses the ``forwarded_allow_ips`` trust list: h2c is only ever expected
    from the TLS-terminating proxy in front of gunicorn, which is the same
    peer already trusted to set forwarded headers. Unix socket peers are
    trusted, matching that policy.
    """
    ...
def prior_knowledge_allowed(cfg: Config, peer_addr: _AddressType) -> bool:
    """
    Whether to sniff for the connection preface from this peer.

    Deliberately separate from :func:`upgrade_allowed`: enabling one mechanism
    must not quietly enable the other.
    """
    ...
def mismatch_is_error(cfg: Config) -> bool:
    """
    Whether a trusted peer failing to send the preface is a 400.

    Only when prior knowledge is the sole mechanism: such a peer is expected
    to speak HTTP/2 and a silent downgrade would hide a misconfiguration.
    When upgrade is also enabled, an HTTP/1 request is not a mistake, it is
    how an upgrade begins, so it has to be allowed through.
    """
    ...
def upgrade_allowed(cfg: Config, peer_addr: _AddressType) -> bool:
    """Whether to honour an ``Upgrade: h2c`` request from this peer."""
    ...
def read_preface_blocking(sock: socket.socket, timeout: float | None = None) -> tuple[bool, bytes]:
    """
    Read up to the length of the preface from a blocking socket.

    Returns ``(matched, consumed_bytes)``. The caller owns the consumed bytes
    and must hand them to whichever protocol wins, since they have already
    left the socket.

    The timeout is an absolute budget for the whole preface, checked before
    every read. ``socket.settimeout()`` alone would bound each call instead,
    which lets a client trickle one byte per interval and hold the connection
    (and, on gthread, a pool slot) for as many intervals as the preface has
    bytes.
    """
    ...

UPGRADE_101: Final[bytes]

def upgrade_settings(req: _HasHeaders) -> bytes | None:
    """
    Return the HTTP2-Settings payload if this request asks for h2c.

    RFC 7540 section 3.2: the request must name ``h2c`` in Upgrade and carry
    exactly one HTTP2-Settings header, itself named in Connection. Returns
    None when the request is not a well-formed upgrade attempt, so the caller
    simply carries on with HTTP/1.
    """
    ...

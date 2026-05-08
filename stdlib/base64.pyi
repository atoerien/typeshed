"""Base16, Base32, Base64 (RFC 3548), Base85 and Ascii85 data encodings"""

import sys
from _typeshed import ReadableBuffer
from typing import IO

__all__ = [
    "encode",
    "decode",
    "encodebytes",
    "decodebytes",
    "b64encode",
    "b64decode",
    "b32encode",
    "b32decode",
    "b16encode",
    "b16decode",
    "b32hexencode",
    "b32hexdecode",
    "b85encode",
    "b85decode",
    "a85encode",
    "a85decode",
    "standard_b64encode",
    "standard_b64decode",
    "urlsafe_b64encode",
    "urlsafe_b64decode",
]

if sys.version_info >= (3, 13):
    __all__ += ["z85decode", "z85encode"]

def b64encode(s: ReadableBuffer, altchars: ReadableBuffer | None = None) -> bytes: ...
def b64decode(s: str | ReadableBuffer, altchars: str | ReadableBuffer | None = None, validate: bool = False) -> bytes: ...
def standard_b64encode(s: ReadableBuffer) -> bytes: ...
def standard_b64decode(s: str | ReadableBuffer) -> bytes: ...
def urlsafe_b64encode(s: ReadableBuffer) -> bytes: ...
def urlsafe_b64decode(s: str | ReadableBuffer) -> bytes: ...
def b32encode(s: ReadableBuffer) -> bytes: ...
def b32decode(s: str | ReadableBuffer, casefold: bool = False, map01: str | ReadableBuffer | None = None) -> bytes: ...
def b16encode(s: ReadableBuffer) -> bytes: ...
def b16decode(s: str | ReadableBuffer, casefold: bool = False) -> bytes: ...
def b32hexencode(s: ReadableBuffer) -> bytes: ...
def b32hexdecode(s: str | ReadableBuffer, casefold: bool = False) -> bytes: ...
def a85encode(
    b: ReadableBuffer, *, foldspaces: bool = False, wrapcol: int = 0, pad: bool = False, adobe: bool = False
) -> bytes:
    r"""
    Encode bytes-like object b using Ascii85 and return a bytes object.

    foldspaces is an optional flag that uses the special short sequence 'y'
    instead of 4 consecutive spaces (ASCII 0x20) as supported by 'btoa'. This
    feature is not supported by the "standard" Adobe encoding.

    wrapcol controls whether the output should have newline (b'\n') characters
    added to it. If this is non-zero, each output line will be at most this
    many characters long, excluding the trailing newline.

    pad controls whether the input is padded to a multiple of 4 before
    encoding. Note that the btoa implementation always pads.

    adobe controls whether the encoded byte sequence is framed with <~ and ~>,
    which is used by the Adobe implementation.
    """
    ...
def a85decode(
    b: str | ReadableBuffer, *, foldspaces: bool = False, adobe: bool = False, ignorechars: bytearray | bytes = b" \t\n\r\x0b"
) -> bytes:
    """
    Decode the Ascii85 encoded bytes-like object or ASCII string b.

    foldspaces is a flag that specifies whether the 'y' short sequence should be
    accepted as shorthand for 4 consecutive spaces (ASCII 0x20). This feature is
    not supported by the "standard" Adobe encoding.

    adobe controls whether the input sequence is in Adobe Ascii85 format (i.e.
    is framed with <~ and ~>).

    ignorechars should be a byte string containing characters to ignore from the
    input. This should only contain whitespace characters, and by default
    contains all whitespace characters in ASCII.

    The result is returned as a bytes object.
    """
    ...
def b85encode(b: ReadableBuffer, pad: bool = False) -> bytes:
    r"""
    Encode bytes-like object b in base85 format and return a bytes object.

    If pad is true, the input is padded with b'\0' so its length is a multiple of
    4 bytes before encoding.
    """
    ...
def b85decode(b: str | ReadableBuffer) -> bytes:
    """
    Decode the base85-encoded bytes-like object or ASCII string b

    The result is returned as a bytes object.
    """
    ...
def decode(input: IO[bytes], output: IO[bytes]) -> None:
    """Decode a file; input and output are binary files."""
    ...
def encode(input: IO[bytes], output: IO[bytes]) -> None:
    """Encode a file; input and output are binary files."""
    ...
def encodebytes(s: ReadableBuffer) -> bytes:
    """
    Encode a bytestring into a bytes object containing multiple lines
    of base-64 data.
    """
    ...
def decodebytes(s: ReadableBuffer) -> bytes:
    """Decode a bytestring of base-64 data into a bytes object."""
    ...

if sys.version_info >= (3, 13):
    def z85encode(s: ReadableBuffer) -> bytes:
        """Encode bytes-like object b in z85 format and return a bytes object."""
        ...
    def z85decode(s: str | ReadableBuffer) -> bytes:
        """
        Decode the z85-encoded bytes-like object or ASCII string b

        The result is returned as a bytes object.
        """
        ...

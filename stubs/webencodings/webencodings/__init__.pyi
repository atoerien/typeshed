"""
webencodings
~~~~~~~~~~~~

This is a Python implementation of the `WHATWG Encoding standard
<http://encoding.spec.whatwg.org/>`. See README for details.

:copyright: Copyright 2012 by Simon Sapin
:license: BSD, see LICENSE for details.
"""

import codecs
from collections.abc import Iterable, Iterator
from typing import Final

VERSION: Final[str]
__version__: Final[str]
PYTHON_NAMES: Final[dict[str, str]]
CACHE: dict[str, Encoding]

def ascii_lower(string: str) -> str:
    r"""
    Transform (only) ASCII letters to lower case: A-Z is mapped to a-z.

    :param string: An Unicode string.
    :returns: A new Unicode string.

    This is used for `ASCII case-insensitive
    <http://encoding.spec.whatwg.org/#ascii-case-insensitive>`_
    matching of encoding labels.
    The same matching is also used, among other things,
    for `CSS keywords <http://dev.w3.org/csswg/css-values/#keywords>`_.

    This is different from the :meth:`str.lower` method of Unicode strings
    which also affect non-ASCII characters,
    sometimes mapping them into the ASCII range:

        >>> keyword = 'Bac\N{KELVIN SIGN}ground'
        >>> assert keyword.lower() == 'background'
        >>> assert ascii_lower(keyword) != keyword.lower()
        >>> assert ascii_lower(keyword) == 'bac\N{KELVIN SIGN}ground'
    """
    ...
def lookup(label: str) -> Encoding | None:
    """
    Look for an encoding by its label.

    This is the spec's `get an encoding
    <http://encoding.spec.whatwg.org/#concept-encoding-get>`_ algorithm.
    Supported labels are listed there.

    :param label: A string.
    :returns:
        An :class:`Encoding` object, or :obj:`None` for an unknown label.
    """
    ...

class Encoding:
    """
    A character encoding that can be used for decoding or encoding.

    .. attribute:: name

        Canonical name of the encoding

    .. attribute:: codec_info

        The actual implementation of the encoding,
        a stdlib :class:`~codecs.CodecInfo` object.
        See :func:`codecs.register`.
    """
    name: str
    codec_info: codecs.CodecInfo
    def __init__(self, name: str, codec_info: codecs.CodecInfo) -> None: ...

UTF8: Final[Encoding]

def decode(input: bytes | bytearray, fallback_encoding: str | Encoding, errors: str = "replace") -> tuple[str, Encoding]:
    """
    Decode a single string.

    :param input: A byte string
    :param fallback_encoding:
        An :class:`Encoding` object or a label string.
        The encoding to use if :obj:`input` does not have a BOM.
    :param errors: Type of error handling. See :func:`codecs.register`.
    :raises: :exc:`LookupError` for an unknown encoding label.
    :return:
        A ``(output, encoding)`` tuple of an Unicode string
        and an :obj:`Encoding`.
    """
    ...
def encode(input: str, encoding: str | Encoding = ..., errors: str = "strict") -> bytes:
    """
    Encode a single string.

    :param input: An Unicode string.
    :param encoding: An :class:`Encoding` object or a label string.
    :param errors: Type of error handling. See :func:`codecs.register`.
    :raises: :exc:`LookupError` for an unknown encoding label.
    :return: A byte string.
    """
    ...
def iter_decode(
    input: Iterable[bytes | bytearray], fallback_encoding: str | Encoding, errors: str = "replace"
) -> tuple[Iterator[Encoding | str], Encoding]:
    """
    "Pull"-based decoder.

    :param input:
        An iterable of byte strings.

        The input is first consumed just enough to determine the encoding
        based on the precense of a BOM,
        then consumed on demand when the return value is.
    :param fallback_encoding:
        An :class:`Encoding` object or a label string.
        The encoding to use if :obj:`input` does not have a BOM.
    :param errors: Type of error handling. See :func:`codecs.register`.
    :raises: :exc:`LookupError` for an unknown encoding label.
    :returns:
        An ``(output, encoding)`` tuple.
        ``output`` is an iterable of Unicode strings,
        ``encoding`` is the :obj:`Encoding` that is being used.
    """
    ...
def iter_encode(input: Iterable[str], encoding: str | Encoding = ..., errors: str = "strict") -> Iterator[bytes]:
    """
    "Pull"-based encoder.

    :param input: An iterable of Unicode strings.
    :param encoding: An :class:`Encoding` object or a label string.
    :param errors: Type of error handling. See :func:`codecs.register`.
    :raises: :exc:`LookupError` for an unknown encoding label.
    :returns: An iterable of byte strings.
    """
    ...

class IncrementalDecoder:
    """
    "Push"-based decoder.

    :param fallback_encoding:
        An :class:`Encoding` object or a label string.
        The encoding to use if :obj:`input` does not have a BOM.
    :param errors: Type of error handling. See :func:`codecs.register`.
    :raises: :exc:`LookupError` for an unknown encoding label.
    """
    encoding: Encoding | None
    def __init__(self, fallback_encoding: str | Encoding, errors: str = "replace") -> None: ...
    def decode(self, input: bytes | bytearray, final: bool = False) -> str:
        """
        Decode one chunk of the input.

        :param input: A byte string.
        :param final:
            Indicate that no more input is available.
            Must be :obj:`True` if this is the last call.
        :returns: An Unicode string.
        """
        ...

class IncrementalEncoder:
    """
    "Push"-based encoder.

    :param encoding: An :class:`Encoding` object or a label string.
    :param errors: Type of error handling. See :func:`codecs.register`.
    :raises: :exc:`LookupError` for an unknown encoding label.

    .. method:: encode(input, final=False)

        :param input: An Unicode string.
        :param final:
            Indicate that no more input is available.
            Must be :obj:`True` if this is the last call.
        :returns: A byte string.
    """
    encode: bytes
    def __init__(self, encoding: str | Encoding = ..., errors: str = "strict") -> None: ...

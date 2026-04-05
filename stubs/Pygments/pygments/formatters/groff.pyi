"""
pygments.formatters.groff
~~~~~~~~~~~~~~~~~~~~~~~~~

Formatter for groff output.

:copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from _typeshed import SupportsWrite
from collections.abc import Iterable
from typing import TypeVar

from pygments.formatter import Formatter
from pygments.token import _TokenType

__all__ = ["GroffFormatter"]

_T = TypeVar("_T", str, bytes)

class GroffFormatter(Formatter[_T]):
    """
    Format tokens with groff escapes to change their color and font style.

    .. versionadded:: 2.11

    Additional options accepted:

    `style`
        The style to use, can be a string or a Style subclass (default:
        ``'default'``).

    `monospaced`
        If set to true, monospace font will be used (default: ``true``).

    `linenos`
        If set to true, print the line numbers (default: ``false``).

    `wrap`
        Wrap lines to the specified number of characters. Disabled if set to 0
        (default: ``0``).
    """
    monospaced: bool
    linenos: bool
    wrap: int
    styles: dict[_TokenType, tuple[str, str]]
    def __init__(self, **options) -> None: ...
    def format_unencoded(self, tokensource: Iterable[tuple[_TokenType, str]], outfile: SupportsWrite[str]) -> None: ...

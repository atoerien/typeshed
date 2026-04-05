"""
pygments.formatters.pangomarkup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Formatter for Pango markup output.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from _typeshed import Incomplete
from typing import TypeVar

from pygments.formatter import Formatter

_T = TypeVar("_T", str, bytes)

__all__ = ["PangoMarkupFormatter"]

class PangoMarkupFormatter(Formatter[_T]):
    """
    Format tokens as Pango Markup code. It can then be rendered to an SVG.

    .. versionadded:: 2.9
    """
    name: str
    aliases: Incomplete
    filenames: Incomplete
    styles: Incomplete
    def format_unencoded(self, tokensource, outfile) -> None: ...

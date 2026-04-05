"""
pygments.formatters.img
~~~~~~~~~~~~~~~~~~~~~~~

Formatter for Pixmap output.

:copyright: Copyright 2006-2025 by the Pygments team, see AUTHORS.
:license: BSD, see LICENSE for details.
"""

from _typeshed import Incomplete
from typing import TypeVar

from pygments.formatter import Formatter

_T = TypeVar("_T", str, bytes)

__all__ = ["ImageFormatter", "GifImageFormatter", "JpgImageFormatter", "BmpImageFormatter"]

class PilNotAvailable(ImportError): ...
class FontNotFound(Exception): ...

class FontManager:
    """Manages a set of fonts: normal, italic, bold, etc..."""
    font_name: Incomplete
    font_size: Incomplete
    fonts: Incomplete
    encoding: Incomplete
    variable: bool
    def __init__(self, font_name, font_size: int = 14) -> None: ...
    def get_char_size(self):
        """Get the character size."""
        ...
    def get_text_size(self, text):
        """Get the text size (width, height)."""
        ...
    def get_font(self, bold, oblique):
        """Get the font based on bold and italic flags."""
        ...
    def get_style(self, style):
        """
        Get the specified style of the font if it is a variable font.
        If not found, return the normal font.
        """
        ...

class ImageFormatter(Formatter[_T]):
    r"""
    Create a PNG image from source code. This uses the Python Imaging Library to
    generate a pixmap from the source code.

    .. versionadded:: 0.10

    Additional options accepted:

    `image_format`
        An image format to output to that is recognised by PIL, these include:

        * "PNG" (default)
        * "JPEG"
        * "BMP"
        * "GIF"

    `line_pad`
        The extra spacing (in pixels) between each line of text.

        Default: 2

    `font_name`
        The font name to be used as the base font from which others, such as
        bold and italic fonts will be generated.  This really should be a
        monospace font to look sane.
        If a filename or a file-like object is specified, the user must
        provide different styles of the font.

        Default: "Courier New" on Windows, "Menlo" on Mac OS, and
                 "DejaVu Sans Mono" on \*nix

    `font_size`
        The font size in points to be used.

        Default: 14

    `image_pad`
        The padding, in pixels to be used at each edge of the resulting image.

        Default: 10

    `line_numbers`
        Whether line numbers should be shown: True/False

        Default: True

    `line_number_start`
        The line number of the first line.

        Default: 1

    `line_number_step`
        The step used when printing line numbers.

        Default: 1

    `line_number_bg`
        The background colour (in "#123456" format) of the line number bar, or
        None to use the style background color.

        Default: "#eed"

    `line_number_fg`
        The text color of the line numbers (in "#123456"-like format).

        Default: "#886"

    `line_number_chars`
        The number of columns of line numbers allowable in the line number
        margin.

        Default: 2

    `line_number_bold`
        Whether line numbers will be bold: True/False

        Default: False

    `line_number_italic`
        Whether line numbers will be italicized: True/False

        Default: False

    `line_number_separator`
        Whether a line will be drawn between the line number area and the
        source code area: True/False

        Default: True

    `line_number_pad`
        The horizontal padding (in pixels) between the line number margin, and
        the source code area.

        Default: 6

    `hl_lines`
        Specify a list of lines to be highlighted.

        .. versionadded:: 1.2

        Default: empty list

    `hl_color`
        Specify the color for highlighting lines.

        .. versionadded:: 1.2

        Default: highlight color of the selected style
    """
    name: str
    aliases: Incomplete
    filenames: Incomplete
    unicodeoutput: bool
    default_image_format: str
    encoding: str
    styles: Incomplete
    background_color: str
    image_format: Incomplete
    image_pad: Incomplete
    line_pad: Incomplete
    fonts: Incomplete
    line_number_fg: Incomplete
    line_number_bg: Incomplete
    line_number_chars: Incomplete
    line_number_bold: Incomplete
    line_number_italic: Incomplete
    line_number_pad: Incomplete
    line_numbers: Incomplete
    line_number_separator: Incomplete
    line_number_step: Incomplete
    line_number_start: Incomplete
    line_number_width: Incomplete
    hl_lines: Incomplete
    hl_color: Incomplete
    drawables: Incomplete
    def get_style_defs(self, arg: str = "") -> None: ...
    def format(self, tokensource, outfile) -> None:
        """
        Format ``tokensource``, an iterable of ``(tokentype, tokenstring)``
        tuples and write it into ``outfile``.

        This implementation calculates where it should draw each token on the
        pixmap, then calculates the required pixmap size and draws the items.
        """
        ...

class GifImageFormatter(ImageFormatter[_T]):
    """
    Create a GIF image from source code. This uses the Python Imaging Library to
    generate a pixmap from the source code.

    .. versionadded:: 1.0
    """
    name: str
    aliases: Incomplete
    filenames: Incomplete
    default_image_format: str

class JpgImageFormatter(ImageFormatter[_T]):
    """
    Create a JPEG image from source code. This uses the Python Imaging Library to
    generate a pixmap from the source code.

    .. versionadded:: 1.0
    """
    name: str
    aliases: Incomplete
    filenames: Incomplete
    default_image_format: str

class BmpImageFormatter(ImageFormatter[_T]):
    """
    Create a bitmap image from source code. This uses the Python Imaging Library to
    generate a pixmap from the source code.

    .. versionadded:: 1.0
    """
    name: str
    aliases: Incomplete
    filenames: Incomplete
    default_image_format: str

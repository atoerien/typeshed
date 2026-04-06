from _typeshed import Incomplete, SupportsWrite
from collections.abc import Iterable
from typing_extensions import Never

from pygments.formatter import Formatter
from pygments.token import _TokenType

__all__ = ["ImageFormatter", "GifImageFormatter", "JpgImageFormatter", "BmpImageFormatter"]

class PilNotAvailable(ImportError):
    """When Python imaging library is not available"""
    ...
class FontNotFound(Exception):
    """When there are no usable fonts specified"""
    ...

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

class ImageFormatter(Formatter[bytes]):
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
    def get_style_defs(self, arg: str = "") -> Never: ...
    def format(self, tokensource: Iterable[tuple[_TokenType, str]], outfile: SupportsWrite[bytes]) -> None: ...

class GifImageFormatter(ImageFormatter):
    default_image_format: str

class JpgImageFormatter(ImageFormatter):
    default_image_format: str

class BmpImageFormatter(ImageFormatter):
    default_image_format: str

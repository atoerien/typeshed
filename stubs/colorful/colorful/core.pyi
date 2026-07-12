"""
colorful
~~~~~~~~

Terminal string styling done right, in Python.

:copyright: (c) 2017 by Timo Furrer <tuxtimo@gmail.com>
:license: MIT, see LICENSE for more details.
"""

from _typeshed import SupportsGetItem, SupportsItems, SupportsWrite

# This module defines a function "str()", which is why "str" can't be used
# as a type annotation or type alias.
from builtins import str as _str
from collections.abc import Iterator
from typing import Any, Final, Literal, TypeAlias
from typing_extensions import LiteralString, Self

# Custom type helpers
_ColorModeType: TypeAlias = Literal[0, 8, 16, 256, 16777215]
_PaletteType: TypeAlias = dict[_str, _str] | dict[_str, tuple[int, int, int]] | dict[_str, _str | tuple[int, int, int]]
_StyleType: TypeAlias = tuple[_str, _str]

DEFAULT_RGB_TXT_PATH: Final[_str]
COLOR_PALETTE: Final[dict[_str, _str]]
COLORNAMES_COLORS_PATH: Final[_str]

class ColorfulError(Exception):
    """
    Exception which is raised for Colorful specific
    usage errors.
    """
    ...
class ColorfulAttributeError(AttributeError, ColorfulError):
    """
    Exception which is raised for Colorful specific
    usage errors raised during ``__getattr__`` calls.

    This is to ensure a correct ``__getattr__`` protocol implementation.
    """
    ...

def translate_rgb_to_ansi_code(red: int, green: int, blue: int, offset: int, colormode: _ColorModeType) -> _str:
    """
    Translate the given RGB color into the appropriate ANSI escape code
    for the given color mode.
    The offset is used for the base color which is used.

    The ``colormode`` has to be one of:
        * 0: no colors / disabled
        * 8: use ANSI 8 colors
        * 16: use ANSI 16 colors (same as 8 but with brightness)
        * 256: use ANSI 256 colors
        * 0xFFFFFF / 16777215: use 16 Million true colors

    :param int red: the red channel value
    :param int green: the green channel value
    :param int blue: the blue channel value
    :param int offset: the offset to use for the base color
    :param int colormode: the color mode to use. See explanation above
    """
    ...
def translate_colorname_to_ansi_code(
    colorname: _str, offset: int, colormode: _ColorModeType, colorpalette: SupportsGetItem[_str, _str | tuple[int, int, int]]
) -> _str:
    """
    Translate the given color name to a valid
    ANSI escape code.

    :parma str colorname: the name of the color to resolve
    :parma str offset: the offset for the color code
    :param int colormode: the color mode to use. See ``translate_rgb_to_ansi_code``
    :parma dict colorpalette: the color palette to use for the color name mapping

    :returns str: the color as ANSI escape code

    :raises ColorfulError: if the given color name is invalid
    """
    ...
def resolve_modifier_to_ansi_code(modifiername: _str, colormode: _ColorModeType) -> _str:
    """
    Resolve the given modifier name to a valid
    ANSI escape code.

    :param str modifiername: the name of the modifier to resolve
    :param int colormode: the color mode to use. See ``translate_rgb_to_ansi_code``

    :returns str: the ANSI escape code for the modifier

    :raises ColorfulError: if the given modifier name is invalid
    """
    ...
def translate_style(
    style: _str, colormode: _ColorModeType, colorpalette: SupportsGetItem[_str, _str | tuple[int, int, int]]
) -> _str:
    """
    Translate the given style to an ANSI escape code
    sequence.

    ``style`` examples are:

    * green
    * bold
    * red_on_black
    * bold_green
    * italic_yellow_on_cyan

    :param str style: the style to translate
    :param int colormode: the color mode to use. See ``translate_rgb_to_ansi_code``
    :parma dict colorpalette: the color palette to use for the color name mapping
    """
    ...
def style_string(string: _str, ansi_style: _StyleType, colormode: _ColorModeType, nested: bool = False) -> _str:
    """
    Style the given string according to the given
    ANSI style string.

    :param str string: the string to style
    :param tuple ansi_style: the styling string returned by ``translate_style``
    :param int colormode: the color mode to use. See ``translate_rgb_to_ansi_code``

    :returns: a string containing proper ANSI sequence
    """
    ...

class ColorfulString:
    """Represents a colored string"""
    orig_string: _str
    styled_string: _str
    colorful_ctx: Colorful
    def __init__(self, orig_string: _str, styled_string: _str, colorful_ctx: Colorful) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_str]: ...
    def __add__(self, other: _str | ColorfulString) -> Self: ...
    def __iadd__(self, other: _str | ColorfulString) -> Self: ...
    def __radd__(self, other: _str | ColorfulString) -> Self: ...
    def __mul__(self, other: _str) -> Self: ...
    def __format__(self, format_spec: _str) -> _str: ...
    # Forwards item access to styled_string (a str).
    def __getattr__(self, name: _str) -> Any: ...

class Colorful:
    """
    Provides methods to style strings for terminal
    output.

    :param int colormode: the color mode to use. See ``translate_rgb_to_ansi_code``
    """
    NO_COLORS: Final[int]
    ANSI_8_COLORS: Final[int]
    ANSI_16_COLORS: Final[int]
    ANSI_256_COLORS: Final[int]
    TRUE_COLORS: Final[int]
    COLORNAMES_COLORS = COLORNAMES_COLORS_PATH
    close_fg_color: Final[_str]
    close_bg_color: Final[_str]
    no_bold: Final[_str]
    no_dimmed: Final[_str]
    no_italic: Final[_str]
    no_underlined: Final[_str]
    no_blinkslow: Final[_str]
    no_blinkrapid: Final[_str]
    no_inversed: Final[_str]
    no_concealed: Final[_str]
    no_struckthrough: Final[_str]
    colormode: _ColorModeType
    def __init__(self, colormode: _ColorModeType | None = None, colorpalette: _str | _PaletteType | None = None) -> None: ...

    @property
    def colorpalette(self) -> SupportsItems[_str, _str | tuple[int, int, int]] | None:
        """Get the current used color palette"""
        ...
    @colorpalette.setter
    def colorpalette(self, colorpalette: _str | _PaletteType) -> None:
        """Get the current used color palette"""
        ...

    def setup(
        self,
        colormode: _ColorModeType | None = None,
        colorpalette: _str | _PaletteType | None = None,
        extend_colors: bool = False,
    ) -> None:
        """
        Setup this colorful object by setting a ``colormode`` and
        the ``colorpalette`. The ``extend_colors`` flag is used
        to extend the currently active color palette instead of
        replacing it.

        :param int colormode: the color mode to use. See ``translate_rgb_to_ansi_code``
        :parma dict colorpalette: the colorpalette to use. This ``dict`` should map
                                  color names to it's corresponding RGB value
        :param bool extend_colors: extend the active color palette instead of replacing it
        """
        ...
    def disable(self) -> None:
        """Disable all colors and styles"""
        ...
    def use_8_ansi_colors(self) -> None:
        """Use 8 ANSI colors for this colorful object"""
        ...
    def use_16_ansi_colors(self) -> None:
        """Use 16 ANSI colors for this colorful object"""
        ...
    def use_256_ansi_colors(self) -> None:
        """Use 256 ANSI colors for this colorful object"""
        ...
    def use_true_colors(self) -> None:
        """Use true colors for this colorful object"""
        ...
    def use_palette(self, colorpalette: _str | _PaletteType) -> None:
        """Use the given color palette"""
        ...
    def update_palette(self, colorpalette: _str | _PaletteType) -> None:
        """
        Update the currently active color palette
        with the given color palette
        """
        ...
    def use_style(self, style_name: _str) -> None:
        """
        Use a predefined style as color palette

        :param str style_name: the name of the style
        """
        ...
    def format(self, string: _str, *args: LiteralString, **kwargs: LiteralString) -> _str:
        """
        Format the given string with the given ``args`` and ``kwargs``.
        The string can contain references to ``c`` which is provided by
        this colorful object.

        :param str string: the string to format
        """
        ...
    def str(self, string: _str) -> ColorfulString:
        "Create a new ColorfulString instance of the given\nunstyled string.\n\nThis method should be used to create a ColorfulString\nwhich is actually not styled yet but can safely be concatinated\nwith other ColorfulStrings like:\n\n>>> s = colorful.str('Hello ')\n>>> s =+ colorful.black('World')\n>>> str(s)\n'Hello \x1b[30mWorld\x1b[39m'\n\n:param str string: the string to use for the ColorfulString"
        ...
    def print(
        self, *objects: object, sep: _str = " ", end: _str = "\n", file: SupportsWrite[_str] | None = None, flush: bool = False
    ) -> None:
        """
        Print the given objects to the given file stream.
        See https://docs.python.org/3/library/functions.html#print

        The only difference to the ``print()`` built-in is that
        ``Colorful.print()`` formats the string with ``c=self``.
        With that stylings are possible

        :param str sep: the seperater between the objects
        :param str end: the ending delimiter after all objects
        :param file: the file stream to write to
        :param bool flush: if the stream should be flushed
        """
        ...

    class ColorfulStyle:
        """Represents a colorful style"""
        colormode: _ColorModeType
        colorful_ctx: Colorful
        def __init__(self, style: _StyleType, colormode: _ColorModeType, colorful_ctx: Colorful) -> None: ...
        def evaluate(self, string: _str, nested: bool = False) -> ColorfulString:
            """
            Evaluate the style on the given string.

            :parma str string: the string to style
            :param bool nested: if the string is part of another styled string
                                (=> nested in another style)
            """
            ...
        def __and__(self, other: Self) -> Self: ...
        def __call__(self, string: _str, nested: bool = False) -> ColorfulString: ...
        def __or__(self, other) -> ColorfulString: ...
        def __eq__(self, other: object) -> bool: ...
        def __hash__(self) -> int: ...

    def __getattr__(self, name: _str) -> ColorfulStyle: ...

from collections.abc import Iterable
from typing import Literal

from . import color4
from .ast import Node

COLOR_SCHEMES: set[str]
COLOR_SPACES: set[str]
D50: tuple[float, float, float]
D65: tuple[float, float, float]

class Color(color4.Color):
    COLOR_SPACES: set[str] | None

def parse_color(
    input: str | Iterable[Node], color_schemes: Literal["normal"] | Iterable[str] | None = None
) -> color4.Color | Color | Literal["currentcolor"] | None:
    """
    Parse a color value as defined in CSS Color Level 5.

    https://www.w3.org/TR/css-color-5/

    :type input: :obj:`str` or :term:`iterable`
    :param input: A string or an iterable of :term:`component values`.
    :type color_schemes: :obj:`str` or :term:`iterable`
    :param color_schemes: the ``'normal'`` string, or an iterable of color
        schemes used to resolve the ``light-dark()`` function.
    :returns:
        * :obj:`None` if the input is not a valid color value.
          (No exception is raised.)
        * The string ``'currentcolor'`` for the ``currentcolor`` keyword
        * A :class:`Color` object for every other values, including keywords.
    """
    ...

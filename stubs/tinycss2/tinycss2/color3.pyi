from collections.abc import Iterable
from typing import NamedTuple

from .ast import Node

class RGBA(NamedTuple):
    """
    An RGBA color.

    A tuple of four floats in the 0..1 range: ``(red, green, blue, alpha)``.

    .. attribute:: red

        Convenience access to the red channel. Same as ``rgba[0]``.

    .. attribute:: green

        Convenience access to the green channel. Same as ``rgba[1]``.

    .. attribute:: blue

        Convenience access to the blue channel. Same as ``rgba[2]``.

    .. attribute:: alpha

        Convenience access to the alpha channel. Same as ``rgba[3]``.
    """
    red: float
    green: float
    blue: float
    alpha: float

def parse_color(input: str | Iterable[Node]) -> str | RGBA | None:
    """
    Parse a color value as defined in CSS Color Level 3.

    https://www.w3.org/TR/css-color-3/

    :type input: :obj:`str` or :term:`iterable`
    :param input: A string or an iterable of :term:`component values`.
    :returns:
        * :obj:`None` if the input is not a valid color value.
          (No exception is raised.)
        * The string ``'currentColor'`` for the ``currentColor`` keyword
        * Or a :class:`RGBA` object for every other values
          (including keywords, HSL and HSLA.)
          The alpha channel is clipped to [0, 1]
          but red, green, or blue can be out of range
          (eg. ``rgb(-10%, 120%, 0%)`` is represented as
          ``(-0.1, 1.2, 0, 1)``.)
    """
    ...

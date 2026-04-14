from collections.abc import Iterable, Iterator
from typing import Literal

from .ast import Node

class Color:
    """
    A specified color in a defined color space.

    The color space is one of ``COLOR_SPACES``.

    Coordinates are floats with undefined ranges, but alpha channel is clipped
    to [0, 1]. Coordinates can also be set to ``None`` when undefined.
    """
    COLOR_SPACES: set[str] | None
    def __init__(self, space: str, coordinates: tuple[float | None, ...], alpha: float) -> None: ...
    def __iter__(self) -> Iterator[float | None]: ...
    def __getitem__(self, key: int) -> float: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: object) -> bool: ...
    def to(self, space: str) -> Color:
        """
        Return new instance with coordinates transformed to given ``space``.

        The destination color space is one of ``SPACES``.

        ``None`` coordinates are always transformed into ``0`` values.

        Here are the supported combinations:

        - from hsl and hwb to srgb;
        - from lab and lch to xyz-d50;
        - from oklab and oklch to xyz-d65;
        - from xyz-d50, xyz-d65, lch, oklab and oklch to lab.
        """
        ...

def parse_color(input: str | Iterable[Node]) -> Color | Literal["currentcolor"] | None:
    """
    Parse a color value as defined in CSS Color Level 4.

    https://www.w3.org/TR/css-color-4/

    :type input: :obj:`str` or :term:`iterable`
    :param input: A string or an iterable of :term:`component values`.
    :returns:
        * :obj:`None` if the input is not a valid color value.
          (No exception is raised.)
        * The string ``'currentcolor'`` for the ``currentcolor`` keyword
        * A :class:`Color` object for every other values, including keywords.
    """
    ...

COLOR_SPACES: set[str]
D50: tuple[float, float, float]
D65: tuple[float, float, float]

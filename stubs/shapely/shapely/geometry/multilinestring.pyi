"""Collections of linestrings and related utilities."""

from collections.abc import Collection
from typing import Literal
from typing_extensions import Self

from .base import BaseMultipartGeometry
from .linestring import LineString, _ConvertibleToLineString
from .multipoint import MultiPoint

__all__ = ["MultiLineString"]

class MultiLineString(BaseMultipartGeometry[LineString]):
    """
    A collection of one or more LineStrings.

    A MultiLineString has non-zero length and zero area.

    Parameters
    ----------
    lines : sequence
        A sequence LineStrings, or a sequence of line-like coordinate
        sequences or array-likes (see accepted input for LineString).

    Attributes
    ----------
    geoms : sequence
        A sequence of LineStrings

    Examples
    --------
    Construct a MultiLineString containing two LineStrings.

    >>> from shapely import MultiLineString
    >>> lines = MultiLineString([[[0, 0], [1, 2]], [[4, 4], [5, 6]]])
    """
    __slots__: list[str] = []
    def __new__(self, lines: BaseMultipartGeometry | Collection[_ConvertibleToLineString] | None = None) -> Self:
        """Create a new MultiLineString geometry."""
        ...
    def svg(self, scale_factor: float = 1.0, stroke_color: str | None = None, opacity: float | None = None) -> str:
        """
        Return a group of SVG polyline elements for the LineString geometry.

        Parameters
        ----------
        scale_factor : float
            Multiplication factor for the SVG stroke-width.  Default is 1.
        stroke_color : str, optional
            Hex string for stroke color. Default is to use "#66cc99" if
            geometry is valid, and "#ff3333" if invalid.
        opacity : float
            Float number between 0 and 1 for color opacity. Default value is 0.8
        """
        ...
    # more precise base overrides
    @property
    def geom_type(self) -> Literal["MultiLineString"]: ...
    @property
    def boundary(self) -> MultiPoint: ...

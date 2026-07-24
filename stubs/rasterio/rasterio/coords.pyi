"""Bounding box tuple, and disjoint operator."""

from typing import NamedTuple, TypeAlias

_Quadruple: TypeAlias = tuple[float, float, float, float]

class BoundingBox(NamedTuple):
    """
    Bounding box named tuple, defining extent in cartesian coordinates.

    .. code::

        BoundingBox(left, bottom, right, top)
    """
    left: float
    bottom: float
    right: float
    top: float

def disjoint_bounds(bounds1: BoundingBox | _Quadruple, bounds2: BoundingBox | _Quadruple) -> bool:
    """
    Compare two bounds and determine if they are disjoint.

    Parameters
    ----------
    bounds1: 4-tuple
        rasterio bounds tuple (left, bottom, right, top)
    bounds2: 4-tuple
        rasterio bounds tuple

    Returns
    -------
    boolean
    ``True`` if bounds are disjoint,
    ``False`` if bounds overlap
    """
    ...

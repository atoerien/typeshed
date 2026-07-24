"""Ground control points"""

from collections.abc import Sequence
from typing import Literal, TypedDict, type_check_only

@type_check_only
class GroundControlPointDict(TypedDict):
    id: str
    info: str | None
    row: float
    col: float
    x: float
    y: float
    z: float | None

@type_check_only
class GroundControlPointGeometry(TypedDict):
    type: Literal["Point"]
    coordinates: Sequence[float]

@type_check_only
class GroundControlPointFeature(TypedDict):
    id: str
    type: Literal["Feature"]
    geometry: GroundControlPointGeometry
    properties: GroundControlPointDict

class GroundControlPoint:
    """A mapping of row, col image coordinates to x, y, z."""
    id: str
    info: str | None
    row: float
    col: float
    x: float
    y: float
    z: float | None
    def __init__(
        self,
        row: float | None = None,
        col: float | None = None,
        x: float | None = None,
        y: float | None = None,
        z: float | None = None,
        id: str | None = None,
        info: str | None = None,
    ) -> None:
        """
        Create a new ground control point

        Parameters
        ----------
        row, col : float, required
            The row (or line) and column (or pixel) coordinates that
            map to spatial coordinate values ``y`` and ``x``,
            respectively.
        x, y : float, required
            Spatial coordinates of a ground control point.
        z : float, optional
            Optional ``z`` coordinate.
        id : str, optional
            A unique identifier for the ground control point.
        info : str, optional
            A short description for the ground control point.
        """
        ...
    def asdict(self) -> GroundControlPointDict:
        """A dict representation of the GCP"""
        ...
    @property
    def __geo_interface__(self) -> GroundControlPointFeature:
        """A GeoJSON representation of the GCP"""
        ...

from collections.abc import Sequence
from decimal import Decimal
from typing import Literal, TypeAlias

from geojson.base import GeoJSON

_InputCoord: TypeAlias = float | Decimal | Geometry | Sequence[_InputCoord]
_CleanCoord: TypeAlias = float | Decimal | list[_CleanCoord]

DEFAULT_PRECISION: Literal[6]

class Geometry(GeoJSON):
    """Represents an abstract base class for a WGS84 geometry."""
    def __init__(
        self,
        coordinates: None | Sequence[_InputCoord] | Geometry = None,
        validate: bool = False,
        precision: None | int = None,
        **extra,
    ) -> None:
        """
        Initialises a Geometry object.

        :param coordinates: Coordinates of the Geometry object.
        :type coordinates: tuple or list of tuple
        :param validate: Raise exception if validation errors are present?
        :type validate: boolean
        :param precision: Number of decimal places for lat/lon coords.
        :type precision: integer
        """
        ...
    @classmethod
    def clean_coordinates(cls, coords: Sequence[_InputCoord] | Geometry, precision: int) -> list[_CleanCoord]: ...

class GeometryCollection(GeoJSON):
    """Represents an abstract base class for collections of WGS84 geometries."""
    def __init__(self, geometries: Sequence[Geometry] | None = None, **extra) -> None: ...
    def errors(self) -> list[str] | None: ...
    def __getitem__(self, key) -> Geometry | tuple[()] | None: ...

def check_point(coord) -> str | None: ...

class Point(Geometry):
    def errors(self) -> list[str] | None: ...

class MultiPoint(Geometry):
    def errors(self) -> list[str] | None: ...

def check_line_string(coord) -> str | None: ...

class LineString(Geometry):
    def errors(self) -> list[str] | None: ...

class MultiLineString(MultiPoint):
    def errors(self) -> list[str] | None: ...

def check_polygon(coord) -> str | None: ...

class Polygon(Geometry):
    def errors(self) -> list[str] | None: ...

class MultiPolygon(Geometry):
    def errors(self) -> list[str] | None: ...

class Default:
    """GeoJSON default object."""
    ...

"""Feature extraction"""

from collections.abc import Iterator
from typing import Any, Final

from rasterio._typing import _OGRGeometry
from rasterio.enums import MergeAlg as MergeAlg

GEOMETRY_TYPES: Final[dict[int, str]]
GEOJSON2OGR_GEOMETRY_TYPES: Final[dict[str, int]]

bool_: Final[str]
int8: Final[str]
int16: Final[str]
int32: Final[str]
int64: Final[str]
uint8: Final[str]
uint16: Final[str]
uint32: Final[str]
uint64: Final[str]
float16: Final[str]
float32: Final[str]
float64: Final[str]

# Cython-side builders. `geom` arguments are opaque C structs / OGR
# geometry handles passed through `__pyx_capi__`; not surfaced via the
# public `rasterio.features` API.
class GeomBuilder:
    """Builds a GeoJSON (Fiona-style) geometry from an OGR geometry."""
    def build(self, geom: object) -> dict[str, Any]: ...

class OGRGeomBuilder:
    """
    Builds an OGR geometry from GeoJSON geometry.
    From Fiona: https://github.com/Toblerity/Fiona/blob/master/fiona/ogrext.pyx
    """
    def build(self, geom: dict[str, Any]) -> _OGRGeometry: ...

class ShapeIterator:
    """Provides an iterator over shapes in an OGR feature layer."""
    def __iter__(self) -> Iterator[tuple[dict[str, Any], float]]:
        """Implement iter(self)."""
        ...
    def __next__(self) -> tuple[dict[str, Any], float]: ...

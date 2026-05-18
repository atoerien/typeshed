"""Support for various GEOS geometry operations."""

from collections.abc import Callable, Iterable
from typing import Any, Literal, overload

from ._typing import GeoT, OptGeoArrayLike, SupportsGeoInterface
from .algorithms.polylabel import polylabel as polylabel
from .geometry import GeometryCollection, LineString, MultiLineString, Point, Polygon
from .geometry.base import BaseGeometry, BaseMultipartGeometry, GeometrySequence
from .geometry.linestring import _ConvertibleToLineString
from .lib import Geometry

__all__ = [
    "clip_by_rect",
    "linemerge",
    "nearest_points",
    "operator",
    "orient",
    "polygonize",
    "polygonize_full",
    "shared_paths",
    "snap",
    "split",
    "substring",
    "transform",
    "triangulate",
    "unary_union",
    "validate",
    "voronoi_diagram",
]

class CollectionOperator:
    @overload
    def shapeup(self, ob: GeoT) -> GeoT: ...  # type: ignore[overload-overlap]
    @overload
    def shapeup(self, ob: dict[str, Any] | SupportsGeoInterface) -> BaseGeometry: ...  # type: ignore[overload-overlap]
    @overload
    def shapeup(self, ob: _ConvertibleToLineString) -> LineString: ...

    def polygonize(
        self, lines: OptGeoArrayLike | Iterable[_ConvertibleToLineString | None]
    ) -> GeometrySequence[GeometryCollection[Polygon]]:
        """
        Create polygons from a source of lines.

        The source may be a MultiLineString, a sequence of LineString objects,
        or a sequence of objects than can be adapted to LineStrings.
        """
        ...
    def polygonize_full(
        self, lines: OptGeoArrayLike | Iterable[_ConvertibleToLineString | None]
    ) -> tuple[
        GeometryCollection[Polygon], GeometryCollection[LineString], GeometryCollection[LineString], GeometryCollection[Polygon]
    ]:
        """
        Create polygons from a source of lines.

        The polygons and leftover geometries are returned as well.

        The source may be a MultiLineString, a sequence of LineString objects,
        or a sequence of objects than can be adapted to LineStrings.

        Returns a tuple of objects: (polygons, cut edges, dangles, invalid ring
        lines). Each are a geometry collection.

        Dangles are edges which have one or both ends which are not incident on
        another edge endpoint. Cut edges are connected at both ends but do not
        form part of polygon. Invalid ring lines form rings which are invalid
        (bowties, etc).
        """
        ...
    def linemerge(
        self, lines: MultiLineString | BaseMultipartGeometry | Iterable[_ConvertibleToLineString], directed: bool = False
    ) -> LineString | MultiLineString:
        """
        Merge all connected lines from a source.

        The source may be a MultiLineString, a sequence of LineString objects,
        or a sequence of objects than can be adapted to LineStrings.  Returns a
        LineString or MultiLineString when lines are not contiguous.
        """
        ...
    def unary_union(self, geoms: OptGeoArrayLike) -> BaseGeometry:
        """
        Return the union of a sequence of geometries.

        Usually used to convert a collection into the smallest set of polygons
        that cover the same area.
        """
        ...

operator: CollectionOperator
polygonize = operator.polygonize
polygonize_full = operator.polygonize_full
linemerge = operator.linemerge
unary_union = operator.unary_union

# This is also an alias to operator method but we want to mark it as deprecated
@overload  # edges false
def triangulate(geom: Geometry, tolerance: float = 0.0, edges: Literal[False] = False) -> list[Polygon]:
    """
    Create the Delaunay triangulation and return a list of geometries.

    The source may be any geometry type. All vertices of the geometry will be
    used as the points of the triangulation.

    From the GEOS documentation:
    tolerance is the snapping tolerance used to improve the robustness of
    the triangulation computation. A tolerance of 0.0 specifies that no
    snapping will take place.

    If edges is False, a list of Polygons (triangles) will be returned.
    Otherwise the list of LineString edges is returned.
    """
    ...
@overload  # edges true (keyword)
def triangulate(geom: Geometry, tolerance: float = 0.0, *, edges: Literal[True]) -> list[LineString]:
    """
    Create the Delaunay triangulation and return a list of geometries.

    The source may be any geometry type. All vertices of the geometry will be
    used as the points of the triangulation.

    From the GEOS documentation:
    tolerance is the snapping tolerance used to improve the robustness of
    the triangulation computation. A tolerance of 0.0 specifies that no
    snapping will take place.

    If edges is False, a list of Polygons (triangles) will be returned.
    Otherwise the list of LineString edges is returned.
    """
    ...
@overload  # edges true (positional)
def triangulate(geom: Geometry, tolerance: float, edges: Literal[True]) -> list[LineString]:
    """
    Create the Delaunay triangulation and return a list of geometries.

    The source may be any geometry type. All vertices of the geometry will be
    used as the points of the triangulation.

    From the GEOS documentation:
    tolerance is the snapping tolerance used to improve the robustness of
    the triangulation computation. A tolerance of 0.0 specifies that no
    snapping will take place.

    If edges is False, a list of Polygons (triangles) will be returned.
    Otherwise the list of LineString edges is returned.
    """
    ...
@overload  # fallback
def triangulate(geom: Geometry, tolerance: float = 0.0, edges: bool = False) -> list[Polygon] | list[LineString]: ...

@overload
def voronoi_diagram(
    geom: Geometry, envelope: Geometry | None = None, tolerance: float = 0.0, edges: Literal[False] = False
) -> GeometryCollection[Polygon]:
    """
    Construct a Voronoi Diagram [1] from the given geometry.

    Returns a list of geometries.

    Parameters
    ----------
    geom: geometry
        the input geometry whose vertices will be used to calculate
        the final diagram.
    envelope: geometry, None
        clipping envelope for the returned diagram, automatically
        determined if None. The diagram will be clipped to the larger
        of this envelope or an envelope surrounding the sites.
    tolerance: float, 0.0
        sets the snapping tolerance used to improve the robustness
        of the computation. A tolerance of 0.0 specifies that no
        snapping will take place.
    edges: bool, False
        If False, return regions as polygons. Else, return only
        edges e.g. LineStrings.

    GEOS documentation can be found at [2]

    Returns
    -------
    GeometryCollection
        geometries representing the Voronoi regions.

    Notes
    -----
    The tolerance `argument` can be finicky and is known to cause the
    algorithm to fail in several cases. If you're using `tolerance`
    and getting a failure, try removing it. The test cases in
    tests/test_voronoi_diagram.py show more details.


    References
    ----------
    [1] https://en.wikipedia.org/wiki/Voronoi_diagram
    [2] https://geos.osgeo.org/doxygen/geos__c_8h_source.html  (line 730)
    """
    ...
@overload
def voronoi_diagram(
    geom: Geometry, envelope: Geometry | None, tolerance: float, edges: Literal[True]
) -> GeometryCollection[LineString | MultiLineString]:
    """
    Construct a Voronoi Diagram [1] from the given geometry.

    Returns a list of geometries.

    Parameters
    ----------
    geom: geometry
        the input geometry whose vertices will be used to calculate
        the final diagram.
    envelope: geometry, None
        clipping envelope for the returned diagram, automatically
        determined if None. The diagram will be clipped to the larger
        of this envelope or an envelope surrounding the sites.
    tolerance: float, 0.0
        sets the snapping tolerance used to improve the robustness
        of the computation. A tolerance of 0.0 specifies that no
        snapping will take place.
    edges: bool, False
        If False, return regions as polygons. Else, return only
        edges e.g. LineStrings.

    GEOS documentation can be found at [2]

    Returns
    -------
    GeometryCollection
        geometries representing the Voronoi regions.

    Notes
    -----
    The tolerance `argument` can be finicky and is known to cause the
    algorithm to fail in several cases. If you're using `tolerance`
    and getting a failure, try removing it. The test cases in
    tests/test_voronoi_diagram.py show more details.


    References
    ----------
    [1] https://en.wikipedia.org/wiki/Voronoi_diagram
    [2] https://geos.osgeo.org/doxygen/geos__c_8h_source.html  (line 730)
    """
    ...
@overload
def voronoi_diagram(
    geom: Geometry, envelope: Geometry | None = None, tolerance: float = 0.0, *, edges: Literal[True]
) -> GeometryCollection[LineString | MultiLineString]:
    """
    Construct a Voronoi Diagram [1] from the given geometry.

    Returns a list of geometries.

    Parameters
    ----------
    geom: geometry
        the input geometry whose vertices will be used to calculate
        the final diagram.
    envelope: geometry, None
        clipping envelope for the returned diagram, automatically
        determined if None. The diagram will be clipped to the larger
        of this envelope or an envelope surrounding the sites.
    tolerance: float, 0.0
        sets the snapping tolerance used to improve the robustness
        of the computation. A tolerance of 0.0 specifies that no
        snapping will take place.
    edges: bool, False
        If False, return regions as polygons. Else, return only
        edges e.g. LineStrings.

    GEOS documentation can be found at [2]

    Returns
    -------
    GeometryCollection
        geometries representing the Voronoi regions.

    Notes
    -----
    The tolerance `argument` can be finicky and is known to cause the
    algorithm to fail in several cases. If you're using `tolerance`
    and getting a failure, try removing it. The test cases in
    tests/test_voronoi_diagram.py show more details.


    References
    ----------
    [1] https://en.wikipedia.org/wiki/Voronoi_diagram
    [2] https://geos.osgeo.org/doxygen/geos__c_8h_source.html  (line 730)
    """
    ...
@overload
def voronoi_diagram(
    geom: Geometry, envelope: Geometry | None = None, tolerance: float = 0.0, edges: bool = False
) -> GeometryCollection[Polygon | LineString | MultiLineString]: ...

@overload
def validate(geom: None) -> None:
    """Return True if the geometry is valid."""
    ...
@overload
def validate(geom: Geometry) -> str:
    """Return True if the geometry is valid."""
    ...
@overload
def validate(geom: Geometry | None) -> str | None: ...

def transform(func: Callable[[float, float, float | None], tuple[float, ...]], geom: GeoT) -> GeoT: ...
def nearest_points(g1: Geometry, g2: Geometry) -> tuple[Point, Point]: ...
def snap(g1: GeoT, g2: Geometry, tolerance: float) -> GeoT: ...
def shared_paths(g1: LineString, g2: LineString) -> GeometryCollection[MultiLineString]: ...

class SplitOp:
    @staticmethod
    def split(geom: Geometry, splitter: Geometry) -> GeometryCollection:
        """
        Split a geometry by another geometry and return a collection of geometries.

        This function is the theoretical opposite of the union of
        the split geometry parts. If the splitter does not split the geometry, a
        collection with a single geometry equal to the input geometry is
        returned.

        The function supports:
          - Splitting a (Multi)LineString by a (Multi)Point or (Multi)LineString
            or (Multi)Polygon
          - Splitting a (Multi)Polygon by a LineString

        It may be convenient to snap the splitter with low tolerance to the
        geometry. For example in the case of splitting a line by a point, the
        point must be exactly on the line, for the line to be correctly split.
        When splitting a line by a polygon, the boundary of the polygon is used
        for the operation. When splitting a line by another line, a ValueError
        is raised if the two overlap at some segment.

        Parameters
        ----------
        geom : geometry
            The geometry to be split
        splitter : geometry
            The geometry that will split the input geom

        Examples
        --------
        >>> import shapely.ops
        >>> from shapely import Point, LineString
        >>> pt = Point((1, 1))
        >>> line = LineString([(0,0), (2,2)])
        >>> result = shapely.ops.split(line, pt)
        >>> result.wkt
        'GEOMETRYCOLLECTION (LINESTRING (0 0, 1 1), LINESTRING (1 1, 2 2))'
        """
        ...

split = SplitOp.split

def substring(geom: LineString, start_dist: float, end_dist: float, normalized: bool = False) -> Point | LineString:
    """
    Return a line segment between specified distances along a LineString.

    Negative distance values are taken as measured in the reverse
    direction from the end of the geometry. Out-of-range index
    values are handled by clamping them to the valid range of values.

    If the start distance equals the end distance, a Point is returned.

    If the start distance is actually beyond the end distance, then the
    reversed substring is returned such that the start distance is
    at the first coordinate.

    Parameters
    ----------
    geom : LineString
        The geometry to get a substring of.
    start_dist : float
        The distance along `geom` of the start of the substring.
    end_dist : float
        The distance along `geom` of the end of the substring.
    normalized : bool, False
        Whether the distance parameters are interpreted as a
        fraction of the geometry's length.

    Returns
    -------
    Union[Point, LineString]
        The substring between `start_dist` and `end_dist` or a Point
        if they are at the same location.

    Raises
    ------
    TypeError
        If `geom` is not a LineString.

    Examples
    --------
    >>> from shapely.geometry import LineString
    >>> from shapely.ops import substring
    >>> ls = LineString((i, 0) for i in range(6))
    >>> ls.wkt
    'LINESTRING (0 0, 1 0, 2 0, 3 0, 4 0, 5 0)'
    >>> substring(ls, start_dist=1, end_dist=3).wkt
    'LINESTRING (1 0, 2 0, 3 0)'
    >>> substring(ls, start_dist=3, end_dist=1).wkt
    'LINESTRING (3 0, 2 0, 1 0)'
    >>> substring(ls, start_dist=1, end_dist=-3).wkt
    'LINESTRING (1 0, 2 0)'
    >>> substring(ls, start_dist=0.2, end_dist=-0.6, normalized=True).wkt
    'LINESTRING (1 0, 2 0)'

    Returning a `Point` when `start_dist` and `end_dist` are at the
    same location.

    >>> substring(ls, 2.5, -2.5).wkt
    'POINT (2.5 0)'
    """
    ...
def clip_by_rect(geom: Geometry, xmin: float, ymin: float, xmax: float, ymax: float) -> BaseGeometry:
    """
    Return the portion of a geometry within a rectangle.

    The geometry is clipped in a fast but possibly dirty way. The output is
    not guaranteed to be valid. No exceptions will be raised for topological
    errors.

    Parameters
    ----------
    geom : geometry
        The geometry to be clipped
    xmin : float
        Minimum x value of the rectangle
    ymin : float
        Minimum y value of the rectangle
    xmax : float
        Maximum x value of the rectangle
    ymax : float
        Maximum y value of the rectangle

    Notes
    -----
    New in 1.7.
    """
    ...
def orient(geom: GeoT, sign: float = 1.0) -> GeoT:
    """
    Return a properly oriented copy of the given geometry.

    The signed area of the result will have the given sign. A sign of
    1.0 means that the coordinates of the product's exterior rings will
    be oriented counter-clockwise.

    It is recommended to use :func:`shapely.orient_polygons` instead.

    Parameters
    ----------
    geom : Geometry
        The original geometry. May be a Polygon, MultiPolygon, or
        GeometryCollection.
    sign : float, optional.
        The sign of the result's signed area.

    Returns
    -------
    Geometry
    """
    ...

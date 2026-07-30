"""Coordinate utility functions."""

from _typeshed import Incomplete
from collections.abc import Callable, Generator
from typing import Any, Literal

from geojson.base import GeoJSON
from geojson.geometry import Geometry, LineString, Point, Polygon

def coords(obj: GeoJSON | dict[str, Any]) -> Generator[tuple[float]]:
    """
    Yields the coordinates from a Feature or Geometry.

    :param obj: A geometry or feature to extract the coordinates from.
    :type obj: Feature, Geometry
    :return: A generator with coordinate tuples from the geometry or feature.
    :rtype: generator
    """
    ...
def map_coords(func: Callable[[Incomplete], float | Geometry], obj: GeoJSON | dict[str, Any]) -> dict[str, Any]:
    """
    Returns the mapped coordinates from a Geometry after applying the provided
    function to each dimension in tuples list (ie, linear scaling).

    :param func: Function to apply to individual coordinate values
    independently
    :type func: function
    :param obj: A geometry or feature to extract the coordinates from.
    :type obj: Point, LineString, MultiPoint, MultiLineString, Polygon,
    MultiPolygon
    :return: The result of applying the function to each dimension in the
    array.
    :rtype: list
    :raises ValueError: if the provided object is not GeoJSON.
    """
    ...
def map_tuples(func: Callable[[Incomplete], float | Geometry], obj: GeoJSON | dict[str, Any]) -> dict[str, Any]:
    """
    Returns the mapped coordinates from a Geometry after applying the provided
    function to each coordinate.

    :param func: Function to apply to tuples
    :type func: function
    :param obj: A geometry or feature to extract the coordinates from.
    :type obj: Point, LineString, MultiPoint, MultiLineString, Polygon,
    MultiPolygon
    :return: The result of applying the function to each dimension in the
    array.
    :rtype: list
    :raises ValueError: if the provided object is not GeoJSON.
    """
    ...
def map_geometries(func: Callable[[Incomplete], float | Geometry], obj: GeoJSON | dict[str, Any]) -> dict[str, Any]:
    """
    Returns the result of passing every geometry in the given geojson object
    through func.

    :param func: Function to apply to tuples
    :type func: function
    :param obj: A geometry or feature to extract the coordinates from.
    :type obj: GeoJSON
    :return: The result of applying the function to each geometry
    :rtype: list
    :raises ValueError: if the provided object is not geojson.
    """
    ...
def generate_random(
    featureType: Literal["Point", "LineString", "Polygon"],
    numberVertices: int = 3,
    boundingBox: list[float] = [-180.0, -90.0, 180.0, 90.0],
) -> Point | LineString | Polygon:
    """
    Generates random geojson features depending on the parameters
    passed through.
    The bounding box defaults to the world - [-180.0, -90.0, 180.0, 90.0].
    The number of vertices defaults to 3.

    :param featureType: A geometry type
    :type featureType: Point, LineString, Polygon
    :param numberVertices: The number vertices that a linestring or polygon
    will have
    :type numberVertices: int
    :param boundingBox: A bounding box in which features will be restricted to
    :type boundingBox: list
    :return: The resulting random geojson object or geometry collection.
    :rtype: object
    :raises ValueError: if there is no featureType provided.
    """
    ...

from typing import Any

from geojson.base import GeoJSON
from geojson.geometry import Geometry

class Feature(GeoJSON):
    """Represents a WGS84 GIS feature."""
    def __init__(
        self, id: str | int | None = None, geometry: Geometry | None = None, properties: dict[str, Any] | None = None, **extra
    ) -> None:
        """
        Initialises a Feature object with the given parameters.

        :param id: Feature identifier, such as a sequential number.
        :type id: str, int
        :param geometry: Geometry corresponding to the feature.
        :param properties: Dict containing properties of the feature.
        :type properties: dict
        :return: Feature object
        :rtype: Feature
        """
        ...
    def errors(self) -> list[str] | None: ...

class FeatureCollection(GeoJSON):
    """Represents a FeatureCollection, a set of multiple Feature objects."""
    def __init__(self, features: list[Feature | Geometry], **extra) -> None:
        """
        Initialises a FeatureCollection object from the
        :param features: List of features to constitute the FeatureCollection.
        :type features: list
        :return: FeatureCollection object
        :rtype: FeatureCollection
        """
        ...
    def errors(self) -> list[str] | None: ...
    def __getitem__(self, key: int | str) -> Feature: ...

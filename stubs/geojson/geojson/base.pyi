from _typeshed import Incomplete
from collections.abc import Iterable
from typing import Any

class GeoJSON(dict[str, Any]):
    """A class representing a GeoJSON object."""
    def __init__(self, iterable: Iterable[tuple[str, Any]] = (), **extra) -> None:
        """
        Initialises a GeoJSON object

        :param iterable: iterable from which to draw the content of the GeoJSON
        object.
        :type iterable: dict, array, tuple
        :return: a GeoJSON object
        :rtype: GeoJSON
        """
        ...
    def __getattr__(self, name: str | int) -> Incomplete:
        """
        Permit dictionary items to be retrieved like object attributes

        :param name: attribute name
        :type name: str, int
        :return: dictionary value
        """
        ...
    def __setattr__(self, name: str, value) -> None:
        """
        Permit dictionary items to be set like object attributes.

        :param name: key of item to be set
        :type name: str
        :param value: value to set item to
        """
        ...
    def __delattr__(self, name: str) -> None:
        """
        Permit dictionary items to be deleted like object attributes

        :param name: key of item to be deleted
        :type name: str
        """
        ...
    @property
    def __geo_interface__(self) -> None | GeoJSON: ...
    @classmethod
    def to_instance(cls, ob, default=None, strict: bool = False) -> GeoJSON:
        """
        Encode a GeoJSON dict into an GeoJSON object.
        Assumes the caller knows that the dict should satisfy a GeoJSON type.

        :param cls: Dict containing the elements to be encoded into a GeoJSON
        object.
        :type cls: dict
        :param ob: GeoJSON object into which to encode the dict provided in
        `cls`.
        :type ob: GeoJSON
        :param default: A default instance to append the content of the dict
        to if none is provided.
        :type default: GeoJSON
        :param strict: Raise error if unable to coerce particular keys or
        attributes to a valid GeoJSON structure.
        :type strict: bool
        :return: A GeoJSON object with the dict's elements as its constituents.
        :rtype: GeoJSON
        :raises TypeError: If the input dict contains items that are not valid
        GeoJSON types.
        :raises UnicodeEncodeError: If the input dict contains items of a type
        that contain non-ASCII characters.
        :raises AttributeError: If the input dict contains items that are not
        valid GeoJSON types.
        """
        ...
    @property
    def is_valid(self) -> bool: ...
    def check_list_errors(self, checkFunc, lst) -> list[str] | None:
        """Validation helper function."""
        ...
    def errors(self) -> list[str] | None:
        """
        Return validation errors (if any).
        Implement in each subclass.
        """
        ...

from typing import Any, Literal

GEO_INTERFACE_MARKER: Literal["__geo_interface__"]

def is_mapping(obj) -> bool:
    """
    Checks if the object is an instance of MutableMapping.

    :param obj: Object to be checked.
    :return: Truth value of whether the object is an instance of
    MutableMapping.
    :rtype: bool
    """
    ...
def to_mapping(obj) -> dict[str, Any]: ...

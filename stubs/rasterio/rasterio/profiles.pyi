"""Raster dataset profiles."""

from collections import UserDict
from typing import Any, ClassVar, Final

# A `Profile` is a dict of GDAL driver-specific dataset-creation options
# (e.g. `count`, `dtype`, `compress`); value types depend on the option.
class Profile(UserDict[str, Any]):
    """
    Base class for Rasterio dataset profiles.

    Subclasses will declare driver-specific creation options.
    """
    defaults: ClassVar[dict[str, Any]]
    def __init__(self, data: dict[str, Any] = ..., **kwds: Any) -> None:
        """
        Create a new profile based on the class defaults, which are
        overlaid with items from the `data` dict and keyword arguments.
        """
        ...
    def __getitem__(self, key: str) -> Any:
        """Like normal item access but with affine alias."""
        ...
    def __setitem__(self, key: str, val: Any) -> None:
        """Like normal item setter but forbidding affine item."""
        ...

class DefaultGTiffProfile(Profile):
    """Tiled, band-interleaved, LZW-compressed, 8-bit GTiff."""
    defaults: ClassVar[dict[str, Any]]

default_gtiff_profile: Final[DefaultGTiffProfile]

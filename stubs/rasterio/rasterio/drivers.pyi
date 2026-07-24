"""
Driver policies and utilities

GDAL has many standard and extension format drivers and completeness of
these drivers varies greatly. It's possible to succeed poorly with some
formats and drivers, meaning that easy problems can be solved but that
harder problems are blocked by limitations of the drivers and formats.

NetCDF writing, for example, is presently blacklisted. Rasterio users
should use netcdf4-python instead:
http://unidata.github.io/netcdf4-python/.
"""

import os
from typing import Final

blacklist: Final[dict[str, tuple[str, ...]]]

def raster_driver_extensions() -> dict[str, str]:
    """
    Returns
    -------
    dict:
        Map of extensions to the driver.
    """
    ...
def driver_from_extension(path: str | os.PathLike[str]) -> str:
    """
    Attempt to auto-detect driver based on the extension.

    Parameters
    ----------
    path: str or pathlike object
        The path to the dataset to write with.

    Returns
    -------
    str:
        The name of the driver for the extension.
    """
    ...
def is_blacklisted(name: str, mode: str) -> bool:
    """Returns True if driver `name` and `mode` are blacklisted."""
    ...

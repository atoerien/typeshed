"""Raster file management."""

import os
from typing import Any

from rasterio._typing import _OpenOption

def exists(path: str | os.PathLike[str]) -> bool:
    """
    Determine if a dataset exists by attempting to open it.

    Parameters
    ----------
    path : str
        Path to dataset
    """
    ...
def copy(
    # An open dataset handle (DatasetReader / DatasetWriter / DatasetBase) or a path.
    src: str | os.PathLike[str] | Any,
    dst: str | os.PathLike[str],
    driver: str | None = None,
    strict: bool = True,
    **creation_options: _OpenOption,
) -> None:
    """
    Copy a raster from a path or open dataset handle to a new destination
    with driver specific creation options.

    Parameters
    ----------
    src : str or PathLike or dataset object opened in 'r' mode
        Source dataset
    dst : str or PathLike
        Output dataset path
    driver : str, optional
        Output driver name
    strict : bool, optional.  Default: True
        Indicates if the output must be strictly equivalent or if the
        driver may adapt as necessary
    creation_options : dict, optional
        Creation options for output dataset

    Returns
    -------
    None
    """
    ...
def copyfiles(src: str | os.PathLike[str], dst: str | os.PathLike[str]) -> None:
    """
    Copy files associated with a dataset from one location to another.

    Parameters
    ----------
    src : str or PathLike
        Source dataset
    dst : str or PathLike
        Target dataset

    Returns
    -------
    None
    """
    ...
def delete(path: str | os.PathLike[str], driver: str | None = None) -> None:
    """
    Delete a GDAL dataset

    Parameters
    ----------
    path : path
        Path to dataset to delete
    driver : str or None, optional
        Name of driver to use for deleting.  Defaults to whatever GDAL
        determines is the appropriate driver
    """
    ...

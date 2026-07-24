"""
Dataset paths, identifiers, and filenames

Note well: this module is deprecated in 1.3.0 and will be removed in a
future version.
"""

from typing import TypeAlias
from typing_extensions import deprecated

from rasterio._path import _ParsedPath, _UnparsedPath
from rasterio.errors import RasterioDeprecationWarning as RasterioDeprecationWarning

ParsedPath: TypeAlias = _ParsedPath
UnparsedPath: TypeAlias = _UnparsedPath

@deprecated("rasterio.path.parse_path is deprecated; use rasterio._path._parse_path or pass paths directly to rasterio.open.")
def parse_path(path: str) -> _ParsedPath | _UnparsedPath:
    """
    Parse a dataset's identifier or path into its parts

    Parameters
    ----------
    path : str or path-like object
        The path to be parsed.

    Returns
    -------
    ParsedPath or UnparsedPath

    Notes
    -----
    When legacy GDAL filenames are encountered, they will be returned
    in a UnparsedPath.
    """
    ...
@deprecated("rasterio.path.vsi_path is deprecated; use rasterio._path._vsi_path directly.")
def vsi_path(path: _ParsedPath | _UnparsedPath) -> str:
    """
    Convert a parsed path to a GDAL VSI path

    Parameters
    ----------
    path : Path
        A ParsedPath or UnparsedPath object.

    Returns
    -------
    str
    """
    ...

"""Utility functions."""

from pathlib import Path

from ._typing import ReadPathOrBuffer

def get_vsi_path_or_buffer(path_or_buffer: ReadPathOrBuffer) -> str | bytes:
    """
    Get VSI-prefixed path or bytes buffer depending on type of path_or_buffer.

    If path_or_buffer is a bytes object, it will be returned directly and will
    be read into an in-memory dataset when passed to one of the Cython functions.

    If path_or_buffer is a file-like object with a read method, bytes will be
    read from the file-like object and returned.

    Otherwise, it will be converted to a string, and parsed to prefix with
    appropriate GDAL /vsi*/ prefixes.

    Parameters
    ----------
    path_or_buffer : str, pathlib.Path, bytes, or file-like
        A dataset path or URI, raw buffer, or file-like object with a read method.

    Returns
    -------
    str or bytes
    """
    ...
def vsi_path(path: str | Path) -> str:
    """Ensure path is a local path or a GDAL-compatible VSI path."""
    ...

SCHEMES: dict[str, str]
CURLSCHEMES: set[str]

def vsimem_rmtree_toplevel(path: str | Path) -> None:
    """
    Remove the parent directory of the file path recursively.

    This is used for final cleanup of an in-memory dataset, which may have been
    created within a directory to contain sibling files.

    Additional VSI handlers may be chained to the left of /vsimem/ in path and
    will be ignored.

    Remark: function is defined here to be able to run tests on it.

    Parameters
    ----------
    path : str or pathlib.Path
        path to in-memory file
    """
    ...

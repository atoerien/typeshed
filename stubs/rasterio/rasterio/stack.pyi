"""Raster stacking tool."""

import logging
import os
from collections.abc import Sequence
from typing import Any, Final

from numpy.typing import DTypeLike, NDArray
from rasterio._affine_types import Affine
from rasterio.enums import Resampling
from rasterio.io import DatasetReader

logger: Final[logging.Logger]

def stack(
    sources: Sequence[DatasetReader | str | os.PathLike[str]],
    bounds: tuple[float, float, float, float] | None = None,
    res: float | tuple[float, float] | None = None,
    nodata: float | None = None,
    dtype: DTypeLike | None = None,
    indexes: int | Sequence[int] | None = None,
    output_count: int | None = None,
    resampling: Resampling = ...,
    target_aligned_pixels: bool = False,
    mem_limit: int = 64,
    use_highest_res: bool = False,
    masked: bool = False,
    dst_path: str | os.PathLike[str] | None = None,
    dst_kwds: dict[str, Any] | None = None,
) -> tuple[NDArray[Any], Affine]:
    """
    Copy valid pixels from input files to an output file.

    All files must have the same data type, and
    coordinate reference system. Rotated, flipped, or upside-down
    rasters cannot be stacked.

    Geospatial bounds and resolution of a new output file in the units
    of the input file coordinate reference system may be provided and
    are otherwise taken from the source datasets.

    Parameters
    ----------
    sources : list
        A sequence of dataset objects opened in 'r' mode or Path-like
        objects.
    bounds: tuple, optional
        Bounds of the output image (left, bottom, right, top).
        If not set, bounds are determined from bounds of input rasters.
    res: tuple, optional
        Output resolution in units of coordinate reference system. If
        not set, a source resolution will be used. If a single value is
        passed, output pixels will be square.
    use_highest_res: bool, optional. Default: False.
        If True, the highest resolution of all sources will be used. If
        False, the first source's resolution will be used.
    masked: bool, optional. Default: False.
        If True, return a masked array. Note: nodata is always set in
        the case of file output.
    nodata: float, optional
        nodata value to use in output file. If not set, uses the nodata
        value in the first input raster.
    dtype: numpy.dtype or string
        dtype to use in outputfile. If not set, uses the dtype value in
        the first input raster.
    indexes : list of ints or a single int, optional
        bands to read and stack.
    output_count: int, optional
        If using callable it may be useful to have additional bands in
        the output in addition to the indexes specified for read.
    resampling : Resampling, optional
        Resampling algorithm used when reading input files.
        Default: `Resampling.nearest`.
    target_aligned_pixels : bool, optional
        Whether to adjust output image bounds so that pixel coordinates
        are integer multiples of pixel size, matching the ``-tap``
        options of GDAL utilities.  Default: False.
    mem_limit : int, optional
        Process stack output in chunks of mem_limit MB in size.
    dst_path : str or PathLike, optional
        Path of output dataset.
    dst_kwds : dict, optional
        Dictionary of creation options and other parameters that will be
        overlaid on the profile of the output dataset.

    Returns
    -------
    tuple
        Two elements:
            dest: numpy.ndarray
                Contents of all input rasters in single array
            out_transform: affine.Affine()
                Information for mapping pixel coordinates in `dest` to
                another coordinate system

    Raises
    ------
    StackError
        When sources cannot be stacked due to incompatibility between
        them or limitations of the tool.
    """
    ...

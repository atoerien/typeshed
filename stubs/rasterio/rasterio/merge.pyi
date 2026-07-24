"""Copy valid pixels from input files to an output file."""

import logging
import os
from collections.abc import Callable, Sequence
from typing import Any, Final, Literal, TypeAlias, overload
from typing_extensions import deprecated

from numpy.typing import DTypeLike, NDArray
from rasterio._affine_types import Affine
from rasterio.enums import Resampling
from rasterio.io import DatasetReader

logger: Final[logging.Logger]

MethodFunction: TypeAlias = Callable[..., None]
MERGE_METHODS: Final[dict[str, MethodFunction]]

_Arr: TypeAlias = NDArray[Any]

# `**kwargs` on each merge method accepts forwarded options from `merge()` (e.g. `index`); ignored otherwise.
def copy_first(merged_data: _Arr, new_data: _Arr, merged_mask: _Arr, new_mask: _Arr, **kwargs: Any) -> None:
    """Returns the first available pixel."""
    ...
def copy_last(merged_data: _Arr, new_data: _Arr, merged_mask: _Arr, new_mask: _Arr, **kwargs: Any) -> None:
    """Returns the last available pixel."""
    ...
def copy_min(merged_data: _Arr, new_data: _Arr, merged_mask: _Arr, new_mask: _Arr, **kwargs: Any) -> None:
    """Returns the minimum value pixel."""
    ...
def copy_max(merged_data: _Arr, new_data: _Arr, merged_mask: _Arr, new_mask: _Arr, **kwargs: Any) -> None:
    """Returns the maximum value pixel."""
    ...
def copy_sum(merged_data: _Arr, new_data: _Arr, merged_mask: _Arr, new_mask: _Arr, **kwargs: Any) -> None:
    """Returns the sum of all pixel values."""
    ...
def copy_count(merged_data: _Arr, new_data: _Arr, merged_mask: _Arr, new_mask: _Arr, **kwargs: Any) -> None:
    """Returns the count of valid pixels."""
    ...

@overload
def merge(
    sources: Sequence[DatasetReader | str | os.PathLike[str]],
    bounds: tuple[float, float, float, float] | None = None,
    res: float | tuple[float, float] | None = None,
    nodata: float | None = None,
    dtype: DTypeLike | None = None,
    *,
    indexes: int | Sequence[int] | None = None,
    output_count: int | None = None,
    resampling: Resampling = ...,
    method: Literal["first", "last", "min", "max", "sum", "count"] | MethodFunction = "first",
    target_aligned_pixels: bool = False,
    mem_limit: int = 64,
    use_highest_res: bool = False,
    masked: bool = False,
    dst_path: str | os.PathLike[str] | None = None,
    dst_kwds: dict[str, Any] | None = None,
) -> tuple[NDArray[Any], Affine]:
    """
    Copy valid pixels from input files to an output file.

    All files must have the same number of bands, data type, and
    coordinate reference system. Rotated, flipped, or upside-down
    rasters cannot be merged.

    Input files are merged in their listed order using the reverse
    painter's algorithm (default) or another method. If the output file
    exists, its values will be overwritten by input values.

    Geospatial bounds and resolution of a new output file in the units
    of the input file coordinate reference system may be provided and
    are otherwise taken from the first input file.

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
    nodata: float, optional
        nodata value to use in output file. If not set, uses the nodata
        value in the first input raster.
    masked: bool, optional. Default: False.
        If True, return a masked array. Note: nodata is always set in
        the case of file output.
    dtype: numpy.dtype or string
        dtype to use in outputfile. If not set, uses the dtype value in
        the first input raster.
    precision: int, optional
        This parameters is unused, deprecated in rasterio 1.3.0, and
        will be removed in version 2.0.0.
    indexes : list of ints or a single int, optional
        bands to read and merge
    output_count: int, optional
        If using callable it may be useful to have additional bands in
        the output in addition to the indexes specified for read
    resampling : Resampling, optional
        Resampling algorithm used when reading input files.
        Default: `Resampling.nearest`.
    method : str or callable
        pre-defined method:

            * first: reverse painting
            * last: paint valid new on top of existing
            * min: pixel-wise min of existing and new
            * max: pixel-wise max of existing and new
            * sum: pixel-wise sum of existing and new
            * count: pixel-wise count of valid pixels

        or custom callable with signature:
            merged_data : array_like
                array to update with new_data
            new_data : array_like
                data to merge
                same shape as merged_data
            merged_mask, new_mask : array_like
                boolean masks where merged/new data pixels are invalid
                same shape as merged_data
            index: int
                index of the current dataset within the merged dataset
                collection
            roff: int
                row offset in base array
            coff: int
                column offset in base array

    target_aligned_pixels : bool, optional
        Whether to adjust output image bounds so that pixel coordinates
        are integer multiples of pixel size, matching the ``-tap``
        options of GDAL utilities.  Default: False.
    mem_limit : int, optional
        Process merge output in chunks of mem_limit MB in size.
    dst_path : str or PathLike, optional
        Path of output dataset
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
    MergeError
        When sources cannot be merged due to incompatibility between
        them or limitations of the tool.
    """
    ...
@overload
@deprecated("The `precision` parameter is unused since rasterio 1.3 and will be removed in 2.0.0.")
def merge(
    sources: Sequence[DatasetReader | str | os.PathLike[str]],
    bounds: tuple[float, float, float, float] | None = None,
    res: float | tuple[float, float] | None = None,
    nodata: float | None = None,
    dtype: DTypeLike | None = None,
    precision: int | None = None,
    indexes: int | Sequence[int] | None = None,
    output_count: int | None = None,
    resampling: Resampling = ...,
    method: Literal["first", "last", "min", "max", "sum", "count"] | MethodFunction = "first",
    target_aligned_pixels: bool = False,
    mem_limit: int = 64,
    use_highest_res: bool = False,
    masked: bool = False,
    dst_path: str | os.PathLike[str] | None = None,
    dst_kwds: dict[str, Any] | None = None,
) -> tuple[NDArray[Any], Affine]:
    """
    Copy valid pixels from input files to an output file.

    All files must have the same number of bands, data type, and
    coordinate reference system. Rotated, flipped, or upside-down
    rasters cannot be merged.

    Input files are merged in their listed order using the reverse
    painter's algorithm (default) or another method. If the output file
    exists, its values will be overwritten by input values.

    Geospatial bounds and resolution of a new output file in the units
    of the input file coordinate reference system may be provided and
    are otherwise taken from the first input file.

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
    nodata: float, optional
        nodata value to use in output file. If not set, uses the nodata
        value in the first input raster.
    masked: bool, optional. Default: False.
        If True, return a masked array. Note: nodata is always set in
        the case of file output.
    dtype: numpy.dtype or string
        dtype to use in outputfile. If not set, uses the dtype value in
        the first input raster.
    precision: int, optional
        This parameters is unused, deprecated in rasterio 1.3.0, and
        will be removed in version 2.0.0.
    indexes : list of ints or a single int, optional
        bands to read and merge
    output_count: int, optional
        If using callable it may be useful to have additional bands in
        the output in addition to the indexes specified for read
    resampling : Resampling, optional
        Resampling algorithm used when reading input files.
        Default: `Resampling.nearest`.
    method : str or callable
        pre-defined method:

            * first: reverse painting
            * last: paint valid new on top of existing
            * min: pixel-wise min of existing and new
            * max: pixel-wise max of existing and new
            * sum: pixel-wise sum of existing and new
            * count: pixel-wise count of valid pixels

        or custom callable with signature:
            merged_data : array_like
                array to update with new_data
            new_data : array_like
                data to merge
                same shape as merged_data
            merged_mask, new_mask : array_like
                boolean masks where merged/new data pixels are invalid
                same shape as merged_data
            index: int
                index of the current dataset within the merged dataset
                collection
            roff: int
                row offset in base array
            coff: int
                column offset in base array

    target_aligned_pixels : bool, optional
        Whether to adjust output image bounds so that pixel coordinates
        are integer multiples of pixel size, matching the ``-tap``
        options of GDAL utilities.  Default: False.
    mem_limit : int, optional
        Process merge output in chunks of mem_limit MB in size.
    dst_path : str or PathLike, optional
        Path of output dataset
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
    MergeError
        When sources cannot be merged due to incompatibility between
        them or limitations of the tool.
    """
    ...

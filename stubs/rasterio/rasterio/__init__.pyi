"""Rasterio"""

import logging
import os
from collections.abc import Callable, Sequence
from typing import Any, Final, Literal, NamedTuple, TypeAlias, overload

from numpy.typing import DTypeLike, NDArray
from rasterio._base import DatasetBase as DatasetBase
from rasterio._io import Statistics as Statistics
from rasterio._path import _parse_path as _parse_path, _UnparsedPath as _UnparsedPath
from rasterio._show_versions import show_versions as show_versions
from rasterio._typing import AnyDataset, CRSInput, _Opener, _OpenOption
from rasterio._version import (
    gdal_version as gdal_version,
    get_geos_version as get_geos_version,
    get_proj_version as get_proj_version,
)
from rasterio._vsiopener import _opener_registration as _opener_registration
from rasterio.crs import CRS as CRS
from rasterio.drivers import driver_from_extension as driver_from_extension, is_blacklisted as is_blacklisted
from rasterio.dtypes import (
    bool_ as bool_,
    check_dtype as check_dtype,
    complex_ as complex_,
    complex_int16 as complex_int16,
    float16 as float16,
    float32 as float32,
    float64 as float64,
    int8 as int8,
    int16 as int16,
    int32 as int32,
    int64 as int64,
    sbyte as sbyte,
    ubyte as ubyte,
    uint8 as uint8,
    uint16 as uint16,
    uint32 as uint32,
    uint64 as uint64,
)
from rasterio.env import Env as Env, ensure_env_with_credentials as ensure_env_with_credentials
from rasterio.errors import (
    DriverCapabilityError as DriverCapabilityError,
    RasterioDeprecationWarning as RasterioDeprecationWarning,
    RasterioIOError as RasterioIOError,
)
from rasterio.io import (
    BufferedDatasetWriter as BufferedDatasetWriter,
    DatasetReader as DatasetReader,
    DatasetWriter as DatasetWriter,
    FilePath as FilePath,
    MemoryFile as MemoryFile,
    get_writer_for_driver as get_writer_for_driver,
    get_writer_for_path as get_writer_for_path,
)
from rasterio.profiles import default_gtiff_profile as default_gtiff_profile
from rasterio.transform import Affine as Affine, guard_transform as guard_transform

__all__ = ["CRS", "Band", "Env", "band", "open", "pad"]

__version__: Final[str]
__gdal_version__: Final[str]
__proj_version__: Final[str]
__geos_version__: Final[str]

have_vsi_plugin: Final[bool]
log: logging.Logger

_Fp: TypeAlias = str | os.PathLike[str] | MemoryFile | FilePath

@overload
def open(
    fp: _Fp,
    mode: Literal["r"] = "r",
    driver: str | Sequence[str] | None = None,
    width: int | None = None,
    height: int | None = None,
    count: int | None = None,
    crs: CRSInput | None = None,
    transform: Affine | None = None,
    dtype: DTypeLike | None = None,
    nodata: float | None = None,
    sharing: bool = False,
    thread_safe: bool = False,
    opener: _Opener | None = None,
    **kwargs: _OpenOption,
) -> DatasetReader:
    """
    Open a dataset for reading or writing.

    The dataset may be located in a local file, in a resource located by
    a URL, or contained within a stream of bytes. This function accepts
    different types of fp parameters. However, it is almost always best
    to pass a string that has a dataset name as its value. These are
    passed directly to GDAL protocol and format handlers. A path to
    a zipfile is more efficiently used by GDAL than a Python ZipFile
    object, for example.

    In read ('r') or read/write ('r+') mode, no keyword arguments are
    required: these attributes are supplied by the opened dataset.

    In write ('w' or 'w+') mode, the driver, width, height, count, and
    dtype keywords are strictly required.

    Parameters
    ----------
    fp : str, os.PathLike, file-like, or rasterio.io.MemoryFile
        A filename or URL, a file object opened in binary ('rb') mode,
        a Path object, or one of the rasterio classes that provides the
        dataset-opening interface (has an open method that returns
        a dataset). Use a string when possible: GDAL can more
        efficiently access a dataset if it opens it natively.
    mode : str, optional
        'r' (read, the default), 'r+' (read/write), 'w' (write), or
        'w+' (write/read).
    driver : str, optional
        A short format driver name (e.g. "GTiff" or "JPEG") or a list of
        such names (see GDAL docs at
        https://gdal.org/drivers/raster/index.html). In 'w' or 'w+' modes
        a single name is required. In 'r' or 'r+' modes the driver can
        usually be omitted. Registered drivers will be tried
        sequentially until a match is found. When multiple drivers are
        available for a format such as JPEG2000, one of them can be
        selected by using this keyword argument.
    width : int, optional
        The number of columns of the raster dataset. Required in 'w' or
        'w+' modes, it is ignored in 'r' or 'r+' modes.
    height : int, optional
        The number of rows of the raster dataset. Required in 'w' or
        'w+' modes, it is ignored in 'r' or 'r+' modes.
    count : int, optional
        The count of dataset bands. Required in 'w' or 'w+' modes, it is
        ignored in 'r' or 'r+' modes.
    crs : str, dict, or CRS, optional
        The coordinate reference system. Required in 'w' or 'w+' modes,
        it is ignored in 'r' or 'r+' modes.
    transform : affine.Affine, optional
        Affine transformation mapping the pixel space to geographic
        space. Required in 'w' or 'w+' modes, it is ignored in 'r' or
        'r+' modes.
    dtype : str or numpy.dtype, optional
        The data type for bands. For example: 'uint8' or
        `rasterio.uint16`. Required in 'w' or 'w+' modes, it is
        ignored in 'r' or 'r+' modes.
    nodata : int, float, or nan, optional
        Defines the pixel value to be interpreted as not valid data.
        Required in 'w' or 'w+' modes, it is ignored in 'r' or 'r+'
        modes.
    sharing : bool, optional
        To reduce overhead and prevent programs from running out of file
        descriptors, rasterio maintains a pool of shared low level
        dataset handles. If True this function will use a shared
        handle if one is available. Multithreaded programs must avoid
        sharing and should set *sharing* to False.
    thread_safe: bool, optional
        Open GDAL dataset in `thread safe mode <https://gdal.org/en/stable/user/multithreading.html>`__.
        For multithreaded read-only GDAL dataset operations (e.g. ``GDAL_NUM_THREADS``, `LIBERTIFF driver <https://gdal.org/en/stable/drivers/raster/libertiff.html#open-options>`__).
        Requires rasterio 1.5+ & GDAL 3.10+.
    opener : callable, optional
        A custom dataset opener which can serve GDAL's virtual
        filesystem machinery via Python file-like objects. The
        underlying file-like object is obtained by calling *opener* with
        (*fp*, *mode*) or (*fp*, *mode* + 'b') depending on the format
        driver's native mode. *opener* must return a Python file-like
        object that provides read, seek, tell, and close methods. Note:
        only one opener at a time per fp, mode pair is allowed.
    kwargs : optional
        These are passed to format drivers as directives for creating or
        interpreting datasets. For example: in 'w' or 'w+' modes
        a tiled=True keyword argument will direct the GeoTIFF format
        driver to create a tiled, rather than striped, TIFF.

    Returns
    -------
    :class:`rasterio.io.DatasetReader`
        If mode is 'r'.
    :class:`rasterio.io.DatasetWriter`
        If mode is 'r+', 'w', or 'w+'.

    Raises
    ------
    :class:`TypeError`
        If arguments are of the wrong Python type.
    :class:`rasterio.errors.RasterioIOError`
        If the dataset can not be opened. Such as when there is no
        dataset with the given name.
    :class:`rasterio.errors.DriverCapabilityError`
        If the detected format driver does not support the requested
        opening mode.

    Notes
    -----
    If *fp* is a is a file-like object, its entire contents will be
    read into a MemoryFile instance. It will almost always be better
    to use a path or URL, or the *opener* keyword argument.

    Examples
    --------
    To open a local GeoTIFF dataset for reading using standard driver
    discovery and no directives:

    >>> import rasterio
    >>> with rasterio.open('example.tif') as dataset:
    ...     print(dataset.profile)

    To open a local JPEG2000 dataset using only the JP2OpenJPEG driver:

    >>> with rasterio.open(
    ...         'example.jp2', driver='JP2OpenJPEG') as dataset:
    ...     print(dataset.profile)

    To create a new 8-band, 16-bit unsigned, tiled, and LZW-compressed
    GeoTIFF with a global extent and 0.5 degree resolution:

    >>> from rasterio.transform import from_origin
    >>> with rasterio.open(
    ...         'example.tif', 'w', driver='GTiff', dtype='uint16',
    ...         width=720, height=360, count=8, crs='EPSG:4326',
    ...         transform=from_origin(-180.0, 90.0, 0.5, 0.5),
    ...         nodata=0, tiled=True, compress='lzw') as dataset:
    ...     dataset.write(...)
    """
    ...
@overload
def open(
    fp: _Fp,
    mode: Literal["r+", "w", "w+"],
    driver: str | Sequence[str] | None = None,
    width: int | None = None,
    height: int | None = None,
    count: int | None = None,
    crs: CRSInput | None = None,
    transform: Affine | None = None,
    dtype: DTypeLike | None = None,
    nodata: float | None = None,
    sharing: bool = False,
    thread_safe: bool = False,
    opener: _Opener | None = None,
    **kwargs: _OpenOption,
) -> DatasetWriter:
    """
    Open a dataset for reading or writing.

    The dataset may be located in a local file, in a resource located by
    a URL, or contained within a stream of bytes. This function accepts
    different types of fp parameters. However, it is almost always best
    to pass a string that has a dataset name as its value. These are
    passed directly to GDAL protocol and format handlers. A path to
    a zipfile is more efficiently used by GDAL than a Python ZipFile
    object, for example.

    In read ('r') or read/write ('r+') mode, no keyword arguments are
    required: these attributes are supplied by the opened dataset.

    In write ('w' or 'w+') mode, the driver, width, height, count, and
    dtype keywords are strictly required.

    Parameters
    ----------
    fp : str, os.PathLike, file-like, or rasterio.io.MemoryFile
        A filename or URL, a file object opened in binary ('rb') mode,
        a Path object, or one of the rasterio classes that provides the
        dataset-opening interface (has an open method that returns
        a dataset). Use a string when possible: GDAL can more
        efficiently access a dataset if it opens it natively.
    mode : str, optional
        'r' (read, the default), 'r+' (read/write), 'w' (write), or
        'w+' (write/read).
    driver : str, optional
        A short format driver name (e.g. "GTiff" or "JPEG") or a list of
        such names (see GDAL docs at
        https://gdal.org/drivers/raster/index.html). In 'w' or 'w+' modes
        a single name is required. In 'r' or 'r+' modes the driver can
        usually be omitted. Registered drivers will be tried
        sequentially until a match is found. When multiple drivers are
        available for a format such as JPEG2000, one of them can be
        selected by using this keyword argument.
    width : int, optional
        The number of columns of the raster dataset. Required in 'w' or
        'w+' modes, it is ignored in 'r' or 'r+' modes.
    height : int, optional
        The number of rows of the raster dataset. Required in 'w' or
        'w+' modes, it is ignored in 'r' or 'r+' modes.
    count : int, optional
        The count of dataset bands. Required in 'w' or 'w+' modes, it is
        ignored in 'r' or 'r+' modes.
    crs : str, dict, or CRS, optional
        The coordinate reference system. Required in 'w' or 'w+' modes,
        it is ignored in 'r' or 'r+' modes.
    transform : affine.Affine, optional
        Affine transformation mapping the pixel space to geographic
        space. Required in 'w' or 'w+' modes, it is ignored in 'r' or
        'r+' modes.
    dtype : str or numpy.dtype, optional
        The data type for bands. For example: 'uint8' or
        `rasterio.uint16`. Required in 'w' or 'w+' modes, it is
        ignored in 'r' or 'r+' modes.
    nodata : int, float, or nan, optional
        Defines the pixel value to be interpreted as not valid data.
        Required in 'w' or 'w+' modes, it is ignored in 'r' or 'r+'
        modes.
    sharing : bool, optional
        To reduce overhead and prevent programs from running out of file
        descriptors, rasterio maintains a pool of shared low level
        dataset handles. If True this function will use a shared
        handle if one is available. Multithreaded programs must avoid
        sharing and should set *sharing* to False.
    thread_safe: bool, optional
        Open GDAL dataset in `thread safe mode <https://gdal.org/en/stable/user/multithreading.html>`__.
        For multithreaded read-only GDAL dataset operations (e.g. ``GDAL_NUM_THREADS``, `LIBERTIFF driver <https://gdal.org/en/stable/drivers/raster/libertiff.html#open-options>`__).
        Requires rasterio 1.5+ & GDAL 3.10+.
    opener : callable, optional
        A custom dataset opener which can serve GDAL's virtual
        filesystem machinery via Python file-like objects. The
        underlying file-like object is obtained by calling *opener* with
        (*fp*, *mode*) or (*fp*, *mode* + 'b') depending on the format
        driver's native mode. *opener* must return a Python file-like
        object that provides read, seek, tell, and close methods. Note:
        only one opener at a time per fp, mode pair is allowed.
    kwargs : optional
        These are passed to format drivers as directives for creating or
        interpreting datasets. For example: in 'w' or 'w+' modes
        a tiled=True keyword argument will direct the GeoTIFF format
        driver to create a tiled, rather than striped, TIFF.

    Returns
    -------
    :class:`rasterio.io.DatasetReader`
        If mode is 'r'.
    :class:`rasterio.io.DatasetWriter`
        If mode is 'r+', 'w', or 'w+'.

    Raises
    ------
    :class:`TypeError`
        If arguments are of the wrong Python type.
    :class:`rasterio.errors.RasterioIOError`
        If the dataset can not be opened. Such as when there is no
        dataset with the given name.
    :class:`rasterio.errors.DriverCapabilityError`
        If the detected format driver does not support the requested
        opening mode.

    Notes
    -----
    If *fp* is a is a file-like object, its entire contents will be
    read into a MemoryFile instance. It will almost always be better
    to use a path or URL, or the *opener* keyword argument.

    Examples
    --------
    To open a local GeoTIFF dataset for reading using standard driver
    discovery and no directives:

    >>> import rasterio
    >>> with rasterio.open('example.tif') as dataset:
    ...     print(dataset.profile)

    To open a local JPEG2000 dataset using only the JP2OpenJPEG driver:

    >>> with rasterio.open(
    ...         'example.jp2', driver='JP2OpenJPEG') as dataset:
    ...     print(dataset.profile)

    To create a new 8-band, 16-bit unsigned, tiled, and LZW-compressed
    GeoTIFF with a global extent and 0.5 degree resolution:

    >>> from rasterio.transform import from_origin
    >>> with rasterio.open(
    ...         'example.tif', 'w', driver='GTiff', dtype='uint16',
    ...         width=720, height=360, count=8, crs='EPSG:4326',
    ...         transform=from_origin(-180.0, 90.0, 0.5, 0.5),
    ...         nodata=0, tiled=True, compress='lzw') as dataset:
    ...     dataset.write(...)
    """
    ...
@overload
def open(
    fp: _Fp,
    mode: str = "r",
    driver: str | Sequence[str] | None = None,
    width: int | None = None,
    height: int | None = None,
    count: int | None = None,
    crs: CRSInput | None = None,
    transform: Affine | None = None,
    dtype: DTypeLike | None = None,
    nodata: float | None = None,
    sharing: bool = False,
    thread_safe: bool = False,
    opener: _Opener | None = None,
    **kwargs: _OpenOption,
) -> DatasetReader | DatasetWriter:
    """
    Open a dataset for reading or writing.

    The dataset may be located in a local file, in a resource located by
    a URL, or contained within a stream of bytes. This function accepts
    different types of fp parameters. However, it is almost always best
    to pass a string that has a dataset name as its value. These are
    passed directly to GDAL protocol and format handlers. A path to
    a zipfile is more efficiently used by GDAL than a Python ZipFile
    object, for example.

    In read ('r') or read/write ('r+') mode, no keyword arguments are
    required: these attributes are supplied by the opened dataset.

    In write ('w' or 'w+') mode, the driver, width, height, count, and
    dtype keywords are strictly required.

    Parameters
    ----------
    fp : str, os.PathLike, file-like, or rasterio.io.MemoryFile
        A filename or URL, a file object opened in binary ('rb') mode,
        a Path object, or one of the rasterio classes that provides the
        dataset-opening interface (has an open method that returns
        a dataset). Use a string when possible: GDAL can more
        efficiently access a dataset if it opens it natively.
    mode : str, optional
        'r' (read, the default), 'r+' (read/write), 'w' (write), or
        'w+' (write/read).
    driver : str, optional
        A short format driver name (e.g. "GTiff" or "JPEG") or a list of
        such names (see GDAL docs at
        https://gdal.org/drivers/raster/index.html). In 'w' or 'w+' modes
        a single name is required. In 'r' or 'r+' modes the driver can
        usually be omitted. Registered drivers will be tried
        sequentially until a match is found. When multiple drivers are
        available for a format such as JPEG2000, one of them can be
        selected by using this keyword argument.
    width : int, optional
        The number of columns of the raster dataset. Required in 'w' or
        'w+' modes, it is ignored in 'r' or 'r+' modes.
    height : int, optional
        The number of rows of the raster dataset. Required in 'w' or
        'w+' modes, it is ignored in 'r' or 'r+' modes.
    count : int, optional
        The count of dataset bands. Required in 'w' or 'w+' modes, it is
        ignored in 'r' or 'r+' modes.
    crs : str, dict, or CRS, optional
        The coordinate reference system. Required in 'w' or 'w+' modes,
        it is ignored in 'r' or 'r+' modes.
    transform : affine.Affine, optional
        Affine transformation mapping the pixel space to geographic
        space. Required in 'w' or 'w+' modes, it is ignored in 'r' or
        'r+' modes.
    dtype : str or numpy.dtype, optional
        The data type for bands. For example: 'uint8' or
        `rasterio.uint16`. Required in 'w' or 'w+' modes, it is
        ignored in 'r' or 'r+' modes.
    nodata : int, float, or nan, optional
        Defines the pixel value to be interpreted as not valid data.
        Required in 'w' or 'w+' modes, it is ignored in 'r' or 'r+'
        modes.
    sharing : bool, optional
        To reduce overhead and prevent programs from running out of file
        descriptors, rasterio maintains a pool of shared low level
        dataset handles. If True this function will use a shared
        handle if one is available. Multithreaded programs must avoid
        sharing and should set *sharing* to False.
    thread_safe: bool, optional
        Open GDAL dataset in `thread safe mode <https://gdal.org/en/stable/user/multithreading.html>`__.
        For multithreaded read-only GDAL dataset operations (e.g. ``GDAL_NUM_THREADS``, `LIBERTIFF driver <https://gdal.org/en/stable/drivers/raster/libertiff.html#open-options>`__).
        Requires rasterio 1.5+ & GDAL 3.10+.
    opener : callable, optional
        A custom dataset opener which can serve GDAL's virtual
        filesystem machinery via Python file-like objects. The
        underlying file-like object is obtained by calling *opener* with
        (*fp*, *mode*) or (*fp*, *mode* + 'b') depending on the format
        driver's native mode. *opener* must return a Python file-like
        object that provides read, seek, tell, and close methods. Note:
        only one opener at a time per fp, mode pair is allowed.
    kwargs : optional
        These are passed to format drivers as directives for creating or
        interpreting datasets. For example: in 'w' or 'w+' modes
        a tiled=True keyword argument will direct the GeoTIFF format
        driver to create a tiled, rather than striped, TIFF.

    Returns
    -------
    :class:`rasterio.io.DatasetReader`
        If mode is 'r'.
    :class:`rasterio.io.DatasetWriter`
        If mode is 'r+', 'w', or 'w+'.

    Raises
    ------
    :class:`TypeError`
        If arguments are of the wrong Python type.
    :class:`rasterio.errors.RasterioIOError`
        If the dataset can not be opened. Such as when there is no
        dataset with the given name.
    :class:`rasterio.errors.DriverCapabilityError`
        If the detected format driver does not support the requested
        opening mode.

    Notes
    -----
    If *fp* is a is a file-like object, its entire contents will be
    read into a MemoryFile instance. It will almost always be better
    to use a path or URL, or the *opener* keyword argument.

    Examples
    --------
    To open a local GeoTIFF dataset for reading using standard driver
    discovery and no directives:

    >>> import rasterio
    >>> with rasterio.open('example.tif') as dataset:
    ...     print(dataset.profile)

    To open a local JPEG2000 dataset using only the JP2OpenJPEG driver:

    >>> with rasterio.open(
    ...         'example.jp2', driver='JP2OpenJPEG') as dataset:
    ...     print(dataset.profile)

    To create a new 8-band, 16-bit unsigned, tiled, and LZW-compressed
    GeoTIFF with a global extent and 0.5 degree resolution:

    >>> from rasterio.transform import from_origin
    >>> with rasterio.open(
    ...         'example.tif', 'w', driver='GTiff', dtype='uint16',
    ...         width=720, height=360, count=8, crs='EPSG:4326',
    ...         transform=from_origin(-180.0, 90.0, 0.5, 0.5),
    ...         nodata=0, tiled=True, compress='lzw') as dataset:
    ...     dataset.write(...)
    """
    ...

class Band(NamedTuple):
    """
    Band(s) of a Dataset.

    Parameters
    ----------
    ds: dataset object
        An opened rasterio dataset object.
    bidx: int or sequence of ints
        Band number(s), index starting at 1.
    dtype: str
        rasterio data type of the data.
    shape: tuple
        Width, height of band.
    """
    ds: AnyDataset
    bidx: int | Sequence[int]
    dtype: str
    shape: tuple[int, ...]

def band(ds: AnyDataset, bidx: int | Sequence[int]) -> Band:
    """
    A dataset and one or more of its bands

    Parameters
    ----------
    ds: dataset object
        An opened rasterio dataset object.
    bidx: int or sequence of ints
        Band number(s), index starting at 1.

    Returns
    -------
    Band
    """
    ...

# `mode` and `**kwargs` mirror `numpy.pad`'s signature; see numpy.pad documentation.
def pad(
    array: NDArray[Any], transform: Affine, pad_width: int, mode: str | Callable[..., Any] | None = None, **kwargs: Any
) -> tuple[NDArray[Any], Affine]:
    """
    pad array and adjust affine transform matrix.

    Parameters
    ----------
    array: numpy.ndarray
        Numpy ndarray, for best results a 2D array
    transform: Affine transform
        transform object mapping pixel space to coordinates
    pad_width: int
        number of pixels to pad array on all four
    mode: str or function
        define the method for determining padded values

    Returns
    -------
    (array, transform): tuple
        Tuple of new array and affine transform

    Notes
    -----
    See :func:`numpy.pad` for details on mode and other kwargs.
    """
    ...

"""Numpy-free base classes."""

import logging
import os
from collections.abc import Iterable, Sequence
from types import TracebackType
from typing import Any, Final
from typing_extensions import Self, deprecated

from rasterio._affine_types import Affine
from rasterio._path import _ParsedPath, _UnparsedPath
from rasterio._typing import Colormap, CRSInput, _OpenOption
from rasterio.control import GroundControlPoint
from rasterio.coords import BoundingBox
from rasterio.crs import CRS
from rasterio.enums import ColorInterp, Compression, Interleaving, MaskFlags, PhotometricInterp
from rasterio.profiles import Profile
from rasterio.rpc import RPC
from rasterio.windows import Window

log: Final[logging.Logger]

def get_dataset_driver(path: str) -> str:
    """
    Get the name of the driver that opens a dataset.

    Parameters
    ----------
    path : rasterio.path.Path or str
        A remote or local dataset path.

    Returns
    -------
    str
    """
    ...
def driver_supports_mode(drivername: str, creation_mode: str) -> bool:
    """Return True if the driver supports the mode"""
    ...
def driver_can_create(drivername: str) -> bool:
    """Return True if the driver has CREATE capability"""
    ...
def driver_can_create_copy(drivername: str) -> bool:
    """Return True if the driver has CREATE_COPY capability"""
    ...
def tastes_like_gdal(seq: Affine | Sequence[float]) -> bool:
    """Return True if `seq` matches the GDAL geotransform pattern."""
    ...
def _raster_driver_extensions() -> dict[str, str]:
    """Logic based on: https://github.com/rasterio/rasterio/issues/265#issuecomment-367044836"""
    ...
def _can_create_osr(crs: CRSInput) -> bool:
    """
    Evaluate if a valid OGRSpatialReference can be created from crs.

    Specifically, it must not be None or an empty dict or string.

    Parameters
    ----------
    crs: Source coordinate reference system, in rasterio dict format.

    Returns
    -------
    out: bool
        True if source coordinate reference appears valid.
    """
    ...
def _transform(
    src_crs: CRSInput, dst_crs: CRSInput, xs: Sequence[float], ys: Sequence[float], zs: Sequence[float] | None
) -> tuple[list[float], list[float], list[float]]:
    """Transform input arrays from src to dst CRS."""
    ...

class DatasetBase:
    """
    Dataset base class

    Attributes
    ----------
    block_shapes
    bounds
    closed
    colorinterp
    count
    crs
    descriptions
    files
    gcps
    rpcs
    indexes
    mask_flag_enums
    meta
    nodata
    nodatavals
    profile
    res
    subdatasets
    transform
    units
    compression : str
        Compression algorithm's short name
    driver : str
        Format driver used to open the dataset
    interleaving : str
        'pixel' or 'band'
    kwds : dict
        Stored creation option tags
    mode : str
        Access mode
    name : str
        Remote or local dataset name
    options : dict
        Copy of opening options
    photometric : str
        Photometric interpretation's short name
    """
    name: str
    mode: str
    options: dict[str, Any]
    width: int
    height: int
    shape: tuple[int, int]
    driver: str

    def __init__(
        self,
        path: str | os.PathLike[str] | _ParsedPath | _UnparsedPath | None = None,
        driver: str | Sequence[str] | None = None,
        sharing: bool = False,
        thread_safe: bool = False,
        **kwargs: _OpenOption,
    ) -> None:
        """
        Construct a new dataset

        Parameters
        ----------
        path : rasterio.path.Path or str
            Path of the local or remote dataset.
        driver : str or list of str
            A single driver name or a list of driver names to consider when
            opening the dataset.
        sharing : bool, optional
            Whether to share underlying GDAL dataset handles (default: False).
        thread_safe: bool, optional
            Open GDAL dataset in `thread safe mode <https://gdal.org/en/stable/user/multithreading.html>`__.
            For multithreaded read-only GDAL dataset operations (e.g. ``GDAL_NUM_THREADS``, `LIBERTIFF driver <https://gdal.org/en/stable/drivers/raster/libertiff.html#open-options>`__).
            Requires rasterio 1.5+ & GDAL 3.10+.
        kwargs : dict
            GDAL dataset opening options.

        Returns
        -------
        dataset
        """
        ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...
    def read_crs(self) -> CRS | None:
        """Return the GDAL dataset's stored CRS"""
        ...
    def read_transform(self) -> list[float]:
        """Return the stored GDAL GeoTransform"""
        ...
    def start(self) -> None:
        """Start the dataset's life cycle"""
        ...
    def stop(self) -> None:
        """Close the GDAL dataset handle"""
        ...
    def close(self) -> None:
        """Close the dataset and unwind attached exit stack."""
        ...
    @property
    def closed(self) -> bool:
        """
        Test if the dataset is closed

        Returns
        -------
        bool
        """
        ...
    @property
    def count(self) -> int:
        """
        The number of raster bands in the dataset

        Returns
        -------
        int
        """
        ...
    @property
    def indexes(self) -> tuple[int, ...]:
        """
        The 1-based indexes of each band in the dataset

        For a 3-band dataset, this property will be ``[1, 2, 3]``.

        Returns
        -------
        list of int
        """
        ...
    @property
    def dtypes(self) -> tuple[str, ...]:
        """
        The data types of each band in index order

        Returns
        -------
        list of str
        """
        ...
    @property
    def block_shapes(self) -> tuple[tuple[int, int], ...]:
        """
        An ordered list of block shapes for each bands

        Shapes are tuples and have the same ordering as the dataset's
        shape: (count of image rows, count of image columns).

        Returns
        -------
        list
        """
        ...
    def get_nodatavals(self) -> tuple[float | None, ...]: ...
    @property
    def nodatavals(self) -> tuple[float | None, ...]:
        """
        Nodata values for each band

        Notes
        -----
        This may not be set.

        Returns
        -------
        list of float
        """
        ...

    @property
    def nodata(self) -> float | None:
        """
        The dataset's single nodata value

        Notes
        -----
        May be set.

        Returns
        -------
        float
        """
        ...
    @nodata.setter
    def nodata(self, value: float | None) -> None:
        """
        The dataset's single nodata value

        Notes
        -----
        May be set.

        Returns
        -------
        float
        """
        ...

    @property
    def mask_flag_enums(self) -> tuple[list[MaskFlags], ...]:
        """
        Sets of flags describing the sources of band masks.

        Parameters
        ----------

        all_valid: There are no invalid pixels, all mask values will be
            255. When used this will normally be the only flag set.
        per_dataset: The mask band is shared between all bands on the
            dataset.
        alpha: The mask band is actually an alpha band and may have
            values other than 0 and 255.
        nodata: Indicates the mask is actually being generated from
            nodata values (mutually exclusive of "alpha").

        Returns
        -------
        list [, list*]
            One list of rasterio.enums.MaskFlags members per band.

        Examples
        --------

        For a 3 band dataset that has masks derived from nodata values:

        >>> dataset.mask_flag_enums
        ([<MaskFlags.nodata: 8>], [<MaskFlags.nodata: 8>], [<MaskFlags.nodata: 8>])
        >>> band1_flags = dataset.mask_flag_enums[0]
        >>> rasterio.enums.MaskFlags.nodata in band1_flags
        True
        >>> rasterio.enums.MaskFlags.alpha in band1_flags
        False
        """
        ...

    @property
    def crs(self) -> CRS:
        """
        The dataset's coordinate reference system

        In setting this property, the value may be a CRS object or an
        EPSG:nnnn or WKT string.

        Returns
        -------
        CRS
        """
        ...
    @crs.setter
    def crs(self, value: CRSInput) -> None:
        """
        The dataset's coordinate reference system

        In setting this property, the value may be a CRS object or an
        EPSG:nnnn or WKT string.

        Returns
        -------
        CRS
        """
        ...

    @property
    def descriptions(self) -> tuple[str | None, ...]:
        """
        Descriptions for each dataset band

        To set descriptions, one for each band is required.

        Returns
        -------
        tuple[str | None, ...]
        """
        ...
    @descriptions.setter
    def descriptions(self, value: Sequence[str | None]) -> None:
        """
        Descriptions for each dataset band

        To set descriptions, one for each band is required.

        Returns
        -------
        tuple[str | None, ...]
        """
        ...

    def write_transform(self, transform: Sequence[float]) -> None: ...

    @property
    def transform(self) -> Affine:
        """
        The dataset's georeferencing transformation matrix

        This transform maps pixel row/column coordinates to coordinates
        in the dataset's coordinate reference system.

        Returns
        -------
        Affine
        """
        ...
    @transform.setter
    def transform(self, value: Affine) -> None:
        """
        The dataset's georeferencing transformation matrix

        This transform maps pixel row/column coordinates to coordinates
        in the dataset's coordinate reference system.

        Returns
        -------
        Affine
        """
        ...

    @property
    def offsets(self) -> tuple[float, ...]:
        """
        Raster offset for each dataset band

        To set offsets, one for each band is required.

        Returns
        -------
        list of float
        """
        ...
    @offsets.setter
    def offsets(self, value: Sequence[float]) -> None:
        """
        Raster offset for each dataset band

        To set offsets, one for each band is required.

        Returns
        -------
        list of float
        """
        ...

    @property
    def scales(self) -> tuple[float, ...]:
        """
        Raster scale for each dataset band

        To set scales, one for each band is required.

        Returns
        -------
        list of float
        """
        ...
    @scales.setter
    def scales(self, value: Sequence[float]) -> None:
        """
        Raster scale for each dataset band

        To set scales, one for each band is required.

        Returns
        -------
        list of float
        """
        ...

    @property
    def units(self) -> tuple[str | None, ...]:
        """
        A list of str: one units string for each dataset band

        Possible values include 'meters' or 'degC'. See the Pint
        project for a suggested list of units.

        To set units, one for each band is required.

        Returns
        -------
        list of str
        """
        ...
    @units.setter
    def units(self, value: Sequence[str | None]) -> None:
        """
        A list of str: one units string for each dataset band

        Possible values include 'meters' or 'degC'. See the Pint
        project for a suggested list of units.

        To set units, one for each band is required.

        Returns
        -------
        list of str
        """
        ...

    def block_window(self, bidx: int, i: int, j: int) -> Window:
        """
        Returns the window for a particular block

        Parameters
        ----------
        bidx: int
            Band index, starting with 1.
        i: int
            Row index of the block, starting with 0.
        j: int
            Column index of the block, starting with 0.

        Returns
        -------
        Window
        """
        ...
    def block_size(self, bidx: int, i: int, j: int) -> int:
        """
        Returns the size in bytes of a particular block

        Only useful for TIFF formatted datasets.

        Parameters
        ----------
        bidx: int
            Band index, starting with 1.
        i: int
            Row index of the block, starting with 0.
        j: int
            Column index of the block, starting with 0.

        Returns
        -------
        int
        """
        ...
    def block_windows(self, bidx: int = 0) -> Iterable[tuple[tuple[int, int], Window]]:
        """
        Iterator over a band's blocks and their windows


        The primary use of this method is to obtain windows to pass to
        `read()` for highly efficient access to raster block data.

        The positional parameter `bidx` takes the index (starting at 1) of the
        desired band.  This iterator yields blocks "left to right" and "top to
        bottom" and is similar to Python's ``enumerate()`` in that the first
        element is the block index and the second is the dataset window.

        Blocks are built-in to a dataset and describe how pixels are grouped
        within each band and provide a mechanism for efficient I/O.  A window
        is a range of pixels within a single band defined by row start, row
        stop, column start, and column stop.  For example, ``((0, 2), (0, 2))``
        defines a ``2 x 2`` window at the upper left corner of a raster band.
        Blocks are referenced by an ``(i, j)`` tuple where ``(0, 0)`` would be
        a band's upper left block.

        Raster I/O is performed at the block level, so accessing a window
        spanning multiple rows in a striped raster requires reading each row.
        Accessing a ``2 x 2`` window at the center of a ``1800 x 3600`` image
        requires reading 2 rows, or 7200 pixels just to get the target 4.  The
        same image with internal ``256 x 256`` blocks would require reading at
        least 1 block (if the window entire window falls within a single block)
        and at most 4 blocks, or at least 512 pixels and at most 2048.

        Given an image that is ``512 x 512`` with blocks that are
        ``256 x 256``, its blocks and windows would look like::

            Blocks:

                    0       256     512
                  0 +--------+--------+
                    |        |        |
                    | (0, 0) | (0, 1) |
                    |        |        |
                256 +--------+--------+
                    |        |        |
                    | (1, 0) | (1, 1) |
                    |        |        |
                512 +--------+--------+


            Windows:

                UL: ((0, 256), (0, 256))
                UR: ((0, 256), (256, 512))
                LL: ((256, 512), (0, 256))
                LR: ((256, 512), (256, 512))


        Parameters
        ----------
        bidx : int, optional
            The band index (using 1-based indexing) from which to extract
            windows. A value less than 1 uses the first band if all bands have
            homogeneous windows and raises an exception otherwise.

        Yields
        ------
        block, window
        """
        ...
    @property
    def bounds(self) -> BoundingBox:
        """
        Returns the lower left and upper right bounds of the dataset
        in the units of its coordinate reference system.

        The returned value is a tuple:
        (lower left x, lower left y, upper right x, upper right y)
        """
        ...
    @property
    def res(self) -> tuple[float, float]:
        """
        Returns the (width, height) of pixels in the units of its
        coordinate reference system.
        """
        ...
    @property
    def meta(self) -> dict[str, Any]:
        """The basic metadata of this dataset."""
        ...
    @property
    def compression(self) -> Compression | None: ...
    @property
    def interleaving(self) -> Interleaving | None: ...
    @property
    def photometric(self) -> PhotometricInterp | None: ...
    @property
    @deprecated("DatasetBase.is_tiled will be removed in a future rasterio release; inspect block_shapes / profile directly.")
    def is_tiled(self) -> bool: ...
    @property
    def profile(self) -> Profile:
        """
        Basic metadata and creation options of this dataset.

        May be passed as keyword arguments to `rasterio.open()` to
        create a clone of this dataset.
        """
        ...
    def lnglat(self) -> tuple[float, float]:
        """
        Geographic coordinates of the dataset's center.

        Returns
        -------
        (longitude, latitude) of centroid.
        """
        ...
    def get_transform(self) -> list[float]:
        """Returns a GDAL geotransform in its native form."""
        ...
    @property
    def subdatasets(self) -> list[str]:
        """Sequence of subdatasets"""
        ...
    def tag_namespaces(self, bidx: int = 0) -> list[str]:
        """
        Get a list of the dataset's metadata domains.

        Returned items may be passed as `ns` to the tags method.

        Parameters
        ----------
        bidx int, optional
            Can be used to select a specific band, otherwise the
            dataset's general metadata domains are returned.

        Returns
        -------
        list of str
        """
        ...
    def tags(self, bidx: int = 0, ns: str | None = None) -> dict[str, str]:
        """
        Returns a dict containing copies of the dataset or band's
        tags.

        Tags are pairs of key and value strings. Tags belong to
        namespaces.  The standard namespaces are: default (None) and
        'IMAGE_STRUCTURE'.  Applications can create their own additional
        namespaces.

        The optional bidx argument can be used to select the tags of
        a specific band. The optional ns argument can be used to select
        a namespace other than the default.
        """
        ...
    def get_tag_item(self, ns: str, dm: str | None = None, bidx: int = 0, ovr: int | None = None) -> str | None:
        """
        Returns tag item value

        Parameters
        ----------
        ns: str
            The key for the metadata item to fetch.
        dm: str
            The domain to fetch for.
        bidx: int
            Band index, starting with 1.
        ovr: int
            Overview level

        Returns
        -------
        str
        """
        ...

    @property
    def colorinterp(self) -> tuple[ColorInterp, ...]:
        """
        A sequence of ``ColorInterp.<enum>`` in band order.

        Returns
        -------
        tuple
        """
        ...
    @colorinterp.setter
    def colorinterp(self, value: Sequence[ColorInterp]) -> None:
        """
        A sequence of ``ColorInterp.<enum>`` in band order.

        Returns
        -------
        tuple
        """
        ...

    def colormap(self, bidx: int) -> Colormap:
        """
        Returns a dict containing the colormap for a band.

        Parameters
        ----------
        bidx : int
            Index of the band whose colormap will be returned. Band index
            starts at 1.

        Returns
        -------
        dict
            Mapping of color index value (starting at 0) to RGBA color as a
            4-element tuple.

        Raises
        ------
        ValueError
            If no colormap is found for the specified band (NULL color table).
        IndexError
            If no band exists for the provided index.
        """
        ...
    def overviews(self, bidx: int) -> list[int]: ...
    def checksum(self, bidx: int, window: Window | None = None) -> int:
        """
        Compute an integer checksum for the stored band

        Parameters
        ----------
        bidx : int
            The band's index (1-indexed).
        window: tuple, optional
            A window of the band. Default is the entire extent of the band.

        Returns
        -------
        An int.
        """
        ...
    def get_gcps(self) -> tuple[list[GroundControlPoint], CRS]:
        """Get GCPs and their associated CRS."""
        ...

    @property
    def gcps(self) -> tuple[list[GroundControlPoint], CRS]:
        """
        ground control points and their coordinate reference system.

        This property is a 2-tuple, or pair: (gcps, crs).

        gcps : list of GroundControlPoint
            Zero or more ground control points.
        crs: CRS
            The coordinate reference system of the ground control points.
        """
        ...
    @gcps.setter
    def gcps(self, value: tuple[Sequence[GroundControlPoint], CRSInput]) -> None:
        """
        ground control points and their coordinate reference system.

        This property is a 2-tuple, or pair: (gcps, crs).

        gcps : list of GroundControlPoint
            Zero or more ground control points.
        crs: CRS
            The coordinate reference system of the ground control points.
        """
        ...

    @property
    def rpcs(self) -> RPC | None:
        """
        Rational polynomial coefficients mapping between pixel and geodetic coordinates.

        This property is a dict-like object.

        rpcs : RPC instance containing coefficients. Empty if dataset does not have any
        metadata in the "RPC" domain.
        """
        ...
    @rpcs.setter
    def rpcs(self, value: RPC | None) -> None:
        """
        Rational polynomial coefficients mapping between pixel and geodetic coordinates.

        This property is a dict-like object.

        rpcs : RPC instance containing coefficients. Empty if dataset does not have any
        metadata in the "RPC" domain.
        """
        ...

    @property
    def files(self) -> list[str]:
        """
        Returns a sequence of files associated with the dataset.

        Returns
        -------
        tuple
        """
        ...

_GDAL_AT_LEAST_3_10: Final[bool]

complex64: Final[str]
complex128: Final[str]
complex_int16: Final[str]
float32: Final[str]
float64: Final[str]
int16: Final[str]

def _parse_path(path: str) -> _ParsedPath | _UnparsedPath:
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

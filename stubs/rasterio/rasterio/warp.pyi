"""Raster warping and reprojection."""

from _typeshed import Incomplete
from collections.abc import Mapping, Sequence
from typing import Any, Final, TypeAlias, overload
from typing_extensions import deprecated

from numpy.typing import ArrayLike, NDArray
from rasterio._affine_types import Affine
from rasterio._typing import CRSInput, _GDALOption
from rasterio.control import GroundControlPoint
from rasterio.enums import Resampling
from rasterio.rpc import RPC

_Resolution: TypeAlias = tuple[float, float] | float
_Gcps: TypeAlias = Sequence[GroundControlPoint]
_Rpcs: TypeAlias = RPC | Mapping[str, Any]

SUPPORTED_RESAMPLING: Final[list[Resampling]]

def transform(
    src_crs: CRSInput, dst_crs: CRSInput, xs: ArrayLike, ys: ArrayLike, zs: ArrayLike | None = None
) -> tuple[list[float], list[float]] | tuple[list[float], list[float], list[float]]:
    """
    Transform vectors from source to target coordinate reference system.

    Transform vectors of x, y and optionally z from source
    coordinate reference system into target.

    Parameters
    ------------
    src_crs: CRS or dict
        Source coordinate reference system, as a rasterio CRS object.
        Example: CRS({'init': 'EPSG:4326'})
    dst_crs: CRS or dict
        Target coordinate reference system.
    xs: array_like
        Contains x values.  Will be cast to double floating point values.
    ys:  array_like
        Contains y values.
    zs: array_like, optional
        Contains z values.  Assumed to be all 0 if absent.

    Returns
    ---------
    out: tuple of array_like, (xs, ys, [zs])
        Tuple of x, y, and optionally z vectors, transformed into the target
        coordinate reference system.
    """
    ...

@overload
def transform_geom(
    src_crs: CRSInput, dst_crs: CRSInput, geom: Mapping[str, Any] | Sequence[Mapping[str, Any]], *, precision: float = -1
) -> dict[str, Any] | list[dict[str, Any]]:
    """
    Transform geometry from source coordinate reference system into target.

    Parameters
    ------------
    src_crs: CRS or dict
        Source coordinate reference system, in rasterio dict format.
        Example: CRS({'init': 'EPSG:4326'})
    dst_crs: CRS or dict
        Target coordinate reference system.
    geom: GeoJSON like dict object or iterable of GeoJSON like objects.
    antimeridian_cutting: bool
        DEPRECATED: Always enabled since GDAL 2.2.
    antimeridian_offset: float
        DEPRECATED: No longer has any effect since GDAL 2.2.
    precision: float
        If >= 0, geometry coordinates will be rounded to this number of decimal
        places after the transform operation, otherwise original coordinate
        values will be preserved (default).

    Returns
    ---------
    out: GeoJSON like dict object or list of GeoJSON like objects.
        Transformed geometry(s) in GeoJSON dict format
    """
    ...
@overload
@deprecated(
    "`antimeridian_cutting` and `antimeridian_offset` are no-ops since GDAL 2.2 "
    "and will be removed in a future rasterio release. Call transform_geom "
    "without them."
)
def transform_geom(
    src_crs: CRSInput,
    dst_crs: CRSInput,
    geom: Mapping[str, Any] | Sequence[Mapping[str, Any]],
    antimeridian_cutting: bool | None = None,
    antimeridian_offset: float | None = None,
    precision: float = -1,
) -> dict[str, Any] | list[dict[str, Any]]:
    """
    Transform geometry from source coordinate reference system into target.

    Parameters
    ------------
    src_crs: CRS or dict
        Source coordinate reference system, in rasterio dict format.
        Example: CRS({'init': 'EPSG:4326'})
    dst_crs: CRS or dict
        Target coordinate reference system.
    geom: GeoJSON like dict object or iterable of GeoJSON like objects.
    antimeridian_cutting: bool
        DEPRECATED: Always enabled since GDAL 2.2.
    antimeridian_offset: float
        DEPRECATED: No longer has any effect since GDAL 2.2.
    precision: float
        If >= 0, geometry coordinates will be rounded to this number of decimal
        places after the transform operation, otherwise original coordinate
        values will be preserved (default).

    Returns
    ---------
    out: GeoJSON like dict object or list of GeoJSON like objects.
        Transformed geometry(s) in GeoJSON dict format
    """
    ...

def transform_bounds(
    src_crs: CRSInput, dst_crs: CRSInput, left: float, bottom: float, right: float, top: float, densify_pts: int = 21
) -> tuple[float, float, float, float]:
    """
    Transform bounds from src_crs to dst_crs.

    Optionally densifying the edges (to account for nonlinear transformations
    along these edges) and extracting the outermost bounds.

    Note: antimeridian support added in version 1.3.0

    Parameters
    ----------
    src_crs: CRS or dict
        Source coordinate reference system, in rasterio dict format.
        Example: CRS({'init': 'EPSG:4326'})
    dst_crs: CRS or dict
        Target coordinate reference system.
    left, bottom, right, top: float
        Bounding coordinates in src_crs, from the bounds property of a raster.
    densify_pts: uint, optional
        Number of points to add to each edge to account for nonlinear
        edges produced by the transform process.  Large numbers will produce
        worse performance.  Default: 21 (gdal default).

    Returns
    -------
    left, bottom, right, top: float
        Outermost coordinates in target coordinate reference system.
    """
    ...
def reproject(
    source: ArrayLike | Incomplete,
    destination: ArrayLike | Incomplete | None = None,
    src_transform: Affine | None = None,
    gcps: _Gcps | None = None,
    rpcs: _Rpcs | None = None,
    src_crs: CRSInput | None = None,
    src_nodata: float | None = None,
    dst_transform: Affine | None = None,
    dst_crs: CRSInput | None = None,
    dst_nodata: float | None = None,
    dst_resolution: _Resolution | None = None,
    src_alpha: int = 0,
    dst_alpha: int = 0,
    masked: bool = False,
    resampling: Resampling = ...,
    num_threads: int = 1,
    init_dest_nodata: bool = True,
    warp_mem_limit: int = 0,
    src_geoloc_array: NDArray[Any] | None = None,
    **kwargs: _GDALOption,
) -> tuple[NDArray[Any], Affine]:
    """
    Reproject a source raster to a destination raster.

    If the source and destination are ndarrays, coordinate reference
    system definitions and geolocation parameters are required for
    reprojection. Only one of src_transform, gcps, rpcs, or
    src_geoloc_array can be used.

    If the source and destination are rasterio Bands, shorthand for
    bands of datasets on disk, the coordinate reference systems and
    transforms will be read from the appropriate datasets.

    Parameters
    ------------
    source: ndarray or Band
        The source is a 2 or 3-D ndarray, or a single or a multiple
        Rasterio Band object. The dimensionality of source
        and destination must match, i.e., for multiband reprojection
        the lengths of the first axes of the source and destination
        must be the same.
    destination: ndarray or Band, optional
        The destination is a 2 or 3-D ndarray, or a single or a multiple
        Rasterio Band object. The dimensionality of source
        and destination must match, i.e., for multiband reprojection
        the lengths of the first axes of the source and destination
        must be the same.
    src_transform: affine.Affine(), optional
        Source affine transformation. Required if source and
        destination are ndarrays. Will be derived from source if it is
        a rasterio Band. An error will be raised if this parameter is
        defined together with gcps.
    gcps: sequence of GroundControlPoint, optional
        Ground control points for the source. An error will be raised
        if this parameter is defined together with src_transform or rpcs.
    rpcs: RPC or dict, optional
        Rational polynomial coefficients for the source. An error will
        be raised if this parameter is defined together with src_transform
        or gcps.
    src_geoloc_array : array-like, optional
        A pair of 2D arrays holding x and y coordinates, like
        a dense array of ground control points that may be used in place
        of src_transform.
    src_crs: CRS or dict, optional
        Source coordinate reference system, in rasterio dict format.
        Required if source and destination are ndarrays.
        Will be derived from source if it is a rasterio Band.
        Example: CRS({'init': 'EPSG:4326'})
    src_nodata: int or float, optional
        The source nodata value. Pixels with this value will not be
        used for interpolation. If not set, it will default to the
        nodata value of the source image if a masked ndarray or
        rasterio band, if available.
    dst_transform: affine.Affine(), optional
        Target affine transformation. Required if source and
        destination are ndarrays. Will be derived from target if it is
        a rasterio Band.
    dst_crs: CRS or dict, optional
        Target coordinate reference system. Required if source and
        destination are ndarrays. Will be derived from target if it
        is a rasterio Band.
    dst_nodata: int or float, optional
        The nodata value used to initialize the destination; it will
        remain in all areas not covered by the reprojected source.
        Defaults to the nodata value of the destination image (if set),
        the value of src_nodata, or 0 (GDAL default).
    dst_resolution: tuple (x resolution, y resolution) or float, optional
        Target resolution, in units of target coordinate reference
        system.
    src_alpha : int, optional
        Index of a band to use as the alpha band when warping.
    dst_alpha : int, optional
        Index of a band to use as the alpha band when warping.
    masked: bool, optional
        If True and destination is None, return a masked array.
    resampling: int, rasterio.enums.Resampling
        Resampling method to use.
        Default is :attr:`rasterio.enums.Resampling.nearest`.
        An exception will be raised for a method not supported by the running
        version of GDAL.
    num_threads : int, optional
        The number of warp worker threads. Default: 1.
    init_dest_nodata: bool
        Flag to specify initialization of nodata in destination;
        prevents overwrite of previous warps. Defaults to True.
    warp_mem_limit : int, optional
        The warp operation memory limit in MB. Larger values allow the
        warp operation to be carried out in fewer chunks. The amount of
        memory required to warp a 3-band uint8 2000 row x 2000 col
        raster to a destination of the same size is approximately
        56 MB. The default (0) means 64 MB with GDAL 2.2.
    kwargs:  dict, optional
        Additional arguments passed to both the image to image
        transformer :cpp:func:`GDALCreateGenImgProjTransformer2` (for example,
        MAX_GCP_ORDER=2) and the :cpp:struct:`GDALWarpOptions` (for example,
        INIT_DEST=NO_DATA).

    Returns
    ---------
    destination: ndarray or Band
        The transformed ndarray or Band.
    dst_transform: Affine
        The affine transformation matrix of the destination.
    """
    ...
def aligned_target(transform: Affine, width: int, height: int, resolution: _Resolution) -> tuple[Affine, int, int]:
    """
    Aligns target to specified resolution

    Parameters
    ----------
    transform : Affine
        Input affine transformation matrix
    width, height: int
        Input dimensions
    resolution: tuple (x resolution, y resolution) or float
        Target resolution, in units of target coordinate reference
        system.

    Returns
    -------
    transform: Affine
        Output affine transformation matrix
    width, height: int
        Output dimensions
    """
    ...
def calculate_default_transform(
    src_crs: CRSInput,
    dst_crs: CRSInput,
    width: int,
    height: int,
    left: float | None = None,
    bottom: float | None = None,
    right: float | None = None,
    top: float | None = None,
    gcps: _Gcps | None = None,
    rpcs: _Rpcs | None = None,
    resolution: _Resolution | None = None,
    dst_width: int | None = None,
    dst_height: int | None = None,
    src_geoloc_array: NDArray[Any] | None = None,
    **kwargs: _GDALOption,
) -> tuple[Affine, int, int]:
    """
    Computes the default dimensions and transform for a reprojection.

    Destination width and height (and resolution if not provided), are
    calculated using GDAL's method for suggest warp output.  The
    destination transform is anchored at the left, top coordinate.

    Source georeferencing can be specified using either ground control
    points (GCPs), rational polynomial coefficients (RPCs), geolocation
    arrays, or spatial bounds (left, bottom, right, top). These forms of
    georeferencing are mutually exclusive.

    Source and destination coordinate reference systems and source
    width and height are the first four, required, parameters.

    Parameters
    ----------
    src_crs : CRS or dict
        Source coordinate reference system, in rasterio dict format.
        Example: CRS({'init': 'EPSG:4326'})
    dst_crs : CRS or dict
        Target coordinate reference system.
    width, height : int
        Source raster width and height.
    left, bottom, right, top : float, optional
        Bounding coordinates in src_crs, from the bounds property of a
        raster. Required unless using gcps.
    gcps : sequence of GroundControlPoint, optional
        Instead of a bounding box for the source, a sequence of ground
        control points may be provided.
    rpcs : RPC or dict, optional
        Instead of a bounding box for the source, rational polynomial
        coefficients may be provided.
    src_geoloc_array : array-like, optional
        A pair of 2D arrays holding x and y coordinates, like a like
        a dense array of ground control points that may be used in place
        of src_transform.
    resolution : tuple (x resolution, y resolution) or float, optional
        Target resolution, in units of target coordinate reference
        system.
    dst_width, dst_height : int, optional
        Output file size in pixels and lines. Cannot be used together
        with resolution.
    kwargs :  dict, optional
        Additional arguments passed to transformation function.

    Returns
    -------
    transform: Affine
        Output affine transformation matrix
    width, height: int
        Output dimensions

    Notes
    -----
    Some behavior of this function is determined by the
    CHECK_WITH_INVERT_PROJ environment variable:

        YES
            constrain output raster to extents that can be inverted
            avoids visual artifacts and coordinate discontinuties.
        NO
            reproject coordinates beyond valid bound limits
    """
    ...

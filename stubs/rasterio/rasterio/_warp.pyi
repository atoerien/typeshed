"""Raster and vector warping and reprojection."""

from collections.abc import Mapping, Sequence
from typing import Any, Final

from numpy.typing import DTypeLike, NDArray
from rasterio._affine_types import Affine
from rasterio._io import DatasetReaderBase
from rasterio._typing import CRSInput, Indexes, ShapeND, WindowInput, _GDALOption, _NestedScalar
from rasterio.control import GroundControlPoint
from rasterio.crs import CRS
from rasterio.enums import Resampling
from rasterio.io import DatasetReader
from rasterio.rpc import RPC

SUPPORTED_RESAMPLING: Final[list[Resampling]]
DEFAULT_NODATA_FLAG: Final[object]

def recursive_round(val: _NestedScalar, precision: int) -> _NestedScalar:
    """Recursively round coordinates."""
    ...
def _transform_geom(
    src_crs: CRSInput, dst_crs: CRSInput, geom: Mapping[str, Any] | Sequence[Mapping[str, Any]], precision: int
) -> dict[str, Any] | list[dict[str, Any]]:
    """Return a transformed geometry."""
    ...
def _reproject(
    source: NDArray[Any] | Any,
    destination: NDArray[Any] | Any,
    src_transform: Affine | None = None,
    gcps: Sequence[GroundControlPoint] | None = None,
    rpcs: RPC | None = None,
    src_crs: CRSInput | None = None,
    src_nodata: float | None = None,
    dst_transform: Affine | None = None,
    dst_crs: CRSInput | None = None,
    dst_nodata: float | None = None,
    dst_alpha: int = 0,
    src_alpha: int = 0,
    resampling: Resampling = ...,
    init_dest_nodata: bool = True,
    tolerance: float = 0.125,
    num_threads: int = 1,
    warp_mem_limit: int = 0,
    working_data_type: int = 0,
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
    source : ndarray or rasterio Band
        Source raster.
    destination : ndarray or rasterio Band
        Target raster.
    src_transform : affine.Affine(), optional
        Source affine transformation.  Required if source and destination
        are ndarrays.  Will be derived from source if it is a rasterio Band.
    gcps : sequence of `GroundControlPoint` instances, optional
        Ground control points for the source. May be used in place of
        src_transform.
    rpcs : RPC or dict, optional
        Rational polynomial coefficients for the source. May be used
        in place of src_transform.
    src_geoloc_array : array-like, optional
        A pair of 2D arrays holding x and y coordinates, like a like
        a dense array of ground control points that may be used in place
        of src_transform.
    src_crs : dict, optional
        Source coordinate reference system, in rasterio dict format.
        Required if source and destination are ndarrays.  Will be
        derived from source if it is a rasterio Band.  Example:
        'EPSG:4326'.
    src_nodata : int or float, optional
        The source nodata value.  Pixels with this value will not be used
        for interpolation.  If not set, it will be default to the
        nodata value of the source image if a masked ndarray or rasterio band,
        if available.
    dst_transform : affine.Affine(), optional
        Target affine transformation.  Required if source and destination
        are ndarrays.  Will be derived from target if it is a rasterio Band.
    dst_crs : dict, optional
        Target coordinate reference system.  Required if source and destination
        are ndarrays.  Will be derived from target if it is a rasterio Band.
    dst_nodata : int or float, optional
        The nodata value used to initialize the destination; it will remain
        in all areas not covered by the reprojected source.  Defaults to the
        nodata value of the destination image (if set), the value of
        src_nodata, or 0 (gdal default).
    src_alpha : int, optional
        Index of a band to use as the source alpha band when warping.
    dst_alpha : int, optional
        Index of a band to use as the destination alpha band when warping.
    resampling : int
        Resampling method to use.  One of the following:
            Resampling.nearest,
            Resampling.bilinear,
            Resampling.cubic,
            Resampling.cubic_spline,
            Resampling.lanczos,
            Resampling.average,
            Resampling.mode
    init_dest_nodata : bool
        Flag to specify initialization of nodata in destination;
        prevents overwrite of previous warps. Defaults to True.
    tolerance : float, optional
        The maximum error tolerance in input pixels when
        approximating the warp transformation. Default: 0.125,
        or one-eigth of a pixel.
    num_threads : int
        Number of worker threads.
    warp_mem_limit : int, optional
        The warp operation memory limit in MB. Larger values allow the
        warp operation to be carried out in fewer chunks. The amount of
        memory required to warp a 3-band uint8 2000 row x 2000 col
        raster to a destination of the same size is approximately
        56 MB. The default (0) means 64 MB with GDAL 2.2.
        The warp operation's memory limit in MB. The default (0)
        means 64 MB with GDAL 2.2.
    kwargs :  dict, optional
        Additional arguments passed to both the image to image
        transformer GDALCreateGenImgProjTransformer2() (for example,
        MAX_GCP_ORDER=2) and to the Warper (for example,
        INIT_DEST=NO_DATA).

    Returns
    ---------
    out : None
        Output is written to destination.
    """
    ...
def _calculate_default_transform(
    src_crs: CRSInput,
    dst_crs: CRSInput,
    width: int,
    height: int,
    left: float | None = None,
    bottom: float | None = None,
    right: float | None = None,
    top: float | None = None,
    gcps: Sequence[GroundControlPoint] | None = None,
    rpcs: RPC | None = None,
    src_geoloc_array: NDArray[Any] | None = None,
    **kwargs: _GDALOption,
) -> tuple[Affine, int, int]:
    """Wraps GDAL's algorithm."""
    ...
def _transform_bounds(
    src_crs: CRS, dst_crs: CRS, left: float, bottom: float, right: float, top: float, densify_pts: int
) -> tuple[float, float, float, float]: ...
def _suggested_proxy_vrt_doc(
    width: int,
    height: int,
    transform: Affine | None = None,
    crs: CRSInput | None = None,
    gcps: Sequence[GroundControlPoint] | None = None,
    rpcs: RPC | None = None,
) -> str:
    """Make a VRT XML document to serve _calculate_default_transform."""
    ...

class WarpedVRTReaderBase(DatasetReaderBase):
    src_dataset: DatasetReader
    src_crs: CRS
    src_transform: Affine | None
    resampling: Resampling
    tolerance: float
    src_nodata: float | None
    dst_nodata: float | None
    working_dtype: DTypeLike | None
    warp_extras: dict[str, _GDALOption]

    def __init__(
        self,
        src_dataset: DatasetReader,
        src_crs: CRSInput | None = None,
        crs: CRSInput | None = None,
        resampling: Resampling = ...,
        tolerance: float = 0.125,
        src_nodata: float | None = ...,
        nodata: float | None = ...,
        width: int | None = None,
        height: int | None = None,
        src_transform: Affine | None = None,
        transform: Affine | None = None,
        init_dest_nodata: bool = True,
        src_alpha: int = 0,
        dst_alpha: int = 0,
        add_alpha: bool = False,
        warp_mem_limit: int = 0,
        dtype: DTypeLike | None = None,
        **warp_extras: _GDALOption,
    ) -> None:
        """
        Make a virtual warped dataset

        Parameters
        ----------
        src_dataset : dataset object
            The warp source dataset. Must be opened in "r" mode.
        src_crs : CRS or str, optional
            Overrides the coordinate reference system of `src_dataset`.
        src_transfrom : Affine, optional
            Overrides the transform of `src_dataset`.
        src_nodata : float, optional
            Overrides the nodata value of `src_dataset`, which is the
            default.
        crs : CRS or str, optional
            The coordinate reference system at the end of the warp
            operation.  Default: the crs of `src_dataset`. dst_crs was
            a deprecated alias for this parameter.
        transform : Affine, optional
            The transform for the virtual dataset. Default: will be
            computed from the attributes of `src_dataset`. dst_transform
            was a deprecated alias for this parameter.
        height, width: int, optional
            The dimensions of the virtual dataset. Defaults: will be
            computed from the attributes of `src_dataset`. dst_height
            and dst_width were deprecated alias for these parameters.
        nodata : float, optional
            Nodata value for the virtual dataset. Default: the nodata
            value of `src_dataset` or 0.0. dst_nodata was a deprecated
            alias for this parameter.
        resampling : Resampling, optional
            Warp resampling algorithm. Default: `Resampling.nearest`.
        tolerance : float, optional
            The maximum error tolerance in input pixels when
            approximating the warp transformation. Default: 0.125,
            or one-eigth of a pixel.
        src_alpha : int, optional
            Index of a source band to use as an alpha band for warping.
        dst_alpha : int, optional
            Index of a destination band to use as an alpha band for warping.
        add_alpha : bool, optional
            Whether to add an alpha masking band to the virtual dataset.
            Default: False. This option will cause deletion of the VRT
            nodata value.
        init_dest_nodata : bool, optional
            Whether or not to initialize output to `nodata`. Default:
            True.
        warp_mem_limit : int, optional
            The warp operation's memory limit in MB. The default (0)
            means 64 MB with GDAL 2.2.
        dtype : str, optional
            The working data type for warp operation and output.
        warp_extras : dict, optional
            GDAL extra warp options. See:
            https://gdal.org/doxygen/structGDALWarpOptions.html.
            Also, GDALCreateGenImgProjTransformer2() options.
            Requires rasterio 1.3+, GDAL 3.2+. See:
            https://gdal.org/doxygen/gdal__alg_8h.html#a94cd172f78dbc41d6f407d662914f2e3

        Returns
        -------
        WarpedVRT
        """
        ...
    def read(  # type: ignore[override]
        self,
        indexes: Indexes | None = None,
        out: NDArray[Any] | None = None,
        window: WindowInput | None = None,
        masked: bool = False,
        out_shape: ShapeND | None = None,
        resampling: Resampling = ...,
        fill_value: float | None = None,
        out_dtype: DTypeLike | None = None,
        # Swallows the deprecated `boundless` kwarg (raises ValueError if True).
        **kwargs: bool,
    ) -> NDArray[Any]:
        """
        Read a dataset's raw pixels as an N-d array

        This data is read from the dataset's band cache, which means
        that repeated reads of the same windows may avoid I/O.

        Parameters
        ----------
        indexes : list of ints or a single int, optional
            If `indexes` is a list, the result is a 3D array, but is
            a 2D array if it is a band index number.

        out : numpy.ndarray, optional
            As with Numpy ufuncs, this is an optional reference to an
            output array into which data will be placed. If the height
            and width of `out` differ from that of the specified
            window (see below), the raster image will be decimated or
            replicated using the specified resampling method (also see
            below).

            *Note*: the method's return value may be a view on this
            array. In other words, `out` is likely to be an
            incomplete representation of the method's results.

            This parameter cannot be combined with `out_shape`.

        out_dtype : str or numpy.dtype
            The desired output data type. For example: 'uint8' or
            rasterio.uint16.

        out_shape : tuple, optional
            A tuple describing the shape of a new output array. See
            `out` (above) for notes on image decimation and
            replication.

            Cannot combined with `out`.

        window : a pair (tuple) of pairs of ints or Window, optional
            The optional `window` argument is a 2 item tuple. The first
            item is a tuple containing the indexes of the rows at which
            the window starts and stops and the second is a tuple
            containing the indexes of the columns at which the window
            starts and stops. For example, ((0, 2), (0, 2)) defines
            a 2x2 window at the upper left of the raster dataset.

        masked : bool, optional
            If `masked` is `True` the return value will be a masked
            array. Otherwise (the default) the return value will be a
            regular array. Masks will be exactly the inverse of the
            GDAL RFC 15 conforming arrays returned by read_masks().

        resampling : Resampling
            By default, pixel values are read raw or interpolated using
            a nearest neighbor algorithm from the band cache. Other
            resampling algorithms may be specified. Resampled pixels
            are not cached.

        fill_value : scalar
            Fill value applied in the `boundless=True` case only.

        kwargs : dict
            This is only for backwards compatibility. No keyword arguments
            are supported other than the ones named above.

        Returns
        -------
        numpy.ndarray or a view on a numpy.ndarray

        Note: as with Numpy ufuncs, an object is returned even if you
        use the optional `out` argument and the return value shall be
        preferentially used by callers.
        """
        ...
    def read_masks(  # type: ignore[override]
        self,
        indexes: Indexes | None = None,
        out: NDArray[Any] | None = None,
        out_shape: ShapeND | None = None,
        window: WindowInput | None = None,
        resampling: Resampling = ...,
        # Swallows the deprecated `boundless` kwarg (raises ValueError if True).
        **kwargs: bool,
    ) -> NDArray[Any]:
        """Read raster band masks as a multidimensional array"""
        ...

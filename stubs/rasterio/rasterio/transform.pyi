"""Geospatial transforms"""

from collections.abc import Callable, Sequence
from typing import Final, Literal, TypeAlias, overload
from typing_extensions import Self, deprecated

from rasterio._affine_types import Affine as Affine
from rasterio._transform import GCPTransformerBase, RPCTransformerBase
from rasterio._typing import _GDALOption
from rasterio.control import GroundControlPoint
from rasterio.enums import TransformDirection as TransformDirection, TransformMethod as TransformMethod
from rasterio.errors import RasterioDeprecationWarning as RasterioDeprecationWarning
from rasterio.rpc import RPC

_Sextuple: TypeAlias = tuple[float, float, float, float, float, float]
_OffsetOptions: TypeAlias = Literal["center", "ul", "ur", "ll", "lr"]
_RoundOperation: TypeAlias = Callable[[float], int]

IDENTITY: Final[Affine]
GDAL_IDENTITY: Final[_Sextuple]

class TransformMethodsMixin:
    """
    Mixin providing methods for calculations related
    to transforming between rows and columns of the raster
    array and the coordinates.

    These methods are wrappers for the functionality in
    `rasterio.transform` module.

    A subclass with this mixin MUST provide a `transform`
    property.
    """
    def xy(
        self,
        row: int | Sequence[int],
        col: int | Sequence[int],
        z: float | Sequence[float] | None = None,
        offset: _OffsetOptions = "center",
        transform_method: TransformMethod = ...,
        **rpc_options: _GDALOption,
    ) -> tuple[float, float] | tuple[list[float], list[float]]:
        """
        Get the coordinates x, y of a pixel at row, col.

        The pixel's center is returned by default, but a corner can be returned
        by setting `offset` to one of `ul, ur, ll, lr`.

        Parameters
        ----------
        row : int
            Pixel row.
        col : int
            Pixel column.
        z : float, optional
            Height associated with coordinates. Primarily used for RPC based
            coordinate transformations. Ignored for affine based
            transformations. Default: 0.
        offset : str, optional
            Determines if the returned coordinates are for the center of the
            pixel or for a corner.
        transform_method: TransformMethod, optional
            The coordinate transformation method. Default: `TransformMethod.affine`.
        rpc_options: dict, optional
            Additional arguments passed to GDALCreateRPCTransformer

        Returns
        -------
        tuple
            x, y
        """
        ...
    def index(
        self,
        x: float | Sequence[float],
        y: float | Sequence[float],
        z: float | Sequence[float] | None = None,
        op: _RoundOperation | None = None,
        precision: int | None = None,
        transform_method: TransformMethod = ...,
        **rpc_options: _GDALOption,
    ) -> tuple[int, int] | tuple[list[int], list[int]]:
        """
        Get the (row, col) index of the pixel containing (x, y).

        Parameters
        ----------
        x : float
            x value in coordinate reference system
        y : float
            y value in coordinate reference system
        z : float, optional
            Height associated with coordinates. Primarily used for RPC
            based coordinate transformations. Ignored for affine based
            transformations. Default: 0.
        op : function, optional (default: numpy.floor)
            Function to convert fractional pixels to whole numbers
            (floor, ceiling, round)
        transform_method: TransformMethod, optional
            The coordinate transformation method. Default:
            `TransformMethod.affine`.
        rpc_options: dict, optional
            Additional arguments passed to GDALCreateRPCTransformer
        precision : int, optional
            This parameter is unused, deprecated in rasterio 1.3.0, and
            will be removed in version 2.0.0.

        Returns
        -------
        tuple: int, int
            (row index, col index)
        """
        ...

def tastes_like_gdal(seq: Affine | _Sextuple) -> bool:
    """Return True if `seq` matches the GDAL geotransform pattern."""
    ...
def guard_transform(transform: Affine | _Sextuple) -> Affine:
    """Return an Affine transformation instance."""
    ...
def from_origin(west: float, north: float, xsize: float, ysize: float) -> Affine:
    """
    Return an Affine transformation given upper left and pixel sizes.

    Return an Affine transformation for a georeferenced raster given
    the coordinates of its upper left corner `west`, `north` and pixel
    sizes `xsize`, `ysize`.
    """
    ...
def from_bounds(west: float, south: float, east: float, north: float, width: float, height: float) -> Affine:
    """
    Return an Affine transformation given bounds, width and height.

    Return an Affine transformation for a georeferenced raster given
    its bounds `west`, `south`, `east`, `north` and its `width` and
    `height` in number of pixels.
    """
    ...
def array_bounds(height: int, width: int, transform: Affine) -> tuple[float, float, float, float]:
    """
    Return the bounds of an array given height, width, and a transform.

    Return the `west, south, east, north` bounds of an array given
    its height, width, and an affine transform.
    """
    ...
def from_gcps(gcps: Sequence[GroundControlPoint]) -> Affine:
    """
    Make an Affine transform from ground control points.

    Parameters
    ----------
    gcps : sequence of GroundControlPoint
        Such as the first item of a dataset's `gcps` property.

    Returns
    -------
    Affine
    """
    ...
def xy(
    transform: Affine | Sequence[GroundControlPoint] | RPC,
    rows: int | Sequence[int],
    cols: int | Sequence[int],
    zs: float | Sequence[float] | None = None,
    offset: _OffsetOptions = "center",
    **rpc_options: _GDALOption,
) -> tuple[float, float] | tuple[list[float], list[float]]:
    """
    Get the x and y coordinates of pixels at `rows` and `cols`.

    The pixel's center is returned by default, but a corner can be returned
    by setting `offset` to one of `ul, ur, ll, lr`.

    Supports affine, Ground Control Point (GCP), or Rational Polynomial
    Coefficients (RPC) based coordinate transformations.

    Parameters
    ----------
    transform : Affine or sequence of GroundControlPoint or RPC
        Transform suitable for input to AffineTransformer, GCPTransformer, or RPCTransformer.
    rows : list or int
        Pixel rows.
    cols : int or sequence of ints
        Pixel columns.
    zs : list or float, optional
        Height associated with coordinates. Primarily used for RPC based
        coordinate transformations. Ignored for affine based
        transformations. Default: 0.
    offset : str, optional
        Determines if the returned coordinates are for the center of the
        pixel or for a corner.
    rpc_options : dict, optional
        Additional arguments passed to GDALCreateRPCTransformer.

    Returns
    -------
    xs : float or list of floats
        x coordinates in coordinate reference system
    ys : float or list of floats
        y coordinates in coordinate reference system
    """
    ...
def rowcol(
    transform: Affine | Sequence[GroundControlPoint] | RPC,
    xs: float | Sequence[float],
    ys: float | Sequence[float],
    zs: float | Sequence[float] | None = None,
    op: _RoundOperation | None = None,
    precision: int | None = None,
    **rpc_options: _GDALOption,
) -> tuple[int, int] | tuple[list[int], list[int]]:
    """
    Get rows and cols of the pixels containing (x, y).

    Parameters
    ----------
    transform : Affine or sequence of GroundControlPoint or RPC
        Transform suitable for input to AffineTransformer,
        GCPTransformer, or RPCTransformer.
    xs : list or float
        x values in coordinate reference system.
    ys : list or float
        y values in coordinate reference system.
    zs : list or float, optional
        Height associated with coordinates. Primarily used for RPC based
        coordinate transformations. Ignored for affine based
        transformations. Default: 0.
    op : function, optional (default: numpy.floor)
        Function to convert fractional pixels to whole numbers (floor,
        ceiling, round)
    precision : int or float, optional
        This parameter is unused, deprecated in rasterio 1.3.0, and
        will be removed in version 2.0.0.
    rpc_options : dict, optional
        Additional arguments passed to GDALCreateRPCTransformer.

    Returns
    -------
    rows : array of ints or floats
    cols : array of ints or floats
        Integers are the default. The numerical type is determined by
        the type returned by op().
    """
    ...
def get_transformer(
    transform: Affine | Sequence[GroundControlPoint] | RPC, **rpc_options: _GDALOption
) -> type[TransformerBase]:
    """Return the appropriate transformer class"""
    ...

class TransformerBase:
    """
    Generic GDAL transformer base class

    Notes
    -----
    Subclasses must have a _transformer attribute and implement a `_transform` method.
    """
    def __init__(self) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, *args: object) -> None: ...
    def xy(
        self,
        rows: int | Sequence[int],
        cols: int | Sequence[int],
        zs: float | Sequence[float] | None = None,
        offset: _OffsetOptions = "center",
    ) -> tuple[float, float] | tuple[list[float], list[float]]:
        """
        Returns geographic coordinates given dataset rows and cols coordinates

        Parameters
        ----------
        rows, cols : int or list of int
            Image pixel coordinates
        zs : float or list of float, optional
            Height associated with coordinates. Primarily used for RPC based
            coordinate transformations. Ignored for affine based
            transformations. Default: 0.
        offset : str, optional
            Determines if the returned coordinates are for the center of the
            pixel or for a corner. Available options include center, ul, ur, ll,
            lr.
        Raises
        ------
        ValueError
            If input coordinates are not all equal length

        Returns
        -------
        tuple of float or list of float
        """
        ...

    @overload
    def rowcol(
        self,
        xs: float | Sequence[float],
        ys: float | Sequence[float],
        zs: float | Sequence[float] | None = None,
        op: _RoundOperation | None = None,
    ) -> tuple[int, int] | tuple[list[int], list[int]]:
        """
        Get rows and cols coordinates given geographic coordinates.

        Parameters
        ----------
        xs, ys : float or list of float
            Geographic coordinates
        zs : float or list of float, optional
            Height associated with coordinates. Primarily used for RPC
            based coordinate transformations. Ignored for affine based
            transformations. Default: 0.
        op : function, optional (default: numpy.floor)
            Function to convert fractional pixels to whole numbers
            (floor, ceiling, round)
        precision : int, optional (default: None)
            This parameter is unused, deprecated in rasterio 1.3.0, and
            will be removed in version 2.0.0.

        Raises
        ------
        TypeError
            If coordinate transformation fails.
        ValueError
            If input coordinates are not all equal length.

        Returns
        -------
        tuple of numbers or array of numbers.
            Integers are the default. The numerical type is determined
            by the type returned by op().
        """
        ...
    @overload
    @deprecated("The `precision` parameter is unused since rasterio 1.3 and will be removed in 2.0.0.")
    def rowcol(
        self,
        xs: float | Sequence[float],
        ys: float | Sequence[float],
        zs: float | Sequence[float] | None = None,
        op: _RoundOperation | None = None,
        precision: int | None = None,
    ) -> tuple[int, int] | tuple[list[int], list[int]]:
        """
        Get rows and cols coordinates given geographic coordinates.

        Parameters
        ----------
        xs, ys : float or list of float
            Geographic coordinates
        zs : float or list of float, optional
            Height associated with coordinates. Primarily used for RPC
            based coordinate transformations. Ignored for affine based
            transformations. Default: 0.
        op : function, optional (default: numpy.floor)
            Function to convert fractional pixels to whole numbers
            (floor, ceiling, round)
        precision : int, optional (default: None)
            This parameter is unused, deprecated in rasterio 1.3.0, and
            will be removed in version 2.0.0.

        Raises
        ------
        TypeError
            If coordinate transformation fails.
        ValueError
            If input coordinates are not all equal length.

        Returns
        -------
        tuple of numbers or array of numbers.
            Integers are the default. The numerical type is determined
            by the type returned by op().
        """
        ...

class GDALTransformerBase(TransformerBase):
    def __init__(self) -> None: ...
    def close(self) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, *args: object) -> None: ...

class AffineTransformer(TransformerBase):
    """A pure Python class related to affine based coordinate transformations."""
    def __init__(self, affine_transform: Affine | _Sextuple) -> None: ...

class GCPTransformer(GCPTransformerBase, GDALTransformerBase):
    """
    Class related to Ground Control Point (GCPs) based
    coordinate transformations.

    Uses GDALCreateGCPTransformer and GDALGCPTransform for computations.
    Ensure that GDAL transformer objects are destroyed by calling `close()`
    method or using context manager interface. If `tps` is set to True,
    uses GDALCreateTPSTransformer and GDALTPSTransform instead.
    """
    def __init__(self, gcps: Sequence[GroundControlPoint], tps: bool = False) -> None: ...

class RPCTransformer(RPCTransformerBase, GDALTransformerBase):
    """
    Class related to Rational Polynomial Coeffecients (RPCs) based
    coordinate transformations.

    Uses GDALCreateRPCTransformer and GDALRPCTransform for computations. Options
    for GDALCreateRPCTransformer may be passed using `rpc_options`.
    Ensure that GDAL transformer objects are destroyed by calling `close()`
    method or using context manager interface.
    """
    def __init__(self, rpcs: RPC, **rpc_options: _GDALOption) -> None: ...

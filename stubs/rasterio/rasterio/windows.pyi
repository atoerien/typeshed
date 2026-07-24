"""
Window utilities and related functions.

A window is an instance of Window

    Window(column_offset, row_offset, width, height)

or a 2D N-D array indexer in the form of a tuple.

    ((row_start, row_stop), (col_start, col_stop))

The latter can be evaluated within the context of a given height and
width and a boolean flag specifying whether the evaluation is boundless
or not. If boundless=True, negative index values do not mean index from
the end of the array dimension as they do in the boundless=False case.

The newer float precision read-write window capabilities of Rasterio
require instances of Window to be used.
"""

from collections.abc import Callable, Sequence
from typing import Any, TypeAlias, overload
from typing_extensions import Self, deprecated

from numpy.typing import NDArray
from rasterio._affine_types import Affine
from rasterio.errors import RasterioDeprecationWarning as RasterioDeprecationWarning, WindowError as WindowError

_Bounds: TypeAlias = tuple[float, float, float, float]
_Ranges: TypeAlias = tuple[tuple[int, int], tuple[int, int]]
_Slices: TypeAlias = tuple[slice, slice]

class WindowMethodsMixin:
    """
    Mixin providing methods for window-related calculations.
    These methods are wrappers for the functionality in
    `rasterio.windows` module.

    A subclass with this mixin MUST provide the following
    properties: `transform`, `height` and `width`.
    """
    @overload
    def window(self, left: float, bottom: float, right: float, top: float) -> Window:
        """
        Get the window corresponding to the bounding coordinates.

        The resulting window is not cropped to the row and column
        limits of the dataset.

        Parameters
        ----------
        left: float
            Left (west) bounding coordinate
        bottom: float
            Bottom (south) bounding coordinate
        right: float
            Right (east) bounding coordinate
        top: float
            Top (north) bounding coordinate
        precision: int, optional
            This parameter is unused, deprecated in rasterio 1.3.0, and
            will be removed in version 2.0.0.

        Returns
        -------
        window: Window
        """
        ...
    @overload
    @deprecated("The `precision` parameter is unused since rasterio 1.3 and will be removed in 2.0.0.")
    def window(self, left: float, bottom: float, right: float, top: float, precision: int | None = None) -> Window:
        """
        Get the window corresponding to the bounding coordinates.

        The resulting window is not cropped to the row and column
        limits of the dataset.

        Parameters
        ----------
        left: float
            Left (west) bounding coordinate
        bottom: float
            Bottom (south) bounding coordinate
        right: float
            Right (east) bounding coordinate
        top: float
            Top (north) bounding coordinate
        precision: int, optional
            This parameter is unused, deprecated in rasterio 1.3.0, and
            will be removed in version 2.0.0.

        Returns
        -------
        window: Window
        """
        ...

    def window_transform(self, window: Window) -> Affine:
        """
        Get the affine transform for a dataset window.

        Parameters
        ----------
        window: rasterio.windows.Window
            Dataset window

        Returns
        -------
        transform: Affine
            The affine transform matrix for the given window
        """
        ...
    def window_bounds(self, window: Window) -> _Bounds:
        """
        Get the bounds of a window

        Parameters
        ----------
        window: rasterio.windows.Window
            Dataset window

        Returns
        -------
        bounds : tuple
            x_min, y_min, x_max, y_max for the given window
        """
        ...

def iter_args(function: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to allow function to take either ``*args`` or
    a single iterable which gets expanded to ``*args``.
    """
    ...
def toranges(window: Window | _Ranges) -> _Ranges:
    """Normalize Windows to range tuples"""
    ...
def get_data_window(arr: NDArray[Any], nodata: float | None = None) -> Window:
    """
    Window covering the input array's valid data pixels.

    Parameters
    ----------
    arr: numpy ndarray, <= 3 dimensions
    nodata: number
        If None, will either return a full window if arr is not a masked
        array, or will use the mask to determine non-nodata pixels.
        If provided, it must be a number within the valid range of the
        dtype of the input array.

    Returns
    -------
    Window
    """
    ...
def union(*windows: Window) -> Window:
    """
    Union windows and return the outermost extent they cover.

    Parameters
    ----------
    windows: sequence
        One or more Windows.

    Returns
    -------
    Window
    """
    ...
def intersection(*windows: Window) -> Window:
    """
    Innermost extent of window intersections.

    Will raise WindowError if windows do not intersect.

    Parameters
    ----------
    windows: sequence
        One or more Windows.

    Returns
    -------
    Window
    """
    ...
def intersect(*windows: Window) -> bool:
    """
    Test if all given windows intersect.

    Parameters
    ----------
    windows: sequence
        One or more Windows.

    Returns
    -------
    bool
        True if all windows intersect.
    """
    ...

@overload
def from_bounds(left: float, bottom: float, right: float, top: float, transform: Affine | None = None) -> Window:
    """
    Get the window corresponding to the bounding coordinates.

    Parameters
    ----------
    left: float, required
        Left (west) bounding coordinates
    bottom: float, required
        Bottom (south) bounding coordinates
    right: float, required
        Right (east) bounding coordinates
    top: float, required
        Top (north) bounding coordinates
    transform: Affine, required
        Affine transform matrix.
    precision, height, width: int, optional
        These parameters are unused, deprecated in rasterio 1.3.0, and
        will be removed in version 2.0.0.

    Returns
    -------
    Window
        A new Window.

    Raises
    ------
    WindowError
        If a window can't be calculated.
    """
    ...
@overload
@deprecated(
    "`height`, `width`, and `precision` on windows.from_bounds are unused since rasterio 1.3 and will be removed in 2.0.0."
)
def from_bounds(
    left: float,
    bottom: float,
    right: float,
    top: float,
    transform: Affine | None = None,
    height: int | None = None,
    width: int | None = None,
    precision: int | None = None,
) -> Window:
    """
    Get the window corresponding to the bounding coordinates.

    Parameters
    ----------
    left: float, required
        Left (west) bounding coordinates
    bottom: float, required
        Bottom (south) bounding coordinates
    right: float, required
        Right (east) bounding coordinates
    top: float, required
        Top (north) bounding coordinates
    transform: Affine, required
        Affine transform matrix.
    precision, height, width: int, optional
        These parameters are unused, deprecated in rasterio 1.3.0, and
        will be removed in version 2.0.0.

    Returns
    -------
    Window
        A new Window.

    Raises
    ------
    WindowError
        If a window can't be calculated.
    """
    ...

def transform(window: Window, transform: Affine) -> Affine:
    """
    Construct an affine transform matrix relative to a window.

    Parameters
    ----------
    window: Window
        The input window.
    transform: Affine
        an affine transform matrix.

    Returns
    -------
    Affine
        The affine transform matrix for the given window
    """
    ...
def bounds(window: Window, transform: Affine, height: int = 0, width: int = 0) -> _Bounds:
    """
    Get the spatial bounds of a window.

    Parameters
    ----------
    window: Window
        The input window.
    transform: Affine
        an affine transform matrix.

    Returns
    -------
    left, bottom, right, top: float
        A tuple of spatial coordinate bounding values.
    """
    ...
def crop(window: Window, height: int, width: int) -> Window:
    """
    Crops a window to given height and width.

    Parameters
    ----------
    window : Window.
        The input window.
    height, width : int
        The number of rows and cols in the cropped window.

    Returns
    -------
    Window
        A new Window object.
    """
    ...
def evaluate(window: Window, height: int, width: int, boundless: bool = False) -> Window:
    """
    Evaluates a window tuple that may contain relative index values.

    The height and width of the array the window targets is the context
    for evaluation.

    Parameters
    ----------
    window: Window or tuple of (rows, cols).
        The input window.
    height, width: int
        The number of rows or columns in the array that the window
        targets.

    Returns
    -------
    Window
        A new Window object with absolute index values.
    """
    ...
def shape(window: Window, height: int = -1, width: int = -1) -> tuple[int, int]:
    """
    The shape of a window.

    height and width arguments are optional if there are no negative
    values in the window.

    Parameters
    ----------
    window: Window
        The input window.
    height, width : int, optional
        The number of rows or columns in the array that the window
        targets.

    Returns
    -------
    num_rows, num_cols
        The number of rows and columns of the window.
    """
    ...
def window_index(window: Window, height: int = 0, width: int = 0) -> _Slices:
    """
    Construct a pair of slice objects for ndarray indexing

    Starting indexes are rounded down, Stopping indexes are rounded up.

    Parameters
    ----------
    window: Window
        The input window.

    Returns
    -------
    row_slice, col_slice: slice
        A pair of slices in row, column order
    """
    ...
def round_window_to_full_blocks(
    window: Window, block_shapes: Sequence[tuple[int, int]], height: int = 0, width: int = 0
) -> Window:
    """
    Round window to include full expanse of intersecting tiles.

    Parameters
    ----------
    window: Window
        The input window.

    block_shapes : tuple of block shapes
        The input raster's block shape. All bands must have the same
        block/stripe structure

    Returns
    -------
    Window
    """
    ...
def validate_length_value(instance: object, attribute: object, value: float) -> None: ...
def subdivide(window: Window, height: int, width: int) -> list[Window]:
    """
    Divide a window into smaller windows.

    Windows have no overlap and will be at most the desired
    height and width. Smaller windows will be generated where
    the height and width do not evenly divide the window dimensions.

    Parameters
    ----------
    window : Window
        Source window to subdivide.
    height : int
        Subwindow height.
    width : int
        Subwindow width.

    Returns
    -------
    list of Windows
    """
    ...

class Window:
    """
    Windows are rectangular subsets of rasters.

    This class abstracts the 2-tuples mentioned in the module docstring
    and adds methods and new constructors.

    Attributes
    ----------
    col_off, row_off: float
        The offset for the window.
    width, height: float
        Lengths of the window.

    Notes
    -----
    Previously the lengths were called 'num_cols' and 'num_rows' but
    this is a bit confusing in the new float precision world and the
    attributes have been changed. The originals are deprecated.
    """
    col_off: float
    row_off: float
    width: float
    height: float
    def __init__(self, col_off: float, row_off: float, width: float, height: float) -> None:
        """Method generated by attrs for class Window."""
        ...
    def flatten(self) -> tuple[float, float, float, float]:
        """
        A flattened form of the window.

        Returns
        -------
        col_off, row_off, width, height: float
            Window offsets and lengths.
        """
        ...
    def todict(self) -> dict[str, float]:
        """
        A mapping of attribute names and values.

        Returns
        -------
        dict
        """
        ...
    def toranges(self) -> _Ranges:
        """Makes an equivalent pair of range tuples"""
        ...
    def toslices(self) -> _Slices:
        """
        Slice objects for use as an ndarray indexer.

        Returns
        -------
        row_slice, col_slice: slice
            A pair of slices in row, column order
        """
        ...
    @classmethod
    def from_slices(
        cls, rows: slice | Sequence[int], cols: slice | Sequence[int], height: int = -1, width: int = -1, boundless: bool = False
    ) -> Self:
        """
        Construct a Window from row and column slices or tuples / lists of
        start and stop indexes. Converts the rows and cols to offsets, height,
        and width.

        In general, indexes are defined relative to the upper left corner of
        the dataset: rows=(0, 10), cols=(0, 4) defines a window that is 4
        columns wide and 10 rows high starting from the upper left.

        Start indexes may be `None` and will default to 0.
        Stop indexes may be `None` and will default to width or height, which
        must be provided in this case.

        Negative start indexes are evaluated relative to the lower right of the
        dataset: rows=(-2, None), cols=(-2, None) defines a window that is 2
        rows high and 2 columns wide starting from the bottom right.

        Parameters
        ----------
        rows, cols: slice, tuple, or list
            Slices or 2 element tuples/lists containing start, stop indexes.
        height, width: float
            A shape to resolve relative values against. Only used when a start
            or stop index is negative or a stop index is None.
        boundless: bool, optional
            Whether the inputs are bounded (default) or not.

        Returns
        -------
        Window
        """
        ...
    # `**kwds` accepts the deprecated kwargs `op` (callable) and `pixel_precision` (int) emitted by rasterio < 1.3.
    def round_lengths(self, **kwds: Any) -> Window:
        """
        Return a copy with width and height rounded.

        Lengths are rounded to the nearest whole number. The offsets are
        not changed.

        Parameters
        ----------
        kwds : dict
            Collects keyword arguments that are no longer used.

        Returns
        -------
        Window
        """
        ...
    @deprecated("Window.round_shape is deprecated and will be removed in Rasterio 2.0.0; use round_lengths instead.")
    def round_shape(self, **kwds: Any) -> Window: ...
    def round_offsets(self, **kwds: Any) -> Window:
        """
        Return a copy with column and row offsets rounded.

        Offsets are rounded to the preceding whole number. The lengths
        are not changed.

        Parameters
        ----------
        kwds : dict
            Collects keyword arguments that are no longer used.

        Returns
        -------
        Window
        """
        ...
    def round(self, ndigits: int | None = None) -> Window:
        """
        Round a window's offsets and lengths

        Rounding to a very small fraction of a pixel can help treat
        floating point issues arising from computation of windows.
        """
        ...
    def crop(self, height: int, width: int) -> Window:
        """Return a copy cropped to height and width"""
        ...
    def intersection(self, other: Window) -> Window:
        """
        Return the intersection of this window and another

        Parameters
        ----------

        other: Window
            Another window

        Returns
        -------
        Window
        """
        ...

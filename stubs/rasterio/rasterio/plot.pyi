"""
Implementations of various common operations.

Including `show()` for displaying an array or with matplotlib.
Most can handle a numpy array or `rasterio.Band()`.
Primarily supports `$ rio insp`.
"""

import logging
from collections.abc import Mapping, Sequence
from typing import Any, Final, Literal

from numpy.typing import NDArray
from rasterio._affine_types import Affine
from rasterio.io import DatasetReader as DatasetReader
from rasterio.transform import guard_transform as guard_transform

logger: Final[logging.Logger]

# Returns the `matplotlib.pyplot` module (lazy import).
def get_plt() -> Any:
    """
    import matplotlib.pyplot
    raise import error if matplotlib is not installed
    """
    ...

# `ax`: matplotlib.axes.Axes; returns matplotlib.image.AxesImage or
# the input `ax` for contour plots. `**kwargs` are forwarded to
# matplotlib's `imshow`/`contour` call.
def show(
    source: NDArray[Any] | DatasetReader | tuple[DatasetReader, int],
    with_bounds: bool = True,
    contour: bool = False,
    contour_label_kws: Mapping[str, Any] | None = None,
    indexes: Sequence[int] | None = None,
    ax: Any | None = None,
    title: str | None = None,
    transform: Affine | None = None,
    percent_range: tuple[float, float] | None = None,
    adjust: bool = True,
    **kwargs: Any,
) -> Any:
    """
    Display a raster or raster band using matplotlib.

    Parameters
    ----------
    source : array or dataset object opened in 'r' mode or Band or tuple(dataset, bidx)
        If Band or tuple (dataset, bidx), display the selected band.
        If raster dataset display the rgb image
        as defined in the colorinterp metadata, or default to first band.
    with_bounds : bool (opt)
        Whether to change the image extent to the spatial bounds of the image,
        rather than pixel coordinates. Only works when source is
        (raster dataset, bidx) or raster dataset.
    contour : bool (opt)
        Whether to plot the raster data as contours
    contour_label_kws : dictionary (opt)
        Keyword arguments for labeling the contours,
        empty dictionary for no labels.
    indexes: list or tupel, optional, defines the color composite of bands.
    ax : matplotlib.axes.Axes, optional
        Axes to plot on, otherwise uses current axes.
    title : str, optional
        Title for the figure.
    transform : Affine, optional
        Defines the affine transform if source is an array
    percent_range: tuple, optional
        percent_range[0], the minimum value (cumulative percentage) of the histogram for histogram streching,
        percent_range[1], the maximum value (cumulative percentage) of the histogram for histogram streching
        default percent_range is set to (2, 98).
    adjust : bool
        If the plotted data is an RGB image, adjust the values of
        each band so that they fall between 0 and 1 before plotting. If
        True, values will be adjusted by the min / max of each band. If
        False, no adjustment will be applied.
    **kwargs : key, value pairings optional
        These will be passed to the :func:`matplotlib.pyplot.imshow` or
        :func:`matplotlib.pyplot.contour` contour method depending on contour argument.

    Returns
    -------
    ax : matplotlib.axes.Axes
        Axes with plot.
    """
    ...
def plotting_extent(
    source: NDArray[Any] | DatasetReader, transform: Affine | None = None
) -> tuple[float, float, float, float]:
    """
    Returns an extent in the format needed
     for :func:`matplotlib.pyplot.imshow` (left, right, bottom, top)
     instead of rasterio's bounds (left, bottom, right, top)

    Parameters
    ----------
    source : numpy.ndarray or dataset object opened in 'r' mode
        If array, data in the order rows, columns and optionally bands. If array
        is band order (bands in the first dimension), use arr[0]
    transform: Affine, required if source is array
        Defines the affine transform if source is an array

    Returns
    -------
    tuple of float
        left, right, bottom, top
    """
    ...
def reshape_as_image(arr: NDArray[Any]) -> NDArray[Any]:
    """
    Returns the source array reshaped into the order
    expected by image processing and visualization software
    (matplotlib, scikit-image, etc)
    by swapping the axes order from (bands, rows, columns)
    to (rows, columns, bands)

    Parameters
    ----------
    arr : array-like of shape (bands, rows, columns)
        image to reshape
    """
    ...
def reshape_as_raster(arr: NDArray[Any]) -> NDArray[Any]:
    """
    Returns the array in a raster order
    by swapping the axes order from (rows, columns, bands)
    to (bands, rows, columns)

    Parameters
    ----------
    arr : array-like in the image form of (rows, columns, bands)
        image to reshape
    """
    ...

# `ax`: matplotlib.axes.Axes; `**kwargs` are forwarded to matplotlib's `hist` call.
def show_hist(
    source: NDArray[Any] | DatasetReader,
    bins: int = 10,
    masked: bool = True,
    title: str = "Histogram",
    ax: Any | None = None,
    label: str | Sequence[str] | None = None,
    range: tuple[float, float] | None = None,
    **kwargs: Any,
) -> None:
    """
    Easily display a histogram with matplotlib.

    Parameters
    ----------
    source : array or dataset object opened in 'r' mode or Band or tuple(dataset, bidx)
        Input data to display.
        The first three arrays in multi-dimensional
        arrays are plotted as red, green, and blue.
    bins : int, optional
        Compute histogram across N bins.
    masked : bool, optional
        When working with a `rasterio.Band()` object, specifies if the data
        should be masked on read.
    title : str, optional
        Title for the figure.
    ax : matplotlib.axes.Axes, optional
        The raster will be added to this axes if passed.
    label : str, optional
        String, or list of strings. If passed, matplotlib will use this label list.
        Otherwise, a default label list will be automatically created
    range : list, optional
        List of `[min, max]` values. If passed, matplotlib will use this range.
        Otherwise, a default range will be automatically created
    **kwargs : optional keyword arguments
        These will be passed to the :meth:`matplotlib.axes.Axes.hist` method.
    """
    ...
def adjust_band(band: NDArray[Any], kind: Literal["linear", "log"] | None = None) -> NDArray[Any]:
    """
    Adjust a band to be between 0 and 1.
    Parameters
    ----------
    band : array, shape (height, width)
        A band of a raster object.
    kind : str
        An unused option. For now, there is only one option ('linear').

    Returns
    -------
    band_normed : array, shape (height, width)
        An adjusted version of the input band.
    """
    ...
def contrast_strech(arr: NDArray[Any], percent_range: tuple[float, float] = (2.0, 98.0)) -> NDArray[Any]:
    """
    Histogram streching for better image visualization.

    Parameters
    ----------
    arr : array-like in the image form of (rows, columns, bands)
        image to reshape
    percent_range: tuple, optional
        percent_range[0], the minimum values (cumulative percentage) of the histogram for histogram streching,
        percent_range[1], the maximum value (cumulative percentage) of the histogram for histogram streching
        default percent_range is set to (2, 98).
    """
    ...

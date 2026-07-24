from collections.abc import Iterable, Iterator, Sequence
from typing import Any

from numpy.typing import NDArray
from rasterio.io import DatasetReader

def sample_gen(
    dataset: DatasetReader, xy: Iterable[tuple[float, float]], indexes: int | Sequence[int] | None = None, masked: bool = False
) -> Iterator[NDArray[Any]]:
    """
    Sample pixels from a dataset

    Parameters
    ----------
    dataset : rasterio Dataset
        Opened in "r" mode.
    xy : iterable
        Pairs of x, y coordinates in the dataset's reference system.

        Note: Sorting coordinates can often yield better performance.
        A sort_xy function is provided in this module for convenience.
    indexes : int or list of int
        Indexes of dataset bands to sample.
    masked : bool, default: False
        Whether to mask samples that fall outside the extent of the
        dataset.

    Yields
    ------
    array
        A array of length equal to the number of specified indexes
        containing the dataset values for the bands corresponding to
        those indexes.
    """
    ...
def sort_xy(xy: Iterable[tuple[float, float]]) -> list[tuple[float, float]]:
    """
    Sort x, y coordinates by x then y

    Parameters
    ----------
    xy : iterable
        Pairs of x, y coordinates

    Returns
    -------
    list
        A list of sorted x, y coordinates
    """
    ...

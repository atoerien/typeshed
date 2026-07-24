"""Mapping of GDAL to Numpy data types."""

from collections.abc import Sequence
from typing import Any, Final

import numpy as np
from numpy.typing import ArrayLike, DTypeLike

bool_: Final[str]
ubyte: Final[str]
uint8: Final[str]
sbyte: Final[str]
int8: Final[str]
uint16: Final[str]
int16: Final[str]
uint32: Final[str]
int32: Final[str]
int64: Final[str]
uint64: Final[str]
float16: Final[str]
float32: Final[str]
float64: Final[str]
complex_: Final[str]
complex64: Final[str]
complex128: Final[str]
complex_int16: Final[str]

dtype_fwd: Final[dict[int, str | None]]
dtype_rev: Final[dict[str | None, int]]
typename_fwd: Final[dict[int, str]]
typename_rev: Final[dict[str, int]]
dtype_ranges: Final[dict[str, tuple[float, float]]]
dtype_info_registry: Final[dict[str, type]]

# `numpy.finfo` instances cached at module import; used by `in_dtype_range`.
f16i: Final[np.finfo[np.float16]]
f32i: Final[np.finfo[np.float32]]
f64i: Final[np.finfo[np.float64]]

def in_dtype_range(value: float, dtype: DTypeLike) -> bool:
    """Test if the value is within the dtype's range of values, Nan, or Inf."""
    ...
def check_dtype(dt: DTypeLike) -> bool:
    """Check if dtype is a known dtype."""
    ...
def get_minimum_dtype(values: ArrayLike) -> str:
    """
    Determine minimum type to represent values.

    Uses range checking to determine the minimum integer or floating point
    data type required to represent values.

    Parameters
    ----------
    values: list-like


    Returns
    -------
    rasterio dtype string
    """
    ...

# isinstance check; accepts any object and returns True for numpy.ndarray
# and any object exposing `__array__`.
def is_ndarray(array: Any) -> bool:
    """Check if array is a ndarray."""
    ...
def can_cast_dtype(values: ArrayLike, dtype: DTypeLike) -> bool:
    """
    Test if values can be cast to dtype without loss of information.

    Parameters
    ----------
    values: list-like
    dtype: numpy.dtype or string

    Returns
    -------
    boolean
        True if values can be cast to data type.
    """
    ...
def validate_dtype(values: ArrayLike, valid_dtypes: Sequence[DTypeLike]) -> bool:
    """
    Test if dtype of values is one of valid_dtypes.

    Parameters
    ----------
    values: list-like
    valid_dtypes: list-like
        list of valid dtype strings, e.g., ('int16', 'int32')

    Returns
    -------
    boolean:
        True if dtype of values is one of valid_dtypes
    """
    ...

from _typeshed import Incomplete
from collections.abc import Mapping
from typing import (
    # pyarrow types returned as Any to avoid depending on pyarrow (40 MB) in stubs
    Any as _PAArray,
    Any as _PAField,
    Any as _PATable,
    Literal,
    Protocol,
    type_check_only,
)
from typing_extensions import CapsuleType, TypeAlias

import numpy as np
from numpy.typing import NDArray

from ..array import GeometryArray
from ..geodataframe import GeoDataFrame

# Literal for language server completions and str because runtime normalizes to lowercase
_GeomEncoding: TypeAlias = Literal["WKB", "geoarrow"] | str  # noqa: Y051

@type_check_only
class _PyarrowTableLike(Protocol):
    def __arrow_c_stream__(self, requested_schema=None) -> CapsuleType: ...

@type_check_only
class _PyarrowFieldLike(Protocol):
    def __arrow_c_schema__(self) -> CapsuleType: ...

@type_check_only
class _PyarrowArrayLike(Protocol):
    def __arrow_c_array__(self) -> tuple[CapsuleType, CapsuleType]: ...

GEOARROW_ENCODINGS: list[str]

class ArrowTable:
    """
    Wrapper class for Arrow data.

    This class implements the `Arrow PyCapsule Protocol`_ (i.e. having an
    ``__arrow_c_stream__`` method). This object can then be consumed by
    your Arrow implementation of choice that supports this protocol.

    .. _Arrow PyCapsule Protocol: https://arrow.apache.org/docs/format/CDataInterface/PyCapsuleInterface.html

    Example
    -------
    >>> import pyarrow as pa
    >>> pa.table(gdf.to_arrow())  # doctest: +SKIP
    """
    def __init__(self, pa_table: _PyarrowTableLike) -> None: ...
    def __arrow_c_stream__(self, requested_schema=None) -> CapsuleType: ...

class GeoArrowArray:
    """
    Wrapper class for a geometry array as Arrow data.

    This class implements the `Arrow PyCapsule Protocol`_ (i.e. having an
    ``__arrow_c_array/stream__`` method). This object can then be consumed by
    your Arrow implementation of choice that supports this protocol.

    .. _Arrow PyCapsule Protocol: https://arrow.apache.org/docs/format/CDataInterface/PyCapsuleInterface.html

    Example
    -------
    >>> import pyarrow as pa
    >>> pa.array(ser.to_arrow())  # doctest: +SKIP
    """
    def __init__(self, pa_field: _PyarrowFieldLike, pa_array: _PyarrowArrayLike) -> None: ...
    def __arrow_c_array__(self, requested_schema=None) -> tuple[CapsuleType, CapsuleType]: ...

def geopandas_to_arrow(
    df: GeoDataFrame,
    index: bool | None = None,
    geometry_encoding: _GeomEncoding = "WKB",
    interleaved: bool = True,
    include_z: bool | None = None,
) -> tuple[_PATable, dict[str, str]]:
    """
    Convert GeoDataFrame to a pyarrow.Table.

    Parameters
    ----------
    df : GeoDataFrame
        The GeoDataFrame to convert.
    index : bool, default None
        If ``True``, always include the dataframe's index(es) as columns
        in the file output.
        If ``False``, the index(es) will not be written to the file.
        If ``None``, the index(ex) will be included as columns in the file
        output except `RangeIndex` which is stored as metadata only.
    geometry_encoding : {'WKB', 'geoarrow' }, default 'WKB'
        The GeoArrow encoding to use for the data conversion.
    interleaved : bool, default True
        Only relevant for 'geoarrow' encoding. If True, the geometries'
        coordinates are interleaved in a single fixed size list array.
        If False, the coordinates are stored as separate arrays in a
        struct type.
    include_z : bool, default None
        Only relevant for 'geoarrow' encoding (for WKB, the dimensionality
        of the individual geometries is preserved).
        If False, return 2D geometries. If True, include the third dimension
        in the output (if a geometry has no third dimension, the z-coordinates
        will be NaN). By default, will infer the dimensionality from the
        input geometries. Note that this inference can be unreliable with
        empty geometries (for a guaranteed result, it is recommended to
        specify the keyword).
    """
    ...
def construct_wkb_array(
    shapely_arr: NDArray[np.object_], *, field_name: str = "geometry", crs: str | None = None
) -> tuple[_PAField, _PAArray]: ...
def construct_geometry_array(
    shapely_arr: NDArray[np.object_],
    include_z: bool | None = None,
    *,
    field_name: str = "geometry",
    crs: str | None = None,
    interleaved: bool = True,
) -> tuple[_PAField, _PAArray]: ...
def arrow_to_geopandas(
    table, geometry: str | None = None, to_pandas_kwargs: Mapping[str, Incomplete] | None = None
) -> GeoDataFrame:
    """
    Convert Arrow table object to a GeoDataFrame based on GeoArrow extension types.

    Parameters
    ----------
    table : pyarrow.Table
        The Arrow table to convert.
    geometry : str, default None
        The name of the geometry column to set as the active geometry
        column. If None, the first geometry column found will be used.
    to_pandas_kwargs : dict, optional
        Arguments passed to the `pa.Table.to_pandas` method for non-geometry columns.
        This can be used to control the behavior of the conversion of the non-geometry
        columns to a pandas DataFrame. For example, you can use this to control the
        dtype conversion of the columns. By default, the `to_pandas` method is called
        with no additional arguments.

    Returns
    -------
    GeoDataFrame
    """
    ...
def arrow_to_geometry_array(arr) -> GeometryArray:
    """
    Convert Arrow array object (representing single GeoArrow array) to a
    geopandas GeometryArray.

    Specifically for GeoSeries.from_arrow.
    """
    ...
def construct_shapely_array(arr: _PAArray, extension_name: str) -> NDArray[np.object_]:
    """
    Construct a NumPy array of shapely geometries from a pyarrow.Array
    with GeoArrow extension type.
    """
    ...

"""Low level functions to read and write OGR data sources."""

from collections.abc import Collection, Iterable
from contextlib import AbstractContextManager
from typing import Any, Literal, TypedDict, overload, type_check_only

import numpy as np
import pyarrow as pa  # type: ignore[import-not-found]  # pyright: ignore[reportMissingImports]
import shapely as shp

from ._typing import Array1D, ArrayLikeInt, ReadPathOrBuffer, SupportsArrowCStream, WritePathOrBuffer

DRIVERS_NO_MIXED_SINGLE_MULTI: set[str]
DRIVERS_NO_MIXED_DIMENSIONS: set[str]

@type_check_only
class _Meta(TypedDict):
    crs: str
    fields: Array1D[np.object_]
    dtypes: Array1D[np.object_]
    ogr_types: list[str]
    ogr_subtypes: list[str]
    encoding: str
    geometry_type: str
    geometry_name: str
    fid_column: str

@overload
def read(
    path_or_buffer: ReadPathOrBuffer,
    /,
    layer: int | str | None = None,
    encoding: str | None = None,
    columns: Collection[str] | None = None,
    read_geometry: bool = True,
    force_2d: bool = False,
    skip_features: int = 0,
    max_features: int | None = None,
    where: str | None = None,
    bbox: tuple[float, float, float, float] | None = None,
    mask: shp.Geometry | None = None,
    fids: ArrayLikeInt | None = None,
    sql: str | None = None,
    sql_dialect: str | None = None,
    return_fids: Literal[False] = False,
    datetime_as_string: bool = False,
    **kwargs: Any,  # Dataset open options passed to OGR
) -> tuple[_Meta, None, Array1D[np.object_] | None, list[np.ndarray]]:
    """
    Read OGR data source into numpy arrays.

    IMPORTANT: non-linear geometry types (e.g., MultiSurface) are converted
    to their linear approximations.

    Parameters
    ----------
    path_or_buffer : pathlib.Path or str, or bytes buffer
        A dataset path or URI, raw buffer, or file-like object with a read method.
    layer : int or str, optional (default: first layer)
        If an integer is provided, it corresponds to the index of the layer
        with the data source.  If a string is provided, it must match the name
        of the layer in the data source.  Defaults to first layer in data source.
    encoding : str, optional (default: None)
        If present, will be used as the encoding for reading string values from
        the data source.  By default will automatically try to detect the native
        encoding and decode to ``UTF-8``.
    columns : list-like, optional (default: all columns)
        List of column names to import from the data source.  Column names must
        exactly match the names in the data source, and will be returned in
        the order they occur in the data source.  To avoid reading any columns,
        pass an empty list-like.  If combined with ``where`` parameter, must
        include columns referenced in the ``where`` expression or the data may
        not be correctly read; the data source may return empty results or
        raise an exception (behavior varies by driver).
    read_geometry : bool, optional (default: True)
        If True, will read geometry into WKB.  If False, geometry will be None.
    force_2d : bool, optional (default: False)
        If the geometry has Z values, setting this to True will cause those to
        be ignored and 2D geometries to be returned
    skip_features : int, optional (default: 0)
        Number of features to skip from the beginning of the file before
        returning features.  If greater than available number of features, an
        empty DataFrame will be returned.  Using this parameter may incur
        significant overhead if the driver does not support the capability to
        randomly seek to a specific feature, because it will need to iterate
        over all prior features.
    max_features : int, optional (default: None)
        Number of features to read from the file.
    where : str, optional (default: None)
        Where clause to filter features in layer by attribute values. If the data source
        natively supports SQL, its specific SQL dialect should be used (eg. SQLite and
        GeoPackage: `SQLITE`_, PostgreSQL). If it doesn't, the `OGRSQL WHERE`_ syntax
        should be used. Note that it is not possible to overrule the SQL dialect, this
        is only possible when you use the SQL parameter.
        Examples: ``"ISO_A3 = 'CAN'"``, ``"POP_EST > 10000000 AND POP_EST < 100000000"``
    bbox : tuple of (xmin, ymin, xmax, ymax), optional (default: None)
        If present, will be used to filter records whose geometry intersects this
        box.  This must be in the same CRS as the dataset.  If GEOS is present
        and used by GDAL, only geometries that intersect this bbox will be
        returned; if GEOS is not available or not used by GDAL, all geometries
        with bounding boxes that intersect this bbox will be returned.
        Cannot be combined with ``mask`` keyword.
    mask : Shapely geometry, optional (default: None)
        If present, will be used to filter records whose geometry intersects
        this geometry.  This must be in the same CRS as the dataset.  If GEOS is
        present and used by GDAL, only geometries that intersect this geometry
        will be returned; if GEOS is not available or not used by GDAL, all
        geometries with bounding boxes that intersect the bounding box of this
        geometry will be returned.  Requires Shapely >= 2.0.
        Cannot be combined with ``bbox`` keyword.
    fids : array-like, optional (default: None)
        Array of integer feature id (FID) values to select. Cannot be combined
        with other keywords to select a subset (``skip_features``,
        ``max_features``, ``where``, ``bbox``, or ``mask``). Note that the
        starting index is driver and file specific (e.g. typically 0 for
        Shapefile and 1 for GeoPackage, but can still depend on the specific
        file). The performance of reading a large number of features usings FIDs
        is also driver specific.
    sql : str, optional (default: None)
        The SQL statement to execute. Look at the sql_dialect parameter for more
        information on the syntax to use for the query. When combined with other
        keywords like ``columns``, ``skip_features``, ``max_features``,
        ``where``, ``bbox``, or ``mask``, those are applied after the SQL query.
        Be aware that this can have an impact on performance, (e.g. filtering
        with the ``bbox`` or ``mask`` keywords may not use spatial indexes).
        Cannot be combined with the ``layer`` or ``fids`` keywords.
    sql_dialect : str, optional (default: None)
        The SQL dialect the ``sql`` statement is written in. Possible values:

          - **None**: if the data source natively supports SQL, its specific SQL dialect
            will be used by default (eg. SQLite and Geopackage: `SQLITE`_, PostgreSQL).
            If the data source doesn't natively support SQL, the `OGRSQL`_ dialect is
            the default.
          - '`OGRSQL`_': can be used on any data source. Performance can suffer
            when used on data sources with native support for SQL.
          - '`SQLITE`_': can be used on any data source. All spatialite_
            functions can be used. Performance can suffer on data sources with
            native support for SQL, except for Geopackage and SQLite as this is
            their native SQL dialect.

    return_fids : bool, optional (default: False)
        If True, will return the FIDs of the feature that were read.
    datetime_as_string : bool, optional (default: False)
        If True, will return datetime dtypes as detected by GDAL as a string
        array (which can be used to extract time zone info), instead of
        a datetime64 array.

    **kwargs
        Additional driver-specific dataset open options passed to OGR.  Invalid
        options will trigger a warning.

    Returns
    -------
    (dict, fids, geometry, data fields)
        Returns a tuple of meta information about the data source in a dict,
        an ndarray of FIDs corresponding to the features that were read or None
        (if return_fids is False),
        an ndarray of geometry objects or None (if data source does not include
        geometry or read_geometry is False), a tuple of ndarrays for each field
        in the data layer.

        Meta is: {
            "crs": "<crs>",
            "fields": <ndarray of field names>,
            "dtypes": <ndarray of numpy dtypes corresponding to fields>,
            "ogr_types": <ndarray of OGR types corresponding to fields>,
            "ogr_subtypes": <ndarray of OGR subtypes corresponding to fields>,
            "encoding": "<encoding>",
            "geometry_type": "<geometry type>",
        }

    .. _OGRSQL:

        https://gdal.org/user/ogr_sql_dialect.html#ogr-sql-dialect

    .. _OGRSQL WHERE:

        https://gdal.org/user/ogr_sql_dialect.html#where

    .. _SQLITE:

        https://gdal.org/user/sql_sqlite_dialect.html#sql-sqlite-dialect

    .. _spatialite:

        https://www.gaia-gis.it/gaia-sins/spatialite-sql-latest.html
    """
    ...
@overload
def read(
    path_or_buffer: ReadPathOrBuffer,
    /,
    layer: int | str | None = None,
    encoding: str | None = None,
    columns: Collection[str] | None = None,
    read_geometry: bool = True,
    force_2d: bool = False,
    skip_features: int = 0,
    max_features: int | None = None,
    where: str | None = None,
    bbox: tuple[float, float, float, float] | None = None,
    mask: shp.Geometry | None = None,
    fids: ArrayLikeInt | None = None,
    sql: str | None = None,
    sql_dialect: str | None = None,
    *,
    return_fids: Literal[True],
    datetime_as_string: bool = False,
    **kwargs: Any,  # Dataset open options passed to OGR
) -> tuple[_Meta, Array1D[np.int64], Array1D[np.object_] | None, list[np.ndarray]]:
    """
    Read OGR data source into numpy arrays.

    IMPORTANT: non-linear geometry types (e.g., MultiSurface) are converted
    to their linear approximations.

    Parameters
    ----------
    path_or_buffer : pathlib.Path or str, or bytes buffer
        A dataset path or URI, raw buffer, or file-like object with a read method.
    layer : int or str, optional (default: first layer)
        If an integer is provided, it corresponds to the index of the layer
        with the data source.  If a string is provided, it must match the name
        of the layer in the data source.  Defaults to first layer in data source.
    encoding : str, optional (default: None)
        If present, will be used as the encoding for reading string values from
        the data source.  By default will automatically try to detect the native
        encoding and decode to ``UTF-8``.
    columns : list-like, optional (default: all columns)
        List of column names to import from the data source.  Column names must
        exactly match the names in the data source, and will be returned in
        the order they occur in the data source.  To avoid reading any columns,
        pass an empty list-like.  If combined with ``where`` parameter, must
        include columns referenced in the ``where`` expression or the data may
        not be correctly read; the data source may return empty results or
        raise an exception (behavior varies by driver).
    read_geometry : bool, optional (default: True)
        If True, will read geometry into WKB.  If False, geometry will be None.
    force_2d : bool, optional (default: False)
        If the geometry has Z values, setting this to True will cause those to
        be ignored and 2D geometries to be returned
    skip_features : int, optional (default: 0)
        Number of features to skip from the beginning of the file before
        returning features.  If greater than available number of features, an
        empty DataFrame will be returned.  Using this parameter may incur
        significant overhead if the driver does not support the capability to
        randomly seek to a specific feature, because it will need to iterate
        over all prior features.
    max_features : int, optional (default: None)
        Number of features to read from the file.
    where : str, optional (default: None)
        Where clause to filter features in layer by attribute values. If the data source
        natively supports SQL, its specific SQL dialect should be used (eg. SQLite and
        GeoPackage: `SQLITE`_, PostgreSQL). If it doesn't, the `OGRSQL WHERE`_ syntax
        should be used. Note that it is not possible to overrule the SQL dialect, this
        is only possible when you use the SQL parameter.
        Examples: ``"ISO_A3 = 'CAN'"``, ``"POP_EST > 10000000 AND POP_EST < 100000000"``
    bbox : tuple of (xmin, ymin, xmax, ymax), optional (default: None)
        If present, will be used to filter records whose geometry intersects this
        box.  This must be in the same CRS as the dataset.  If GEOS is present
        and used by GDAL, only geometries that intersect this bbox will be
        returned; if GEOS is not available or not used by GDAL, all geometries
        with bounding boxes that intersect this bbox will be returned.
        Cannot be combined with ``mask`` keyword.
    mask : Shapely geometry, optional (default: None)
        If present, will be used to filter records whose geometry intersects
        this geometry.  This must be in the same CRS as the dataset.  If GEOS is
        present and used by GDAL, only geometries that intersect this geometry
        will be returned; if GEOS is not available or not used by GDAL, all
        geometries with bounding boxes that intersect the bounding box of this
        geometry will be returned.  Requires Shapely >= 2.0.
        Cannot be combined with ``bbox`` keyword.
    fids : array-like, optional (default: None)
        Array of integer feature id (FID) values to select. Cannot be combined
        with other keywords to select a subset (``skip_features``,
        ``max_features``, ``where``, ``bbox``, or ``mask``). Note that the
        starting index is driver and file specific (e.g. typically 0 for
        Shapefile and 1 for GeoPackage, but can still depend on the specific
        file). The performance of reading a large number of features usings FIDs
        is also driver specific.
    sql : str, optional (default: None)
        The SQL statement to execute. Look at the sql_dialect parameter for more
        information on the syntax to use for the query. When combined with other
        keywords like ``columns``, ``skip_features``, ``max_features``,
        ``where``, ``bbox``, or ``mask``, those are applied after the SQL query.
        Be aware that this can have an impact on performance, (e.g. filtering
        with the ``bbox`` or ``mask`` keywords may not use spatial indexes).
        Cannot be combined with the ``layer`` or ``fids`` keywords.
    sql_dialect : str, optional (default: None)
        The SQL dialect the ``sql`` statement is written in. Possible values:

          - **None**: if the data source natively supports SQL, its specific SQL dialect
            will be used by default (eg. SQLite and Geopackage: `SQLITE`_, PostgreSQL).
            If the data source doesn't natively support SQL, the `OGRSQL`_ dialect is
            the default.
          - '`OGRSQL`_': can be used on any data source. Performance can suffer
            when used on data sources with native support for SQL.
          - '`SQLITE`_': can be used on any data source. All spatialite_
            functions can be used. Performance can suffer on data sources with
            native support for SQL, except for Geopackage and SQLite as this is
            their native SQL dialect.

    return_fids : bool, optional (default: False)
        If True, will return the FIDs of the feature that were read.
    datetime_as_string : bool, optional (default: False)
        If True, will return datetime dtypes as detected by GDAL as a string
        array (which can be used to extract time zone info), instead of
        a datetime64 array.

    **kwargs
        Additional driver-specific dataset open options passed to OGR.  Invalid
        options will trigger a warning.

    Returns
    -------
    (dict, fids, geometry, data fields)
        Returns a tuple of meta information about the data source in a dict,
        an ndarray of FIDs corresponding to the features that were read or None
        (if return_fids is False),
        an ndarray of geometry objects or None (if data source does not include
        geometry or read_geometry is False), a tuple of ndarrays for each field
        in the data layer.

        Meta is: {
            "crs": "<crs>",
            "fields": <ndarray of field names>,
            "dtypes": <ndarray of numpy dtypes corresponding to fields>,
            "ogr_types": <ndarray of OGR types corresponding to fields>,
            "ogr_subtypes": <ndarray of OGR subtypes corresponding to fields>,
            "encoding": "<encoding>",
            "geometry_type": "<geometry type>",
        }

    .. _OGRSQL:

        https://gdal.org/user/ogr_sql_dialect.html#ogr-sql-dialect

    .. _OGRSQL WHERE:

        https://gdal.org/user/ogr_sql_dialect.html#where

    .. _SQLITE:

        https://gdal.org/user/sql_sqlite_dialect.html#sql-sqlite-dialect

    .. _spatialite:

        https://www.gaia-gis.it/gaia-sins/spatialite-sql-latest.html
    """
    ...

def read_arrow(
    path_or_buffer: ReadPathOrBuffer,
    /,
    layer: int | str | None = None,
    encoding: str | None = None,
    columns: Collection[str] | None = None,
    read_geometry: bool = True,
    force_2d: bool = False,
    skip_features: int = 0,
    max_features: int | None = None,
    where: str | None = None,
    bbox: tuple[float, float, float, float] | None = None,
    mask: shp.Geometry | None = None,
    fids: ArrayLikeInt | None = None,
    sql: str | None = None,
    sql_dialect: str | None = None,
    return_fids: bool = False,
    datetime_as_string: bool = False,
    *,
    batch_size: int = 65536,  # Extracted from kwargs
    **kwargs: Any,  # Dataset open options passed to OGR
) -> tuple[_Meta, pa.Table]:
    """
    Read OGR data source into a pyarrow Table.

    See docstring of `read` for parameters.

    Returns
    -------
    (dict, pyarrow.Table)

        Returns a tuple of meta information about the returned data in a dict,
        and a pyarrow Table with data.

        Meta is: {
            "crs": "<crs>",
            "fields": <ndarray of field names>,
            "dtypes": <ndarray of numpy dtypes corresponding to fields>,
            "ogr_types": <ndarray of OGR types corresponding to fields>,
            "ogr_subtypes": <ndarray of OGR subtypes corresponding to fields>,
            "encoding": "<encoding>",
            "geometry_type": "<geometry_type>",
            "geometry_name": "<name of geometry column in arrow table>",
            "fid_column": "<name of FID column in arrow table>"
        }
    """
    ...

@overload
def open_arrow(
    path_or_buffer: ReadPathOrBuffer,
    /,
    layer: int | str | None = None,
    encoding: str | None = None,
    columns: Collection[str] | None = None,
    read_geometry: bool = True,
    force_2d: bool = False,
    skip_features: int = 0,
    max_features: int | None = None,
    where: str | None = None,
    bbox: tuple[float, float, float, float] | None = None,
    mask: shp.Geometry | None = None,
    fids: ArrayLikeInt | None = None,
    sql: str | None = None,
    sql_dialect: str | None = None,
    return_fids: bool = False,
    batch_size: int = 65536,
    use_pyarrow: Literal[False] = False,
    datetime_as_string: bool = False,
    **kwargs: Any,  # Dataset open options passed to OGR
) -> AbstractContextManager[tuple[_Meta, SupportsArrowCStream]]:
    """
    Open OGR data source as a stream of Arrow record batches.

    See docstring of `read` for parameters.

    The returned object is reading from a stream provided by OGR and must not be
    accessed after the OGR dataset has been closed, i.e. after the context manager has
    been closed.

    By default this functions returns a generic stream object implementing
    the `Arrow PyCapsule Protocol`_ (i.e. having an ``__arrow_c_stream__``
    method). This object can then be consumed by your Arrow implementation
    of choice that supports this protocol.
    Optionally, you can specify ``use_pyarrow=True`` to directly get the
    stream as a `pyarrow.RecordBatchReader`.

    .. _Arrow PyCapsule Protocol: https://arrow.apache.org/docs/format/CDataInterface/PyCapsuleInterface.html

    Other Parameters
    ----------------
    batch_size : int (default: 65_536)
        Maximum number of features to retrieve in a batch.
    use_pyarrow : bool (default: False)
        If True, return a pyarrow RecordBatchReader instead of a generic
        ArrowStream object. In the default case, this stream object needs
        to be passed to another library supporting the Arrow PyCapsule
        Protocol to consume the stream of data.
    datetime_as_string : bool, optional (default: False)
        If True, will return datetime dtypes as detected by GDAL as strings,
        as Arrow doesn't support e.g. mixed time zones.

    Examples
    --------
    >>> from pyogrio.raw import open_arrow
    >>> import pyarrow as pa
    >>> import shapely
    >>>
    >>> with open_arrow(path) as source:
    >>>     meta, stream = source
    >>>     # wrap the arrow stream object in a pyarrow RecordBatchReader
    >>>     reader = pa.RecordBatchReader.from_stream(stream)
    >>>     geom_col = meta["geometry_name"] or "wkb_geometry"
    >>>     for batch in reader:
    >>>         geometries = shapely.from_wkb(batch[geom_col])

    The returned `stream` object needs to be consumed by a library implementing
    the Arrow PyCapsule Protocol. In the above example, pyarrow is used through
    its RecordBatchReader. For this case, you can also specify ``use_pyarrow=True``
    to directly get this result as a short-cut:

    >>> with open_arrow(path, use_pyarrow=True) as source:
    >>>     meta, reader = source
    >>>     geom_col = meta["geometry_name"] or "wkb_geometry"
    >>>     for batch in reader:
    >>>         geometries = shapely.from_wkb(batch[geom_col])

    Returns
    -------
    (dict, pyarrow.RecordBatchReader or ArrowStream)

        Returns a tuple of meta information about the data source in a dict,
        and a data stream object (a generic ArrowStream object, or a pyarrow
        RecordBatchReader if `use_pyarrow` is set to True).

        Meta is: {
            "crs": "<crs>",
            "fields": <ndarray of field names>,
            "dtypes": <ndarray of numpy dtypes corresponding to fields>,
            "ogr_types": <ndarray of OGR types corresponding to fields>,
            "ogr_subtypes": <ndarray of OGR subtypes corresponding to fields>,
            "encoding": "<encoding>",
            "geometry_type": "<geometry_type>",
            "geometry_name": "<name of geometry column in arrow table>",
            "fid_column": "<name of FID column in arrow table>"
        }
    """
    ...
@overload
def open_arrow(
    path_or_buffer: ReadPathOrBuffer,
    /,
    layer: int | str | None = None,
    encoding: str | None = None,
    columns: Collection[str] | None = None,
    read_geometry: bool = True,
    force_2d: bool = False,
    skip_features: int = 0,
    max_features: int | None = None,
    where: str | None = None,
    bbox: tuple[float, float, float, float] | None = None,
    mask: shp.Geometry | None = None,
    fids: ArrayLikeInt | None = None,
    sql: str | None = None,
    sql_dialect: str | None = None,
    return_fids: bool = False,
    batch_size: int = 65536,
    *,
    use_pyarrow: Literal[True],
    datetime_as_string: bool = False,
    **kwargs: Any,  # Dataset open options passed to OGR
) -> AbstractContextManager[tuple[_Meta, pa.RecordBatchReader]]:
    """
    Open OGR data source as a stream of Arrow record batches.

    See docstring of `read` for parameters.

    The returned object is reading from a stream provided by OGR and must not be
    accessed after the OGR dataset has been closed, i.e. after the context manager has
    been closed.

    By default this functions returns a generic stream object implementing
    the `Arrow PyCapsule Protocol`_ (i.e. having an ``__arrow_c_stream__``
    method). This object can then be consumed by your Arrow implementation
    of choice that supports this protocol.
    Optionally, you can specify ``use_pyarrow=True`` to directly get the
    stream as a `pyarrow.RecordBatchReader`.

    .. _Arrow PyCapsule Protocol: https://arrow.apache.org/docs/format/CDataInterface/PyCapsuleInterface.html

    Other Parameters
    ----------------
    batch_size : int (default: 65_536)
        Maximum number of features to retrieve in a batch.
    use_pyarrow : bool (default: False)
        If True, return a pyarrow RecordBatchReader instead of a generic
        ArrowStream object. In the default case, this stream object needs
        to be passed to another library supporting the Arrow PyCapsule
        Protocol to consume the stream of data.
    datetime_as_string : bool, optional (default: False)
        If True, will return datetime dtypes as detected by GDAL as strings,
        as Arrow doesn't support e.g. mixed time zones.

    Examples
    --------
    >>> from pyogrio.raw import open_arrow
    >>> import pyarrow as pa
    >>> import shapely
    >>>
    >>> with open_arrow(path) as source:
    >>>     meta, stream = source
    >>>     # wrap the arrow stream object in a pyarrow RecordBatchReader
    >>>     reader = pa.RecordBatchReader.from_stream(stream)
    >>>     geom_col = meta["geometry_name"] or "wkb_geometry"
    >>>     for batch in reader:
    >>>         geometries = shapely.from_wkb(batch[geom_col])

    The returned `stream` object needs to be consumed by a library implementing
    the Arrow PyCapsule Protocol. In the above example, pyarrow is used through
    its RecordBatchReader. For this case, you can also specify ``use_pyarrow=True``
    to directly get this result as a short-cut:

    >>> with open_arrow(path, use_pyarrow=True) as source:
    >>>     meta, reader = source
    >>>     geom_col = meta["geometry_name"] or "wkb_geometry"
    >>>     for batch in reader:
    >>>         geometries = shapely.from_wkb(batch[geom_col])

    Returns
    -------
    (dict, pyarrow.RecordBatchReader or ArrowStream)

        Returns a tuple of meta information about the data source in a dict,
        and a data stream object (a generic ArrowStream object, or a pyarrow
        RecordBatchReader if `use_pyarrow` is set to True).

        Meta is: {
            "crs": "<crs>",
            "fields": <ndarray of field names>,
            "dtypes": <ndarray of numpy dtypes corresponding to fields>,
            "ogr_types": <ndarray of OGR types corresponding to fields>,
            "ogr_subtypes": <ndarray of OGR subtypes corresponding to fields>,
            "encoding": "<encoding>",
            "geometry_type": "<geometry_type>",
            "geometry_name": "<name of geometry column in arrow table>",
            "fid_column": "<name of FID column in arrow table>"
        }
    """
    ...

def write(
    path: WritePathOrBuffer,
    geometry: np.ndarray | None,  # ndarray of WKB encoded geometries or None
    field_data: Iterable[np.ndarray] | None,
    fields: Iterable[str],
    field_mask: Iterable[np.ndarray | None] | None = None,
    layer: str | None = None,
    driver: str | None = None,
    geometry_type: str | None = None,
    crs: str | None = None,
    encoding: str | None = None,
    promote_to_multi: bool | None = None,
    nan_as_null: bool = True,
    append: bool = False,
    dataset_metadata: dict[str, str] | None = None,
    layer_metadata: dict[str, str] | None = None,
    metadata: dict[str, str] | None = None,
    dataset_options: dict[str, Any] | None = None,
    layer_options: dict[str, Any] | None = None,
    gdal_tz_offsets: dict[str, Any] | None = None,
    **kwargs: Any,  # Additional driver-specific dataset or layer creation options passed to OGR
) -> None:
    """
    Write geometry and field data to an OGR file format.

    Parameters
    ----------
    path : str or io.BytesIO
        path to output file on writeable file system or an io.BytesIO object to
        allow writing to memory.  Will raise NotImplementedError if an open file
        handle is passed; use BytesIO instead.
        NOTE: support for writing to memory is limited to specific drivers.
    geometry : ndarray of WKB encoded geometries or None
        If None, geometries will not be written to output file
    field_data : list-like of shape (num_fields, num_records)
        contains one record per field to be written in same order as fields
    fields : list-like
        contains field names
    field_mask : list-like of ndarrays or None, optional (default: None)
        contains mask arrays indicating null values of the field at the same
        position in the outer list, or None to indicate field does not have
        a mask array
    layer : str, optional (default: None)
        layer name to create.  If writing to memory and layer name is not
        provided, it layer name will be set to a UUID4 value.
    driver : string, optional (default: None)
        The OGR format driver used to write the vector file. By default attempts
        to infer driver from path.  Must be provided to write to memory.
    geometry_type : str, optional (default: None)
        Possible values are: "Unknown", "Point", "LineString", "Polygon",
        "MultiPoint", "MultiLineString", "MultiPolygon" or "GeometryCollection".

        This parameter does not modify the geometry, but it will try to force
        the layer type of the output file to this value. Use this parameter with
        caution because using a wrong layer geometry type may result in errors
        when writing the file, may be ignored by the driver, or may result in
        invalid files.
    crs : str, optional (default: None)
        WKT-encoded CRS of the geometries to be written.
    encoding : str, optional (default: None)
        If present, will be used as the encoding for writing string values to
        the file.  Use with caution, only certain drivers support encodings
        other than UTF-8.
    promote_to_multi : bool, optional (default: None)
        If True, will convert singular geometry types in the data to their
        corresponding multi geometry type for writing. By default, will convert
        mixed singular and multi geometry types to multi geometry types for
        drivers that do not support mixed singular and multi geometry types. If
        False, geometry types will not be promoted, which may result in errors
        or invalid files when attempting to write mixed singular and multi
        geometry types to drivers that do not support such combinations.
    nan_as_null : bool, default True
        For floating point columns (float32 / float64), whether NaN values are
        written as "null" (missing value). Defaults to True because in pandas
        NaNs are typically used as missing value. Note that when set to False,
        behaviour is format specific: some formats don't support NaNs by
        default (e.g. GeoJSON will skip this property) or might treat them as
        null anyway (e.g. GeoPackage).
    append : bool, optional (default: False)
        If True, the data source specified by path already exists, and the
        driver supports appending to an existing data source, will cause the
        data to be appended to the existing records in the data source.  Not
        supported for writing to in-memory files.
        NOTE: append support is limited to specific drivers and GDAL versions.
    dataset_metadata : dict, optional (default: None)
        Metadata to be stored at the dataset level in the output file; limited
        to drivers that support writing metadata, such as GPKG, and silently
        ignored otherwise. Keys and values must be strings.
    layer_metadata : dict, optional (default: None)
        Metadata to be stored at the layer level in the output file; limited to
        drivers that support writing metadata, such as GPKG, and silently
        ignored otherwise. Keys and values must be strings.
    metadata : dict, optional (default: None)
        alias of layer_metadata
    dataset_options : dict, optional
        Dataset creation options (format specific) passed to OGR. Specify as
        a key-value dictionary.
    layer_options : dict, optional
        Layer creation options (format specific) passed to OGR. Specify as
        a key-value dictionary.
    gdal_tz_offsets : dict, optional (default: None)
        Used to handle GDAL time zone offsets for each field contained in dict.
    **kwargs
        Additional driver-specific dataset creation options passed to OGR. Invalid
        options will trigger a warning.
    """
    ...
def write_arrow(
    arrow_obj: SupportsArrowCStream,
    path: WritePathOrBuffer,
    layer: str | None = None,
    driver: str | None = None,
    geometry_name: str | None = None,
    geometry_type: str | None = None,
    crs: str | None = None,
    encoding: str | None = None,
    append: bool = False,
    dataset_metadata: dict[str, str] | None = None,
    layer_metadata: dict[str, str] | None = None,
    metadata: dict[str, str] | None = None,
    dataset_options: dict[str, Any] | None = None,
    layer_options: dict[str, Any] | None = None,
    **kwargs: Any,  # Additional driver-specific dataset or layer creation options passed to OGR
) -> None:
    """
    Write an Arrow-compatible data source to an OGR file format.

    .. _Arrow PyCapsule Protocol: https://arrow.apache.org/docs/format/CDataInterface/PyCapsuleInterface.html

    Parameters
    ----------
    arrow_obj
        The Arrow data to write. This can be any Arrow-compatible tabular data
        object that implements the `Arrow PyCapsule Protocol`_ (i.e. has an
        ``__arrow_c_stream__`` method), for example a pyarrow Table or
        RecordBatchReader.
    path : str or io.BytesIO
        path to output file on writeable file system or an io.BytesIO object to
        allow writing to memory
        NOTE: support for writing to memory is limited to specific drivers.
    layer : str, optional (default: None)
        layer name to create.  If writing to memory and layer name is not
        provided, it layer name will be set to a UUID4 value.
    driver : string, optional (default: None)
        The OGR format driver used to write the vector file. By default attempts
        to infer driver from path.  Must be provided to write to memory.
    geometry_name : str, optional (default: None)
        The name of the column in the input data that will be written as the
        geometry field. Will be inferred from the input data if the geometry
        column is annotated as an "geoarrow.wkb" or "ogc.wkb" extension type.
        Otherwise needs to be specified explicitly.
    geometry_type : str
        The geometry type of the written layer. Currently, this needs to be
        specified explicitly when creating a new layer with geometries.
        Possible values are: "Unknown", "Point", "LineString", "Polygon",
        "MultiPoint", "MultiLineString", "MultiPolygon" or "GeometryCollection".

        This parameter does not modify the geometry, but it will try to force the layer
        type of the output file to this value. Use this parameter with caution because
        using a wrong layer geometry type may result in errors when writing the
        file, may be ignored by the driver, or may result in invalid files.
    crs : str, optional (default: None)
        WKT-encoded CRS of the geometries to be written.
    encoding : str, optional (default: None)
        Only used for the .dbf file of ESRI Shapefiles. If not specified,
        uses the default locale.
    append : bool, optional (default: False)
        If True, the data source specified by path already exists, and the
        driver supports appending to an existing data source, will cause the
        data to be appended to the existing records in the data source.  Not
        supported for writing to in-memory files.
        NOTE: append support is limited to specific drivers and GDAL versions.
    dataset_metadata : dict, optional (default: None)
        Metadata to be stored at the dataset level in the output file; limited
        to drivers that support writing metadata, such as GPKG, and silently
        ignored otherwise. Keys and values must be strings.
    layer_metadata : dict, optional (default: None)
        Metadata to be stored at the layer level in the output file; limited to
        drivers that support writing metadata, such as GPKG, and silently
        ignored otherwise. Keys and values must be strings.
    metadata : dict, optional (default: None)
        alias of layer_metadata
    dataset_options : dict, optional
        Dataset creation options (format specific) passed to OGR. Specify as
        a key-value dictionary.
    layer_options : dict, optional
        Layer creation options (format specific) passed to OGR. Specify as
        a key-value dictionary.
    **kwargs
        Additional driver-specific dataset or layer creation options passed
        to OGR. pyogrio will attempt to automatically pass those keywords
        either as dataset or as layer creation option based on the known
        options for the specific driver. Alternatively, you can use the
        explicit `dataset_options` or `layer_options` keywords to manually
        do this (for example if an option exists as both dataset and layer
        option).
    """
    ...

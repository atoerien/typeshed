"""Functions for reading and writing GeoPandas dataframes."""

import os
from collections.abc import Collection, Mapping
from typing import Any, Literal, overload

import geopandas as gpd
import pandas as pd
import shapely as shp

from ._typing import ArrayLikeInt, ReadPathOrBuffer, WritePathOrBuffer

@overload
def read_dataframe(
    path_or_buffer: ReadPathOrBuffer | os.PathLike[str],
    /,
    layer: int | str | None = None,
    encoding: str | None = None,
    columns: Collection[str] | None = None,
    read_geometry: Literal[True] = True,
    force_2d: bool = False,
    skip_features: int = 0,
    max_features: int | None = None,
    where: str | None = None,
    bbox: tuple[float, float, float, float] | None = None,
    mask: shp.Geometry | None = None,
    fids: ArrayLikeInt | None = None,
    sql: str | None = None,
    sql_dialect: str | None = None,
    fid_as_index: bool = False,
    use_arrow: bool | None = None,
    on_invalid: Literal["raise", "warn", "ignore", "fix"] = "raise",
    arrow_to_pandas_kwargs: Mapping[str, Any] | None = None,
    datetime_as_string: bool = False,
    mixed_offsets_as_utc: bool = True,
    **kwargs: Any,  # Dataset open options passed to OGR
) -> gpd.GeoDataFrame:
    """
    Read from an OGR data source to a GeoPandas GeoDataFrame or Pandas DataFrame.

    If the data source does not have a geometry column or ``read_geometry`` is False,
    a DataFrame will be returned.

    If you read data with datetime columns containing time zone information, check out
    the notes below.

    Requires ``geopandas`` >= 0.8.

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
        If True, will read geometry into a GeoSeries.  If False, a Pandas DataFrame
        will be returned instead.
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
        is only possible when you use the ``sql`` parameter.
        Examples: ``"ISO_A3 = 'CAN'"``, ``"POP_EST > 10000000 AND POP_EST < 100000000"``
    bbox : tuple of (xmin, ymin, xmax, ymax) (default: None)
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
        ``max_features``, ``where``, ``bbox``, ``mask``, or ``sql``). Note that
        the starting index is driver and file specific (e.g. typically 0 for
        Shapefile and 1 for GeoPackage, but can still depend on the specific
        file). The performance of reading a large number of features usings FIDs
        is also driver specific and depends on the value of ``use_arrow``. The order
        of the rows returned is undefined. If you would like to sort based on FID, use
        ``fid_as_index=True`` to have the index of the GeoDataFrame returned set to the
        FIDs of the features read. If ``use_arrow=True``, the number of FIDs is limited
        to 4997 for drivers with 'OGRSQL' as default SQL dialect. To read a larger
        number of FIDs, set ``user_arrow=False``.
    sql : str, optional (default: None)
        The SQL statement to execute. Look at the sql_dialect parameter for more
        information on the syntax to use for the query. When combined with other
        keywords like ``columns``, ``skip_features``, ``max_features``,
        ``where``, ``bbox``, or ``mask``, those are applied after the SQL query.
        Be aware that this can have an impact on performance, (e.g. filtering
        with the ``bbox`` or ``mask`` keywords may not use spatial indexes).
        Cannot be combined with the ``layer`` or ``fids`` keywords.
    sql_dialect : str, optional (default: None)
        The SQL dialect the SQL statement is written in. Possible values:

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

    fid_as_index : bool, optional (default: False)
        If True, will use the FIDs of the features that were read as the
        index of the GeoDataFrame.  May start at 0 or 1 depending on the driver.
    use_arrow : bool, optional (default: False)
        Whether to use Arrow as the transfer mechanism of the read data
        from GDAL to Python (requires GDAL >= 3.6 and `pyarrow` to be
        installed). When enabled, this provides a further speed-up.
        Defaults to False, but this default can also be globally overridden
        by setting the ``PYOGRIO_USE_ARROW=1`` environment variable.
    on_invalid : str, optional (default: "raise")
        The action to take when an invalid geometry is encountered. Possible
        values:

        - **raise**: an exception will be raised if a WKB input geometry is
          invalid.
        - **warn**: invalid WKB geometries will be returned as ``None`` and a
          warning will be raised.
        - **ignore**: invalid WKB geometries will be returned as ``None``
          without a warning.
        - **fix**: an effort is made to fix invalid input geometries (currently
          just unclosed rings). If this is not possible, they are returned as
          ``None`` without a warning. Requires GEOS >= 3.11 and shapely >= 2.1.

    arrow_to_pandas_kwargs : dict, optional (default: None)
        When `use_arrow` is True, these kwargs will be passed to the `to_pandas`_
        call for the arrow to pandas conversion.
    datetime_as_string : bool, optional (default: False)
        If True, will return datetime columns as detected by GDAL as ISO8601
        strings and ``mixed_offsets_as_utc`` will be ignored.
    mixed_offsets_as_utc: bool, optional (default: True)
        By default, datetime columns are read as the pandas datetime64 dtype.
        This can represent the data as-is in the case that the column contains
        only naive datetimes (without time zone information), only UTC datetimes,
        or if all datetimes in the column have the same time zone offset. Note
        that in time zones with daylight saving time, datetimes will have
        different offsets throughout the year!

        For columns that don't comply with the above, i.e. columns that contain
        mixed offsets, the behavior depends on the value of this parameter:

        - If ``True`` (default), such datetimes are converted to UTC. In the case
          of a mixture of time zone aware and naive datetimes, the naive
          datetimes are assumed to be in UTC already. Datetime columns returned
          will always be pandas datetime64.
        - If ``False``, such datetimes with mixed offsets are returned with
          those offsets preserved. Because pandas datetime64 columns don't
          support mixed time zone offsets, such columns are returned as object
          columns with python datetime values with fixed offsets. If you want
          to roundtrip datetimes without data loss, this is the recommended
          option, but you lose the functionality of a datetime64 column.

        If ``datetime_as_string`` is True, this option is ignored.

    **kwargs
        Additional driver-specific dataset open options passed to OGR. Invalid
        options will trigger a warning.

    Returns
    -------
    GeoDataFrame or DataFrame (if no geometry is present)

    Notes
    -----
    When you have datetime columns with time zone information, it is important to
    note that GDAL only represents time zones as UTC offsets, whilst pandas uses
    IANA time zones (via `pytz` or `zoneinfo`). As a result, even if a column in a
    DataFrame contains datetimes in a single time zone, this will often still result
    in mixed time zone offsets being written for time zones where daylight saving
    time is used (e.g. +01:00 and +02:00 offsets for time zone Europe/Brussels). When
    roundtripping through GDAL, the information about the original time zone is
    lost, only the offsets can be preserved. By default, `pyogrio.read_dataframe()`
    will convert columns with mixed offsets to UTC to return a datetime64 column. If
    you want to preserve the original offsets, you can use `datetime_as_string=True`
    or `mixed_offsets_as_utc=False`.

    .. _OGRSQL:

        https://gdal.org/user/ogr_sql_dialect.html#ogr-sql-dialect

    .. _OGRSQL WHERE:

        https://gdal.org/user/ogr_sql_dialect.html#where

    .. _SQLITE:

        https://gdal.org/user/sql_sqlite_dialect.html#sql-sqlite-dialect

    .. _spatialite:

        https://www.gaia-gis.it/gaia-sins/spatialite-sql-latest.html

    .. _to_pandas:

        https://arrow.apache.org/docs/python/generated/pyarrow.Table.html#pyarrow.Table.to_pandas
    """
    ...
@overload
def read_dataframe(
    path_or_buffer: ReadPathOrBuffer | os.PathLike[str],
    /,
    layer: int | str | None = None,
    encoding: str | None = None,
    columns: Collection[str] | None = None,
    *,
    read_geometry: Literal[False],
    force_2d: bool = False,
    skip_features: int = 0,
    max_features: int | None = None,
    where: str | None = None,
    bbox: tuple[float, float, float, float] | None = None,
    mask: shp.Geometry | None = None,
    fids: ArrayLikeInt | None = None,
    sql: str | None = None,
    sql_dialect: str | None = None,
    fid_as_index: bool = False,
    use_arrow: bool | None = None,
    on_invalid: Literal["raise", "warn", "ignore", "fix"] = "raise",
    arrow_to_pandas_kwargs: Mapping[str, Any] | None = None,
    datetime_as_string: bool = False,
    mixed_offsets_as_utc: bool = True,
    **kwargs: Any,  # Dataset open options passed to OGR
) -> pd.DataFrame:
    """
    Read from an OGR data source to a GeoPandas GeoDataFrame or Pandas DataFrame.

    If the data source does not have a geometry column or ``read_geometry`` is False,
    a DataFrame will be returned.

    If you read data with datetime columns containing time zone information, check out
    the notes below.

    Requires ``geopandas`` >= 0.8.

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
        If True, will read geometry into a GeoSeries.  If False, a Pandas DataFrame
        will be returned instead.
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
        is only possible when you use the ``sql`` parameter.
        Examples: ``"ISO_A3 = 'CAN'"``, ``"POP_EST > 10000000 AND POP_EST < 100000000"``
    bbox : tuple of (xmin, ymin, xmax, ymax) (default: None)
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
        ``max_features``, ``where``, ``bbox``, ``mask``, or ``sql``). Note that
        the starting index is driver and file specific (e.g. typically 0 for
        Shapefile and 1 for GeoPackage, but can still depend on the specific
        file). The performance of reading a large number of features usings FIDs
        is also driver specific and depends on the value of ``use_arrow``. The order
        of the rows returned is undefined. If you would like to sort based on FID, use
        ``fid_as_index=True`` to have the index of the GeoDataFrame returned set to the
        FIDs of the features read. If ``use_arrow=True``, the number of FIDs is limited
        to 4997 for drivers with 'OGRSQL' as default SQL dialect. To read a larger
        number of FIDs, set ``user_arrow=False``.
    sql : str, optional (default: None)
        The SQL statement to execute. Look at the sql_dialect parameter for more
        information on the syntax to use for the query. When combined with other
        keywords like ``columns``, ``skip_features``, ``max_features``,
        ``where``, ``bbox``, or ``mask``, those are applied after the SQL query.
        Be aware that this can have an impact on performance, (e.g. filtering
        with the ``bbox`` or ``mask`` keywords may not use spatial indexes).
        Cannot be combined with the ``layer`` or ``fids`` keywords.
    sql_dialect : str, optional (default: None)
        The SQL dialect the SQL statement is written in. Possible values:

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

    fid_as_index : bool, optional (default: False)
        If True, will use the FIDs of the features that were read as the
        index of the GeoDataFrame.  May start at 0 or 1 depending on the driver.
    use_arrow : bool, optional (default: False)
        Whether to use Arrow as the transfer mechanism of the read data
        from GDAL to Python (requires GDAL >= 3.6 and `pyarrow` to be
        installed). When enabled, this provides a further speed-up.
        Defaults to False, but this default can also be globally overridden
        by setting the ``PYOGRIO_USE_ARROW=1`` environment variable.
    on_invalid : str, optional (default: "raise")
        The action to take when an invalid geometry is encountered. Possible
        values:

        - **raise**: an exception will be raised if a WKB input geometry is
          invalid.
        - **warn**: invalid WKB geometries will be returned as ``None`` and a
          warning will be raised.
        - **ignore**: invalid WKB geometries will be returned as ``None``
          without a warning.
        - **fix**: an effort is made to fix invalid input geometries (currently
          just unclosed rings). If this is not possible, they are returned as
          ``None`` without a warning. Requires GEOS >= 3.11 and shapely >= 2.1.

    arrow_to_pandas_kwargs : dict, optional (default: None)
        When `use_arrow` is True, these kwargs will be passed to the `to_pandas`_
        call for the arrow to pandas conversion.
    datetime_as_string : bool, optional (default: False)
        If True, will return datetime columns as detected by GDAL as ISO8601
        strings and ``mixed_offsets_as_utc`` will be ignored.
    mixed_offsets_as_utc: bool, optional (default: True)
        By default, datetime columns are read as the pandas datetime64 dtype.
        This can represent the data as-is in the case that the column contains
        only naive datetimes (without time zone information), only UTC datetimes,
        or if all datetimes in the column have the same time zone offset. Note
        that in time zones with daylight saving time, datetimes will have
        different offsets throughout the year!

        For columns that don't comply with the above, i.e. columns that contain
        mixed offsets, the behavior depends on the value of this parameter:

        - If ``True`` (default), such datetimes are converted to UTC. In the case
          of a mixture of time zone aware and naive datetimes, the naive
          datetimes are assumed to be in UTC already. Datetime columns returned
          will always be pandas datetime64.
        - If ``False``, such datetimes with mixed offsets are returned with
          those offsets preserved. Because pandas datetime64 columns don't
          support mixed time zone offsets, such columns are returned as object
          columns with python datetime values with fixed offsets. If you want
          to roundtrip datetimes without data loss, this is the recommended
          option, but you lose the functionality of a datetime64 column.

        If ``datetime_as_string`` is True, this option is ignored.

    **kwargs
        Additional driver-specific dataset open options passed to OGR. Invalid
        options will trigger a warning.

    Returns
    -------
    GeoDataFrame or DataFrame (if no geometry is present)

    Notes
    -----
    When you have datetime columns with time zone information, it is important to
    note that GDAL only represents time zones as UTC offsets, whilst pandas uses
    IANA time zones (via `pytz` or `zoneinfo`). As a result, even if a column in a
    DataFrame contains datetimes in a single time zone, this will often still result
    in mixed time zone offsets being written for time zones where daylight saving
    time is used (e.g. +01:00 and +02:00 offsets for time zone Europe/Brussels). When
    roundtripping through GDAL, the information about the original time zone is
    lost, only the offsets can be preserved. By default, `pyogrio.read_dataframe()`
    will convert columns with mixed offsets to UTC to return a datetime64 column. If
    you want to preserve the original offsets, you can use `datetime_as_string=True`
    or `mixed_offsets_as_utc=False`.

    .. _OGRSQL:

        https://gdal.org/user/ogr_sql_dialect.html#ogr-sql-dialect

    .. _OGRSQL WHERE:

        https://gdal.org/user/ogr_sql_dialect.html#where

    .. _SQLITE:

        https://gdal.org/user/sql_sqlite_dialect.html#sql-sqlite-dialect

    .. _spatialite:

        https://www.gaia-gis.it/gaia-sins/spatialite-sql-latest.html

    .. _to_pandas:

        https://arrow.apache.org/docs/python/generated/pyarrow.Table.html#pyarrow.Table.to_pandas
    """
    ...

def write_dataframe(
    df: pd.DataFrame,
    path: WritePathOrBuffer,
    layer: str | None = None,
    driver: str | None = None,
    encoding: str | None = None,
    geometry_type: str | None = None,
    promote_to_multi: bool | None = None,
    nan_as_null: bool = True,
    append: bool = False,
    use_arrow: bool | None = None,
    dataset_metadata: dict[str, Any] | None = None,
    layer_metadata: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
    dataset_options: dict[str, Any] | None = None,
    layer_options: dict[str, Any] | None = None,
    **kwargs: Any,  # Additional driver-specific dataset or layer creation options passed to OGR
) -> None:
    """
    Write GeoPandas GeoDataFrame to an OGR file format.

    Parameters
    ----------
    df : GeoDataFrame or DataFrame
        The data to write. For attribute columns of the "object" dtype,
        all values will be converted to strings to be written to the
        output file, except None and np.nan, which will be set to NULL
        in the output file.
    path : str or io.BytesIO
        path to output file on writeable file system or an io.BytesIO object to
        allow writing to memory.  Will raise NotImplementedError if an open file
        handle is passed; use BytesIO instead.
        NOTE: support for writing to memory is limited to specific drivers.
    layer : str, optional (default: None)
        layer name to create.  If writing to memory and layer name is not
        provided, it layer name will be set to a UUID4 value.
    driver : string, optional (default: None)
        The OGR format driver used to write the vector file. By default attempts
        to infer driver from path.  Must be provided to write to memory.
    encoding : str, optional (default: None)
        If present, will be used as the encoding for writing string values to
        the file.  Use with caution, only certain drivers support encodings
        other than UTF-8.
    geometry_type : string, optional (default: None)
        By default, the geometry type of the layer will be inferred from the
        data, after applying the promote_to_multi logic. If the data only contains a
        single geometry type (after applying the logic of promote_to_multi), this type
        is used for the layer. If the data (still) contains mixed geometry types, the
        output layer geometry type will be set to "Unknown".

        This parameter does not modify the geometry, but it will try to force the layer
        type of the output file to this value. Use this parameter with caution because
        using a non-default layer geometry type may result in errors when writing the
        file, may be ignored by the driver, or may result in invalid files. Possible
        values are: "Unknown", "Point", "LineString", "Polygon", "MultiPoint",
        "MultiLineString", "MultiPolygon" or "GeometryCollection".
    promote_to_multi : bool, optional (default: None)
        If True, will convert singular geometry types in the data to their
        corresponding multi geometry type for writing. By default, will convert
        mixed singular and multi geometry types to multi geometry types for drivers
        that do not support mixed singular and multi geometry types. If False, geometry
        types will not be promoted, which may result in errors or invalid files when
        attempting to write mixed singular and multi geometry types to drivers that do
        not support such combinations.
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
    use_arrow : bool, optional (default: False)
        Whether to use Arrow as the transfer mechanism of the data to write
        from Python to GDAL (requires GDAL >= 3.8 and `pyarrow` to be
        installed). When enabled, this provides a further speed-up.
        Defaults to False, but this default can also be globally overridden
        by setting the ``PYOGRIO_USE_ARROW=1`` environment variable.
        Using Arrow does not support writing an object-dtype column with
        mixed types.
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

    Notes
    -----
    When you have datetime columns with time zone information, it is important to
    note that GDAL only represents time zones as UTC offsets, whilst pandas uses
    IANA time zones (via `pytz` or `zoneinfo`). As a result, even if a column in a
    DataFrame contains datetimes in a single time zone, this will often still result
    in mixed time zone offsets being written for time zones where daylight saving
    time is used (e.g. +01:00 and +02:00 offsets for time zone Europe/Brussels).

    Object dtype columns containing `datetime` or `pandas.Timestamp` objects will
    also be written as datetime fields, preserving time zone information where possible.
    """
    ...

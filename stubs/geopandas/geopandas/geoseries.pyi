import io
import json
import os
from _typeshed import Incomplete, SupportsRead
from collections.abc import Callable, Hashable
from typing import Any, Literal, final, overload
from typing_extensions import Self

import pandas as pd
from numpy.typing import ArrayLike
from pandas._typing import Axes, Dtype
from pyproj import CRS
from shapely.geometry.base import BaseGeometry

from ._decorator import doc
from .array import GeometryArray
from .base import GeoPandasBase, _BboxLike, _ClipMask, _ConvertibleToCRS, _ConvertibleToGeoSeries, _MaskLike
from .explore import _explore_geoseries
from .io._geoarrow import GeoArrowArray
from .plotting import plot_series

class GeoSeries(GeoPandasBase, pd.Series[BaseGeometry]):  # type: ignore[type-var,misc]  # pyright: ignore[reportInvalidTypeArguments]
    """
    A Series object designed to store shapely geometry objects.

    Parameters
    ----------
    data : array-like, dict, scalar value
        The geometries to store in the GeoSeries.
    index : array-like or Index
        The index for the GeoSeries.
    crs : value (optional)
        Coordinate Reference System of the geometry objects. Can be anything accepted by
        :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
        such as an authority string (eg "EPSG:4326") or a WKT string.

    kwargs
        Additional arguments passed to the Series constructor,
         e.g. ``name``.

    Examples
    --------
    >>> from shapely.geometry import Point
    >>> s = geopandas.GeoSeries([Point(1, 1), Point(2, 2), Point(3, 3)])
    >>> s
    0    POINT (1 1)
    1    POINT (2 2)
    2    POINT (3 3)
    dtype: geometry

    >>> s = geopandas.GeoSeries(
    ...     [Point(1, 1), Point(2, 2), Point(3, 3)], crs="EPSG:3857"
    ... )
    >>> s.crs  # doctest: +SKIP
    <Projected CRS: EPSG:3857>
    Name: WGS 84 / Pseudo-Mercator
    Axis Info [cartesian]:
    - X[east]: Easting (metre)
    - Y[north]: Northing (metre)
    Area of Use:
    - name: World - 85°S to 85°N
    - bounds: (-180.0, -85.06, 180.0, 85.06)
    Coordinate Operation:
    - name: Popular Visualisation Pseudo-Mercator
    - method: Popular Visualisation Pseudo Mercator
    Datum: World Geodetic System 1984
    - Ellipsoid: WGS 84
    - Prime Meridian: Greenwich

    >>> s = geopandas.GeoSeries(
    ...    [Point(1, 1), Point(2, 2), Point(3, 3)], index=["a", "b", "c"], crs=4326
    ... )
    >>> s
    a    POINT (1 1)
    b    POINT (2 2)
    c    POINT (3 3)
    dtype: geometry

    >>> s.crs
    <Geographic 2D CRS: EPSG:4326>
    Name: WGS 84
    Axis Info [ellipsoidal]:
    - Lat[north]: Geodetic latitude (degree)
    - Lon[east]: Geodetic longitude (degree)
    Area of Use:
    - name: World.
    - bounds: (-180.0, -90.0, 180.0, 90.0)
    Datum: World Geodetic System 1984 ensemble
    - Ellipsoid: WGS 84
    - Prime Meridian: Greenwich

    See Also
    --------
    GeoDataFrame
    pandas.Series
    """
    # Override the weird annotation of Series.__new__ in pandas-stubs
    def __new__(
        self,
        data: _ConvertibleToGeoSeries | None = None,
        index: Axes | None = None,
        crs: _ConvertibleToCRS | None = None,
        *,
        dtype: Dtype | None = None,
        name: Hashable = None,
        copy: bool | None = None,
        fastpath: bool = False,
    ) -> Self: ...
    def __init__(
        self,
        data: _ConvertibleToGeoSeries | None = None,
        index: Axes | None = None,
        crs: _ConvertibleToCRS | None = None,
        *,
        dtype: Dtype | None = None,
        name: Hashable = None,
        copy: bool | None = None,
        fastpath: bool = False,
    ) -> None: ...
    @final  # type: ignore[misc]
    def copy(self, deep: bool = True) -> Self:
        """
        Make a copy of this object's indices and data.

        When ``deep=True`` (default), a new object will be created with a
        copy of the calling object's data and indices. Modifications to
        the data or indices of the copy will not be reflected in the
        original object (see notes below).

        When ``deep=False``, a new object will be created without copying
        the calling object's data or index (only references to the data
        and index are copied). With Copy-on-Write, changes to the original
        will *not* be reflected in the shallow copy (and vice versa). The
        shallow copy uses a lazy (deferred) copy mechanism that copies the
        data only when any changes to the original or shallow copy are made,
        ensuring memory efficiency while maintaining data integrity.

        .. note::
            In pandas versions prior to 3.0, the default behavior without
            Copy-on-Write was different: changes to the original *were* reflected
            in the shallow copy (and vice versa). See the :ref:`Copy-on-Write
            user guide <copy_on_write>` for more information.

        Parameters
        ----------
        deep : bool, default True
            Make a deep copy, including a copy of the data and the indices.
            With ``deep=False`` neither the indices nor the data are copied.

        Returns
        -------
        Series or DataFrame
            Object type matches caller.

        See Also
        --------
        copy.copy : Return a shallow copy of an object.
        copy.deepcopy : Return a deep copy of an object.

        Notes
        -----
        When ``deep=True``, data is copied but actual Python objects
        will not be copied recursively, only the reference to the object.
        This is in contrast to `copy.deepcopy` in the Standard Library,
        which recursively copies object data (see examples below).

        While ``Index`` objects are copied when ``deep=True``, the underlying
        numpy array is not copied for performance reasons. Since ``Index`` is
        immutable, the underlying data can be safely shared and a copy
        is not needed.

        Since pandas is not thread safe, see the
        :ref:`gotchas <gotchas.thread-safety>` when copying in a threading
        environment.

        Copy-on-Write protects shallow copies against accidental modifications.
        This means that any changes to the copied data would make a new copy
        of the data upon write (and vice versa). Changes made to either the
        original or copied variable would not be reflected in the counterpart.
        See :ref:`Copy_on_Write <copy_on_write>` for more information.

        Examples
        --------
        >>> s = pd.Series([1, 2], index=["a", "b"])
        >>> s
        a    1
        b    2
        dtype: int64

        >>> s_copy = s.copy(deep=True)
        >>> s_copy
        a    1
        b    2
        dtype: int64

        Due to Copy-on-Write, shallow copies still protect data modifications.
        Note shallow does not get modified below.

        >>> s = pd.Series([1, 2], index=["a", "b"])
        >>> shallow = s.copy(deep=False)
        >>> s.iloc[1] = 200
        >>> shallow
        a    1
        b    2
        dtype: int64

        When the data has object dtype, even a deep copy does not copy the
        underlying Python objects. Updating a nested data object will be
        reflected in the deep copy.

        >>> s = pd.Series([[1, 2], [3, 4]])
        >>> deep = s.copy()
        >>> s[0][0] = 10
        >>> s
        0    [10, 2]
        1     [3, 4]
        dtype: object
        >>> deep
        0    [10, 2]
        1     [3, 4]
        dtype: object
        """
        ...
    @property
    def values(self) -> GeometryArray:
        """
        Return Series as ndarray or ndarray-like depending on the dtype.

        .. warning::

           We recommend using :attr:`Series.array` or
           :meth:`Series.to_numpy`, depending on whether you need
           a reference to the underlying data or a NumPy array.

        Returns
        -------
        numpy.ndarray or ndarray-like

        See Also
        --------
        Series.array : Reference to the underlying data.
        Series.to_numpy : A NumPy array representing the underlying data.

        Examples
        --------
        >>> pd.Series([1, 2, 3]).values
        array([1, 2, 3])

        >>> pd.Series(list("aabc")).values
        <ArrowStringArray>
        ['a', 'a', 'b', 'c']
        Length: 4, dtype: str

        >>> pd.Series(list("aabc")).astype("category").values
        ['a', 'a', 'b', 'c']
        Categories (3, str): ['a', 'b', 'c']

        Timezone aware datetime data is converted to UTC:

        >>> pd.Series(pd.date_range("20130101", periods=3, tz="US/Eastern")).values
        array(['2013-01-01T05:00:00.000000',
               '2013-01-02T05:00:00.000000',
               '2013-01-03T05:00:00.000000'], dtype='datetime64[us]')
        """
        ...
    @property
    def geometry(self) -> Self: ...
    @property
    def x(self) -> pd.Series[float]:
        """
        Return the x location of point geometries in a GeoSeries.

        Returns
        -------
        pandas.Series

        Examples
        --------
        >>> from shapely.geometry import Point
        >>> s = geopandas.GeoSeries([Point(1, 1), Point(2, 2), Point(3, 3)])
        >>> s.x
        0    1.0
        1    2.0
        2    3.0
        dtype: float64

        See Also
        --------
        GeoSeries.y
        GeoSeries.z
        """
        ...
    @property
    def y(self) -> pd.Series[float]:
        """
        Return the y location of point geometries in a GeoSeries.

        Returns
        -------
        pandas.Series

        Examples
        --------
        >>> from shapely.geometry import Point
        >>> s = geopandas.GeoSeries([Point(1, 1), Point(2, 2), Point(3, 3)])
        >>> s.y
        0    1.0
        1    2.0
        2    3.0
        dtype: float64

        See Also
        --------
        GeoSeries.x
        GeoSeries.z
        GeoSeries.m
        """
        ...
    @property
    def z(self) -> pd.Series[float]:
        """
        Return the z location of point geometries in a GeoSeries.

        Returns
        -------
        pandas.Series

        Examples
        --------
        >>> from shapely.geometry import Point
        >>> s = geopandas.GeoSeries([Point(1, 1, 1), Point(2, 2, 2), Point(3, 3, 3)])
        >>> s.z
        0    1.0
        1    2.0
        2    3.0
        dtype: float64

        See Also
        --------
        GeoSeries.x
        GeoSeries.y
        GeoSeries.m
        """
        ...
    @property
    def m(self) -> pd.Series[float]:
        """
        Return the m coordinate of point geometries in a GeoSeries.

        Requires Shapely >= 2.1.

        .. versionadded:: 1.1.0

        Returns
        -------
        pandas.Series

        Examples
        --------
        >>> from shapely.geometry import Point
        >>> s = geopandas.GeoSeries.from_wkt(
        ...     [
        ...         "POINT M (2 3 5)",
        ...         "POINT M (1 2 3)",
        ...     ]
        ... )
        >>> s
        0    POINT M (2 3 5)
        1    POINT M (1 2 3)
        dtype: geometry

        >>> s.m
        0    5.0
        1    3.0
        dtype: float64

        See Also
        --------
        GeoSeries.x
        GeoSeries.y
        GeoSeries.z
        """
        ...
    # Keep inline with GeoDataFrame.from_file and geopandas.io.file._read_file
    @classmethod
    def from_file(
        cls,
        filename: str | os.PathLike[str] | SupportsRead[Incomplete],
        *,
        bbox: _BboxLike | None = None,
        mask: _MaskLike | None = None,
        rows: int | slice | None = None,
        engine: Literal["fiona", "pyogrio"] | None = None,
        ignore_geometry: Literal[False] = False,
        layer: int | str | None = None,
        encoding: str | None = None,
        **kwargs,  # engine dependent
    ) -> GeoSeries:
        """
        Alternate constructor to create a ``GeoSeries`` from a file.

        Can load a ``GeoSeries`` from a file from any format recognized by
        `pyogrio`. See http://pyogrio.readthedocs.io/ for details.
        From a file with attributes loads only geometry column. Note that to do
        that, GeoPandas first loads the whole GeoDataFrame.

        Parameters
        ----------
        filename : str
            File path or file handle to read from. Depending on which kwargs
            are included, the content of filename may vary. See
            :func:`pyogrio.read_dataframe` for usage details.
        kwargs : key-word arguments
            These arguments are passed to :func:`pyogrio.read_dataframe`, and can be
            used to access multi-layer data, data stored within archives (zip files),
            etc.

        Examples
        --------
        >>> import geodatasets
        >>> path = geodatasets.get_path('nybb')
        >>> s = geopandas.GeoSeries.from_file(path)
        >>> s
        0    MULTIPOLYGON (((970217.022 145643.332, 970227....
        1    MULTIPOLYGON (((1029606.077 156073.814, 102957...
        2    MULTIPOLYGON (((1021176.479 151374.797, 102100...
        3    MULTIPOLYGON (((981219.056 188655.316, 980940....
        4    MULTIPOLYGON (((1012821.806 229228.265, 101278...
        Name: geometry, dtype: geometry

        See Also
        --------
        read_file : read file to GeoDataFrame
        """
        ...
    @classmethod
    def from_wkb(
        cls,
        data: ArrayLike,  # array-like of bytes handled by shapely.from_wkb(data)
        index: Axes | None = None,
        crs: _ConvertibleToCRS | None = None,
        on_invalid: Literal["raise", "warn", "ignore", "fix"] = "raise",
        *,
        dtype: Dtype | None = None,
        name: Hashable = None,
        copy: bool | None = None,
        fastpath: bool = False,
    ) -> Self:
        r"""
        Alternate constructor to create a ``GeoSeries``
        from a list or array of WKB objects.

        Parameters
        ----------
        data : array-like or Series
            Series, list or array of WKB objects
        index : array-like or Index
            The index for the GeoSeries.
        crs : value, optional
            Coordinate Reference System of the geometry objects. Can be anything
            accepted by
            :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
            such as an authority string (eg "EPSG:4326") or a WKT string.
        on_invalid: {"raise", "warn", "ignore"}, default "raise"
            - raise: an exception will be raised if a WKB input geometry is invalid.
            - warn: a warning will be raised and invalid WKB geometries will be returned
              as None.
            - ignore: invalid WKB geometries will be returned as None without a warning.
            - fix: an effort is made to fix invalid input geometries (e.g. close
              unclosed rings). If this is not possible, they are returned as ``None``
              without a warning. Requires GEOS >= 3.11 and shapely >= 2.1.

        kwargs
            Additional arguments passed to the Series constructor,
            e.g. ``name``.

        Returns
        -------
        GeoSeries

        See Also
        --------
        GeoSeries.from_wkt

        Examples
        --------
        >>> wkbs = [
        ... (
        ...     b"\x01\x01\x00\x00\x00\x00\x00\x00\x00"
        ...     b"\x00\x00\xf0?\x00\x00\x00\x00\x00\x00\xf0?"
        ... ),
        ... (
        ...     b"\x01\x01\x00\x00\x00\x00\x00\x00\x00"
        ...     b"\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00@"
        ... ),
        ... (
        ...    b"\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00"
        ...    b"\x00\x08@\x00\x00\x00\x00\x00\x00\x08@"
        ... ),
        ... ]
        >>> s = geopandas.GeoSeries.from_wkb(wkbs)
        >>> s
        0    POINT (1 1)
        1    POINT (2 2)
        2    POINT (3 3)
        dtype: geometry
        """
        ...
    @classmethod
    def from_wkt(
        cls,
        data: ArrayLike,  # array-like of str handled by shapely.from_wkt(data)
        index: Axes | None = None,
        crs: _ConvertibleToCRS | None = None,
        on_invalid: Literal["raise", "warn", "ignore", "fix"] = "raise",
        *,
        dtype: Dtype | None = None,
        name: Hashable = None,
        copy: bool | None = None,
        fastpath: bool = False,
    ) -> Self:
        """
        Alternate constructor to create a ``GeoSeries``
        from a list or array of WKT objects.

        Parameters
        ----------
        data : array-like, Series
            Series, list, or array of WKT objects
        index : array-like or Index
            The index for the GeoSeries.
        crs : value, optional
            Coordinate Reference System of the geometry objects. Can be anything
            accepted by
            :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
            such as an authority string (eg "EPSG:4326") or a WKT string.
        on_invalid : {"raise", "warn", "ignore"}, default "raise"
            - raise: an exception will be raised if a WKT input geometry is invalid.
            - warn: a warning will be raised and invalid WKT geometries will be
              returned as ``None``.
            - ignore: invalid WKT geometries will be returned as ``None`` without a
              warning.
            - fix: an effort is made to fix invalid input geometries (e.g. close
              unclosed rings). If this is not possible, they are returned as ``None``
              without a warning. Requires GEOS >= 3.11 and shapely >= 2.1.

        kwargs
            Additional arguments passed to the Series constructor,
            e.g. ``name``.

        Returns
        -------
        GeoSeries

        See Also
        --------
        GeoSeries.from_wkb

        Examples
        --------
        >>> wkts = [
        ... 'POINT (1 1)',
        ... 'POINT (2 2)',
        ... 'POINT (3 3)',
        ... ]
        >>> s = geopandas.GeoSeries.from_wkt(wkts)
        >>> s
        0    POINT (1 1)
        1    POINT (2 2)
        2    POINT (3 3)
        dtype: geometry
        """
        ...
    @classmethod
    def from_xy(
        cls,
        # x, y, z: array-like of floats handled by np.asarray(..., dtype="float64")
        x: ArrayLike,
        y: ArrayLike,
        z: ArrayLike | None = None,
        index: Axes | None = None,
        crs: _ConvertibleToCRS | None = None,
        *,
        dtype: Dtype | None = None,
        name: Hashable = None,
        copy: bool | None = None,
        fastpath: bool = False,
    ) -> Self:
        """
        Alternate constructor to create a :class:`~geopandas.GeoSeries` of Point
        geometries from lists or arrays of x, y(, z) coordinates.

        In case of geographic coordinates, it is assumed that longitude is captured
        by ``x`` coordinates and latitude by ``y``.

        Parameters
        ----------
        x, y, z : iterable
        index : array-like or Index, optional
            The index for the GeoSeries. If not given and all coordinate inputs
            are Series with an equal index, that index is used.
        crs : value, optional
            Coordinate Reference System of the geometry objects. Can be anything
            accepted by
            :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
            such as an authority string (eg "EPSG:4326") or a WKT string.
        **kwargs
            Additional arguments passed to the Series constructor,
            e.g. ``name``.

        Returns
        -------
        GeoSeries

        See Also
        --------
        GeoSeries.from_wkt
        points_from_xy

        Examples
        --------
        >>> x = [2.5, 5, -3.0]
        >>> y = [0.5, 1, 1.5]
        >>> s = geopandas.GeoSeries.from_xy(x, y, crs="EPSG:4326")
        >>> s
        0    POINT (2.5 0.5)
        1    POINT (5 1)
        2    POINT (-3 1.5)
        dtype: geometry
        """
        ...
    @classmethod
    def from_arrow(
        cls,
        arr,
        *,
        # GeoSeries constructor kwargs
        index: Axes | None = None,
        crs: _ConvertibleToCRS | None = None,
        dtype: Dtype | None = None,
        name: Hashable = None,
        copy: bool | None = None,
        fastpath: bool = False,
    ) -> Self:
        """
        Construct a GeoSeries from an Arrow array object with a GeoArrow
        extension type.

        See https://geoarrow.org/ for details on the GeoArrow specification.

        This functions accepts any Arrow array object implementing
        the `Arrow PyCapsule Protocol`_ (i.e. having an ``__arrow_c_array__``
        method).

        .. _Arrow PyCapsule Protocol: https://arrow.apache.org/docs/format/CDataInterface/PyCapsuleInterface.html

        .. versionadded:: 1.0

        Parameters
        ----------
        arr : pyarrow.Array, Arrow array
            Any array object implementing the Arrow PyCapsule Protocol
            (i.e. has an ``__arrow_c_array__`` or ``__arrow_c_stream__``
            method). The type of the array should be one of the
            geoarrow geometry types.
        **kwargs
            Other parameters passed to the GeoSeries constructor.

        Returns
        -------
        GeoSeries
        """
        ...
    @property
    def __geo_interface__(self) -> dict[str, Any]:
        """
        Returns a ``GeoSeries`` as a python feature collection.

        Implements the `geo_interface`. The returned python data structure
        represents the ``GeoSeries`` as a GeoJSON-like ``FeatureCollection``.
        Note that the features will have an empty ``properties`` dict as they
        don't have associated attributes (geometry only).

        Examples
        --------
        >>> from shapely.geometry import Point
        >>> s = geopandas.GeoSeries([Point(1, 1), Point(2, 2), Point(3, 3)])
        >>> s.__geo_interface__
        {'type': 'FeatureCollection', 'features': [{'id': '0', 'type': 'Feature', 'properties': {}, 'geometry': {'type': 'Point', 'coordinates': (1.0, 1.0)}, 'bbox': (1.0, 1.0, 1.0, 1.0)}, {'id': '1', 'type': 'Feature', 'properties': {}, 'geometry': {'type': 'Point', 'coordinates': (2.0, 2.0)}, 'bbox': (2.0, 2.0, 2.0, 2.0)}, {'id': '2', 'type': 'Feature', 'properties': {}, 'geometry': {'type': 'Point', 'coordinates': (3.0, 3.0)}, 'bbox': (3.0, 3.0, 3.0, 3.0)}], 'bbox': (1.0, 1.0, 3.0, 3.0)}
        """
        ...
    # Keep method to_file roughly in line with GeoDataFrame.to_file
    def to_file(
        self,
        filename: str | os.PathLike[str] | io.BytesIO,
        driver: str | None = None,
        index: bool | None = None,
        *,
        # kwargs from `_to_file` function
        schema: dict[str, Incomplete] | None = None,
        mode: Literal["w", "a"] = "w",
        crs: _ConvertibleToCRS | None = None,
        engine: Literal["fiona", "pyogrio"] | None = None,
        metadata: dict[str, str] | None = None,
        # kwargs extracted from engines
        layer: int | str | None = None,
        encoding: str | None = None,
        overwrite: bool | None = ...,
        **kwargs,  # engine and driver dependent
    ) -> None:
        """
        Write the ``GeoSeries`` to a file.

        By default, an ESRI shapefile is written, but any OGR data source
        supported by Pyogrio or Fiona can be written.

        Parameters
        ----------
        filename : string
            File path or file handle to write to. The path may specify a
            GDAL VSI scheme.
        driver : string, default None
            The OGR format driver used to write the vector file.
            If not specified, it attempts to infer it from the file extension.
            If no extension is specified, it saves ESRI Shapefile to a folder.
        index : bool, default None
            If True, write index into one or more columns (for MultiIndex).
            Default None writes the index into one or more columns only if
            the index is named, is a MultiIndex, or has a non-integer data
            type. If False, no index is written.

            .. versionadded:: 0.7
                Previously the index was not written.
        mode : string, default 'w'
            The write mode, 'w' to overwrite the existing file and 'a' to append.
            Not all drivers support appending. The drivers that support appending
            are listed in fiona.supported_drivers or
            https://github.com/Toblerity/Fiona/blob/master/fiona/drvsupport.py
        crs : pyproj.CRS, default None
            If specified, the CRS is passed to Fiona to
            better control how the file is written. If None, GeoPandas
            will determine the crs based on crs df attribute.
            The value can be anything accepted
            by :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
            such as an authority string (eg "EPSG:4326") or a WKT string. The keyword
            is not supported for the "pyogrio" engine.
        engine : str, "pyogrio" or "fiona"
            The underlying library that is used to write the file. Currently, the
            supported options are "pyogrio" and "fiona". Defaults to "pyogrio" if
            installed, otherwise tries "fiona".
        **kwargs :
            Keyword args to be passed to the engine, and can be used to write
            to multi-layer data, store data within archives (zip files), etc.
            In case of the "pyogrio" engine, the keyword arguments are passed to
            `pyogrio.write_dataframe`. In case of the "fiona" engine, the keyword
            arguments are passed to fiona.open`. For more information on possible
            keywords, type: ``import pyogrio; help(pyogrio.write_dataframe)``.

        See Also
        --------
        GeoDataFrame.to_file : write GeoDataFrame to file
        read_file : read file to GeoDataFrame

        Examples
        --------
        >>> s.to_file('series.shp')  # doctest: +SKIP

        >>> s.to_file('series.gpkg', driver='GPKG', layer='name1')  # doctest: +SKIP

        >>> s.to_file('series.geojson', driver='GeoJSON')  # doctest: +SKIP
        """
        ...
    # *** `__getitem__`, `sort_index` and `take` are annotated with `-> Self` in pandas-stubs; no need to override them ***
    # *** `apply` annotation in pandas-stubs is compatible except for deprecated `convert_dtype` argument ***
    # def apply(self, func, convert_dtype: bool | None = None, args=(), **kwargs): ...
    def isna(self) -> pd.Series[bool]:
        """
        Detect missing values.

        Historically, NA values in a GeoSeries could be represented by
        empty geometric objects, in addition to standard representations
        such as None and np.nan. This behaviour is changed in version 0.6.0,
        and now only actual missing values return True. To detect empty
        geometries, use ``GeoSeries.is_empty`` instead.

        Returns
        -------
        A boolean pandas Series of the same size as the GeoSeries,
        True where a value is NA.

        Examples
        --------
        >>> from shapely.geometry import Polygon
        >>> s = geopandas.GeoSeries(
        ...     [Polygon([(0, 0), (1, 1), (0, 1)]), None, Polygon([])]
        ... )
        >>> s
        0    POLYGON ((0 0, 1 1, 0 1, 0 0))
        1                              None
        2                     POLYGON EMPTY
        dtype: geometry

        >>> s.isna()
        0    False
        1     True
        2    False
        dtype: bool

        See Also
        --------
        GeoSeries.notna : inverse of isna
        GeoSeries.is_empty : detect empty geometries
        """
        ...
    def isnull(self) -> pd.Series[bool]:
        """Alias for `isna` method. See `isna` for more detail."""
        ...
    def notna(self) -> pd.Series[bool]:
        """
        Detect non-missing values.

        Historically, NA values in a GeoSeries could be represented by
        empty geometric objects, in addition to standard representations
        such as None and np.nan. This behaviour is changed in version 0.6.0,
        and now only actual missing values return False. To detect empty
        geometries, use ``~GeoSeries.is_empty`` instead.

        Returns
        -------
        A boolean pandas Series of the same size as the GeoSeries,
        False where a value is NA.

        Examples
        --------
        >>> from shapely.geometry import Polygon
        >>> s = geopandas.GeoSeries(
        ...     [Polygon([(0, 0), (1, 1), (0, 1)]), None, Polygon([])]
        ... )
        >>> s
        0    POLYGON ((0 0, 1 1, 0 1, 0 0))
        1                              None
        2                     POLYGON EMPTY
        dtype: geometry

        >>> s.notna()
        0     True
        1    False
        2     True
        dtype: bool

        See Also
        --------
        GeoSeries.isna : inverse of notna
        GeoSeries.is_empty : detect empty geometries
        """
        ...
    def notnull(self) -> pd.Series[bool]:
        """Alias for `notna` method. See `notna` for more detail."""
        ...
    # *** TODO: `fillna` annotation in pandas-stubs is NOT compatible; must `-> Self` ***
    # def fillna(self, value=None, method: FillnaOptions | None = None, inplace: bool = False, **kwargs): ...
    def __contains__(self, other: object) -> bool:
        """
        Allow tests of the form "geom in s".

        Tests whether a GeoSeries contains a geometry.

        Note: This is not the same as the geometric method "contains".
        """
        ...
    @doc(plot_series)
    def plot(self, *args, **kwargs):
        """
        Plot a GeoSeries.

        Generate a plot of a GeoSeries geometry with matplotlib.

        Parameters
        ----------
        s : Series
            The GeoSeries to be plotted. Currently Polygon,
            MultiPolygon, LineString, MultiLineString, Point and MultiPoint
            geometries can be plotted.
        cmap : str (default None)
            The name of a colormap recognized by matplotlib. Any
            colormap will work, but categorical colormaps are
            generally recommended. Examples of useful discrete
            colormaps include:

                tab10, tab20, Accent, Dark2, Paired, Pastel1, Set1, Set2

        color : str, np.array, pd.Series, List (default None)
            If specified, all objects will be colored uniformly.
        ax : matplotlib.pyplot.Artist (default None)
            axes on which to draw the plot
        figsize : pair of floats (default None)
            Size of the resulting matplotlib.figure.Figure. If the argument
            ax is given explicitly, figsize is ignored.
        aspect : 'auto', 'equal', None or float (default 'auto')
            Set aspect of axis. If 'auto', the default aspect for map plots is 'equal'; if
            however data are not projected (coordinates are long/lat), the aspect is by
            default set to 1/cos(s_y * pi/180) with s_y the y coordinate of the middle of
            the GeoSeries (the mean of the y range of bounding box) so that a long/lat
            square appears square in the middle of the plot. This implies an
            Equirectangular projection. If None, the aspect of `ax` won't be changed. It can
            also be set manually (float) as the ratio of y-unit to x-unit.
        autolim : bool (default True)
            Update axes data limits to contain the new geometries.
        **style_kwds : dict
            Color options to be passed on to the actual plot function, such
            as ``edgecolor``, ``facecolor``, ``linewidth``, ``markersize``,
            ``alpha``.

        Returns
        -------
        ax : matplotlib axes instance
        """
        ...
    @doc(_explore_geoseries)  # pyright: ignore[reportUnknownArgumentType]
    def explore(self, *args, **kwargs): ...  # signature of `_explore_geoseries` copied in `@doc`
    def explode(self, ignore_index: bool = False, index_parts: bool = False) -> GeoSeries: ...

    @overload
    def set_crs(
        self, crs: _ConvertibleToCRS, epsg: int | None = None, inplace: bool = False, allow_override: bool = False
    ) -> Self: ...
    @overload
    def set_crs(
        self, crs: _ConvertibleToCRS | None = None, *, epsg: int, inplace: bool = False, allow_override: bool = False
    ) -> Self: ...
    @overload
    def set_crs(self, crs: _ConvertibleToCRS | None, epsg: int, inplace: bool = False, allow_override: bool = False) -> Self: ...

    @overload
    def to_crs(self, crs: _ConvertibleToCRS, epsg: int | None = None) -> GeoSeries:
        """
        Return a ``GeoSeries`` with all geometries transformed to a new
        coordinate reference system.

        Transform all geometries in a GeoSeries to a different coordinate
        reference system.  The ``crs`` attribute on the current GeoSeries must
        be set.  Either ``crs`` or ``epsg`` may be specified for output.

        This method will transform all points in all objects.  It has no notion
        of projecting entire geometries.  All segments joining points are
        assumed to be lines in the current projection, not geodesics.  Objects
        crossing the dateline (or other projection boundary) will have
        undesirable behavior.

        Parameters
        ----------
        crs : pyproj.CRS, optional if `epsg` is specified
            The value can be anything accepted
            by :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
            such as an authority string (eg "EPSG:4326") or a WKT string.
        epsg : int, optional if `crs` is specified
            EPSG code specifying output projection.

        Returns
        -------
        GeoSeries

        Examples
        --------
        >>> from shapely.geometry import Point
        >>> s = geopandas.GeoSeries([Point(1, 1), Point(2, 2), Point(3, 3)], crs=4326)
        >>> s
        0    POINT (1 1)
        1    POINT (2 2)
        2    POINT (3 3)
        dtype: geometry
        >>> s.crs  # doctest: +SKIP
        <Geographic 2D CRS: EPSG:4326>
        Name: WGS 84
        Axis Info [ellipsoidal]:
        - Lat[north]: Geodetic latitude (degree)
        - Lon[east]: Geodetic longitude (degree)
        Area of Use:
        - name: World
        - bounds: (-180.0, -90.0, 180.0, 90.0)
        Datum: World Geodetic System 1984
        - Ellipsoid: WGS 84
        - Prime Meridian: Greenwich

        >>> s = s.to_crs(3857)
        >>> s
        0    POINT (111319.491 111325.143)
        1    POINT (222638.982 222684.209)
        2    POINT (333958.472 334111.171)
        dtype: geometry
        >>> s.crs  # doctest: +SKIP
        <Projected CRS: EPSG:3857>
        Name: WGS 84 / Pseudo-Mercator
        Axis Info [cartesian]:
        - X[east]: Easting (metre)
        - Y[north]: Northing (metre)
        Area of Use:
        - name: World - 85°S to 85°N
        - bounds: (-180.0, -85.06, 180.0, 85.06)
        Coordinate Operation:
        - name: Popular Visualisation Pseudo-Mercator
        - method: Popular Visualisation Pseudo Mercator
        Datum: World Geodetic System 1984
        - Ellipsoid: WGS 84
        - Prime Meridian: Greenwich

        See Also
        --------
        GeoSeries.set_crs : assign CRS
        """
        ...
    @overload
    def to_crs(self, crs: _ConvertibleToCRS | None = None, *, epsg: int) -> GeoSeries:
        """
        Return a ``GeoSeries`` with all geometries transformed to a new
        coordinate reference system.

        Transform all geometries in a GeoSeries to a different coordinate
        reference system.  The ``crs`` attribute on the current GeoSeries must
        be set.  Either ``crs`` or ``epsg`` may be specified for output.

        This method will transform all points in all objects.  It has no notion
        of projecting entire geometries.  All segments joining points are
        assumed to be lines in the current projection, not geodesics.  Objects
        crossing the dateline (or other projection boundary) will have
        undesirable behavior.

        Parameters
        ----------
        crs : pyproj.CRS, optional if `epsg` is specified
            The value can be anything accepted
            by :meth:`pyproj.CRS.from_user_input() <pyproj.crs.CRS.from_user_input>`,
            such as an authority string (eg "EPSG:4326") or a WKT string.
        epsg : int, optional if `crs` is specified
            EPSG code specifying output projection.

        Returns
        -------
        GeoSeries

        Examples
        --------
        >>> from shapely.geometry import Point
        >>> s = geopandas.GeoSeries([Point(1, 1), Point(2, 2), Point(3, 3)], crs=4326)
        >>> s
        0    POINT (1 1)
        1    POINT (2 2)
        2    POINT (3 3)
        dtype: geometry
        >>> s.crs  # doctest: +SKIP
        <Geographic 2D CRS: EPSG:4326>
        Name: WGS 84
        Axis Info [ellipsoidal]:
        - Lat[north]: Geodetic latitude (degree)
        - Lon[east]: Geodetic longitude (degree)
        Area of Use:
        - name: World
        - bounds: (-180.0, -90.0, 180.0, 90.0)
        Datum: World Geodetic System 1984
        - Ellipsoid: WGS 84
        - Prime Meridian: Greenwich

        >>> s = s.to_crs(3857)
        >>> s
        0    POINT (111319.491 111325.143)
        1    POINT (222638.982 222684.209)
        2    POINT (333958.472 334111.171)
        dtype: geometry
        >>> s.crs  # doctest: +SKIP
        <Projected CRS: EPSG:3857>
        Name: WGS 84 / Pseudo-Mercator
        Axis Info [cartesian]:
        - X[east]: Easting (metre)
        - Y[north]: Northing (metre)
        Area of Use:
        - name: World - 85°S to 85°N
        - bounds: (-180.0, -85.06, 180.0, 85.06)
        Coordinate Operation:
        - name: Popular Visualisation Pseudo-Mercator
        - method: Popular Visualisation Pseudo Mercator
        Datum: World Geodetic System 1984
        - Ellipsoid: WGS 84
        - Prime Meridian: Greenwich

        See Also
        --------
        GeoSeries.set_crs : assign CRS
        """
        ...
    @overload
    def to_crs(self, crs: _ConvertibleToCRS | None, epsg: int) -> GeoSeries: ...

    def estimate_utm_crs(self, datum_name: str = "WGS 84") -> CRS: ...
    def to_json(  # type: ignore[override]
        self,
        show_bbox: bool = True,
        drop_id: bool = False,
        to_wgs84: bool = False,
        *,
        # Keywords from json.dumps
        skipkeys: bool = False,
        ensure_ascii: bool = True,
        check_circular: bool = True,
        allow_nan: bool = True,
        cls: type[json.JSONEncoder] | None = None,
        indent: None | int | str = None,
        separators: tuple[str, str] | None = None,
        default: Callable[..., Any] | None = None,  # as typed in the json stdlib module
        sort_keys: bool = False,
        **kwds,
    ) -> str: ...

    @overload
    def to_wkb(self, hex: Literal[False] = False, **kwargs) -> pd.Series[bytes]:
        """
        Convert GeoSeries geometries to WKB.

        Parameters
        ----------
        hex : bool
            If true, export the WKB as a hexadecimal string.
            The default is to return a binary bytes object.
        kwargs
            Additional keyword args will be passed to
            :func:`shapely.to_wkb`.

        Returns
        -------
        Series
            WKB representations of the geometries

        See Also
        --------
        GeoSeries.to_wkt
        """
        ...
    @overload
    def to_wkb(self, hex: Literal[True], **kwargs) -> pd.Series[str]:
        """
        Convert GeoSeries geometries to WKB.

        Parameters
        ----------
        hex : bool
            If true, export the WKB as a hexadecimal string.
            The default is to return a binary bytes object.
        kwargs
            Additional keyword args will be passed to
            :func:`shapely.to_wkb`.

        Returns
        -------
        Series
            WKB representations of the geometries

        See Also
        --------
        GeoSeries.to_wkt
        """
        ...
    @overload
    def to_wkb(self, hex: bool = False, **kwargs) -> pd.Series[str] | pd.Series[bytes]: ...

    def to_wkt(self, **kwargs) -> pd.Series[str]: ...
    def to_arrow(
        self,
        geometry_encoding: Literal["WKB", "geoarrow", "wkb", "GeoArrow"] = "WKB",
        interleaved: bool | None = True,
        include_z: bool | None = None,
    ) -> GeoArrowArray:
        """
        Encode a GeoSeries to GeoArrow format.

        See https://geoarrow.org/ for details on the GeoArrow specification.

        This functions returns a generic Arrow array object implementing
        the `Arrow PyCapsule Protocol`_ (i.e. having an ``__arrow_c_array__``
        method). This object can then be consumed by your Arrow implementation
        of choice that supports this protocol.

        .. _Arrow PyCapsule Protocol: https://arrow.apache.org/docs/format/CDataInterface/PyCapsuleInterface.html

        .. versionadded:: 1.0

        Parameters
        ----------
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

        Returns
        -------
        GeoArrowArray
            A generic Arrow array object with geometry data encoded to GeoArrow.

        Examples
        --------
        >>> from shapely.geometry import Point
        >>> gser = geopandas.GeoSeries([Point(1, 2), Point(2, 1)])
        >>> gser
        0    POINT (1 2)
        1    POINT (2 1)
        dtype: geometry

        >>> arrow_array = gser.to_arrow()
        >>> arrow_array
        <geopandas.io._geoarrow.GeoArrowArray object at ...>

        The returned array object needs to be consumed by a library implementing
        the Arrow PyCapsule Protocol. For example, wrapping the data as a
        pyarrow.Array (requires pyarrow >= 14.0):

        >>> import pyarrow as pa
        >>> array = pa.array(arrow_array)
        >>> array
        <pyarrow.lib.BinaryArray object at ...>
        [
          0101000000000000000000F03F0000000000000040,
          01010000000000000000000040000000000000F03F
        ]
        """
        ...
    def clip(self, mask: _ClipMask, keep_geom_type: bool = False, sort: bool = False) -> GeoSeries:
        """
        Clip points, lines, or polygon geometries to the mask extent.

        Both layers must be in the same Coordinate Reference System (CRS).
        The GeoSeries will be clipped to the full extent of the `mask` object.

        If there are multiple polygons in mask, data from the GeoSeries will be
        clipped to the total boundary of all polygons in mask.

        Parameters
        ----------
        mask : GeoDataFrame, GeoSeries, (Multi)Polygon, list-like
            Polygon vector layer used to clip `gdf`.
            The mask's geometry is dissolved into one geometric feature
            and intersected with GeoSeries.
            If the mask is list-like with four elements ``(minx, miny, maxx, maxy)``,
            ``clip`` will use a faster rectangle clipping
            (:meth:`~GeoSeries.clip_by_rect`), possibly leading to slightly different
            results.
        keep_geom_type : boolean, default False
            If True, return only geometries of original type in case of intersection
            resulting in multiple geometry types or GeometryCollections.
            If False, return all resulting geometries (potentially mixed-types).
        sort : boolean, default False
            If True, the order of rows in the clipped GeoSeries will be preserved
            at small performance cost.
            If False the order of rows in the clipped GeoSeries will be random.

        Returns
        -------
        GeoSeries
            Vector data (points, lines, polygons) from `gdf` clipped to
            polygon boundary from mask.

        See Also
        --------
        clip : top-level function for clip

        Examples
        --------
        Clip points (grocery stores) with polygons (the Near West Side community):

        >>> import geodatasets
        >>> chicago = geopandas.read_file(
        ...     geodatasets.get_path("geoda.chicago_health")
        ... )
        >>> near_west_side = chicago[chicago["community"] == "NEAR WEST SIDE"]
        >>> groceries = geopandas.read_file(
        ...     geodatasets.get_path("geoda.groceries")
        ... ).to_crs(chicago.crs)
        >>> groceries.shape
        (148, 8)

        >>> nws_groceries = groceries.geometry.clip(near_west_side)
        >>> nws_groceries.shape
        (7,)
        """
        ...

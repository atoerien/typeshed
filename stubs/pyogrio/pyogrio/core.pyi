"""Core functions to interact with OGR data sources."""

from pathlib import Path
from typing import Any, Literal, TypedDict, type_check_only

import numpy as np
import shapely as shp

from ._typing import Array1D, Array2D, ReadPathOrBuffer

__gdal_version__: tuple[int, int, int]
__gdal_version_string__: str
__gdal_geos_version__: tuple[int, int, int] | None

@type_check_only
class _Capabilities(TypedDict):
    random_read: bool
    fast_set_next_by_index: bool
    fast_spatial_filter: bool
    fast_feature_count: bool
    fast_total_bounds: bool

@type_check_only
class _LayerInfo(TypedDict):
    layer_name: str
    # crs is `None` for non-spatial layers
    crs: str | None
    fields: Array1D[np.object_]  # field names (strings)
    dtypes: Array1D[np.object_]  # field dtypes (strings)
    ogr_types: list[str]
    ogr_subtypes: list[str]
    encoding: str
    fid_column: str
    geometry_name: str
    # geometry_type is `None` for non-spatial layers
    geometry_type: str | None
    features: int
    # total_bounds is `None` for non-spatial layers or if expensive to compute
    total_bounds: tuple[float, float, float, float] | None
    driver: str
    capabilities: _Capabilities
    dataset_metadata: dict[str, str] | None
    layer_metadata: dict[str, str] | None

@type_check_only
class _DriverDetails(TypedDict):
    long_name: str
    read: bool
    append: bool
    write: bool
    supports_vsi: bool
    help_topic_url: str | None
    extensions: list[str] | None

def list_drivers(read: bool = False, write: bool = False, append: bool = False) -> dict[str, Literal["r", "rw"]]:
    """
    List drivers available in GDAL.

    Parameters
    ----------
    read: bool, optional (default: False)
        If True, will only return drivers that are known to support read capabilities.
    write: bool, optional (default: False)
        If True, will only return drivers that are known to support write capabilities.
    append: bool, optional (default: False)
        If True, will only return drivers that are known to support append capabilities.
        .. versionadded:: 0.13.0

    Returns
    -------
    dict
        Mapping of driver name to file mode capabilities: ``"r"``: read,
        ``"a"``: append, ``"w"``: write.
        Drivers that are available but with unknown support are marked with ``"?"``

        .. versionchanged:: 0.13.0
           Added the ``a`` flag, which is available for GDAL >= 3.11.
    """
    ...
def list_drivers_details() -> dict[str, _DriverDetails]:
    """
    List all available drivers with detailed information.

    For each driver, the following properties are included:

    - long_name: the long name of the driver.
    - read: a boolean indicating if the driver supports opening and reading an
      existing file.
    - append: a boolean indicating if the driver supports appending rows to an
      existing file. This property is None if GDAL < 3.11.
    - write: a boolean indicating if the driver supports creating and writing
      new files.
    - help_topic_url: an URL to the GDAL documentation for the help topic of
      this driver.
    - extensions: a list of file extensions associated with this driver,
      if any.

    Returns
    -------
    dict of dicts
        Mapping of driver short name to a dict with detailed driver properties.
    """
    ...
def detect_write_driver(path: str | Path) -> str:
    """
    Attempt to infer the driver for a path by extension or prefix.

    Only drivers that support write capabilities will be detected.

    If the path cannot be resolved to a single driver, a ValueError will be
    raised.

    Parameters
    ----------
    path : str
        data source path

    Returns
    -------
    str
        name of the driver, if detected
    """
    ...
def list_layers(path_or_buffer: ReadPathOrBuffer, /) -> Array2D[np.object_]:
    """
    List layers available in an OGR data source.

    NOTE: includes both spatial and nonspatial layers.

    Parameters
    ----------
    path_or_buffer : str, pathlib.Path, bytes, or file-like
        A dataset path or URI, raw buffer, or file-like object with a read method.

    Returns
    -------
    ndarray shape (2, n)
        array of pairs of [<layer name>, <layer geometry type>]
        Note: geometry is `None` for nonspatial layers.
    """
    ...
def read_bounds(
    path_or_buffer: ReadPathOrBuffer,
    /,
    layer: int | str | None = None,
    skip_features: int = 0,
    max_features: int | None = None,
    where: str | None = None,
    bbox: tuple[float, float, float, float] | None = None,
    mask: shp.Geometry | None = None,
) -> tuple[Array1D[np.int64], Array2D[np.float64]]:
    """
    Read bounds of each feature.

    This can be used to assist with spatial indexing and partitioning, in
    order to avoid reading all features into memory.  It is roughly 2-3x faster
    than reading the full geometry and attributes of a dataset.

    Parameters
    ----------
    path_or_buffer : str, pathlib.Path, bytes, or file-like
        A dataset path or URI, raw buffer, or file-like object with a read method.
    layer : int or str, optional (default: first layer)
        If an integer is provided, it corresponds to the index of the layer
        with the data source.  If a string is provided, it must match the name
        of the layer in the data source.  Defaults to first layer in data source.
    skip_features : int, optional (default: 0)
        Number of features to skip from the beginning of the file before returning
        features.  Must be less than the total number of features in the file.
    max_features : int, optional (default: None)
        Number of features to read from the file.  Must be less than the total
        number of features in the file minus ``skip_features`` (if used).
    where : str, optional (default: None)
        Where clause to filter features in layer by attribute values.  Uses a
        restricted form of SQL WHERE clause, defined here:
        http://ogdi.sourceforge.net/prop/6.2.CapabilitiesMetadata.html
        Examples: ``"ISO_A3 = 'CAN'"``, ``"POP_EST > 10000000 AND POP_EST < 100000000"``
    bbox : tuple of (xmin, ymin, xmax, ymax), optional (default: None)
        If present, will be used to filter records whose geometry intersects this
        box.  This must be in the same CRS as the dataset.  If GEOS is present
        and used by GDAL, only geometries that intersect this bbox will be
        returned; if GEOS is not available or not used by GDAL, all geometries
        with bounding boxes that intersect this bbox will be returned.
    mask : Shapely geometry, optional (default: None)
        If present, will be used to filter records whose geometry intersects
        this geometry.  This must be in the same CRS as the dataset.  If GEOS is
        present and used by GDAL, only geometries that intersect this geometry
        will be returned; if GEOS is not available or not used by GDAL, all
        geometries with bounding boxes that intersect the bounding box of this
        geometry will be returned.  Requires Shapely >= 2.0.
        Cannot be combined with ``bbox`` keyword.

    Returns
    -------
    tuple of (fids, bounds)
        fids are global IDs read from the FID field of the dataset
        bounds are ndarray of shape(4, n) containing ``xmin``, ``ymin``, ``xmax``,
        ``ymax``
    """
    ...
def read_info(
    path_or_buffer: ReadPathOrBuffer,
    /,
    layer: int | str | None = None,
    encoding: str | None = None,
    force_feature_count: bool = False,
    force_total_bounds: bool = False,
    **kwargs: Any,  # Dataset open options passed to OGR
) -> _LayerInfo:
    """
    Read information about an OGR data source.

    ``crs``, ``geometry`` and ``total_bounds`` will be ``None`` and ``features`` will be
    0 for a nonspatial layer.

    ``features`` will be -1 if this is an expensive operation for this driver. You can
    force it to be calculated using the ``force_feature_count`` parameter.

    ``total_bounds`` is the 2-dimensional extent of all features within the dataset:
    (xmin, ymin, xmax, ymax). It will be None if this is an expensive operation for this
    driver or if the data source is nonspatial. You can force it to be calculated using
    the ``force_total_bounds`` parameter.

    ``fid_column`` is the name of the FID field in the data source, if the FID is
    physically stored (e.g. in GPKG). If the FID is just a sequence, ``fid_column``
    will be "" (e.g. ESRI Shapefile).

    ``geometry_name`` is the name of the field where the main geometry is stored in the
    data data source, if the field name can by customized (e.g. in GPKG). If no custom
    name is supported, ``geometry_name`` will be "" (e.g. ESRI Shapefile).

    ``encoding`` will be ``UTF-8`` if either the native encoding is likely to be
    ``UTF-8`` or GDAL can automatically convert from the detected native encoding
    to ``UTF-8``.

    Parameters
    ----------
    path_or_buffer : str, pathlib.Path, bytes, or file-like
        A dataset path or URI, raw buffer, or file-like object with a read method.
    layer : str or int, optional
        Name or index of layer in data source.  Reads the first layer by default.
    encoding : str, optional (default: None)
        If present, will be used as the encoding for reading string values from
        the data source, unless encoding can be inferred directly from the data
        source.
    force_feature_count : bool, optional (default: False)
        True if the feature count should be computed even if it is expensive.
    force_total_bounds : bool, optional (default: False)
        True if the total bounds should be computed even if it is expensive.
    **kwargs
        Additional driver-specific dataset open options passed to OGR.  Invalid
        options will trigger a warning.

    Returns
    -------
    dict
        A dictionary with the following keys::

            {
                "layer_name": "<layer name>",
                "crs": "<crs>",
                "fields": <ndarray of field names>,
                "dtypes": <ndarray of field dtypes>,
                "ogr_types": <ndarray of OGR field types>,
                "ogr_subtypes": <ndarray of OGR field subtypes>,
                "encoding": "<encoding>",
                "fid_column": "<fid column name or "">",
                "geometry_name": "<geometry column name or "">",
                "geometry_type": "<geometry type>",
                "features": <feature count or -1>,
                "total_bounds": <tuple with total bounds or None>,
                "driver": "<driver>",
                "capabilities": "<dict of driver capabilities>"
                "dataset_metadata": "<dict of dataset metadata or None>"
                "layer_metadata": "<dict of layer metadata or None>"
            }
    """
    ...
def set_gdal_config_options(options: dict[str, Any]) -> None:
    """
    Set GDAL configuration options.

    Options are listed here: https://trac.osgeo.org/gdal/wiki/ConfigOptions

    No error is raised if invalid option names are provided.

    These options are applied for an entire session rather than for individual
    functions.

    Parameters
    ----------
    options : dict
        If present, provides a mapping of option name / value pairs for GDAL
        configuration options.  ``True`` / ``False`` are normalized to ``'ON'``
        / ``'OFF'``. A value of ``None`` for a config option can be used to clear out a
        previously set value.
    """
    ...
def get_gdal_config_option(name: str) -> Any:
    """
    Get the value for a GDAL configuration option.

    Parameters
    ----------
    name : str
        name of the option to retrive

    Returns
    -------
    value of the option or None if not set
        ``'ON'`` / ``'OFF'`` are normalized to ``True`` / ``False``.
    """
    ...
def get_gdal_data_path() -> str:
    """
    Get the path to the directory GDAL uses to read data files.

    Returns
    -------
    str, or None if data directory was not found
    """
    ...
def vsi_listtree(path: str | Path, pattern: str | None = None) -> list[str]:
    """
    Recursively list the contents of a VSI directory.

    An fnmatch pattern can be specified to filter the directories/files
    returned.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the VSI directory to be listed.
    pattern : str, optional
        Pattern to filter results, in fnmatch format.
    """
    ...
def vsi_rmtree(path: str | Path) -> None:
    """
    Recursively remove VSI directory.

    Parameters
    ----------
    path : str or pathlib.Path
        path to the VSI directory to be removed.
    """
    ...
def vsi_unlink(path: str | Path) -> None:
    """
    Remove a VSI file.

    Parameters
    ----------
    path : str or pathlib.Path
        path to vsimem file to be removed
    """
    ...
def vsi_curl_clear_cache(prefix: str | Path = "") -> None:
    """
    Clean local cache associated with /vsicurl/.

    When a `prefix` is provided, only cached state for any file or directory
    starting with that prefix will be (exposing `VSICurlPartialClearCache <https://gdal.org/en/stable/api/cpl.html#_CPPv424VSICurlPartialClearCachePKc>`__).
    If no `prefix` is specified, the entire local cache is cleared (exposing
    `VSICurlClearCache <https://gdal.org/en/stable/api/cpl.html#_CPPv417VSICurlClearCachev>`__).

    Parameters
    ----------
    prefix : str
        Filename or prefix to clear associated cache. If not specified clear all cache.
    """
    ...

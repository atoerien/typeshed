"""Transforms."""

from collections.abc import Sequence

from rasterio._typing import _GDALOption
from rasterio.control import GroundControlPoint
from rasterio.errors import TransformWarning as TransformWarning
from rasterio.rpc import RPC

class GCPTransformerBase:
    def __init__(self, gcps: Sequence[GroundControlPoint]) -> None:
        """
        Construct a new GCP transformer

        Ground Control Points (GCPs) can be used to map specific world coordinates to pixel coordinates
        within an image. GDAL can use GCP interpolation in order to compute image pixel or geographic/
        projected coordinates as needed. Rasterio allows GDAL to determine the appropriate kind of 
        interpolation (up to cubic) depending on the number of GCPs available.

        Parameters
        ----------
        gcps : a sequence of GroundControlPoint
            Ground Control Points for a dataset.
        tps : bool
            If True, use GDALs thin plate spline transformer instead of polynomials.
        """
        ...
    def close(self) -> None:
        """Destroy transformer"""
        ...

class RPCTransformerBase:
    """Rational Polynomial Coefficients (RPC) transformer base class"""
    def __init__(self, rpcs: RPC, **kwargs: _GDALOption) -> None:
        """
        Construct a new RPC transformer

        The RPCs map geographic coordinates referenced against the WGS84 ellipsoid (longitude, latitude, height)
        to image pixel/line coordinates. The reverse is done through an iterative solver implemented
        in GDAL.

        Parameters
        ----------
        rpcs : rasterio.rpc.RPC or dict
            RPCs for a dataset. If passing a dict, should be in the form expected
            by rasterio.rpc.RPC.from_gdal.
        kwargs : dict
            GDALCreateRPCTransformer options. See
            https://gdal.org/api/gdal_alg.html#_CPPv426GDALCreateRPCTransformerV2PK13GDALRPCInfoV2idPPc.

        Notes
        -----
        Explicit control of the transformer (and open datasets if RPC_DEM
        is specified) can be achieved by use within a context manager or 
        by calling `close()` method e.g.

        >>> with rasterio.transform.RPCTransformer(rpcs) as transform:
        ...    transform.xy(0, 0)
        >>> transform.xy(0, 0)
        ValueError: Unexpected NULL transformer

        Coordinate transformations using RPCs are typically:
            1. Only well-defined over the extent of the dataset the RPCs were generated.
            2. Require accurate height values in order to provide accurate results.
               Consider using RPC_DEM to supply a DEM to sample accurate height measurements
               from.
        """
        ...
    def close(self) -> None:
        """Destroy transformer"""
        ...

def _transform_from_gcps(gcps: Sequence[GroundControlPoint]) -> tuple[float, ...]: ...

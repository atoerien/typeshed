"""
Coordinate reference systems, the CRS class and supporting functions.

A coordinate reference system (CRS) defines how a dataset's pixels map
to locations on, for example, a globe or the Earth. A CRS may be local
or global. The GIS field shares a number of authority files that define
CRS. "EPSG:32618" is the name of a regional CRS from the European
Petroleum Survey Group authority file. "OGC:CRS84" is the name of a
global CRS from the Open Geospatial Consortium authority. Custom CRS can
be described in text using several formats. Rasterio's CRS class is our
abstraction for coordinate reference systems.

A rasterio dataset's crs property is an instance of CRS. CRS are also
used to define transformations between coordinate reference systems.
These transformations are performed by the PROJ library. Rasterio does
not call PROJ functions directly, but invokes them via calls to GDAL's
"OSR*" functions.
"""

from collections.abc import Iterator, Mapping
from typing import Any
from typing_extensions import Self, deprecated, disjoint_base

from rasterio.enums import WktVersion

all_proj_keys: set[str]

@disjoint_base
class CRS(Mapping[str, Any]):
    """
    CRS(initialdata=None, **kwargs)

    A geographic or projected coordinate reference system.

    CRS objects may be created by passing PROJ parameters as keyword
    arguments to the standard constructor or by passing EPSG codes, PROJ
    mappings, PROJ strings, or WKT strings to the from_epsg, from_dict,
    from_string, or from_wkt static methods.

    Examples
    --------

    The from_dict method takes PROJ parameters as keyword arguments.

    >>> crs = CRS.from_dict(proj="aea")

    EPSG codes may be used with the from_epsg method.

    >>> crs = CRS.from_epsg(3005)

    The from_string method takes a variety of input.

    >>> crs = CRS.from_string("EPSG:3005")
    """
    def __init__(self, initialdata: Mapping[str, Any] | None = None, **kwargs: Any) -> None:
        """
        Make a CRS from a PROJ dict or mapping.

        Parameters
        ----------
        initialdata : mapping, optional
            A dictionary or other mapping
        kwargs : mapping, optional
            Another mapping. Will be overlaid on the initialdata.

        Returns
        -------
        CRS
        """
        ...
    def __getitem__(self, key: str, /) -> Any:
        """Return self[key]."""
        ...
    def __iter__(self) -> Iterator[str]:
        """Implement iter(self)."""
        ...
    def __len__(self) -> int:
        """Return len(self)."""
        ...
    def __bool__(self) -> bool:
        """True if self else False"""
        ...
    def __nonzero__(self) -> bool:
        """True if self else False"""
        ...
    def __eq__(self, other: object, /) -> bool:
        """Return self==value."""
        ...
    def __copy__(self) -> Self:
        """CRS.__copy__(self)"""
        ...
    def __hash__(self) -> int:
        """Return hash(self)."""
        ...
    def __getstate__(self) -> dict[str, Any]:
        """CRS.__getstate__(self)"""
        ...
    def __setstate__(self, state: Mapping[str, Any]) -> None:
        """CRS.__setstate__(self, state)"""
        ...
    def to_proj4(self) -> str:
        """
        CRS.to_proj4(self)

        Convert to a PROJ4 representation.

        Returns
        -------
        str
        """
        ...
    def to_wkt(self, morph_to_esri_dialect: bool = False, version: WktVersion | str | None = None) -> str:
        """
        CRS.to_wkt(self, morph_to_esri_dialect=False, version=None)

        Convert to a OGC WKT representation.

         .. versionadded:: 1.3.0 version

        Parameters
        ----------
        morph_to_esri_dialect : bool, optional
            Whether or not to morph to the Esri dialect of WKT Only
            applies to GDAL versions < 3. This parameter will be removed
            in a future version of rasterio.
        version : WktVersion or str, optional
            The version of the WKT output.
            Only works with GDAL 3+. Default is WKT1_GDAL.

        Returns
        -------
        str

        Raises
        ------
        CRSError
        """
        ...
    @property
    def wkt(self) -> str:
        """
        An OGC WKT representation of the CRS

        Returns
        -------
        str
        """
        ...
    def to_epsg(self, confidence_threshold: int = 70) -> int | None:
        """
        CRS.to_epsg(self, confidence_threshold=70)

        Convert to the best match EPSG code.

        For a CRS created using an EPSG code, that same value is
        returned.  For other CRS, including custom CRS, an attempt is
        made to match it to definitions in the EPSG authority file.
        Matches with a confidence below the threshold are discarded.

        Parameters
        ----------
        confidence_threshold : int
            Percent match confidence threshold (0-100).
   
        Returns
        -------
        int or None

        Raises
        ------
        CRSError
        """
        ...
    def to_authority(self, confidence_threshold: int = 70) -> tuple[str, str] | None:
        """
        CRS.to_authority(self, confidence_threshold=70)

        Convert to the best match authority name and code.

        For a CRS created using an EPSG code, that same value is
        returned.  For other CRS, including custom CRS, an attempt is
        made to match it to definitions in authority files.  Matches
        with a confidence below the threshold are discarded.

        Parameters
        ----------
        confidence_threshold : int
            Percent match confidence threshold (0-100).

        Returns
        -------
        name : str
            Authority name.
        code : str
            Code from the authority file.

        or None
        """
        ...
    def to_dict(self, projjson: bool = False) -> dict[str, Any]:
        """
        CRS.to_dict(self, projjson=False)

        Convert CRS to a PROJ dict.

        .. note:: If there is a corresponding EPSG code, it will be used
           when returning PROJ parameter dict.

        .. versionadded:: 1.3.0

        Parameters
        ----------
        projjson: bool, default=False
            If True, will convert to PROJ JSON dict (Requites GDAL 3.1+
            and PROJ 6.2+).  If False, will convert to PROJ parameter
            dict.

        Returns
        -------
        dict
        """
        ...
    @property
    def data(self) -> dict[str, Any]:
        """
        A PROJ4 dict representation of the CRS.
        
        """
        ...
    @property
    def is_geographic(self) -> bool:
        """
        Test if the CRS is a geographic coordinate reference system.

        Returns
        -------
        bool

        Raises
        ------
        CRSError
        """
        ...
    @property
    def is_projected(self) -> bool:
        """
        Test if the CRS is a projected coordinate reference system.

        Returns
        -------
        bool

        Raises
        ------
        CRSError
        """
        ...
    @property
    @deprecated("CRS.is_valid is deprecated since rasterio 1.4 and will be removed in 2.0.0.")
    def is_valid(self) -> bool:
        """
        Test that the CRS is a geographic or projected CRS.

        .. deprecated:: 1.4.0
           This property is not useful and will be removed in 2.0.0.

        Returns
        -------
        bool
        """
        ...
    @property
    def is_epsg_code(self) -> bool:
        """
        Test if the CRS is defined by an EPSG code.

        Returns
        -------
        bool
        """
        ...
    @property
    def linear_units_factor(self) -> tuple[str, float]:
        """
        Get linear units and the conversion factor to meters of the CRS.

        Returns
        -------
        units : str
            "m", "ft", etc.
        factor : float
            Ratio of one unit to one meter.    

        Raises
        ------
        CRSError
        """
        ...
    @property
    def linear_units(self) -> str:
        """
        Get a short name for the linear units of the CRS.

        Returns
        -------
        units : str
            "m", "ft", etc.

        Raises
        ------
        CRSError
        """
        ...
    @property
    def units_factor(self) -> tuple[str, float]:
        """
        Get units and the conversion factor of the CRS.

        Returns
        -------
        units : str
            "m", "ft", etc.
        factor : float
            Ratio of one unit to one radian if the CRS is geographic
            otherwise, it is to one meter.

        Raises
        ------
        CRSError
        """
        ...
    @property
    def geodetic_crs(self) -> CRS | None:
        """
        Get the Geographic CRS from the CRS.

        Returns
        -------
        CRS

        Raises
        ------
        CRSError
        """
        ...
    def to_string(self) -> str:
        """
        CRS.to_string(self)

        Convert to a PROJ4 or WKT string.

        The output will be reduced as much as possible by attempting a
        match to CRS defined in authority files.

        Notes
        -----
        Mapping keys are tested against the ``all_proj_keys`` list.
        Values of ``True`` are omitted, leaving the key bare:
        {'no_defs': True} -> "+no_defs" and items where the value is
        otherwise not a str, int, or float are omitted.

        Returns
        -------
        str

        Raises
        ------
        CRSError
        """
        ...
    def equals(self, other: CRS, ignore_axis_order: bool = False) -> bool:
        """
        CRS.equals(self, other, ignore_axis_order=False)

        Check if the crs objects are equivalent.

        Properties
        ----------
        other: CRS
            the other CRS to compare to
        ignore_axis_order: bool, default=False
            If True, it will compare the CRS class and ignore the axis order.

        Returns
        -------
        bool
        """
        ...
    def get(self, item: str) -> Any:
        """CRS.get(self, item)"""
        ...
    @staticmethod
    def from_epsg(code: int | str) -> CRS:
        """
        CRS.from_epsg(code)

        Make a CRS from an EPSG code.

        Parameters
        ----------
        code : int or str
            An EPSG code. Strings will be converted to integers.

        Notes
        -----
        The input code is not validated against an EPSG database.

        Returns
        -------
        CRS

        Raises
        ------
        CRSError
        """
        ...
    @staticmethod
    def from_authority(auth_name: str, code: int | str) -> CRS:
        """
        CRS.from_authority(auth_name, code)

        Make a CRS from an authority name and code.

        .. versionadded:: 1.1.7

        Parameters
        ----------
        auth_name: str
        code : int or str
            The code used by the authority.

        Returns
        -------
        CRS

        Raises
        ------
        CRSError
        """
        ...
    @staticmethod
    def from_string(value: str, morph_from_esri_dialect: bool = False) -> CRS:
        """
        CRS.from_string(value, morph_from_esri_dialect=False)

        Make a CRS from an EPSG, PROJ, or WKT string

        Parameters
        ----------
        value : str
            An EPSG, PROJ, or WKT string.
        morph_from_esri_dialect : bool, optional
            If True, items in the input using Esri's dialect of WKT
            will be replaced by OGC standard equivalents.

        Returns
        -------
        CRS

        Raises
        ------
        CRSError
        """
        ...
    @staticmethod
    def from_proj4(proj: str) -> CRS:
        """
        CRS.from_proj4(proj)

        Make a CRS from a PROJ4 string.

        Parameters
        ----------
        proj : str
            A PROJ4 string like "+proj=longlat ..."

        Returns
        -------
        CRS

        Raises
        ------
        CRSError
        """
        ...
    @staticmethod
    def from_dict(initialdata: Mapping[str, Any] | None = None, **kwargs: Any) -> CRS:
        """
        CRS.from_dict(initialdata=None, **kwargs)

        Make a CRS from a dict of PROJ parameters or PROJ JSON.

        Parameters
        ----------
        initialdata : mapping, optional
            A dictionary or other mapping
        kwargs : mapping, optional
            Another mapping. Will be overlaid on the initialdata.

        Returns
        -------
        CRS

        Raises
        ------
        CRSError
        """
        ...
    @staticmethod
    def from_wkt(wkt: str, morph_from_esri_dialect: bool = False) -> CRS:
        """
        CRS.from_wkt(wkt, morph_from_esri_dialect=False)

        Make a CRS from a WKT string.

        Parameters
        ----------
        wkt : str
            A WKT string.
        morph_from_esri_dialect : bool, optional
            If True, items in the input using Esri's dialect of WKT
            will be replaced by OGC standard equivalents.

        Returns
        -------
        CRS

        Raises
        ------
        CRSError
        """
        ...
    # `value` is dispatched at runtime: CRS, int (EPSG), str (PROJ/WKT/auth), Mapping[str, Any], or any pyproj-CRS-like object.
    @staticmethod
    def from_user_input(value: Any, morph_from_esri_dialect: bool = False) -> CRS:
        """
        CRS.from_user_input(value, morph_from_esri_dialect=False)

        Make a CRS from a variety of inputs.

        Parameters
        ----------
        value : object
            User input of many different kinds.
        morph_from_esri_dialect : bool, optional
            If True, items in the input using Esri's dialect of WKT
            will be replaced by OGC standard equivalents.

        Returns
        -------
        CRS

        Raises
        ------
        CRSError
        """
        ...

def epsg_treats_as_latlong(input_crs: CRS) -> bool:
    """
    epsg_treats_as_latlong(input_crs)

    Test if the CRS is in latlon order

    From GDAL docs:

    > This method returns TRUE if EPSG feels this geographic coordinate
    system should be treated as having lat/long coordinate ordering.

    > Currently this returns TRUE for all geographic coordinate systems with
    an EPSG code set, and axes set defining it as lat, long.

    > FALSE will be returned for all coordinate systems that are not
    geographic, or that do not have an EPSG code set.

    > **Note**

    > Important change of behavior since GDAL 3.0.
    In previous versions, geographic CRS imported with importFromEPSG()
    would cause this method to return FALSE on them, whereas now it returns
    TRUE, since importFromEPSG() is now equivalent to importFromEPSGA().

    Parameters
    ----------
    input_crs : CRS
        Coordinate reference system, as a rasterio CRS object
        Example: CRS({'init': 'EPSG:4326'})

    Returns
    -------
    bool
    """
    ...
def epsg_treats_as_northingeasting(input_crs: CRS) -> bool:
    """
    epsg_treats_as_northingeasting(input_crs)

    Test if the CRS should be treated as having northing/easting coordinate ordering

    From GDAL docs:

    > This method returns TRUE if EPSG feels this projected coordinate
    system should be treated as having northing/easting coordinate ordering.

    > Currently this returns TRUE for all projected coordinate systems with
    an EPSG code set, and axes set defining it as northing, easting.

    > FALSE will be returned for all coordinate systems that are not
    projected, or that do not have an EPSG code set.

    > **Note**

    > Important change of behavior since GDAL 3.0.
    In previous versions, projected CRS with northing, easting axis order
    imported with importFromEPSG() would cause this method to return FALSE
    on them, whereas now it returns TRUE, since importFromEPSG() is now 
    equivalent to importFromEPSGA().

    Parameters
    ----------
    input_crs : CRS
        Coordinate reference system, as a rasterio CRS object
        Example: CRS({'init': 'EPSG:4326'})

    Returns
    -------
    bool
    """
    ...
def auth_preference(item: str) -> None:
    """auth_preference(item)"""
    ...

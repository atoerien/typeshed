"""Astronomical calculations for Python"""

from _typeshed import Unused
from datetime import datetime as _datetime
from typing import Final, NoReturn, TypedDict, overload, type_check_only
from typing_extensions import Self, TypeAlias, deprecated, disjoint_base

_DateInitType: TypeAlias = (
    Date
    | float
    | str
    | tuple[int]
    | tuple[int, int]
    | tuple[int, int, float]
    | tuple[int, int, float, float]
    | tuple[int, int, float, float, float]
    | tuple[int, int, float, float, float, float]
    | _datetime
)

@type_check_only
class _DateDescriptor:
    @overload
    def __get__(self, obj: None, objtype: type | None = None) -> Self: ...
    @overload
    def __get__(self, obj: object, objtype: type | None = None) -> Date: ...
    def __set__(self, obj: object, value: _DateInitType) -> None: ...

@type_check_only
class _AngleDescriptorRadiansHours:
    @overload
    def __get__(self, obj: None, objtype: type | None = None) -> Self: ...
    @overload
    def __get__(self, obj: object, objtype: type | None = None) -> Angle: ...
    def __set__(self, obj: object, value: float | str) -> None: ...

@type_check_only
class _AngleDescriptorRadiansDegrees:
    @overload
    def __get__(self, obj: None, objtype: type | None = None) -> Self: ...
    @overload
    def __get__(self, obj: object, objtype: type | None = None) -> Angle: ...
    def __set__(self, obj: object, value: float | str) -> None: ...

@type_check_only
class _AngleDescriptorDegreesRadians:
    @overload
    def __get__(self, obj: None, objtype: type | None = None) -> Self: ...
    @overload
    def __get__(self, obj: object, objtype: type | None = None) -> Angle: ...
    @overload
    @deprecated("Do not pass Angle objects! The radian value will be incorrectly interpreted as degrees.")
    def __set__(self, obj: object, value: Angle) -> None: ...
    @overload
    def __set__(self, obj: object, value: float | str) -> None: ...

J2000: Final[float]
MJD0: Final[float]
earth_radius: Final[float]
meters_per_au: Final[float]
moon_radius: Final[float]
sun_radius: Final[float]

@disjoint_base
class Angle(float):  # type: ignore[type-var]
    """
    An angle in radians that can print itself in an astronomical format.
    Use ephem.degrees() and ephem.radians() to create one.
    """
    def __new__(cls, *args: Unused, **kwargs: Unused) -> NoReturn: ...
    @property
    def norm(self) -> Angle:
        """Return this angle normalized to the interval [0, 2*pi)."""
        ...
    @property
    def znorm(self) -> Angle:
        """Return this angle normalized to the interval (-pi, pi]."""
        ...

class Date(float):
    """
    Floating point value used by ephem to represent a date.
    The value is the number of days since 1899 December 31 12:00 UT. When
    creating an instance you can pass in a Python datetime instance, timetuple,
    year-month-day triple, or a plain float. Run str() onthis object to see
    the UTC date it represents.
    """
    @overload
    def __new__(cls) -> Date: ...
    @overload
    def __new__(cls, date: _DateInitType, /) -> Date: ...
    def triple(self) -> tuple[int, int, float]:
        """Return the date as a (year, month, day_with_fraction) tuple"""
        ...
    def tuple(self) -> tuple[int, int, int, int, int, float]:
        """Return the date as a (year, month, day, hour, minute, second) tuple"""
        ...
    def datetime(self) -> _datetime:
        """Return the date as a (year, month, day, hour, minute, second) tuple"""
        ...

@disjoint_base
class Observer:
    """
    Describes an observer standing on the Earth's surface.
    This object can also store the time at which the observer is watching;
    the epoch in which they want astrometric coordinates returned; and the
    temperature and barometric pressure, which affect horizon refraction.
    See Body.compute() for how to use instances of this class.
    """
    lat: _AngleDescriptorRadiansDegrees
    lon: _AngleDescriptorRadiansDegrees
    long: _AngleDescriptorRadiansDegrees
    elevation: float
    elev: float
    temp: float
    temperature: float
    pressure: float
    horizon: _AngleDescriptorRadiansDegrees
    epoch: _DateDescriptor
    date: _DateDescriptor

    def __init__(self) -> None: ...
    def sidereal_time(self) -> Angle:
        """compute the local sidereal time for this location and time"""
        ...
    def radec_of(self, az: float | str, alt: float | str) -> tuple[Angle, Angle]:
        """compute the right ascension and declination of a point identified by its azimuth and altitude"""
        ...

@disjoint_base
class Body:
    @property
    def name(self) -> str | None:
        """object name (read-only string)"""
        ...
    @property
    def a_ra(self) -> Angle:
        """astrometric geocentric right ascension as a float giving radians, or a string giving hours:minutes:seconds"""
        ...
    @property
    def a_dec(self) -> Angle:
        """astrometric geocentric declination as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def a_epoch(self) -> Date:
        """date giving the equinox of the body's astrometric right ascension and declination"""
        ...
    @property
    def ra(self) -> Angle:
        """right ascension as a float giving radians, or a string giving hours:minutes:seconds"""
        ...
    @property
    def dec(self) -> Angle:
        """declination as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def g_ra(self) -> Angle:
        """apparent geocentric right ascension as a float giving radians, or a string giving hours:minutes:seconds"""
        ...
    @property
    def g_dec(self) -> Angle:
        """apparent geocentric declination as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def elong(self) -> Angle:
        """elongation as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def mag(self) -> float:
        """magnitude"""
        ...
    @property
    def size(self) -> float:
        """visual size in arcseconds"""
        ...
    @property
    def radius(self) -> Angle:
        """visual radius as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def alt(self) -> Angle:
        """altitude as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def az(self) -> Angle:
        """azimuth as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def ha(self) -> Angle:
        """hour angle as a float giving radians, or a string giving hours:minutes:seconds"""
        ...
    @property
    def rise_time(self) -> Date | None:
        """rise time"""
        ...
    @property
    def rise_az(self) -> Angle | None:
        """azimuth at which the body rises as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def transit_time(self) -> Date | None:
        """transit time"""
        ...
    @property
    def transit_alt(self) -> Angle | None:
        """transit altitude as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def set_time(self) -> Date | None:
        """set time"""
        ...
    @property
    def set_az(self) -> Angle | None:
        """azimuth at which the body sets as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def circumpolar(self) -> bool:
        """whether object remains above the horizon this day"""
        ...
    @property
    def neverup(self) -> bool:
        """whether object never rises above the horizon this day"""
        ...
    def __init__(self, *args: Unused, **kwargs: Unused) -> None: ...
    def __copy__(self) -> Self:
        """Return a new copy of this body"""
        ...
    @overload
    def compute(self, observer: Observer, /) -> None:
        """compute the location of the body for the given date or Observer, or for the current time if no date is supplied"""
        ...
    @overload
    def compute(self, when: _DateInitType = ..., epoch: _DateInitType = ...) -> None:
        """compute the location of the body for the given date or Observer, or for the current time if no date is supplied"""
        ...
    def copy(self) -> Self:
        """Return a new copy of this body"""
        ...
    def writedb(self) -> str:
        """return a string representation of the body appropriate for inclusion in an ephem database file"""
        ...
    def parallactic_angle(self) -> Angle:
        """return the parallactic angle to the body; an Observer must have been provided to the most recent compute() call, because a parallactic angle is always measured with respect to a specfic observer"""
        ...

class Planet(Body):
    @property
    def hlon(self) -> Angle:
        """heliocentric longitude (but Sun().hlon means the hlon of Earth) as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def hlat(self) -> Angle:
        """heliocentric latitude (but Sun().hlat means the hlat of Earth) as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def sun_distance(self) -> float:
        """distance from sun in AU"""
        ...
    @property
    def earth_distance(self) -> float:
        """distance from earth in AU"""
        ...
    @property
    def phase(self) -> float:
        """phase as percent of the surface illuminated"""
        ...
    @property
    def hlong(self) -> Angle:
        """heliocentric longitude as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @overload
    def __init__(self, observer: Observer, /) -> None: ...
    @overload
    def __init__(self, when: _DateInitType, /, epoch: _DateInitType = ...) -> None: ...
    @overload
    def __init__(self, *args: Unused, **kwargs: Unused) -> None: ...

@disjoint_base
class Moon(Planet):
    """Create a Body Instance representing the Moon."""
    @property
    def libration_lat(self) -> Angle:
        """lunar libration in latitude as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def libration_long(self) -> Angle:
        """lunar libration in longitude as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def colong(self) -> Angle:
        """lunar selenographic colongitude as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def moon_phase(self) -> float:
        """fraction of lunar surface illuminated when viewed from earth"""
        ...
    @property
    def subsolar_lat(self) -> Angle:
        """lunar latitude of subsolar point as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...

@disjoint_base
class Jupiter(Planet):
    """Create a Body instance representing Jupiter."""
    @property
    def cmlI(self) -> Angle:
        """central meridian longitude, System I as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def cmlII(self) -> Angle:
        """central meridian longitude, System II as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...

@disjoint_base
class Saturn(Planet):
    """Create a Body instance representing Saturn."""
    @property
    def earth_tilt(self) -> Angle:
        """tilt of rings towards Earth, positive for southward tilt, as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def sun_tilt(self) -> Angle:
        """tilt of rings towards Sun, positive for southward tilt, as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...

@disjoint_base
class PlanetMoon:
    @property
    def name(self) -> str:
        """object name (read-only string)"""
        ...
    @property
    def a_ra(self) -> Angle:
        """astrometric geocentric right ascension as a float giving radians, or a string giving hours:minutes:seconds"""
        ...
    @property
    def a_dec(self) -> Angle:
        """astrometric geocentric declination as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def ra(self) -> Angle:
        """right ascension as a float giving radians, or a string giving hours:minutes:seconds"""
        ...
    @property
    def dec(self) -> Angle:
        """declination as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def g_ra(self) -> Angle:
        """apparent geocentric right ascension as a float giving radians, or a string giving hours:minutes:seconds"""
        ...
    @property
    def g_dec(self) -> Angle:
        """apparent geocentric declination as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def alt(self) -> Angle:
        """altitude as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def az(self) -> Angle:
        """azimuth as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def x(self) -> float:
        """how far east or west of its planet the moon lies in the sky in planet radii; east is positive"""
        ...
    @property
    def y(self) -> float:
        """how far north or south of its planet the moon lies in the sky in planet radii; south is positive"""
        ...
    @property
    def z(self) -> float:
        """how much closer or farther from Earth the moon is than its planet in planet radii; closer to Earth is positive"""
        ...
    @property
    def earth_visible(self) -> float:
        """whether visible from earth"""
        ...
    @property
    def sun_visible(self) -> float:
        """whether visible from sun"""
        ...
    @overload
    def __init__(self, observer: Observer, /) -> None: ...
    @overload
    def __init__(self, when: _DateInitType, /, epoch: _DateInitType = ...) -> None: ...
    @overload
    def __init__(self, **kwargs: Unused) -> None: ...
    def __copy__(self) -> Self:
        """Return a new copy of this body"""
        ...
    @overload
    def compute(self, observer: Observer, /) -> None:
        """compute the location of the body for the given date or Observer, or for the current time if no date is supplied"""
        ...
    @overload
    def compute(self, when: _DateInitType = ..., epoch: _DateInitType = ...) -> None:
        """compute the location of the body for the given date or Observer, or for the current time if no date is supplied"""
        ...
    def copy(self) -> Self:
        """Return a new copy of this body"""
        ...
    def writedb(self) -> str:
        """return a string representation of the body appropriate for inclusion in an ephem database file"""
        ...
    def parallactic_angle(self) -> Angle:
        """return the parallactic angle to the body; an Observer must have been provided to the most recent compute() call, because a parallactic angle is always measured with respect to a specfic observer"""
        ...

class FixedBody(Body):
    """A celestial body, that can compute() its sky position"""
    name: str | None
    mag: float
    _spect: str
    _ratio: float
    _pa: _AngleDescriptorRadiansDegrees
    _epoch: _DateDescriptor
    _ra: _AngleDescriptorRadiansHours
    _dec: _AngleDescriptorRadiansDegrees
    _pmra: float
    _pmdec: float
    _class: str

    def __init__(self) -> None: ...

class EllipticalBody(Planet):
    """A celestial body, that can compute() its sky position"""
    name: str | None
    _inc: _AngleDescriptorDegreesRadians
    _Om: _AngleDescriptorDegreesRadians
    _om: _AngleDescriptorDegreesRadians
    _M: _AngleDescriptorDegreesRadians
    _epoch_M: _DateDescriptor
    _epoch: _DateDescriptor
    _H: float
    _G: float
    _g: float
    _k: float
    _a: float
    _size: float
    _e: float

    def __init__(self, *args: Unused, **kwargs: Unused) -> None: ...

class ParabolicBody(Planet):
    """A celestial body, that can compute() its sky position"""
    name: str | None
    _epoch: _DateDescriptor
    _epoch_p: _DateDescriptor
    _inc: _AngleDescriptorDegreesRadians
    _om: _AngleDescriptorDegreesRadians
    _Om: _AngleDescriptorDegreesRadians
    _q: float
    _g: float
    _k: float
    _size: float

    def __init__(self, *args: Unused, **kwargs: Unused) -> None: ...

class HyperbolicBody(Planet):
    """A celestial body, that can compute() its sky position"""
    name: str | None
    _epoch: _DateDescriptor
    _epoch_p: _DateDescriptor
    _inc: _AngleDescriptorDegreesRadians
    _Om: _AngleDescriptorDegreesRadians
    _om: _AngleDescriptorDegreesRadians
    _e: float
    _q: float
    _g: float
    _k: float
    _size: float

    def __init__(self, *args: Unused, **kwargs: Unused) -> None: ...

@disjoint_base
class EarthSatellite(Body):
    """
    A satellite in orbit around the Earth, usually built by passing the text of a TLE entry to the `ephem.readtle()` routine. You can read and write its orbital parameters through the following attributes:

    _ap -- argument of perigee at epoch (degrees)
    _decay -- orbit decay rate (revolutions per day-squared)
    _drag -- object drag coefficient (per earth radius)
    _e -- eccentricity
    _epoch -- reference epoch (mjd)
    _inc -- inclination (degrees)
    _M -- mean anomaly (degrees from perigee at epoch)
    _n -- mean motion (revolutions per day)
    _orbit -- integer orbit number of epoch
    _raan -- right ascension of ascending node (degrees)
    """
    name: str | None
    epoch: _DateDescriptor
    _epoch: _DateDescriptor
    _inc: _AngleDescriptorDegreesRadians
    _raan: _AngleDescriptorDegreesRadians
    _ap: _AngleDescriptorDegreesRadians
    _M: _AngleDescriptorDegreesRadians
    n: float
    inc: float
    raan: float
    e: float
    ap: float
    M: float
    decay: float
    drag: float
    orbit: float
    _n: float
    _e: float
    _decay: float
    _drag: float
    _orbit: int
    catalog_number: str | None

    @property
    def sublat(self) -> Angle:
        """latitude beneath satellite as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def sublong(self) -> Angle:
        """longitude beneath satellite as a float giving radians, or a string giving degrees:minutes:seconds"""
        ...
    @property
    def elevation(self) -> float:
        """height above sea level in meters"""
        ...
    @property
    def range(self) -> float:
        """distance from observer to satellite in meters"""
        ...
    @property
    def range_velocity(self) -> float:
        """range rate of change in meters per second"""
        ...
    @property
    def eclipsed(self) -> bool:
        """whether satellite is in earth's shadow"""
        ...

@type_check_only
class _MoonPhases(TypedDict):
    new: Date
    full: Date

def builtin_planets() -> list[tuple[int, str, str]]:
    """return the list of built-in planet objects"""
    ...
def degrees(angle: float | str, /) -> Angle:
    """build an angle measured in degrees"""
    ...
def hours(angle: float | str, /) -> Angle:
    """build an angle measured in hours of arc"""
    ...
def now() -> Date:
    """Return the current time"""
    ...
def separation(
    obj1: tuple[float | str, float | str] | Body | Observer, obj2: tuple[float | str, float | str] | Body | Observer, /
) -> Angle:
    """Return the angular separation between two objects or positions as a float giving radians, or a string giving degrees:minutes:seconds"""
    ...
def readdb(db_line: str, /) -> Body:
    """Read an ephem database entry"""
    ...
def readtle(name: str, line1: str, line2: str, /) -> EarthSatellite:
    """Read TLE-format satellite elements"""
    ...
def unrefract(pressure: float, temperature: float, apparent_alt: float, /) -> Angle:
    """Reverse angle of refraction"""
    ...
def uranometria(ra: float | str, dec: float | str, /) -> int:
    """given right ascension and declination (in radians), return the page of the original Uranometria displaying that location"""
    ...
def uranometria2000(ra: float | str, dec: float | str, /) -> int:
    """given right ascension and declination (in radians), return the page of the Uranometria 2000.0 displaying that location"""
    ...
def millennium_atlas(ra: float | str, dec: float | str, /) -> int:
    """given right ascension and declination (in radians), return the page of the Millenium Star Atlas displaying that location"""
    ...
@overload
def constellation(position: Body) -> tuple[str, str]:
    """Return the constellation in which the object or coordinates lie"""
    ...
@overload
def constellation(position: tuple[Angle | float, Angle | float], epoch: Date | float = ...) -> tuple[str, str]:
    """Return the constellation in which the object or coordinates lie"""
    ...
def julian_date(date: _DateInitType | Observer = ..., /) -> float:
    """Return the Julian date of the current time, or of an argument that can be converted into an ephem.Date."""
    ...
def delta_t(date: _DateInitType | Observer = ..., /) -> float:
    """Compute the difference between Terrestrial Time and Coordinated Universal Time."""
    ...
def moon_phases(date: _DateInitType | Observer = ...) -> _MoonPhases:
    """compute the new and full moons nearest a given date"""
    ...
def eq_ecl(epoch: Date | float, ra: Angle | float, dec: Angle | float, /) -> tuple[Angle, Angle]:
    """compute the ecliptic longitude and latitude of an RA and dec"""
    ...
def ecl_eq(epoch: Date | float, lon: Angle | float, lat: Angle | float, /) -> tuple[Angle, Angle]:
    """compute the ecliptic longitude and latitude of an RA and dec"""
    ...
def eq_gal(epoch: Date | float, ra: Angle | float, dec: Angle | float, /) -> tuple[Angle, Angle]:
    """compute the ecliptic longitude and latitude of an RA and dec"""
    ...
def gal_eq(epoch: Date | float, glon: Angle | float, glat: Angle | float, /) -> tuple[Angle, Angle]:
    """compute the ecliptic longitude and latitude of an RA and dec"""
    ...
def precess(epoch1: Date | float, epoch2: Date | float, ra: Angle | float, dec: Angle | float, /) -> tuple[Angle, Angle]:
    """precess a right ascension and declination to another equinox"""
    ...
def _next_pass(
    observer: Observer, body: Body, /
) -> tuple[Date | None, Angle | None, Date | None, Angle | None, Date | None, Angle | None]:
    """Return as a tuple the next rising, culmination, and setting of an EarthSatellite"""
    ...

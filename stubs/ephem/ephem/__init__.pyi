from collections.abc import Callable
from datetime import datetime as _datetime, timedelta as _timedelta, tzinfo as _tzinfo
from typing import Final, NoReturn, overload
from typing_extensions import Self

from . import _libastro

__version__: Final[str]

# Mathematical constants
tau: Final[float]
twopi: Final[float]
halfpi: Final[float]
quarterpi: Final[float]
eighthpi: Final[float]
degree: Final[float]
arcminute: Final[float]
arcsecond: Final[float]
half_arcsecond: Final[float]
tiny: Final[float]

# Physical constants
c: Final[float]
meters_per_au: Final[float]
earth_radius: Final[float]
moon_radius: Final[float]
sun_radius: Final[float]

# Epoch constants
B1900: Final[float]
B1950: Final[float]
J2000: Final[float]

# Type imports from _libastro
Angle = _libastro.Angle
degrees = _libastro.degrees
hours = _libastro.hours
Date = _libastro.Date

# Time constants
hour: Final[float]
minute: Final[float]
second: Final[float]

# Precision constants
default_newton_precision: Final[float]
rise_set_iterations: Final[tuple[int, int, int, int, int, int, int]]

# Function imports from _libastro
delta_t = _libastro.delta_t
julian_date = _libastro.julian_date

# Body type imports from _libastro
Body = _libastro.Body
Planet = _libastro.Planet
PlanetMoon = _libastro.PlanetMoon
FixedBody = _libastro.FixedBody
EllipticalBody = _libastro.EllipticalBody
ParabolicBody = _libastro.ParabolicBody
HyperbolicBody = _libastro.HyperbolicBody
EarthSatellite = _libastro.EarthSatellite

# Database and coordinate functions from _libastro
readdb = _libastro.readdb
readtle = _libastro.readtle
constellation = _libastro.constellation
separation = _libastro.separation
unrefract = _libastro.unrefract
now = _libastro.now

# Star atlas functions from _libastro
millennium_atlas = _libastro.millennium_atlas
uranometria = _libastro.uranometria
uranometria2000 = _libastro.uranometria2000

# Special planet classes from _libastro
Jupiter = _libastro.Jupiter
Saturn = _libastro.Saturn
Moon = _libastro.Moon

# Dynamically created planet classes
class Mercury(Planet):
    __planet__: Final = 0

class Venus(Planet):
    __planet__: Final = 1

class Mars(Planet):
    __planet__: Final = 2

class Uranus(Planet):
    __planet__: Final = 5

class Neptune(Planet):
    __planet__: Final = 6

class Pluto(Planet):
    __planet__: Final = 7

class Sun(Planet):
    __planet__: Final = 8

# Planet moon classes
class Phobos(PlanetMoon):
    __planet__: Final = 10

class Deimos(PlanetMoon):
    __planet__: Final = 11

class Io(PlanetMoon):
    __planet__: Final = 12

class Europa(PlanetMoon):
    __planet__: Final = 13

class Ganymede(PlanetMoon):
    __planet__: Final = 14

class Callisto(PlanetMoon):
    __planet__: Final = 15

class Mimas(PlanetMoon):
    __planet__: Final = 16

class Enceladus(PlanetMoon):
    __planet__: Final = 17

class Tethys(PlanetMoon):
    __planet__: Final = 18

class Dione(PlanetMoon):
    __planet__: Final = 19

class Rhea(PlanetMoon):
    __planet__: Final = 20

class Titan(PlanetMoon):
    __planet__: Final = 21

class Hyperion(PlanetMoon):
    __planet__: Final = 22

class Iapetus(PlanetMoon):
    __planet__: Final = 23

class Ariel(PlanetMoon):
    __planet__: Final = 24

class Umbriel(PlanetMoon):
    __planet__: Final = 25

class Titania(PlanetMoon):
    __planet__: Final = 26

class Oberon(PlanetMoon):
    __planet__: Final = 27

class Miranda(PlanetMoon):
    __planet__: Final = 28

# Newton's method
def newton(f: Callable[[float], float], x0: float, x1: float, precision: float = ...) -> float:
    """
    Return an x-value at which the given function reaches zero.

    Stops and declares victory once the x-value is within ``precision``
    of the solution, which defaults to a half-second of clock time.
    """
    ...

# Equinox and solstice functions
def holiday(d0: _libastro._DateInitType, motion: float, offset: float) -> Date:
    """Function that assists the finding of equinoxes and solstices."""
    ...
def previous_vernal_equinox(date: _libastro._DateInitType) -> Date:
    """Return the date of the previous vernal equinox."""
    ...
def next_vernal_equinox(date: _libastro._DateInitType) -> Date:
    """Return the date of the next vernal equinox."""
    ...
def previous_summer_solstice(date: _libastro._DateInitType) -> Date:
    """Return the date of the previous summer solstice."""
    ...
def next_summer_solstice(date: _libastro._DateInitType) -> Date:
    """Return the date of the next summer solstice."""
    ...
def previous_autumnal_equinox(date: _libastro._DateInitType) -> Date:
    """Return the date of the previous autumnal equinox."""
    ...
def next_autumnal_equinox(date: _libastro._DateInitType) -> Date:
    """Return the date of the next autumnal equinox."""
    ...
def previous_winter_solstice(date: _libastro._DateInitType) -> Date:
    """Return the date of the previous winter solstice."""
    ...
def next_winter_solstice(date: _libastro._DateInitType) -> Date:
    """Return the date of the next winter solstice."""
    ...

# Synonyms
next_spring_equinox = next_vernal_equinox
previous_spring_equinox = previous_vernal_equinox
next_fall_equinox = next_autumnal_equinox
next_autumn_equinox = next_autumnal_equinox
previous_fall_equinox = previous_autumnal_equinox
previous_autumn_equinox = previous_autumnal_equinox

# More general equinox/solstice functions
def previous_equinox(date: _libastro._DateInitType) -> Date:
    """Return the date of the previous equinox."""
    ...
def next_equinox(date: _libastro._DateInitType) -> Date:
    """Return the date of the next equinox."""
    ...
def previous_solstice(date: _libastro._DateInitType) -> Date:
    """Return the date of the previous solstice."""
    ...
def next_solstice(date: _libastro._DateInitType) -> Date:
    """Return the date of the next solstice."""
    ...
def previous_new_moon(date: _libastro._DateInitType) -> Date:
    """Return the date of the previous New Moon."""
    ...
def next_new_moon(date: _libastro._DateInitType) -> Date:
    """Return the date of the next New Moon."""
    ...
def previous_first_quarter_moon(date: _libastro._DateInitType) -> Date:
    """Return the date of the previous First Quarter Moon."""
    ...
def next_first_quarter_moon(date: _libastro._DateInitType) -> Date:
    """Return the date of the next First Quarter Moon."""
    ...
def previous_full_moon(date: _libastro._DateInitType) -> Date:
    """Return the date of the previous Full Moon."""
    ...
def next_full_moon(date: _libastro._DateInitType) -> Date:
    """Return the date of the next Full Moon."""
    ...
def previous_last_quarter_moon(date: _libastro._DateInitType) -> Date:
    """Return the date of the previous Last Quarter Moon."""
    ...
def next_last_quarter_moon(date: _libastro._DateInitType) -> Date:
    """Return the date of the next Last Quarter Moon."""
    ...

# Exceptions
class CircumpolarError(ValueError): ...
class NeverUpError(CircumpolarError): ...
class AlwaysUpError(CircumpolarError): ...

# Observer class
class Observer(_libastro.Observer):
    """
    A location on earth for which positions are to be computed.

    An `Observer` instance allows you to compute the positions of
    celestial bodies as seen from a particular latitude and longitude on
    the Earth's surface.  The constructor takes no parameters; instead,
    set its attributes once you have created it.  Defaults:

    `date` - the moment the `Observer` is created
    `lat` - zero latitude
    `lon` - zero longitude
    `elevation` - 0 meters above sea level
    `horizon` - 0 degrees
    `epoch` - J2000
    `temp` - 15 degrees Celsius
    `pressure` - 1010 mBar
    """
    __slots__: list[str] = ["name"]

    name: object

    def copy(self) -> Self: ...
    __copy__ = copy
    def compute_pressure(self) -> None:
        """Set the atmospheric pressure for the current elevation."""
        ...
    def previous_transit(self, body: Body, start: _libastro._DateInitType | None = None) -> Date:
        """Find the previous passage of a body across the meridian."""
        ...
    def next_transit(self, body: Body, start: _libastro._DateInitType | None = None) -> Date:
        """Find the next passage of a body across the meridian."""
        ...
    def previous_antitransit(self, body: Body, start: _libastro._DateInitType | None = None) -> Date:
        """Find the previous passage of a body across the anti-meridian."""
        ...
    def next_antitransit(self, body: Body, start: _libastro._DateInitType | None = None) -> Date:
        """Find the next passage of a body across the anti-meridian."""
        ...
    def disallow_circumpolar(self, declination: float) -> None:
        """
        Raise an exception if the given declination is circumpolar.

        Raises NeverUpError if an object at the given declination is
        always below this Observer's horizon, or AlwaysUpError if such
        an object would always be above the horizon.
        """
        ...
    def previous_rising(self, body: Body, start: _libastro._DateInitType | None = None, use_center: bool = False) -> Date:
        """
        Search for the given body's previous rising, returning its date.

        The search starts at the `date` of this `Observer` and is limited to
        the single circuit of the sky, from antitransit to antitransit, that
        the `body` was in the middle of describing at that date and time.
        If the body did not, in fact, cross the horizon in the direction you
        are asking about during that particular circuit, then the search
        must raise a `CircumpolarError` exception like `NeverUpError` or
        `AlwaysUpError` instead of returning a date.
        """
        ...
    def previous_setting(self, body: Body, start: _libastro._DateInitType | None = None, use_center: bool = False) -> Date:
        """
        Search for the given body's previous setting, returning its date.

        The search starts at the `date` of this `Observer` and is limited to
        the single circuit of the sky, from antitransit to antitransit, that
        the `body` was in the middle of describing at that date and time.
        If the body did not, in fact, cross the horizon in the direction you
        are asking about during that particular circuit, then the search
        must raise a `CircumpolarError` exception like `NeverUpError` or
        `AlwaysUpError` instead of returning a date.
        """
        ...
    def next_rising(self, body: Body, start: _libastro._DateInitType | None = None, use_center: bool = False) -> Date:
        """
        Search for the given body's next rising, returning its date.

        The search starts at the `date` of this `Observer` and is limited to
        the single circuit of the sky, from antitransit to antitransit, that
        the `body` was in the middle of describing at that date and time.
        If the body did not, in fact, cross the horizon in the direction you
        are asking about during that particular circuit, then the search
        must raise a `CircumpolarError` exception like `NeverUpError` or
        `AlwaysUpError` instead of returning a date.
        """
        ...
    def next_setting(self, body: Body, start: _libastro._DateInitType | None = None, use_center: bool = False) -> Date:
        """
        Search for the given body's next setting, returning its date.

        The search starts at the `date` of this `Observer` and is limited to
        the single circuit of the sky, from antitransit to antitransit, that
        the `body` was in the middle of describing at that date and time.
        If the body did not, in fact, cross the horizon in the direction you
        are asking about during that particular circuit, then the search
        must raise a `CircumpolarError` exception like `NeverUpError` or
        `AlwaysUpError` instead of returning a date.
        """
        ...
    def next_pass(
        self, body: EarthSatellite, singlepass: bool = True
    ) -> tuple[Date | None, Date | None, Date | None, Date | None, Date | None, Date | None]:
        """
        Return the next rising, culmination, and setting of a satellite.

        If singlepass is True, return next consecutive set of
        ``(rising, culmination, setting)``.

        If singlepass is False, return
        ``(next_rising, next_culmination, next_setting)``.
        """
        ...

# Time conversion functions
def localtime(date: Date | float) -> _datetime:
    """Convert a PyEphem date into naive local time, returning a Python datetime."""
    ...

class _UTC(_tzinfo):
    ZERO: _timedelta
    def tzname(self, dt: _datetime | None, /) -> NoReturn:
        """datetime -> string name of time zone."""
        ...
    def utcoffset(self, dt: _datetime | None) -> _timedelta: ...
    def dst(self, dt: _datetime | None) -> _timedelta: ...

UTC: _UTC

def to_timezone(date: Date | float, tzinfo: _tzinfo) -> _datetime:
    """"Convert a PyEphem date into a timezone aware Python datetime representation."""
    ...

# Coordinate classes
class Coordinate:
    epoch: Date

    @overload
    def __init__(self, body: Body, *, epoch: _libastro._DateInitType | None = None) -> None: ...
    @overload
    def __init__(self, coord1: float | str, coord2: float | str, *, epoch: _libastro._DateInitType | None = None) -> None: ...
    @overload
    def __init__(self, coord: Coordinate, *, epoch: _libastro._DateInitType | None = None) -> None: ...

class Equatorial(Coordinate):
    """An equatorial sky coordinate in right ascension and declination."""
    ra: Angle
    dec: Angle

    def get(self) -> tuple[Angle, Angle]: ...
    def set(self, ra: float | str, dec: float | str) -> None: ...

    to_radec = get
    from_radec = set

class LonLatCoordinate(Coordinate):
    """A coordinate that is measured with a longitude and latitude."""
    lon: Angle
    lat: Angle

    def set(self, lon: float | str, lat: float | str) -> None: ...
    def get(self) -> tuple[Angle, Angle]: ...
    @property
    def long(self) -> Angle: ...
    @long.setter
    def long(self, value: Angle) -> None: ...

class Ecliptic(LonLatCoordinate):
    """An ecliptic latitude and longitude."""
    def to_radec(self) -> tuple[Angle, Angle]: ...
    def from_radec(self, ra: float | str, dec: float | str) -> None: ...

class Galactic(LonLatCoordinate):
    """A galactic latitude and longitude."""
    def to_radec(self) -> tuple[Angle, Angle]: ...
    def from_radec(self, ra: float | str, dec: float | str) -> None: ...

# Backwards compatibility aliases
date = Date
angle = Angle
LongLatCoordinate = LonLatCoordinate

# Catalog functions
@overload
def star(name: str, observer: Observer, /) -> FixedBody:
    """Load the stars database and return a star."""
    ...
@overload
def star(name: str, when: _libastro._DateInitType, epoch: _libastro._DateInitType) -> FixedBody:
    """Load the stars database and return a star."""
    ...
def city(name: str) -> Observer:
    """Load the cities database and return a city."""
    ...

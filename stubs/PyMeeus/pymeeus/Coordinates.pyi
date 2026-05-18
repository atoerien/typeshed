import datetime
from typing import Final, overload

from pymeeus.Angle import Angle
from pymeeus.Epoch import Epoch

NUTATION_ARG_TABLE: Final[list[list[int]]]
NUTATION_SINE_COEF_TABLE: Final[list[list[float]]]
NUTATION_COSINE_COEF_TABLE: Final[list[list[float]]]

@overload
def mean_obliquity(
    a: Epoch | list[float] | tuple[float, ...] | datetime.date,
    /,
    *,
    leap_seconds: float = 0,
    local: bool = False,
    utc: bool = False,
) -> Angle:
    """
    This function computes the mean obliquity (epsilon0) at the provided
    date.

    This function internally uses an :class:`Epoch` object, and the **utc**
    argument then controls the way the UTC->TT conversion is handled for that
    object. If **leap_seconds** argument is set to a value different than zero,
    then that value will be used for the UTC->TAI conversion, and the internal
    leap seconds table will be bypassed.

    :param args: Either :class:`Epoch`, date, datetime or year, month,
        day values, by themselves or inside a tuple or list
    :type args: int, float, :py:class:`Epoch`, datetime, date, tuple,
        list
    :param utc: Whether the provided epoch is a civil time (UTC) or TT
    :type utc: bool
    :param leap_seconds: This is the value to be used in the UTC->TAI
        conversion, instead of taking it from internal leap seconds table.
    :type leap_seconds: int, float

    :returns: The mean obliquity of the ecliptic, as an :class:`Angle`
    :rtype: :class:`Angle`
    :raises: ValueError if input values are in the wrong range.
    :raises: TypeError if input values are of wrong type.

    >>> e0 = mean_obliquity(1987, 4, 10)
    >>> a = e0.dms_tuple()
    >>> a[0]
    23
    >>> a[1]
    26
    >>> round(a[2], 3)
    27.407
    """
    ...
@overload
def mean_obliquity(
    year: int, month: int, day: int, /, *, leap_seconds: float = 0, local: bool = False, utc: bool = False
) -> Angle: ...

@overload
def true_obliquity(
    a: Epoch | list[float] | tuple[float, ...] | datetime.date,
    /,
    *,
    leap_seconds: float = 0,
    local: bool = False,
    utc: bool = False,
) -> Angle:
    """
    This function computes the true obliquity (epsilon) at the provided
    date. The true obliquity is the mean obliquity (epsilon0) plus the
    correction provided by the nutation in obliquity (Delta epsilon).

    This function internally uses an :class:`Epoch` object, and the **utc**
    argument then controls the way the UTC->TT conversion is handled for that
    object. If **leap_seconds** argument is set to a value different than zero,
    then that value will be used for the UTC->TAI conversion, and the internal
    leap seconds table will be bypassed.

    :param args: Either :class:`Epoch`, date, datetime or year, month,
        day values, by themselves or inside a tuple or list
    :type args: int, float, :py:class:`Epoch`, datetime, date, tuple,
        list
    :param utc: Whether the provided epoch is a civil time (UTC) or TT
    :type utc: bool
    :param leap_seconds: This is the value to be used in the UTC->TAI
        conversion, instead of taking it from internal leap seconds table.
    :type leap_seconds: int, float

    :returns: The true obliquity of the ecliptic, as an Angle
    :rtype: :class:`Angle`
    :raises: ValueError if input values are in the wrong range.
    :raises: TypeError if input values are of wrong type.

    >>> epsilon = true_obliquity(1987, 4, 10)
    >>> a = epsilon.dms_tuple()
    >>> a[0]
    23
    >>> a[1]
    26
    >>> round(a[2], 3)
    36.849
    """
    ...
@overload
def true_obliquity(
    year: int, month: int, day: int, /, *, leap_seconds: float = 0, local: bool = False, utc: bool = False
) -> Angle: ...

@overload
def nutation_longitude(
    a: Epoch | list[float] | tuple[float, ...] | datetime.date,
    /,
    *,
    leap_seconds: float = 0,
    local: bool = False,
    utc: bool = False,
) -> Angle:
    """
    This function computes the nutation in longitude (Delta psi) at the
    provided date.

    This function internally uses an :class:`Epoch` object, and the **utc**
    argument then controls the way the UTC->TT conversion is handled for that
    object. If **leap_seconds** argument is set to a value different than zero,
    then that value will be used for the UTC->TAI conversion, and the internal
    leap seconds table will be bypassed.

    :param args: Either :class:`Epoch`, date, datetime or year, month,
        day values, by themselves or inside a tuple or list
    :type args: int, float, :py:class:`Epoch`, datetime, date, tuple,
        list
    :param utc: Whether the provided epoch is a civil time (UTC) or TT
    :type utc: bool
    :param leap_seconds: This is the value to be used in the UTC->TAI
        conversion, instead of taking it from internal leap seconds table.
    :type leap_seconds: int, float

    :returns: The nutation in longitude (Delta psi), as an Angle
    :rtype: :class:`Angle`
    :raises: ValueError if input values are in the wrong range.
    :raises: TypeError if input values are of wrong type.

    >>> dpsi = nutation_longitude(1987, 4, 10)
    >>> a = dpsi.dms_tuple()
    >>> a[0]
    0
    >>> a[1]
    0
    >>> round(a[2], 3)
    3.788
    >>> a[3]
    -1.0
    """
    ...
@overload
def nutation_longitude(
    year: int, month: int, day: int, /, *, leap_seconds: float = 0, local: bool = False, utc: bool = False
) -> Angle: ...

@overload
def nutation_obliquity(
    a: Epoch | list[float] | tuple[float, ...] | datetime.date,
    /,
    *,
    leap_seconds: float = 0,
    local: bool = False,
    utc: bool = False,
) -> Angle:
    """
    This function computes the nutation in obliquity (Delta epsilon) at
    the provided date.

    This function internally uses an :class:`Epoch` object, and the **utc**
    argument then controls the way the UTC->TT conversion is handled for that
    object. If **leap_seconds** argument is set to a value different than zero,
    then that value will be used for the UTC->TAI conversion, and the internal
    leap seconds table will be bypassed.

    :param args: Either :class:`Epoch`, date, datetime or year, month,
        day values, by themselves or inside a tuple or list
    :type args: int, float, :py:class:`Epoch`, datetime, date, tuple,
        list
    :param utc: Whether the provided epoch is a civil time (UTC) or TT
    :type utc: bool
    :param leap_seconds: This is the value to be used in the UTC->TAI
        conversion, instead of taking it from internal leap seconds table.
    :type leap_seconds: int, float

    :returns: The nutation in obliquity (Delta epsilon), as an
        :class:`Angle`
    :rtype: :class:`Angle`
    :raises: ValueError if input values are in the wrong range.
    :raises: TypeError if input values are of wrong type.

    >>> depsilon = nutation_obliquity(1987, 4, 10)
    >>> a = depsilon.dms_tuple()
    >>> a[0]
    0
    >>> a[1]
    0
    >>> round(a[2], 3)
    9.443
    >>> a[3]
    1.0
    """
    ...
@overload
def nutation_obliquity(
    year: int, month: int, day: int, /, *, leap_seconds: float = 0, local: bool = False, utc: bool = False
) -> Angle: ...

def precession_equatorial(
    start_epoch: Epoch,
    final_epoch: Epoch,
    start_ra: Angle,
    start_dec: Angle,
    p_motion_ra: float | Angle = 0.0,
    p_motion_dec: float | Angle = 0.0,
) -> tuple[Angle, Angle]:
    """
    This function converts the equatorial coordinates (right ascension and
    declination) given for an epoch and a equinox, to the corresponding
    values for another epoch and equinox. Only the **mean** positions, i.e.
    the effects of precession and proper motion, are considered here.

    :param start_epoch: Initial epoch when initial coordinates are given
    :type start_epoch: :py:class:`Epoch`
    :param final_epoch: Final epoch for when coordinates are going to be
        computed
    :type final_epoch: :py:class:`Epoch`
    :param start_ra: Initial right ascension
    :type start_ra: :py:class:`Angle`
    :param start_dec: Initial declination
    :type start_dec: :py:class:`Angle`
    :param p_motion_ra: Proper motion in right ascension, in degrees per
        year. Zero by default.
    :type p_motion_ra: :py:class:`Angle`
    :param p_motion_dec: Proper motion in declination, in degrees per year.
        Zero by default.
    :type p_motion_dec: :py:class:`Angle`

    :returns: Equatorial coordinates (right ascension, declination, in that
        order) corresponding to the final epoch, given as two objects
        :class:`Angle` inside a tuple
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.

    >>> start_epoch = JDE2000
    >>> final_epoch = Epoch(2028, 11, 13.19)
    >>> alpha0 = Angle(2, 44, 11.986, ra=True)
    >>> delta0 = Angle(49, 13, 42.48)
    >>> pm_ra = Angle(0, 0, 0.03425, ra=True)
    >>> pm_dec = Angle(0, 0, -0.0895)
    >>> alpha, delta = precession_equatorial(start_epoch, final_epoch, alpha0,
    ...                                      delta0, pm_ra, pm_dec)
    >>> print(alpha.ra_str(False, 3))
    2:46:11.331
    >>> print(delta.dms_str(False, 2))
    49:20:54.54
    """
    ...
def precession_ecliptical(
    start_epoch: Epoch,
    final_epoch: Epoch,
    start_lon: Angle,
    start_lat: Angle,
    p_motion_lon: float | Angle = 0.0,
    p_motion_lat: float | Angle = 0.0,
) -> tuple[Angle, Angle]:
    """
    This function converts the ecliptical coordinates (longitude and
    latitude) given for an epoch and a equinox, to the corresponding
    values for another epoch and equinox. Only the **mean** positions, i.e.
    the effects of precession and proper motion, are considered here.

    :param start_epoch: Initial epoch when initial coordinates are given
    :type start_epoch: :py:class:`Epoch`
    :param final_epoch: Final epoch for when coordinates are going to be
        computed
    :type final_epoch: :py:class:`Epoch`
    :param start_lon: Initial longitude
    :type start_lon: :py:class:`Angle`
    :param start_lat: Initial latitude
    :type start_lat: :py:class:`Angle`
    :param p_motion_lon: Proper motion in longitude, in degrees per year.
        Zero by default.
    :type p_motion_lon: :py:class:`Angle`
    :param p_motion_lat: Proper motion in latitude, in degrees per year.
        Zero by default.
    :type p_motion_lat: :py:class:`Angle`

    :returns: Ecliptical coordinates (longitude, latitude, in that order)
        corresponding to the final epoch, given as two :class:`Angle`
        objects inside a tuple
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.

    >>> start_epoch = JDE2000
    >>> final_epoch = Epoch(-214, 6, 30.0)
    >>> lon0 = Angle(149.48194)
    >>> lat0 = Angle(1.76549)
    >>> lon, lat = precession_ecliptical(start_epoch, final_epoch, lon0, lat0)
    >>> print(round(lon(), 3))
    118.704
    >>> print(round(lat(), 3))
    1.615
    """
    ...
def p_motion_equa2eclip(
    p_motion_ra: Angle, p_motion_dec: Angle, ra: Angle, dec: Angle, lat: Angle, epsilon: Angle
) -> tuple[float, float]:
    """
    It is usual that proper motions are given in equatorial coordinates,
    not in ecliptical ones. Therefore, this function converts the provided
    proper motions in equatorial coordinates to the corresponding ones in
    ecliptical coordinates.

    :param p_motion_ra: Proper motion in right ascension, in degrees per
        year, as an :class:`Angle` object
    :type p_motion_ra: :py:class:`Angle`
    :param p_motion_dec: Proper motion in declination, in degrees per year,
        as an :class:`Angle` object
    :type p_motion_dec: :py:class:`Angle`
    :param ra: Right ascension of the astronomical object, as degrees in an
        :class:`Angle` object
    :type ra: :py:class:`Angle`
    :param dec: Declination of the astronomical object, as degrees in an
        :class:`Angle` object
    :type dec: :py:class:`Angle`
    :param lat: Ecliptical latitude of the astronomical object, as degrees
        in an :class:`Angle` object
    :type lat: :py:class:`Angle`
    :param epsilon: Obliquity of the ecliptic
    :type epsilon: :py:class:`Angle`

    :returns: Proper motions in ecliptical longitude and latitude (in that
        order), given as two :class:`Angle` objects inside a tuple
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.
    """
    ...
def precession_newcomb(
    start_epoch: Epoch,
    final_epoch: Epoch,
    start_ra: Angle,
    start_dec: Angle,
    p_motion_ra: float | Angle = 0.0,
    p_motion_dec: float | Angle = 0.0,
) -> tuple[Angle, Angle]:
    """
    This function implements the Newcomb precessional equations used in
    the old FK4 system. It takes equatorial coordinates (right ascension
    and declination) given for an epoch and a equinox, and converts them to
    the corresponding values for another epoch and equinox. Only the
    **mean** positions, i.e. the effects of precession and proper motion,
    are considered here.

    :param start_epoch: Initial epoch when initial coordinates are given
    :type start_epoch: :py:class:`Epoch`
    :param final_epoch: Final epoch for when coordinates are going to be
        computed
    :type final_epoch: :py:class:`Epoch`
    :param start_ra: Initial right ascension
    :type start_ra: :py:class:`Angle`
    :param start_dec: Initial declination
    :type start_dec: :py:class:`Angle`
    :param p_motion_ra: Proper motion in right ascension, in degrees per
        year. Zero by default.
    :type p_motion_ra: :py:class:`Angle`
    :param p_motion_dec: Proper motion in declination, in degrees per year.
        Zero by default.
    :type p_motion_dec: :py:class:`Angle`

    :returns: Equatorial coordinates (right ascension, declination, in that
        order) corresponding to the final epoch, given as two objects
        :class:`Angle` inside a tuple
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.
    """
    ...
def motion_in_space(
    start_ra: Angle,
    start_dec: Angle,
    distance: float,
    velocity: float,
    p_motion_ra: float | Angle,
    p_motion_dec: float | Angle,
    time: float,
) -> tuple[Angle, Angle]:
    """
    This function computes the star's true motion through space relative
    to the Sun, allowing to compute the start proper motion at a given
    time.

    :param start_ra: Initial right ascension
    :type start_ra: :py:class:`Angle`
    :param start_dec: Initial declination
    :type start_dec: :py:class:`Angle`
    :param distance: Star's distance to the Sun, in parsecs. If distance is
        given in light-years, multipy it by 0.3066. If the star's parallax
        **pie** (in arcseconds) is given, use (1.0/pie).
    :type distance: float
    :param velocity: Radial velocity in km/s
    :type velocity: float
    :param p_motion_ra: Proper motion in right ascension, in degrees per
        year.
    :type p_motion_ra: :py:class:`Angle`
    :param p_motion_dec: Proper motion in declination, in degrees per year.
    :type p_motion_dec: :py:class:`Angle`
    :param time: Number of years since starting epoch, positive in the
        future, negative in the past
    :type time: float

    :returns: Equatorial coordinates (right ascension, declination, in that
        order) corresponding to the final epoch, given as two objects
        :class:`Angle` inside a tuple
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.

    >>> ra = Angle(6, 45, 8.871, ra=True)
    >>> dec = Angle(-16.716108)
    >>> pm_ra = Angle(0, 0, -0.03847, ra=True)
    >>> pm_dec = Angle(0, 0, -1.2053)
    >>> dist = 2.64
    >>> vel = -7.6
    >>> alpha, delta = motion_in_space(ra, dec, dist, vel, pm_ra, pm_dec,
    ...                                -1000.0)
    >>> print(alpha.ra_str(False, 2))
    6:45:47.16
    >>> print(delta.dms_str(False, 1))
    -16:22:56.0
    >>> alpha, delta = motion_in_space(ra, dec, dist, vel, pm_ra, pm_dec,
    ...                                -4000.0)
    >>> print(alpha.ra_str(False, 2))
    6:47:39.91
    >>> print(delta.dms_str(False, 1))
    -15:23:30.6
    """
    ...
def equatorial2ecliptical(right_ascension: Angle, declination: Angle, obliquity: Angle) -> tuple[Angle, Angle]:
    """
    This function converts from equatorial coordinated (right ascension and
    declination) to ecliptical coordinates (longitude and latitude).

    :param right_ascension: Right ascension, as an Angle object
    :type start_epoch: :py:class:`Angle`
    :param declination: Declination, as an Angle object
    :type start_epoch: :py:class:`Angle`
    :param obliquity: Obliquity of the ecliptic, as an Angle object
    :type obliquity: :py:class:`Angle`

    :returns: Ecliptical coordinates (longitude, latitude, in that order),
        given as two :class:`Angle` objects inside a tuple
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.

    >>> ra = Angle(7, 45, 18.946, ra=True)
    >>> dec = Angle(28, 1, 34.26)
    >>> epsilon = Angle(23.4392911)
    >>> lon, lat = equatorial2ecliptical(ra, dec, epsilon)
    >>> print(round(lon(), 5))
    113.21563
    >>> print(round(lat(), 5))
    6.68417
    """
    ...
def ecliptical2equatorial(longitude: Angle, latitude: Angle, obliquity: Angle) -> tuple[Angle, Angle]:
    """
    This function converts from ecliptical coordinates (longitude and
    latitude) to equatorial coordinated (right ascension and declination).

    :param longitude: Ecliptical longitude, as an Angle object
    :type longitude: :py:class:`Angle`
    :param latitude: Ecliptical latitude, as an Angle object
    :type latitude: :py:class:`Angle`
    :param obliquity: Obliquity of the ecliptic, as an Angle object
    :type obliquity: :py:class:`Angle`

    :returns: Equatorial coordinates (right ascension, declination, in that
        order), given as two :class:`Angle` objects inside a tuple
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.

    >>> lon = Angle(113.21563)
    >>> lat = Angle(6.68417)
    >>> epsilon = Angle(23.4392911)
    >>> ra, dec = ecliptical2equatorial(lon, lat, epsilon)
    >>> print(ra.ra_str(n_dec=3))
    7h 45' 18.946''
    >>> print(dec.dms_str(n_dec=2))
    28d 1' 34.26''
    """
    ...
def equatorial2horizontal(hour_angle: Angle, declination: Angle, geo_latitude: Angle) -> tuple[Angle, Angle]:
    """
    This function converts from equatorial coordinates (right ascension and
    declination) to local horizontal coordinates (azimuth and elevation).

    Following Meeus' convention, the azimuth is measured westward from the
    SOUTH. If you want the azimuth to be measured from the north (common custom
    between navigators and meteorologits), you should add 180 degrees.

    The hour angle (H) comprises information about the sidereal time, the
    observer's geodetic longitude (positive west from Greenwich) and the right
    ascension. If theta is the local sidereal time, theta0 the sidereal time at
    Greenwich, lon the observer's longitude and ra the right ascension, the
    following expressions hold:

        H = theta - ra
        H = theta0 - lon - ra

    :param hour_angle: Hour angle, as an Angle object
    :type hour_angle: :py:class:`Angle`
    :param declination: Declination, as an Angle object
    :type declination: :py:class:`Angle`
    :param geo_latitude: Geodetic latitude of the observer, as an Angle object
    :type geo_latitude: :py:class:`Angle`

    :returns: Local horizontal coordinates (azimuth, elevation, in that order),
        given as two :class:`Angle` objects inside a tuple
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.

    >>> lon = Angle(77, 3, 56)
    >>> lat = Angle(38, 55, 17)
    >>> ra = Angle(23, 9, 16.641, ra=True)
    >>> dec = Angle(-6, 43, 11.61)
    >>> theta0 = Angle(8, 34, 57.0896, ra=True)
    >>> eps = Angle(23, 26, 36.87)
    >>> delta = Angle(0, 0, ((-3.868*cos(eps.rad()))/15.0), ra=True)
    >>> theta0 += delta
    >>> h = theta0 - lon - ra
    >>> azi, ele = equatorial2horizontal(h, dec, lat)
    >>> print(round(azi, 3))
    68.034
    >>> print(round(ele, 3))
    15.125
    """
    ...
def horizontal2equatorial(azimuth: Angle, elevation: Angle, geo_latitude: Angle) -> tuple[Angle, Angle]:
    """
    This function converts from local horizontal coordinates (azimuth and
    elevation) to equatorial coordinates (right ascension and declination).

    Following Meeus' convention, the azimuth is measured westward from the
    SOUTH.

    This function returns the hour angle and the declination. The hour angle
    (H) comprises information about the sidereal time, the observer's geodetic
    longitude (positive west from Greenwich) and the right ascension. If theta
    is the local sidereal time, theta0 the sidereal time at Greenwich, lon the
    observer's longitude and ra the right ascension, the following expressions
    hold:

        H = theta - ra
        H = theta0 - lon - ra

    :param azimuth: Azimuth, measured westward from south, as an Angle object
    :type azimuth: :py:class:`Angle`
    :param elevation: Elevation from the horizon, as an Angle object
    :type elevation: :py:class:`Angle`
    :param geo_latitude: Geodetic latitude of the observer, as an Angle object
    :type geo_latitude: :py:class:`Angle`

    :returns: Equatorial coordinates (as hour angle and declination, in that
        order), given as two :class:`Angle` objects inside a tuple
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.

    >>> azi = Angle(68.0337)
    >>> ele = Angle(15.1249)
    >>> lat = Angle(38, 55, 17)
    >>> h, dec = horizontal2equatorial(azi, ele, lat)
    >>> print(round(h, 4))
    64.3521
    >>> print(dec.dms_str(n_dec=0))
    -6d 43' 12.0''
    """
    ...
def equatorial2galactic(right_ascension: Angle, declination: Angle) -> tuple[Angle, Angle]:
    """
    This function converts from equatorial coordinates (right ascension and
    declination) to galactic coordinates (longitude and latitude).

    The current galactic system of coordinates was defined by the International
    Astronomical Union in 1959, using the standard equatorial system of epoch
    B1950.0.

    :param right_ascension: Right ascension, as an Angle object
    :type right_ascension: :py:class:`Angle`
    :param declination: Declination, as an Angle object
    :type declination: :py:class:`Angle`

    :returns: Galactic coordinates (longitude and latitude, in that order),
        given as two :class:`Angle` objects inside a tuple
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.

    >>> ra = Angle(17, 48, 59.74, ra=True)
    >>> dec = Angle(-14, 43, 8.2)
    >>> lon, lat = equatorial2galactic(ra, dec)
    >>> print(round(lon, 4))
    12.9593
    >>> print(round(lat, 4))
    6.0463
    """
    ...
def galactic2equatorial(longitude: Angle, latitude: Angle) -> tuple[Angle, Angle]:
    """
    This function converts from galactic coordinates (longitude and
    latitude) to equatorial coordinates (right ascension and declination).

    The current galactic system of coordinates was defined by the International
    Astronomical Union in 1959, using the standard equatorial system of epoch
    B1950.0.

    :param longitude: Longitude, as an Angle object
    :type longitude: :py:class:`Angle`
    :param latitude: Latitude, as an Angle object
    :type latitude: :py:class:`Angle`

    :returns: Equatorial coordinates (right ascension and declination, in that
        order), given as two :class:`Angle` objects inside a tuple
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.

    >>> lon = Angle(12.9593)
    >>> lat = Angle(6.0463)
    >>> ra, dec = galactic2equatorial(lon, lat)
    >>> print(ra.ra_str(n_dec=1))
    17h 48' 59.7''
    >>> print(dec.dms_str(n_dec=0))
    -14d 43' 8.0''
    """
    ...
def parallactic_angle(hour_angle: Angle, declination: Angle, geo_latitude: Angle) -> Angle | None:
    """
    This function computes the parallactic angle, an apparent rotation that
    appears because celestial bodies move along parallel circles. By
    convention, the parallactic angle is negative before the passage through
    the southern meridian (in the north hemisphere), and positive afterwards.
    Exactly on the meridian, its value is zero.

    Please note that when the celestial body is exactly at the zenith, the
    parallactic angle is not defined, and this function will return 'None'.

    The hour angle (H) comprises information about the sidereal time, the
    observer's geodetic longitude (positive west from Greenwich) and the right
    ascension. If theta is the local sidereal time, theta0 the sidereal time at
    Greenwich, lon the observer's longitude and ra the right ascension, the
    following expressions hold:

        H = theta - ra
        H = theta0 - lon - ra

    :param hour_angle: Hour angle, as an Angle object
    :type hour_angle: :py:class:`Angle`
    :param declination: Declination, as an Angle object
    :type declination: :py:class:`Angle`
    :param geo_latitude: Geodetic latitude of the observer, as an Angle object
    :type geo_latitude: :py:class:`Angle`

    :returns: Parallactic angle as an py:class:`Angle` object
    :rtype: :py:class:`Angle`
    :raises: TypeError if input values are of wrong type.

    >>> hour_angle = Angle(0.0)
    >>> declination = Angle(45.0)
    >>> latitude = Angle(50.0)
    >>> q = parallactic_angle(hour_angle, declination, latitude)
    >>> print(q.dms_str(n_dec=1))
    0d 0' 0.0''
    """
    ...
def ecliptic_horizon(local_sidereal_time: Angle, geo_latitude: Angle, obliquity: Angle) -> tuple[Angle, Angle, Angle]:
    """
    This function returns the longitudes of the two points of the ecliptic
    which are on the horizon, as well as the angle between the ecliptic and the
    horizon.

    :param local_sidereal_time: Local sidereal time, as an Angle object
    :type local_sidereal_time: :py:class:`Angle`
    :param geo_latitude: Geodetic latitude, as an Angle object
    :type geo_latitude: :py:class:`Angle`
    :param obliquity: Obliquity of the ecliptic, as an Angle object
    :type obliquity: :py:class:`Angle`

    :returns: Longitudes of the two points of the ecliptic which are on the
        horizon, and the angle between the ecliptic and the horizon (in that
        order), given as three :class:`Angle` objects inside a tuple
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.

    >>> sidereal_time = Angle(5.0, ra=True)
    >>> lat = Angle(51.0)
    >>> epsilon = Angle(23.44)
    >>> lon1, lon2, i = ecliptic_horizon(sidereal_time, lat, epsilon)
    >>> print(lon1.dms_str(n_dec=1))
    169d 21' 29.9''
    >>> print(lon2.dms_str(n_dec=1))
    349d 21' 29.9''
    >>> print(round(i, 0))
    62.0
    """
    ...
def ecliptic_equator(longitude: Angle, latitude: Angle, obliquity: Angle) -> Angle:
    """
    This function returns the angle between the direction of the northern
    celestial pole and the direction of the north pole of the ecliptic, taking
    as reference the point whose ecliptic longitude and latitude are given.

    Please note that if we make latitude=0, the result is the angle between the
    ecliptic (at the given ecliptical longitude) and the east-west direction on
    the celestial sphere.

    :param longitude: Ecliptical longitude, as an Angle object
    :type longitude: :py:class:`Angle`
    :param latitude: Ecliptical latitude, as an Angle object
    :type latitude: :py:class:`Angle`
    :param obliquity: Obliquity of the ecliptic, as an Angle object
    :type obliquity: :py:class:`Angle`

    :returns: Angle between the direction of the northern celestial pole and
        the direction of the north pole of the ecliptic, given as one
        :class:`Angle` object
    :rtype: :class:`Angle`
    :raises: TypeError if input values are of wrong type.

    >>> lon = Angle(0.0)
    >>> lat = Angle(0.0)
    >>> eps = Angle(23.5)
    >>> ang_ecl_equ = ecliptic_equator(lon, lat, eps)
    >>> print(ang_ecl_equ.dms_str(n_dec=1))
    156d 30' 0.0''
    """
    ...
def diurnal_path_horizon(declination: Angle, geo_latitude: Angle) -> Angle:
    """
    This function returns the angle of the diurnal path of a celestial body
    relative to the horizon at the time of its rising or setting.

    :param declination: Declination, as an Angle object
    :type declination: :py:class:`Angle`
    :param geo_latitude: Geodetic latitude, as an Angle object
    :type geo_latitude: :py:class:`Angle`

    :returns: Angle of the diurnal path of the celestial body relative to the
        horizon at the time of rising or setting, given as one
        :class:`Angle` object
    :rtype: :class:`Angle`
    :raises: TypeError if input values are of wrong type.

    >>> declination = Angle(23.44)
    >>> latitude = Angle(40.0)
    >>> path_angle = diurnal_path_horizon(declination, latitude)
    >>> print(path_angle.dms_str(n_dec=1))
    45d 31' 28.4''
    """
    ...
def times_rise_transit_set(
    longitude: Angle,
    latitude: Angle,
    alpha1: Angle,
    delta1: Angle,
    alpha2: Angle,
    delta2: Angle,
    alpha3: Angle,
    delta3: Angle,
    h0: Angle,
    delta_t: float,
    theta0: Angle,
) -> tuple[float, float, float] | tuple[None, None, None]:
    """
    This function computes the times (in Universal Time UT) of rising,
    transit and setting of a given celestial body.

    .. note:: If the body is circumpolar there are no rising, transit nor
        setting times. In such a case a tuple with None's is returned

    .. note:: Care must be taken when interpreting the results. For instance,
        if the setting time is **smaller** than the rising time, it means that
        it belongs to the **following** day. Also, if the rising time is
        **bigger** than the setting time, it belong to the **previous** day.
        The same applies to the transit time.

    :param longitude: Geodetic longitude, as an Angle object. It is measured
        positively west from Greenwich, and negatively to the east.
    :type longitude: :py:class:`Angle`
    :param latitude: Geodetic latitude, as an Angle object
    :type latitude: :py:class:`Angle`
    :param alpha1: Apparent right ascension the previous day at 0h TT, as an
        Angle object
    :type alpha1: :py:class:`Angle`
    :param delta1: Apparent declination the previous day at 0h TT, as an Angle
        object
    :type delta1: :py:class:`Angle`
    :param alpha2: Apparent right ascension the current day at 0h TT, as an
        Angle object
    :type alpha2: :py:class:`Angle`
    :param delta2: Apparent declination the current day at 0h TT, as an Angle
        object
    :type delta2: :py:class:`Angle`
    :param alpha3: Apparent right ascension the following day at 0h TT, as an
        Angle object
    :type alpha3: :py:class:`Angle`
    :param delta3: Apparent declination the following day at 0h TT, as an Angle
        object
    :type delta3: :py:class:`Angle`
    :param h0: 'Standard' altitude: the geometric altitude of the center of the
        body at the time of apparent rising or setting, as degrees in an Angle
        object. It should be -0.5667 deg for stars and planets, -0.8333 deg
        for the Sun, and 0.125 deg for the Moon.
    :type h0: :py:class:`Angle`
    :param delta_t: The difference between Terrestrial Time and Universal Time
        (TT - UT) in seconds of time
    :type delta_t: float
    :param theta0: Apparent sidereal time at 0h TT on the current day for the
        meridian of Greenwich, as degrees in an Angle object
    :type theta0: :py:class:`Angle`

    :returns: A tuple with the times of rising, transit and setting, in that
        order, as hours in UT.
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.

    >>> longitude = Angle(71, 5, 0.0)
    >>> latitude = Angle(42, 20, 0.0)
    >>> alpha1 = Angle(2, 42, 43.25, ra=True)
    >>> delta1 = Angle(18, 2, 51.4)
    >>> alpha2 = Angle(2, 46, 55.51, ra=True)
    >>> delta2 = Angle(18, 26, 27.3)
    >>> alpha3 = Angle(2, 51, 7.69, ra=True)
    >>> delta3 = Angle(18, 49, 38.7)
    >>> h0 = Angle(-0.5667)
    >>> delta_t = 56.0
    >>> theta0 = Angle(11, 50, 58.1, ra=True)
    >>> rising, transit, setting = times_rise_transit_set(longitude, latitude,                                                          alpha1, delta1,                                                           alpha2, delta2,                                                           alpha3, delta3, h0,                                                           delta_t, theta0)
    >>> print(round(rising, 4))
    12.4238
    >>> print(round(transit, 3))
    19.675
    >>> print(round(setting, 3))
    2.911
    """
    ...
def refraction_apparent2true(apparent_elevation: Angle, pressure: float = 1010.0, temperature: float = 10.0) -> Angle:
    """
    This function computes the atmospheric refraction converting from the
    apparent elevation (i.e., the observed elevation through the air) to the
    true, 'airless', elevation.

    .. note:: This function, by default, assumes that the atmospheric pressure
        is 1010 milibars, and the air temperature is 10 Celsius.

    .. note:: Due to the numerous factors that may affect the atmospheric
        refraction, especially near the horizon, the values given by this
        function are approximate values.

    :param apparent_elevation: The elevation, in degrees and as an Angle
        object, of a given celestial object when observed through the
        normal atmosphere
    :type apparent_elevation: :py:class:`Angle`
    :param pressure: Atmospheric pressure at the observation point, in milibars
    :type pressure: float
    :param temperature: Atmospheric temperature at the observation point, in
        degrees Celsius
    :type temperature: :float

    :returns: An Angle object with the true, 'airless' elevation of the
        celestial object
    :rtype: :py:class:`Angle`
    :raises: TypeError if input values are of wrong type.

    >>> apparent_elevation = Angle(0, 30, 0.0)
    >>> true_elevation = refraction_apparent2true(apparent_elevation)
    >>> print(true_elevation.dms_str(n_dec=1))
    1' 14.7''
    """
    ...
def refraction_true2apparent(true_elevation: Angle, pressure: float = 1010.0, temperature: float = 10.0) -> Angle:
    """
    This function computes the atmospheric refraction converting from the
    true, 'airless', elevation (i.e., the one computed from celestial
    coordinates) to the apparent elevation (the observed elevation through the
    air)

    .. note:: This function, by default, assumes that the atmospheric pressure
        is 1010 milibars, and the air temperature is 10 Celsius.

    .. note:: Due to the numerous factors that may affect the atmospheric
        refraction, especially near the horizon, the values given by this
        function are approximate values.

    :param true_elevation: The elevation, in degrees and as an Angle
        object, of a given celestial object when computed from celestial
        coordinates, and assuming there is no atmospheric refraction due to the
        air
    :type true_elevation: :py:class:`Angle`
    :param pressure: Atmospheric pressure at the observation point, in milibars
    :type pressure: float
    :param temperature: Atmospheric temperature at the observation point, in
        degrees Celsius
    :type temperature: :float

    :returns: An Angle object with the aparent, 'with air' elevation of the
        celestial object
    :rtype: :py:class:`Angle`
    :raises: TypeError if input values are of wrong type.

    >>> true_elevation = Angle(0, 33, 14.76)
    >>> apparent_elevation = refraction_true2apparent(true_elevation)
    >>> print(apparent_elevation.dms_str(n_dec=2))
    57' 51.96''
    """
    ...
def angular_separation(alpha1: Angle, delta1: Angle, alpha2: Angle, delta2: Angle) -> Angle:
    """
    This function computes the angular distance between two celestial bodies
    whose right ascensions and declinations are given.

    .. note:: It is possible to use this formula with ecliptial (celestial)
        longitudes and latitudes instead of right ascensions and declinations,
        respectively.

    :param alpha1: Right ascension of celestial body #1, as an Angle object
    :type alpha1: :py:class:`Angle`
    :param delta1: Declination of celestial body #1, as an Angle object
    :type delta1: :py:class:`Angle`
    :param alpha2: Right ascension of celestial body #2, as an Angle object
    :type alpha2: :py:class:`Angle`
    :param delta2: Declination of celestial body #2, as an Angle object
    :type delta2: :py:class:`Angle`

    :returns: An Angle object with the angular separation between the given
        celestial objects
    :rtype: :py:class:`Angle`
    :raises: TypeError if input values are of wrong type.

    >>> alpha1 = Angle(14, 15, 39.7, ra=True)
    >>> delta1 = Angle(19, 10, 57.0)
    >>> alpha2 = Angle(13, 25, 11.6, ra=True)
    >>> delta2 = Angle(-11, 9, 41.0)
    >>> sep_ang = angular_separation(alpha1, delta1, alpha2, delta2)
    >>> print(round(sep_ang, 3))
    32.793
    """
    ...
def minimum_angular_separation(
    alpha1_1: Angle,
    delta1_1: Angle,
    alpha1_2: Angle,
    delta1_2: Angle,
    alpha1_3: Angle,
    delta1_3: Angle,
    alpha2_1: Angle,
    delta2_1: Angle,
    alpha2_2: Angle,
    delta2_2: Angle,
    alpha2_3: Angle,
    delta2_3: Angle,
) -> tuple[float, Angle]:
    """
    Given the positions at three different instants of times (equidistant)
    of two celestial objects, this function computes the minimum angular
    distance that will be achieved within that interval of time.

    .. note:: Suffix '1 _' is for the first celestial object, and '2 _' is for
        the second one.

    .. note:: This function provides as output the 'n' fraction of time when
        the minimum angular separation is achieved. For that, the epoch in the
        middle is assigned the value "n = 0". Therefore, n < 0 is for times
        **before** the middle epoch, and n > 0 is for times **after** the
        middle epoch.

    :param alpha1_1: First right ascension of celestial body #1, as an Angle
        object
    :type alpha1_1: :py:class:`Angle`
    :param delta1_1: First declination of celestial body #1, as an Angle object
    :type delta1_1: :py:class:`Angle`
    :param alpha1_2: Second right ascension of celestial body #1, as an Angle
        object
    :type alpha1_2: :py:class:`Angle`
    :param delta1_2: Second declination of celestial body #1, as Angle object
    :type delta1_2: :py:class:`Angle`
    :param alpha1_3: Third right ascension of celestial body #1, as an Angle
        object
    :type alpha1_3: :py:class:`Angle`
    :param delta1_3: Third declination of celestial body #1, as an Angle object
    :type delta1_3: :py:class:`Angle`
    :param alpha2_1: First right ascension of celestial body #2, as an Angle
        object
    :type alpha2_1: :py:class:`Angle`
    :param delta2_1: First declination of celestial body #2, as an Angle object
    :type delta2_1: :py:class:`Angle`
    :param alpha2_2: Second right ascension of celestial body #2, as an Angle
        object
    :type alpha2_2: :py:class:`Angle`
    :param delta2_2: Second declination of celestial body #2, as Angle object
    :type delta2_2: :py:class:`Angle`
    :param alpha2_3: Third right ascension of celestial body #2, as an Angle
        object
    :type alpha2_3: :py:class:`Angle`
    :param delta2_3: Third declination of celestial body #2, as an Angle object
    :type delta2_3: :py:class:`Angle`

    :returns: A tuple with two components: The first component is a float
        containing the 'n' fraction of time when the minimum angular separation
        is achieved. The second component is an Angle object containing the
        minimum angular separation between the given celestial objects
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.

    >>> alpha1_1 = Angle(10, 29, 44.27, ra=True)
    >>> delta1_1 = Angle(11, 2, 5.9)
    >>> alpha2_1 = Angle(10, 33, 29.64, ra=True)
    >>> delta2_1 = Angle(10, 40, 13.2)
    >>> alpha1_2 = Angle(10, 36, 19.63, ra=True)
    >>> delta1_2 = Angle(10, 29, 51.7)
    >>> alpha2_2 = Angle(10, 33, 57.97, ra=True)
    >>> delta2_2 = Angle(10, 37, 33.4)
    >>> alpha1_3 = Angle(10, 43, 1.75, ra=True)
    >>> delta1_3 = Angle(9, 55, 16.7)
    >>> alpha2_3 = Angle(10, 34, 26.22, ra=True)
    >>> delta2_3 = Angle(10, 34, 53.9)
    >>> a = minimum_angular_separation(alpha1_1, delta1_1, alpha1_2, delta1_2,                                       alpha1_3, delta1_3, alpha2_1, delta2_1,                                       alpha2_2, delta2_2, alpha2_3, delta2_3)
    >>> print(round(a[0], 6))
    -0.370726
    >>> print(a[1].dms_str(n_dec=0))
    3' 44.0''
    """
    ...
def relative_position_angle(alpha1: Angle, delta1: Angle, alpha2: Angle, delta2: Angle) -> Angle:
    """
    This function computes the position angle P of a body with respect to
    another body.

    :param alpha1: Right ascension of celestial body #1, as an Angle object
    :type alpha1: :py:class:`Angle`
    :param delta1: Declination of celestial body #1, as an Angle object
    :type delta1: :py:class:`Angle`
    :param alpha2: Right ascension of celestial body #2, as an Angle object
    :type alpha2: :py:class:`Angle`
    :param delta2: Declination of celestial body #2, as an Angle object
    :type delta2: :py:class:`Angle`

    :returns: An Angle object with the relative position angle between the
        given celestial objects
    :rtype: :py:class:`Angle`
    :raises: TypeError if input values are of wrong type.

    >>> alpha1 = Angle(14, 15, 39.7, ra=True)
    >>> delta1 = Angle(19, 10, 57.0)
    >>> alpha2 = Angle(14, 15, 39.7, ra=True)
    >>> delta2 = Angle(-11, 9, 41.0)
    >>> pos_ang = relative_position_angle(alpha1, delta1, alpha2, delta2)
    >>> print(round(pos_ang, 1))
    0.0
    """
    ...
def planetary_conjunction(
    alpha1_list: list[Angle] | tuple[Angle, ...],
    delta1_list: list[Angle] | tuple[Angle, ...],
    alpha2_list: list[Angle] | tuple[Angle, ...],
    delta2_list: list[Angle] | tuple[Angle, ...],
) -> tuple[float, Angle]:
    """
    Given the positions of two planets passing near each other, this
    function computes the time of conjunction in right ascension, and the
    difference in declination of the two bodies at that time.

    .. note:: This function provides as output the 'n' fraction of time when
        the minimum angular separation is achieved. For that, the epoch in the
        middle is assigned the value "n = 0". Therefore, n < 0 is for times
        **before** the middle epoch, and n > 0 is for times **after** the
        middle epoch.

    .. note:: When the entries in the input values are more than three and
        even, the last entry is discarted and an odd number of entries will be
        used.

    :param alpha1_list: List (or tuple) containing the right ascensions (as
        Angle objects) for object #1 (minimum 3 entries)
    :type alpha1_list: list, tuple of :py:class:`Angle`
    :param delta1_list: List (or tuple) containing the declinations (as Angle
        objects) for object #1 (minimum 3 entries)
    :type delta1_list: list, tuple of :py:class:`Angle`
    :param alpha2_list: List (or tuple) containing the right ascensions (as
        Angle objects) for object #2 (minimum 3 entries)
    :type alpha2_list: list, tuple of :py:class:`Angle`
    :param delta2_list: List (or tuple) containing the declinations (as Angle
        objects) for object #2 (minimum 3 entries)
    :type delta2_list: list, tuple of :py:class:`Angle`

    :returns: A tuple with two components: The first component is a float
        containing the 'n' fraction of time when the conjunction occurs. The
        second component is an Angle object containing the declination
        separation between the given objects at conjunction epoch
    :rtype: tuple
    :raises: ValueError if input values have less than three entries or they
        don't have the same number of entries.
    :raises: TypeError if input values are of wrong type.

    >>> alpha1_1 = Angle(10, 24, 30.125, ra=True)
    >>> delta1_1 = Angle( 6, 26, 32.05)
    >>> alpha1_2 = Angle(10, 25,  0.342, ra=True)
    >>> delta1_2 = Angle( 6, 10, 57.72)
    >>> alpha1_3 = Angle(10, 25, 12.515, ra=True)
    >>> delta1_3 = Angle( 5, 57, 33.08)
    >>> alpha1_4 = Angle(10, 25,  6.235, ra=True)
    >>> delta1_4 = Angle( 5, 46, 27.07)
    >>> alpha1_5 = Angle(10, 24, 41.185, ra=True)
    >>> delta1_5 = Angle( 5, 37, 48.45)
    >>> alpha2_1 = Angle(10, 27, 27.175, ra=True)
    >>> delta2_1 = Angle( 4,  4, 41.83)
    >>> alpha2_2 = Angle(10, 26, 32.410, ra=True)
    >>> delta2_2 = Angle( 3, 55, 54.66)
    >>> alpha2_3 = Angle(10, 25, 29.042, ra=True)
    >>> delta2_3 = Angle( 3, 48,  3.51)
    >>> alpha2_4 = Angle(10, 24, 17.191, ra=True)
    >>> delta2_4 = Angle( 3, 41, 10.25)
    >>> alpha2_5 = Angle(10, 22, 57.024, ra=True)
    >>> delta2_5 = Angle( 3, 35, 16.61)
    >>> alpha1_list = [alpha1_1, alpha1_2, alpha1_3, alpha1_4, alpha1_5]
    >>> delta1_list = [delta1_1, delta1_2, delta1_3, delta1_4, delta1_5]
    >>> alpha2_list = [alpha2_1, alpha2_2, alpha2_3, alpha2_4, alpha2_5]
    >>> delta2_list = [delta2_1, delta2_2, delta2_3, delta2_4, delta2_5]
    >>> pc = planetary_conjunction(alpha1_list, delta1_list,                                    alpha2_list, delta2_list)
    >>> print(round(pc[0], 5))
    0.23797
    >>> print(pc[1].dms_str(n_dec=1))
    2d 8' 21.8''
    """
    ...
def planet_star_conjunction(
    alpha_list: list[Angle] | tuple[Angle, ...], delta_list: list[Angle] | tuple[Angle, ...], alpha_star: Angle, delta_star: Angle
) -> tuple[float, Angle]:
    """
    Given the positions of one planet passing near a star, this function
    computes the time of conjunction in right ascension, and the difference in
    declination of the two bodies at that time.

    .. note:: This function provides as output the 'n' fraction of time when
        the minimum angular separation is achieved. For that, the epoch in the
        middle is assigned the value "n = 0". Therefore, n < 0 is for times
        **before** the middle epoch, and n > 0 is for times **after** the
        middle epoch.

    .. note:: When the entries in the input values for the planet are more than
        three and pair, the last entry is discarted and an odd number of
        entries will be used.

    :param alpha_list: List (or tuple) containing the right ascensions (as
        Angle objects) for the planet (minimum 3 entries)
    :type alpha_list: list, tuple of :py:class:`Angle`
    :param delta_list: List (or tuple) containing the declinations (as Angle
        objects) for the planet (minimum 3 entries)
    :type delta_list: list, tuple of :py:class:`Angle`
    :param alpha_star: Right ascension, as an Angle object, of the star
    :type alpha_star: :py:class:`Angle`
    :param delta_star: Declination, as an Angle object, of the star
    :type delta_star: :py:class:`Angle`

    :returns: A tuple with two components: The first component is a float
        containing the 'n' fraction of time when the conjunction occurs. The
        second component is an Angle object containing the declination
        separation between the given objects at conjunction epoch
    :rtype: tuple
    :raises: ValueError if input values for planet have less than three entries
        or they don't have the same number of entries.
    :raises: TypeError if input values are of wrong type.

    >>> alpha_1 = Angle(15,  3, 51.937, ra=True)
    >>> delta_1 = Angle(-8, 57, 34.51)
    >>> alpha_2 = Angle(15,  9, 57.327, ra=True)
    >>> delta_2 = Angle(-9,  9,  3.88)
    >>> alpha_3 = Angle(15, 15, 37.898, ra=True)
    >>> delta_3 = Angle(-9, 17, 37.94)
    >>> alpha_4 = Angle(15, 20, 50.632, ra=True)
    >>> delta_4 = Angle(-9, 23, 16.25)
    >>> alpha_5 = Angle(15, 25, 32.695, ra=True)
    >>> delta_5 = Angle(-9, 26,  1.01)
    >>> alpha_star = Angle(15, 17, 0.446, ra=True)
    >>> delta_star = Angle(-9, 22, 58.47)
    >>> alpha_list = [alpha_1, alpha_2, alpha_3, alpha_4, alpha_5]
    >>> delta_list = [delta_1, delta_2, delta_3, delta_4, delta_5]
    >>> pc = planet_star_conjunction(alpha_list, delta_list,                                      alpha_star, delta_star)
    >>> print(round(pc[0], 4))
    0.2551
    >>> print(pc[1].dms_str(n_dec=0))
    3' 38.0''
    """
    ...
def planet_stars_in_line(
    alpha_list: list[Angle] | tuple[Angle, ...],
    delta_list: list[Angle] | tuple[Angle, ...],
    alpha_star1: Angle,
    delta_star1: Angle,
    alpha_star2: Angle,
    delta_star2: Angle,
) -> float:
    """
    Given the positions of one planet, this function computes the time when
    it is in a straight line with two other stars.

    .. note:: This function provides as output the 'n' fraction of time when
        the minimum angular separation is achieved. For that, the epoch in the
        middle is assigned the value "n = 0". Therefore, n < 0 is for times
        **before** the middle epoch, and n > 0 is for times **after** the
        middle epoch.

    .. note:: When the entries in the input values for the planet are more than
        three and pair, the last entry is discarted and an odd number of
        entries will be used.

    :param alpha_list: List (or tuple) containing the right ascensions (as
        Angle objects) for the planet (minimum 3 entries)
    :type alpha_list: list, tuple of :py:class:`Angle`
    :param delta_list: List (or tuple) containing the declinations (as Angle
        objects) for the planet (minimum 3 entries)
    :type delta_list: list, tuple of :py:class:`Angle`
    :param alpha_star1: Right ascension, as an Angle object, of star #1
    :type alpha_star1: :py:class:`Angle`
    :param delta_star1: Declination, as an Angle object, of star #1
    :type delta_star1: :py:class:`Angle`
    :param alpha_star2: Right ascension, as an Angle object, of star #2
    :type alpha_star2: :py:class:`Angle`
    :param delta_star2: Declination, as an Angle object, of star #2
    :type delta_star2: :py:class:`Angle`

    :returns: A float containing the 'n' fraction of time when the alignment
        occurs.
    :rtype: float
    :raises: ValueError if input values for planet have less than three entries
        or they don't have the same number of entries.
    :raises: TypeError if input values are of wrong type.

    >>> alpha_1 = Angle( 7, 55, 55.36, ra=True)
    >>> delta_1 = Angle(21, 41,  3.0)
    >>> alpha_2 = Angle( 7, 58, 22.55, ra=True)
    >>> delta_2 = Angle(21, 35, 23.4)
    >>> alpha_3 = Angle( 8,  0, 48.99, ra=True)
    >>> delta_3 = Angle(21, 29, 38.2)
    >>> alpha_4 = Angle( 8,  3, 14.66, ra=True)
    >>> delta_4 = Angle(21, 23, 47.5)
    >>> alpha_5 = Angle( 8,  5, 39.54, ra=True)
    >>> delta_5 = Angle(21, 17, 51.4)
    >>> alpha_star1 = Angle( 7, 34, 16.40, ra=True)
    >>> delta_star1 = Angle(31, 53, 51.2)
    >>> alpha_star2 = Angle( 7, 45,  0.10, ra=True)
    >>> delta_star2 = Angle(28,  2, 12.5)
    >>> alpha_list = [alpha_1, alpha_2, alpha_3, alpha_4, alpha_5]
    >>> delta_list = [delta_1, delta_2, delta_3, delta_4, delta_5]
    >>> n = planet_stars_in_line(alpha_list, delta_list, alpha_star1,                                  delta_star1, alpha_star2, delta_star2)
    >>> print(round(n, 4))
    0.2233
    """
    ...
def straight_line(
    alpha1: Angle, delta1: Angle, alpha2: Angle, delta2: Angle, alpha3: Angle, delta3: Angle
) -> tuple[Angle, Angle]:
    """
    This function computes if three celestial bodies are in a straight line,
    providing the angle with which the bodies differ from a great circle.

    :param alpha1: Right ascension, as an Angle object, of celestial body #1
    :type alpha1: :py:class:`Angle`
    :param delta1: Declination, as an Angle object, of celestial body #1
    :type delta1: :py:class:`Angle`
    :param alpha2: Right ascension, as an Angle object, of celestial body #2
    :type alpha2: :py:class:`Angle`
    :param delta2: Declination, as an Angle object, of celestial body #2
    :type delta2: :py:class:`Angle`
    :param alpha3: Right ascension, as an Angle object, of celestial body #3
    :type alpha3: :py:class:`Angle`
    :param delta3: Declination, as an Angle object, of celestial body #3
    :type delta3: :py:class:`Angle`

    :returns: A tuple with two components. The first element is an angle (as
        Angle object) with which the bodies differ from a great circle. The
        second element is the Angular distance of central point to the straight
        line (also as Angle object).
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.

    >>> alpha1 = Angle( 5, 32,  0.40, ra=True)
    >>> delta1 = Angle(0, -17, 56.9)
    >>> alpha2 = Angle( 5, 36, 12.81, ra=True)
    >>> delta2 = Angle(-1, 12,  7.0)
    >>> alpha3 = Angle( 5, 40, 45.52, ra=True)
    >>> delta3 = Angle(-1, 56, 33.3)
    >>> psi, om = straight_line(alpha1, delta1, alpha2, delta2, alpha3, delta3)
    >>> print(psi.dms_str(n_dec=0))
    7d 31' 1.0''
    >>> print(om.dms_str(n_dec=0))
    -5' 24.0''
    """
    ...
def circle_diameter(alpha1: Angle, delta1: Angle, alpha2: Angle, delta2: Angle, alpha3: Angle, delta3: Angle) -> Angle:
    """
    This function computes the diameter of the smallest circle that contains
    three celestial bodies.

    :param alpha1: Right ascension, as an Angle object, of celestial body #1
    :type alpha1: :py:class:`Angle`
    :param delta1: Declination, as an Angle object, of celestial body #1
    :type delta1: :py:class:`Angle`
    :param alpha2: Right ascension, as an Angle object, of celestial body #2
    :type alpha2: :py:class:`Angle`
    :param delta2: Declination, as an Angle object, of celestial body #2
    :type delta2: :py:class:`Angle`
    :param alpha3: Right ascension, as an Angle object, of celestial body #3
    :type alpha3: :py:class:`Angle`
    :param delta3: Declination, as an Angle object, of celestial body #3
    :type delta3: :py:class:`Angle`

    :returns: The diameter (as an Angle object) of the smallest circle
        containing the three bodies.
    :rtype: :py:class:`Angle`
    :raises: TypeError if input values are of wrong type.

    >>> alpha1 = Angle(12, 41,  8.63, ra=True)
    >>> delta1 = Angle(-5, 37, 54.2)
    >>> alpha2 = Angle(12, 52,  5.21, ra=True)
    >>> delta2 = Angle(-4, 22, 26.2)
    >>> alpha3 = Angle(12, 39, 28.11, ra=True)
    >>> delta3 = Angle(-1, 50,  3.7)
    >>> d = circle_diameter(alpha1, delta1, alpha2, delta2, alpha3, delta3)
    >>> print(d.dms_str(n_dec=0))
    4d 15' 49.0''
    >>> alpha1 = Angle(9,  5, 41.44, ra=True)
    >>> delta1 = Angle(18, 30, 30.0)
    >>> alpha2 = Angle(9,  9, 29.0, ra=True)
    >>> delta2 = Angle(17, 43, 56.7)
    >>> alpha3 = Angle(8, 59, 47.14, ra=True)
    >>> delta3 = Angle(17, 49, 36.8)
    >>> d = circle_diameter(alpha1, delta1, alpha2, delta2, alpha3, delta3)
    >>> print(d.dms_str(n_dec=0))
    2d 18' 38.0''
    """
    ...
def vsop_pos(
    epoch: Epoch, vsop_l: list[list[list[float]]], vsop_b: list[list[list[float]]], vsop_r: list[list[list[float]]]
) -> tuple[Angle, Angle, float]:
    """
    This function computes the position of a celestial body at a given epoch
    when its VSOP87 periodic term tables are provided.

    :param epoch: Epoch to compute the position, given as an :class:`Epoch`
        object
    :type epoch: :py:class:`Epoch`
    :param vsop_l: Table of VSOP87 terms for the heliocentric longitude
    :type vsop_l: list
    :param vsop_b: Table of VSOP87 terms for the heliocentric latitude
    :type vsop_b: list
    :param vsop_r: Table of VSOP87 terms for the radius vector
    :type vsop_r: list

    :returns: A tuple with the heliocentric longitude and latitude (as
        :py:class:`Angle` objects), and the radius vector (as a float,
        in astronomical units), in that order
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.
    """
    ...
def geometric_vsop_pos(
    epoch: Epoch,
    vsop_l: list[list[list[float]]],
    vsop_b: list[list[list[float]]],
    vsop_r: list[list[list[float]]],
    tofk5: bool | None = True,
) -> tuple[Angle, Angle, float]:
    """
    This function computes the geometric position of a celestial body at a
    given epoch when its VSOP87 periodic term tables are provided. The small
    correction to convert to the FK5 system may or not be included.

    :param epoch: Epoch to compute the position, given as an :class:`Epoch`
        object
    :type epoch: :py:class:`Epoch`
    :param vsop_l: Table of VSOP87 terms for the heliocentric longitude
    :type vsop_l: list
    :param vsop_b: Table of VSOP87 terms for the heliocentric latitude
    :type vsop_b: list
    :param vsop_r: Table of VSOP87 terms for the radius vector
    :type vsop_r: list
    :param tofk5: Whether or not the small correction to convert to the FK5
        system will be applied
    :type tofk5: bool

    :returns: A tuple with the geometric heliocentric longitude and latitude
        (as :py:class:`Angle` objects), and the radius vector (as a float,
        in astronomical units), in that order
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.
    """
    ...
def apparent_vsop_pos(
    epoch: Epoch,
    vsop_l: list[list[list[float]]],
    vsop_b: list[list[list[float]]],
    vsop_r: list[list[list[float]]],
    nutation: bool | None = True,
) -> tuple[Angle, Angle, float]:
    """
    This function computes the apparent position of a celestial body at a
    given epoch when its VSOP87 periodic term tables are provided. The small
    correction to convert to the FK5 system is always included.

    :param epoch: Epoch to compute the position, given as an :class:`Epoch`
        object
    :type epoch: :py:class:`Epoch`
    :param vsop_l: Table of VSOP87 terms for the heliocentric longitude
    :type vsop_l: list
    :param vsop_b: Table of VSOP87 terms for the heliocentric latitude
    :type vsop_b: list
    :param vsop_r: Table of VSOP87 terms for the radius vector
    :type vsop_r: list
    :param nutation: Whether the nutation correction will be applied
    :type tofk5: bool

    :returns: A tuple with the geometric heliocentric longitude and latitude
        (as :py:class:`Angle` objects), and the radius vector (as a float,
        in astronomical units), in that order
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.
    """
    ...
def apparent_position(epoch: Epoch, alpha: Angle, delta: Angle, sun_lon: Angle) -> tuple[Angle, Angle]:
    """
    This function computes the apparent position of a star, correcting by
    nutation and aberration effects.

    :param epoch: Epoch to compute the apparent position for
    :type epoch: :py:class:`Epoch`
    :param alpha: Right ascension of the star, as an Angle object
    :type alpha: :py:class:`Angle`
    :param delta: Declination of the star, as an Angle object
    :type delta: :py:class:`Angle`
    :param sun_lon: True (geometric) longitude of the Sun
    :type sun_lon: :py:class:`Angle`

    :returns: A tuple with two Angle objects: Apparent right ascension, and
        aparent declination
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.

    >>> epoch = Epoch(2028, 11, 13.19)
    >>> alpha = Angle(2, 46, 11.331, ra=True)
    >>> delta = Angle(49, 20, 54.54)
    >>> sun_lon = Angle(231.328)
    >>> app_alpha, app_delta = apparent_position(epoch, alpha, delta, sun_lon)
    >>> print(app_alpha.ra_str(n_dec=2))
    2h 46' 14.39''
    >>> print(app_delta.dms_str(n_dec=2))
    49d 21' 7.45''
    """
    ...
def orbital_equinox2equinox(epoch0: Epoch, epoch: Epoch, i0: Angle, arg0: Angle, lon0: Angle) -> tuple[Angle, Angle, Angle]:
    """
    This function reduces the orbital elements of a celestial object from
    one equinox to another.

    :param epoch0: Initial epoch
    :type epoch0: :py:class:`Epoch`
    :param epoch: Final epoch
    :type epoch: :py:class:`Epoch`
    :param i0: Initial inclination, as an Angle object
    :type i0: :py:class:`Angle`
    :param arg0: Initial argument of perihelion, as an Angle object
    :type arg0: :py:class:`Angle`
    :param lon0: Initial longitude of ascending node, as an Angle object
    :type lon0: :py:class:`Angle`

    :returns: A tuple with three Angle objects: Final inclination, argument of
        perihelion and longitude of ascending node, in that order
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.

    >>> epoch0 = Epoch(2358042.5305)
    >>> epoch = Epoch(2433282.4235)
    >>> i0 = Angle(47.122)
    >>> arg0 = Angle(151.4486)
    >>> lon0 = Angle(45.7481)
    >>> i1, arg1, lon1 = orbital_equinox2equinox(epoch0, epoch, i0, arg0, lon0)
    >>> print(round(i1(), 3))
    47.138
    >>> print(round(arg1(), 4))
    151.4782
    >>> print(round(lon1(), 4))
    48.6037
    """
    ...
def kepler_equation(eccentricity: float, mean_anomaly: Angle) -> tuple[Angle, Angle]:
    """
    This function computes the eccentric and true anomalies taking as input
    the mean anomaly and the eccentricity.

    :param eccentricity: Orbit's eccentricity
    :type eccentricity: int, float
    :param mean_anomaly: Mean anomaly, as an Angle object
    :type mean_anomaly: :py:class:`Angle`

    :returns: A tuple with two Angle objects: Eccentric and true anomalies
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.

    >>> eccentricity = 0.1
    >>> mean_anomaly = Angle(5.0)
    >>> e, v = kepler_equation(eccentricity, mean_anomaly)
    >>> print(round(e(), 6))
    5.554589
    >>> print(round(v(), 6))
    6.139762
    >>> eccentricity = 0.99
    >>> mean_anomaly = Angle(2.0)
    >>> e, v = kepler_equation(eccentricity, mean_anomaly)
    >>> print(round(e(), 6))
    32.361007
    >>> print(round(v(), 6))
    152.542134
    >>> eccentricity = 0.99
    >>> mean_anomaly = Angle(5.0)
    >>> e, v = kepler_equation(eccentricity, mean_anomaly)
    >>> print(round(e(), 6))
    45.361023
    >>> print(round(v(), 6))
    160.745616
    >>> eccentricity = 0.99
    >>> mean_anomaly = Angle(1.0)
    >>> e, v = kepler_equation(eccentricity, mean_anomaly)
    >>> print(round(e(), 6))
    24.725822
    >>> print(round(v(), 6))
    144.155952
    >>> e, v = kepler_equation(0.999, Angle(7.0))
    >>> print(round(e(), 7))
    52.2702615
    >>> print(round(v(), 6))
    174.780018
    >>> e, v = kepler_equation(0.99, Angle(0.2, radians=True))
    >>> print(round(e(), 8))
    61.13444578
    >>> print(round(v(), 6))
    166.311977
    """
    ...
def orbital_elements(
    epoch: Epoch, parameters1: list[list[float]], parameters2: list[list[float]]
) -> tuple[Angle, float, float, Angle, Angle, Angle]:
    """
    This function computes the orbital elements for a given epoch, according
    to the parameters beeing passed as arguments.

    :param epoch: Epoch to compute orbital elements, as an Epoch object
    :type epoch: :py:class:`Epoch`
    :param parameters1: First set of parameters
    :type parameters1: list
    :param parameters2: Second set of parameters
    :type parameters2: list

    :returns: A tuple containing the following six orbital elements:
        - Mean longitude of the planet (Angle)
        - Semimajor axis of the orbit (float, astronomical units)
        - eccentricity of the orbit (float)
        - inclination on the plane of the ecliptic (Angle)
        - longitude of the ascending node (Angle)
        - argument of the perihelion (Angle)
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.
    """
    ...
def velocity(r: float, a: float) -> float:
    """
    This function computes the instantaneous velocity of the moving body, in
    kilometers per second, for an unperturbed elliptic orbit.

    :param r: Distance of the body to the Sun, in Astronomical Units
    :type r: float
    :param a: Semimajor axis of the orbit, in Astronomical Units
    :type a: float

    :returns: Velocity of the body, in kilometers per second
    :rtype: float
    :raises: TypeError if input values are of wrong type.

    >>> r = 1.0
    >>> a = 17.9400782
    >>> v = velocity(r, a)
    >>> print(round(v, 2))
    41.53
    """
    ...
def velocity_perihelion(e: float, a: float) -> float:
    """
    This function computes the velocity of the moving body at perihelion, in
    kilometers per second, for an unperturbed elliptic orbit.

    :param e: Orbital eccentricity
    :type e: float
    :param a: Semimajor axis of the orbit, in Astronomical Units
    :type a: float

    :returns: Velocity of the body at perihelion, in kilometers per second
    :rtype: float
    :raises: TypeError if input values are of wrong type.

    >>> a = 17.9400782
    >>> e = 0.96727426
    >>> vp = velocity_perihelion(e, a)
    >>> print(round(vp, 2))
    54.52
    """
    ...
def velocity_aphelion(e: float, a: float) -> float:
    """
    This function computes the velocity of the moving body at aphelion, in
    kilometers per second, for an unperturbed elliptic orbit.

    :param e: Orbital eccentricity
    :type e: float
    :param a: Semimajor axis of the orbit, in Astronomical Units
    :type a: float

    :returns: Velocity of the body at aphelion, in kilometers per second
    :rtype: float
    :raises: TypeError if input values are of wrong type.

    >>> a = 17.9400782
    >>> e = 0.96727426
    >>> va = velocity_aphelion(e, a)
    >>> print(round(va, 2))
    0.91
    """
    ...
def length_orbit(e: float, a: float) -> float:
    """
    This function computes the length of an elliptic orbit given its
    eccentricity and semimajor axis.

    :param e: Orbital eccentricity
    :type e: float
    :param a: Semimajor axis of the orbit, in Astronomical Units
    :type a: float

    :returns: Length of the orbit in Astronomical Units
    :rtype: float
    :raises: TypeError if input values are of wrong type.

    >>> a = 17.9400782
    >>> e = 0.96727426
    >>> length = length_orbit(e, a)
    >>> print(round(length, 2))
    77.06
    """
    ...
def passage_nodes_elliptic(omega: Angle, e: float, a: float, t: Epoch, ascending: bool | None = True) -> tuple[Epoch, float]:
    """
    This function computes the time of passage by the nodes (ascending or
    descending) of a given celestial object with an elliptic orbit.

    :param omega: Argument of the perihelion
    :type omega: :py:class:`Angle`
    :param e: Orbital eccentricity
    :type e: float
    :param a: Semimajor axis of the orbit, in Astronomical Units
    :type a: float
    :param t: Time of perihelion passage
    :type t: :py:class:`Epoch`
    :param ascending: Whether the time of passage by the ascending (True) or
        descending (False) node will be computed
    :type ascending: bool

    :returns: Tuple containing:
        - Time of passage through the node (:py:class:`Epoch`)
        - Radius vector when passing through the node (in AU, float)
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.

    >>> omega = Angle(111.84644)
    >>> e = 0.96727426
    >>> a = 17.9400782
    >>> t = Epoch(1986, 2, 9.45891)
    >>> time, r = passage_nodes_elliptic(omega, e, a, t)
    >>> year, month, day = time.get_date()
    >>> print(year)
    1985
    >>> print(month)
    11
    >>> print(round(day, 2))
    9.16
    >>> print(round(r, 4))
    1.8045
    >>> time, r = passage_nodes_elliptic(omega, e, a, t, ascending=False)
    >>> year, month, day = time.get_date()
    >>> print(year)
    1986
    >>> print(month)
    3
    >>> print(round(day, 2))
    10.37
    >>> print(round(r, 4))
    0.8493
    """
    ...
def passage_nodes_parabolic(omega: Angle, q: float, t: Epoch, ascending: bool | None = True) -> tuple[Epoch, float]:
    """
    This function computes the time of passage by the nodes (ascending or
    descending) of a given celestial object with a parabolic orbit.

    :param omega: Argument of the perihelion
    :type omega: :py:class:`Angle`
    :param q: Perihelion distance, in Astronomical Units
    :type q: float
    :param t: Time of perihelion passage
    :type t: :py:class:`Epoch`
    :param ascending: Whether the time of passage by the ascending (True) or
        descending (False) node will be computed
    :type ascending: bool

    :returns: Tuple containing:
        - Time of passage through the node (:py:class:`Epoch`)
        - Radius vector when passing through the node (in AU, float)
    :rtype: tuple
    :raises: TypeError if input values are of wrong type.

    >>> omega = Angle(154.9103)
    >>> q = 1.324502
    >>> t = Epoch(1989, 8, 20.291)
    >>> time, r = passage_nodes_parabolic(omega, q, t)
    >>> year, month, day = time.get_date()
    >>> print(year)
    1977
    >>> print(month)
    9
    >>> print(round(day, 2))
    17.64
    >>> print(round(r, 4))
    28.0749
    >>> time, r = passage_nodes_parabolic(omega, q, t, ascending=False)
    >>> year, month, day = time.get_date()
    >>> print(year)
    1989
    >>> print(month)
    9
    >>> print(round(day, 3))
    17.636
    >>> print(round(r, 4))
    1.3901
    """
    ...
def phase_angle(sun_dist: float, earth_dist: float, sun_earth_dist: float) -> Angle:
    """
    This function computes the phase angle, i.e., the angle Sun-planet-Earth
    from the corresponding distances.

    :param sun_dist: Planet's distance to the Sun, in Astronomical Units
    :type sun_dist: float
    :param earth_dist: Distance from planet to Earth, in Astronomical Units
    :type earth_dist: float
    :param sun_earth_dist: Distance Sun-Earth, in Astronomical Units
    :type sun_earth_dist: float

    :returns: The phase angle, as an Angle object
    :rtype: :py:class:`Angle`
    :raises: TypeError if input values are of wrong type.

    >>> sun_dist = 0.724604
    >>> earth_dist = 0.910947
    >>> sun_earth_dist = 0.983824
    >>> angle = phase_angle(sun_dist, earth_dist, sun_earth_dist)
    >>> print(round(angle, 2))
    72.96
    """
    ...
def illuminated_fraction(sun_dist: float, earth_dist: float, sun_earth_dist: float) -> float:
    """
    This function computes the illuminated fraction of the disk of a planet,
    as seen from the Earth.

    :param sun_dist: Planet's distance to the Sun, in Astronomical Units
    :type sun_dist: float
    :param earth_dist: Distance from planet to Earth, in Astronomical Units
    :type earth_dist: float
    :param sun_earth_dist: Distance Sun-Earth, in Astronomical Units
    :type sun_earth_dist: float

    :returns: The illuminated fraction of the disc of a planet
    :rtype: float
    :raises: TypeError if input values are of wrong type.

    >>> sun_dist = 0.724604
    >>> earth_dist = 0.910947
    >>> sun_earth_dist = 0.983824
    >>> k = illuminated_fraction(sun_dist, earth_dist, sun_earth_dist)
    >>> print(round(k, 3))
    0.647
    """
    ...
def main() -> None: ...

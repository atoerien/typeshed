import datetime
from typing import Final, Literal, overload
from typing_extensions import Self

from pymeeus.Angle import Angle

DAY2SEC: Final = 86400.0
DAY2MIN: Final = 1440.0
DAY2HOURS: Final = 24.0
LEAP_TABLE: Final[dict[float, int]]

class Epoch:
    """
    Class Epoch deals with the tasks related to time handling.

    The constructor takes either a single JDE value, another Epoch object, or a
    series of values representing year, month, day, hours, minutes, seconds.
    This series of values are by default supposed to be in **Terrestial Time**
    (TT).

    This is not necesarily the truth, though. For instance, the time of a
    current observation is tipically in UTC time (civil time), not in TT, and
    there is some offset between those two time references.

    When a UTC time is provided, the parameter **utc=True** must be given.
    Then, the input is converted to International Atomic Time (TAI) using an
    internal table of leap seconds, and from there, it is converted to (and
    stored as) Terrestrial Time (TT).

    Given that leap seconds are added or subtracted in a rather irregular
    basis, it is not possible to predict them in advance, and the internal leap
    seconds table will become outdated at some point in time. To counter this,
    you have two options:

    - Download an updated version of this Pymeeus package.
    - Use the argument **leap_seconds** in the constructor or :meth:`set`
      method to provide the correct number of leap seconds (w.r.t. TAI) to be
      applied.

    .. note:: Providing the **leap_seconds** argument will automatically set
       the argument **utc** to True.

    For instance, if at some time in the future the TAI-UTC difference is 43
    seconds, you should set **leap_seconds=43** if you don't have an updated
    version of this class.

    In order to know which is the most updated leap second value stored in this
    class, you may use the :meth:`get_last_leap_second()` method.

    .. note:: The current version of UTC was implemented in January 1st, 1972.
       Therefore, for dates before that date the correction is **NOT** carried
       out, even if the **utc** argument is set to True, and it is supposed
       that the input data is already in TT scale.

    .. note:: For conversions between TT and Universal Time (UT), please use
       the method :meth:`tt2ut`.

    .. note:: Internally, time values are stored as a Julian Ephemeris Day
       (JDE), based on the uniform scale of Dynamical Time, or more
       specifically, Terrestial Time (TT) (itself the redefinition of
       Terrestrial Dynamical Time, TDT).

    .. note:: The UTC-TT conversion is composed of three corrections:

       a. TT-TAI, comprising 32.184 s,
       b. TAI-UTC(1972), 10 s, and
       c. UTC(1972)-UTC(target)

       item c. is the corresponding amount of leap seconds to the target Epoch.
       When you do, for instance, **leap_seconds=43**, you modify the c. part.

    .. note:: Given that this class stores the epoch as JDE, if the JDE value
       is in the order of millions of days then, for a computer with 15-digit
       accuracy, the final time resolution is about 10 milliseconds. That is
       considered enough for most applications of this class.
    """
    @overload
    def __init__(self) -> None:
        """
        Epoch constructor.

        This constructor takes either a single JDE value, another Epoch object,
        or a series of values representing year, month, day, hours, minutes,
        seconds. This series of values are by default supposed to be in
        **Terrestial Time** (TT).

        It is also possible that the year, month, etc. arguments be provided in
        a tuple or list. Moreover, it is also possible provide :class:`date` or
        :class:`datetime` objects for initialization.

        The **month** value can be provided as an integer (1 = January, 2 =
        February, etc), or it can be provided with short (Jan, Feb,...) or long
        (January, February,...) names. Also, hours, minutes, seconds can be
        provided separately, or as decimals of the day value.

        When a UTC time is provided, the parameter **utc=True** must be given.
        Then, the input is converted to International Atomic Time (TAI) using
        an internal table of leap seconds, and from there, it is converted to
        (and stored as) Terrestrial Time (TT). If **utc** is not provided, it
        is supposed that the input data is already in TT scale.

        If a value is provided with the **leap_seconds** argument, then that
        value will be used for the UTC->TAI conversion, and the internal leap
        seconds table will be bypassed.

        :param args: Either JDE, Epoch, date, datetime or year, month, day,
           hours, minutes, seconds values, by themselves or inside a tuple or
           list
        :type args: int, float, :py:class:`Epoch`, tuple, list, date,
           datetime
        :param utc: Whether the provided epoch is a civil time (UTC)
        :type utc: bool
        :param leap_seconds: This is the value to be used in the UTC->TAI
            conversion, instead of taking it from internal leap seconds table.
        :type leap_seconds: int, float

        :returns: Epoch object.
        :rtype: :py:class:`Epoch`
        :raises: ValueError if input values are in the wrong range.
        :raises: TypeError if input values are of wrong type.

        >>> e = Epoch(1987, 6, 19.5)
        >>> print(e)
        2446966.0
        """
        ...
    @overload
    def __init__(
        self, year: int, month: int, day: int, /, *time: float, leap_seconds: float = 0, local: bool = False, utc: bool = False
    ) -> None:
        """
        Epoch constructor.

        This constructor takes either a single JDE value, another Epoch object,
        or a series of values representing year, month, day, hours, minutes,
        seconds. This series of values are by default supposed to be in
        **Terrestial Time** (TT).

        It is also possible that the year, month, etc. arguments be provided in
        a tuple or list. Moreover, it is also possible provide :class:`date` or
        :class:`datetime` objects for initialization.

        The **month** value can be provided as an integer (1 = January, 2 =
        February, etc), or it can be provided with short (Jan, Feb,...) or long
        (January, February,...) names. Also, hours, minutes, seconds can be
        provided separately, or as decimals of the day value.

        When a UTC time is provided, the parameter **utc=True** must be given.
        Then, the input is converted to International Atomic Time (TAI) using
        an internal table of leap seconds, and from there, it is converted to
        (and stored as) Terrestrial Time (TT). If **utc** is not provided, it
        is supposed that the input data is already in TT scale.

        If a value is provided with the **leap_seconds** argument, then that
        value will be used for the UTC->TAI conversion, and the internal leap
        seconds table will be bypassed.

        :param args: Either JDE, Epoch, date, datetime or year, month, day,
           hours, minutes, seconds values, by themselves or inside a tuple or
           list
        :type args: int, float, :py:class:`Epoch`, tuple, list, date,
           datetime
        :param utc: Whether the provided epoch is a civil time (UTC)
        :type utc: bool
        :param leap_seconds: This is the value to be used in the UTC->TAI
            conversion, instead of taking it from internal leap seconds table.
        :type leap_seconds: int, float

        :returns: Epoch object.
        :rtype: :py:class:`Epoch`
        :raises: ValueError if input values are in the wrong range.
        :raises: TypeError if input values are of wrong type.

        >>> e = Epoch(1987, 6, 19.5)
        >>> print(e)
        2446966.0
        """
        ...
    @overload
    def __init__(
        self,
        a: float | Epoch | list[float] | tuple[float, ...] | datetime.date,
        /,
        *,
        leap_seconds: float = 0,
        local: bool = False,
        utc: bool = False,
    ) -> None: ...

    def __hash__(self) -> int: ...

    @overload
    def set(self) -> None:
        """
        Method used to set the value of this object.

        This method takes either a single JDE value, or a series of values
        representing year, month, day, hours, minutes, seconds. This series of
        values are by default supposed to be in **Terrestial Time** (TT).

        It is also possible to provide another Epoch object as input for the
        :meth:`set` method, or the year, month, etc arguments can be provided
        in a tuple or list. Moreover, it is also possible provide :class:`date`
        or :class:`datetime` objects for initialization.

        The **month** value can be provided as an integer (1 = January, 2 =
        February, etc), or it can be provided as short (Jan, Feb, ...) or long
        (January, February, ...) names. Also, hours, minutes, seconds can be
        provided separately, or as decimals of the day value.

        When a UTC time is provided, the parameter **utc=True** must be given.
        Then, the input is converted to International Atomic Time (TAI) using
        an internal table of leap seconds, and from there, it is converted to
        (and stored as) Terrestrial Time (TT). If **utc** is not provided, it
        is supposed that the input data is already in TT scale.

        If a value is provided with the **leap_seconds** argument, then that
        value will be used for the UTC->TAI conversion, and the internal leap
        seconds table will be bypassed.

        It is also possible to provide a local time with the parameter
        **local=True**. In such case, the method :meth:`utc2local()` is called
        to compute the LocalTime-UTC difference. This implies that the
        parameter **utc=True** is automatically set.

        .. note:: The UTC to TT correction is only carried out for dates after
           January 1st, 1972.

        .. note:: Please bear in mind that, in order for the method
           :meth:`utc2local()` to work, your operative system must be correctly
           configured, with the right time and corresponding time zone.

        :param args: Either JDE, Epoch, date, datetime or year, month, day,
           hours, minutes, seconds values, by themselves or inside a tuple or
           list.
        :type args: int, float, :py:class:`Epoch`, tuple, list, date,
           datetime
        :param utc: Whether the provided epoch is a civil time (UTC).
        :type utc: bool
        :param leap_seconds: This is the value to be used in the UTC->TAI
            conversion, instead of taking it from internal leap seconds table.
        :type leap_seconds: int, float
        :param local: Whether the provided epoch is a local time.
        :type utc: bool

        :returns: None.
        :rtype: None
        :raises: ValueError if input values are in the wrong range.
        :raises: TypeError if input values are of wrong type.

        >>> e = Epoch()
        >>> e.set(1987, 6, 19.5)
        >>> print(e)
        2446966.0
        >>> e.set(1977, 'Apr', 26.4)
        >>> print(e)
        2443259.9
        >>> e.set(1957, 'October', 4.81)
        >>> print(e)
        2436116.31
        >>> e.set(333, 'Jan', 27, 12)
        >>> print(e)
        1842713.0
        >>> e.set(1900, 'Jan', 1)
        >>> print(e)
        2415020.5
        >>> e.set(-1001, 'august', 17.9)
        >>> print(e)
        1355671.4
        >>> e.set(-4712, 1, 1.5)
        >>> print(e)
        0.0
        >>> e.set((1600, 12, 31))
        >>> print(e)
        2305812.5
        >>> e.set([1988, 'JUN', 19, 12])
        >>> print(e)
        2447332.0
        >>> d = datetime.date(2000, 1, 1)
        >>> e.set(d)
        >>> print(e)
        2451544.5
        >>> e.set(837, 'Apr', 10, 7, 12)
        >>> print(e)
        2026871.8
        >>> d = datetime.datetime(837, 4, 10, 7, 12, 0, 0)
        >>> e.set(d)
        >>> print(e)
        2026871.8
        >>> e = Epoch(JDE2000, utc=True)
        >>> print(round((e - JDE2000) * DAY2SEC, 3))
        64.184
        >>> e = Epoch(2451545.0, utc=True)
        >>> print(round((e - JDE2000) * DAY2SEC, 3))
        64.184
        >>> e = Epoch(JDE2000, local=True)
        >>> print(round((e - JDE2000) * DAY2SEC - Epoch.utc2local(), 3))
        64.184
        >>> e = Epoch(JDE2000, local=True, leap_seconds=35.0)
        >>> print(round((e - JDE2000) * DAY2SEC - Epoch.utc2local(), 3))
        77.184
        """
        ...
    @overload
    def set(
        self, year: int, month: int, day: int, /, *time: float, leap_seconds: float = 0, local: bool = False, utc: bool = False
    ) -> None:
        """
        Method used to set the value of this object.

        This method takes either a single JDE value, or a series of values
        representing year, month, day, hours, minutes, seconds. This series of
        values are by default supposed to be in **Terrestial Time** (TT).

        It is also possible to provide another Epoch object as input for the
        :meth:`set` method, or the year, month, etc arguments can be provided
        in a tuple or list. Moreover, it is also possible provide :class:`date`
        or :class:`datetime` objects for initialization.

        The **month** value can be provided as an integer (1 = January, 2 =
        February, etc), or it can be provided as short (Jan, Feb, ...) or long
        (January, February, ...) names. Also, hours, minutes, seconds can be
        provided separately, or as decimals of the day value.

        When a UTC time is provided, the parameter **utc=True** must be given.
        Then, the input is converted to International Atomic Time (TAI) using
        an internal table of leap seconds, and from there, it is converted to
        (and stored as) Terrestrial Time (TT). If **utc** is not provided, it
        is supposed that the input data is already in TT scale.

        If a value is provided with the **leap_seconds** argument, then that
        value will be used for the UTC->TAI conversion, and the internal leap
        seconds table will be bypassed.

        It is also possible to provide a local time with the parameter
        **local=True**. In such case, the method :meth:`utc2local()` is called
        to compute the LocalTime-UTC difference. This implies that the
        parameter **utc=True** is automatically set.

        .. note:: The UTC to TT correction is only carried out for dates after
           January 1st, 1972.

        .. note:: Please bear in mind that, in order for the method
           :meth:`utc2local()` to work, your operative system must be correctly
           configured, with the right time and corresponding time zone.

        :param args: Either JDE, Epoch, date, datetime or year, month, day,
           hours, minutes, seconds values, by themselves or inside a tuple or
           list.
        :type args: int, float, :py:class:`Epoch`, tuple, list, date,
           datetime
        :param utc: Whether the provided epoch is a civil time (UTC).
        :type utc: bool
        :param leap_seconds: This is the value to be used in the UTC->TAI
            conversion, instead of taking it from internal leap seconds table.
        :type leap_seconds: int, float
        :param local: Whether the provided epoch is a local time.
        :type utc: bool

        :returns: None.
        :rtype: None
        :raises: ValueError if input values are in the wrong range.
        :raises: TypeError if input values are of wrong type.

        >>> e = Epoch()
        >>> e.set(1987, 6, 19.5)
        >>> print(e)
        2446966.0
        >>> e.set(1977, 'Apr', 26.4)
        >>> print(e)
        2443259.9
        >>> e.set(1957, 'October', 4.81)
        >>> print(e)
        2436116.31
        >>> e.set(333, 'Jan', 27, 12)
        >>> print(e)
        1842713.0
        >>> e.set(1900, 'Jan', 1)
        >>> print(e)
        2415020.5
        >>> e.set(-1001, 'august', 17.9)
        >>> print(e)
        1355671.4
        >>> e.set(-4712, 1, 1.5)
        >>> print(e)
        0.0
        >>> e.set((1600, 12, 31))
        >>> print(e)
        2305812.5
        >>> e.set([1988, 'JUN', 19, 12])
        >>> print(e)
        2447332.0
        >>> d = datetime.date(2000, 1, 1)
        >>> e.set(d)
        >>> print(e)
        2451544.5
        >>> e.set(837, 'Apr', 10, 7, 12)
        >>> print(e)
        2026871.8
        >>> d = datetime.datetime(837, 4, 10, 7, 12, 0, 0)
        >>> e.set(d)
        >>> print(e)
        2026871.8
        >>> e = Epoch(JDE2000, utc=True)
        >>> print(round((e - JDE2000) * DAY2SEC, 3))
        64.184
        >>> e = Epoch(2451545.0, utc=True)
        >>> print(round((e - JDE2000) * DAY2SEC, 3))
        64.184
        >>> e = Epoch(JDE2000, local=True)
        >>> print(round((e - JDE2000) * DAY2SEC - Epoch.utc2local(), 3))
        64.184
        >>> e = Epoch(JDE2000, local=True, leap_seconds=35.0)
        >>> print(round((e - JDE2000) * DAY2SEC - Epoch.utc2local(), 3))
        77.184
        """
        ...
    @overload
    def set(
        self,
        a: float | Epoch | list[float] | tuple[float, ...] | datetime.date,
        /,
        *,
        leap_seconds: float = 0,
        local: bool = False,
        utc: bool = False,
    ) -> None: ...

    @overload
    @overload
    @staticmethod
    def check_input_date(
        a: Epoch | list[float] | tuple[float, ...] | datetime.date,
        /,
        *,
        leap_seconds: float = 0,
        local: bool = False,
        utc: bool = False,
    ) -> Epoch:
        """
        Method to check that the input is a proper date.

        This method returns an Epoch object, and the **leap_seconds** argument
        then controls the way the UTC->TT conversion is handled for that new
        object. If **leap_seconds** argument is set to a value different than
        zero, then that value will be used for the UTC->TAI conversion, and the
        internal leap seconds table will be bypassed. On the other hand, if it
        is set to zero, then the UTC to TT correction is disabled, and it is
        supposed that the input data is already in TT scale.

        :param args: Either Epoch, date, datetime or year, month, day values,
            by themselves or inside a tuple or list
        :type args: int, float, :py:class:`Epoch`, datetime, date, tuple,
            list
        :param leap_seconds: If different from zero, this is the value to be
           used in the UTC->TAI conversion. If equals to zero, conversion is
           disabled. If not given, UTC to TT conversion is carried out
           (default).
        :type leap_seconds: int, float

        :returns: Epoch object corresponding to the input date
        :rtype: :py:class:`Epoch`
        :raises: ValueError if input values are in the wrong range.
        :raises: TypeError if input values are of wrong type.
        """
        ...
    @overload
    @staticmethod
    def check_input_date(
        year: int, month: int, day: int, /, *, leap_seconds: float = 0, local: bool = False, utc: bool = False
    ) -> Epoch: ...

    @staticmethod
    def is_julian(year: int, month: int, day: int) -> bool: ...
    def julian(self) -> bool: ...

    @overload
    @staticmethod
    def get_month(month: float | str, as_string: Literal[True]) -> str:
        """
        Method to get the month as a integer in the [1, 12] range, or as a
        full name.

        :param month: Month, in numeric, short name or long name format
        :type month: int, float, str
        :param as_string: Whether the output will be numeric, or a long name.
        :type as_string: bool

        :returns: Month as integer in the [1, 12] range, or as a long name.
        :rtype: int, str
        :raises: ValueError if input month value is invalid.

        >>> Epoch.get_month(4.0)
        4
        >>> Epoch.get_month('Oct')
        10
        >>> Epoch.get_month('FEB')
        2
        >>> Epoch.get_month('August')
        8
        >>> Epoch.get_month('august')
        8
        >>> Epoch.get_month('NOVEMBER')
        11
        >>> Epoch.get_month(9.0, as_string=True)
        'September'
        >>> Epoch.get_month('Feb', as_string=True)
        'February'
        >>> Epoch.get_month('March', as_string=True)
        'March'
        """
        ...
    @overload
    @staticmethod
    def get_month(month: float | str, as_string: Literal[False] | None = False) -> int: ...

    @staticmethod
    def is_leap(year: float) -> bool:
        """
        Method to check if a given year is a leap year.

        :param year: Year to be checked.
        :type year: int, float

        :returns: Whether or not year is a leap year.
        :rtype: bool
        :raises: ValueError if input year value is invalid.

        >>> Epoch.is_leap(2003)
        False
        >>> Epoch.is_leap(2012)
        True
        >>> Epoch.is_leap(1900)
        False
        >>> Epoch.is_leap(-1000)
        True
        >>> Epoch.is_leap(1000)
        True
        """
        ...
    def leap(self) -> bool:
        """
        This method checks if the current Epoch object holds a leap year.

        :returns: Whether or the year in this Epoch object is a leap year.
        :rtype: bool

        >>> e = Epoch(2003, 1, 1)
        >>> e.leap()
        False
        >>> e = Epoch(2012, 1, 1)
        >>> e.leap()
        True
        >>> e = Epoch(1900, 1, 1)
        >>> e.leap()
        False
        >>> e = Epoch(-1000, 1, 1)
        >>> e.leap()
        True
        >>> e = Epoch(1000, 1, 1)
        >>> e.leap()
        True
        """
        ...
    @staticmethod
    def get_doy(yyyy: int, mm: int, dd: int) -> float:
        """
        This method returns the Day Of Year (DOY) for the given date.

        :param yyyy: Year, in four digits format
        :type yyyy: int, float
        :param mm: Month, in numeric format (1 = January, 2 = February, etc)
        :type mm: int, float
        :param dd: Day, in numeric format
        :type dd: int, float

        :returns: Day Of Year (DOY).
        :rtype: float
        :raises: ValueError if input values correspond to a wrong date.

        >>> Epoch.get_doy(1999, 1, 29)
        29.0
        >>> Epoch.get_doy(1978, 11, 14)
        318.0
        >>> Epoch.get_doy(2017, 12, 31.7)
        365.7
        >>> Epoch.get_doy(2012, 3, 3.1)
        63.1
        >>> Epoch.get_doy(-400, 2, 29.9)
        60.9
        """
        ...
    def doy(self) -> float:
        """
        This method returns the Day Of Year (DOY) for the current Epoch
        object.

        :returns: Day Of Year (DOY).
        :rtype: float

        >>> e = Epoch(1999, 1, 29)
        >>> round(e.doy(), 1)
        29.0
        >>> e = Epoch(2017, 12, 31.7)
        >>> round(e.doy(), 1)
        365.7
        >>> e = Epoch(2012, 3, 3.1)
        >>> round(e.doy(), 1)
        63.1
        >>> e = Epoch(-400, 2, 29.9)
        >>> round(e.doy(), 1)
        60.9
        """
        ...
    @staticmethod
    def doy2date(year: int, doy: float) -> tuple[int, int, float]:
        """
        This method takes a year and a Day Of Year values, and returns the
        corresponding date.

        :param year: Year, in four digits format
        :type year: int, float
        :param doy: Day of Year number
        :type doy: int, float

        :returns: Year, month, day.
        :rtype: tuple
        :raises: ValueError if either input year or doy values are invalid.

        >>> t = Epoch.doy2date(1999, 29)
        >>> print("{}/{}/{}".format(t[0], t[1], round(t[2], 1)))
        1999/1/29.0
        >>> t = Epoch.doy2date(2017, 365.7)
        >>> print("{}/{}/{}".format(t[0], t[1], round(t[2], 1)))
        2017/12/31.7
        >>> t = Epoch.doy2date(2012, 63.1)
        >>> print("{}/{}/{}".format(t[0], t[1], round(t[2], 1)))
        2012/3/3.1
        >>> t = Epoch.doy2date(-1004, 60)
        >>> print("{}/{}/{}".format(t[0], t[1], round(t[2], 1)))
        -1004/2/29.0
        >>> t = Epoch.doy2date(0, 60)
        >>> print("{}/{}/{}".format(t[0], t[1], round(t[2], 1)))
        0/2/29.0
        >>> t = Epoch.doy2date(1, 60)
        >>> print("{}/{}/{}".format(t[0], t[1], round(t[2], 1)))
        1/3/1.0
        >>> t = Epoch.doy2date(-1, 60)
        >>> print("{}/{}/{}".format(t[0], t[1], round(t[2], 1)))
        -1/3/1.0
        >>> t = Epoch.doy2date(-2, 60)
        >>> print("{}/{}/{}".format(t[0], t[1], round(t[2], 1)))
        -2/3/1.0
        >>> t = Epoch.doy2date(-3, 60)
        >>> print("{}/{}/{}".format(t[0], t[1], round(t[2], 1)))
        -3/3/1.0
        >>> t = Epoch.doy2date(-4, 60)
        >>> print("{}/{}/{}".format(t[0], t[1], round(t[2], 1)))
        -4/2/29.0
        >>> t = Epoch.doy2date(-5, 60)
        >>> print("{}/{}/{}".format(t[0], t[1], round(t[2], 1)))
        -5/3/1.0
        """
        ...
    @staticmethod
    def leap_seconds(year: int, month: int) -> int:
        """
        Returns the leap seconds accumulated for the given year and month.

        :param year: Year
        :type year: int
        :param month: Month, in numeric format ([1:12] range)
        :type month: int

        :returns: Leap seconds accumulated for given year and month.
        :rtype: int

        >>> Epoch.leap_seconds(1972, 4)
        0
        >>> Epoch.leap_seconds(1972, 6)
        0
        >>> Epoch.leap_seconds(1972, 7)
        1
        >>> Epoch.leap_seconds(1983, 6)
        11
        >>> Epoch.leap_seconds(1983, 7)
        12
        >>> Epoch.leap_seconds(1985, 8)
        13
        >>> Epoch.leap_seconds(2016, 11)
        26
        >>> Epoch.leap_seconds(2017, 1)
        27
        >>> Epoch.leap_seconds(2018, 7)
        27
        """
        ...
    @staticmethod
    def get_last_leap_second() -> tuple[int, int, float, int]:
        """
        Method to get the date and value of the last leap second added to
        the table

        :returns: Tuple with year, month, day, leap second value.
        :rtype: tuple
        """
        ...
    @staticmethod
    def utc2local() -> float:
        """
        Method to return the difference between UTC and local time.

        This method provides you the seconds that you have to add or subtract
        to UTC time to convert to your local time. The correct way to apply
        this method is according to the expression:

        utc2local() = LocalTime - UTC

        Therefore, if for example you are located in a place whose
        corresponding time zone is UTC+2, then this method will yield 7200
        (seconds in two hours) and you must then apply this expression:

        LocalTime = UTC + utclocal() = UTC + 7200

        .. note:: Please bear in mind that, in order for this method to work,
           your operative system must be correctly configured, with the right
           time and corresponding time zone.

        .. note:: Remember that class :py:class:`Epoch` internally stores time
           as Terrestrial Time (TT), not UTC. In order to get the UTC time you
           must use a method like :meth:`get_date()` or :meth:`get_full_date()`
           and pass the parameter **utc=True**.

        :returns: Difference in seconds between local and UTC time, in that
            order.
        :rtype: float
        """
        ...
    @staticmethod
    def easter(year: float) -> tuple[int, int]:
        """
        Method to return the Easter day for given year.

        .. note:: This method is valid for both Gregorian and Julian years.

        :param year: Year
        :type year: int

        :returns: Easter month and day, as a tuple
        :rtype: tuple
        :raises: TypeError if input values are of wrong type.

        >>> Epoch.easter(1991)
        (3, 31)
        >>> Epoch.easter(1818)
        (3, 22)
        >>> Epoch.easter(1943)
        (4, 25)
        >>> Epoch.easter(2000)
        (4, 23)
        >>> Epoch.easter(1954)
        (4, 18)
        >>> Epoch.easter(179)
        (4, 12)
        >>> Epoch.easter(1243)
        (4, 12)
        """
        ...
    @staticmethod
    def jewish_pesach(year: float) -> tuple[int, int]:
        """
        Method to return the Jewish Easter (Pesach) day for given year.

        .. note:: This method is valid for both Gregorian and Julian years.

        :param year: Year
        :type year: int

        :returns: Jewish Easter (Pesach) month and day, as a tuple
        :rtype: tuple
        :raises: TypeError if input values are of wrong type.

        >>> Epoch.jewish_pesach(1990)
        (4, 10)
        """
        ...
    @staticmethod
    def moslem2gregorian(year: float, month: float, day: float) -> tuple[int, int, int]:
        """
        Method to convert a date in the Moslen calendar to the Gregorian
        (or Julian) calendar.

        .. note:: This method is valid for both Gregorian and Julian years.

        :param year: Year
        :type year: int
        :param month: Month
        :type month: int
        :param day: Day
        :type day: int

        :returns: Date in Gregorian (Julian) calendar: year, month and day, as
           a tuple
        :rtype: tuple
        :raises: TypeError if input values are of wrong type.

        >>> Epoch.moslem2gregorian(1421, 1, 1)
        (2000, 4, 6)
        """
        ...
    @staticmethod
    def gregorian2moslem(year: float, month: float, day: float) -> tuple[int, int, int]:
        """
        Method to convert a date in the Gregorian (or Julian) calendar to
        the Moslen calendar.

        :param year: Year
        :type year: int
        :param month: Month
        :type month: int
        :param day: Day
        :type day: int

        :returns: Date in Moslem calendar: year, month and day, as a tuple
        :rtype: tuple
        :raises: TypeError if input values are of wrong type.

        >>> Epoch.gregorian2moslem(1991, 8, 13)
        (1412, 2, 2)
        """
        ...
    def get_date(self, *, utc: bool = False, leap_seconds: float = 0.0, local: bool = ...) -> tuple[int, int, float]:
        """
        This method converts the internal JDE value back to a date.

        Use **utc=True** to enable the TT to UTC conversion mechanism, or
        provide a non zero value to **leap_seconds** to apply a specific leap
        seconds value.

        It is also possible to retrieve a local time with the parameter
        **local=True**. In such case, the method :meth:`utc2local()` is called
        to compute the LocalTime-UTC difference. This implies that the
        parameter **utc=True** is automatically set.

        .. note:: Please bear in mind that, in order for the method
           :meth:`utc2local()` to work, your operative system must be correctly
           configured, with the right time and corresponding time zone.

        :param utc: Whether the TT to UTC conversion mechanism will be enabled
        :type utc: bool
        :param leap_seconds: Optional value for leap seconds.
        :type leap_seconds: int, float
        :param local: Whether the retrieved epoch is converted to local time.
        :type utc: bool

        :returns: Year, month, day in a tuple
        :rtype: tuple

        >>> e = Epoch(2436116.31)
        >>> y, m, d = e.get_date()
        >>> print("{}/{}/{}".format(y, m, round(d, 2)))
        1957/10/4.81
        >>> e = Epoch(1988, 1, 27)
        >>> y, m, d = e.get_date()
        >>> print("{}/{}/{}".format(y, m, round(d, 2)))
        1988/1/27.0
        >>> e = Epoch(1842713.0)
        >>> y, m, d = e.get_date()
        >>> print("{}/{}/{}".format(y, m, round(d, 2)))
        333/1/27.5
        >>> e = Epoch(1507900.13)
        >>> y, m, d = e.get_date()
        >>> print("{}/{}/{}".format(y, m, round(d, 2)))
        -584/5/28.63
        """
        ...
    def get_full_date(
        self, *, utc: bool = False, leap_seconds: float = 0.0, local: bool = ...
    ) -> tuple[int, int, int, int, int, float]:
        """
        This method converts the internal JDE value back to a full date.

        Use **utc=True** to enable the TT to UTC conversion mechanism, or
        provide a non zero value to **leap_seconds** to apply a specific leap
        seconds value.

        It is also possible to retrieve a local time with the parameter
        **local=True**. In such case, the method :meth:`utc2local()` is called
        to compute the LocalTime-UTC difference. This implies that the
        parameter **utc=True** is automatically set.

        .. note:: Please bear in mind that, in order for the method
           :meth:`utc2local()` to work, your operative system must be correctly
           configured, with the right time and corresponding time zone.

        :param utc: Whether the TT to UTC conversion mechanism will be enabled
        :type utc: bool
        :param leap_seconds: Optional value for leap seconds.
        :type leap_seconds: int, float
        :param local: Whether the retrieved epoch is converted to local time.
        :type utc: bool

        :returns: Year, month, day, hours, minutes, seconds in a tuple
        :rtype: tuple

        >>> e = Epoch(2436116.31)
        >>> y, m, d, h, mi, s = e.get_full_date()
        >>> print("{}/{}/{} {}:{}:{}".format(y, m, d, h, mi, round(s, 1)))
        1957/10/4 19:26:24.0
        >>> e = Epoch(1988, 1, 27)
        >>> y, m, d, h, mi, s = e.get_full_date()
        >>> print("{}/{}/{} {}:{}:{}".format(y, m, d, h, mi, round(s, 1)))
        1988/1/27 0:0:0.0
        >>> e = Epoch(1842713.0)
        >>> y, m, d, h, mi, s = e.get_full_date()
        >>> print("{}/{}/{} {}:{}:{}".format(y, m, d, h, mi, round(s, 1)))
        333/1/27 12:0:0.0
        >>> e = Epoch(1507900.13)
        >>> y, m, d, h, mi, s = e.get_full_date()
        >>> print("{}/{}/{} {}:{}:{}".format(y, m, d, h, mi, round(s, 1)))
        -584/5/28 15:7:12.0
        """
        ...
    @staticmethod
    def tt2ut(year: int, month: int) -> float: ...

    @overload
    def dow(self, as_string: Literal[True]) -> str:
        """
        Method to return the day of week corresponding to this Epoch.

        By default, this method returns an integer value: 0 for Sunday, 1 for
        Monday, etc. However, when **as_string=True** is passed, the names of
        the days are returned.

        :param as_string: Whether result will be given as a integer or as a
           string. False by default.
        :type as_string: bool

        :returns: Day of the week, as a integer or as a string.
        :rtype: int, str

        >>> e = Epoch(1954, 'June', 30)
        >>> e.dow()
        3
        >>> e = Epoch(2018, 'Feb', 14.9)
        >>> e.dow(as_string=True)
        'Wednesday'
        >>> e = Epoch(2018, 'Feb', 15)
        >>> e.dow(as_string=True)
        'Thursday'
        >>> e = Epoch(2018, 'Feb', 15.99)
        >>> e.dow(as_string=True)
        'Thursday'
        >>> e.set(2018, 'Jul', 15.4)
        >>> e.dow(as_string=True)
        'Sunday'
        >>> e.set(2018, 'Jul', 15.9)
        >>> e.dow(as_string=True)
        'Sunday'
        """
        ...
    @overload
    def dow(self, as_string: Literal[False] | None = False) -> int: ...

    def mean_sidereal_time(self) -> float: ...
    def apparent_sidereal_time(self, true_obliquity: float | Angle, nutation_longitude: float | Angle) -> float: ...
    def mjd(self) -> float: ...
    def jde(self) -> float: ...
    def year(self) -> float: ...
    def rise_set(self, latitude: Angle, longitude: Angle, altitude: float = 0.0) -> tuple[Epoch, Epoch]: ...
    def __call__(self) -> float: ...
    def __add__(self, b: float) -> Epoch: ...

    @overload
    def __sub__(self, b: float) -> Epoch:
        """
        This method defines the subtraction between Epochs or between an
        Epoch and a given number of days.

        :param b: Value to be subtracted, either an Epoch or days.
        :type b: py:class:`Epoch`, int, float

        :returns: A new Epoch object if parameter 'b' is in days, or the
           difference between provided Epochs, in days.
        :rtype: :py:class:`Epoch`, float
        :raises: TypeError if operand is of wrong type.

        >>> a = Epoch(1986, 2, 9.0)
        >>> print(round(a(), 2))
        2446470.5
        >>> b = Epoch(1910, 4, 20.0)
        >>> print(round(b(), 2))
        2418781.5
        >>> c = a - b
        >>> print(round(c, 2))
        27689.0
        >>> a = Epoch(2003, 12, 31.0)
        >>> b = a - 365.5
        >>> y, m, d = b.get_date()
        >>> print("{}/{}/{}".format(y, m, round(d, 2)))
        2002/12/30.5
        """
        ...
    @overload
    def __sub__(self, b: Epoch) -> float: ...

    def __iadd__(self, b: float) -> Self: ...
    def __isub__(self, b: float) -> Self: ...  # type: ignore[misc] # __sub__ and __isub__ are incompatible
    def __radd__(self, b: float) -> Epoch: ...
    def __int__(self) -> int: ...
    def __float__(self) -> float: ...
    def __eq__(self, b: float | Epoch) -> bool: ...  # type: ignore[override]
    def __ne__(self, b: float | Epoch) -> bool: ...  # type: ignore[override]
    def __lt__(self, b: float | Epoch) -> bool: ...
    def __ge__(self, b: float | Epoch) -> bool: ...
    def __gt__(self, b: float | Epoch) -> bool: ...
    def __le__(self, b: float | Epoch) -> bool: ...

JDE2000: Epoch

def main() -> None: ...

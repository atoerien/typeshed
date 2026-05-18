"""
The dates module implements classes for representing and
manipulating several date types.

Contents
--------
* :class:`Rounding`
* :class:`BaseDate`
* :class:`CalendarDateMixin`
* :class:`JulianDay`
* :class:`GregorianDate`
* :class:`HebrewDate`

Note
----
All instances of the classes in this module should be treated as read
only. No attributes should be changed once they're created.
"""

import abc
import datetime
from collections.abc import Generator
from enum import Enum
from typing import TypedDict, overload, type_check_only
from typing_extensions import Self

@type_check_only
class _DateDict(TypedDict):
    year: int
    month: int
    day: int

class Rounding(Enum):
    """
    Enumerator to provide options for rounding Hebrew dates.

    This provides constants to use as arguments for functions. It
    should not be instantiated.

    Attributes
    ----------
    PREVIOUS_DAY
        If the day is the 30th and the month only has 29 days, round to
        the 29th of the month.
    NEXT_DAY
        If the day is the 30th and the month only has 29 days, round to
        the 1st of the next month.
    EXCEPTION
        If the day is the 30th and the month only has 29 days, raise a
        ValueError.
    """
    PREVIOUS_DAY = 1
    NEXT_DAY = 2
    EXCEPTION = 3

class BaseDate(abc.ABC, metaclass=abc.ABCMeta):
    """
    BaseDate is a base class for all date types.

    It provides the following arithmetic and comparison operators
    common to all child date types.

    ===================  =================================================
    Operation            Result
    ===================  =================================================
    d2 = date1 + int     New date ``int`` days after date1
    d2 = date1 - int     New date ``int`` days before date1
    int = date1 - date2  Positive integer equal to the duration from date1
                         to date2
    date1 > date2        True if date1 occurs later than date2
    date1 < date2        True if date1 occurs earlier than date2
    date1 == date2       True if date1 occurs on the same day as date2
    date1 != date2       True if ``date1 == date2`` is False
    ===================  =================================================

    Any subclass of ``BaseDate`` can be compared to and diffed with any other
    subclass date.
    """
    @property
    @abc.abstractmethod
    def jd(self) -> float:
        """
        Return julian day number.

        Returns
        -------
        float
            The Julian day number at midnight (as ``n.5``).
        """
        ...
    @abc.abstractmethod
    def to_heb(self) -> HebrewDate:
        """
        Return Hebrew Date.

        Returns
        -------
        HebrewDate
        """
        ...
    def __hash__(self) -> int: ...
    def __add__(self, other: float) -> BaseDate: ...

    @overload
    def __sub__(self, other: float) -> BaseDate: ...
    @overload
    def __sub__(self, other: BaseDate) -> int: ...

    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...
    def __le__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def weekday(self) -> int:
        """
        Return day of week as an integer.

        Returns
        -------
        int
            An integer representing the day of the week with Sunday as 1
            through Saturday as 7.
        """
        ...
    def isoweekday(self) -> int:
        """
        Return the day of the week corresponding to the iso standard.

        Returns
        -------
        int
            An integer representing the day of the week where Monday
            is 1 and and Sunday is 7.
        """
        ...
    def shabbos(self) -> Self:
        """
        Return the Shabbos on or following the date.

        Returns
        -------
        JulianDay, GregorianDate, or HebrewDate
            `self` if the date is Shabbos or else the following Shabbos as
            the same date type as called from.

        Examples
        --------
        >>> heb_date = HebrewDate(5781, 3, 29)
        >>> greg_date = heb_date.to_greg()
        >>> heb_date.shabbos()
        HebrewDate(5781, 4, 2)
        >>> greg_date.shabbos()
        GregorianDate(2021, 6, 12)
        """
        ...
    def fast_day(self, hebrew: bool = False) -> str | None:
        """
        Return name of fast day of date.

        Parameters
        ----------
        hebrew : bool, optional
            ``True`` if you want the fast day name in Hebrew letters. Default
            is ``False``, which returns the name transliterated into English.

        Returns
        -------
        str or None
            The name of the fast day or ``None`` if the date is not
            a fast day.
        """
        ...
    def festival(
        self, israel: bool = False, hebrew: bool = False, include_working_days: bool = True, prefix_day: bool = False
    ) -> str | None:
        """
        Return name of Jewish festival of date.

        This method will return all major and minor religous
        Jewish holidays not including fast days.

        Parameters
        ----------
        israel : bool, optional
            ``True`` if you want the holidays according to the Israel
            schedule. Defaults to ``False``.
        hebrew : bool, optional
            ``True`` if you want the festival name in Hebrew letters. Default
            is ``False``, which returns the name transliterated into English.
        include_working_days : bool, optional
            ``True`` to include festival days on which melacha (work) is
            allowed; ie. Pesach Sheni, Chol Hamoed, etc.
            Default is ``True``.
        prefix_day : bool, optional
            ``True`` to prefix multi day festivals with the day of the
            festival. Default is ``False``.

        Returns
        -------
        str or None
            The name of the festival or ``None`` if the given date is not
            a Jewish festival.

        Examples
        --------
        >>> pesach = HebrewDate(2023, 1, 15)
        >>> pesach.festival(prefix_day=True)
        '1 Pesach'
        >>> pesach.festival(hebrew=True, prefix_day=True)
        'א׳ פסח'
        >>> shavuos = HebrewDate(5783, 3, 6)
        >>> shavuos.festival(israel=True, prefix_day=True)
        'Shavuos'
        """
        ...
    def holiday(self, israel: bool = False, hebrew: bool = False, prefix_day: bool = False) -> str | None:
        """
        Return name of Jewish holiday of the date.

        The holidays include the major and minor religious Jewish
        holidays including fast days.

        Parameters
        ----------
        israel : bool, optional
            ``True`` if you want the holidays according to the Israel
            schedule. Defaults to ``False``.
        hebrew : bool, optional
            ``True`` if you want the holiday name in Hebrew letters. Default is
            ``False``, which returns the name transliterated into English.
        prefix_day : bool, optional
            ``True`` to prefix multi day holidays with the day of the
            holiday. Default is ``False``.

        Returns
        -------
        str or None
            The name of the holiday or ``None`` if the given date is not
            a Jewish holiday.

        Examples
        --------
        >>> pesach = HebrewDate(2023, 1, 15)
        >>> pesach.holiday(prefix_day=True)
        '1 Pesach'
        >>> pesach.holiday(hebrew=True, prefix_day=True)
        'א׳ פסח'
        >>> taanis_esther = HebrewDate(5783, 12, 13)
        >>> taanis_esther.holiday(prefix_day=True)
        'Taanis Esther'
        """
        ...

class CalendarDateMixin:
    """
    CalendarDateMixin is a mixin for Hebrew and Gregorian dates.

    Parameters
    ----------
    year : int
    month : int
    day : int

    Attributes
    ----------
    year : int
    month : int
    day : int
    jd : float
        The equivalent Julian day at midnight.
    """
    year: int
    month: int
    day: int
    def __init__(self, year: int, month: int, day: int, jd: float | None = None) -> None: ...
    def __iter__(self) -> Generator[int]: ...
    def tuple(self) -> tuple[int, int, int]:
        """
        Return date as tuple.

        Returns
        -------
        tuple of ints
            A tuple of ints in the form ``(year, month, day)``.
        """
        ...
    def dict(self) -> _DateDict:
        """
        Return the date as a dictionary.

        Returns
        -------
        dict
            A dictionary in the form
            ``{'year': int, 'month': int, 'day': int}``.
        """
        ...
    def replace(self, year: int | None = None, month: int | None = None, day: int | None = None) -> Self:
        """
        Return new date with new values for the specified field.

        Parameters
        ----------
        year : int, optional
        month: int, optional
        day : int, optional

        Returns
        -------
        CalendarDateMixin
            Any date that inherits from CalendarDateMixin
            (``GregorianDate``, ````HebrewDate``).

        Raises
        ValueError
            Raises a ``ValueError`` if the new date does not exist.
        """
        ...

class JulianDay(BaseDate):
    """
    A JulianDay object represents a Julian Day at midnight.

    Parameters
    ----------
    day : float or int
        The julian day. Note that Julian days start at noon so day
        number 10 is represented as 9.5 which is day 10 at midnight.

    Attributes
    ----------
    day : float
        The Julian Day Number at midnight (as *n*.5)
    """
    day: float
    def __init__(self, day: float) -> None: ...
    @property
    def jd(self) -> float:
        """
        Return julian day.

        Returns
        -------
        float
        """
        ...
    @staticmethod
    def from_pydate(pydate: datetime.date) -> JulianDay:
        """
        Return a `JulianDay` from a python date object.

        Parameters
        ----------
        pydate : datetime.date
            A python standard library ``datetime.date`` instance

        Returns
        -------
        JulianDay
        """
        ...
    @staticmethod
    def today() -> JulianDay:
        """
        Return instance of current Julian day from timestamp.

        Extends the built-in ``datetime.date.today()``.

        Returns
        -------
        JulianDay
            A JulianDay instance representing the current Julian day from
            the timestamp.

        Warning
        -------
        Julian Days change at noon, but pyluach treats them as if they
        change at midnight, so at midnight this method will return
        ``JulianDay(n.5)`` until the following midnight when it will
        return ``JulianDay(n.5 + 1)``.
        """
        ...
    def to_greg(self) -> GregorianDate:
        """
        Convert JulianDay to a Gregorian Date.

        Returns
        -------
        GregorianDate
            The equivalent Gregorian date instance.

        Notes
        -----
        This method uses the Fliegel-Van Flandern algorithm.
        """
        ...
    def to_heb(self) -> HebrewDate:
        """
        Convert to a Hebrew date.

        Returns
        -------
        HebrewDate
            The equivalent Hebrew date instance.
        """
        ...
    def to_pydate(self) -> datetime.date:
        """
        Convert to a datetime.date object.

        Returns
        -------
        datetime.date
            A standard library ``datetime.date`` instance.
        """
        ...

class GregorianDate(BaseDate, CalendarDateMixin):
    """
    A GregorianDate object represents a Gregorian date (year, month, day).

    This is an idealized date with the current Gregorian calendar
    infinitely extended in both directions.

    Parameters
    ----------
    year : int
    month : int
    day : int
    jd : float, optional
      This parameter should not be assigned manually.

    Attributes
    ----------
    year : int
    month : int
    day : int

    Warnings
    --------
    Although B.C.E. dates are allowed, they should be treated as
    approximations as they may return inconsistent results when converting
    between date types and using arithmetic and comparison operators!
    """
    def __init__(self, year: int, month: int, day: int, jd: float | None = None) -> None:
        """
        Initialize a GregorianDate.

        This initializer extends the CalendarDateMixin initializer
        adding in date validation specific to Gregorian dates.
        """
        ...
    def __format__(self, fmt: str) -> str: ...
    def strftime(self, fmt: str) -> str:
        """
        Return formatted date.

        Wraps :py:meth:`datetime.date.strftime` method and uses the same
        format options.

        Parameters
        ----------
        fmt : str
            The format string.

        Returns
        -------
        str
        """
        ...
    @property
    def jd(self) -> float:
        """
        Return the corresponding Julian day number.

        Returns
        -------
        float
            The Julian day number at midnight.
        """
        ...
    @classmethod
    def from_pydate(cls, pydate: datetime.date) -> Self:
        """
        Return a `GregorianDate` instance from a python date object.

        Parameters
        ----------
        pydate : datetime.date
            A python standard library ``datetime.date`` instance.

        Returns
        -------
        GregorianDate
        """
        ...
    @staticmethod
    def today() -> GregorianDate:
        """
        Return a GregorianDate instance for the current day.

        This static method wraps the Python standard library's
        date.today() method to get the date from the timestamp.

        Returns
        -------
        GregorianDate
          The current Gregorian date from the computer's timestamp.
        """
        ...
    def is_leap(self) -> bool:
        """
        Return if the date is in a leap year

        Returns
        -------
        bool
            True if the date is in a leap year, False otherwise.
        """
        ...
    def to_jd(self) -> JulianDay:
        """
        Convert to a Julian day.

        Returns
        -------
        JulianDay
            The equivalent JulianDay instance.
        """
        ...
    def to_heb(self) -> HebrewDate:
        """
        Convert to Hebrew date.

        Returns
        -------
        HebrewDate
            The equivalent HebrewDate instance.
        """
        ...
    def to_pydate(self) -> datetime.date:
        """
        Convert to a standard library date.

        Returns
        -------
        datetime.date
            The equivalent datetime.date instance.
        """
        ...

class HebrewDate(BaseDate, CalendarDateMixin):
    """
    A class for manipulating Hebrew dates.

    The following format options are available similar to strftime:

    ====== ======= ===========================================================
    Format Example Meaning
    ====== ======= ===========================================================
    %a     Sun     Weekday as locale's abbreviated name
    %A     Sunday  Weekday as locale's full name
    %w     1       Weekday as decimal number 1-7 Sunday-Shabbos
    %d     07      Day of the month as a 0-padded 2 digit decimal number
    %-d    7       Day of the month as a decimal number
    %B     Iyar    Month name transliterated into English
    %m     02      Month as a 0-padded 2 digit decimal number
    %-m    2       Month as a decimal number
    %y     82, 01  Year without century as a zero-padded decimal number
    %Y     5782    Year as a decimal number
    %*a    א׳      Weekday as a Hebrew numeral
    %*A    ראשון   Weekday name in Hebrew
    %*d    ז׳, ט״ז Day of month as Hebrew numeral
    %*-d   א, טו   Day of month without gershayim
    %*B    אייר    Name of month in Hebrew
    %*y    תשפ״ב   Year in Hebrew numerals without the thousands place
    %*Y    ה'תשפ״ב Year in Hebrew numerals with the thousands place
    %%     %       A literal '%' character
    ====== ======= ===========================================================

    Example
    -------
    >>> date = HebrewDate(5783, 1, 15)
    >>> f'Today is {date:%a - %*-d %*B, %*y}'
    'Today is Thu - טו אייר, תשפ"ג'

    Parameters
    ----------
    year : int
        The Hebrew year.

    month : int
        The Hebrew month starting with Nissan as 1 (and Tishrei as 7). If
        there is a second Adar in the year it is has a value of 13.

    day : int
        The Hebrew day of the month.

    jd : float, optional
        This parameter should not be assigned manually.

    Attributes
    ----------
    year : int
    month : int
        The Hebrew month starting with Nissan as 1 (and Tishrei as 7).
        If there is a second Adar it has a value of 13.
    day : int
        The day of the month.

    Raises
    ------
    ValueError
        If the year is less than 1, if the month is less than 1 or greater
        than the last month, or if the day does not exist in the month a
        ``ValueError`` will be raised.
    """
    def __init__(self, year: int, month: int, day: int, jd: float | None = None) -> None:
        """
        Initialize a HebrewDate instance.

        This initializer extends the CalendarDateMixin adding validation
        specific to hebrew dates.
        """
        ...
    def __format__(self, fmt: str) -> str: ...
    @property
    def jd(self) -> float:
        """
        Return the corresponding Julian day number.

        Returns
        -------
        float
            The Julian day number at midnight.
        """
        ...
    @staticmethod
    def from_pydate(pydate: datetime.date) -> HebrewDate:
        """
        Return a `HebrewDate` from a python date object.

        Parameters
        ----------
        pydate : datetime.date
            A python standard library ``datetime.date`` instance

        Returns
        -------
        HebrewDate
        """
        ...
    @staticmethod
    def today() -> HebrewDate:
        """
        Return HebrewDate instance for the current day.

        This static method wraps the Python standard library's
        ``date.today()`` method to get the date from the timestamp.

        Returns
        -------
        HebrewDate
            The current Hebrew date from the computer's timestamp.

        Warning
        -------
        Pyluach treats Hebrew dates as if they change at midnight. If it's
        after nightfall but before midnight, to get the true Hebrew date do
        ``HebrewDate.today() + 1``.
        """
        ...
    def to_jd(self) -> JulianDay:
        """
        Convert to a Julian day.

        Returns
        -------
        JulianDay
            The equivalent JulianDay instance.
        """
        ...
    def to_greg(self) -> GregorianDate:
        """
        Convert to a Gregorian date.

        Returns
        -------
        GregorianDate
            The equivalent GregorianDate instance.
        """
        ...
    def to_pydate(self) -> datetime.date:
        """
        Convert to a standard library date.

        Returns
        -------
        datetime.date
            The equivalent datetime.date instance.
        """
        ...
    def to_heb(self) -> HebrewDate: ...
    def month_name(self, hebrew: bool = False) -> str:
        """
        Return the name of the month.

        Parameters
        ----------
        hebrew : bool, optional
            ``True`` if the month name should be in Hebrew characters.
            Default is ``False`` which returns the month name
            transliterated into English.

        Returns
        -------
        str
        """
        ...
    def hebrew_day(self, withgershayim: bool = True) -> str:
        """
        Return the day of the month in Hebrew letters.

        Parameters
        ----------
        withgershayim : bool, optional
            Default is ``True`` which includes a geresh with a single
            character and gershayim between two characters.

        Returns
        -------
        str
            The day of the month in Hebrew letters.

        Examples
        --------
        >>> date = HebrewDate(5782, 3, 6)
        >>> date.hebrew_day()
        'ו׳'
        >>> date.hebrew_day(False)
        'ו'
        >>> HebrewDate(5783, 12, 14).hebrew_day()
        'י״ד'
        """
        ...
    def hebrew_year(self, thousands: bool = False, withgershayim: bool = True) -> str:
        """
        Return the year in Hebrew letters.

        Parameters
        ----------
        thousands : bool
            ``True`` to prefix the year with a letter for the
            thousands place, ie. 'ה׳תשפ״א'. Default is ``False``.
        withgershayim : bool, optional
            Default is ``True`` which includes a geresh after the thousands
            place if applicable and a gershayim before the last character
            of the year.

        Returns
        -------
        str
        """
        ...
    def hebrew_date_string(self, thousands: bool = False) -> str:
        """
        Return a Hebrew string representation of the date.

        The date is in the form ``f'{day} {month} {year}'``.

        Parameters
        ----------
        thousands : bool
            ``True`` to have the thousands include in the year.
            Default is ``False``.

        Returns
        -------
        str

        Examples
        --------
        >>> date = HebrewDate(5781, 9, 25)
        >>> date.hebrew_date_string()
        'כ״ה כסלו תשפ״א'
        >>> date.hebrew_date_string(True)
        'כ״ה כסלו ה׳תשפ״א'
        """
        ...
    def add(
        self, years: int = 0, months: int = 0, days: int = 0, adar1: bool | None = False, rounding: Rounding = Rounding.NEXT_DAY
    ) -> HebrewDate:
        """
        Add years, months, and days to date.

        Parameters
        ----------
        years : int, optional
            The number of years to add. Default is 0.
        months : int, optional
            The number of months to add. Default is 0.
        days : int, optional
            The number of days to add. Default is 0.
        adar1 : bool, optional
            True to return a date in Adar Aleph if `self` is in a regular
            Adar and after adding the years it's leap year. Default is
            ``False`` which will return the date in Adar Beis.
        rounding : Rounding, optional
            Choose what to do if self is the 30th day of the month, and
            there are only 29 days in the destination month.
            :obj:`Rounding.NEXT_DAY` to return the first day of the next
            month. :obj:`Rounding.PREVIOUS_DAY` to return the last day of
            the month. :obj:`Rounding.EXCEPTION` to raise a ValueError.
            Default is :obj:`Rounding.NEXT_DAY`.

        Returns
        -------
        HebrewDate

        Note
        ----
        This method first adds the `years`. If the starting month is
        Adar and the destination year has two Adars, it chooses which
        one based on the `adar1` argument, then it adds the `months`. If
        the starting day doesn't exist in that month it adjusts it based
        on the `rounding` argument, then it adds the `days`.

        Examples
        --------
        >>> date = HebrewDate(5783, 11, 30)
        >>> date.add(months=1)
        HebrewDate(5783, 1, 1)
        >>> date.add(months=1, rounding=Rounding.PREVIOUS_DAY)
        HebrewDate(5783, 12, 29)
        """
        ...
    def subtract(
        self, years: int = 0, months: int = 0, days: int = 0, adar1: bool | None = False, rounding: Rounding = Rounding.NEXT_DAY
    ) -> HebrewDate:
        """
        Subtract years, months, and days from date.

        Parameters
        ----------
        years : int, optional
            The number of years to subtract. Default is 0.
        months : int, optional
            The number of months to subtract. Default is 0.
        days : int, optional
            The number of days to subtract. Default is 0.
        adar1 : bool, optional
            True to return a date in Adar Aleph if `self` is in a regular
            Adar and the destination year is leap year. Default is
            ``False`` which will return the date in Adar Beis.
        rounding : Rounding, optional
            Choose what to do if self is the 30th day of the month, and
            there are only 29 days in the destination month.
            :obj:`Rounding.NEXT_DAY` to return the first day of the next
            month. :obj:`Rounding.PREVIOUS_DAY` to return the last day of
            the month. :obj:`Rounding.EXCEPTION` to raise a ValueError.
            Default is :obj:`Rounding.NEXT_DAY`.

        Returns
        -------
        HebrewDate

        Note
        ----
        This method first subtracts the `years`. If the starting month
        is Adar and the destination year has two Adars, it chooses which
        one based on the `adar1` argument, then it subtracts the
        `months`. If the starting day doesn't exist in that month it
        adjusts it based on the `rounding` argument, then it subtracts
        the `days`.
        """
        ...

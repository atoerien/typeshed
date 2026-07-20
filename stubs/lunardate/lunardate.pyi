"""
A Chinese Calendar Library in Pure Python
=========================================

Chinese Calendar: http://en.wikipedia.org/wiki/Chinese_calendar

Usage
-----
        >>> LunarDate.from_solar_date(1976, 10, 1)
        LunarDate(1976, 8, 8, 1)
        >>> LunarDate(1976, 8, 8, 1).to_solar_date()
        datetime.date(1976, 10, 1)
        >>> LunarDate(1976, 8, 8, 1).year
        1976
        >>> LunarDate(1976, 8, 8, 1).month
        8
        >>> LunarDate(1976, 8, 8, 1).day
        8
        >>> LunarDate(1976, 8, 8, 1).is_leap_month
        True

        >>> today = LunarDate.today()
        >>> type(today).__name__
        'LunarDate'

        >>> # support '+' and '-' between datetime.date and datetime.timedelta
        >>> ld = LunarDate(1976,8,8)
        >>> sd = datetime.date(2008,1,1)
        >>> td = datetime.timedelta(days=10)
        >>> ld-ld
        datetime.timedelta(0)
        >>> (ld-sd).days
        -11444
        >>> ld-td
        LunarDate(1976, 7, 27, 0)
        >>> (sd-ld).days
        11444
        >>> ld+td
        LunarDate(1976, 8, 18, 0)
        >>> td+ld
        LunarDate(1976, 8, 18, 0)
        >>> ld2 = LunarDate.today()
        >>> ld < ld2
        True
        >>> ld <= ld2
        True
        >>> ld > ld2
        False
        >>> ld >= ld2
        False
        >>> ld == ld2
        False
        >>> ld != ld2
        True
        >>> ld == ld
        True
        >>> LunarDate.today() == LunarDate.today()
        True
        >>> before_leap_month = LunarDate.from_solar_date(2088, 5, 17)
        >>> before_leap_month.year
        2088
        >>> before_leap_month.month
        4
        >>> before_leap_month.day
        27
        >>> before_leap_month.is_leap_month
        False
        >>> leap_month = LunarDate.from_solar_date(2088, 6, 17)
        >>> leap_month.year
        2088
        >>> leap_month.month
        4
        >>> leap_month.day
        28
        >>> leap_month.is_leap_month
        True
        >>> after_leap_month = LunarDate.from_solar_date(2088, 7, 17)
        >>> after_leap_month.year
        2088
        >>> after_leap_month.month
        5
        >>> after_leap_month.day
        29
        >>> after_leap_month.is_leap_month
        False

        >>> LunarDate.leap_month_for_year(2023)
        2
        >>> LunarDate.leap_month_for_year(2022) # will return None

Limits
------

this library can only deal with year from 1900 to 2099 (in chinese calendar).

See also
--------

* lunar: http://packages.qa.debian.org/l/lunar.html,
  A converter written in C, this program is derived from it.
* python-lunar: http://code.google.com/p/liblunar/
  Another library written in C, including a python binding.
"""

import datetime
from typing import Final, SupportsIndex, overload
from typing_extensions import deprecated

__version__: Final[str]
__all__ = ["LunarDate"]

class LunarDate:
    year: int
    month: int
    day: int
    is_leap_month: bool
    def __init__(self, year: int, month: int, day: int, is_leap_month: bool | None = False) -> None: ...
    @property
    @deprecated("The `isLeapMonth` is deprecated since v0.3.0. Use `is_leap_month` instead.")
    def isLeapMonth(self) -> bool: ...
    @staticmethod
    @deprecated("The `leapMonthForYear` is deprecated since v0.3.0. Use `leap_month_for_year` instead.")
    def leapMonthForYear(year: int) -> int | None: ...
    @staticmethod
    def leap_month_for_year(year: int) -> int | None:
        """
        return None if no leap month, otherwise return the leap month of the year.
        return 1 for the first month, and return 12 for the last month.

        >>> LunarDate.leap_month_for_year(1976)
        8
        >>> LunarDate.leap_month_for_year(2023)
        2
        >>> LunarDate.leap_month_for_year(2022)
        """
        ...
    @staticmethod
    @deprecated("The `fromSolarDate` is deprecated since v0.3.0. Use `from_solar_date` instead.")
    def fromSolarDate(year: SupportsIndex, month: SupportsIndex, day: SupportsIndex) -> LunarDate: ...
    @staticmethod
    def from_solar_date(year: SupportsIndex, month: SupportsIndex, day: SupportsIndex) -> LunarDate:
        """
        >>> LunarDate.from_solar_date(1900, 1, 31)
        LunarDate(1900, 1, 1, 0)
        >>> LunarDate.from_solar_date(2008, 10, 2)
        LunarDate(2008, 9, 4, 0)
        >>> LunarDate.from_solar_date(1976, 10, 1)
        LunarDate(1976, 8, 8, 1)
        >>> LunarDate.from_solar_date(2033, 10, 23)
        LunarDate(2033, 10, 1, 0)
        >>> LunarDate.from_solar_date(1956, 12, 2)
        LunarDate(1956, 11, 1, 0)
        """
        ...
    @deprecated("The `toSolarDate` is deprecated since v0.3.0. Use `to_solar_date` instead.")
    def toSolarDate(self) -> datetime.date: ...
    def to_solar_date(self) -> datetime.date:
        """
        >>> LunarDate(1900, 1, 1).to_solar_date()
        datetime.date(1900, 1, 31)
        >>> LunarDate(2008, 9, 4).to_solar_date()
        datetime.date(2008, 10, 2)
        >>> LunarDate(1976, 8, 8, 1).to_solar_date()
        datetime.date(1976, 10, 1)
        >>> LunarDate(1976, 7, 8, 1).to_solar_date()
        Traceback (most recent call last):
        ...
        ValueError: month out of range
        >>> LunarDate(1899, 1, 1).to_solar_date()
        Traceback (most recent call last):
        ...
        ValueError: year out of range [1900, 2100)
        >>> LunarDate(2004, 1, 30).to_solar_date()
        Traceback (most recent call last):
        ...
        ValueError: day out of range
        >>> LunarDate(2004, 13, 1).to_solar_date()
        Traceback (most recent call last):
        ...
        ValueError: month out of range
        >>> LunarDate(2100, 1, 1).to_solar_date()
        Traceback (most recent call last):
        ...
        ValueError: year out of range [1900, 2100)
        >>>
        """
        ...

    @overload
    def __sub__(self, other: LunarDate | datetime.date) -> datetime.timedelta: ...
    @overload
    def __sub__(self, other: datetime.timedelta) -> LunarDate: ...

    def __rsub__(self, other: datetime.date) -> datetime.timedelta: ...
    def __add__(self, other: datetime.timedelta) -> LunarDate: ...
    def __radd__(self, other: datetime.timedelta) -> LunarDate: ...
    def __eq__(self, other: object) -> bool:
        """
        >>> LunarDate.today() == 5
        False
        """
        ...
    def __lt__(self, other: LunarDate | datetime.date) -> bool:
        """
        >>> LunarDate.today() < LunarDate.today()
        False
        >>> LunarDate.today() < 5
        Traceback (most recent call last):
        ...
        TypeError: can't compare LunarDate to int
        """
        ...
    def __le__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool:
        """
        >>> LunarDate.today() > LunarDate.today()
        False
        >>> LunarDate.today() > 5
        Traceback (most recent call last):
        ...
        TypeError: can't compare LunarDate to int
        """
        ...
    def __ge__(self, other: LunarDate | datetime.date) -> bool:
        """
        >>> LunarDate.today() >= LunarDate.today()
        True
        >>> LunarDate.today() >= 5
        Traceback (most recent call last):
        ...
        TypeError: can't compare LunarDate to int
        """
        ...
    @classmethod
    def today(cls) -> LunarDate: ...

YEAR_INFOS: Final[list[int]]

def year_info_to_year_day(year_info: int) -> int:
    """
    calculate the days in a lunar year from the lunar year's info

    >>> year_info_to_year_day(0) # no leap month, and every month has 29 days.
    348
    >>> year_info_to_year_day(1) # 1 leap month, and every month has 29 days.
    377
    >>> year_info_to_year_day((2**12-1)*16) # no leap month, and every month has 30 days.
    360
    >>> year_info_to_year_day((2**13-1)*16+1) # 1 leap month, and every month has 30 days.
    390
    >>> # 1 leap month, and every normal month has 30 days, and leap month has 29 days.
    >>> year_info_to_year_day((2**12-1)*16+1)
    389
    """
    ...

YEAR_DAYS: Final[list[int]]

def day_to_lunar_date(offset: int) -> None: ...

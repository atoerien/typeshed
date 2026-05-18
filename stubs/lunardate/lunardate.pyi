"""
A Chinese Calendar Library in Pure Python
=========================================

Chinese Calendar: http://en.wikipedia.org/wiki/Chinese_calendar

Usage
-----
        >>> LunarDate.fromSolarDate(1976, 10, 1)
        LunarDate(1976, 8, 8, 1)
        >>> LunarDate(1976, 8, 8, 1).toSolarDate()
        datetime.date(1976, 10, 1)
        >>> LunarDate(1976, 8, 8, 1).year
        1976
        >>> LunarDate(1976, 8, 8, 1).month
        8
        >>> LunarDate(1976, 8, 8, 1).day
        8
        >>> LunarDate(1976, 8, 8, 1).isLeapMonth
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
        >>> before_leap_month = LunarDate.fromSolarDate(2088, 5, 17)
        >>> before_leap_month.year
        2088
        >>> before_leap_month.month
        4
        >>> before_leap_month.day
        27
        >>> before_leap_month.isLeapMonth
        False
        >>> leap_month = LunarDate.fromSolarDate(2088, 6, 17)
        >>> leap_month.year
        2088
        >>> leap_month.month
        4
        >>> leap_month.day
        28
        >>> leap_month.isLeapMonth
        True
        >>> after_leap_month = LunarDate.fromSolarDate(2088, 7, 17)
        >>> after_leap_month.year
        2088
        >>> after_leap_month.month
        5
        >>> after_leap_month.day
        29
        >>> after_leap_month.isLeapMonth
        False

        >>> LunarDate.leapMonthForYear(2023)
        2
        >>> LunarDate.leapMonthForYear(2022)
        None        

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
from _typeshed import ConvertibleToInt
from typing import Final, SupportsIndex, overload

__version__: Final[str]
__all__ = ["LunarDate"]

class LunarDate:
    year: int
    month: int
    day: int
    isLeapMonth: bool
    def __init__(self, year: int, month: int, day: int, isLeapMonth: bool | None = False) -> None: ...
    @staticmethod
    def leapMonthForYear(year: int) -> int | None:
        """
        return None if no leap month, otherwise return the leap month of the year.
        return 1 for the first month, and return 12 for the last month.

        >>> LunarDate.leapMonthForYear(1976)
        8
        >>> LunarDate.leapMonthForYear(2023)
        2
        >>> LunarDate.leapMonthForYear(2022)
        """
        ...
    @staticmethod
    def fromSolarDate(year: SupportsIndex, month: SupportsIndex, day: SupportsIndex) -> LunarDate: ...
    def toSolarDate(self) -> datetime.date: ...

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

yearInfos: Final[list[int]]

def yearInfo2yearDay(yearInfo: ConvertibleToInt) -> int:
    """
    calculate the days in a lunar year from the lunar year's info

    >>> yearInfo2yearDay(0) # no leap month, and every month has 29 days.
    348
    >>> yearInfo2yearDay(1) # 1 leap month, and every month has 29 days.
    377
    >>> yearInfo2yearDay((2**12-1)*16) # no leap month, and every month has 30 days.
    360
    >>> yearInfo2yearDay((2**13-1)*16+1) # 1 leap month, and every month has 30 days.
    390
    >>> # 1 leap month, and every normal month has 30 days, and leap month has 29 days.
    >>> yearInfo2yearDay((2**12-1)*16+1)
    389
    """
    ...

yearDays: Final[list[int]]

def day2LunarDate(offset: ConvertibleToInt) -> None: ...

"""
The hebrewcal module contains Hebrew calendar related classes and functions.

It contains classes for representing a Hebrew year and month, functions
for getting the holiday or fast day for a given date, and classes adapting
:py:mod:`calendar` classes to render Hebrew calendars.

Contents
--------
* :class:`Year`
* :class:`Month`
* :func:`to_hebrew_numeral`
* :class:`HebrewCalendar`
* :class:`HebrewHTMLCalendar`
* :class:`HebrewTextCalendar`
* :func:`fast_day`
* :func:`festival`
* :func:`holiday`
"""

import calendar
import datetime
from collections.abc import Generator
from typing import Literal, TypedDict, overload, type_check_only
from typing_extensions import Self

from .dates import BaseDate, HebrewDate

@type_check_only
class _MoladDict(TypedDict):
    weekday: int
    hours: int
    parts: int

@type_check_only
class _MoladAnnouncementDict(TypedDict):
    weekday: int
    hour: int
    minutes: int
    parts: int

class IllegalMonthError(ValueError):
    """
    An exception for an illegal month.

    Subclasses ``ValueError`` to show a message for an invalid month number
    for the Hebrew calendar. Mimics :py:class:`calendar.IllegalMonthError`.

    Parameters
    ----------
    month : int
        The invalid month number
    """
    month: int
    def __init__(self, month: int) -> None: ...

class IllegalWeekdayError(ValueError):
    """
    An exception for an illegal weekday.

    Subclasses ``ValueError`` to show a message for an invalid weekday
    number. Mimics :py:class:`calendar.IllegalWeekdayError`.

    Parameters
    ----------
    month : int
        The invalid month number
    """
    weekday: int
    def __init__(self, weekday: int) -> None: ...

class Year:
    """
    A Year object represents a Hebrew calendar year.

    It provided the following operators:

    =====================  ================================================
    Operation              Result
    =====================  ================================================
    year2 = year1 + int    New ``Year`` ``int``  days after year1.
    year2 = year1 - int    New ``Year`` ``int`` days before year1.
    int = year1 - year2    ``int`` equal to the absolute value of
                           the difference between year2 and year1.
    bool = year1 == year2  True if year1 represents the same year as year2.
    bool = year1 > year2   True if year1 is later than year2.
    bool = year1 >= year2  True if year1 is later or equal to year2.
    bool = year1 < year2   True if year 1 earlier than year2.
    bool = year1 <= year2  True if year 1 earlier or equal to year 2.
    =====================  ================================================

    Parameters
    ----------
    year : int
        A Hebrew year.

    Attributes
    ----------
    year : int
        The hebrew year.
    leap : bool
        True if the year is a leap year else false.
    """
    year: int
    leap: bool
    def __init__(self, year: int) -> None: ...
    def __len__(self) -> int: ...
    def __eq__(self, other: object) -> bool: ...
    def __add__(self, other: int) -> Year: ...

    @overload
    def __sub__(self, other: int) -> Year:
        """
        Subtract int or Year from Year.

        If other is an int return a new Year other before original year. If
        other is a Year object, return delta of the two years as an int.
        """
        ...
    @overload
    def __sub__(self, other: Year) -> int: ...

    def __gt__(self, other: Year) -> bool: ...
    def __ge__(self, other: Year) -> bool: ...
    def __lt__(self, other: Year) -> bool: ...
    def __le__(self, other: Year) -> bool: ...
    def __iter__(self) -> Generator[int]:
        """Yield integer for each month in year."""
        ...
    def monthscount(self) -> Literal[12, 13]:
        """
        Return number of months in the year.

        Returns
        -------
        int
        """
        ...
    def itermonths(self) -> Generator[Month]:
        """
        Yield Month instance for each month of the year.

        Yields
        ------
        :obj:`Month`
            The next month in the Hebrew calendar year as a
            ``Month`` instance beginning with Tishrei through Elul.
        """
        ...
    def iterdays(self) -> Generator[int]:
        """
        Yield integer for each day of the year.

        Yields
        ------
        :obj:`int`
            An integer beginning with 1 for the the next day of
            the year.
        """
        ...
    def iterdates(self) -> Generator[HebrewDate]:
        """
        Iterate through each Hebrew date of the year.

        Yields
        ------
        :obj:`pyluach.dates.HebrewDate`
            The next date of the Hebrew calendar year starting with
            the first of Tishrei.
        """
        ...
    @classmethod
    def from_date(cls, date: BaseDate) -> Self:
        """
        Return Year object that given date occurs in.

        Parameters
        ----------
        date : ~pyluach.dates.BaseDate
            Any subclass of ``BaseDate``.

        Returns
        -------
        Year
        """
        ...
    @classmethod
    def from_pydate(cls, pydate: datetime.date) -> Self:
        """
        Return Year object from python date object.

        Parameters
        ----------
        pydate : datetime.date
            A python standard library date object

        Returns
        -------
        Year
            The Hebrew year the given date occurs in
        """
        ...
    def year_string(self, thousands: bool = False) -> str:
        """
        Return year as a Hebrew string.

        Parameters
        ----------
        thousands: bool, optional
            ``True`` to prefix the year with the thousands place.
            Default is ``False``.

        Examples
        --------
        >>> year = Year(5781)
        >>> year.year_string()
        תשפ״א
        >>> year.year_string(True)
        ה׳תשפ״א
        """
        ...

class Month:
    """
    A Month object represents a month of the Hebrew calendar.

    It provides the same operators as a `Year` object.

    Parameters
    ----------
    year : int
    month : int
        The month as an integer starting with 7 for Tishrei through 13
        if necessary for Adar Sheni and then 1-6 for Nissan - Elul.

    Attributes
    ----------
    year : int
        The Hebrew year.
    month : int
        The month as an integer starting with 7 for Tishrei through 13
        if necessary for Adar Sheni and then 1-6 for Nissan - Elul.
    """
    year: int
    month: int
    def __init__(self, year: int, month: int) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Generator[int]: ...
    def __eq__(self, other: object) -> bool: ...
    def __add__(self, other: int) -> Month: ...

    @overload
    def __sub__(self, other: int) -> Month: ...
    @overload
    def __sub__(self, other: Month) -> int: ...

    def __gt__(self, other: Month) -> bool: ...
    def __ge__(self, other: Month) -> bool: ...
    def __lt__(self, other: Month) -> bool: ...
    def __le__(self, other: Month) -> bool: ...
    @classmethod
    def from_date(cls, date: BaseDate) -> Month:
        """
        Return Month object that given date occurs in.

        Parameters
        ----------
        date : ~pyluach.dates.BaseDate
            Any subclass of ``BaseDate``.
        Returns
        -------
        Month
            The Hebrew month the given date occurs in
        """
        ...
    @classmethod
    def from_pydate(cls, pydate: datetime.date) -> Month:
        """
        Return Month object from python date object.

        Parameters
        ----------
        pydate : datetime.date
            A python standard library date object

        Returns
        -------
        Month
            The Hebrew month the given date occurs in
        """
        ...
    def month_name(self, hebrew: bool = False) -> str:
        """
        Return the name of the month.

        Replaces `name` attribute.

        Parameters
        ----------
        hebrew : bool, optional
            `True` if the month name should be written with Hebrew letters
            and False to be transliterated into English using the Ashkenazic
            pronunciation. Default is `False`.

        Returns
        -------
        str
        """
        ...
    def month_string(self, thousands: bool = False) -> str:
        """
        Return month and year in Hebrew.

        Parameters
        ----------
        thousands : bool, optional
            ``True`` to prefix year with thousands place.
            Default is ``False``.

        Returns
        -------
        str
            The month and year in Hebrew in the form ``f'{month} {year}'``.
        """
        ...
    def starting_weekday(self) -> int:
        """
        Return first weekday of the month.

        Returns
        -------
        int
            The weekday of the first day of the month starting with Sunday as 1
            through Saturday as 7.
        """
        ...
    def iterdates(self) -> Generator[HebrewDate]:
        """
        Iterate through the Hebrew dates of the month.

        Yields
        ------
        :obj:`pyluach.dates.HebrewDate`
            The next Hebrew date of the month.
        """
        ...
    def molad(self) -> _MoladDict:
        """
        Return the month's molad.

        Returns
        -------
        dict
            A dictionary in the form
            ``{weekday: int, hours: int, parts: int}``

        Note
        -----
        This method does not return the molad in the form that is
        traditionally announced in the shul. This is the molad in the
        form used to calculate the length of the year.

        See Also
        --------
        molad_announcement: The molad as it is traditionally announced.
        """
        ...
    def molad_announcement(self) -> _MoladAnnouncementDict:
        """
        Return the month's molad in the announcement form.

        Returns a dictionary in the form that the molad is traditionally
        announced. The weekday is adjusted to change at midnight and
        the hour of the day and minutes are given as traditionally announced.
        Note that the hour is given as in a twenty four hour clock ie. 0 for
        12:00 AM through 23 for 11:00 PM.

        Returns
        -------
        dict
            A dictionary in the form::

                {
                    weekday: int,
                    hour: int,
                    minutes: int,
                    parts: int
                }
        """
        ...

def to_hebrew_numeral(num: int, thousands: bool = False, withgershayim: bool = True) -> str:
    """
    Convert int to Hebrew numeral.

    Function useful in formatting Hebrew calendars.

    Parameters
    ----------
    num : int
        The number to convert
    thousands : bool, optional
        True if the hebrew returned should include a letter for the
        thousands place ie. 'ה׳' for five thousand. Default is  ``False``.
    withgershayim : bool, optional
        ``True`` to include a geresh after a single letter and double
        geresh before the last letter if there is more than one letter.
        Default is ``True``.

    Returns
    -------
    str
        The Hebrew numeral representation of the number.
    """
    ...

class HebrewCalendar(calendar.Calendar):
    """
    Calendar base class.

    This class extends the python library
    :py:class:`Calendar <calendar.Calendar>` class for the Hebrew calendar. The
    weekdays are 1 for Sunday through 7 for Shabbos.

    Parameters
    ----------
    firstweekday : int, optional
        The weekday to start each week with. Default is ``1`` for Sunday.
    hebrewnumerals : bool, optional
        Default is ``True``, which shows the days of the month with Hebrew
        numerals. ``False`` shows the days of the month as a decimal number.
    hebrewweekdays : bool, optional
        ``True`` to show the weekday in Hebrew. Default is ``False``,
        which shows the weekday in English.
    hebrewmonths : bool, optional
        ``True`` to show the month name in Hebrew. Default is ``False``,
        which shows the month name transliterated into English.
    hebrewyear : bool, optional
        ``True`` to show the year in Hebrew numerals. Default is ``False``,
        which shows the year as a decimal number.

    Attributes
    ----------
    hebrewnumerals : bool
    hebrewweekdays : bool
    hebrewmonths : bool
    hebrewyear : bool

    Note
    ----
    All of the parameters other than `firstweekday` are not used in the
    ``HebrewCalendar`` base class. They're there for use in child
    classes.
    """
    hebrewnumerals: bool
    hebrewweekdays: bool
    hebrewmonths: bool
    hebrewyear: bool
    def __init__(
        self,
        firstweekday: int = 1,
        hebrewnumerals: bool = True,
        hebrewweekdays: bool = False,
        hebrewmonths: bool = False,
        hebrewyear: bool = False,
    ) -> None: ...

    @property
    def firstweekday(self) -> int:
        """
        Get and set the weekday the weeks should start with.

        Returns
        -------
        int
        """
        ...
    @firstweekday.setter
    def firstweekday(self, thefirstweekday: int) -> None: ...

    def iterweekdays(self) -> Generator[int]: ...
    def itermonthdates(self, year: int, month: int) -> Generator[HebrewDate]: ...  # type: ignore[override]
    def itermonthdays(self, year: int, month: int) -> Generator[int]: ...
    def itermonthdays2(self, year: int, month: int) -> Generator[tuple[int, int]]: ...
    def itermonthdays3(self, year: int, month: int) -> Generator[tuple[int, int, int]]: ...
    def itermonthdays4(self, year: int, month: int) -> Generator[tuple[int, int, int, int]]: ...
    def yeardatescalendar(self, year: int, width: int = 3) -> list[list[list[list[HebrewDate]]]]: ...  # type: ignore[override]
    def yeardays2calendar(self, year: int, width: int = 3) -> list[list[list[list[tuple[int, int]]]]]: ...
    def yeardayscalendar(self, year: int, width: int = 3) -> list[list[list[list[int]]]]: ...
    def monthdatescalendar(self, year: int, month: int) -> list[list[HebrewDate]]: ...  # type: ignore[override]

class HebrewHTMLCalendar(HebrewCalendar, calendar.HTMLCalendar):
    """
    Class to generate html calendars .

    Adapts :py:class:`calendar.HTMLCalendar` for the Hebrew calendar.

    Parameters
    ----------
    firstweekday : int, optional
        The weekday to start each week with. Default is ``1`` for Sunday.
    hebrewnumerals : bool, optional
        Default is ``True``, which shows the days of the month with Hebrew
        numerals. ``False`` shows the days of the month as a decimal number.
    hebrewweekdays : bool, optional
        ``True`` to show the weekday in Hebrew. Default is ``False``,
        which shows the weekday in English.
    hebrewmonths : bool, optional
        ``True`` to show the month name in Hebrew. Default is ``False``,
        which shows the month name transliterated into English.
    hebrewyear : bool, optional
        ``True`` to show the year in Hebrew numerals. Default is ``False``,
        which shows the year as a decimal number.
    rtl : bool, optional
        ``True``  to arrange the months and the days of the month from
        right to left. Default is ``False``.

    Attributes
    ----------
    hebrewnumerals : bool
    hebrewweekdays : bool
    hebrewmonths : bool
    hebrewyear : bool
    rtl : bool
    """
    rtl: bool
    def __init__(
        self,
        firstweekday: int = 1,
        hebrewnumerals: bool = True,
        hebrewweekdays: bool = False,
        hebrewmonths: bool = False,
        hebrewyear: bool = False,
        rtl: bool = False,
    ) -> None: ...
    def formatday(self, day: int, weekday: int) -> str:
        """
        Return a day as an html table cell.

        Parameters
        ----------
        day : int
            The day of the month or zero for a day outside the month.
        weekday : int
            The weekday with 1 as Sunday through 7 as Shabbos.

        Returns
        -------
        str
        """
        ...
    def formatweekday(self, day: int) -> str:
        """
        Return a weekday name as an html table header.

        Parameters
        ----------
        day : int
            The day of the week 1-7 with Sunday as 1 and Shabbos as 7.

        Returns
        -------
        str
        """
        ...
    def formatyearnumber(self, theyear: int) -> int | str:
        """
        Return a formatted year.

        Parameters
        ----------
        theyear : int

        Returns
        -------
        int or str
            If ``self.hebrewyear`` is ``True`` return the year as a Hebrew
            numeral, else return `theyear` as is.
        """
        ...
    def formatmonthname(self, theyear: int, themonth: int, withyear: bool = True) -> str:
        """
        Return month name as an html table row.

        Parameters
        ----------
        theyear : int
        themonth : int
            The month as an int 1-12 Nissan - Adar and 13 if leap year.
        withyear : bool, optional
            ``True`` to append the year to the month name. Default is
            ``True``.

        Return
        ------
        str
        """
        ...
    def formatmonth(self, theyear: int, themonth: int, withyear: bool = True) -> str:
        """
        Return a formatted month as an html table.

        Parameters
        ----------
        theyear : int
        themonth : int
        withyear : bool, optional
            ``True`` to have the year appended to the month name. Default
            is ``True``.

        Returns
        -------
        str
        """
        ...
    def formatyear(self, theyear: int, width: int = 3) -> str:
        """
        Return a formatted year as an html table.

        Parameters
        ----------
        theyear : int
        width : int, optional
            The number of months to display per row. Default is 3.

        Returns
        -------
        str
        """
        ...

class HebrewTextCalendar(HebrewCalendar, calendar.TextCalendar):
    """
    Subclass of HebrewCalendar that outputs a plaintext calendar.

    ``HebrewTextCalendar`` adapts :py:class:`calendar.TextCalendar` for the
    Hebrew calendar.

    Parameters
    ----------
    firstweekday : int, optional
        The weekday to start each week with. Default is ``1`` for Sunday.
    hebrewnumerals : bool, optional
        Default is ``True``, which shows the days of the month with Hebrew
        numerals. ``False`` shows the days of the month as a decimal number.
    hebrewweekdays : bool, optional
        ``True`` to show the weekday in Hebrew. Default is ``False``,
        which shows the weekday in English.
    hebrewmonths : bool, optional
        ``True`` to show the month name in Hebrew. Default is ``False``,
        which shows the month name transliterated into English.
    hebrewyear : bool, optional
        ``True`` to show the year in Hebrew numerals. Default is ``False``,
        which shows the year as a decimal number.

    Attributes
    ----------
    hebrewnumerals : bool
    hebrewweekdays : bool
    hebrewmonths : bool
    hebrewyear : bool

    Note
    ----
    This class generates plain text calendars. Any program that adds
    any formatting may misrender the calendars especially when using any
    Hebrew characters.
    """
    def formatday(self, day: int, weekday: int, width: int) -> str:
        """
        Return a formatted day.

        Extends calendar.TextCalendar formatday method.

        Parameters
        ----------
        day : int
            The day of the month.
        weekday : int
            The weekday 1-7 Sunday-Shabbos.
        width : int
            The width of the day column.

        Returns
        -------
        str
        """
        ...
    def formatweekday(self, day: int, width: int) -> str:
        """
        Return formatted weekday.

        Extends calendar.TextCalendar formatweekday method.

        Parameters
        ----------
        day : int
            The weekday 1-7 Sunday-Shabbos.
        width : int
            The width of the day column.

        Returns
        -------
        str
        """
        ...
    def formatmonthname(self, theyear: int, themonth: int, width: int = 0, withyear: bool = True) -> str:
        """
        Return formatted month name.

        Parameters
        ----------
        theyear : int
        themonth : int
            1-12 or 13 for Nissan-Adar Sheni
        width : int, optional
            The number of columns per day. Default is 0
        withyear : bool, optional
            Default is ``True`` to include the year with the month name.

        Returns
        -------
        str
        """
        ...
    def formatyear(self, theyear: int, w: int = 2, l: int = 1, c: int = 6, m: int = 3) -> str:
        """
        Return a year's calendar as a multi-line string.

        Parameters
        ----------
        theyear : int
        w : int, optional
            The date column width. Default is 2
        l : int, optional
            The number of lines per week. Default is 1.
        c : int, optional
            The number of columns in between each month. Default is 6
        m : int, optional
            The number of months per row. Default is 3.

        Returns
        -------
        str
        """
        ...

def fast_day(date: BaseDate, hebrew: bool = False) -> str | None:
    """
    Return name of fast day or None.

    Parameters
    ----------
    date : ~pyluach.dates.BaseDate
        Any date instance from a subclass of ``BaseDate`` can be used.
    hebrew : bool, optional
        ``True`` if you want the fast_day name in Hebrew letters. Default
        is ``False``, which returns the name transliterated into English.

    Returns
    -------
    str or None
        The name of the fast day or ``None`` if the given date is not
        a fast day.
    """
    ...
def festival(
    date: BaseDate, israel: bool = False, hebrew: bool = False, include_working_days: bool = True, prefix_day: bool = False
) -> str | None:
    """
    Return Jewish festival of given day.

    This method will return all major and minor religous
    Jewish holidays not including fast days.

    Parameters
    ----------
    date : ~pyluach.dates.BaseDate
        Any subclass of ``BaseDate`` can be used.

    israel : bool, optional
        ``True`` if you want the festivals according to the Israel
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
    >>> from pyluach.dates import HebrewDate
    pesach = HebrewDate(2023, 1, 15)
    >>> festival(pesach, prefix_day=True)
    '1 Pesach'
    >>> festival(pesach, hebrew=True, prefix_day=True)
    'א׳ פסח'
    >>> shavuos = HebrewDate(5783, 3, 6)
    >>> festival(shavuos, israel=True, prefix_day=True)
    'Shavuos'
    """
    ...
def holiday(date: BaseDate, israel: bool = False, hebrew: bool = False, prefix_day: bool = False) -> str | None:
    """
    Return Jewish holiday of given date.

    The holidays include the major and minor religious Jewish
    holidays including fast days.

    Parameters
    ----------
    date : pyluach.dates.BaseDate
        Any subclass of ``BaseDate`` can be used.
    israel : bool, optional
        ``True`` if you want the holidays according to the israel
        schedule. Default is ``False``.
    hebrew : bool, optional
        ``True`` if you want the holiday name in Hebrew letters. Default
        is ``False``, which returns the name transliterated into English.
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
    >>> from pyluach.dates import HebrewDate
    >>> pesach = HebrewDate(2023, 1, 15)
    >>> holiday(pesach, prefix_day=True)
    '1 Pesach'
    >>> holiday(pesach, hebrew=True, prefix_day=True)
    'א׳ פסח'
    >>> taanis_esther = HebrewDate(5783, 12, 13)
    >>> holiday(taanis_esther, prefix_day=True)
    'Taanis Esther'
    """
    ...

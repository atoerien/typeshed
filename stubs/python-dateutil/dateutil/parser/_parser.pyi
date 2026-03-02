"""
This module offers a generic date/time string parser which is able to parse
most known formats to represent a date and/or time.

This module attempts to be forgiving with regards to unlikely input formats,
returning a datetime object even for dates which are ambiguous. If an element
of a date/time stamp is omitted, the following rules are applied:

- If AM or PM is left unspecified, a 24-hour clock is assumed, however, an hour
  on a 12-hour clock (``0 <= hour <= 12``) *must* be specified if AM or PM is
  specified.
- If a time zone is omitted, a timezone-naive datetime is returned.

If any other elements are missing, they are taken from the
:class:`datetime.datetime` object passed to the parameter ``default``. If this
results in a day number exceeding the valid number of days per month, the
value falls back to the end of the month.

Additional resources about date/time string formats can be found below:

- `A summary of the international standard date and time notation
  <https://www.cl.cam.ac.uk/~mgk25/iso-time.html>`_
- `W3C Date and Time Formats <https://www.w3.org/TR/NOTE-datetime>`_
- `Time Formats (Planetary Rings Node) <https://pds-rings.seti.org:443/tools/time_formats.html>`_
- `CPAN ParseDate module
  <https://metacpan.org/pod/release/MUIR/Time-modules-2013.0912/lib/Time/ParseDate.pm>`_
- `Java SimpleDateFormat Class
  <https://docs.oracle.com/javase/6/docs/api/java/text/SimpleDateFormat.html>`_
"""

import re
from _typeshed import SupportsRead
from collections.abc import Callable, Mapping
from datetime import _TzInfo, datetime
from io import StringIO
from typing import IO, Any, Literal, overload
from typing_extensions import Self, TypeAlias

_FileOrStr: TypeAlias = bytes | str | IO[str] | IO[Any]
_TzData: TypeAlias = _TzInfo | int | str | None
_TzInfos: TypeAlias = Mapping[str, _TzData] | Callable[[str, int], _TzData]

__all__ = ["parse", "parserinfo", "ParserError"]

class _timelex:
    _split_decimal: re.Pattern[str]
    instream: StringIO | SupportsRead[str]
    charstack: list[str]
    tokenstack: list[str]
    eof: bool
    def __init__(self, instream: str | bytes | bytearray | SupportsRead[str]) -> None: ...
    def get_token(self) -> str | None:
        """
        This function breaks the time string into lexical units (tokens), which
        can be parsed by the parser. Lexical units are demarcated by changes in
        the character set, so any continuous string of letters is considered
        one unit, any continuous string of numbers is considered one unit.

        The main complication arises from the fact that dots ('.') can be used
        both as separators (e.g. "Sep.20.2009") or decimal points (e.g.
        "4:30:21.447"). As such, it is necessary to read the full context of
        any dot-separated strings before breaking it into tokens; as such, this
        function maintains a "token stack", for when the ambiguous context
        demands that multiple tokens be parsed at once.
        """
        ...
    def __iter__(self) -> Self: ...
    def __next__(self) -> str: ...
    def next(self) -> str: ...
    @classmethod
    def split(cls, s: str) -> list[str]: ...
    @classmethod
    def isword(cls, nextchar: str) -> bool:
        """Whether or not the next character is part of a word """
        ...
    @classmethod
    def isnum(cls, nextchar: str) -> bool:
        """Whether the next character is part of a number """
        ...
    @classmethod
    def isspace(cls, nextchar: str) -> bool:
        """Whether the next character is whitespace """
        ...

class _resultbase:
    def __init__(self) -> None: ...
    def _repr(self, classname: str) -> str: ...
    def __len__(self) -> int: ...

class parserinfo:
    """
    Class which handles what inputs are accepted. Subclass this to customize
    the language and acceptable values for each parameter.

    :param dayfirst:
        Whether to interpret the first value in an ambiguous 3-integer date
        (e.g. 01/05/09) as the day (``True``) or month (``False``). If
        ``yearfirst`` is set to ``True``, this distinguishes between YDM
        and YMD. Default is ``False``.

    :param yearfirst:
        Whether to interpret the first value in an ambiguous 3-integer date
        (e.g. 01/05/09) as the year. If ``True``, the first number is taken
        to be the year, otherwise the last number is taken to be the year.
        Default is ``False``.
    """
    JUMP: list[str]
    WEEKDAYS: list[tuple[str, str]]
    MONTHS: list[tuple[str, str] | tuple[str, str, str]]
    HMS: list[tuple[str, str, str]]
    AMPM: list[tuple[str, str]]
    UTCZONE: list[str]
    PERTAIN: list[str]
    TZOFFSET: dict[str, int]
    def __init__(self, dayfirst: bool = False, yearfirst: bool = False) -> None: ...
    def jump(self, name: str) -> bool: ...
    def weekday(self, name: str) -> int | None: ...
    def month(self, name: str) -> int | None: ...
    def hms(self, name: str) -> int | None: ...
    def ampm(self, name: str) -> int | None: ...
    def pertain(self, name: str) -> bool: ...
    def utczone(self, name: str) -> bool: ...
    def tzoffset(self, name: str) -> int | None: ...
    def convertyear(self, year: int, century_specified: bool = False) -> int:
        """
        Converts two-digit years to year within [-50, 49]
        range of self._year (current local time)
        """
        ...
    def validate(self, res: datetime) -> bool: ...

class _ymd(list[int]):
    century_specified: bool
    dstridx: int | None
    mstridx: int | None
    ystridx: int | None
    @property
    def has_year(self) -> bool: ...
    @property
    def has_month(self) -> bool: ...
    @property
    def has_day(self) -> bool: ...
    def could_be_day(self, value: int) -> bool: ...
    def append(self, val: str | int, label: str | None = None) -> None: ...
    def _resolve_from_stridxs(self, strids: dict[str, int]) -> tuple[int, int, int]:
        """
        Try to resolve the identities of year/month/day elements using
        ystridx, mstridx, and dstridx, if enough of these are specified.
        """
        ...
    def resolve_ymd(self, yearfirst: bool | None, dayfirst: bool | None) -> tuple[int, int, int]: ...

class parser:
    info: parserinfo
    def __init__(self, info: parserinfo | None = None) -> None: ...
    @overload
    def parse(
        self,
        timestr: _FileOrStr,
        default: datetime | None = None,
        ignoretz: bool = False,
        tzinfos: _TzInfos | None = None,
        *,
        dayfirst: bool | None = ...,
        yearfirst: bool | None = ...,
        fuzzy: bool = ...,
        fuzzy_with_tokens: Literal[False] = False,
    ) -> datetime: ...
    @overload
    def parse(
        self,
        timestr: _FileOrStr,
        default: datetime | None = None,
        ignoretz: bool = False,
        tzinfos: _TzInfos | None = None,
        *,
        dayfirst: bool | None = ...,
        yearfirst: bool | None = ...,
        fuzzy: bool = ...,
        fuzzy_with_tokens: Literal[True],
    ) -> tuple[datetime, tuple[str, ...]]: ...

DEFAULTPARSER: parser

@overload
def parse(
    timestr: _FileOrStr,
    parserinfo: parserinfo | None = None,
    *,
    dayfirst: bool | None = ...,
    yearfirst: bool | None = ...,
    ignoretz: bool = ...,
    fuzzy: bool = ...,
    fuzzy_with_tokens: Literal[False] = False,
    default: datetime | None = ...,
    tzinfos: _TzInfos | None = ...,
) -> datetime: ...
@overload
def parse(
    timestr: _FileOrStr,
    parserinfo: parserinfo | None = None,
    *,
    dayfirst: bool | None = ...,
    yearfirst: bool | None = ...,
    ignoretz: bool = ...,
    fuzzy: bool = ...,
    fuzzy_with_tokens: Literal[True],
    default: datetime | None = ...,
    tzinfos: _TzInfos | None = ...,
) -> tuple[datetime, tuple[str, ...]]: ...

class _tzparser:
    class _result(_resultbase):
        __slots__ = ["stdabbr", "stdoffset", "dstabbr", "dstoffset", "start", "end"]
        stdabbr: str | None
        stdoffset: int | None
        dstabbr: str | None
        dstoffset: int | None
        start: _attr
        end: _attr

        class _attr(_resultbase):
            __slots__ = ["month", "week", "weekday", "yday", "jyday", "day", "time"]
            month: int | None
            week: int | None
            weekday: int | None
            yday: int | None
            jyday: int | None
            day: int | None
            time: int | None

        def __init__(self): ...

    def parse(self, tzstr: str | re.Pattern[str]) -> _result | None: ...

DEFAULTTZPARSER: _tzparser

class ParserError(ValueError):
    """
    Exception subclass used for any failure to parse a datetime string.

    This is a subclass of :py:exc:`ValueError`, and should be raised any time
    earlier versions of ``dateutil`` would have raised ``ValueError``.

    .. versionadded:: 2.8.1
    """
    ...
class UnknownTimezoneWarning(RuntimeWarning):
    """
    Raised when the parser finds a timezone it cannot parse into a tzinfo.

    .. versionadded:: 2.7.0
    """
    ...

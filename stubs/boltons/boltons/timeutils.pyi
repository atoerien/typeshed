"""
Python's :mod:`datetime` module provides some of the most complex
and powerful primitives in the Python standard library. Time is
nontrivial, but thankfully its support is first-class in
Python. ``dateutils`` provides some additional tools for working with
time.

Additionally, timeutils provides a few basic utilities for working
with timezones in Python. The Python :mod:`datetime` module's
documentation describes how to create a
:class:`~datetime.datetime`-compatible :class:`~datetime.tzinfo`
subtype. It even provides a few examples.

The following module defines usable forms of the timezones in those
docs, as well as a couple other useful ones, :data:`UTC` (aka GMT) and
:data:`LocalTZ` (representing the local timezone as configured in the
operating system). For timezones beyond these, as well as a higher
degree of accuracy in corner cases, check out `pytz`_ and `dateutil`_.

.. _pytz: https://pypi.python.org/pypi/pytz
.. _dateutil: https://dateutil.readthedocs.io/en/stable/index.html
"""

from collections.abc import Generator
from datetime import date, datetime, timedelta, tzinfo

total_seconds = timedelta.total_seconds

def dt_to_timestamp(dt: datetime) -> int:
    """
    Converts from a :class:`~datetime.datetime` object to an integer
    timestamp, suitable interoperation with :func:`time.time` and
    other `Epoch-based timestamps`.

    .. _Epoch-based timestamps: https://en.wikipedia.org/wiki/Unix_time

    >>> timestamp = int(time.time())
    >>> utc_dt = datetime.fromtimestamp(timestamp, timezone.utc)
    >>> timestamp - dt_to_timestamp(utc_dt)
    0.0

    ``dt_to_timestamp`` supports both timezone-aware and naïve
    :class:`~datetime.datetime` objects. Note that it assumes naïve
    datetime objects are implied UTC, such as those generated with
    :meth:`datetime.datetime.utcnow`. If your datetime objects are
    local time, such as those generated with
    :meth:`datetime.datetime.now`, first convert it using the
    :meth:`datetime.datetime.replace` method with ``tzinfo=``
    :class:`LocalTZ` object in this module, then pass the result of
    that to ``dt_to_timestamp``.
    """
    ...
def isoparse(iso_str: str) -> datetime:
    """
    Parses the limited subset of `ISO8601-formatted time`_ strings as
    returned by :meth:`datetime.datetime.isoformat`.

    >>> epoch_dt = datetime.fromtimestamp(0, timezone.utc).replace(tzinfo=None)
    >>> iso_str = epoch_dt.isoformat()
    >>> print(iso_str)
    1970-01-01T00:00:00
    >>> isoparse(iso_str)
    datetime.datetime(1970, 1, 1, 0, 0)

    >>> utcnow = datetime.now(timezone.utc).replace(tzinfo=None)
    >>> utcnow == isoparse(utcnow.isoformat())
    True

    For further datetime parsing, see the `iso8601`_ package for strict
    ISO parsing and `dateutil`_ package for loose parsing and more.

    .. _ISO8601-formatted time: https://en.wikipedia.org/wiki/ISO_8601
    .. _iso8601: https://pypi.python.org/pypi/iso8601
    .. _dateutil: https://pypi.python.org/pypi/python-dateutil
    """
    ...
def parse_timedelta(text: str) -> timedelta:
    """
    Robustly parses a short text description of a time period into a
    :class:`datetime.timedelta`. Supports weeks, days, hours, minutes,
    and seconds, with or without decimal points:

    Args:
        text (str): Text to parse.
    Returns:
        datetime.timedelta
    Raises:
        ValueError: on parse failure.

    >>> parse_td('1d 2h 3.5m 0s') == timedelta(days=1, seconds=7410)
    True

    Also supports full words and whitespace.

    >>> parse_td('2 weeks 1 day') == timedelta(days=15)
    True

    Negative times are supported, too:

    >>> parse_td('-1.5 weeks 3m 20s') == timedelta(days=-11, seconds=43400)
    True
    """
    ...

parse_td = parse_timedelta

def decimal_relative_time(
    d: datetime, other: datetime | None = None, ndigits: int = 0, cardinalize: bool = True
) -> tuple[float, str]: ...
def relative_time(d: datetime, other: datetime | None = None, ndigits: int = 0) -> str: ...
def strpdate(string: str, format: str) -> date: ...
def daterange(start: date, stop: date, step: int = 1, inclusive: bool = False) -> Generator[date]: ...

ZERO: timedelta
HOUR: timedelta

class ConstantTZInfo(tzinfo):
    """
    A :class:`~datetime.tzinfo` subtype whose *offset* remains constant
    (no daylight savings).

    Args:
        name (str): Name of the timezone.
        offset (datetime.timedelta): Offset of the timezone.
    """
    name: str
    offset: timedelta
    def __init__(self, name: str = "ConstantTZ", offset: timedelta = ...) -> None: ...
    @property
    def utcoffset_hours(self) -> str: ...
    def utcoffset(self, dt: datetime | None) -> timedelta: ...
    def tzname(self, dt: datetime | None) -> str: ...
    def dst(self, dt: datetime | None) -> timedelta: ...

UTC: ConstantTZInfo
EPOCH_AWARE: datetime

class LocalTZInfo(tzinfo):
    """
    The ``LocalTZInfo`` type takes data available in the time module
    about the local timezone and makes a practical
    :class:`datetime.tzinfo` to represent the timezone settings of the
    operating system.

    For a more in-depth integration with the operating system, check
    out `tzlocal`_. It builds on `pytz`_ and implements heuristics for
    many versions of major operating systems to provide the official
    ``pytz`` tzinfo, instead of the LocalTZ generalization.

    .. _tzlocal: https://pypi.python.org/pypi/tzlocal
    .. _pytz: https://pypi.python.org/pypi/pytz
    """
    def is_dst(self, dt: datetime) -> bool: ...
    def utcoffset(self, dt: datetime) -> timedelta: ...  # type: ignore[override] # Doesn't support None
    def dst(self, dt: datetime) -> timedelta: ...  # type: ignore[override] # Doesn't support None
    def tzname(self, dt: datetime) -> str: ...  # type: ignore[override] # Doesn't support None

LocalTZ: LocalTZInfo
DSTSTART_2007: datetime
DSTEND_2007: datetime
DSTSTART_1987_2006: datetime
DSTEND_1987_2006: datetime
DSTSTART_1967_1986: datetime
DSTEND_1967_1986: datetime

class USTimeZone(tzinfo):
    """
    Copied directly from the Python docs, the ``USTimeZone`` is a
    :class:`datetime.tzinfo` subtype used to create the
    :data:`Eastern`, :data:`Central`, :data:`Mountain`, and
    :data:`Pacific` tzinfo types.
    """
    stdoffset: timedelta
    reprname: str
    stdname: str
    dstname: str
    def __init__(self, hours: int, reprname: str, stdname: str, dstname: str) -> None: ...
    def tzname(self, dt: datetime | None) -> str: ...
    def utcoffset(self, dt: datetime | None) -> timedelta: ...
    def dst(self, dt: datetime | None) -> timedelta: ...

Eastern: USTimeZone
Central: USTimeZone
Mountain: USTimeZone
Pacific: USTimeZone

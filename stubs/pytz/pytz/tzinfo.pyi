"""Base classes and helpers for building zone specific tzinfo classes"""

import datetime
from abc import abstractmethod
from typing import Any, overload

class BaseTzInfo(datetime.tzinfo):
    _utcoffset: datetime.timedelta | None
    _tzname: str | None
    zone: str | None  # Actually None but should be set on concrete subclasses
    # The following abstract methods don't exist in the implementation, but
    # are implemented by all sub-classes.
    @abstractmethod
    def localize(self, dt: datetime.datetime, is_dst: bool | None = ...) -> datetime.datetime: ...
    @abstractmethod
    def normalize(self, dt: datetime.datetime) -> datetime.datetime: ...
    @abstractmethod
    def tzname(self, dt: datetime.datetime | None, /) -> str:
        """datetime -> string name of time zone."""
        ...
    @abstractmethod
    def utcoffset(self, dt: datetime.datetime | None, /) -> datetime.timedelta | None:
        """datetime -> timedelta showing offset from UTC, negative values indicating West of UTC"""
        ...
    @abstractmethod
    def dst(self, dt: datetime.datetime | None, /) -> datetime.timedelta | None:
        """datetime -> DST offset as timedelta positive east of UTC."""
        ...

class StaticTzInfo(BaseTzInfo):
    """
    A timezone that has a constant offset from UTC

    These timezones are rare, as most locations have changed their
    offset at some point in their history
    """
    def fromutc(self, dt: datetime.datetime) -> datetime.datetime:
        """See datetime.tzinfo.fromutc"""
        ...
    def localize(self, dt: datetime.datetime, is_dst: bool | None = False) -> datetime.datetime:
        """Convert naive time to local time"""
        ...
    def normalize(self, dt: datetime.datetime, is_dst: bool | None = False) -> datetime.datetime:
        """
        Correct the timezone information on the given datetime.

        This is normally a no-op, as StaticTzInfo timezones never have
        ambiguous cases to correct:

        >>> from pytz import timezone
        >>> gmt = timezone('GMT')
        >>> isinstance(gmt, StaticTzInfo)
        True
        >>> dt = datetime(2011, 5, 8, 1, 2, 3, tzinfo=gmt)
        >>> gmt.normalize(dt) is dt
        True

        The supported method of converting between timezones is to use
        datetime.astimezone(). Currently normalize() also works:

        >>> la = timezone('America/Los_Angeles')
        >>> dt = la.localize(datetime(2011, 5, 7, 1, 2, 3))
        >>> fmt = '%Y-%m-%d %H:%M:%S %Z (%z)'
        >>> gmt.normalize(dt).strftime(fmt)
        '2011-05-07 08:02:03 GMT (+0000)'
        """
        ...
    def tzname(self, dt: datetime.datetime | None, is_dst: bool | None = None) -> str:
        """
        See datetime.tzinfo.tzname

        is_dst is ignored for StaticTzInfo, and exists only to
        retain compatibility with DstTzInfo.
        """
        ...
    def utcoffset(self, dt: datetime.datetime | None, is_dst: bool | None = None) -> datetime.timedelta:
        """
        See datetime.tzinfo.utcoffset

        is_dst is ignored for StaticTzInfo, and exists only to
        retain compatibility with DstTzInfo.
        """
        ...
    def dst(self, dt: datetime.datetime | None, is_dst: bool | None = None) -> datetime.timedelta:
        """
        See datetime.tzinfo.dst

        is_dst is ignored for StaticTzInfo, and exists only to
        retain compatibility with DstTzInfo.
        """
        ...

class DstTzInfo(BaseTzInfo):
    """
    A timezone that has a variable offset from UTC

    The offset might change if daylight saving time comes into effect,
    or at a point in history when the region decides to change their
    timezone definition.
    """
    def __init__(self, _inf: Any = None, _tzinfos: Any = None) -> None: ...
    def fromutc(self, dt: datetime.datetime) -> datetime.datetime: ...
    def localize(self, dt: datetime.datetime, is_dst: bool | None = False) -> datetime.datetime: ...
    def normalize(self, dt: datetime.datetime) -> datetime.datetime: ...
    def tzname(self, dt: datetime.datetime | None, is_dst: bool | None = None) -> str: ...

    # https://github.com/python/mypy/issues/12379
    @overload  # type: ignore[override]
    def utcoffset(self, dt: None, is_dst: bool | None = None) -> None:
        """
        See datetime.tzinfo.utcoffset

        The is_dst parameter may be used to remove ambiguity during DST
        transitions.

        >>> from pytz import timezone
        >>> tz = timezone('America/St_Johns')
        >>> ambiguous = datetime(2009, 10, 31, 23, 30)

        >>> str(tz.utcoffset(ambiguous, is_dst=False))
        '-1 day, 20:30:00'

        >>> str(tz.utcoffset(ambiguous, is_dst=True))
        '-1 day, 21:30:00'

        >>> try:
        ...     tz.utcoffset(ambiguous)
        ... except AmbiguousTimeError:
        ...     print('Ambiguous')
        Ambiguous
        """
        ...
    @overload
    def utcoffset(self, dt: datetime.datetime, is_dst: bool | None = None) -> datetime.timedelta: ...

    def dst(self, dt: datetime.datetime | None, is_dst: bool | None = None) -> datetime.timedelta | None: ...

__all__: list[str] = []

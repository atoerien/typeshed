"""
win32timezone:
    Module for handling datetime.tzinfo time zones using the windows
registry for time zone information.  The time zone names are dependent
on the registry entries defined by the operating system.

    This module may be tested using the doctest module.

    Written by Jason R. Coombs (jaraco@jaraco.com).
    Copyright © 2003-2012.
    All Rights Reserved.

    This module is licensed for use in Mark Hammond's pywin32
library under the same terms as the pywin32 library.

    To use this time zone module with the datetime module, simply pass
the TimeZoneInfo object to the datetime constructor.  For example,

>>> import win32timezone, datetime
>>> assert 'Mountain Standard Time' in win32timezone.TimeZoneInfo.get_sorted_time_zone_names()
>>> MST = win32timezone.TimeZoneInfo('Mountain Standard Time')
>>> now = datetime.datetime.now(MST)

    The now object is now a time-zone aware object, and daylight savings-
aware methods may be called on it.

>>> now.utcoffset() in (datetime.timedelta(-1, 61200), datetime.timedelta(-1, 64800))
True

(note that the result of utcoffset call will be different based on when now was
generated, unless standard time is always used)

>>> now = datetime.datetime.now(win32timezone.TimeZoneInfo('Mountain Standard Time', True))
>>> now.utcoffset()
datetime.timedelta(days=-1, seconds=61200)

>>> aug2 = datetime.datetime(2003, 8, 2, tzinfo = MST)
>>> tuple(aug2.utctimetuple())
(2003, 8, 2, 6, 0, 0, 5, 214, 0)
>>> nov2 = datetime.datetime(2003, 11, 25, tzinfo = MST)
>>> tuple(nov2.utctimetuple())
(2003, 11, 25, 7, 0, 0, 1, 329, 0)

To convert from one timezone to another, just use the astimezone method.

>>> aug2.isoformat()
'2003-08-02T00:00:00-06:00'
>>> aug2est = aug2.astimezone(win32timezone.TimeZoneInfo('Eastern Standard Time'))
>>> aug2est.isoformat()
'2003-08-02T02:00:00-04:00'

calling the displayName member will return the display name as set in the
registry.

>>> est = win32timezone.TimeZoneInfo('Eastern Standard Time')
>>> str(est.displayName)
'(UTC-05:00) Eastern Time (US & Canada)'

>>> gmt = win32timezone.TimeZoneInfo('GMT Standard Time', True)
>>> str(gmt.displayName)
'(UTC+00:00) Dublin, Edinburgh, Lisbon, London'

To get the complete list of available time zone keys,
>>> zones = win32timezone.TimeZoneInfo.get_all_time_zones()

If you want to get them in an order that's sorted longitudinally
>>> zones = win32timezone.TimeZoneInfo.get_sorted_time_zones()

TimeZoneInfo now supports being pickled and comparison
>>> import pickle
>>> tz = win32timezone.TimeZoneInfo('China Standard Time')
>>> tz == pickle.loads(pickle.dumps(tz))
True

It's possible to construct a TimeZoneInfo from a TimeZoneDescription
including the currently-defined zone.
>>> code, info = win32timezone.TimeZoneDefinition.current()
>>> tz = win32timezone.TimeZoneInfo(info, not code)
>>> tz == pickle.loads(pickle.dumps(tz))
True

Although it's easier to use TimeZoneInfo.local() to get the local info
>>> tz == TimeZoneInfo.local()
True

>>> aest = win32timezone.TimeZoneInfo('AUS Eastern Standard Time')
>>> est = win32timezone.TimeZoneInfo('E. Australia Standard Time')
>>> dt = datetime.datetime(2006, 11, 11, 1, 0, 0, tzinfo = aest)
>>> estdt = dt.astimezone(est)
>>> estdt.strftime('%Y-%m-%d %H:%M:%S')
'2006-11-11 00:00:00'

>>> dt = datetime.datetime(2007, 1, 12, 1, 0, 0, tzinfo = aest)
>>> estdt = dt.astimezone(est)
>>> estdt.strftime('%Y-%m-%d %H:%M:%S')
'2007-01-12 00:00:00'

>>> dt = datetime.datetime(2007, 6, 13, 1, 0, 0, tzinfo = aest)
>>> estdt = dt.astimezone(est)
>>> estdt.strftime('%Y-%m-%d %H:%M:%S')
'2007-06-13 01:00:00'

Microsoft now has a patch for handling time zones in 2007 (see
https://learn.microsoft.com/en-us/troubleshoot/windows-client/system-management-components/daylight-saving-time-help-support)

As a result, patched systems will give an incorrect result for
dates prior to the designated year except for Vista and its
successors, which have dynamic time zone support.
>>> nov2_pre_change = datetime.datetime(2003, 11, 2, tzinfo = MST)
>>> old_response = (2003, 11, 2, 7, 0, 0, 6, 306, 0)
>>> incorrect_patch_response = (2003, 11, 2, 6, 0, 0, 6, 306, 0)
>>> pre_response = nov2_pre_change.utctimetuple()
>>> pre_response in (old_response, incorrect_patch_response)
True

Furthermore, unpatched systems pre-Vista will give an incorrect
result for dates after 2007.
>>> nov2_post_change = datetime.datetime(2007, 11, 2, tzinfo = MST)
>>> incorrect_unpatched_response = (2007, 11, 2, 7, 0, 0, 4, 306, 0)
>>> new_response = (2007, 11, 2, 6, 0, 0, 4, 306, 0)
>>> post_response = nov2_post_change.utctimetuple()
>>> post_response in (new_response, incorrect_unpatched_response)
True


There is a function you can call to get some capabilities of the time
zone data.
>>> caps = GetTZCapabilities()
>>> isinstance(caps, dict)
True
>>> 'MissingTZPatch' in caps
True
>>> 'DynamicTZSupport' in caps
True

>>> both_dates_correct = (pre_response == old_response and post_response == new_response)
>>> old_dates_wrong = (pre_response == incorrect_patch_response)
>>> new_dates_wrong = (post_response == incorrect_unpatched_response)

>>> caps['DynamicTZSupport'] == both_dates_correct
True

>>> (not caps['DynamicTZSupport'] and caps['MissingTZPatch']) == new_dates_wrong
True

>>> (not caps['DynamicTZSupport'] and not caps['MissingTZPatch']) == old_dates_wrong
True

This test helps ensure language support for unicode characters
>>> x = TIME_ZONE_INFORMATION(0, 'français')


Test conversion from one time zone to another at a DST boundary
===============================================================

>>> tz_hi = TimeZoneInfo('Hawaiian Standard Time')
>>> tz_pac = TimeZoneInfo('Pacific Standard Time')
>>> time_before = datetime.datetime(2011, 11, 5, 15, 59, 59, tzinfo=tz_hi)
>>> tz_hi.utcoffset(time_before)
datetime.timedelta(days=-1, seconds=50400)
>>> tz_hi.dst(time_before)
datetime.timedelta(0)

Hawaii doesn't need dynamic TZ info
>>> getattr(tz_hi, 'dynamicInfo', None)

Here's a time that gave some trouble as reported in #3523104
because one minute later, the equivalent UTC time changes from DST
in the U.S.
>>> dt_hi = datetime.datetime(2011, 11, 5, 15, 59, 59, 0, tzinfo=tz_hi)
>>> dt_hi.timetuple()
time.struct_time(tm_year=2011, tm_mon=11, tm_mday=5, tm_hour=15, tm_min=59, tm_sec=59, tm_wday=5, tm_yday=309, tm_isdst=0)
>>> dt_hi.utctimetuple()
time.struct_time(tm_year=2011, tm_mon=11, tm_mday=6, tm_hour=1, tm_min=59, tm_sec=59, tm_wday=6, tm_yday=310, tm_isdst=0)

Convert the time to pacific time.
>>> dt_pac = dt_hi.astimezone(tz_pac)
>>> dt_pac.timetuple()
time.struct_time(tm_year=2011, tm_mon=11, tm_mday=5, tm_hour=18, tm_min=59, tm_sec=59, tm_wday=5, tm_yday=309, tm_isdst=1)

Notice that the UTC time is almost 2am.
>>> dt_pac.utctimetuple()
time.struct_time(tm_year=2011, tm_mon=11, tm_mday=6, tm_hour=1, tm_min=59, tm_sec=59, tm_wday=6, tm_yday=310, tm_isdst=0)

Now do the same tests one minute later in Hawaii.
>>> time_after = datetime.datetime(2011, 11, 5, 16, 0, 0, 0, tzinfo=tz_hi)
>>> tz_hi.utcoffset(time_after)
datetime.timedelta(days=-1, seconds=50400)
>>> tz_hi.dst(time_before)
datetime.timedelta(0)

>>> dt_hi = datetime.datetime(2011, 11, 5, 16, 0, 0, 0, tzinfo=tz_hi)
>>> print(dt_hi.timetuple())
time.struct_time(tm_year=2011, tm_mon=11, tm_mday=5, tm_hour=16, tm_min=0, tm_sec=0, tm_wday=5, tm_yday=309, tm_isdst=0)
>>> print(dt_hi.utctimetuple())
time.struct_time(tm_year=2011, tm_mon=11, tm_mday=6, tm_hour=2, tm_min=0, tm_sec=0, tm_wday=6, tm_yday=310, tm_isdst=0)

According to the docs, this is what astimezone does.
>>> utc = (dt_hi - dt_hi.utcoffset()).replace(tzinfo=tz_pac)
>>> utc
datetime.datetime(2011, 11, 6, 2, 0, tzinfo=TimeZoneInfo('Pacific Standard Time'))
>>> tz_pac.fromutc(utc) == dt_hi.astimezone(tz_pac)
True
>>> tz_pac.fromutc(utc)
datetime.datetime(2011, 11, 5, 19, 0, tzinfo=TimeZoneInfo('Pacific Standard Time'))

Make sure the converted time is correct.
>>> dt_pac = dt_hi.astimezone(tz_pac)
>>> dt_pac.timetuple()
time.struct_time(tm_year=2011, tm_mon=11, tm_mday=5, tm_hour=19, tm_min=0, tm_sec=0, tm_wday=5, tm_yday=309, tm_isdst=1)
>>> dt_pac.utctimetuple()
time.struct_time(tm_year=2011, tm_mon=11, tm_mday=6, tm_hour=2, tm_min=0, tm_sec=0, tm_wday=6, tm_yday=310, tm_isdst=0)

Check some internal methods
>>> tz_pac._getStandardBias(datetime.datetime(2011, 1, 1))
datetime.timedelta(seconds=28800)
>>> tz_pac._getDaylightBias(datetime.datetime(2011, 1, 1))
datetime.timedelta(seconds=25200)

Test the offsets
>>> offset = tz_pac.utcoffset(datetime.datetime(2011, 11, 6, 2, 0))
>>> offset == datetime.timedelta(hours=-8)
True
>>> dst_offset = tz_pac.dst(datetime.datetime(2011, 11, 6, 2, 0) + offset)
>>> dst_offset == datetime.timedelta(hours=1)
True
>>> (offset + dst_offset) == datetime.timedelta(hours=-7)
True


Test offsets that occur right at the DST changeover
>>> datetime.datetime.utcfromtimestamp(1320570000).replace(
...     tzinfo=TimeZoneInfo.utc()).astimezone(tz_pac)
datetime.datetime(2011, 11, 6, 1, 0, tzinfo=TimeZoneInfo('Pacific Standard Time'))
"""

import datetime
from _operator import _SupportsComparison
from _typeshed import Incomplete, SupportsKeysAndGetItem
from collections.abc import Callable, Iterable, Mapping
from logging import Logger
from typing import ClassVar, TypeVar, overload, type_check_only
from typing_extensions import Self

_RangeMapKT = TypeVar("_RangeMapKT", bound=_SupportsComparison)

_T = TypeVar("_T")
_VT = TypeVar("_VT")

log: Logger

class _SimpleStruct:
    def __init__(self, *args, **kw) -> None: ...
    def field_names(self) -> list[str]: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

class SYSTEMTIME(_SimpleStruct): ...
class TIME_ZONE_INFORMATION(_SimpleStruct): ...
class DYNAMIC_TIME_ZONE_INFORMATION(_SimpleStruct): ...

class TimeZoneDefinition(DYNAMIC_TIME_ZONE_INFORMATION):
    """
    A time zone definition class based on the win32
    DYNAMIC_TIME_ZONE_INFORMATION structure.

    Describes a bias against UTC (bias), and two dates at which a separate
    additional bias applies (standard_bias and daylight_bias).
    """
    def __init__(self, *args, **kwargs) -> None:
        """
        >>> test_args = [1] * 44

        Try to construct a TimeZoneDefinition from:

        a) [DYNAMIC_]TIME_ZONE_INFORMATION args
        >>> TimeZoneDefinition(*test_args).bias
        datetime.timedelta(seconds=60)

        b) another TimeZoneDefinition or [DYNAMIC_]TIME_ZONE_INFORMATION
        >>> TimeZoneDefinition(TimeZoneDefinition(*test_args)).bias
        datetime.timedelta(seconds=60)
        >>> TimeZoneDefinition(DYNAMIC_TIME_ZONE_INFORMATION(*test_args)).bias
        datetime.timedelta(seconds=60)
        >>> TimeZoneDefinition(TIME_ZONE_INFORMATION(*test_args)).bias
        datetime.timedelta(seconds=60)

        c) a byte structure (using _from_bytes)
        >>> TimeZoneDefinition(bytes(test_args)).bias
        datetime.timedelta(days=11696, seconds=46140)
        """
        ...
    # TIME_ZONE_INFORMATION fields as obtained by __getattribute__
    bias: datetime.timedelta
    standard_name: str
    standard_start: SYSTEMTIME
    standard_bias: datetime.timedelta
    daylight_name: str
    daylight_start: SYSTEMTIME
    daylight_bias: datetime.timedelta
    def __getattribute__(self, attr: str): ...
    @classmethod
    def current(cls) -> tuple[int, Self]:
        """Windows Platform SDK GetTimeZoneInformation"""
        ...
    def set(self) -> None: ...
    def copy(self) -> Self: ...
    def locate_daylight_start(self, year) -> datetime.datetime: ...
    def locate_standard_start(self, year) -> datetime.datetime: ...

class TimeZoneInfo(datetime.tzinfo):
    """
    Main class for handling Windows time zones.
    Usage:
        TimeZoneInfo(<Time Zone Standard Name>, [<Fix Standard Time>])

    If <Fix Standard Time> evaluates to True, daylight savings time is
    calculated in the same way as standard time.

    >>> tzi = TimeZoneInfo('Pacific Standard Time')
    >>> march31 = datetime.datetime(2000,3,31)

    We know that time zone definitions haven't changed from 2007
    to 2012, so regardless of whether dynamic info is available,
    there should be consistent results for these years.
    >>> subsequent_years = [march31.replace(year=year)
    ...     for year in range(2007, 2013)]
    >>> offsets = set(tzi.utcoffset(year) for year in subsequent_years)
    >>> len(offsets)
    1

    Cannot create a `TimeZoneInfo` with an invalid name.
    >>> TimeZoneInfo('Does not exist')
    Traceback (most recent call last):
    ...
    ValueError: Timezone Name 'Does not exist' not found
    >>> TimeZoneInfo(None)
    Traceback (most recent call last):
    ...
    ValueError: subkey name cannot be empty
    >>> TimeZoneInfo("")
    Traceback (most recent call last):
    ...
    ValueError: subkey name cannot be empty
    """
    tzRegKey: ClassVar[str]
    timeZoneName: str
    fixedStandardTime: bool
    def __init__(self, param: str | TimeZoneDefinition, fix_standard_time: bool = False) -> None: ...
    @overload  # type: ignore[override] # Split definition into overrides
    def tzname(self, dt: datetime.datetime) -> str:
        """
        >>> MST = TimeZoneInfo('Mountain Standard Time')
        >>> MST.tzname(datetime.datetime(2003, 8, 2))
        'Mountain Daylight Time'
        >>> MST.tzname(datetime.datetime(2003, 11, 25))
        'Mountain Standard Time'
        >>> MST.tzname(None)
        """
        ...
    @overload
    def tzname(self, dt: None) -> None:
        """
        >>> MST = TimeZoneInfo('Mountain Standard Time')
        >>> MST.tzname(datetime.datetime(2003, 8, 2))
        'Mountain Daylight Time'
        >>> MST.tzname(datetime.datetime(2003, 11, 25))
        'Mountain Standard Time'
        >>> MST.tzname(None)
        """
        ...
    def getWinInfo(self, targetYear: int) -> TimeZoneDefinition:
        """
        Return the most relevant "info" for this time zone
        in the target year.
        """
        ...
    @overload  # type: ignore[override] # False-positive, our overload covers all base types
    def utcoffset(self, dt: None) -> None:
        """Calculates the utcoffset according to the datetime.tzinfo spec"""
        ...
    @overload
    def utcoffset(self, dt: datetime.datetime) -> datetime.timedelta:
        """Calculates the utcoffset according to the datetime.tzinfo spec"""
        ...
    @overload  # type: ignore[override] # False-positive, our overload covers all base types
    def dst(self, dt: None) -> None:
        """
        Calculate the daylight savings offset according to the
        datetime.tzinfo spec.
        """
        ...
    @overload
    def dst(self, dt: datetime.datetime) -> datetime.timedelta:
        """
        Calculate the daylight savings offset according to the
        datetime.tzinfo spec.
        """
        ...
    def GetDSTStartTime(self, year: int) -> datetime.datetime:
        """Given a year, determines the time when daylight savings time starts"""
        ...
    def GetDSTEndTime(self, year: int) -> datetime.datetime:
        """Given a year, determines the time when daylight savings ends."""
        ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    @classmethod
    def local(cls) -> Self:
        """
        Returns the local time zone as defined by the operating system in the
        registry.
        >>> localTZ = TimeZoneInfo.local()
        >>> now_local = datetime.datetime.now(localTZ)
        >>> now_UTC = datetime.datetime.utcnow()  # deprecated
        >>> (now_UTC - now_local) < datetime.timedelta(seconds = 5)
        Traceback (most recent call last):
        ...
        TypeError: can't subtract offset-naive and offset-aware datetimes

        >>> now_UTC = now_UTC.replace(tzinfo = TimeZoneInfo('GMT Standard Time', True))

        Now one can compare the results of the two offset aware values
        >>> (now_UTC - now_local) < datetime.timedelta(seconds = 5)
        True

        Or use the newer `datetime.timezone.utc`
        >>> now_UTC = datetime.datetime.now(datetime.timezone.utc)
        >>> (now_UTC - now_local) < datetime.timedelta(seconds = 5)
        True
        """
        ...
    @classmethod
    def utc(cls) -> Self:
        """
        Returns a time-zone representing UTC.

        Same as TimeZoneInfo('GMT Standard Time', True) but caches the result
        for performance.

        >>> isinstance(TimeZoneInfo.utc(), TimeZoneInfo)
        True
        """
        ...
    @staticmethod
    def get_sorted_time_zone_names() -> list[str]:
        """
        Return a list of time zone names that can
        be used to initialize TimeZoneInfo instances.
        """
        ...
    @staticmethod
    def get_all_time_zones() -> list[TimeZoneInfo]: ...
    @staticmethod
    def get_sorted_time_zones(key: Incomplete | None = ...):
        """
        Return the time zones sorted by some key.
        key must be a function that takes a TimeZoneInfo object and returns
        a value suitable for sorting on.
        The key defaults to the bias (descending), as is done in Windows
        (see https://web.archive.org/web/20130723075340/http://blogs.msdn.com/b/michkap/archive/2006/12/22/1350684.aspx)
        """
        ...

def utcnow() -> datetime.datetime:
    """
    Return the UTC time now with timezone awareness as enabled
    by this module
    >>> now = utcnow()

    >>> (now - datetime.datetime.now(datetime.timezone.utc)) < datetime.timedelta(seconds = 5)
    True
    >>> type(now.tzinfo) is TimeZoneInfo
    True
    """
    ...
def now() -> datetime.datetime:
    """
    Return the local time now with timezone awareness as enabled
    by this module
    >>> now_local = now()

    >>> (now_local - datetime.datetime.now(datetime.timezone.utc)) < datetime.timedelta(seconds = 5)
    True
    >>> type(now_local.tzinfo) is TimeZoneInfo
    True
    """
    ...
def GetTZCapabilities() -> dict[str, bool]:
    """
    Run a few known tests to determine the capabilities of
    the time zone database on this machine.
    Note Dynamic Time Zone support is not available on any
    platform at this time; this
    is a limitation of this library, not the platform.
    """
    ...

class DLLHandleCache:
    def __getitem__(self, filename: str) -> int: ...

DLLCache: DLLHandleCache

def resolveMUITimeZone(spec: str) -> str | None:
    """
    Resolve a multilingual user interface resource for the time zone name

    spec should be of the format @path,-stringID[;comment]
    see https://learn.microsoft.com/en-ca/windows/win32/api/timezoneapi/ns-timezoneapi-time_zone_information
    for details

    >>> import sys
    >>> result = resolveMUITimeZone('@tzres.dll,-110')
    >>> expectedResultType = [type(None),str][sys.getwindowsversion() >= (6,)]
    >>> type(result) is expectedResultType
    True
    """
    ...

class RangeMap(dict[_RangeMapKT, _VT]):
    """
    A dictionary-like object that uses the keys as bounds for a range.
    Inclusion of the value for that range is determined by the
    key_match_comparator, which defaults to less-than-or-equal.
    A value is returned for a key if it is the first key that matches in
    the sorted list of keys.

    One may supply keyword parameters to be passed to the sort function used
    to sort keys (i.e. key, reverse) as sort_params.

    Create a map that maps 1-3 -> 'a', 4-6 -> 'b'

    >>> r = RangeMap({3: 'a', 6: 'b'})  # boy, that was easy
    >>> r[1], r[2], r[3], r[4], r[5], r[6]
    ('a', 'a', 'a', 'b', 'b', 'b')

    Even float values should work so long as the comparison operator
    supports it.

    >>> r[4.5]
    'b'

    Notice that the way rangemap is defined, it must be open-ended
    on one side.

    >>> r[0]
    'a'
    >>> r[-1]
    'a'

    One can close the open-end of the RangeMap by using undefined_value

    >>> r = RangeMap({0: RangeMap.undefined_value, 3: 'a', 6: 'b'})
    >>> r[0]
    Traceback (most recent call last):
    ...
    KeyError: 0

    One can get the first or last elements in the range by using RangeMap.Item

    >>> last_item = RangeMap.Item(-1)
    >>> r[last_item]
    'b'

    .last_item is a shortcut for Item(-1)

    >>> r[RangeMap.last_item]
    'b'

    Sometimes it's useful to find the bounds for a RangeMap

    >>> r.bounds()
    (0, 6)

    RangeMap supports .get(key, default)

    >>> r.get(0, 'not found')
    'not found'

    >>> r.get(7, 'not found')
    'not found'

    One often wishes to define the ranges by their left-most values,
    which requires use of sort params and a key_match_comparator.

    >>> r = RangeMap({1: 'a', 4: 'b'},
    ...     sort_params=dict(reverse=True),
    ...     key_match_comparator=operator.ge)
    >>> r[1], r[2], r[3], r[4], r[5], r[6]
    ('a', 'a', 'a', 'b', 'b', 'b')

    That wasn't nearly as easy as before, so an alternate constructor
    is provided:

    >>> r = RangeMap.left({1: 'a', 4: 'b', 7: RangeMap.undefined_value})
    >>> r[1], r[2], r[3], r[4], r[5], r[6]
    ('a', 'a', 'a', 'b', 'b', 'b')
    """
    sort_params: Mapping[str, Incomplete]
    match: Callable[[_RangeMapKT, _RangeMapKT], bool]
    def __init__(
        self,
        source: SupportsKeysAndGetItem[_RangeMapKT, _VT] | Iterable[tuple[_RangeMapKT, _VT]],
        sort_params: Mapping[str, Incomplete] = {},
        key_match_comparator: Callable[[_RangeMapKT, _RangeMapKT], bool] = ...,
    ) -> None: ...
    @classmethod
    def left(cls, source: SupportsKeysAndGetItem[_RangeMapKT, _VT] | Iterable[tuple[_RangeMapKT, _VT]]) -> Self: ...
    def __getitem__(self, item: _RangeMapKT) -> _VT: ...
    @overload  # type: ignore[override] # Signature simplified over dict and Mapping
    def get(self, key: _RangeMapKT, default: _T) -> _VT | _T:
        """
        Return the value for key if key is in the dictionary, else default.
        If default is not given, it defaults to None, so that this method
        never raises a KeyError.
        """
        ...
    @overload
    def get(self, key: _RangeMapKT, default: None = None) -> _VT | None:
        """
        Return the value for key if key is in the dictionary, else default.
        If default is not given, it defaults to None, so that this method
        never raises a KeyError.
        """
        ...
    def bounds(self) -> tuple[_RangeMapKT, _RangeMapKT]: ...
    @type_check_only
    class RangeValueUndefined: ...

    undefined_value: RangeValueUndefined

    class Item(int):
        """RangeMap Item"""
        ...
    first_item: Item
    last_item: Item

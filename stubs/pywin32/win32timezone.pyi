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

from win32.lib.win32timezone import *

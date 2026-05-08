import datetime
from typing import Any, TypeAlias

from .core import UnitedStates

_HebrewDate: TypeAlias = Any  # from `pyluach.dates` package

class HebrewHolidays:
    hebrew_calendars: dict[int, list[tuple[_HebrewDate | None, datetime.date]]]
    @classmethod
    def get_hebrew_calendar(cls, gregorian_year: int) -> list[tuple[_HebrewDate | None, datetime.date]]:
        """Build and cache the Hebrew calendar for the given Gregorian Year."""
        ...
    @classmethod
    def search_hebrew_calendar(cls, gregorian_year: int, hebrew_month: int, hebrew_day: int) -> datetime.date:
        """Search for a specific Hebrew month and day in the Hebrew calendar."""
        ...
    @classmethod
    def get_rosh_hashanah(cls, year: int) -> datetime.date:
        """Return the gregorian date of the first day of Rosh Hashanah"""
        ...
    @classmethod
    def get_yom_kippur(cls, year: int) -> datetime.date:
        """Return the gregorian date of Yom Kippur."""
        ...

class Florida(UnitedStates):
    """Florida"""
    ...

class FloridaLegal(Florida):
    """Florida Legal Holidays"""
    def __init__(self, *args, **kwargs) -> None: ...

class FloridaCircuitCourts(HebrewHolidays, Florida):
    """Florida Circuits Courts"""
    ...
class FloridaMiamiDade(Florida):
    """Miami-Dade, Florida"""
    ...

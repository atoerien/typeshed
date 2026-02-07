"""Utilities for handling time spans and date ranges."""

from datetime import date, datetime
from typing import TypedDict, overload, type_check_only
from typing_extensions import NotRequired

from dateparser import _Settings

@type_check_only
class _SpanInformation(TypedDict):
    type: str
    direction: str
    matched_text: str
    start_pos: int
    end_pos: int
    number: NotRequired[int]

@overload
def get_week_start(date: datetime, start_of_week: str = "monday") -> datetime:
    """Get the start of the week for a given date."""
    ...
@overload
def get_week_start(date: date, start_of_week: str = "monday") -> date:
    """Get the start of the week for a given date."""
    ...
@overload
def get_week_end(date: datetime, start_of_week: str = "monday") -> datetime:
    """Get the end of the week for a given date."""
    ...
@overload
def get_week_end(date: date, start_of_week: str = "monday") -> date:
    """Get the end of the week for a given date."""
    ...
def detect_time_span(text: str) -> _SpanInformation | None:
    """Detect time span expressions in text and return span information."""
    ...
@overload
def generate_time_span(
    span_info: _SpanInformation, base_date: datetime | None = None, settings: _Settings | None = None
) -> tuple[datetime, datetime]:
    """Generate start and end dates for a time span."""
    ...
@overload
def generate_time_span(
    span_info: _SpanInformation, base_date: date = ..., settings: _Settings | None = None
) -> tuple[date, date]:
    """Generate start and end dates for a time span."""
    ...

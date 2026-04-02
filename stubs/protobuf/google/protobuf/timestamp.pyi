"""Contains the Timestamp helper APIs."""

from datetime import datetime, tzinfo

from google.protobuf.timestamp_pb2 import Timestamp

def from_json_string(value: str) -> Timestamp:
    """
    Parse a RFC 3339 date string format to Timestamp.

    Args:
      value: A date string. Any fractional digits (or none) and any offset are
        accepted as long as they fit into nano-seconds precision. Example of
        accepted format: '1972-01-01T10:00:20.021-05:00'

    Raises:
      ValueError: On parsing problems.
    """
    ...
def from_microseconds(micros: float) -> Timestamp:
    """Converts microseconds since epoch to Timestamp."""
    ...
def from_milliseconds(millis: float) -> Timestamp:
    """Converts milliseconds since epoch to Timestamp."""
    ...
def from_nanoseconds(nanos: float) -> Timestamp:
    """Converts nanoseconds since epoch to Timestamp."""
    ...
def from_seconds(seconds: float) -> Timestamp:
    """Converts seconds since epoch to Timestamp."""
    ...
def from_current_time() -> Timestamp:
    """Converts the current UTC to Timestamp."""
    ...
def to_json_string(ts: Timestamp) -> str:
    """
    Converts Timestamp to RFC 3339 date string format.

    Returns:
      A string converted from timestamp. The string is always Z-normalized
      and uses 3, 6 or 9 fractional digits as required to represent the
      exact time. Example of the return format: '1972-01-01T10:00:20.021Z'
    """
    ...
def to_microseconds(ts: Timestamp) -> int:
    """Converts Timestamp to microseconds since epoch."""
    ...
def to_milliseconds(ts: Timestamp) -> int:
    """Converts Timestamp to milliseconds since epoch."""
    ...
def to_nanoseconds(ts: Timestamp) -> int:
    """Converts Timestamp to nanoseconds since epoch."""
    ...
def to_seconds(ts: Timestamp) -> int:
    """Converts Timestamp to seconds since epoch."""
    ...
def to_datetime(ts: Timestamp, tz: tzinfo | None = None) -> datetime:
    """
    Converts Timestamp to a datetime.

    Args:
      tz: A datetime.tzinfo subclass; defaults to None.

    Returns:
      If tzinfo is None, returns a timezone-naive UTC datetime (with no timezone
      information, i.e. not aware that it's UTC).

      Otherwise, returns a timezone-aware datetime in the input timezone.
    """
    ...

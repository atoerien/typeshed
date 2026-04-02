"""Contains the Duration helper APIs."""

from datetime import timedelta

from google.protobuf.duration_pb2 import Duration

def from_json_string(value: str) -> Duration:
    """
    Converts a string to Duration.

    Args:
      value: A string to be converted. The string must end with 's'. Any
        fractional digits (or none) are accepted as long as they fit into
        precision. For example: "1s", "1.01s", "1.0000001s", "-3.100s"

    Raises:
      ValueError: On parsing problems.
    """
    ...
def from_microseconds(micros: float) -> Duration:
    """Converts microseconds to Duration."""
    ...
def from_milliseconds(millis: float) -> Duration:
    """Converts milliseconds to Duration."""
    ...
def from_nanoseconds(nanos: float) -> Duration:
    """Converts nanoseconds to Duration."""
    ...
def from_seconds(seconds: float) -> Duration:
    """Converts seconds to Duration."""
    ...
def from_timedelta(td: timedelta) -> Duration:
    """Converts timedelta to Duration."""
    ...
def to_json_string(duration: Duration) -> str:
    """
    Converts Duration to string format.

    Returns:
      A string converted from self. The string format will contains
      3, 6, or 9 fractional digits depending on the precision required to
      represent the exact Duration value. For example: "1s", "1.010s",
      "1.000000100s", "-3.100s"
    """
    ...
def to_microseconds(duration: Duration) -> int:
    """Converts a Duration to microseconds."""
    ...
def to_milliseconds(duration: Duration) -> int:
    """Converts a Duration to milliseconds."""
    ...
def to_nanoseconds(duration: Duration) -> int:
    """Converts a Duration to nanoseconds."""
    ...
def to_seconds(duration: Duration) -> int:
    """Converts a Duration to seconds."""
    ...
def to_timedelta(duration: Duration) -> timedelta:
    """Converts Duration to timedelta."""
    ...

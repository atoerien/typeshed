"""
Contains Unknown Fields APIs.

Simple usage example:
  unknown_field_set = UnknownFieldSet(message)
  for unknown_field in unknown_field_set:
    wire_type = unknown_field.wire_type
    field_number = unknown_field.field_number
    data = unknown_field.data
"""

from typing import Any, final

from google.protobuf.message import Message

@final
class UnknownFieldSet:
    def __new__(cls, msg: Message) -> UnknownFieldSet: ...  # noqa: Y034
    def __getitem__(self, index: int, /) -> Any: ...  # Any: internal unknown field object
    def __len__(self) -> int: ...

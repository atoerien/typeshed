"""
Provides type checking routines.

This module defines type checking utilities in the forms of dictionaries:

VALUE_CHECKERS: A dictionary of field types and a value validation object.
TYPE_TO_BYTE_SIZE_FN: A dictionary with field types and a size computing
  function.
TYPE_TO_SERIALIZE_METHOD: A dictionary with field types and serialization
  function.
FIELD_TYPE_TO_WIRE_TYPE: A dictionary with field typed and their
  corresponding wire types.
TYPE_TO_DESERIALIZE_METHOD: A dictionary with field types and deserialization
  function.
"""

from collections.abc import Callable
from typing import Any, Generic, TypeVar

from google.protobuf.descriptor import EnumDescriptor, FieldDescriptor

_T = TypeVar("_T")

def TruncateToFourByteFloat(original: float) -> float: ...
def ToShortestFloat(original: float) -> float:
    """Returns the shortest float that has same value in wire."""
    ...
def GetTypeChecker(
    field: FieldDescriptor,
) -> TypeChecker[Any] | IntValueChecker | EnumValueChecker | UnicodeValueChecker | DoubleValueChecker | BoolValueChecker:
    """
    Returns a type checker for a message field of the specified types.

    Args:
      field: FieldDescriptor object for this field.

    Returns:
      An instance of TypeChecker which can be used to verify the types
      of values assigned to a field of the specified type.
    """
    ...

class TypeChecker(Generic[_T]):
    """
    Type checker used to catch type errors as early as possible
    when the client is setting scalar fields in protocol messages.
    """
    def __init__(self, *acceptable_types: _T): ...
    def CheckValue(self, proposed_value: _T) -> _T:
        """
        Type check the provided value and return it.

        The returned value might have been normalized to another type.
        """
        ...

class TypeCheckerWithDefault(TypeChecker[_T]):
    def __init__(self, default_value: _T, *acceptable_types: _T): ...
    def DefaultValue(self) -> _T: ...

class BoolValueChecker:
    """Type checker used for bool fields."""
    def CheckValue(self, proposed_value: bool) -> bool: ...
    def DefaultValue(self) -> bool: ...

class IntValueChecker:
    """Checker used for integer fields.  Performs type-check and range check."""
    def CheckValue(self, proposed_value: int) -> int: ...
    def DefaultValue(self) -> int: ...

class EnumValueChecker:
    """Checker used for enum fields.  Performs type-check and range check."""
    def __init__(self, enum_type: EnumDescriptor) -> None: ...
    def CheckValue(self, proposed_value: int) -> int: ...
    def DefaultValue(self) -> int: ...

class UnicodeValueChecker:
    """
    Checker used for string fields.

    Always returns a unicode value, even if the input is of type str.
    """
    def CheckValue(self, proposed_value: str) -> str: ...
    def DefaultValue(self) -> str: ...

class Int32ValueChecker(IntValueChecker): ...
class Uint32ValueChecker(IntValueChecker): ...
class Int64ValueChecker(IntValueChecker): ...
class Uint64ValueChecker(IntValueChecker): ...

class DoubleValueChecker:
    """
    Checker used for double fields.

    Performs type-check and range check.
    """
    def CheckValue(self, proposed_value: float) -> float:
        """Check and convert proposed_value to float."""
        ...
    def DefaultValue(self) -> float: ...

class FloatValueChecker(DoubleValueChecker):
    """
    Checker used for float fields.

    Performs type-check and range check.

    Values exceeding a 32-bit float will be converted to inf/-inf.
    """
    def CheckValue(self, proposed_value: float) -> float:
        """Check and convert proposed_value to float."""
        ...

TYPE_TO_BYTE_SIZE_FN: dict[int, Callable[..., int]]
TYPE_TO_ENCODER: dict[int, Callable[..., Any]]
TYPE_TO_SIZER: dict[int, Callable[..., Any]]
TYPE_TO_DECODER: dict[int, Callable[..., Any]]
FIELD_TYPE_TO_WIRE_TYPE: dict[int, int]

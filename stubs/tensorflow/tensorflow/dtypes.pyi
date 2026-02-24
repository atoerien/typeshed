"""Public API for tf._api.v2.dtypes namespace"""

from _typeshed import Incomplete
from abc import ABCMeta
from builtins import bool as _bool
from typing import Any

import numpy as np
from tensorflow._aliases import DTypeLike
from tensorflow.python.framework.dtypes import HandleData

class _DTypeMeta(ABCMeta): ...

class DType(metaclass=_DTypeMeta):
    __slots__ = ["_handle_data"]
    def __init__(self, type_enum: int, handle_data: HandleData | None = None) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def as_numpy_dtype(self) -> type[np.number[Any]]:
        """Returns a Python `type` object based on this `DType`."""
        ...
    @property
    def is_numpy_compatible(self) -> _bool:
        """Returns whether this data type has a compatible NumPy data type."""
        ...
    @property
    def is_bool(self) -> _bool:
        """Returns whether this is a boolean data type."""
        ...
    @property
    def is_floating(self) -> _bool:
        """Returns whether this is a (non-quantized, real) floating point type."""
        ...
    @property
    def is_integer(self) -> _bool:
        """Returns whether this is a (non-quantized) integer type."""
        ...
    @property
    def is_quantized(self) -> _bool:
        """Returns whether this is a quantized data type."""
        ...
    @property
    def is_unsigned(self) -> _bool:
        """
        Returns whether this type is unsigned.

        Non-numeric, unordered, and quantized types are not considered unsigned, and
        this function returns `False`.
        """
        ...
    def __getattr__(self, name: str) -> Incomplete: ...

bool: DType
complex128: DType
complex64: DType
bfloat16: DType
float16: DType
half: DType
float32: DType
float64: DType
double: DType
int8: DType
int16: DType
int32: DType
int64: DType
uint8: DType
uint16: DType
uint32: DType
uint64: DType
qint8: DType
qint16: DType
qint32: DType
quint8: DType
quint16: DType
string: DType

def as_dtype(type_value: DTypeLike) -> DType:
    """
    Converts the given `type_value` to a `tf.DType`.

    Inputs can be existing `tf.DType` objects, a [`DataType`
    enum](https://www.tensorflow.org/code/tensorflow/core/framework/types.proto),
    a string type name, or a
    [`numpy.dtype`](https://numpy.org/doc/stable/reference/generated/numpy.dtype.html).

    Examples:
    >>> tf.as_dtype(2)  # Enum value for float64.
    tf.float64

    >>> tf.as_dtype('float')
    tf.float32

    >>> tf.as_dtype(np.int32)
    tf.int32

    Note: `DType` values are interned (i.e. a single instance of each dtype is
    stored in a map). When passed a new `DType` object, `as_dtype` always returns
    the interned value.

    Args:
      type_value: A value that can be converted to a `tf.DType` object.

    Returns:
      A `DType` corresponding to `type_value`.

    Raises:
      TypeError: If `type_value` cannot be converted to a `DType`.
    """
    ...
def __getattr__(name: str): ...  # incomplete module

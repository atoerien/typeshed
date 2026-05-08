"""Public API for tf._api.v2.sparse namespace"""

from _typeshed import Incomplete
from abc import ABCMeta
from typing import TypeAlias

from tensorflow import Tensor, TensorShape
from tensorflow._aliases import TensorCompatible
from tensorflow.dtypes import DType

_SparseTensorCompatible: TypeAlias = TensorCompatible | SparseTensor

class SparseTensor(metaclass=ABCMeta):
    """
    Represents a sparse tensor.

    TensorFlow represents a sparse tensor as three separate dense tensors:
    `indices`, `values`, and `dense_shape`.  In Python, the three tensors are
    collected into a `SparseTensor` class for ease of use.  If you have separate
    `indices`, `values`, and `dense_shape` tensors, wrap them in a `SparseTensor`
    object before passing to the ops below.

    Concretely, the sparse tensor `SparseTensor(indices, values, dense_shape)`
    comprises the following components, where `N` and `ndims` are the number
    of values and number of dimensions in the `SparseTensor`, respectively:

    * `indices`: A 2-D int64 tensor of shape `[N, ndims]`, which specifies the
      indices of the elements in the sparse tensor that contain nonzero values
      (elements are zero-indexed). For example, `indices=[[1,3], [2,4]]` specifies
      that the elements with indexes of [1,3] and [2,4] have nonzero values.

    * `values`: A 1-D tensor of any type and shape `[N]`, which supplies the
      values for each element in `indices`. For example, given `indices=[[1,3],
      [2,4]]`, the parameter `values=[18, 3.6]` specifies that element [1,3] of
      the sparse tensor has a value of 18, and element [2,4] of the tensor has a
      value of 3.6.

    * `dense_shape`: A 1-D int64 tensor of shape `[ndims]`, which specifies the
      dense_shape of the sparse tensor. Takes a list indicating the number of
      elements in each dimension. For example, `dense_shape=[3,6]` specifies a
      two-dimensional 3x6 tensor, `dense_shape=[2,3,4]` specifies a
      three-dimensional 2x3x4 tensor, and `dense_shape=[9]` specifies a
      one-dimensional tensor with 9 elements.

    The corresponding dense tensor satisfies:

    ```python
    dense.shape = dense_shape
    dense[tuple(indices[i])] = values[i]
    ```

    By convention, `indices` should be sorted in row-major order (or equivalently
    lexicographic order on the tuples `indices[i]`). This is not enforced when
    `SparseTensor` objects are constructed, but most ops assume correct ordering.
    If the ordering of sparse tensor `st` is wrong, a fixed version can be
    obtained by calling `tf.sparse.reorder(st)`.

    Example: The sparse tensor

    ```python
    SparseTensor(indices=[[0, 0], [1, 2]], values=[1, 2], dense_shape=[3, 4])
    ```

    represents the dense tensor

    ```python
    [[1, 0, 0, 0]
     [0, 0, 2, 0]
     [0, 0, 0, 0]]
    ```
    """
    @property
    def indices(self) -> Tensor:
        """
        The indices of non-zero values in the represented dense tensor.

        Returns:
          A 2-D Tensor of int64 with dense_shape `[N, ndims]`, where `N` is the
            number of non-zero values in the tensor, and `ndims` is the rank.
        """
        ...
    @property
    def values(self) -> Tensor:
        """
        The non-zero values in the represented dense tensor.

        Returns:
          A 1-D Tensor of any data type.
        """
        ...
    @property
    def dense_shape(self) -> Tensor:
        """A 1-D Tensor of int64 representing the shape of the dense tensor."""
        ...
    @property
    def shape(self) -> TensorShape:
        """
        Get the `TensorShape` representing the shape of the dense tensor.

        Returns:
          A `TensorShape` object.
        """
        ...
    @property
    def dtype(self) -> DType:
        """The `DType` of elements in this tensor."""
        ...
    name: str
    def __init__(self, indices: TensorCompatible, values: TensorCompatible, dense_shape: TensorCompatible) -> None:
        """
        Creates a `SparseTensor`.

        Args:
          indices: A 2-D int64 tensor of shape `[N, ndims]`.
          values: A 1-D tensor of any type and shape `[N]`.
          dense_shape: A 1-D int64 tensor of shape `[ndims]`.

        Raises:
          ValueError: When building an eager SparseTensor if `dense_shape` is
            unknown or contains unknown elements (None or -1).
        """
        ...
    def get_shape(self) -> TensorShape:
        """
        Get the `TensorShape` representing the shape of the dense tensor.

        Returns:
          A `TensorShape` object.
        """
        ...
    # Many arithmetic operations are not directly supported. Some have alternatives like tf.sparse.add instead of +.
    def __div__(self, y: _SparseTensorCompatible) -> SparseTensor:
        """
        Component-wise divides a SparseTensor by a dense Tensor.

        *Limitation*: this Op only broadcasts the dense side to the sparse side, but not
        the other direction.

        Args:
          sp_indices: A `Tensor` of type `int64`.
            2-D.  `N x R` matrix with the indices of non-empty values in a
            SparseTensor, possibly not in canonical ordering.
          sp_values: A `Tensor`. Must be one of the following types: `float32`, `float64`, `int32`, `uint8`, `int16`, `int8`, `complex64`, `int64`, `qint8`, `quint8`, `qint32`, `bfloat16`, `qint16`, `quint16`, `uint16`, `complex128`, `half`, `uint32`, `uint64`.
            1-D.  `N` non-empty values corresponding to `sp_indices`.
          sp_shape: A `Tensor` of type `int64`.
            1-D.  Shape of the input SparseTensor.
          dense: A `Tensor`. Must have the same type as `sp_values`.
            `R`-D.  The dense Tensor operand.
          name: A name for the operation (optional).

        Returns:
          A `Tensor`. Has the same type as `sp_values`.
        """
        ...
    def __truediv__(self, y: _SparseTensorCompatible) -> SparseTensor:
        """Internal helper function for 'sp_t / dense_t'."""
        ...
    def __mul__(self, y: _SparseTensorCompatible) -> SparseTensor:
        """
        Component-wise multiplies a SparseTensor by a dense Tensor.

        The output locations corresponding to the implicitly zero elements in the sparse
        tensor will be zero (i.e., will not take up storage space), regardless of the
        contents of the dense tensor (even if it's +/-INF and that INF*0 == NaN).

        *Limitation*: this Op only broadcasts the dense side to the sparse side, but not
        the other direction.

        Args:
          sp_indices: A `Tensor` of type `int64`.
            2-D.  `N x R` matrix with the indices of non-empty values in a
            SparseTensor, possibly not in canonical ordering.
          sp_values: A `Tensor`. Must be one of the following types: `float32`, `float64`, `int32`, `uint8`, `int16`, `int8`, `complex64`, `int64`, `qint8`, `quint8`, `qint32`, `bfloat16`, `qint16`, `quint16`, `uint16`, `complex128`, `half`, `uint32`, `uint64`.
            1-D.  `N` non-empty values corresponding to `sp_indices`.
          sp_shape: A `Tensor` of type `int64`.
            1-D.  Shape of the input SparseTensor.
          dense: A `Tensor`. Must have the same type as `sp_values`.
            `R`-D.  The dense Tensor operand.
          name: A name for the operation (optional).

        Returns:
          A `Tensor`. Has the same type as `sp_values`.
        """
        ...
    def __getattr__(self, name: str) -> Incomplete: ...

def __getattr__(name: str): ...  # incomplete module

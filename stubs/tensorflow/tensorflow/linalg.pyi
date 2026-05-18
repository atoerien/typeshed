"""Public API for tf._api.v2.linalg namespace"""

from builtins import bool as _bool
from collections.abc import Iterable
from typing import Literal, overload

import tensorflow as tf
from tensorflow import RaggedTensor, Tensor, norm as norm
from tensorflow._aliases import DTypeLike, IntArray, Integer, ScalarTensorCompatible, TensorCompatible
from tensorflow.math import l2_normalize as l2_normalize

@overload
def matmul(
    a: TensorCompatible,
    b: TensorCompatible,
    transpose_a: _bool = False,
    transpose_b: _bool = False,
    adjoint_a: _bool = False,
    adjoint_b: _bool = False,
    a_is_sparse: _bool = False,
    b_is_sparse: _bool = False,
    output_type: DTypeLike | None = None,
    grad_a: _bool = False,
    grad_b: _bool = False,
    name: str | None = None,
) -> Tensor:
    """
    Multiplies matrix `a` by matrix `b`, producing `a` * `b`.

    The inputs must, following any transpositions, be tensors of rank >= 2
    where the inner 2 dimensions specify valid matrix multiplication dimensions,
    and any further outer dimensions specify matching batch size.

    Both matrices must be of the same type. The supported types are:
    `bfloat16`, `float16`, `float32`, `float64`, `int32`, `int64`,
    `complex64`, `complex128`.

    Either matrix can be transposed or adjointed (conjugated and transposed) on
    the fly by setting one of the corresponding flag to `True`. These are `False`
    by default.

    If one or both of the matrices contain a lot of zeros, a more efficient
    multiplication algorithm can be used by setting the corresponding
    `a_is_sparse` or `b_is_sparse` flag to `True`. These are `False` by default.
    This optimization is only available for plain matrices (rank-2 tensors) with
    datatypes `bfloat16` or `float32`.

    A simple 2-D tensor matrix multiplication:

    >>> a = tf.constant([1, 2, 3, 4, 5, 6], shape=[2, 3])
    >>> a  # 2-D tensor
    <tf.Tensor: shape=(2, 3), dtype=int32, numpy=
    array([[1, 2, 3],
           [4, 5, 6]], dtype=int32)>
    >>> b = tf.constant([7, 8, 9, 10, 11, 12], shape=[3, 2])
    >>> b  # 2-D tensor
    <tf.Tensor: shape=(3, 2), dtype=int32, numpy=
    array([[ 7,  8],
           [ 9, 10],
           [11, 12]], dtype=int32)>
    >>> c = tf.matmul(a, b)
    >>> c  # `a` * `b`
    <tf.Tensor: shape=(2, 2), dtype=int32, numpy=
    array([[ 58,  64],
           [139, 154]], dtype=int32)>

    A batch matrix multiplication with batch shape [2]:

    >>> a = tf.constant(np.arange(1, 13, dtype=np.int32), shape=[2, 2, 3])
    >>> a  # 3-D tensor
    <tf.Tensor: shape=(2, 2, 3), dtype=int32, numpy=
    array([[[ 1,  2,  3],
            [ 4,  5,  6]],
           [[ 7,  8,  9],
            [10, 11, 12]]], dtype=int32)>
    >>> b = tf.constant(np.arange(13, 25, dtype=np.int32), shape=[2, 3, 2])
    >>> b  # 3-D tensor
    <tf.Tensor: shape=(2, 3, 2), dtype=int32, numpy=
    array([[[13, 14],
            [15, 16],
            [17, 18]],
           [[19, 20],
            [21, 22],
            [23, 24]]], dtype=int32)>
    >>> c = tf.matmul(a, b)
    >>> c  # `a` * `b`
    <tf.Tensor: shape=(2, 2, 2), dtype=int32, numpy=
    array([[[ 94, 100],
            [229, 244]],
           [[508, 532],
            [697, 730]]], dtype=int32)>

    Since python >= 3.5 the @ operator is supported
    (see [PEP 465](https://www.python.org/dev/peps/pep-0465/)). In TensorFlow,
    it simply calls the `tf.matmul()` function, so the following lines are
    equivalent:

    >>> d = a @ b @ [[10], [11]]
    >>> d = tf.matmul(tf.matmul(a, b), [[10], [11]])

    Args:
      a: `tf.Tensor` of type `float16`, `float32`, `float64`, `int32`,
        `complex64`, `complex128` and rank > 1.
      b: `tf.Tensor` with same type and rank as `a`.
      transpose_a: If `True`, `a` is transposed before multiplication.
      transpose_b: If `True`, `b` is transposed before multiplication.
      adjoint_a: If `True`, `a` is conjugated and transposed before
        multiplication.
      adjoint_b: If `True`, `b` is conjugated and transposed before
        multiplication.
      a_is_sparse: If `True`, `a` is treated as a sparse matrix. Notice, this
        **does not support `tf.sparse.SparseTensor`**, it just makes optimizations
        that assume most values in `a` are zero. See
        `tf.sparse.sparse_dense_matmul` for some support for
        `tf.sparse.SparseTensor` multiplication.
      b_is_sparse: If `True`, `b` is treated as a sparse matrix. Notice, this
        **does not support `tf.sparse.SparseTensor`**, it just makes optimizations
        that assume most values in `b` are zero. See
        `tf.sparse.sparse_dense_matmul` for some support for
        `tf.sparse.SparseTensor` multiplication.
      output_type: The output datatype if needed. Defaults to None in which case
        the output_type is the same as input type. Currently only works when input
        tensors are type (u)int8 and output_type can be int32.
      grad_a: Set it to `True` to hint that Tensor `a` is for the backward pass.
      grad_b: Set it to `True` to hint that Tensor `b` is for the backward pass.
      name: Name for the operation (optional).

    Returns:
      A `tf.Tensor` of the same type as `a` and `b` where each inner-most matrix
      is the product of the corresponding matrices in `a` and `b`, e.g. if all
      transpose or adjoint attributes are `False`:

      `output[..., i, j] = sum_k (a[..., i, k] * b[..., k, j])`,
      for all indices `i`, `j`.

      Note: This is matrix product, not element-wise product.


    Raises:
      ValueError: If `transpose_a` and `adjoint_a`, or `transpose_b` and
        `adjoint_b` are both set to `True`.
      TypeError: If output_type is specified but the types of `a`, `b` and
        `output_type` is not (u)int8, (u)int8 and int32.
    """
    ...
@overload
def matmul(
    a: RaggedTensor,
    b: RaggedTensor,
    transpose_a: _bool = False,
    transpose_b: _bool = False,
    adjoint_a: _bool = False,
    adjoint_b: _bool = False,
    a_is_sparse: _bool = False,
    b_is_sparse: _bool = False,
    output_type: DTypeLike | None = None,
    grad_a: _bool = False,
    grad_b: _bool = False,
    name: str | None = None,
) -> RaggedTensor: ...

def set_diag(
    input: TensorCompatible,
    diagonal: TensorCompatible,
    name: str | None = "set_diag",
    k: int = 0,
    align: Literal["RIGHT_LEFT", "RIGHT_RIGHT", "LEFT_LEFT", "LEFT_RIGHT"] = "RIGHT_LEFT",
) -> Tensor:
    """
    Returns a batched matrix tensor with new batched diagonal values.

    Given `input` and `diagonal`, this operation returns a tensor with the
    same shape and values as `input`, except for the specified diagonals of the
    innermost matrices. These will be overwritten by the values in `diagonal`.

    `input` has `r+1` dimensions `[I, J, ..., L, M, N]`. When `k` is scalar or
    `k[0] == k[1]`, `diagonal` has `r` dimensions `[I, J, ..., L, max_diag_len]`.
    Otherwise, it has `r+1` dimensions `[I, J, ..., L, num_diags, max_diag_len]`.
    `num_diags` is the number of diagonals, `num_diags = k[1] - k[0] + 1`.
    `max_diag_len` is the longest diagonal in the range `[k[0], k[1]]`,
    `max_diag_len = min(M + min(k[1], 0), N + min(-k[0], 0))`

    The output is a tensor of rank `k+1` with dimensions `[I, J, ..., L, M, N]`.
    If `k` is scalar or `k[0] == k[1]`:

    ```
    output[i, j, ..., l, m, n]
      = diagonal[i, j, ..., l, n-max(k[1], 0)] ; if n - m == k[1]
        input[i, j, ..., l, m, n]              ; otherwise
    ```

    Otherwise,

    ```
    output[i, j, ..., l, m, n]
      = diagonal[i, j, ..., l, diag_index, index_in_diag] ; if k[0] <= d <= k[1]
        input[i, j, ..., l, m, n]                         ; otherwise
    ```
    where `d = n - m`, `diag_index = k[1] - d`, and
    `index_in_diag = n - max(d, 0) + offset`.

    `offset` is zero except when the alignment of the diagonal is to the right.
    ```
    offset = max_diag_len - diag_len(d) ; if (`align` in {RIGHT_LEFT, RIGHT_RIGHT}
                                               and `d >= 0`) or
                                             (`align` in {LEFT_RIGHT, RIGHT_RIGHT}
                                               and `d <= 0`)
             0                          ; otherwise
    ```
    where `diag_len(d) = min(cols - max(d, 0), rows + min(d, 0))`.

    For example:

    ```
    # The main diagonal.
    input = np.array([[[7, 7, 7, 7],              # Input shape: (2, 3, 4)
                       [7, 7, 7, 7],
                       [7, 7, 7, 7]],
                      [[7, 7, 7, 7],
                       [7, 7, 7, 7],
                       [7, 7, 7, 7]]])
    diagonal = np.array([[1, 2, 3],               # Diagonal shape: (2, 3)
                         [4, 5, 6]])
    tf.matrix_set_diag(input, diagonal)
      ==> [[[1, 7, 7, 7],  # Output shape: (2, 3, 4)
            [7, 2, 7, 7],
            [7, 7, 3, 7]],
           [[4, 7, 7, 7],
            [7, 5, 7, 7],
            [7, 7, 6, 7]]]

    # A superdiagonal (per batch).
    tf.matrix_set_diag(input, diagonal, k = 1)
      ==> [[[7, 1, 7, 7],  # Output shape: (2, 3, 4)
            [7, 7, 2, 7],
            [7, 7, 7, 3]],
           [[7, 4, 7, 7],
            [7, 7, 5, 7],
            [7, 7, 7, 6]]]

    # A band of diagonals.
    diagonals = np.array([[[9, 1, 0],  # Diagonal shape: (2, 4, 3)
                           [6, 5, 8],
                           [1, 2, 3],
                           [0, 4, 5]],
                          [[1, 2, 0],
                           [5, 6, 4],
                           [6, 1, 2],
                           [0, 3, 4]]])
    tf.matrix_set_diag(input, diagonals, k = (-1, 2))
      ==> [[[1, 6, 9, 7],  # Output shape: (2, 3, 4)
            [4, 2, 5, 1],
            [7, 5, 3, 8]],
           [[6, 5, 1, 7],
            [3, 1, 6, 2],
            [7, 4, 2, 4]]]

    # RIGHT_LEFT alignment.
    diagonals = np.array([[[0, 9, 1],  # Diagonal shape: (2, 4, 3)
                           [6, 5, 8],
                           [1, 2, 3],
                           [4, 5, 0]],
                          [[0, 1, 2],
                           [5, 6, 4],
                           [6, 1, 2],
                           [3, 4, 0]]])
    tf.matrix_set_diag(input, diagonals, k = (-1, 2), align="RIGHT_LEFT")
      ==> [[[1, 6, 9, 7],  # Output shape: (2, 3, 4)
            [4, 2, 5, 1],
            [7, 5, 3, 8]],
           [[6, 5, 1, 7],
            [3, 1, 6, 2],
            [7, 4, 2, 4]]]

    ```

    Args:
      input: A `Tensor` with rank `k + 1`, where `k >= 1`.
      diagonal:  A `Tensor` with rank `k`, when `d_lower == d_upper`, or `k + 1`,
        otherwise. `k >= 1`.
      name: A name for the operation (optional).
      k: Diagonal offset(s). Positive value means superdiagonal, 0 refers to the
        main diagonal, and negative value means subdiagonals. `k` can be a single
        integer (for a single diagonal) or a pair of integers specifying the low
        and high ends of a matrix band. `k[0]` must not be larger than `k[1]`.
      align: Some diagonals are shorter than `max_diag_len` and need to be padded.
        `align` is a string specifying how superdiagonals and subdiagonals should
        be aligned, respectively. There are four possible alignments: "RIGHT_LEFT"
        (default), "LEFT_RIGHT", "LEFT_LEFT", and "RIGHT_RIGHT". "RIGHT_LEFT"
        aligns superdiagonals to the right (left-pads the row) and subdiagonals to
        the left (right-pads the row). It is the packing format LAPACK uses.
        cuSPARSE uses "LEFT_RIGHT", which is the opposite alignment.
    """
    ...
def eye(
    num_rows: ScalarTensorCompatible,
    num_columns: ScalarTensorCompatible | None = None,
    batch_shape: Iterable[int] | IntArray | tf.Tensor | None = None,
    dtype: DTypeLike = ...,
    name: str | None = None,
) -> Tensor:
    """
    Construct an identity matrix, or a batch of matrices.

    See also `tf.ones`, `tf.zeros`, `tf.fill`, `tf.one_hot`.

    ```python
    # Construct one identity matrix.
    tf.eye(2)
    ==> [[1., 0.],
         [0., 1.]]

    # Construct a batch of 3 identity matrices, each 2 x 2.
    # batch_identity[i, :, :] is a 2 x 2 identity matrix, i = 0, 1, 2.
    batch_identity = tf.eye(2, batch_shape=[3])

    # Construct one 2 x 3 "identity" matrix
    tf.eye(2, num_columns=3)
    ==> [[ 1.,  0.,  0.],
         [ 0.,  1.,  0.]]
    ```

    Args:
      num_rows: Non-negative `int32` scalar `Tensor` giving the number of rows
        in each batch matrix.
      num_columns: Optional non-negative `int32` scalar `Tensor` giving the number
        of columns in each batch matrix.  Defaults to `num_rows`.
      batch_shape:  A list or tuple of Python integers or a 1-D `int32` `Tensor`.
        If provided, the returned `Tensor` will have leading batch dimensions of
        this shape.
      dtype:  The type of an element in the resulting `Tensor`
      name:  A name for this `Op`.  Defaults to "eye".

    Returns:
      A `Tensor` of shape `batch_shape + [num_rows, num_columns]`
    """
    ...
def band_part(input: TensorCompatible, num_lower: Integer, num_upper: Integer, name: str | None = None) -> Tensor:
    """
    Copy a tensor setting everything outside a central band in each innermost matrix to zero.

    The `band` part is computed as follows:
    Assume `input` has `k` dimensions `[I, J, K, ..., M, N]`, then the output is a
    tensor with the same shape where

    `band[i, j, k, ..., m, n] = in_band(m, n) * input[i, j, k, ..., m, n]`.

    The indicator function

    `in_band(m, n) = (num_lower < 0 || (m-n) <= num_lower)) &&
                     (num_upper < 0 || (n-m) <= num_upper)`.

    For example:

    ```
    # if 'input' is [[ 0,  1,  2, 3]
    #                [-1,  0,  1, 2]
    #                [-2, -1,  0, 1]
    #                [-3, -2, -1, 0]],

    tf.linalg.band_part(input, 1, -1) ==> [[ 0,  1,  2, 3]
                                           [-1,  0,  1, 2]
                                           [ 0, -1,  0, 1]
                                           [ 0,  0, -1, 0]],

    tf.linalg.band_part(input, 2, 1) ==> [[ 0,  1,  0, 0]
                                          [-1,  0,  1, 0]
                                          [-2, -1,  0, 1]
                                          [ 0, -2, -1, 0]]
    ```

    Useful special cases:

    ```
     tf.linalg.band_part(input, 0, -1) ==> Upper triangular part.
     tf.linalg.band_part(input, -1, 0) ==> Lower triangular part.
     tf.linalg.band_part(input, 0, 0) ==> Diagonal.
    ```

    Args:
      input: A `Tensor`. Rank `k` tensor.
      num_lower: A `Tensor`. Must be one of the following types: `int32`, `int64`.
        0-D tensor. Number of subdiagonals to keep. If negative, keep entire
        lower triangle.
      num_upper: A `Tensor`. Must have the same type as `num_lower`.
        0-D tensor. Number of superdiagonals to keep. If negative, keep
        entire upper triangle.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `input`.
    """
    ...
def __getattr__(name: str): ...  # incomplete module

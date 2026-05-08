"""Public API for tf._api.v2.math namespace"""

from collections.abc import Iterable
from typing import TypeAlias, TypeVar, overload

from tensorflow import IndexedSlices, RaggedTensor, Tensor
from tensorflow._aliases import DTypeLike, ShapeLike, TensorCompatible
from tensorflow.sparse import SparseTensor

_TensorCompatibleT = TypeVar("_TensorCompatibleT", bound=TensorCompatible)
_SparseTensorCompatible: TypeAlias = TensorCompatible | SparseTensor

# Most operations support RaggedTensor. Documentation for them is here,
# https://www.tensorflow.org/api_docs/python/tf/ragged.
# Most operations do not support SparseTensor. Operations often don't document
# whether they support SparseTensor and it is best to test them manually. Typically
# if an operation outputs non-zero value for a zero input, it will not support
# SparseTensors. Binary operations with ragged tensors usually only work
# if both operands are ragged.
@overload
def abs(x: TensorCompatible, name: str | None = None) -> Tensor:
    r"""
    Computes the absolute value of a tensor.

    Given a tensor of integer or floating-point values, this operation returns a
    tensor of the same type, where each element contains the absolute value of the
    corresponding element in the input.

    Given a tensor `x` of complex numbers, this operation returns a tensor of type
    `float32` or `float64` that is the absolute value of each element in `x`. For
    a complex number \\(a + bj\\), its absolute value is computed as
    \\(\sqrt{a^2 + b^2}\\).

    For example:

    >>> # real number
    >>> x = tf.constant([-2.25, 3.25])
    >>> tf.abs(x)
    <tf.Tensor: shape=(2,), dtype=float32,
    numpy=array([2.25, 3.25], dtype=float32)>

    >>> # complex number
    >>> x = tf.constant([[-2.25 + 4.75j], [-3.25 + 5.75j]])
    >>> tf.abs(x)
    <tf.Tensor: shape=(2, 1), dtype=float64, numpy=
    array([[5.25594901],
           [6.60492241]])>

    Args:
      x: A `Tensor` or `SparseTensor` of type `float16`, `float32`, `float64`,
        `int32`, `int64`, `complex64` or `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` or `SparseTensor` of the same size, type and sparsity as `x`,
        with absolute values. Note, for `complex64` or `complex128` input, the
        returned `Tensor` will be of type `float32` or `float64`, respectively.

      If `x` is a `SparseTensor`, returns
      `SparseTensor(x.indices, tf.math.abs(x.values, ...), x.dense_shape)`
    """
    ...
@overload
def abs(x: SparseTensor, name: str | None = None) -> SparseTensor:
    r"""
    Computes the absolute value of a tensor.

    Given a tensor of integer or floating-point values, this operation returns a
    tensor of the same type, where each element contains the absolute value of the
    corresponding element in the input.

    Given a tensor `x` of complex numbers, this operation returns a tensor of type
    `float32` or `float64` that is the absolute value of each element in `x`. For
    a complex number \\(a + bj\\), its absolute value is computed as
    \\(\sqrt{a^2 + b^2}\\).

    For example:

    >>> # real number
    >>> x = tf.constant([-2.25, 3.25])
    >>> tf.abs(x)
    <tf.Tensor: shape=(2,), dtype=float32,
    numpy=array([2.25, 3.25], dtype=float32)>

    >>> # complex number
    >>> x = tf.constant([[-2.25 + 4.75j], [-3.25 + 5.75j]])
    >>> tf.abs(x)
    <tf.Tensor: shape=(2, 1), dtype=float64, numpy=
    array([[5.25594901],
           [6.60492241]])>

    Args:
      x: A `Tensor` or `SparseTensor` of type `float16`, `float32`, `float64`,
        `int32`, `int64`, `complex64` or `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` or `SparseTensor` of the same size, type and sparsity as `x`,
        with absolute values. Note, for `complex64` or `complex128` input, the
        returned `Tensor` will be of type `float32` or `float64`, respectively.

      If `x` is a `SparseTensor`, returns
      `SparseTensor(x.indices, tf.math.abs(x.values, ...), x.dense_shape)`
    """
    ...
@overload
def abs(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    r"""
    Computes the absolute value of a tensor.

    Given a tensor of integer or floating-point values, this operation returns a
    tensor of the same type, where each element contains the absolute value of the
    corresponding element in the input.

    Given a tensor `x` of complex numbers, this operation returns a tensor of type
    `float32` or `float64` that is the absolute value of each element in `x`. For
    a complex number \\(a + bj\\), its absolute value is computed as
    \\(\sqrt{a^2 + b^2}\\).

    For example:

    >>> # real number
    >>> x = tf.constant([-2.25, 3.25])
    >>> tf.abs(x)
    <tf.Tensor: shape=(2,), dtype=float32,
    numpy=array([2.25, 3.25], dtype=float32)>

    >>> # complex number
    >>> x = tf.constant([[-2.25 + 4.75j], [-3.25 + 5.75j]])
    >>> tf.abs(x)
    <tf.Tensor: shape=(2, 1), dtype=float64, numpy=
    array([[5.25594901],
           [6.60492241]])>

    Args:
      x: A `Tensor` or `SparseTensor` of type `float16`, `float32`, `float64`,
        `int32`, `int64`, `complex64` or `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` or `SparseTensor` of the same size, type and sparsity as `x`,
        with absolute values. Note, for `complex64` or `complex128` input, the
        returned `Tensor` will be of type `float32` or `float64`, respectively.

      If `x` is a `SparseTensor`, returns
      `SparseTensor(x.indices, tf.math.abs(x.values, ...), x.dense_shape)`
    """
    ...
@overload
def angle(input: TensorCompatible, name: str | None = None) -> Tensor:
    r"""
    Returns the element-wise argument of a complex (or real) tensor.

    Given a tensor `input`, this operation returns a tensor of type `float` that
    is the argument of each element in `input` considered as a complex number.

    The elements in `input` are considered to be complex numbers of the form
    \\(a + bj\\), where *a* is the real part and *b* is the imaginary part.
    If `input` is real then *b* is zero by definition.

    The argument returned by this function is of the form \\(atan2(b, a)\\).
    If `input` is real, a tensor of all zeros is returned.

    For example:

    ```
    input = tf.constant([-2.25 + 4.75j, 3.25 + 5.75j], dtype=tf.complex64)
    tf.math.angle(input).numpy()
    # ==> array([2.0131705, 1.056345 ], dtype=float32)
    ```

    Args:
      input: A `Tensor`. Must be one of the following types: `float`, `double`,
        `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `float32` or `float64`.
    """
    ...
@overload
def angle(input: RaggedTensor, name: str | None = None) -> RaggedTensor:
    r"""
    Returns the element-wise argument of a complex (or real) tensor.

    Given a tensor `input`, this operation returns a tensor of type `float` that
    is the argument of each element in `input` considered as a complex number.

    The elements in `input` are considered to be complex numbers of the form
    \\(a + bj\\), where *a* is the real part and *b* is the imaginary part.
    If `input` is real then *b* is zero by definition.

    The argument returned by this function is of the form \\(atan2(b, a)\\).
    If `input` is real, a tensor of all zeros is returned.

    For example:

    ```
    input = tf.constant([-2.25 + 4.75j, 3.25 + 5.75j], dtype=tf.complex64)
    tf.math.angle(input).numpy()
    # ==> array([2.0131705, 1.056345 ], dtype=float32)
    ```

    Args:
      input: A `Tensor`. Must be one of the following types: `float`, `double`,
        `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `float32` or `float64`.
    """
    ...
@overload
def sin(x: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Computes sine of x element-wise.

      Given an input tensor, this function computes sine of every
      element in the tensor. Input range is `(-inf, inf)` and
      output range is `[-1,1]`.

      ```python
      x = tf.constant([-float("inf"), -9, -0.5, 1, 1.2, 200, 10, float("inf")])
      tf.math.sin(x) ==> [nan -0.4121185 -0.47942555 0.84147096 0.9320391 -0.87329733 -0.54402107 nan]
      ```

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def sin(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Computes sine of x element-wise.

      Given an input tensor, this function computes sine of every
      element in the tensor. Input range is `(-inf, inf)` and
      output range is `[-1,1]`.

      ```python
      x = tf.constant([-float("inf"), -9, -0.5, 1, 1.2, 200, 10, float("inf")])
      tf.math.sin(x) ==> [nan -0.4121185 -0.47942555 0.84147096 0.9320391 -0.87329733 -0.54402107 nan]
      ```

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def cos(x: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Computes cos of x element-wise.

      Given an input tensor, this function computes cosine of every
      element in the tensor. Input range is `(-inf, inf)` and
      output range is `[-1,1]`. If input lies outside the boundary, `nan`
      is returned.

      ```python
      x = tf.constant([-float("inf"), -9, -0.5, 1, 1.2, 200, 10000, float("inf")])
      tf.math.cos(x) ==> [nan -0.91113025 0.87758255 0.5403023 0.36235774 0.48718765 -0.95215535 nan]
      ```

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def cos(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Computes cos of x element-wise.

      Given an input tensor, this function computes cosine of every
      element in the tensor. Input range is `(-inf, inf)` and
      output range is `[-1,1]`. If input lies outside the boundary, `nan`
      is returned.

      ```python
      x = tf.constant([-float("inf"), -9, -0.5, 1, 1.2, 200, 10000, float("inf")])
      tf.math.cos(x) ==> [nan -0.91113025 0.87758255 0.5403023 0.36235774 0.48718765 -0.95215535 nan]
      ```

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def exp(x: TensorCompatible, name: str | None = None) -> Tensor:
    r"""
    Computes exponential of x element-wise.  \\(y = e^x\\).

    This function computes the exponential of the input tensor element-wise.
    i.e. `math.exp(x)` or \\(e^x\\), where `x` is the input tensor.
    \\(e\\) denotes Euler's number and is approximately equal to 2.718281.
    Output is positive for any real input.

    >>> x = tf.constant(2.0)
    >>> tf.math.exp(x)
    <tf.Tensor: shape=(), dtype=float32, numpy=7.389056>

    >>> x = tf.constant([2.0, 8.0])
    >>> tf.math.exp(x)
    <tf.Tensor: shape=(2,), dtype=float32,
    numpy=array([   7.389056, 2980.958   ], dtype=float32)>

    For complex numbers, the exponential value is calculated as
    $$
    e^{x+iy} = {e^x} {e^{iy}} = {e^x} ({\cos (y) + i \sin (y)})
    $$

    For `1+1j` the value would be computed as:
    $$
    e^1 (\cos (1) + i \sin (1)) = 2.7182817 \times (0.5403023+0.84147096j)
    $$

    >>> x = tf.constant(1 + 1j)
    >>> tf.math.exp(x)
    <tf.Tensor: shape=(), dtype=complex128,
    numpy=(1.4686939399158851+2.2873552871788423j)>

    Args:
      x: A `tf.Tensor`. Must be one of the following types: `bfloat16`, `half`,
        `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `tf.Tensor`. Has the same type as `x`.

    @compatibility(numpy)
    Equivalent to np.exp
    @end_compatibility
    """
    ...
@overload
def exp(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    r"""
    Computes exponential of x element-wise.  \\(y = e^x\\).

    This function computes the exponential of the input tensor element-wise.
    i.e. `math.exp(x)` or \\(e^x\\), where `x` is the input tensor.
    \\(e\\) denotes Euler's number and is approximately equal to 2.718281.
    Output is positive for any real input.

    >>> x = tf.constant(2.0)
    >>> tf.math.exp(x)
    <tf.Tensor: shape=(), dtype=float32, numpy=7.389056>

    >>> x = tf.constant([2.0, 8.0])
    >>> tf.math.exp(x)
    <tf.Tensor: shape=(2,), dtype=float32,
    numpy=array([   7.389056, 2980.958   ], dtype=float32)>

    For complex numbers, the exponential value is calculated as
    $$
    e^{x+iy} = {e^x} {e^{iy}} = {e^x} ({\cos (y) + i \sin (y)})
    $$

    For `1+1j` the value would be computed as:
    $$
    e^1 (\cos (1) + i \sin (1)) = 2.7182817 \times (0.5403023+0.84147096j)
    $$

    >>> x = tf.constant(1 + 1j)
    >>> tf.math.exp(x)
    <tf.Tensor: shape=(), dtype=complex128,
    numpy=(1.4686939399158851+2.2873552871788423j)>

    Args:
      x: A `tf.Tensor`. Must be one of the following types: `bfloat16`, `half`,
        `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `tf.Tensor`. Has the same type as `x`.

    @compatibility(numpy)
    Equivalent to np.exp
    @end_compatibility
    """
    ...
@overload
def sinh(x: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Computes hyperbolic sine of x element-wise.

      Given an input tensor, this function computes hyperbolic sine of every
      element in the tensor. Input range is `[-inf,inf]` and output range
      is `[-inf,inf]`.

      ```python
      x = tf.constant([-float("inf"), -9, -0.5, 1, 1.2, 2, 10, float("inf")])
      tf.math.sinh(x) ==> [-inf -4.0515420e+03 -5.2109528e-01 1.1752012e+00 1.5094614e+00 3.6268604e+00 1.1013232e+04 inf]
      ```

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def sinh(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Computes hyperbolic sine of x element-wise.

      Given an input tensor, this function computes hyperbolic sine of every
      element in the tensor. Input range is `[-inf,inf]` and output range
      is `[-inf,inf]`.

      ```python
      x = tf.constant([-float("inf"), -9, -0.5, 1, 1.2, 2, 10, float("inf")])
      tf.math.sinh(x) ==> [-inf -4.0515420e+03 -5.2109528e-01 1.1752012e+00 1.5094614e+00 3.6268604e+00 1.1013232e+04 inf]
      ```

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def cosh(x: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Computes hyperbolic cosine of x element-wise.

      Given an input tensor, this function computes hyperbolic cosine of every
      element in the tensor. Input range is `[-inf, inf]` and output range
      is `[1, inf]`.

      ```python
      x = tf.constant([-float("inf"), -9, -0.5, 1, 1.2, 2, 10, float("inf")])
      tf.math.cosh(x) ==> [inf 4.0515420e+03 1.1276259e+00 1.5430807e+00 1.8106556e+00 3.7621956e+00 1.1013233e+04 inf]
      ```

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def cosh(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Computes hyperbolic cosine of x element-wise.

      Given an input tensor, this function computes hyperbolic cosine of every
      element in the tensor. Input range is `[-inf, inf]` and output range
      is `[1, inf]`.

      ```python
      x = tf.constant([-float("inf"), -9, -0.5, 1, 1.2, 2, 10, float("inf")])
      tf.math.cosh(x) ==> [inf 4.0515420e+03 1.1276259e+00 1.5430807e+00 1.8106556e+00 3.7621956e+00 1.1013233e+04 inf]
      ```

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def tanh(x: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Computes hyperbolic tangent of `x` element-wise.

      Given an input tensor, this function computes hyperbolic tangent of every
      element in the tensor. Input range is `[-inf, inf]` and
      output range is `[-1,1]`.

      >>> x = tf.constant([-float("inf"), -5, -0.5, 1, 1.2, 2, 3, float("inf")])
      >>> tf.math.tanh(x)
      <tf.Tensor: shape=(8,), dtype=float32, numpy=
      array([-1.0, -0.99990916, -0.46211717,  0.7615942 ,  0.8336547 ,
              0.9640276 ,  0.9950547 ,  1.0], dtype=float32)>

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.

      If `x` is a `SparseTensor`, returns
      `SparseTensor(x.indices, tf.math.tanh(x.values, ...), x.dense_shape)`
    """
    ...
@overload
def tanh(x: SparseTensor, name: str | None = None) -> SparseTensor:
    """
    Computes hyperbolic tangent of `x` element-wise.

      Given an input tensor, this function computes hyperbolic tangent of every
      element in the tensor. Input range is `[-inf, inf]` and
      output range is `[-1,1]`.

      >>> x = tf.constant([-float("inf"), -5, -0.5, 1, 1.2, 2, 3, float("inf")])
      >>> tf.math.tanh(x)
      <tf.Tensor: shape=(8,), dtype=float32, numpy=
      array([-1.0, -0.99990916, -0.46211717,  0.7615942 ,  0.8336547 ,
              0.9640276 ,  0.9950547 ,  1.0], dtype=float32)>

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.

      If `x` is a `SparseTensor`, returns
      `SparseTensor(x.indices, tf.math.tanh(x.values, ...), x.dense_shape)`
    """
    ...
@overload
def tanh(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Computes hyperbolic tangent of `x` element-wise.

      Given an input tensor, this function computes hyperbolic tangent of every
      element in the tensor. Input range is `[-inf, inf]` and
      output range is `[-1,1]`.

      >>> x = tf.constant([-float("inf"), -5, -0.5, 1, 1.2, 2, 3, float("inf")])
      >>> tf.math.tanh(x)
      <tf.Tensor: shape=(8,), dtype=float32, numpy=
      array([-1.0, -0.99990916, -0.46211717,  0.7615942 ,  0.8336547 ,
              0.9640276 ,  0.9950547 ,  1.0], dtype=float32)>

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.

      If `x` is a `SparseTensor`, returns
      `SparseTensor(x.indices, tf.math.tanh(x.values, ...), x.dense_shape)`
    """
    ...
@overload
def expm1(x: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Computes `exp(x) - 1` element-wise.

      i.e. `exp(x) - 1` or `e^(x) - 1`, where `x` is the input tensor.
      `e` denotes Euler's number and is approximately equal to 2.718281.

      ```python
      x = tf.constant(2.0)
      tf.math.expm1(x) ==> 6.389056

      x = tf.constant([2.0, 8.0])
      tf.math.expm1(x) ==> array([6.389056, 2979.958], dtype=float32)

      x = tf.constant(1 + 1j)
      tf.math.expm1(x) ==> (0.46869393991588515+2.2873552871788423j)
      ```

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def expm1(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Computes `exp(x) - 1` element-wise.

      i.e. `exp(x) - 1` or `e^(x) - 1`, where `x` is the input tensor.
      `e` denotes Euler's number and is approximately equal to 2.718281.

      ```python
      x = tf.constant(2.0)
      tf.math.expm1(x) ==> 6.389056

      x = tf.constant([2.0, 8.0])
      tf.math.expm1(x) ==> array([6.389056, 2979.958], dtype=float32)

      x = tf.constant(1 + 1j)
      tf.math.expm1(x) ==> (0.46869393991588515+2.2873552871788423j)
      ```

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def log(x: TensorCompatible, name: str | None = None) -> Tensor:
    r"""
    Computes natural logarithm of x element-wise.

    I.e., \\(y = \log_e x\\).

    Example:
    >>> x = tf.constant([0, 0.5, 1, 5])
    >>> tf.math.log(x)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=array([      -inf, -0.6931472,  0.       ,  1.609438 ], dtype=float32)>

    See: https://en.wikipedia.org/wiki/Logarithm

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def log(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    r"""
    Computes natural logarithm of x element-wise.

    I.e., \\(y = \log_e x\\).

    Example:
    >>> x = tf.constant([0, 0.5, 1, 5])
    >>> tf.math.log(x)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=array([      -inf, -0.6931472,  0.       ,  1.609438 ], dtype=float32)>

    See: https://en.wikipedia.org/wiki/Logarithm

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def log1p(x: TensorCompatible, name: str | None = None) -> Tensor:
    r"""
    Computes natural logarithm of (1 + x) element-wise.

    I.e., \\(y = \log_e (1 + x)\\).

    Example:
    >>> x = tf.constant([0, 0.5, 1, 5])
    >>> tf.math.log1p(x)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=array([0.       , 0.4054651, 0.6931472, 1.7917595], dtype=float32)>

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def log1p(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    r"""
    Computes natural logarithm of (1 + x) element-wise.

    I.e., \\(y = \log_e (1 + x)\\).

    Example:
    >>> x = tf.constant([0, 0.5, 1, 5])
    >>> tf.math.log1p(x)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=array([0.       , 0.4054651, 0.6931472, 1.7917595], dtype=float32)>

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def negative(x: TensorCompatible, name: str | None = None) -> Tensor:
    r"""
    Computes numerical negative value element-wise.

    I.e., \\(y = -x\\).

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `int8`, `int16`, `int32`, `int64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.

      If `x` is a `SparseTensor`, returns
      `SparseTensor(x.indices, tf.math.negative(x.values, ...), x.dense_shape)`
    """
    ...
@overload
def negative(x: SparseTensor, name: str | None = None) -> SparseTensor:
    r"""
    Computes numerical negative value element-wise.

    I.e., \\(y = -x\\).

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `int8`, `int16`, `int32`, `int64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.

      If `x` is a `SparseTensor`, returns
      `SparseTensor(x.indices, tf.math.negative(x.values, ...), x.dense_shape)`
    """
    ...
@overload
def negative(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    r"""
    Computes numerical negative value element-wise.

    I.e., \\(y = -x\\).

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `int8`, `int16`, `int32`, `int64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.

      If `x` is a `SparseTensor`, returns
      `SparseTensor(x.indices, tf.math.negative(x.values, ...), x.dense_shape)`
    """
    ...
@overload
def sigmoid(x: TensorCompatible, name: str | None = None) -> Tensor:
    r"""
    Computes sigmoid of `x` element-wise.

    Formula for calculating $\mathrm{sigmoid}(x) = y = 1 / (1 + \exp(-x))$.

    For $x \in (-\infty, \infty)$, $\mathrm{sigmoid}(x) \in (0, 1)$.

    Example Usage:

    If a positive number is large, then its sigmoid will approach to 1 since the
    formula will be `y = <large_num> / (1 + <large_num>)`

    >>> x = tf.constant([0.0, 1.0, 50.0, 100.0])
    >>> tf.math.sigmoid(x)
    <tf.Tensor: shape=(4,), dtype=float32,
    numpy=array([0.5, 0.7310586, 1.0, 1.0], dtype=float32)>

    If a negative number is large, its sigmoid will approach to 0 since the
    formula will be `y = 1 / (1 + <large_num>)`

    >>> x = tf.constant([-100.0, -50.0, -1.0, 0.0])
    >>> tf.math.sigmoid(x)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=
    array([0.0000000e+00, 1.9287499e-22, 2.6894143e-01, 0.5],
          dtype=float32)>

    Args:
      x: A Tensor with type `float16`, `float32`, `float64`, `complex64`, or
        `complex128`.
      name: A name for the operation (optional).

    Returns:
      A Tensor with the same type as `x`.

    Usage Example:

    >>> x = tf.constant([-128.0, 0.0, 128.0], dtype=tf.float32)
    >>> tf.sigmoid(x)
    <tf.Tensor: shape=(3,), dtype=float32,
    numpy=array([0. , 0.5, 1. ], dtype=float32)>

    @compatibility(scipy)
    Equivalent to scipy.special.expit
    @end_compatibility
    """
    ...
@overload
def sigmoid(x: SparseTensor, name: str | None = None) -> SparseTensor:
    r"""
    Computes sigmoid of `x` element-wise.

    Formula for calculating $\mathrm{sigmoid}(x) = y = 1 / (1 + \exp(-x))$.

    For $x \in (-\infty, \infty)$, $\mathrm{sigmoid}(x) \in (0, 1)$.

    Example Usage:

    If a positive number is large, then its sigmoid will approach to 1 since the
    formula will be `y = <large_num> / (1 + <large_num>)`

    >>> x = tf.constant([0.0, 1.0, 50.0, 100.0])
    >>> tf.math.sigmoid(x)
    <tf.Tensor: shape=(4,), dtype=float32,
    numpy=array([0.5, 0.7310586, 1.0, 1.0], dtype=float32)>

    If a negative number is large, its sigmoid will approach to 0 since the
    formula will be `y = 1 / (1 + <large_num>)`

    >>> x = tf.constant([-100.0, -50.0, -1.0, 0.0])
    >>> tf.math.sigmoid(x)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=
    array([0.0000000e+00, 1.9287499e-22, 2.6894143e-01, 0.5],
          dtype=float32)>

    Args:
      x: A Tensor with type `float16`, `float32`, `float64`, `complex64`, or
        `complex128`.
      name: A name for the operation (optional).

    Returns:
      A Tensor with the same type as `x`.

    Usage Example:

    >>> x = tf.constant([-128.0, 0.0, 128.0], dtype=tf.float32)
    >>> tf.sigmoid(x)
    <tf.Tensor: shape=(3,), dtype=float32,
    numpy=array([0. , 0.5, 1. ], dtype=float32)>

    @compatibility(scipy)
    Equivalent to scipy.special.expit
    @end_compatibility
    """
    ...
@overload
def add(x: TensorCompatible, y: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Returns x + y element-wise.

    Example usages below.

    Add a scalar and a list:

    >>> x = [1, 2, 3, 4, 5]
    >>> y = 1
    >>> tf.add(x, y)
    <tf.Tensor: shape=(5,), dtype=int32, numpy=array([2, 3, 4, 5, 6],
    dtype=int32)>

    Note that binary `+` operator can be used instead:

    >>> x = tf.convert_to_tensor([1, 2, 3, 4, 5])
    >>> y = tf.convert_to_tensor(1)
    >>> x + y
    <tf.Tensor: shape=(5,), dtype=int32, numpy=array([2, 3, 4, 5, 6],
    dtype=int32)>

    Add a tensor and a list of same shape:

    >>> x = [1, 2, 3, 4, 5]
    >>> y = tf.constant([1, 2, 3, 4, 5])
    >>> tf.add(x, y)
    <tf.Tensor: shape=(5,), dtype=int32,
    numpy=array([ 2,  4,  6,  8, 10], dtype=int32)>

    **Warning**: If one of the inputs (`x` or `y`) is a tensor and the other is a
    non-tensor, the non-tensor input will adopt (or get casted to) the data type
    of the tensor input. This can potentially cause unwanted overflow or underflow
    conversion.

    For example,

    >>> x = tf.constant([1, 2], dtype=tf.int8)
    >>> y = [2**7 + 1, 2**7 + 2]
    >>> tf.add(x, y)
    <tf.Tensor: shape=(2,), dtype=int8, numpy=array([-126, -124], dtype=int8)>

    When adding two input values of different shapes, `Add` follows NumPy
    broadcasting rules. The two input array shapes are compared element-wise.
    Starting with the trailing dimensions, the two dimensions either have to be
    equal or one of them needs to be `1`.

    For example,

    >>> x = np.ones(6).reshape(1, 2, 1, 3)
    >>> y = np.ones(6).reshape(2, 1, 3, 1)
    >>> tf.add(x, y).shape.as_list()
    [2, 2, 3, 3]

    Another example with two arrays of different dimension.

    >>> x = np.ones([1, 2, 1, 4])
    >>> y = np.ones([3, 4])
    >>> tf.add(x, y).shape.as_list()
    [1, 2, 3, 4]

    The reduction version of this elementwise operation is `tf.math.reduce_sum`

    Args:
      x: A `tf.Tensor`. Must be one of the following types: bfloat16, half,
        float16, float32, float64, uint8, uint16, uint32, uint64, int8, int16,
        int32, int64, complex64, complex128, string.
      y: A `tf.Tensor`. Must have the same type as x.
      name: A name for the operation (optional)
    """
    ...
@overload
def add(x: RaggedTensor, y: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Returns x + y element-wise.

    Example usages below.

    Add a scalar and a list:

    >>> x = [1, 2, 3, 4, 5]
    >>> y = 1
    >>> tf.add(x, y)
    <tf.Tensor: shape=(5,), dtype=int32, numpy=array([2, 3, 4, 5, 6],
    dtype=int32)>

    Note that binary `+` operator can be used instead:

    >>> x = tf.convert_to_tensor([1, 2, 3, 4, 5])
    >>> y = tf.convert_to_tensor(1)
    >>> x + y
    <tf.Tensor: shape=(5,), dtype=int32, numpy=array([2, 3, 4, 5, 6],
    dtype=int32)>

    Add a tensor and a list of same shape:

    >>> x = [1, 2, 3, 4, 5]
    >>> y = tf.constant([1, 2, 3, 4, 5])
    >>> tf.add(x, y)
    <tf.Tensor: shape=(5,), dtype=int32,
    numpy=array([ 2,  4,  6,  8, 10], dtype=int32)>

    **Warning**: If one of the inputs (`x` or `y`) is a tensor and the other is a
    non-tensor, the non-tensor input will adopt (or get casted to) the data type
    of the tensor input. This can potentially cause unwanted overflow or underflow
    conversion.

    For example,

    >>> x = tf.constant([1, 2], dtype=tf.int8)
    >>> y = [2**7 + 1, 2**7 + 2]
    >>> tf.add(x, y)
    <tf.Tensor: shape=(2,), dtype=int8, numpy=array([-126, -124], dtype=int8)>

    When adding two input values of different shapes, `Add` follows NumPy
    broadcasting rules. The two input array shapes are compared element-wise.
    Starting with the trailing dimensions, the two dimensions either have to be
    equal or one of them needs to be `1`.

    For example,

    >>> x = np.ones(6).reshape(1, 2, 1, 3)
    >>> y = np.ones(6).reshape(2, 1, 3, 1)
    >>> tf.add(x, y).shape.as_list()
    [2, 2, 3, 3]

    Another example with two arrays of different dimension.

    >>> x = np.ones([1, 2, 1, 4])
    >>> y = np.ones([3, 4])
    >>> tf.add(x, y).shape.as_list()
    [1, 2, 3, 4]

    The reduction version of this elementwise operation is `tf.math.reduce_sum`

    Args:
      x: A `tf.Tensor`. Must be one of the following types: bfloat16, half,
        float16, float32, float64, uint8, uint16, uint32, uint64, int8, int16,
        int32, int64, complex64, complex128, string.
      y: A `tf.Tensor`. Must have the same type as x.
      name: A name for the operation (optional)
    """
    ...
@overload
def add_n(inputs: Iterable[TensorCompatible | IndexedSlices], name: str | None = None) -> Tensor:
    """
    Returns the element-wise sum of a list of tensors.

    All inputs in the list must have the same shape. This op does not
    [broadcast](https://docs.scipy.org/doc/numpy-1.13.0/user/basics.broadcasting.html)
    its inputs. If you need broadcasting, use `tf.math.add` (or the `+` operator)
    instead.

    For example:

    >>> a = tf.constant([[3, 5], [4, 8]])
    >>> b = tf.constant([[1, 6], [2, 9]])
    >>> tf.math.add_n([a, b, a]).numpy()
    array([[ 7, 16],
           [10, 25]], dtype=int32)

    See Also:

    * `tf.reduce_sum(inputs, axis=0)` - This performs the same mathematical
      operation, but `tf.add_n` may be more efficient because it sums the
      tensors directly. `reduce_sum` on the other hand calls
      `tf.convert_to_tensor` on the list of tensors, unnecessarily stacking them
      into a single tensor before summing.

    Args:
      inputs: A list of `tf.Tensor` or `tf.IndexedSlices` objects, each with the
        same shape and type. `tf.IndexedSlices` objects will be converted into
        dense tensors prior to adding.
      name: A name for the operation (optional).

    Returns:
      A `tf.Tensor` of the same shape and type as the elements of `inputs`.

    Raises:
      ValueError: If `inputs` don't all have same shape and dtype or the shape
      cannot be inferred.
    """
    ...
@overload
def add_n(inputs: Iterable[RaggedTensor], name: str | None = None) -> RaggedTensor:
    """
    Returns the element-wise sum of a list of tensors.

    All inputs in the list must have the same shape. This op does not
    [broadcast](https://docs.scipy.org/doc/numpy-1.13.0/user/basics.broadcasting.html)
    its inputs. If you need broadcasting, use `tf.math.add` (or the `+` operator)
    instead.

    For example:

    >>> a = tf.constant([[3, 5], [4, 8]])
    >>> b = tf.constant([[1, 6], [2, 9]])
    >>> tf.math.add_n([a, b, a]).numpy()
    array([[ 7, 16],
           [10, 25]], dtype=int32)

    See Also:

    * `tf.reduce_sum(inputs, axis=0)` - This performs the same mathematical
      operation, but `tf.add_n` may be more efficient because it sums the
      tensors directly. `reduce_sum` on the other hand calls
      `tf.convert_to_tensor` on the list of tensors, unnecessarily stacking them
      into a single tensor before summing.

    Args:
      inputs: A list of `tf.Tensor` or `tf.IndexedSlices` objects, each with the
        same shape and type. `tf.IndexedSlices` objects will be converted into
        dense tensors prior to adding.
      name: A name for the operation (optional).

    Returns:
      A `tf.Tensor` of the same shape and type as the elements of `inputs`.

    Raises:
      ValueError: If `inputs` don't all have same shape and dtype or the shape
      cannot be inferred.
    """
    ...
@overload
def subtract(x: TensorCompatible, y: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Returns x - y element-wise.

    *NOTE*: `tf.subtract` supports broadcasting. More about broadcasting
    [here](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)

    Both input and output have a range `(-inf, inf)`.

    Example usages below.

    Subtract operation between an array and a scalar:

    >>> x = [1, 2, 3, 4, 5]
    >>> y = 1
    >>> tf.subtract(x, y)
    <tf.Tensor: shape=(5,), dtype=int32, numpy=array([0, 1, 2, 3, 4], dtype=int32)>
    >>> tf.subtract(y, x)
    <tf.Tensor: shape=(5,), dtype=int32,
    numpy=array([ 0, -1, -2, -3, -4], dtype=int32)>

    Note that binary `-` operator can be used instead:

    >>> x = tf.convert_to_tensor([1, 2, 3, 4, 5])
    >>> y = tf.convert_to_tensor(1)
    >>> x - y
    <tf.Tensor: shape=(5,), dtype=int32, numpy=array([0, 1, 2, 3, 4], dtype=int32)>

    Subtract operation between an array and a tensor of same shape:

    >>> x = [1, 2, 3, 4, 5]
    >>> y = tf.constant([5, 4, 3, 2, 1])
    >>> tf.subtract(y, x)
    <tf.Tensor: shape=(5,), dtype=int32,
    numpy=array([ 4,  2,  0, -2, -4], dtype=int32)>

    **Warning**: If one of the inputs (`x` or `y`) is a tensor and the other is a
    non-tensor, the non-tensor input will adopt (or get casted to) the data type
    of the tensor input. This can potentially cause unwanted overflow or underflow
    conversion.

    For example,

    >>> x = tf.constant([1, 2], dtype=tf.int8)
    >>> y = [2**8 + 1, 2**8 + 2]
    >>> tf.subtract(x, y)
    <tf.Tensor: shape=(2,), dtype=int8, numpy=array([0, 0], dtype=int8)>

    When subtracting two input values of different shapes, `tf.subtract` follows the
    [general broadcasting rules](https://numpy.org/doc/stable/user/basics.broadcasting.html#general-broadcasting-rules)
    . The two input array shapes are compared element-wise. Starting with the
    trailing dimensions, the two dimensions either have to be equal or one of them
    needs to be `1`.

    For example,

    >>> x = np.ones(6).reshape(2, 3, 1)
    >>> y = np.ones(6).reshape(2, 1, 3)
    >>> tf.subtract(x, y)
    <tf.Tensor: shape=(2, 3, 3), dtype=float64, numpy=
    array([[[0., 0., 0.],
            [0., 0., 0.],
            [0., 0., 0.]],
           [[0., 0., 0.],
            [0., 0., 0.],
            [0., 0., 0.]]])>

    Example with inputs of different dimensions:

    >>> x = np.ones(6).reshape(2, 3, 1)
    >>> y = np.ones(6).reshape(1, 6)
    >>> tf.subtract(x, y)
    <tf.Tensor: shape=(2, 3, 6), dtype=float64, numpy=
    array([[[0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0.]],
           [[0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0.]]])>

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `uint8`, `int8`, `uint16`, `int16`, `int32`, `int64`, `complex64`, `complex128`, `uint32`, `uint64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def subtract(x: TensorCompatible | RaggedTensor, y: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Returns x - y element-wise.

    *NOTE*: `tf.subtract` supports broadcasting. More about broadcasting
    [here](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)

    Both input and output have a range `(-inf, inf)`.

    Example usages below.

    Subtract operation between an array and a scalar:

    >>> x = [1, 2, 3, 4, 5]
    >>> y = 1
    >>> tf.subtract(x, y)
    <tf.Tensor: shape=(5,), dtype=int32, numpy=array([0, 1, 2, 3, 4], dtype=int32)>
    >>> tf.subtract(y, x)
    <tf.Tensor: shape=(5,), dtype=int32,
    numpy=array([ 0, -1, -2, -3, -4], dtype=int32)>

    Note that binary `-` operator can be used instead:

    >>> x = tf.convert_to_tensor([1, 2, 3, 4, 5])
    >>> y = tf.convert_to_tensor(1)
    >>> x - y
    <tf.Tensor: shape=(5,), dtype=int32, numpy=array([0, 1, 2, 3, 4], dtype=int32)>

    Subtract operation between an array and a tensor of same shape:

    >>> x = [1, 2, 3, 4, 5]
    >>> y = tf.constant([5, 4, 3, 2, 1])
    >>> tf.subtract(y, x)
    <tf.Tensor: shape=(5,), dtype=int32,
    numpy=array([ 4,  2,  0, -2, -4], dtype=int32)>

    **Warning**: If one of the inputs (`x` or `y`) is a tensor and the other is a
    non-tensor, the non-tensor input will adopt (or get casted to) the data type
    of the tensor input. This can potentially cause unwanted overflow or underflow
    conversion.

    For example,

    >>> x = tf.constant([1, 2], dtype=tf.int8)
    >>> y = [2**8 + 1, 2**8 + 2]
    >>> tf.subtract(x, y)
    <tf.Tensor: shape=(2,), dtype=int8, numpy=array([0, 0], dtype=int8)>

    When subtracting two input values of different shapes, `tf.subtract` follows the
    [general broadcasting rules](https://numpy.org/doc/stable/user/basics.broadcasting.html#general-broadcasting-rules)
    . The two input array shapes are compared element-wise. Starting with the
    trailing dimensions, the two dimensions either have to be equal or one of them
    needs to be `1`.

    For example,

    >>> x = np.ones(6).reshape(2, 3, 1)
    >>> y = np.ones(6).reshape(2, 1, 3)
    >>> tf.subtract(x, y)
    <tf.Tensor: shape=(2, 3, 3), dtype=float64, numpy=
    array([[[0., 0., 0.],
            [0., 0., 0.],
            [0., 0., 0.]],
           [[0., 0., 0.],
            [0., 0., 0.],
            [0., 0., 0.]]])>

    Example with inputs of different dimensions:

    >>> x = np.ones(6).reshape(2, 3, 1)
    >>> y = np.ones(6).reshape(1, 6)
    >>> tf.subtract(x, y)
    <tf.Tensor: shape=(2, 3, 6), dtype=float64, numpy=
    array([[[0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0.]],
           [[0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0.]]])>

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `uint8`, `int8`, `uint16`, `int16`, `int32`, `int64`, `complex64`, `complex128`, `uint32`, `uint64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def subtract(
    x: TensorCompatible | RaggedTensor, y: TensorCompatible | RaggedTensor, name: str | None = None
) -> Tensor | RaggedTensor:
    """
    Returns x - y element-wise.

    *NOTE*: `tf.subtract` supports broadcasting. More about broadcasting
    [here](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)

    Both input and output have a range `(-inf, inf)`.

    Example usages below.

    Subtract operation between an array and a scalar:

    >>> x = [1, 2, 3, 4, 5]
    >>> y = 1
    >>> tf.subtract(x, y)
    <tf.Tensor: shape=(5,), dtype=int32, numpy=array([0, 1, 2, 3, 4], dtype=int32)>
    >>> tf.subtract(y, x)
    <tf.Tensor: shape=(5,), dtype=int32,
    numpy=array([ 0, -1, -2, -3, -4], dtype=int32)>

    Note that binary `-` operator can be used instead:

    >>> x = tf.convert_to_tensor([1, 2, 3, 4, 5])
    >>> y = tf.convert_to_tensor(1)
    >>> x - y
    <tf.Tensor: shape=(5,), dtype=int32, numpy=array([0, 1, 2, 3, 4], dtype=int32)>

    Subtract operation between an array and a tensor of same shape:

    >>> x = [1, 2, 3, 4, 5]
    >>> y = tf.constant([5, 4, 3, 2, 1])
    >>> tf.subtract(y, x)
    <tf.Tensor: shape=(5,), dtype=int32,
    numpy=array([ 4,  2,  0, -2, -4], dtype=int32)>

    **Warning**: If one of the inputs (`x` or `y`) is a tensor and the other is a
    non-tensor, the non-tensor input will adopt (or get casted to) the data type
    of the tensor input. This can potentially cause unwanted overflow or underflow
    conversion.

    For example,

    >>> x = tf.constant([1, 2], dtype=tf.int8)
    >>> y = [2**8 + 1, 2**8 + 2]
    >>> tf.subtract(x, y)
    <tf.Tensor: shape=(2,), dtype=int8, numpy=array([0, 0], dtype=int8)>

    When subtracting two input values of different shapes, `tf.subtract` follows the
    [general broadcasting rules](https://numpy.org/doc/stable/user/basics.broadcasting.html#general-broadcasting-rules)
    . The two input array shapes are compared element-wise. Starting with the
    trailing dimensions, the two dimensions either have to be equal or one of them
    needs to be `1`.

    For example,

    >>> x = np.ones(6).reshape(2, 3, 1)
    >>> y = np.ones(6).reshape(2, 1, 3)
    >>> tf.subtract(x, y)
    <tf.Tensor: shape=(2, 3, 3), dtype=float64, numpy=
    array([[[0., 0., 0.],
            [0., 0., 0.],
            [0., 0., 0.]],
           [[0., 0., 0.],
            [0., 0., 0.],
            [0., 0., 0.]]])>

    Example with inputs of different dimensions:

    >>> x = np.ones(6).reshape(2, 3, 1)
    >>> y = np.ones(6).reshape(1, 6)
    >>> tf.subtract(x, y)
    <tf.Tensor: shape=(2, 3, 6), dtype=float64, numpy=
    array([[[0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0.]],
           [[0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0.]]])>

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `uint8`, `int8`, `uint16`, `int16`, `int32`, `int64`, `complex64`, `complex128`, `uint32`, `uint64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def multiply(x: TensorCompatible, y: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Returns an element-wise x * y.

    For example:

    >>> x = tf.constant(([1, 2, 3, 4]))
    >>> tf.math.multiply(x, x)
    <tf.Tensor: shape=(4,), dtype=..., numpy=array([ 1,  4,  9, 16], dtype=int32)>

    Since `tf.math.multiply` will convert its arguments to `Tensor`s, you can also
    pass in non-`Tensor` arguments:

    >>> tf.math.multiply(7,6)
    <tf.Tensor: shape=(), dtype=int32, numpy=42>

    If `x.shape` is not the same as `y.shape`, they will be broadcast to a
    compatible shape. (More about broadcasting
    [here](https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html).)

    For example:

    >>> x = tf.ones([1, 2]);
    >>> y = tf.ones([2, 1]);
    >>> x * y  # Taking advantage of operator overriding
    <tf.Tensor: shape=(2, 2), dtype=float32, numpy=
    array([[1., 1.],
         [1., 1.]], dtype=float32)>

    The reduction version of this elementwise operation is `tf.math.reduce_prod`

    Args:
      x: A Tensor. Must be one of the following types: `bfloat16`,
        `half`, `float32`, `float64`, `uint8`, `int8`, `uint16`,
        `int16`, `int32`, `int64`, `complex64`, `complex128`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:

    A `Tensor`.  Has the same type as `x`.

    Raises:

     * InvalidArgumentError: When `x` and `y` have incompatible shapes or types.
    """
    ...
@overload
def multiply(x: RaggedTensor, y: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Returns an element-wise x * y.

    For example:

    >>> x = tf.constant(([1, 2, 3, 4]))
    >>> tf.math.multiply(x, x)
    <tf.Tensor: shape=(4,), dtype=..., numpy=array([ 1,  4,  9, 16], dtype=int32)>

    Since `tf.math.multiply` will convert its arguments to `Tensor`s, you can also
    pass in non-`Tensor` arguments:

    >>> tf.math.multiply(7,6)
    <tf.Tensor: shape=(), dtype=int32, numpy=42>

    If `x.shape` is not the same as `y.shape`, they will be broadcast to a
    compatible shape. (More about broadcasting
    [here](https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html).)

    For example:

    >>> x = tf.ones([1, 2]);
    >>> y = tf.ones([2, 1]);
    >>> x * y  # Taking advantage of operator overriding
    <tf.Tensor: shape=(2, 2), dtype=float32, numpy=
    array([[1., 1.],
         [1., 1.]], dtype=float32)>

    The reduction version of this elementwise operation is `tf.math.reduce_prod`

    Args:
      x: A Tensor. Must be one of the following types: `bfloat16`,
        `half`, `float32`, `float64`, `uint8`, `int8`, `uint16`,
        `int16`, `int32`, `int64`, `complex64`, `complex128`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:

    A `Tensor`.  Has the same type as `x`.

    Raises:

     * InvalidArgumentError: When `x` and `y` have incompatible shapes or types.
    """
    ...
@overload
def multiply_no_nan(x: TensorCompatible, y: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Computes the product of x and y and returns 0 if the y is zero, even if x is NaN or infinite.

    Note this is noncommutative: if y is NaN or infinite and x is 0, the result
    will be NaN.

    Args:
      x: A `Tensor`. Must be one of the following types: `float32`, `float64`.
      y: A `Tensor` whose dtype is compatible with `x`.
      name: A name for the operation (optional).

    Returns:
      The element-wise value of the x times y.
    """
    ...
@overload
def multiply_no_nan(x: RaggedTensor, y: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Computes the product of x and y and returns 0 if the y is zero, even if x is NaN or infinite.

    Note this is noncommutative: if y is NaN or infinite and x is 0, the result
    will be NaN.

    Args:
      x: A `Tensor`. Must be one of the following types: `float32`, `float64`.
      y: A `Tensor` whose dtype is compatible with `x`.
      name: A name for the operation (optional).

    Returns:
      The element-wise value of the x times y.
    """
    ...
@overload
def divide(x: TensorCompatible, y: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Computes Python style division of `x` by `y`.

    For example:

    >>> x = tf.constant([16, 12, 11])
    >>> y = tf.constant([4, 6, 2])
    >>> tf.divide(x,y)
    <tf.Tensor: shape=(3,), dtype=float64,
    numpy=array([4. , 2. , 5.5])>

    Args:
      x: A `Tensor`
      y: A `Tensor`
      name: A name for the operation (optional).

    Returns:
      A `Tensor` with same shape as input
    """
    ...
@overload
def divide(x: RaggedTensor, y: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Computes Python style division of `x` by `y`.

    For example:

    >>> x = tf.constant([16, 12, 11])
    >>> y = tf.constant([4, 6, 2])
    >>> tf.divide(x,y)
    <tf.Tensor: shape=(3,), dtype=float64,
    numpy=array([4. , 2. , 5.5])>

    Args:
      x: A `Tensor`
      y: A `Tensor`
      name: A name for the operation (optional).

    Returns:
      A `Tensor` with same shape as input
    """
    ...
@overload
def divide_no_nan(x: TensorCompatible, y: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Computes a safe divide which returns 0 if `y` (denominator) is zero.

    For example:

    >>> tf.constant(3.0) / 0.0
    <tf.Tensor: shape=(), dtype=float32, numpy=inf>
    >>> tf.math.divide_no_nan(3.0, 0.0)
    <tf.Tensor: shape=(), dtype=float32, numpy=0.0>

    Note that 0 is returned if `y` is 0 even if `x` is nonfinite:

    >>> tf.math.divide_no_nan(np.nan, 0.0)
    <tf.Tensor: shape=(), dtype=float32, numpy=0.0>

    Args:
      x: A `Tensor` of a floating or integer dtype.
      y: A `Tensor` with the same dtype as `x` and a compatible shape.
      name: A name for the operation (optional).

    Returns:
      The element-wise quotient as in `tf.math.divide(x, y)`,
      except that division by zero produces `0.0`, not `nan`.
    """
    ...
@overload
def divide_no_nan(x: RaggedTensor, y: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Computes a safe divide which returns 0 if `y` (denominator) is zero.

    For example:

    >>> tf.constant(3.0) / 0.0
    <tf.Tensor: shape=(), dtype=float32, numpy=inf>
    >>> tf.math.divide_no_nan(3.0, 0.0)
    <tf.Tensor: shape=(), dtype=float32, numpy=0.0>

    Note that 0 is returned if `y` is 0 even if `x` is nonfinite:

    >>> tf.math.divide_no_nan(np.nan, 0.0)
    <tf.Tensor: shape=(), dtype=float32, numpy=0.0>

    Args:
      x: A `Tensor` of a floating or integer dtype.
      y: A `Tensor` with the same dtype as `x` and a compatible shape.
      name: A name for the operation (optional).

    Returns:
      The element-wise quotient as in `tf.math.divide(x, y)`,
      except that division by zero produces `0.0`, not `nan`.
    """
    ...
@overload
def floormod(x: TensorCompatible, y: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Returns element-wise remainder of division.

    This follows Python semantics in that the
    result here is consistent with a flooring divide. E.g.
    `floor(x / y) * y + floormod(x, y) = x`, regardless of the signs of x and y.

    *NOTE*: `math.floormod` supports broadcasting. More about broadcasting
    [here](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)

    Args:
      x: A `Tensor`. Must be one of the following types: `int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`, `bfloat16`, `half`, `float32`, `float64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def floormod(x: RaggedTensor, y: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Returns element-wise remainder of division.

    This follows Python semantics in that the
    result here is consistent with a flooring divide. E.g.
    `floor(x / y) * y + floormod(x, y) = x`, regardless of the signs of x and y.

    *NOTE*: `math.floormod` supports broadcasting. More about broadcasting
    [here](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)

    Args:
      x: A `Tensor`. Must be one of the following types: `int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`, `bfloat16`, `half`, `float32`, `float64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def ceil(x: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Return the ceiling of the input, element-wise.

    For example:

    >>> tf.math.ceil([-1.7, -1.5, -0.2, 0.2, 1.5, 1.7, 2.0])
    <tf.Tensor: shape=(7,), dtype=float32,
    numpy=array([-1., -1., -0.,  1.,  2.,  2.,  2.], dtype=float32)>

    Args:
      x: A `tf.Tensor`. Must be one of the following types: `bfloat16`, `half`,
        `float32`, `float64`. `int32`
      name: A name for the operation (optional).

    Returns:
      A `tf.Tensor`. Has the same type as `x`.

    @compatibility(numpy)
    Equivalent to np.ceil
    @end_compatibility
    """
    ...
@overload
def ceil(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Return the ceiling of the input, element-wise.

    For example:

    >>> tf.math.ceil([-1.7, -1.5, -0.2, 0.2, 1.5, 1.7, 2.0])
    <tf.Tensor: shape=(7,), dtype=float32,
    numpy=array([-1., -1., -0.,  1.,  2.,  2.,  2.], dtype=float32)>

    Args:
      x: A `tf.Tensor`. Must be one of the following types: `bfloat16`, `half`,
        `float32`, `float64`. `int32`
      name: A name for the operation (optional).

    Returns:
      A `tf.Tensor`. Has the same type as `x`.

    @compatibility(numpy)
    Equivalent to np.ceil
    @end_compatibility
    """
    ...
@overload
def floor(x: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Returns element-wise largest integer not greater than x.

    Both input range is `(-inf, inf)` and the
    output range consists of all integer values.

    For example:

    >>> x = tf.constant([1.3324, -1.5, 5.555, -2.532, 0.99, float("inf")])
    >>> tf.floor(x).numpy()
    array([ 1., -2.,  5., -3.,  0., inf], dtype=float32)

    Args:
      x:  A `Tensor`. Must be one of the following types: `bfloat16`, `half`,
        `float32`, `float64`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as x.
    """
    ...
@overload
def floor(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Returns element-wise largest integer not greater than x.

    Both input range is `(-inf, inf)` and the
    output range consists of all integer values.

    For example:

    >>> x = tf.constant([1.3324, -1.5, 5.555, -2.532, 0.99, float("inf")])
    >>> tf.floor(x).numpy()
    array([ 1., -2.,  5., -3.,  0., inf], dtype=float32)

    Args:
      x:  A `Tensor`. Must be one of the following types: `bfloat16`, `half`,
        `float32`, `float64`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as x.
    """
    ...

# Uses isinstance on list/tuple so other Sequence types are not supported. The TypeVar is to
# behave covariantly.
def accumulate_n(
    inputs: list[_TensorCompatibleT] | tuple[_TensorCompatibleT, ...],
    shape: ShapeLike | None = None,
    tensor_dtype: DTypeLike | None = None,
    name: str | None = None,
) -> Tensor:
    """
    Returns the element-wise sum of a list of tensors. (deprecated)

    Deprecated: THIS FUNCTION IS DEPRECATED. It will be removed in a future version.
    Instructions for updating:
    Use `tf.math.add_n` Instead

    Optionally, pass `shape` and `tensor_dtype` for shape and type checking,
    otherwise, these are inferred.

    For example:

    >>> a = tf.constant([[1, 2], [3, 4]])
    >>> b = tf.constant([[5, 0], [0, 6]])
    >>> tf.math.accumulate_n([a, b, a]).numpy()
    array([[ 7, 4],
           [ 6, 14]], dtype=int32)

    >>> # Explicitly pass shape and type
    >>> tf.math.accumulate_n(
    ...     [a, b, a], shape=[2, 2], tensor_dtype=tf.int32).numpy()
    array([[ 7,  4],
           [ 6, 14]], dtype=int32)

    Note: The input must be a list or tuple. This function does not handle
    `IndexedSlices`

    See Also:

    * `tf.reduce_sum(inputs, axis=0)` - This performe the same mathematical
      operation, but `tf.add_n` may be more efficient because it sums the
      tensors directly. `reduce_sum` on the other hand calls
      `tf.convert_to_tensor` on the list of tensors, unncessairly stacking them
      into a single tensor before summing.
    * `tf.add_n` - This is another python wrapper for the same Op. It has
      nearly identical functionality.

    Args:
      inputs: A list of `Tensor` objects, each with same shape and type.
      shape: Expected shape of elements of `inputs` (optional). Also controls the
        output shape of this op, which may affect type inference in other ops. A
        value of `None` means "infer the input shape from the shapes in `inputs`".
      tensor_dtype: Expected data type of `inputs` (optional). A value of `None`
        means "infer the input dtype from `inputs[0]`".
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of same shape and type as the elements of `inputs`.

    Raises:
      ValueError: If `inputs` don't all have same shape and dtype or the shape
      cannot be inferred.
    """
    ...
@overload
def pow(x: TensorCompatible, y: TensorCompatible, name: str | None = None) -> Tensor:
    r"""
    Computes the power of one value to another.

    Given a tensor `x` and a tensor `y`, this operation computes \\(x^y\\) for
    corresponding elements in `x` and `y`. For example:

    ```python
    x = tf.constant([[2, 2], [3, 3]])
    y = tf.constant([[8, 16], [2, 3]])
    tf.pow(x, y)  # [[256, 65536], [9, 27]]
    ```

    Args:
      x: A `Tensor` of type `float16`, `float32`, `float64`, `int32`, `int64`,
        `complex64`, or `complex128`.
      y: A `Tensor` of type `float16`, `float32`, `float64`, `int32`, `int64`,
        `complex64`, or `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`.
    """
    ...
@overload
def pow(x: RaggedTensor, y: RaggedTensor, name: str | None = None) -> RaggedTensor:
    r"""
    Computes the power of one value to another.

    Given a tensor `x` and a tensor `y`, this operation computes \\(x^y\\) for
    corresponding elements in `x` and `y`. For example:

    ```python
    x = tf.constant([[2, 2], [3, 3]])
    y = tf.constant([[8, 16], [2, 3]])
    tf.pow(x, y)  # [[256, 65536], [9, 27]]
    ```

    Args:
      x: A `Tensor` of type `float16`, `float32`, `float64`, `int32`, `int64`,
        `complex64`, or `complex128`.
      y: A `Tensor` of type `float16`, `float32`, `float64`, `int32`, `int64`,
        `complex64`, or `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`.
    """
    ...
@overload
def reciprocal(x: TensorCompatible, name: str | None = None) -> Tensor:
    r"""
    Computes the reciprocal of x element-wise.

    I.e., \\(y = 1 / x\\).

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `int8`, `int16`, `int32`, `int64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def reciprocal(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    r"""
    Computes the reciprocal of x element-wise.

    I.e., \\(y = 1 / x\\).

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `int8`, `int16`, `int32`, `int64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def is_nan(x: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Returns which elements of x are NaN.

    @compatibility(numpy)
    Equivalent to np.isnan
    @end_compatibility

    Example:

    ```python
    x = tf.constant([5.0, np.nan, 6.8, np.nan, np.inf])
    tf.math.is_nan(x) ==> [False, True, False, True, False]
    ```

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `bool`.
    """
    ...
@overload
def is_nan(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Returns which elements of x are NaN.

    @compatibility(numpy)
    Equivalent to np.isnan
    @end_compatibility

    Example:

    ```python
    x = tf.constant([5.0, np.nan, 6.8, np.nan, np.inf])
    tf.math.is_nan(x) ==> [False, True, False, True, False]
    ```

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `bool`.
    """
    ...
@overload
def minimum(x: TensorCompatible, y: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Returns the min of x and y (i.e. x < y ? x : y) element-wise.

    Both inputs are number-type tensors (except complex).  `minimum` expects that
    both tensors have the same `dtype`.

    Examples:

    >>> x = tf.constant([0., 0., 0., 0.])
    >>> y = tf.constant([-5., -2., 0., 3.])
    >>> tf.math.minimum(x, y)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=array([-5., -2., 0., 0.], dtype=float32)>

    Note that `minimum` supports [broadcast semantics](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html) for `x` and `y`.

    >>> x = tf.constant([-5., 0., 0., 0.])
    >>> y = tf.constant([-3.])
    >>> tf.math.minimum(x, y)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=array([-5., -3., -3., -3.], dtype=float32)>

    The reduction version of this elementwise operation is `tf.math.reduce_min`

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `int8`, `uint8`, `int16`, `uint16`, `int32`, `uint32`, `int64`, `uint64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def minimum(x: RaggedTensor, y: TensorCompatible | RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Returns the min of x and y (i.e. x < y ? x : y) element-wise.

    Both inputs are number-type tensors (except complex).  `minimum` expects that
    both tensors have the same `dtype`.

    Examples:

    >>> x = tf.constant([0., 0., 0., 0.])
    >>> y = tf.constant([-5., -2., 0., 3.])
    >>> tf.math.minimum(x, y)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=array([-5., -2., 0., 0.], dtype=float32)>

    Note that `minimum` supports [broadcast semantics](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html) for `x` and `y`.

    >>> x = tf.constant([-5., 0., 0., 0.])
    >>> y = tf.constant([-3.])
    >>> tf.math.minimum(x, y)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=array([-5., -3., -3., -3.], dtype=float32)>

    The reduction version of this elementwise operation is `tf.math.reduce_min`

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `int8`, `uint8`, `int16`, `uint16`, `int32`, `uint32`, `int64`, `uint64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def minimum(x: TensorCompatible | RaggedTensor, y: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Returns the min of x and y (i.e. x < y ? x : y) element-wise.

    Both inputs are number-type tensors (except complex).  `minimum` expects that
    both tensors have the same `dtype`.

    Examples:

    >>> x = tf.constant([0., 0., 0., 0.])
    >>> y = tf.constant([-5., -2., 0., 3.])
    >>> tf.math.minimum(x, y)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=array([-5., -2., 0., 0.], dtype=float32)>

    Note that `minimum` supports [broadcast semantics](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html) for `x` and `y`.

    >>> x = tf.constant([-5., 0., 0., 0.])
    >>> y = tf.constant([-3.])
    >>> tf.math.minimum(x, y)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=array([-5., -3., -3., -3.], dtype=float32)>

    The reduction version of this elementwise operation is `tf.math.reduce_min`

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `int8`, `uint8`, `int16`, `uint16`, `int32`, `uint32`, `int64`, `uint64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def maximum(x: TensorCompatible, y: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Returns the max of x and y (i.e. x > y ? x : y) element-wise.

    Example:

    >>> x = tf.constant([0., 0., 0., 0.])
    >>> y = tf.constant([-2., 0., 2., 5.])
    >>> tf.math.maximum(x, y)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=array([0., 0., 2., 5.], dtype=float32)>

    Note that `maximum` supports [broadcast semantics](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html) for `x` and `y`.

    >>> x = tf.constant([-5., 0., 0., 0.])
    >>> y = tf.constant([-3.])
    >>> tf.math.maximum(x, y)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=array([-3., 0., 0., 0.], dtype=float32)>

    The reduction version of this elementwise operation is `tf.math.reduce_max`

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `int8`, `uint8`, `int16`, `uint16`, `int32`, `uint32`, `int64`, `uint64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def maximum(x: RaggedTensor, y: TensorCompatible | RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Returns the max of x and y (i.e. x > y ? x : y) element-wise.

    Example:

    >>> x = tf.constant([0., 0., 0., 0.])
    >>> y = tf.constant([-2., 0., 2., 5.])
    >>> tf.math.maximum(x, y)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=array([0., 0., 2., 5.], dtype=float32)>

    Note that `maximum` supports [broadcast semantics](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html) for `x` and `y`.

    >>> x = tf.constant([-5., 0., 0., 0.])
    >>> y = tf.constant([-3.])
    >>> tf.math.maximum(x, y)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=array([-3., 0., 0., 0.], dtype=float32)>

    The reduction version of this elementwise operation is `tf.math.reduce_max`

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `int8`, `uint8`, `int16`, `uint16`, `int32`, `uint32`, `int64`, `uint64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def maximum(x: TensorCompatible | RaggedTensor, y: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Returns the max of x and y (i.e. x > y ? x : y) element-wise.

    Example:

    >>> x = tf.constant([0., 0., 0., 0.])
    >>> y = tf.constant([-2., 0., 2., 5.])
    >>> tf.math.maximum(x, y)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=array([0., 0., 2., 5.], dtype=float32)>

    Note that `maximum` supports [broadcast semantics](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html) for `x` and `y`.

    >>> x = tf.constant([-5., 0., 0., 0.])
    >>> y = tf.constant([-3.])
    >>> tf.math.maximum(x, y)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=array([-3., 0., 0., 0.], dtype=float32)>

    The reduction version of this elementwise operation is `tf.math.reduce_max`

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `int8`, `uint8`, `int16`, `uint16`, `int32`, `uint32`, `int64`, `uint64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.
    """
    ...
@overload
def logical_not(x: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Returns the truth value of `NOT x` element-wise.

    Example:

    >>> tf.math.logical_not(tf.constant([True, False]))
    <tf.Tensor: shape=(2,), dtype=bool, numpy=array([False,  True])>

    Args:
      x: A `Tensor` of type `bool`. A `Tensor` of type `bool`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `bool`.
    """
    ...
@overload
def logical_not(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Returns the truth value of `NOT x` element-wise.

    Example:

    >>> tf.math.logical_not(tf.constant([True, False]))
    <tf.Tensor: shape=(2,), dtype=bool, numpy=array([False,  True])>

    Args:
      x: A `Tensor` of type `bool`. A `Tensor` of type `bool`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `bool`.
    """
    ...
@overload
def logical_and(x: TensorCompatible, y: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Returns the truth value of x AND y element-wise.

    Logical AND function.

    Requires that `x` and `y` have the same shape or have
    [broadcast-compatible](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)
    shapes. For example, `x` and `y` can be:

      - Two single elements of type `bool`.
      - One `tf.Tensor` of type `bool` and one single `bool`, where the result will
        be calculated by applying logical AND with the single element to each
        element in the larger Tensor.
      - Two `tf.Tensor` objects of type `bool` of the same shape. In this case,
        the result will be the element-wise logical AND of the two input tensors.

    You can also use the `&` operator instead.

    Usage:

      >>> a = tf.constant([True])
      >>> b = tf.constant([False])
      >>> tf.math.logical_and(a, b)
      <tf.Tensor: shape=(1,), dtype=bool, numpy=array([False])>
      >>> a & b
      <tf.Tensor: shape=(1,), dtype=bool, numpy=array([False])>

      >>> c = tf.constant([True])
      >>> x = tf.constant([False, True, True, False])
      >>> tf.math.logical_and(c, x)
      <tf.Tensor: shape=(4,), dtype=bool, numpy=array([False,  True,  True, False])>
      >>> c & x
      <tf.Tensor: shape=(4,), dtype=bool, numpy=array([False,  True,  True, False])>

      >>> y = tf.constant([False, False, True, True])
      >>> z = tf.constant([False, True, False, True])
      >>> tf.math.logical_and(y, z)
      <tf.Tensor: shape=(4,), dtype=bool, numpy=array([False, False, False, True])>
      >>> y & z
      <tf.Tensor: shape=(4,), dtype=bool, numpy=array([False, False, False, True])>

      This op also supports broadcasting

      >>> tf.logical_and([[True, False]], [[True], [False]])
      <tf.Tensor: shape=(2, 2), dtype=bool, numpy=
        array([[ True, False],
               [False, False]])>

    The reduction version of this elementwise operation is `tf.math.reduce_all`.

    Args:
        x: A `tf.Tensor` of type bool.
        y: A `tf.Tensor` of type bool.
        name: A name for the operation (optional).

    Returns:
      A `tf.Tensor` of type bool with the shape that `x` and `y` broadcast to.

    Args:
      x: A `Tensor` of type `bool`.
      y: A `Tensor` of type `bool`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `bool`.
    """
    ...
@overload
def logical_and(x: RaggedTensor, y: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Returns the truth value of x AND y element-wise.

    Logical AND function.

    Requires that `x` and `y` have the same shape or have
    [broadcast-compatible](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)
    shapes. For example, `x` and `y` can be:

      - Two single elements of type `bool`.
      - One `tf.Tensor` of type `bool` and one single `bool`, where the result will
        be calculated by applying logical AND with the single element to each
        element in the larger Tensor.
      - Two `tf.Tensor` objects of type `bool` of the same shape. In this case,
        the result will be the element-wise logical AND of the two input tensors.

    You can also use the `&` operator instead.

    Usage:

      >>> a = tf.constant([True])
      >>> b = tf.constant([False])
      >>> tf.math.logical_and(a, b)
      <tf.Tensor: shape=(1,), dtype=bool, numpy=array([False])>
      >>> a & b
      <tf.Tensor: shape=(1,), dtype=bool, numpy=array([False])>

      >>> c = tf.constant([True])
      >>> x = tf.constant([False, True, True, False])
      >>> tf.math.logical_and(c, x)
      <tf.Tensor: shape=(4,), dtype=bool, numpy=array([False,  True,  True, False])>
      >>> c & x
      <tf.Tensor: shape=(4,), dtype=bool, numpy=array([False,  True,  True, False])>

      >>> y = tf.constant([False, False, True, True])
      >>> z = tf.constant([False, True, False, True])
      >>> tf.math.logical_and(y, z)
      <tf.Tensor: shape=(4,), dtype=bool, numpy=array([False, False, False, True])>
      >>> y & z
      <tf.Tensor: shape=(4,), dtype=bool, numpy=array([False, False, False, True])>

      This op also supports broadcasting

      >>> tf.logical_and([[True, False]], [[True], [False]])
      <tf.Tensor: shape=(2, 2), dtype=bool, numpy=
        array([[ True, False],
               [False, False]])>

    The reduction version of this elementwise operation is `tf.math.reduce_all`.

    Args:
        x: A `tf.Tensor` of type bool.
        y: A `tf.Tensor` of type bool.
        name: A name for the operation (optional).

    Returns:
      A `tf.Tensor` of type bool with the shape that `x` and `y` broadcast to.

    Args:
      x: A `Tensor` of type `bool`.
      y: A `Tensor` of type `bool`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `bool`.
    """
    ...
@overload
def logical_or(x: TensorCompatible, y: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Returns the truth value of x OR y element-wise.

    Logical OR function.

    Requires that `x` and `y` have the same shape or have
    [broadcast-compatible](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)
    shapes. For example, `x` and `y` can be:

    - Two single elements of type `bool`.
    - One `tf.Tensor` of type `bool` and one single `bool`, where the result will
      be calculated by applying logical OR with the single element to each
      element in the larger Tensor.
    - Two `tf.Tensor` objects of type `bool` of the same shape. In this case,
      the result will be the element-wise logical OR of the two input tensors.

    You can also use the `|` operator instead.

    Usage:

      >>> a = tf.constant([True])
      >>> b = tf.constant([False])
      >>> tf.math.logical_or(a, b)
      <tf.Tensor: shape=(1,), dtype=bool, numpy=array([ True])>
      >>> a | b
      <tf.Tensor: shape=(1,), dtype=bool, numpy=array([ True])>

      >>> c = tf.constant([False])
      >>> x = tf.constant([False, True, True, False])
      >>> tf.math.logical_or(c, x)
      <tf.Tensor: shape=(4,), dtype=bool, numpy=array([False, True,  True, False])>
      >>> c | x
      <tf.Tensor: shape=(4,), dtype=bool, numpy=array([False, True,  True, False])>

      >>> y = tf.constant([False, False, True, True])
      >>> z = tf.constant([False, True, False, True])
      >>> tf.math.logical_or(y, z)
      <tf.Tensor: shape=(4,), dtype=bool, numpy=array([False, True, True, True])>
      >>> y | z
      <tf.Tensor: shape=(4,), dtype=bool, numpy=array([False, True, True, True])>

      This op also supports broadcasting

      >>> tf.logical_or([[True, False]], [[True], [False]])
      <tf.Tensor: shape=(2, 2), dtype=bool, numpy=
      array([[ True,  True],
           [ True, False]])>

    The reduction version of this elementwise operation is `tf.math.reduce_any`.

    Args:
        x: A `tf.Tensor` of type bool.
        y: A `tf.Tensor` of type bool.
        name: A name for the operation (optional).

    Returns:
      A `tf.Tensor` of type bool with the shape that `x` and `y` broadcast to.

    Args:
      x: A `Tensor` of type `bool`.
      y: A `Tensor` of type `bool`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `bool`.
    """
    ...
@overload
def logical_or(x: RaggedTensor, y: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Returns the truth value of x OR y element-wise.

    Logical OR function.

    Requires that `x` and `y` have the same shape or have
    [broadcast-compatible](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)
    shapes. For example, `x` and `y` can be:

    - Two single elements of type `bool`.
    - One `tf.Tensor` of type `bool` and one single `bool`, where the result will
      be calculated by applying logical OR with the single element to each
      element in the larger Tensor.
    - Two `tf.Tensor` objects of type `bool` of the same shape. In this case,
      the result will be the element-wise logical OR of the two input tensors.

    You can also use the `|` operator instead.

    Usage:

      >>> a = tf.constant([True])
      >>> b = tf.constant([False])
      >>> tf.math.logical_or(a, b)
      <tf.Tensor: shape=(1,), dtype=bool, numpy=array([ True])>
      >>> a | b
      <tf.Tensor: shape=(1,), dtype=bool, numpy=array([ True])>

      >>> c = tf.constant([False])
      >>> x = tf.constant([False, True, True, False])
      >>> tf.math.logical_or(c, x)
      <tf.Tensor: shape=(4,), dtype=bool, numpy=array([False, True,  True, False])>
      >>> c | x
      <tf.Tensor: shape=(4,), dtype=bool, numpy=array([False, True,  True, False])>

      >>> y = tf.constant([False, False, True, True])
      >>> z = tf.constant([False, True, False, True])
      >>> tf.math.logical_or(y, z)
      <tf.Tensor: shape=(4,), dtype=bool, numpy=array([False, True, True, True])>
      >>> y | z
      <tf.Tensor: shape=(4,), dtype=bool, numpy=array([False, True, True, True])>

      This op also supports broadcasting

      >>> tf.logical_or([[True, False]], [[True], [False]])
      <tf.Tensor: shape=(2, 2), dtype=bool, numpy=
      array([[ True,  True],
           [ True, False]])>

    The reduction version of this elementwise operation is `tf.math.reduce_any`.

    Args:
        x: A `tf.Tensor` of type bool.
        y: A `tf.Tensor` of type bool.
        name: A name for the operation (optional).

    Returns:
      A `tf.Tensor` of type bool with the shape that `x` and `y` broadcast to.

    Args:
      x: A `Tensor` of type `bool`.
      y: A `Tensor` of type `bool`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `bool`.
    """
    ...
@overload
def logical_xor(x: TensorCompatible, y: TensorCompatible, name: str | None = "LogicalXor") -> Tensor:
    """
    Logical XOR function.

    x ^ y = (x | y) & ~(x & y)

    Requires that `x` and `y` have the same shape or have
    [broadcast-compatible](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)
    shapes. For example, `x` and `y` can be:

    - Two single elements of type `bool`
    - One `tf.Tensor` of type `bool` and one single `bool`, where the result will
      be calculated by applying logical XOR with the single element to each
      element in the larger Tensor.
    - Two `tf.Tensor` objects of type `bool` of the same shape. In this case,
      the result will be the element-wise logical XOR of the two input tensors.

    Usage:

    >>> a = tf.constant([True])
    >>> b = tf.constant([False])
    >>> tf.math.logical_xor(a, b)
    <tf.Tensor: shape=(1,), dtype=bool, numpy=array([ True])>

    >>> c = tf.constant([True])
    >>> x = tf.constant([False, True, True, False])
    >>> tf.math.logical_xor(c, x)
    <tf.Tensor: shape=(4,), dtype=bool, numpy=array([ True, False, False,  True])>

    >>> y = tf.constant([False, False, True, True])
    >>> z = tf.constant([False, True, False, True])
    >>> tf.math.logical_xor(y, z)
    <tf.Tensor: shape=(4,), dtype=bool, numpy=array([False,  True,  True, False])>

    Args:
        x: A `tf.Tensor` type bool.
        y: A `tf.Tensor` of type bool.
        name: A name for the operation (optional).

    Returns:
      A `tf.Tensor` of type bool with the same size as that of x or y.
    """
    ...
@overload
def logical_xor(x: RaggedTensor, y: RaggedTensor, name: str | None = "LogicalXor") -> RaggedTensor:
    """
    Logical XOR function.

    x ^ y = (x | y) & ~(x & y)

    Requires that `x` and `y` have the same shape or have
    [broadcast-compatible](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)
    shapes. For example, `x` and `y` can be:

    - Two single elements of type `bool`
    - One `tf.Tensor` of type `bool` and one single `bool`, where the result will
      be calculated by applying logical XOR with the single element to each
      element in the larger Tensor.
    - Two `tf.Tensor` objects of type `bool` of the same shape. In this case,
      the result will be the element-wise logical XOR of the two input tensors.

    Usage:

    >>> a = tf.constant([True])
    >>> b = tf.constant([False])
    >>> tf.math.logical_xor(a, b)
    <tf.Tensor: shape=(1,), dtype=bool, numpy=array([ True])>

    >>> c = tf.constant([True])
    >>> x = tf.constant([False, True, True, False])
    >>> tf.math.logical_xor(c, x)
    <tf.Tensor: shape=(4,), dtype=bool, numpy=array([ True, False, False,  True])>

    >>> y = tf.constant([False, False, True, True])
    >>> z = tf.constant([False, True, False, True])
    >>> tf.math.logical_xor(y, z)
    <tf.Tensor: shape=(4,), dtype=bool, numpy=array([False,  True,  True, False])>

    Args:
        x: A `tf.Tensor` type bool.
        y: A `tf.Tensor` of type bool.
        name: A name for the operation (optional).

    Returns:
      A `tf.Tensor` of type bool with the same size as that of x or y.
    """
    ...
@overload
def equal(x: TensorCompatible, y: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Returns the truth value of (x == y) element-wise.

    Performs a [broadcast](
    https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html) with the
    arguments and then an element-wise equality comparison, returning a Tensor of
    boolean values.

    For example:

    >>> x = tf.constant([2, 4])
    >>> y = tf.constant(2)
    >>> tf.math.equal(x, y)
    <tf.Tensor: shape=(2,), dtype=bool, numpy=array([ True,  False])>

    >>> x = tf.constant([2, 4])
    >>> y = tf.constant([2, 4])
    >>> tf.math.equal(x, y)
    <tf.Tensor: shape=(2,), dtype=bool, numpy=array([ True,  True])>

    Args:
      x: A `tf.Tensor`.
      y: A `tf.Tensor`.
      name: A name for the operation (optional).

    Returns:
      A `tf.Tensor` of type bool with the same size as that of x or y.

    Raises:
      `tf.errors.InvalidArgumentError`: If shapes of arguments are incompatible
    """
    ...
@overload
def equal(x: RaggedTensor, y: RaggedTensor | float, name: str | None = None) -> RaggedTensor:
    """
    Returns the truth value of (x == y) element-wise.

    Performs a [broadcast](
    https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html) with the
    arguments and then an element-wise equality comparison, returning a Tensor of
    boolean values.

    For example:

    >>> x = tf.constant([2, 4])
    >>> y = tf.constant(2)
    >>> tf.math.equal(x, y)
    <tf.Tensor: shape=(2,), dtype=bool, numpy=array([ True,  False])>

    >>> x = tf.constant([2, 4])
    >>> y = tf.constant([2, 4])
    >>> tf.math.equal(x, y)
    <tf.Tensor: shape=(2,), dtype=bool, numpy=array([ True,  True])>

    Args:
      x: A `tf.Tensor`.
      y: A `tf.Tensor`.
      name: A name for the operation (optional).

    Returns:
      A `tf.Tensor` of type bool with the same size as that of x or y.

    Raises:
      `tf.errors.InvalidArgumentError`: If shapes of arguments are incompatible
    """
    ...
@overload
def not_equal(x: TensorCompatible, y: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Returns the truth value of (x != y) element-wise.

    Performs a [broadcast](
    https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html) with the
    arguments and then an element-wise inequality comparison, returning a Tensor
    of boolean values.

    For example:

    >>> x = tf.constant([2, 4])
    >>> y = tf.constant(2)
    >>> tf.math.not_equal(x, y)
    <tf.Tensor: shape=(2,), dtype=bool, numpy=array([False,  True])>

    >>> x = tf.constant([2, 4])
    >>> y = tf.constant([2, 4])
    >>> tf.math.not_equal(x, y)
    <tf.Tensor: shape=(2,), dtype=bool, numpy=array([False,  False])>

    Args:
      x: A `tf.Tensor`.
      y: A `tf.Tensor`.
      name: A name for the operation (optional).

    Returns:
      A `tf.Tensor` of type bool with the same size as that of x or y.

    Raises:
      `tf.errors.InvalidArgumentError`: If shapes of arguments are incompatible
    """
    ...
@overload
def not_equal(x: RaggedTensor, y: RaggedTensor | float, name: str | None = None) -> RaggedTensor:
    """
    Returns the truth value of (x != y) element-wise.

    Performs a [broadcast](
    https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html) with the
    arguments and then an element-wise inequality comparison, returning a Tensor
    of boolean values.

    For example:

    >>> x = tf.constant([2, 4])
    >>> y = tf.constant(2)
    >>> tf.math.not_equal(x, y)
    <tf.Tensor: shape=(2,), dtype=bool, numpy=array([False,  True])>

    >>> x = tf.constant([2, 4])
    >>> y = tf.constant([2, 4])
    >>> tf.math.not_equal(x, y)
    <tf.Tensor: shape=(2,), dtype=bool, numpy=array([False,  False])>

    Args:
      x: A `tf.Tensor`.
      y: A `tf.Tensor`.
      name: A name for the operation (optional).

    Returns:
      A `tf.Tensor` of type bool with the same size as that of x or y.

    Raises:
      `tf.errors.InvalidArgumentError`: If shapes of arguments are incompatible
    """
    ...
@overload
def greater(x: TensorCompatible, y: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Returns the truth value of (x > y) element-wise.

    *NOTE*: `math.greater` supports broadcasting. More about broadcasting
    [here](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)

    Example:

    ```python
    x = tf.constant([5, 4, 6])
    y = tf.constant([5, 2, 5])
    tf.math.greater(x, y) ==> [False, True, True]

    x = tf.constant([5, 4, 6])
    y = tf.constant([5])
    tf.math.greater(x, y) ==> [False, False, True]
    ```

    Args:
      x: A `Tensor`. Must be one of the following types: `float32`, `float64`, `int32`, `uint8`, `int16`, `int8`, `int64`, `bfloat16`, `uint16`, `half`, `uint32`, `uint64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `bool`.
    """
    ...
@overload
def greater(x: RaggedTensor, y: RaggedTensor | float, name: str | None = None) -> RaggedTensor:
    """
    Returns the truth value of (x > y) element-wise.

    *NOTE*: `math.greater` supports broadcasting. More about broadcasting
    [here](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)

    Example:

    ```python
    x = tf.constant([5, 4, 6])
    y = tf.constant([5, 2, 5])
    tf.math.greater(x, y) ==> [False, True, True]

    x = tf.constant([5, 4, 6])
    y = tf.constant([5])
    tf.math.greater(x, y) ==> [False, False, True]
    ```

    Args:
      x: A `Tensor`. Must be one of the following types: `float32`, `float64`, `int32`, `uint8`, `int16`, `int8`, `int64`, `bfloat16`, `uint16`, `half`, `uint32`, `uint64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `bool`.
    """
    ...
@overload
def greater_equal(x: TensorCompatible, y: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Returns the truth value of (x >= y) element-wise.

    *NOTE*: `math.greater_equal` supports broadcasting. More about broadcasting
    [here](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)

    Example:

    ```python
    x = tf.constant([5, 4, 6, 7])
    y = tf.constant([5, 2, 5, 10])
    tf.math.greater_equal(x, y) ==> [True, True, True, False]

    x = tf.constant([5, 4, 6, 7])
    y = tf.constant([5])
    tf.math.greater_equal(x, y) ==> [True, False, True, True]
    ```

    Args:
      x: A `Tensor`. Must be one of the following types: `float32`, `float64`, `int32`, `uint8`, `int16`, `int8`, `int64`, `bfloat16`, `uint16`, `half`, `uint32`, `uint64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `bool`.
    """
    ...
@overload
def greater_equal(x: RaggedTensor, y: RaggedTensor | float, name: str | None = None) -> RaggedTensor:
    """
    Returns the truth value of (x >= y) element-wise.

    *NOTE*: `math.greater_equal` supports broadcasting. More about broadcasting
    [here](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)

    Example:

    ```python
    x = tf.constant([5, 4, 6, 7])
    y = tf.constant([5, 2, 5, 10])
    tf.math.greater_equal(x, y) ==> [True, True, True, False]

    x = tf.constant([5, 4, 6, 7])
    y = tf.constant([5])
    tf.math.greater_equal(x, y) ==> [True, False, True, True]
    ```

    Args:
      x: A `Tensor`. Must be one of the following types: `float32`, `float64`, `int32`, `uint8`, `int16`, `int8`, `int64`, `bfloat16`, `uint16`, `half`, `uint32`, `uint64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `bool`.
    """
    ...
@overload
def less(x: TensorCompatible, y: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Returns the truth value of (x < y) element-wise.

    *NOTE*: `math.less` supports broadcasting. More about broadcasting
    [here](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)

    Example:

    ```python
    x = tf.constant([5, 4, 6])
    y = tf.constant([5])
    tf.math.less(x, y) ==> [False, True, False]

    x = tf.constant([5, 4, 6])
    y = tf.constant([5, 6, 7])
    tf.math.less(x, y) ==> [False, True, True]
    ```

    Args:
      x: A `Tensor`. Must be one of the following types: `float32`, `float64`, `int32`, `uint8`, `int16`, `int8`, `int64`, `bfloat16`, `uint16`, `half`, `uint32`, `uint64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `bool`.
    """
    ...
@overload
def less(x: RaggedTensor, y: RaggedTensor | float, name: str | None = None) -> RaggedTensor:
    """
    Returns the truth value of (x < y) element-wise.

    *NOTE*: `math.less` supports broadcasting. More about broadcasting
    [here](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)

    Example:

    ```python
    x = tf.constant([5, 4, 6])
    y = tf.constant([5])
    tf.math.less(x, y) ==> [False, True, False]

    x = tf.constant([5, 4, 6])
    y = tf.constant([5, 6, 7])
    tf.math.less(x, y) ==> [False, True, True]
    ```

    Args:
      x: A `Tensor`. Must be one of the following types: `float32`, `float64`, `int32`, `uint8`, `int16`, `int8`, `int64`, `bfloat16`, `uint16`, `half`, `uint32`, `uint64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `bool`.
    """
    ...
@overload
def less_equal(x: TensorCompatible, y: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Returns the truth value of (x <= y) element-wise.

    *NOTE*: `math.less_equal` supports broadcasting. More about broadcasting
    [here](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)

    Example:

    ```python
    x = tf.constant([5, 4, 6])
    y = tf.constant([5])
    tf.math.less_equal(x, y) ==> [True, True, False]

    x = tf.constant([5, 4, 6])
    y = tf.constant([5, 6, 6])
    tf.math.less_equal(x, y) ==> [True, True, True]
    ```

    Args:
      x: A `Tensor`. Must be one of the following types: `float32`, `float64`, `int32`, `uint8`, `int16`, `int8`, `int64`, `bfloat16`, `uint16`, `half`, `uint32`, `uint64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `bool`.
    """
    ...
@overload
def less_equal(x: RaggedTensor, y: RaggedTensor | float, name: str | None = None) -> RaggedTensor:
    """
    Returns the truth value of (x <= y) element-wise.

    *NOTE*: `math.less_equal` supports broadcasting. More about broadcasting
    [here](http://docs.scipy.org/doc/numpy/user/basics.broadcasting.html)

    Example:

    ```python
    x = tf.constant([5, 4, 6])
    y = tf.constant([5])
    tf.math.less_equal(x, y) ==> [True, True, False]

    x = tf.constant([5, 4, 6])
    y = tf.constant([5, 6, 6])
    tf.math.less_equal(x, y) ==> [True, True, True]
    ```

    Args:
      x: A `Tensor`. Must be one of the following types: `float32`, `float64`, `int32`, `uint8`, `int16`, `int8`, `int64`, `bfloat16`, `uint16`, `half`, `uint32`, `uint64`.
      y: A `Tensor`. Must have the same type as `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `bool`.
    """
    ...
def segment_sum(data: TensorCompatible, segment_ids: TensorCompatible, name: str | None = None) -> Tensor:
    r"""
    Computes the sum along segments of a tensor.

    Read
    [the section on segmentation](https://tensorflow.org/api_docs/python/tf/math#Segmentation)
    for an explanation of segments.

    Computes a tensor such that
    \\(output_i = \sum_j data_j\\) where sum is over `j` such
    that `segment_ids[j] == i`.

    If the sum is empty for a given segment ID `i`, `output[i] = 0`.

    Caution: On CPU, values in `segment_ids` are always validated to be sorted,
    and an error is thrown for indices that are not increasing. On GPU, this
    does not throw an error for unsorted indices. On GPU, out-of-order indices
    result in safe but unspecified behavior, which may include treating
    out-of-order indices as the same as a smaller following index.

    <div style="width:70%; margin:auto; margin-bottom:10px; margin-top:20px;">
    <img style="width:100%" src="https://www.tensorflow.org/images/SegmentSum.png" alt>
    </div>

    For example:

    >>> c = tf.constant([[1,2,3,4], [4, 3, 2, 1], [5,6,7,8]])
    >>> tf.math.segment_sum(c, tf.constant([0, 0, 1])).numpy()
    array([[5, 5, 5, 5],
           [5, 6, 7, 8]], dtype=int32)

    Args:
      data: A `Tensor`. Must be one of the following types: `float32`, `float64`, `int32`, `uint8`, `int16`, `int8`, `complex64`, `int64`, `qint8`, `quint8`, `qint32`, `bfloat16`, `qint16`, `quint16`, `uint16`, `complex128`, `half`, `uint32`, `uint64`.
      segment_ids: A `Tensor`. Must be one of the following types: `int32`, `int64`.
        A 1-D tensor whose size is equal to the size of `data`'s
        first dimension.  Values should be sorted and can be repeated.

        Caution: The values are always validated to be sorted on CPU, never validated
        on GPU.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `data`.
    """
    ...
@overload
def sign(x: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Returns an element-wise indication of the sign of a number.

    `y = sign(x) = -1 if x < 0; 0 if x == 0; 1 if x > 0`.

    For complex numbers, `y = sign(x) = x / |x| if x != 0, otherwise y = 0`.

    Example usage:

    >>> # real number
    >>> tf.math.sign([0., 2., -3.])
    <tf.Tensor: shape=(3,), dtype=float32,
    numpy=array([ 0.,  1., -1.], dtype=float32)>

    >>> # complex number
    >>> tf.math.sign([1 + 1j, 0 + 0j])
    <tf.Tensor: shape=(2,), dtype=complex128,
    numpy=array([0.70710678+0.70710678j, 0.        +0.j        ])>

    Args:
     x: A Tensor. Must be one of the following types: bfloat16, half, float32,
       float64, int32, int64, complex64, complex128.
     name: A name for the operation (optional).

    Returns:
     A Tensor. Has the same type as x.

     If x is a SparseTensor, returns SparseTensor(x.indices,
       tf.math.sign(x.values, ...), x.dense_shape).

      If `x` is a `SparseTensor`, returns
      `SparseTensor(x.indices, tf.math.sign(x.values, ...), x.dense_shape)`
    """
    ...
@overload
def sign(x: SparseTensor, name: str | None = None) -> SparseTensor:
    """
    Returns an element-wise indication of the sign of a number.

    `y = sign(x) = -1 if x < 0; 0 if x == 0; 1 if x > 0`.

    For complex numbers, `y = sign(x) = x / |x| if x != 0, otherwise y = 0`.

    Example usage:

    >>> # real number
    >>> tf.math.sign([0., 2., -3.])
    <tf.Tensor: shape=(3,), dtype=float32,
    numpy=array([ 0.,  1., -1.], dtype=float32)>

    >>> # complex number
    >>> tf.math.sign([1 + 1j, 0 + 0j])
    <tf.Tensor: shape=(2,), dtype=complex128,
    numpy=array([0.70710678+0.70710678j, 0.        +0.j        ])>

    Args:
     x: A Tensor. Must be one of the following types: bfloat16, half, float32,
       float64, int32, int64, complex64, complex128.
     name: A name for the operation (optional).

    Returns:
     A Tensor. Has the same type as x.

     If x is a SparseTensor, returns SparseTensor(x.indices,
       tf.math.sign(x.values, ...), x.dense_shape).

      If `x` is a `SparseTensor`, returns
      `SparseTensor(x.indices, tf.math.sign(x.values, ...), x.dense_shape)`
    """
    ...
@overload
def sign(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Returns an element-wise indication of the sign of a number.

    `y = sign(x) = -1 if x < 0; 0 if x == 0; 1 if x > 0`.

    For complex numbers, `y = sign(x) = x / |x| if x != 0, otherwise y = 0`.

    Example usage:

    >>> # real number
    >>> tf.math.sign([0., 2., -3.])
    <tf.Tensor: shape=(3,), dtype=float32,
    numpy=array([ 0.,  1., -1.], dtype=float32)>

    >>> # complex number
    >>> tf.math.sign([1 + 1j, 0 + 0j])
    <tf.Tensor: shape=(2,), dtype=complex128,
    numpy=array([0.70710678+0.70710678j, 0.        +0.j        ])>

    Args:
     x: A Tensor. Must be one of the following types: bfloat16, half, float32,
       float64, int32, int64, complex64, complex128.
     name: A name for the operation (optional).

    Returns:
     A Tensor. Has the same type as x.

     If x is a SparseTensor, returns SparseTensor(x.indices,
       tf.math.sign(x.values, ...), x.dense_shape).

      If `x` is a `SparseTensor`, returns
      `SparseTensor(x.indices, tf.math.sign(x.values, ...), x.dense_shape)`
    """
    ...
@overload
def sqrt(x: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Computes element-wise square root of the input tensor.

    Note: This operation does not support integer types.

    >>> x = tf.constant([[4.0], [16.0]])
    >>> tf.sqrt(x)
    <tf.Tensor: shape=(2, 1), dtype=float32, numpy=
      array([[2.],
             [4.]], dtype=float32)>
    >>> y = tf.constant([[-4.0], [16.0]])
    >>> tf.sqrt(y)
    <tf.Tensor: shape=(2, 1), dtype=float32, numpy=
      array([[nan],
             [ 4.]], dtype=float32)>
    >>> z = tf.constant([[-1.0], [16.0]], dtype=tf.complex128)
    >>> tf.sqrt(z)
    <tf.Tensor: shape=(2, 1), dtype=complex128, numpy=
      array([[0.0+1.j],
             [4.0+0.j]])>

    Note: In order to support complex type, please provide an input tensor
    of `complex64` or `complex128`.

    Args:
      x: A `tf.Tensor` of type `bfloat16`, `half`, `float32`, `float64`,
        `complex64`, `complex128`
      name: A name for the operation (optional).

    Returns:
      A `tf.Tensor` of same size, type and sparsity as `x`.

      If `x` is a `SparseTensor`, returns
      `SparseTensor(x.indices, tf.math.sqrt(x.values, ...), x.dense_shape)`
    """
    ...
@overload
def sqrt(x: SparseTensor, name: str | None = None) -> SparseTensor:
    """
    Computes element-wise square root of the input tensor.

    Note: This operation does not support integer types.

    >>> x = tf.constant([[4.0], [16.0]])
    >>> tf.sqrt(x)
    <tf.Tensor: shape=(2, 1), dtype=float32, numpy=
      array([[2.],
             [4.]], dtype=float32)>
    >>> y = tf.constant([[-4.0], [16.0]])
    >>> tf.sqrt(y)
    <tf.Tensor: shape=(2, 1), dtype=float32, numpy=
      array([[nan],
             [ 4.]], dtype=float32)>
    >>> z = tf.constant([[-1.0], [16.0]], dtype=tf.complex128)
    >>> tf.sqrt(z)
    <tf.Tensor: shape=(2, 1), dtype=complex128, numpy=
      array([[0.0+1.j],
             [4.0+0.j]])>

    Note: In order to support complex type, please provide an input tensor
    of `complex64` or `complex128`.

    Args:
      x: A `tf.Tensor` of type `bfloat16`, `half`, `float32`, `float64`,
        `complex64`, `complex128`
      name: A name for the operation (optional).

    Returns:
      A `tf.Tensor` of same size, type and sparsity as `x`.

      If `x` is a `SparseTensor`, returns
      `SparseTensor(x.indices, tf.math.sqrt(x.values, ...), x.dense_shape)`
    """
    ...
@overload
def sqrt(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Computes element-wise square root of the input tensor.

    Note: This operation does not support integer types.

    >>> x = tf.constant([[4.0], [16.0]])
    >>> tf.sqrt(x)
    <tf.Tensor: shape=(2, 1), dtype=float32, numpy=
      array([[2.],
             [4.]], dtype=float32)>
    >>> y = tf.constant([[-4.0], [16.0]])
    >>> tf.sqrt(y)
    <tf.Tensor: shape=(2, 1), dtype=float32, numpy=
      array([[nan],
             [ 4.]], dtype=float32)>
    >>> z = tf.constant([[-1.0], [16.0]], dtype=tf.complex128)
    >>> tf.sqrt(z)
    <tf.Tensor: shape=(2, 1), dtype=complex128, numpy=
      array([[0.0+1.j],
             [4.0+0.j]])>

    Note: In order to support complex type, please provide an input tensor
    of `complex64` or `complex128`.

    Args:
      x: A `tf.Tensor` of type `bfloat16`, `half`, `float32`, `float64`,
        `complex64`, `complex128`
      name: A name for the operation (optional).

    Returns:
      A `tf.Tensor` of same size, type and sparsity as `x`.

      If `x` is a `SparseTensor`, returns
      `SparseTensor(x.indices, tf.math.sqrt(x.values, ...), x.dense_shape)`
    """
    ...
@overload
def rsqrt(x: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Computes reciprocal of square root of x element-wise.

    For example:

    >>> x = tf.constant([2., 0., -2.])
    >>> tf.math.rsqrt(x)
    <tf.Tensor: shape=(3,), dtype=float32,
    numpy=array([0.707, inf, nan], dtype=float32)>

    Args:
      x: A `tf.Tensor`. Must be one of the following types: `bfloat16`, `half`,
        `float32`, `float64`.
      name: A name for the operation (optional).

    Returns:
      A `tf.Tensor`. Has the same type as `x`.
    """
    ...
@overload
def rsqrt(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Computes reciprocal of square root of x element-wise.

    For example:

    >>> x = tf.constant([2., 0., -2.])
    >>> tf.math.rsqrt(x)
    <tf.Tensor: shape=(3,), dtype=float32,
    numpy=array([0.707, inf, nan], dtype=float32)>

    Args:
      x: A `tf.Tensor`. Must be one of the following types: `bfloat16`, `half`,
        `float32`, `float64`.
      name: A name for the operation (optional).

    Returns:
      A `tf.Tensor`. Has the same type as `x`.
    """
    ...
@overload
def square(x: TensorCompatible, name: str | None = None) -> Tensor:
    r"""
    Computes square of x element-wise.

    I.e., \\(y = x * x = x^2\\).

    >>> tf.math.square([-2., 0., 3.])
    <tf.Tensor: shape=(3,), dtype=float32, numpy=array([4., 0., 9.], dtype=float32)>

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.

      If `x` is a `SparseTensor`, returns
      `SparseTensor(x.indices, tf.math.square(x.values, ...), x.dense_shape)`
    """
    ...
@overload
def square(x: SparseTensor, name: str | None = None) -> SparseTensor:
    r"""
    Computes square of x element-wise.

    I.e., \\(y = x * x = x^2\\).

    >>> tf.math.square([-2., 0., 3.])
    <tf.Tensor: shape=(3,), dtype=float32, numpy=array([4., 0., 9.], dtype=float32)>

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.

      If `x` is a `SparseTensor`, returns
      `SparseTensor(x.indices, tf.math.square(x.values, ...), x.dense_shape)`
    """
    ...
@overload
def square(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    r"""
    Computes square of x element-wise.

    I.e., \\(y = x * x = x^2\\).

    >>> tf.math.square([-2., 0., 3.])
    <tf.Tensor: shape=(3,), dtype=float32, numpy=array([4., 0., 9.], dtype=float32)>

    Args:
      x: A `Tensor`. Must be one of the following types: `bfloat16`, `half`, `float32`, `float64`, `int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`, `complex64`, `complex128`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `x`.

      If `x` is a `SparseTensor`, returns
      `SparseTensor(x.indices, tf.math.square(x.values, ...), x.dense_shape)`
    """
    ...
@overload
def softplus(features: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Computes elementwise softplus: `softplus(x) = log(exp(x) + 1)`.

    `softplus` is a smooth approximation of `relu`. Like `relu`, `softplus` always
    takes on positive values.

    <img style="width:100%" src="https://www.tensorflow.org/images/softplus.png">

    Example:

    >>> import tensorflow as tf
    >>> tf.math.softplus(tf.range(0, 2, dtype=tf.float32)).numpy()
    array([0.6931472, 1.3132616], dtype=float32)

    Args:
      features: `Tensor`
      name: Optional: name to associate with this operation.
    Returns:
      `Tensor`
    """
    ...
@overload
def softplus(features: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Computes elementwise softplus: `softplus(x) = log(exp(x) + 1)`.

    `softplus` is a smooth approximation of `relu`. Like `relu`, `softplus` always
    takes on positive values.

    <img style="width:100%" src="https://www.tensorflow.org/images/softplus.png">

    Example:

    >>> import tensorflow as tf
    >>> tf.math.softplus(tf.range(0, 2, dtype=tf.float32)).numpy()
    array([0.6931472, 1.3132616], dtype=float32)

    Args:
      features: `Tensor`
      name: Optional: name to associate with this operation.
    Returns:
      `Tensor`
    """
    ...
@overload
def round(x: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Rounds the values of a tensor to the nearest integer, element-wise.

    Rounds half to even.  Also known as bankers rounding. If you want to round
    according to the current system rounding mode use tf::cint.
    For example:

    ```python
    x = tf.constant([0.9, 2.5, 2.3, 1.5, -4.5])
    tf.round(x)  # [ 1.0, 2.0, 2.0, 2.0, -4.0 ]
    ```

    Args:
      x: A `Tensor` of type `float16`, `float32`, `float64`, `int32`, or `int64`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of same shape and type as `x`.
    """
    ...
@overload
def round(x: SparseTensor, name: str | None = None) -> SparseTensor:
    """
    Rounds the values of a tensor to the nearest integer, element-wise.

    Rounds half to even.  Also known as bankers rounding. If you want to round
    according to the current system rounding mode use tf::cint.
    For example:

    ```python
    x = tf.constant([0.9, 2.5, 2.3, 1.5, -4.5])
    tf.round(x)  # [ 1.0, 2.0, 2.0, 2.0, -4.0 ]
    ```

    Args:
      x: A `Tensor` of type `float16`, `float32`, `float64`, `int32`, or `int64`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of same shape and type as `x`.
    """
    ...
@overload
def round(x: RaggedTensor, name: str | None = None) -> RaggedTensor:
    """
    Rounds the values of a tensor to the nearest integer, element-wise.

    Rounds half to even.  Also known as bankers rounding. If you want to round
    according to the current system rounding mode use tf::cint.
    For example:

    ```python
    x = tf.constant([0.9, 2.5, 2.3, 1.5, -4.5])
    tf.round(x)  # [ 1.0, 2.0, 2.0, 2.0, -4.0 ]
    ```

    Args:
      x: A `Tensor` of type `float16`, `float32`, `float64`, `int32`, or `int64`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of same shape and type as `x`.
    """
    ...

# Depending on the method axis is either a rank 0 tensor or a rank 0/1 tensor.
def reduce_mean(
    input_tensor: TensorCompatible | RaggedTensor,
    axis: TensorCompatible | None = None,
    keepdims: bool = False,
    name: str | None = None,
) -> Tensor:
    """
    Computes the mean of elements across dimensions of a tensor.

    Reduces `input_tensor` along the dimensions given in `axis` by computing the
    mean of elements across the dimensions in `axis`.
    Unless `keepdims` is true, the rank of the tensor is reduced by 1 for each
    of the entries in `axis`, which must be unique. If `keepdims` is true, the
    reduced dimensions are retained with length 1.

    If `axis` is None, all dimensions are reduced, and a tensor with a single
    element is returned.

    For example:

    >>> x = tf.constant([[1., 1.], [2., 2.]])
    >>> tf.reduce_mean(x)
    <tf.Tensor: shape=(), dtype=float32, numpy=1.5>
    >>> tf.reduce_mean(x, 0)
    <tf.Tensor: shape=(2,), dtype=float32, numpy=array([1.5, 1.5], dtype=float32)>
    >>> tf.reduce_mean(x, 1)
    <tf.Tensor: shape=(2,), dtype=float32, numpy=array([1., 2.], dtype=float32)>

    Args:
      input_tensor: The tensor to reduce. Should have numeric type.
      axis: The dimensions to reduce. If `None` (the default), reduces all
        dimensions. Must be in the range `[-rank(input_tensor),
        rank(input_tensor))`.
      keepdims: If true, retains reduced dimensions with length 1.
      name: A name for the operation (optional).

    Returns:
      The reduced tensor.

    @compatibility(numpy)
    Equivalent to np.mean

    Please note that `np.mean` has a `dtype` parameter that could be used to
    specify the output type. By default this is `dtype=float64`. On the other
    hand, `tf.reduce_mean` has an aggressive type inference from `input_tensor`,
    for example:

    >>> x = tf.constant([1, 0, 1, 0])
    >>> tf.reduce_mean(x)
    <tf.Tensor: shape=(), dtype=int32, numpy=0>
    >>> y = tf.constant([1., 0., 1., 0.])
    >>> tf.reduce_mean(y)
    <tf.Tensor: shape=(), dtype=float32, numpy=0.5>

    @end_compatibility
    """
    ...
def reduce_sum(
    input_tensor: TensorCompatible | RaggedTensor,
    axis: TensorCompatible | None = None,
    keepdims: bool = False,
    name: str | None = None,
) -> Tensor:
    """
    Computes the sum of elements across dimensions of a tensor.

    This is the reduction operation for the elementwise `tf.math.add` op.

    Reduces `input_tensor` along the dimensions given in `axis`.
    Unless `keepdims` is true, the rank of the tensor is reduced by 1 for each
    of the entries in `axis`, which must be unique. If `keepdims` is true, the
    reduced dimensions are retained with length 1.

    If `axis` is None, all dimensions are reduced, and a
    tensor with a single element is returned.

    For example:

      >>> # x has a shape of (2, 3) (two rows and three columns):
      >>> x = tf.constant([[1, 1, 1], [1, 1, 1]])
      >>> x.numpy()
      array([[1, 1, 1],
             [1, 1, 1]], dtype=int32)
      >>> # sum all the elements
      >>> # 1 + 1 + 1 + 1 + 1+ 1 = 6
      >>> tf.reduce_sum(x).numpy().item()
      6
      >>> # reduce along the first dimension
      >>> # the result is [1, 1, 1] + [1, 1, 1] = [2, 2, 2]
      >>> tf.reduce_sum(x, 0).numpy()
      array([2, 2, 2], dtype=int32)
      >>> # reduce along the second dimension
      >>> # the result is [1, 1] + [1, 1] + [1, 1] = [3, 3]
      >>> tf.reduce_sum(x, 1).numpy()
      array([3, 3], dtype=int32)
      >>> # keep the original dimensions
      >>> tf.reduce_sum(x, 1, keepdims=True).numpy()
      array([[3],
             [3]], dtype=int32)
      >>> # reduce along both dimensions
      >>> # the result is 1 + 1 + 1 + 1 + 1 + 1 = 6
      >>> # or, equivalently, reduce along rows, then reduce the resultant array
      >>> # [1, 1, 1] + [1, 1, 1] = [2, 2, 2]
      >>> # 2 + 2 + 2 = 6
      >>> tf.reduce_sum(x, [0, 1]).numpy().item()
      6

    Args:
      input_tensor: The tensor to reduce. Should have numeric type.
      axis: The dimensions to reduce. If `None` (the default), reduces all
        dimensions. Must be in the range `[-rank(input_tensor),
        rank(input_tensor)]`.
      keepdims: If true, retains reduced dimensions with length 1.
      name: A name for the operation (optional).

    Returns:
      The reduced tensor, of the same dtype as the input_tensor.

    @compatibility(numpy)
    Equivalent to np.sum apart the fact that numpy upcast uint8 and int32 to
    int64 while tensorflow returns the same dtype as the input.
    @end_compatibility
    """
    ...
def reduce_max(
    input_tensor: TensorCompatible | RaggedTensor,
    axis: TensorCompatible | None = None,
    keepdims: bool = False,
    name: str | None = None,
) -> Tensor:
    """
    Computes `tf.math.maximum` of elements across dimensions of a tensor.

    This is the reduction operation for the elementwise `tf.math.maximum` op.

    Reduces `input_tensor` along the dimensions given in `axis`.
    Unless `keepdims` is true, the rank of the tensor is reduced by 1 for each
    of the entries in `axis`, which must be unique. If `keepdims` is true, the
    reduced dimensions are retained with length 1.

    If `axis` is None, all dimensions are reduced, and a
    tensor with a single element is returned.

    Usage example:

      >>> x = tf.constant([5, 1, 2, 4])
      >>> tf.reduce_max(x)
      <tf.Tensor: shape=(), dtype=int32, numpy=5>
      >>> x = tf.constant([-5, -1, -2, -4])
      >>> tf.reduce_max(x)
      <tf.Tensor: shape=(), dtype=int32, numpy=-1>
      >>> x = tf.constant([4, float('nan')])
      >>> tf.reduce_max(x)
      <tf.Tensor: shape=(), dtype=float32, numpy=nan>
      >>> x = tf.constant([float('nan'), float('nan')])
      >>> tf.reduce_max(x)
      <tf.Tensor: shape=(), dtype=float32, numpy=nan>
      >>> x = tf.constant([float('-inf'), float('inf')])
      >>> tf.reduce_max(x)
      <tf.Tensor: shape=(), dtype=float32, numpy=inf>

    See the numpy docs for `np.amax` and `np.nanmax` behavior.

    Args:
      input_tensor: The tensor to reduce. Should have real numeric type.
      axis: The dimensions to reduce. If `None` (the default), reduces all
        dimensions. Must be in the range `[-rank(input_tensor),
        rank(input_tensor))`.
      keepdims: If true, retains reduced dimensions with length 1.
      name: A name for the operation (optional).

    Returns:
      The reduced tensor.
    """
    ...
def reduce_min(
    input_tensor: TensorCompatible | RaggedTensor,
    axis: TensorCompatible | None = None,
    keepdims: bool = False,
    name: str | None = None,
) -> Tensor:
    """
    Computes the `tf.math.minimum` of elements across dimensions of a tensor.

    This is the reduction operation for the elementwise `tf.math.minimum` op.

    Reduces `input_tensor` along the dimensions given in `axis`.
    Unless `keepdims` is true, the rank of the tensor is reduced by 1 for each
    of the entries in `axis`, which must be unique. If `keepdims` is true, the
    reduced dimensions are retained with length 1.

    If `axis` is None, all dimensions are reduced, and a
    tensor with a single element is returned.

    For example:

    >>> a = tf.constant([
    ...   [[1, 2], [3, 4]],
    ...   [[1, 2], [3, 4]]
    ... ])
    >>> tf.reduce_min(a)
    <tf.Tensor: shape=(), dtype=int32, numpy=1>

    Choosing a specific axis returns minimum element in the given axis:

    >>> b = tf.constant([[1, 2, 3], [4, 5, 6]])
    >>> tf.reduce_min(b, axis=0)
    <tf.Tensor: shape=(3,), dtype=int32, numpy=array([1, 2, 3], dtype=int32)>
    >>> tf.reduce_min(b, axis=1)
    <tf.Tensor: shape=(2,), dtype=int32, numpy=array([1, 4], dtype=int32)>

    Setting `keepdims` to `True` retains the dimension of `input_tensor`:

    >>> tf.reduce_min(a, keepdims=True)
    <tf.Tensor: shape=(1, 1, 1), dtype=int32, numpy=array([[[1]]], dtype=int32)>
    >>> tf.math.reduce_min(a, axis=0, keepdims=True)
    <tf.Tensor: shape=(1, 2, 2), dtype=int32, numpy=
    array([[[1, 2],
            [3, 4]]], dtype=int32)>

    Args:
      input_tensor: The tensor to reduce. Should have real numeric type.
      axis: The dimensions to reduce. If `None` (the default), reduces all
        dimensions. Must be in the range `[-rank(input_tensor),
        rank(input_tensor))`.
      keepdims: If true, retains reduced dimensions with length 1.
      name: A name for the operation (optional).

    Returns:
      The reduced tensor.

    @compatibility(numpy)
    Equivalent to np.min
    @end_compatibility
    """
    ...
def reduce_prod(
    input_tensor: TensorCompatible | RaggedTensor,
    axis: TensorCompatible | None = None,
    keepdims: bool = False,
    name: str | None = None,
) -> Tensor:
    """
    Computes `tf.math.multiply` of elements across dimensions of a tensor.

    This is the reduction operation for the elementwise `tf.math.multiply` op.

    Reduces `input_tensor` along the dimensions given in `axis`.
    Unless `keepdims` is true, the rank of the tensor is reduced by 1 for each
    entry in `axis`. If `keepdims` is true, the reduced dimensions
    are retained with length 1.

    If `axis` is None, all dimensions are reduced, and a
    tensor with a single element is returned.

    For example:

      >>> x = tf.constant([[1., 2.], [3., 4.]])
      >>> tf.math.reduce_prod(x)
      <tf.Tensor: shape=(), dtype=float32, numpy=24.>
      >>> tf.math.reduce_prod(x, 0)
      <tf.Tensor: shape=(2,), dtype=float32, numpy=array([3., 8.], dtype=float32)>
      >>> tf.math.reduce_prod(x, 1)
      <tf.Tensor: shape=(2,), dtype=float32, numpy=array([2., 12.],
      dtype=float32)>

    Args:
      input_tensor: The tensor to reduce. Should have numeric type.
      axis: The dimensions to reduce. If `None` (the default), reduces all
        dimensions. Must be in the range `[-rank(input_tensor),
        rank(input_tensor))`.
      keepdims: If true, retains reduced dimensions with length 1.
      name: A name for the operation (optional).

    Returns:
      The reduced tensor.

    @compatibility(numpy)
    Equivalent to np.prod
    @end_compatibility
    """
    ...
def reduce_std(
    input_tensor: TensorCompatible | RaggedTensor,
    axis: TensorCompatible | None = None,
    keepdims: bool = False,
    name: str | None = None,
) -> Tensor:
    """
    Computes the standard deviation of elements across dimensions of a tensor.

    Reduces `input_tensor` along the dimensions given in `axis`.
    Unless `keepdims` is true, the rank of the tensor is reduced by 1 for each
    of the entries in `axis`, which must be unique. If `keepdims` is true, the
    reduced dimensions are retained with length 1.

    If `axis` is None, all dimensions are reduced, and a
    tensor with a single element is returned.

    For example:

    >>> x = tf.constant([[1., 2.], [3., 4.]])
    >>> tf.math.reduce_std(x)
    <tf.Tensor: shape=(), dtype=float32, numpy=1.118034>
    >>> tf.math.reduce_std(x, 0)
    <tf.Tensor: shape=(2,), dtype=float32, numpy=array([1., 1.], dtype=float32)>
    >>> tf.math.reduce_std(x, 1)
    <tf.Tensor: shape=(2,), dtype=float32, numpy=array([0.5, 0.5], dtype=float32)>

    Args:
      input_tensor: The tensor to reduce. Should have real or complex type.
      axis: The dimensions to reduce. If `None` (the default), reduces all
        dimensions. Must be in the range `[-rank(input_tensor),
        rank(input_tensor))`.
      keepdims: If true, retains reduced dimensions with length 1.
      name: A name scope for the associated operations (optional).

    Returns:
      The reduced tensor, of the same dtype as the input_tensor. Note,  for
      `complex64` or `complex128` input, the returned `Tensor` will be of type
      `float32` or `float64`, respectively.

    @compatibility(numpy)
    Equivalent to np.std

    Please note `np.std` has a `dtype` parameter that could be used to specify the
    output type. By default this is `dtype=float64`. On the other hand,
    `tf.math.reduce_std` has aggressive type inference from `input_tensor`.
    @end_compatibility
    """
    ...
def reduce_variance(
    input_tensor: TensorCompatible | RaggedTensor,
    axis: TensorCompatible | None = None,
    keepdims: bool = False,
    name: str | None = None,
) -> Tensor:
    """
    Computes the variance of elements across dimensions of a tensor.

    Reduces `input_tensor` along the dimensions given in `axis`.
    Unless `keepdims` is true, the rank of the tensor is reduced by 1 for each
    of the entries in `axis`, which must be unique. If `keepdims` is true, the
    reduced dimensions are retained with length 1.

    If `axis` is None, all dimensions are reduced, and a
    tensor with a single element is returned.

    For example:

    >>> x = tf.constant([[1., 2.], [3., 4.]])
    >>> tf.math.reduce_variance(x)
    <tf.Tensor: shape=(), dtype=float32, numpy=1.25>
    >>> tf.math.reduce_variance(x, 0)
    <tf.Tensor: shape=(2,), dtype=float32, numpy=array([1., 1.], ...)>
    >>> tf.math.reduce_variance(x, 1)
    <tf.Tensor: shape=(2,), dtype=float32, numpy=array([0.25, 0.25], ...)>

    Args:
      input_tensor: The tensor to reduce. Should have real or complex type.
      axis: The dimensions to reduce. If `None` (the default), reduces all
        dimensions. Must be in the range `[-rank(input_tensor),
        rank(input_tensor))`.
      keepdims: If true, retains reduced dimensions with length 1.
      name: A name scope for the associated operations (optional).

    Returns:
      The reduced tensor, of the same dtype as the input_tensor. Note,  for
      `complex64` or `complex128` input, the returned `Tensor` will be of type
      `float32` or `float64`, respectively.

    @compatibility(numpy)
    Equivalent to np.var

    Please note `np.var` has a `dtype` parameter that could be used to specify the
    output type. By default this is `dtype=float64`. On the other hand,
    `tf.math.reduce_variance` has aggressive type inference from `input_tensor`.
    @end_compatibility
    """
    ...
def argmax(
    input: TensorCompatible, axis: TensorCompatible | None = None, output_type: DTypeLike = ..., name: str | None = None
) -> Tensor:
    """
    Returns the index with the largest value across axes of a tensor.

    In case of identity returns the smallest index.

    For example:

    >>> A = tf.constant([2, 20, 30, 3, 6])
    >>> tf.math.argmax(A)  # A[2] is maximum in tensor A
    <tf.Tensor: shape=(), dtype=int64, numpy=2>
    >>> B = tf.constant([[2, 20, 30, 3, 6], [3, 11, 16, 1, 8],
    ...                  [14, 45, 23, 5, 27]])
    >>> tf.math.argmax(B, 0)
    <tf.Tensor: shape=(5,), dtype=int64, numpy=array([2, 2, 0, 2, 2])>
    >>> tf.math.argmax(B, 1)
    <tf.Tensor: shape=(3,), dtype=int64, numpy=array([2, 2, 1])>
    >>> C = tf.constant([0, 0, 0, 0])
    >>> tf.math.argmax(C) # Returns smallest index in case of ties
    <tf.Tensor: shape=(), dtype=int64, numpy=0>

    Args:
      input: A `Tensor`.
      axis: An integer, the axis to reduce across. Default to 0.
      output_type: An optional output dtype (`tf.int32` or `tf.int64`). Defaults
        to `tf.int64`.
      name: An optional name for the operation.

    Returns:
      A `Tensor` of type `output_type`.
    """
    ...
def argmin(
    input: TensorCompatible, axis: TensorCompatible | None = None, output_type: DTypeLike = ..., name: str | None = None
) -> Tensor:
    """
    Returns the index with the smallest value across axes of a tensor.

    Returns the smallest index in case of ties.

    Args:
      input: A `Tensor`. Must be one of the following types: `float32`, `float64`,
        `int32`, `uint8`, `int16`, `int8`, `complex64`, `int64`, `qint8`,
        `quint8`, `qint32`, `bfloat16`, `uint16`, `complex128`, `half`, `uint32`,
        `uint64`.
      axis: A `Tensor`. Must be one of the following types: `int32`, `int64`.
        int32 or int64, must be in the range `-rank(input), rank(input))`.
        Describes which axis of the input Tensor to reduce across. For vectors,
        use axis = 0.
      output_type: An optional `tf.DType` from: `tf.int32, tf.int64`. Defaults to
        `tf.int64`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `output_type`.

    Usage:
    ```python
    import tensorflow as tf
    a = [1, 10, 26.9, 2.8, 166.32, 62.3]
    b = tf.math.argmin(input = a)
    c = tf.keras.backend.eval(b)
    # c = 0
    # here a[0] = 1 which is the smallest element of a across axis 0
    ```
    """
    ...

# Only for bool tensors.
def reduce_any(
    input_tensor: TensorCompatible | RaggedTensor,
    axis: TensorCompatible | None = None,
    keepdims: bool = False,
    name: str | None = None,
) -> Tensor:
    """
    Computes `tf.math.logical_or` of elements across dimensions of a tensor.

    This is the reduction operation for the elementwise `tf.math.logical_or` op.

    Reduces `input_tensor` along the dimensions given in `axis`.
    Unless `keepdims` is true, the rank of the tensor is reduced by 1 for each
    of the entries in `axis`, which must be unique. If `keepdims` is true, the
    reduced dimensions are retained with length 1.

    If `axis` is None, all dimensions are reduced, and a
    tensor with a single element is returned.

    For example:

      >>> x = tf.constant([[True,  True], [False, False]])
      >>> tf.reduce_any(x)
      <tf.Tensor: shape=(), dtype=bool, numpy=True>
      >>> tf.reduce_any(x, 0)
      <tf.Tensor: shape=(2,), dtype=bool, numpy=array([ True,  True])>
      >>> tf.reduce_any(x, 1)
      <tf.Tensor: shape=(2,), dtype=bool, numpy=array([ True, False])>

    Args:
      input_tensor: The boolean tensor to reduce.
      axis: The dimensions to reduce. If `None` (the default), reduces all
        dimensions. Must be in the range `[-rank(input_tensor),
        rank(input_tensor))`.
      keepdims: If true, retains reduced dimensions with length 1.
      name: A name for the operation (optional).

    Returns:
      The reduced tensor.

    @compatibility(numpy)
    Equivalent to np.any
    @end_compatibility
    """
    ...
def reduce_all(
    input_tensor: TensorCompatible | RaggedTensor,
    axis: TensorCompatible | None = None,
    keepdims: bool = False,
    name: str | None = None,
) -> Tensor:
    """
    Computes `tf.math.logical_and` of elements across dimensions of a tensor.

    This is the reduction operation for the elementwise `tf.math.logical_and` op.

    Reduces `input_tensor` along the dimensions given in `axis`.
    Unless `keepdims` is true, the rank of the tensor is reduced by 1 for each
    of the entries in `axis`, which must be unique. If `keepdims` is true, the
    reduced dimensions are retained with length 1.

    If `axis` is None, all dimensions are reduced, and a
    tensor with a single element is returned.

    For example:

      >>> x = tf.constant([[True,  True], [False, False]])
      >>> tf.math.reduce_all(x)
      <tf.Tensor: shape=(), dtype=bool, numpy=False>
      >>> tf.math.reduce_all(x, 0)
      <tf.Tensor: shape=(2,), dtype=bool, numpy=array([False, False])>
      >>> tf.math.reduce_all(x, 1)
      <tf.Tensor: shape=(2,), dtype=bool, numpy=array([ True, False])>

    Args:
      input_tensor: The boolean tensor to reduce.
      axis: The dimensions to reduce. If `None` (the default), reduces all
        dimensions. Must be in the range `[-rank(input_tensor),
        rank(input_tensor))`.
      keepdims: If true, retains reduced dimensions with length 1.
      name: A name for the operation (optional).

    Returns:
      The reduced tensor.

    @compatibility(numpy)
    Equivalent to np.all
    @end_compatibility
    """
    ...
def count_nonzero(
    input: _SparseTensorCompatible,
    axis: TensorCompatible | None = None,
    keepdims: bool | None = None,
    dtype: DTypeLike = ...,
    name: str | None = None,
) -> Tensor:
    """
    Computes number of nonzero elements across dimensions of a tensor.

    Reduces `input` along the dimensions given in `axis`.
    Unless `keepdims` is true, the rank of the tensor is reduced by 1 for each
    entry in `axis`. If `keepdims` is true, the reduced dimensions
    are retained with length 1.

    If `axis` has no entries, all dimensions are reduced, and a
    tensor with a single element is returned.

    **NOTE** Floating point comparison to zero is done by exact floating point
    equality check.  Small values are **not** rounded to zero for purposes of
    the nonzero check.

    For example:

    ```python
    x = tf.constant([[0, 1, 0], [1, 1, 0]])
    tf.math.count_nonzero(x)  # 3
    tf.math.count_nonzero(x, 0)  # [1, 2, 0]
    tf.math.count_nonzero(x, 1)  # [1, 2]
    tf.math.count_nonzero(x, 1, keepdims=True)  # [[1], [2]]
    tf.math.count_nonzero(x, [0, 1])  # 3
    ```

    **NOTE** Strings are compared against zero-length empty string `""`. Any
    string with a size greater than zero is already considered as nonzero.

    For example:
    ```python
    x = tf.constant(["", "a", "  ", "b", ""])
    tf.math.count_nonzero(x) # 3, with "a", "  ", and "b" as nonzero strings.
    ```

    Args:
      input: The tensor to reduce. Should be of numeric type, `bool`, or `string`.
      axis: The dimensions to reduce. If `None` (the default), reduces all
        dimensions. Must be in the range `[-rank(input), rank(input))`.
      keepdims: If true, retains reduced dimensions with length 1.
      dtype: The output dtype; defaults to `tf.int64`.
      name: A name for the operation (optional).

    Returns:
      The reduced tensor (number of nonzero values).
    """
    ...
def __getattr__(name: str): ...  # incomplete module

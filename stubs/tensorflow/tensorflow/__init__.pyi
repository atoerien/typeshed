"""
Top-level module of TensorFlow. By convention, we refer to this module as
`tf` instead of `tensorflow`, following the common practice of importing
TensorFlow via the command `import tensorflow as tf`.

The primary function of this module is to import all of the public TensorFlow
interfaces into a single place. The interfaces themselves are located in
sub-modules, as described below.

Note that the file `__init__.py` in the TensorFlow source code tree is actually
only a placeholder to enable test cases to run. The TensorFlow build replaces
this file with a file generated from [`api_template.__init__.py`](https://www.github.com/tensorflow/tensorflow/blob/master/tensorflow/api_template.__init__.py)
"""

import abc
from _typeshed import Incomplete, Unused
from abc import ABC, ABCMeta, abstractmethod
from builtins import bool as _bool
from collections.abc import Callable, Generator, Iterable, Iterator, Sequence
from contextlib import contextmanager
from enum import Enum
from types import TracebackType
from typing import Any, Generic, Literal, TypeVar, overload
from typing_extensions import ParamSpec, Self

from google.protobuf.message import Message
from tensorflow import (
    data as data,
    experimental as experimental,
    feature_column as feature_column,
    initializers as initializers,
    io as io,
    keras as keras,
    math as math,
    nn as nn,
    random as random,
    types as types,
)
from tensorflow._aliases import (
    AnyArray,
    DTypeLike,
    IntArray,
    RaggedTensorLike,
    ScalarTensorCompatible,
    ShapeLike,
    Slice,
    SparseTensorCompatible,
    TensorCompatible,
    UIntTensorCompatible,
)
from tensorflow.autodiff import GradientTape as GradientTape
from tensorflow.core.protobuf import struct_pb2
from tensorflow.dtypes import *
from tensorflow.experimental.dtensor import Layout
from tensorflow.keras import losses as losses
from tensorflow.linalg import eye as eye, matmul as matmul

# Most tf.math functions are exported as tf, but sadly not all are.
from tensorflow.math import (
    abs as abs,
    add as add,
    add_n as add_n,
    argmax as argmax,
    argmin as argmin,
    cos as cos,
    cosh as cosh,
    divide as divide,
    equal as equal,
    greater as greater,
    greater_equal as greater_equal,
    less as less,
    less_equal as less_equal,
    logical_and as logical_and,
    logical_not as logical_not,
    logical_or as logical_or,
    maximum as maximum,
    minimum as minimum,
    multiply as multiply,
    not_equal as not_equal,
    pow as pow,
    reduce_max as reduce_max,
    reduce_mean as reduce_mean,
    reduce_min as reduce_min,
    reduce_prod as reduce_prod,
    reduce_sum as reduce_sum,
    round as round,
    sigmoid as sigmoid,
    sign as sign,
    sin as sin,
    sinh as sinh,
    sqrt as sqrt,
    square as square,
    subtract as subtract,
    tanh as tanh,
)
from tensorflow.python.trackable.autotrackable import AutoTrackable
from tensorflow.sparse import SparseTensor as SparseTensor

# Tensors ideally should be a generic type, but properly typing data type/shape
# will be a lot of work. Until we have good non-generic tensorflow stubs,
# we will skip making Tensor generic. Also good type hints for shapes will
# run quickly into many places where type system is not strong enough today.
# So shape typing is probably not worth doing anytime soon.
class Tensor:
    """
    A `tf.Tensor` represents a multidimensional array of elements.

    All elements are of a single known data type.

    When writing a TensorFlow program, the main object that is
    manipulated and passed around is the `tf.Tensor`.

    A `tf.Tensor` has the following properties:

    * a single data type (float32, int32, or string, for example)
    * a shape

    TensorFlow supports eager execution and graph execution.  In eager
    execution, operations are evaluated immediately.  In graph
    execution, a computational graph is constructed for later
    evaluation.

    TensorFlow defaults to eager execution.  In the example below, the
    matrix multiplication results are calculated immediately.

    >>> # Compute some values using a Tensor
    >>> c = tf.constant([[1.0, 2.0], [3.0, 4.0]])
    >>> d = tf.constant([[1.0, 1.0], [0.0, 1.0]])
    >>> e = tf.matmul(c, d)
    >>> print(e)
    tf.Tensor(
    [[1. 3.]
     [3. 7.]], shape=(2, 2), dtype=float32)

    Note that during eager execution, you may discover your `Tensors` are actually
    of type `EagerTensor`.  This is an internal detail, but it does give you
    access to a useful function, `numpy`:

    >>> type(e)
    <class '...ops.EagerTensor'>
    >>> print(e.numpy())
      [[1. 3.]
       [3. 7.]]

    In TensorFlow, `tf.function`s are a common way to define graph execution.

    A Tensor's shape (that is, the rank of the Tensor and the size of
    each dimension) may not always be fully known.  In `tf.function`
    definitions, the shape may only be partially known.

    Most operations produce tensors of fully-known shapes if the shapes of their
    inputs are also fully known, but in some cases it's only possible to find the
    shape of a tensor at execution time.

    A number of specialized tensors are available: see `tf.Variable`,
    `tf.constant`, `tf.placeholder`, `tf.sparse.SparseTensor`, and
    `tf.RaggedTensor`.

    Caution: when constructing a tensor from a numpy array or pandas dataframe
    the underlying buffer may be re-used:

    ```python
    a = np.array([1, 2, 3])
    b = tf.constant(a)
    a[0] = 4
    print(b)  # tf.Tensor([4 2 3], shape=(3,), dtype=int64)
    ```

    Note: this is an implementation detail that is subject to change and users
    should not rely on this behaviour.

    For more on Tensors, see the [guide](https://tensorflow.org/guide/tensor).
    """
    def __init__(self, op: Operation, value_index: int, dtype: DType) -> None: ...
    def consumers(self) -> list[Incomplete]: ...
    @property
    def shape(self) -> TensorShape:
        """
        Returns a `tf.TensorShape` that represents the shape of this tensor.

        >>> t = tf.constant([1,2,3,4,5])
        >>> t.shape
        TensorShape([5])

        `tf.Tensor.shape` is equivalent to `tf.Tensor.get_shape()`.

        In a `tf.function` or when building a model using
        `tf.keras.Input`, they return the build-time shape of the
        tensor, which may be partially unknown.

        A `tf.TensorShape` is not a tensor. Use `tf.shape(t)` to get a tensor
        containing the shape, calculated at runtime.

        See `tf.Tensor.get_shape()`, and `tf.TensorShape` for details and examples.
        """
        ...
    def get_shape(self) -> TensorShape:
        """
        Returns a `tf.TensorShape` that represents the shape of this tensor.

        In eager execution the shape is always fully-known.

        >>> a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        >>> print(a.shape)
        (2, 3)

        `tf.Tensor.get_shape()` is equivalent to `tf.Tensor.shape`.


        When executing in a `tf.function` or building a model using
        `tf.keras.Input`, `Tensor.shape` may return a partial shape (including
        `None` for unknown dimensions). See `tf.TensorShape` for more details.

        >>> inputs = tf.keras.Input(shape = [10])
        >>> # Unknown batch size
        >>> print(inputs.shape)
        (None, 10)

        The shape is computed using shape inference functions that are
        registered for each `tf.Operation`.

        The returned `tf.TensorShape` is determined at *build* time, without
        executing the underlying kernel. It is not a `tf.Tensor`. If you need a
        shape *tensor*, either convert the `tf.TensorShape` to a `tf.constant`, or
        use the `tf.shape(tensor)` function, which returns the tensor's shape at
        *execution* time.

        This is useful for debugging and providing early errors. For
        example, when tracing a `tf.function`, no ops are being executed, shapes
        may be unknown (See the [Concrete Functions
        Guide](https://www.tensorflow.org/guide/concrete_function) for details).

        >>> @tf.function
        ... def my_matmul(a, b):
        ...   result = a@b
        ...   # the `print` executes during tracing.
        ...   print("Result shape: ", result.shape)
        ...   return result

        The shape inference functions propagate shapes to the extent possible:

        >>> f = my_matmul.get_concrete_function(
        ...   tf.TensorSpec([None,3]),
        ...   tf.TensorSpec([3,5]))
        Result shape: (None, 5)

        Tracing may fail if a shape missmatch can be detected:

        >>> cf = my_matmul.get_concrete_function(
        ...   tf.TensorSpec([None,3]),
        ...   tf.TensorSpec([4,5]))
        Traceback (most recent call last):
        ...
        ValueError: Dimensions must be equal, but are 3 and 4 for 'matmul' (op:
        'MatMul') with input shapes: [?,3], [4,5].

        In some cases, the inferred shape may have unknown dimensions. If
        the caller has additional information about the values of these
        dimensions, `tf.ensure_shape` or `Tensor.set_shape()` can be used to augment
        the inferred shape.

        >>> @tf.function
        ... def my_fun(a):
        ...   a = tf.ensure_shape(a, [5, 5])
        ...   # the `print` executes during tracing.
        ...   print("Result shape: ", a.shape)
        ...   return a

        >>> cf = my_fun.get_concrete_function(
        ...   tf.TensorSpec([None, None]))
        Result shape: (5, 5)

        Returns:
          A `tf.TensorShape` representing the shape of this tensor.
        """
        ...
    @property
    def dtype(self) -> DType:
        """The `DType` of elements in this tensor."""
        ...
    @property
    def graph(self) -> Graph: ...
    @property
    def name(self) -> str: ...
    @property
    def op(self) -> Operation: ...
    def numpy(self) -> AnyArray: ...
    def __array__(self, dtype: DTypeLike | None = None) -> AnyArray: ...
    def __int__(self) -> int: ...
    def __abs__(self, name: str | None = None) -> Tensor: ...
    def __add__(self, other: TensorCompatible) -> Tensor: ...
    def __radd__(self, other: TensorCompatible) -> Tensor: ...
    def __sub__(self, other: TensorCompatible) -> Tensor: ...
    def __rsub__(self, other: TensorCompatible) -> Tensor: ...
    def __mul__(self, other: TensorCompatible) -> Tensor: ...
    def __rmul__(self, other: TensorCompatible) -> Tensor: ...
    def __pow__(self, other: TensorCompatible) -> Tensor: ...
    def __matmul__(self, other: TensorCompatible) -> Tensor: ...
    def __rmatmul__(self, other: TensorCompatible) -> Tensor: ...
    def __floordiv__(self, other: TensorCompatible) -> Tensor: ...
    def __rfloordiv__(self, other: TensorCompatible) -> Tensor: ...
    def __truediv__(self, other: TensorCompatible) -> Tensor: ...
    def __rtruediv__(self, other: TensorCompatible) -> Tensor: ...
    def __neg__(self, name: str | None = None) -> Tensor:
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
    def __and__(self, other: TensorCompatible) -> Tensor: ...
    def __rand__(self, other: TensorCompatible) -> Tensor: ...
    def __or__(self, other: TensorCompatible) -> Tensor: ...
    def __ror__(self, other: TensorCompatible) -> Tensor: ...
    def __eq__(self, other: TensorCompatible) -> Tensor: ...  # type: ignore[override]
    def __ne__(self, other: TensorCompatible) -> Tensor: ...  # type: ignore[override]
    def __ge__(self, other: TensorCompatible, name: str | None = None) -> Tensor:
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
    def __gt__(self, other: TensorCompatible, name: str | None = None) -> Tensor:
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
    def __le__(self, other: TensorCompatible, name: str | None = None) -> Tensor:
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
    def __lt__(self, other: TensorCompatible, name: str | None = None) -> Tensor:
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
    def __bool__(self) -> _bool:
        """
        Dummy method to prevent a tensor from being used as a Python `bool`.

        This overload raises a `TypeError` when the user inadvertently
        treats a `Tensor` as a boolean (most commonly in an `if` or `while`
        statement), in code that was not converted by AutoGraph. For example:

        ```python
        if tf.constant(True):  # Will raise.
          # ...

        if tf.constant(5) < tf.constant(7):  # Will raise.
          # ...
        ```

        Raises:
          `TypeError`.
        """
        ...
    def __getitem__(self, slice_spec: Slice | tuple[Slice, ...]) -> Tensor:
        """
        Overload for Tensor.__getitem__.

        This operation extracts the specified region from the tensor.
        The notation is similar to NumPy with the restriction that
        currently only support basic indexing. That means that
        using a non-scalar tensor as input is not currently allowed.

        Some useful examples:

        ```python
        # Strip leading and trailing 2 elements
        foo = tf.constant([1,2,3,4,5,6])
        print(foo[2:-2])  # => [3,4]

        # Skip every other row and reverse the order of the columns
        foo = tf.constant([[1,2,3], [4,5,6], [7,8,9]])
        print(foo[::2,::-1])  # => [[3,2,1], [9,8,7]]

        # Use scalar tensors as indices on both dimensions
        print(foo[tf.constant(0), tf.constant(2)])  # => 3

        # Insert another dimension
        foo = tf.constant([[1,2,3], [4,5,6], [7,8,9]])
        print(foo[tf.newaxis, :, :]) # => [[[1,2,3], [4,5,6], [7,8,9]]]
        print(foo[:, tf.newaxis, :]) # => [[[1,2,3]], [[4,5,6]], [[7,8,9]]]
        print(foo[:, :, tf.newaxis]) # => [[[1],[2],[3]], [[4],[5],[6]],
        [[7],[8],[9]]]

        # Ellipses (3 equivalent operations)
        foo = tf.constant([[1,2,3], [4,5,6], [7,8,9]])
        print(foo[tf.newaxis, :, :])  # => [[[1,2,3], [4,5,6], [7,8,9]]]
        print(foo[tf.newaxis, ...])  # => [[[1,2,3], [4,5,6], [7,8,9]]]
        print(foo[tf.newaxis])  # => [[[1,2,3], [4,5,6], [7,8,9]]]

        # Masks
        foo = tf.constant([[1,2,3], [4,5,6], [7,8,9]])
        print(foo[foo > 2])  # => [3, 4, 5, 6, 7, 8, 9]
        ```

        Notes:
          - `tf.newaxis` is `None` as in NumPy.
          - An implicit ellipsis is placed at the end of the `slice_spec`
          - NumPy advanced indexing is currently not supported.

        Purpose in the API:

          This method is exposed in TensorFlow's API so that library developers
          can register dispatching for `Tensor.__getitem__` to allow it to handle
          custom composite tensors & other custom objects.

          The API symbol is not intended to be called by users directly and does
          appear in TensorFlow's generated documentation.

        Args:
          tensor: An tensor.Tensor object.
          slice_spec: The arguments to Tensor.__getitem__.
          var: In the case of variable slice assignment, the Variable object to slice
            (i.e. tensor is the read-only view of this variable).

        Returns:
          The appropriate slice of "tensor", based on "slice_spec".

        Raises:
          ValueError: If a slice range is negative size.
          TypeError: If the slice indices aren't int, slice, ellipsis,
            tf.newaxis or scalar int32/int64 tensors.
        """
        ...
    def __len__(self) -> int: ...
    # This only works for rank 0 tensors.
    def __index__(self) -> int: ...
    def __getattr__(self, name: str) -> Incomplete: ...

class VariableSynchronization(Enum):
    """
    Indicates when a distributed variable will be synced.

    * `AUTO`: Indicates that the synchronization will be determined by the current
      `DistributionStrategy` (eg. With `MirroredStrategy` this would be
      `ON_WRITE`).
    * `NONE`: Indicates that there will only be one copy of the variable, so
      there is no need to sync.
    * `ON_WRITE`: Indicates that the variable will be updated across devices
      every time it is written.
    * `ON_READ`: Indicates that the variable will be aggregated across devices
      when it is read (eg. when checkpointing or when evaluating an op that uses
      the variable).

      Example:
    >>> temp_grad=[tf.Variable([0.], trainable=False,
    ...                      synchronization=tf.VariableSynchronization.ON_READ,
    ...                      aggregation=tf.VariableAggregation.MEAN
    ...                      )]
    """
    AUTO = 0
    NONE = 1
    ON_WRITE = 2
    ON_READ = 3

class VariableAggregation(Enum):
    """
    Indicates how a distributed variable will be aggregated.

    `tf.distribute.Strategy` distributes a model by making multiple copies
    (called "replicas") acting on different elements of the input batch in a
    data parallel model. When performing some variable-update operation,
    for example `var.assign_add(x)`, in a model, we need to resolve how to combine
    the different values for `x` computed in the different replicas.

    * `NONE`: This is the default, giving an error if you use a
      variable-update operation with multiple replicas.
    * `SUM`: Add the updates across replicas.
    * `MEAN`: Take the arithmetic mean ("average") of the updates across replicas.
    * `ONLY_FIRST_REPLICA`: This is for when every replica is performing the same
      update, but we only want to perform the update once. Used, e.g., for the
      global step counter.

    For example:

    >>> strategy = tf.distribute.MirroredStrategy(["GPU:0", "GPU:1"])
    >>> with strategy.scope():
    ...   v = tf.Variable(5.0, aggregation=tf.VariableAggregation.MEAN)
    >>> @tf.function
    ... def update_fn():
    ...   return v.assign_add(1.0)
    >>> strategy.run(update_fn)
    PerReplica:{
      0: <tf.Tensor: shape=(), dtype=float32, numpy=6.0>,
      1: <tf.Tensor: shape=(), dtype=float32, numpy=6.0>
    }
    """
    NONE = 0
    SUM = 1
    MEAN = 2
    ONLY_FIRST_REPLICA = 3

class _VariableMetaclass(type): ...

# Variable class in intent/documentation is a Tensor. In implementation there's
# TODO: comment to make it Tensor. It is not actually Tensor type wise, but even
# dynamically patches on most methods of tf.Tensor
# https://github.com/tensorflow/tensorflow/blob/9524a636cae9ae3f0554203c1ba7ee29c85fcf12/tensorflow/python/ops/variables.py#L1086.
class Variable(Tensor, metaclass=_VariableMetaclass):
    """
    See the [variable guide](https://tensorflow.org/guide/variable).

    A variable maintains shared, persistent state manipulated by a program.

    The `Variable()` constructor requires an initial value for the variable, which
    can be a `Tensor` of any type and shape. This initial value defines the type
    and shape of the variable. After construction, the type and shape of the
    variable are fixed. The value can be changed using one of the assign methods.

    >>> v = tf.Variable(1.)
    >>> v.assign(2.)
    <tf.Variable ... shape=() dtype=float32, numpy=2.0>
    >>> v.assign_add(0.5)
    <tf.Variable ... shape=() dtype=float32, numpy=2.5>

    The `shape` argument to `Variable`'s constructor allows you to construct a
    variable with a less defined shape than its `initial_value`:

    >>> v = tf.Variable(1., shape=tf.TensorShape(None))
    >>> v.assign([[1.]])
    <tf.Variable ... shape=<unknown> dtype=float32, numpy=array([[1.]], ...)>

    Just like any `Tensor`, variables created with `Variable()` can be used as
    inputs to operations. Additionally, all the operators overloaded for the
    `Tensor` class are carried over to variables.

    >>> w = tf.Variable([[1.], [2.]])
    >>> x = tf.constant([[3., 4.]])
    >>> tf.matmul(w, x)
    <tf.Tensor:... shape=(2, 2), ... numpy=
      array([[3., 4.],
             [6., 8.]], dtype=float32)>
    >>> tf.sigmoid(w + x)
    <tf.Tensor:... shape=(2, 2), ...>

    When building a machine learning model it is often convenient to distinguish
    between variables holding trainable model parameters and other variables such
    as a `step` variable used to count training steps. To make this easier, the
    variable constructor supports a `trainable=<bool>`
    parameter. `tf.GradientTape` watches trainable variables by default:

    >>> with tf.GradientTape(persistent=True) as tape:
    ...   trainable = tf.Variable(1.)
    ...   non_trainable = tf.Variable(2., trainable=False)
    ...   x1 = trainable * 2.
    ...   x2 = non_trainable * 3.
    >>> tape.gradient(x1, trainable)
    <tf.Tensor:... shape=(), dtype=float32, numpy=2.0>
    >>> assert tape.gradient(x2, non_trainable) is None  # Unwatched

    Variables are automatically tracked when assigned to attributes of types
    inheriting from `tf.Module`.

    >>> m = tf.Module()
    >>> m.v = tf.Variable([1.])
    >>> m.trainable_variables
    (<tf.Variable ... shape=(1,) ... numpy=array([1.], dtype=float32)>,)

    This tracking then allows saving variable values to
    [training checkpoints](https://www.tensorflow.org/guide/checkpoint), or to
    [SavedModels](https://www.tensorflow.org/guide/saved_model) which include
    serialized TensorFlow graphs.

    Variables are often captured and manipulated by `tf.function`s. This works the
    same way the un-decorated function would have:

    >>> v = tf.Variable(0.)
    >>> read_and_decrement = tf.function(lambda: v.assign_sub(0.1))
    >>> read_and_decrement()
    <tf.Tensor: shape=(), dtype=float32, numpy=-0.1>
    >>> read_and_decrement()
    <tf.Tensor: shape=(), dtype=float32, numpy=-0.2>

    Variables created inside a `tf.function` must be owned outside the function
    and be created only once:

    >>> class M(tf.Module):
    ...   @tf.function
    ...   def __call__(self, x):
    ...     if not hasattr(self, "v"):  # Or set self.v to None in __init__
    ...       self.v = tf.Variable(x)
    ...     return self.v * x
    >>> m = M()
    >>> m(2.)
    <tf.Tensor: shape=(), dtype=float32, numpy=4.0>
    >>> m(3.)
    <tf.Tensor: shape=(), dtype=float32, numpy=6.0>
    >>> m.v
    <tf.Variable ... shape=() dtype=float32, numpy=2.0>

    See the `tf.function` documentation for details.
    """
    def __init__(
        self,
        initial_value: Tensor | Callable[[], Tensor] | None = None,
        trainable: _bool | None = None,
        validate_shape: _bool = True,
        # Valid non-None values are deprecated.
        caching_device: None = None,
        name: str | None = None,
        # Real type is VariableDef protobuf type. Can be added after adding script
        # to generate tensorflow protobuf stubs with mypy-protobuf.
        variable_def=None,
        dtype: DTypeLike | None = None,
        import_scope: str | None = None,
        constraint: Callable[[Tensor], Tensor] | None = None,
        synchronization: VariableSynchronization = ...,
        aggregation: VariableAggregation = ...,
        shape: ShapeLike | None = None,
        experimental_enable_variable_lifting: _bool = True,
    ) -> None:
        """
        Creates a new variable with value `initial_value`. (deprecated arguments)

        Deprecated: SOME ARGUMENTS ARE DEPRECATED: `(caching_device)`. They will be removed in a future version.
        Instructions for updating:
        A variable's value can be manually cached by calling tf.Variable.read_value() under a tf.device scope. The caching_device argument does not work properly.

        Args:
          initial_value: A `Tensor`, or Python object convertible to a `Tensor`,
            which is the initial value for the Variable. The initial value must have
            a shape specified unless `validate_shape` is set to False. Can also be a
            callable with no argument that returns the initial value when called. In
            that case, `dtype` must be specified. (Note that initializer functions
            from init_ops.py must first be bound to a shape before being used here.)
          trainable: If `True`, GradientTapes automatically watch uses of this
            variable. Defaults to `True`, unless `synchronization` is set to
            `ON_READ`, in which case it defaults to `False`.
          validate_shape: If `False`, allows the variable to be initialized with a
            value of unknown shape. If `True`, the default, the shape of
            `initial_value` must be known.
          caching_device: Note: This argument is only valid when using a v1-style
            `Session`. Optional device string describing where the Variable should
            be cached for reading. Defaults to the Variable's device. If not `None`,
            caches on another device. Typical use is to cache on the device where
            the Ops using the Variable reside, to deduplicate copying through
            `Switch` and other conditional statements.
          name: Optional name for the variable. Defaults to `'Variable'` and gets
            uniquified automatically.
          variable_def: `VariableDef` protocol buffer. If not `None`, recreates the
            Variable object with its contents, referencing the variable's nodes in
            the graph, which must already exist. The graph is not changed.
            `variable_def` and the other arguments are mutually exclusive.
          dtype: If set, initial_value will be converted to the given type. If
            `None`, either the datatype will be kept (if `initial_value` is a
            Tensor), or `convert_to_tensor` will decide.
          import_scope: Optional `string`. Name scope to add to the `Variable.` Only
            used when initializing from protocol buffer.
          constraint: An optional projection function to be applied to the variable
            after being updated by an `Optimizer` (e.g. used to implement norm
            constraints or value constraints for layer weights). The function must
            take as input the unprojected Tensor representing the value of the
            variable and return the Tensor for the projected value (which must have
            the same shape). Constraints are not safe to use when doing asynchronous
            distributed training.
          synchronization: Indicates when a distributed variable will be
            aggregated. Accepted values are constants defined in the class
            `tf.VariableSynchronization`. By default the synchronization is set to
            `AUTO` and the current `DistributionStrategy` chooses when to
            synchronize.
          aggregation: Indicates how a distributed variable will be aggregated.
            Accepted values are constants defined in the class
            `tf.VariableAggregation`.
          shape: (optional) The shape of this variable. If None, the shape of
            `initial_value` will be used. When setting this argument to
            `tf.TensorShape(None)` (representing an unspecified shape), the variable
            can be assigned with values of different shapes.
          experimental_enable_variable_lifting: Whether to lift the variable out if
            it's in a `tf.function`. Default is `True`. When this argument
            is `True`, variable creation will follow the behavior and
            restrictions described
            [here](https://www.tensorflow.org/guide/function#creating_tfvariables).
            If this argument is `False`, that description doesn't apply,
            and you can freely create and use the variable in the
            `tf.function`, as if it's a "mutable `tf.Tensor`". You can't
            return the variable though.

        Raises:
          ValueError: If both `variable_def` and initial_value are specified.
          ValueError: If the initial value is not specified, or does not have a
            shape and `validate_shape` is `True`.
        """
        ...
    def __getattr__(self, name: str) -> Incomplete: ...

class RaggedTensor(metaclass=ABCMeta):
    """
    Represents a ragged tensor.

    A `RaggedTensor` is a tensor with one or more *ragged dimensions*, which are
    dimensions whose slices may have different lengths.  For example, the inner
    (column) dimension of `rt=[[3, 1, 4, 1], [], [5, 9, 2], [6], []]` is ragged,
    since the column slices (`rt[0, :]`, ..., `rt[4, :]`) have different lengths.
    Dimensions whose slices all have the same length are called *uniform
    dimensions*.  The outermost dimension of a `RaggedTensor` is always uniform,
    since it consists of a single slice (and so there is no possibility for
    differing slice lengths).

    The total number of dimensions in a `RaggedTensor` is called its *rank*,
    and the number of ragged dimensions in a `RaggedTensor` is called its
    *ragged-rank*.  A `RaggedTensor`'s ragged-rank is fixed at graph creation
    time: it can't depend on the runtime values of `Tensor`s, and can't vary
    dynamically for different session runs.

    Note that the `__init__` constructor is private. Please use one of the
    following methods to construct a `RaggedTensor`:

    * `tf.RaggedTensor.from_row_lengths`
    * `tf.RaggedTensor.from_value_rowids`
    * `tf.RaggedTensor.from_row_splits`
    * `tf.RaggedTensor.from_row_starts`
    * `tf.RaggedTensor.from_row_limits`
    * `tf.RaggedTensor.from_nested_row_splits`
    * `tf.RaggedTensor.from_nested_row_lengths`
    * `tf.RaggedTensor.from_nested_value_rowids`

    ### Potentially Ragged Tensors

    Many ops support both `Tensor`s and `RaggedTensor`s
    (see [tf.ragged](https://www.tensorflow.org/api_docs/python/tf/ragged) for a
    full listing). The term "potentially ragged tensor" may be used to refer to a
    tensor that might be either a `Tensor` or a `RaggedTensor`.  The ragged-rank
    of a `Tensor` is zero.

    ### Documenting RaggedTensor Shapes

    When documenting the shape of a RaggedTensor, ragged dimensions can be
    indicated by enclosing them in parentheses.  For example, the shape of
    a 3-D `RaggedTensor` that stores the fixed-size word embedding for each
    word in a sentence, for each sentence in a batch, could be written as
    `[num_sentences, (num_words), embedding_size]`.  The parentheses around
    `(num_words)` indicate that dimension is ragged, and that the length
    of each element list in that dimension may vary for each item.

    ### Component Tensors

    Internally, a `RaggedTensor` consists of a concatenated list of values that
    are partitioned into variable-length rows.  In particular, each `RaggedTensor`
    consists of:

      * A `values` tensor, which concatenates the variable-length rows into a
        flattened list.  For example, the `values` tensor for
        `[[3, 1, 4, 1], [], [5, 9, 2], [6], []]` is `[3, 1, 4, 1, 5, 9, 2, 6]`.

      * A `row_splits` vector, which indicates how those flattened values are
        divided into rows.  In particular, the values for row `rt[i]` are stored
        in the slice `rt.values[rt.row_splits[i]:rt.row_splits[i+1]]`.

    Example:

    >>> print(tf.RaggedTensor.from_row_splits(
    ...       values=[3, 1, 4, 1, 5, 9, 2, 6],
    ...       row_splits=[0, 4, 4, 7, 8, 8]))
    <tf.RaggedTensor [[3, 1, 4, 1], [], [5, 9, 2], [6], []]>

    ### Alternative Row-Partitioning Schemes

    In addition to `row_splits`, ragged tensors provide support for five other
    row-partitioning schemes:

      * `row_lengths`: a vector with shape `[nrows]`, which specifies the length
        of each row.

      * `value_rowids` and `nrows`: `value_rowids` is a vector with shape
        `[nvals]`, corresponding one-to-one with `values`, which specifies
        each value's row index.  In particular, the row `rt[row]` consists of the
        values `rt.values[j]` where `value_rowids[j]==row`.  `nrows` is an
        integer scalar that specifies the number of rows in the
        `RaggedTensor`. (`nrows` is used to indicate trailing empty rows.)

      * `row_starts`: a vector with shape `[nrows]`, which specifies the start
        offset of each row.  Equivalent to `row_splits[:-1]`.

      * `row_limits`: a vector with shape `[nrows]`, which specifies the stop
        offset of each row.  Equivalent to `row_splits[1:]`.

      * `uniform_row_length`: A scalar tensor, specifying the length of every
        row.  This row-partitioning scheme may only be used if all rows have
        the same length.

    Example: The following ragged tensors are equivalent, and all represent the
    nested list `[[3, 1, 4, 1], [], [5, 9, 2], [6], []]`.

    >>> values = [3, 1, 4, 1, 5, 9, 2, 6]
    >>> RaggedTensor.from_row_splits(values, row_splits=[0, 4, 4, 7, 8, 8])
    <tf.RaggedTensor [[3, 1, 4, 1], [], [5, 9, 2], [6], []]>
    >>> RaggedTensor.from_row_lengths(values, row_lengths=[4, 0, 3, 1, 0])
    <tf.RaggedTensor [[3, 1, 4, 1], [], [5, 9, 2], [6], []]>
    >>> RaggedTensor.from_value_rowids(
    ...     values, value_rowids=[0, 0, 0, 0, 2, 2, 2, 3], nrows=5)
    <tf.RaggedTensor [[3, 1, 4, 1], [], [5, 9, 2], [6], []]>
    >>> RaggedTensor.from_row_starts(values, row_starts=[0, 4, 4, 7, 8])
    <tf.RaggedTensor [[3, 1, 4, 1], [], [5, 9, 2], [6], []]>
    >>> RaggedTensor.from_row_limits(values, row_limits=[4, 4, 7, 8, 8])
    <tf.RaggedTensor [[3, 1, 4, 1], [], [5, 9, 2], [6], []]>
    >>> RaggedTensor.from_uniform_row_length(values, uniform_row_length=2)
    <tf.RaggedTensor [[3, 1], [4, 1], [5, 9], [2, 6]]>

    ### Multiple Ragged Dimensions

    `RaggedTensor`s with multiple ragged dimensions can be defined by using
    a nested `RaggedTensor` for the `values` tensor.  Each nested `RaggedTensor`
    adds a single ragged dimension.

    >>> inner_rt = RaggedTensor.from_row_splits(  # =rt1 from above
    ...     values=[3, 1, 4, 1, 5, 9, 2, 6], row_splits=[0, 4, 4, 7, 8, 8])
    >>> outer_rt = RaggedTensor.from_row_splits(
    ...     values=inner_rt, row_splits=[0, 3, 3, 5])
    >>> print(outer_rt.to_list())
    [[[3, 1, 4, 1], [], [5, 9, 2]], [], [[6], []]]
    >>> print(outer_rt.ragged_rank)
    2

    The factory function `RaggedTensor.from_nested_row_splits` may be used to
    construct a `RaggedTensor` with multiple ragged dimensions directly, by
    providing a list of `row_splits` tensors:

    >>> RaggedTensor.from_nested_row_splits(
    ...     flat_values=[3, 1, 4, 1, 5, 9, 2, 6],
    ...     nested_row_splits=([0, 3, 3, 5], [0, 4, 4, 7, 8, 8])).to_list()
    [[[3, 1, 4, 1], [], [5, 9, 2]], [], [[6], []]]

    ### Uniform Inner Dimensions

    `RaggedTensor`s with uniform inner dimensions can be defined
    by using a multidimensional `Tensor` for `values`.

    >>> rt = RaggedTensor.from_row_splits(values=tf.ones([5, 3], tf.int32),
    ...                                   row_splits=[0, 2, 5])
    >>> print(rt.to_list())
    [[[1, 1, 1], [1, 1, 1]],
     [[1, 1, 1], [1, 1, 1], [1, 1, 1]]]
    >>> print(rt.shape)
    (2, None, 3)

    ### Uniform Outer Dimensions

    `RaggedTensor`s with uniform outer dimensions can be defined by using
    one or more `RaggedTensor` with a `uniform_row_length` row-partitioning
    tensor.  For example, a `RaggedTensor` with shape `[2, 2, None]` can be
    constructed with this method from a `RaggedTensor` values with shape
    `[4, None]`:

    >>> values = tf.ragged.constant([[1, 2, 3], [4], [5, 6], [7, 8, 9, 10]])
    >>> print(values.shape)
    (4, None)
    >>> rt6 = tf.RaggedTensor.from_uniform_row_length(values, 2)
    >>> print(rt6)
    <tf.RaggedTensor [[[1, 2, 3], [4]], [[5, 6], [7, 8, 9, 10]]]>
    >>> print(rt6.shape)
    (2, 2, None)

    Note that `rt6` only contains one ragged dimension (the innermost
    dimension). In contrast, if `from_row_splits` is used to construct a similar
    `RaggedTensor`, then that `RaggedTensor` will have two ragged dimensions:

    >>> rt7 = tf.RaggedTensor.from_row_splits(values, [0, 2, 4])
    >>> print(rt7.shape)
    (2, None, None)

    Uniform and ragged outer dimensions may be interleaved, meaning that a
    tensor with any combination of ragged and uniform dimensions may be created.
    For example, a RaggedTensor `t4` with shape `[3, None, 4, 8, None, 2]` could
    be constructed as follows:

    ```python
    t0 = tf.zeros([1000, 2])                           # Shape:         [1000, 2]
    t1 = RaggedTensor.from_row_lengths(t0, [...])      #           [160, None, 2]
    t2 = RaggedTensor.from_uniform_row_length(t1, 8)   #         [20, 8, None, 2]
    t3 = RaggedTensor.from_uniform_row_length(t2, 4)   #       [5, 4, 8, None, 2]
    t4 = RaggedTensor.from_row_lengths(t3, [...])      # [3, None, 4, 8, None, 2]
    ```
    """
    def bounding_shape(
        self, axis: TensorCompatible | None = None, name: str | None = None, out_type: DTypeLike | None = None
    ) -> Tensor:
        """
        Returns the tight bounding box shape for this `RaggedTensor`.

        Args:
          axis: An integer scalar or vector indicating which axes to return the
            bounding box for.  If not specified, then the full bounding box is
            returned.
          name: A name prefix for the returned tensor (optional).
          out_type: `dtype` for the returned tensor.  Defaults to
            `self.row_splits.dtype`.

        Returns:
          An integer `Tensor` (`dtype=self.row_splits.dtype`).  If `axis` is not
          specified, then `output` is a vector with
          `output.shape=[self.shape.ndims]`.  If `axis` is a scalar, then the
          `output` is a scalar.  If `axis` is a vector, then `output` is a vector,
          where `output[i]` is the bounding size for dimension `axis[i]`.

        #### Example:

        >>> rt = tf.ragged.constant([[1, 2, 3, 4], [5], [], [6, 7, 8, 9], [10]])
        >>> rt.bounding_shape().numpy()
        array([5, 4])
        """
        ...
    @classmethod
    def from_sparse(cls, st_input: SparseTensor, name: str | None = None, row_splits_dtype: DTypeLike = ...) -> RaggedTensor:
        """
        Converts a 2D `tf.sparse.SparseTensor` to a `RaggedTensor`.

        Each row of the `output` `RaggedTensor` will contain the explicit values
        from the same row in `st_input`.  `st_input` must be ragged-right.  If not
        it is not ragged-right, then an error will be generated.

        Example:

        >>> indices = [[0, 0], [0, 1], [0, 2], [1, 0], [3, 0]]
        >>> st = tf.sparse.SparseTensor(indices=indices,
        ...                             values=[1, 2, 3, 4, 5],
        ...                             dense_shape=[4, 3])
        >>> tf.RaggedTensor.from_sparse(st).to_list()
        [[1, 2, 3], [4], [], [5]]

        Currently, only two-dimensional `SparseTensors` are supported.

        Args:
          st_input: The sparse tensor to convert.  Must have rank 2.
          name: A name prefix for the returned tensors (optional).
          row_splits_dtype: `dtype` for the returned `RaggedTensor`'s `row_splits`
            tensor.  One of `tf.int32` or `tf.int64`.

        Returns:
          A `RaggedTensor` with the same values as `st_input`.
          `output.ragged_rank = rank(st_input) - 1`.
          `output.shape = [st_input.dense_shape[0], None]`.
        Raises:
          ValueError: If the number of dimensions in `st_input` is not known
            statically, or is not two.
        """
        ...
    def to_sparse(self, name: str | None = None) -> SparseTensor:
        """
        Converts this `RaggedTensor` into a `tf.sparse.SparseTensor`.

        Example:

        >>> rt = tf.ragged.constant([[1, 2, 3], [4], [], [5, 6]])
        >>> print(rt.to_sparse())
        SparseTensor(indices=tf.Tensor(
                         [[0 0] [0 1] [0 2] [1 0] [3 0] [3 1]],
                         shape=(6, 2), dtype=int64),
                     values=tf.Tensor([1 2 3 4 5 6], shape=(6,), dtype=int32),
                     dense_shape=tf.Tensor([4 3], shape=(2,), dtype=int64))

        Args:
          name: A name prefix for the returned tensors (optional).

        Returns:
          A SparseTensor with the same values as `self`.
        """
        ...
    def to_tensor(
        self, default_value: float | str | None = None, name: str | None = None, shape: ShapeLike | None = None
    ) -> Tensor:
        """
        Converts this `RaggedTensor` into a `tf.Tensor`.

        If `shape` is specified, then the result is padded and/or truncated to
        the specified shape.

        Examples:

        >>> rt = tf.ragged.constant([[9, 8, 7], [], [6, 5], [4]])
        >>> print(rt.to_tensor())
        tf.Tensor(
            [[9 8 7] [0 0 0] [6 5 0] [4 0 0]], shape=(4, 3), dtype=int32)
        >>> print(rt.to_tensor(shape=[5, 2]))
        tf.Tensor(
            [[9 8] [0 0] [6 5] [4 0] [0 0]], shape=(5, 2), dtype=int32)

        Args:
          default_value: Value to set for indices not specified in `self`. Defaults
            to zero.  `default_value` must be broadcastable to
            `self.shape[self.ragged_rank + 1:]`.
          name: A name prefix for the returned tensors (optional).
          shape: The shape of the resulting dense tensor.  In particular,
            `result.shape[i]` is `shape[i]` (if `shape[i]` is not None), or
            `self.bounding_shape(i)` (otherwise).`shape.rank` must be `None` or
            equal to `self.rank`.

        Returns:
          A `Tensor` with shape `ragged.bounding_shape(self)` and the
          values specified by the non-empty values in `self`.  Empty values are
          assigned `default_value`.
        """
        ...
    def __add__(self, other: RaggedTensor | float, name: str | None = None) -> RaggedTensor:
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
    def __radd__(self, other: RaggedTensor | float, name: str | None = None) -> RaggedTensor:
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
    def __sub__(self, other: RaggedTensor | float, name: str | None = None) -> RaggedTensor:
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
    def __mul__(self, other: RaggedTensor | float, name: str | None = None) -> RaggedTensor:
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
    def __rmul__(self, other: RaggedTensor | float, name: str | None = None) -> RaggedTensor:
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
    def __floordiv__(self, other: RaggedTensor | float, name: str | None = None) -> RaggedTensor:
        """
        Divides `x / y` elementwise, rounding toward the most negative integer.

        Mathematically, this is equivalent to floor(x / y). For example:
          floor(8.4 / 4.0) = floor(2.1) = 2.0
          floor(-8.4 / 4.0) = floor(-2.1) = -3.0
        This is equivalent to the '//' operator in Python 3.0 and above.

        Note: `x` and `y` must have the same type, and the result will have the same
        type as well.

        Args:
          x: `Tensor` numerator of real numeric type.
          y: `Tensor` denominator of real numeric type.
          name: A name for the operation (optional).

        Returns:
          `x / y` rounded toward -infinity.

        Raises:
          TypeError: If the inputs are complex.
        """
        ...
    def __truediv__(self, other: RaggedTensor | float, name: str | None = None) -> RaggedTensor:
        """
        Divides x / y elementwise (using Python 3 division operator semantics).

        NOTE: Prefer using the Tensor operator or tf.divide which obey Python
        division operator semantics.

        This function forces Python 3 division operator semantics where all integer
        arguments are cast to floating types first.   This op is generated by normal
        `x / y` division in Python 3 and in Python 2.7 with
        `from __future__ import division`.  If you want integer division that rounds
        down, use `x // y` or `tf.math.floordiv`.

        `x` and `y` must have the same numeric type.  If the inputs are floating
        point, the output will have the same type.  If the inputs are integral, the
        inputs are cast to `float32` for `int8` and `int16` and `float64` for `int32`
        and `int64` (matching the behavior of Numpy).

        Args:
          x: `Tensor` numerator of numeric type.
          y: `Tensor` denominator of numeric type.
          name: A name for the operation (optional).

        Returns:
          `x / y` evaluated in floating point.

        Raises:
          TypeError: If `x` and `y` have different dtypes.
        """
        ...
    def __getitem__(self, slice_spec: Slice | tuple[Slice, ...]) -> RaggedTensor:
        """
        Returns the specified piece of this RaggedTensor.

        Supports multidimensional indexing and slicing, with one restriction:
        indexing into a ragged inner dimension is not allowed.  This case is
        problematic because the indicated value may exist in some rows but not
        others.  In such cases, it's not obvious whether we should (1) report an
        IndexError; (2) use a default value; or (3) skip that value and return a
        tensor with fewer rows than we started with.  Following the guiding
        principles of Python ("In the face of ambiguity, refuse the temptation to
        guess"), we simply disallow this operation.

        Args:
          rt_input: The RaggedTensor to slice.
          key: Indicates which piece of the RaggedTensor to return, using standard
            Python semantics (e.g., negative values index from the end).  `key`
            may have any of the following types:

            * `int` constant
            * Scalar integer `Tensor`
            * `slice` containing integer constants and/or scalar integer
              `Tensor`s
            * `Ellipsis`
            * `tf.newaxis`
            * `tuple` containing any of the above (for multidimensional indexing)

        Returns:
          A `Tensor` or `RaggedTensor` object.  Values that include at least one
          ragged dimension are returned as `RaggedTensor`.  Values that include no
          ragged dimensions are returned as `Tensor`.  See above for examples of
          expressions that return `Tensor`s vs `RaggedTensor`s.

        Raises:
          ValueError: If `key` is out of bounds.
          ValueError: If `key` is not supported.
          TypeError: If the indices in `key` have an unsupported type.

        Examples:

        >>> # A 2-D ragged tensor with 1 ragged dimension.
        >>> rt = tf.ragged.constant([['a', 'b', 'c'], ['d', 'e'], ['f'], ['g']])
        >>> rt[0].numpy()                 # First row (1-D `Tensor`)
        array([b'a', b'b', b'c'], dtype=object)
        >>> rt[:3].to_list()              # First three rows (2-D RaggedTensor)
        [[b'a', b'b', b'c'], [b'd', b'e'], [b'f']]
        >>> rt[3, 0].numpy()              # 1st element of 4th row (scalar)
        b'g'

        >>> # A 3-D ragged tensor with 2 ragged dimensions.
        >>> rt = tf.ragged.constant([[[1, 2, 3], [4]],
        ...                          [[5], [], [6]],
        ...                          [[7]],
        ...                          [[8, 9], [10]]])
        >>> rt[1].to_list()               # Second row (2-D RaggedTensor)
        [[5], [], [6]]
        >>> rt[3, 0].numpy()              # First element of fourth row (1-D Tensor)
        array([8, 9], dtype=int32)
        >>> rt[:, 1:3].to_list()          # Items 1-3 of each row (3-D RaggedTensor)
        [[[4]], [[], [6]], [], [[10]]]
        >>> rt[:, -1:].to_list()          # Last item of each row (3-D RaggedTensor)
        [[[4]], [[6]], [[7]], [[10]]]
        """
        ...
    def __getattr__(self, name: str) -> Incomplete: ...

class Operation:
    """
    Represents a graph node that performs computation on tensors.

    An `Operation` is a node in a `tf.Graph` that takes zero or more `Tensor`
    objects as input, and produces zero or more `Tensor` objects as output.
    Objects of type `Operation` are created by calling a Python op constructor
    (such as `tf.matmul`) within a `tf.function` or under a `tf.Graph.as_default`
    context manager.

    For example, within a `tf.function`, `c = tf.matmul(a, b)` creates an
    `Operation` of type "MatMul" that takes tensors `a` and `b` as input, and
    produces `c` as output.

    If a `tf.compat.v1.Session` is used, an `Operation` of a `tf.Graph` can be
    executed by passing it to `tf.Session.run`. `op.run()` is a shortcut for
    calling `tf.compat.v1.get_default_session().run(op)`.
    """
    def __init__(
        self,
        node_def,
        g: Graph,
        # isinstance is used so can not be Sequence/Iterable.
        inputs: list[Tensor] | None = None,
        output_types: Unused = None,
        control_inputs: Iterable[Tensor | Operation] | None = None,
        input_types: Iterable[DType] | None = None,
        original_op: Operation | None = None,
        op_def=None,
    ) -> None: ...
    @property
    def inputs(self) -> list[Tensor]:
        """The sequence of `Tensor` objects representing the data inputs of this op."""
        ...
    @property
    def outputs(self) -> list[Tensor]: ...
    @property
    def device(self) -> str:
        """
        The name of the device to which this op has been assigned, if any.

        Returns:
          The string name of the device to which this op has been
          assigned, or an empty string if it has not been assigned to a
          device.
        """
        ...
    @property
    def name(self) -> str: ...
    @property
    def type(self) -> str: ...
    def __getattr__(self, name: str) -> Incomplete: ...

class TensorShape(metaclass=ABCMeta):
    """
    Represents the shape of a `Tensor`.

    >>> t = tf.constant([[1,2,3],[4,5,6]])
    >>> t.shape
    TensorShape([2, 3])

    `TensorShape` is the *static* shape representation of a Tensor.
    During eager execution a Tensor always has a fully specified shape but
    when tracing a `tf.function` it may be one of the following:

    * *Fully-known shape:* has a known number of dimensions and a known size
      for each dimension. e.g. `TensorShape([16, 256])`
    * *Partially-known shape:* has a known number of dimensions, and an unknown
      size for one or more dimension. e.g. `TensorShape([None, 256])`
    * *Unknown shape:* has an unknown number of dimensions, and an unknown
      size in all dimensions. e.g. `TensorShape(None)`

    During function tracing `t.shape` will return a `TensorShape` object
    representing the shape of Tensor as it is known during tracing.
    This static representation will be partially defined in cases where the
    exact shape depends on the values within the tensors. To get the
    *dynamic* representation, please use `tf.shape(t)`
    which will return Tensor representing the fully defined shape of `t`.
    This way, you can express logic that manipulates the shapes of tensors by
    building other tensors that depend on the dynamic shape of `t`.

    Note: `tf.RaggedTensor.shape` also returns a `tf.TensorShape`,
    the lengths of any ragged dimensions are unknown (`None`).

    For example, this function prints the `TensorShape' (`t.shape`), when you
    trace the function, and returns a tensor `tf.shape(t)` for given input `t`:

    >>> @tf.function
    ... def get_dynamic_shape(t):
    ...   print("tracing...")
    ...   print(f"static shape is {t.shape}")
    ...   return tf.shape(t)

    Just calling the function traces it with a fully-specified static shape:

    >>> result = get_dynamic_shape(tf.constant([[1, 1, 1], [0, 0, 0]]))
    tracing...
    static shape is (2, 3)
    >>> result.numpy()
    array([2, 3], dtype=int32)

    But `tf.function` can also trace the function with a partially specified
    (or even unspecified) shape:

    >>> cf1 = get_dynamic_shape.get_concrete_function(tf.TensorSpec(
    ...                                               shape=[None, 2]))
    tracing...
    static shape is (None, 2)
    >>> cf1(tf.constant([[1., 0],[1, 0],[1, 0]])).numpy()
    array([3, 2], dtype=int32)

    >>> cf2 = get_dynamic_shape.get_concrete_function(tf.TensorSpec(shape=None))
    tracing...
    static shape is <unknown>
    >>> cf2(tf.constant([[[[[1., 0]]]]])).numpy()
    array([1, 1, 1, 1, 2], dtype=int32)

    If a tensor is produced by an operation of type `"Foo"`, its shape
    may be inferred if there is a registered shape function for
    `"Foo"`. See [Shape
    functions](https://www.tensorflow.org/guide/create_op#shape_functions_in_c)
    for details of shape functions and how to register them. Alternatively,
    you may set the shape explicitly using `tf.Tensor.ensure_shape`.
    """
    __slots__ = ["_dims"]
    def __init__(self, dims: ShapeLike) -> None:
        """
        Creates a new TensorShape with the given dimensions.

        Args:
          dims: A list of Dimensions, or None if the shape is unspecified.

        Raises:
          TypeError: If dims cannot be converted to a list of dimensions.
        """
        ...
    @property
    def rank(self) -> int:
        """Returns the rank of this shape, or None if it is unspecified."""
        ...
    def as_list(self) -> list[int | None]:
        """
        Returns a list of integers or `None` for each dimension.

        Returns:
          A list of integers or `None` for each dimension.

        Raises:
          ValueError: If `self` is an unknown shape with an unknown rank.
        """
        ...
    def assert_has_rank(self, rank: int) -> None:
        """
        Raises an exception if `self` is not compatible with the given `rank`.

        Args:
          rank: An integer.

        Raises:
          ValueError: If `self` does not represent a shape with the given `rank`.
        """
        ...
    def assert_is_compatible_with(self, other: Iterable[int | None]) -> None:
        """
        Raises exception if `self` and `other` do not represent the same shape.

        This method can be used to assert that there exists a shape that both
        `self` and `other` represent.

        Args:
          other: Another TensorShape.

        Raises:
          ValueError: If `self` and `other` do not represent the same shape.
        """
        ...
    def __bool__(self) -> _bool:
        """Returns True if this shape contains non-zero information."""
        ...
    @overload
    def __getitem__(self, key: int) -> int | None:
        """
        Returns the value of a dimension or a shape, depending on the key.

        Args:
          key: If `key` is an integer, returns the dimension at that index;
            otherwise if `key` is a slice, returns a TensorShape whose dimensions
            are those selected by the slice from `self`.

        Returns:
          An integer if `key` is an integer, or a `TensorShape` if `key` is a
          slice.

        Raises:
          ValueError: If `key` is a slice and `self` is completely unknown and
            the step is set.
        """
        ...
    @overload
    def __getitem__(self, key: slice) -> TensorShape:
        """
        Returns the value of a dimension or a shape, depending on the key.

        Args:
          key: If `key` is an integer, returns the dimension at that index;
            otherwise if `key` is a slice, returns a TensorShape whose dimensions
            are those selected by the slice from `self`.

        Returns:
          An integer if `key` is an integer, or a `TensorShape` if `key` is a
          slice.

        Raises:
          ValueError: If `key` is a slice and `self` is completely unknown and
            the step is set.
        """
        ...
    def __iter__(self) -> Iterator[int | None]:
        """Returns `self.dims` if the rank is known, otherwise raises ValueError."""
        ...
    def __len__(self) -> int:
        """Returns the rank of this shape, or raises ValueError if unspecified."""
        ...
    def __add__(self, other: Iterable[int | None]) -> TensorShape: ...
    def __radd__(self, other: Iterable[int | None]) -> TensorShape: ...
    def __getattr__(self, name: str) -> Incomplete: ...

class Graph:
    """
    A TensorFlow computation, represented as a dataflow graph.

    Graphs are used by `tf.function`s to represent the function's computations.
    Each graph contains a set of `tf.Operation` objects, which represent units of
    computation; and `tf.Tensor` objects, which represent the units of data that
    flow between operations.

    ### Using graphs directly (deprecated)

    A `tf.Graph` can be constructed and used directly without a `tf.function`, as
    was required in TensorFlow 1, but this is deprecated and it is recommended to
    use a `tf.function` instead. If a graph is directly used, other deprecated
    TensorFlow 1 classes are also required to execute the graph, such as a
    `tf.compat.v1.Session`.

    A default graph can be registered with the `tf.Graph.as_default` context
    manager. Then, operations will be added to the graph instead of being executed
    eagerly. For example:

    ```python
    g = tf.Graph()
    with g.as_default():
      # Define operations and tensors in `g`.
      c = tf.constant(30.0)
      assert c.graph is g
    ```

    `tf.compat.v1.get_default_graph()` can be used to obtain the default graph.

    Important note: This class *is not* thread-safe for graph construction. All
    operations should be created from a single thread, or external
    synchronization must be provided. Unless otherwise specified, all methods
    are not thread-safe.

    A `Graph` instance supports an arbitrary number of "collections"
    that are identified by name. For convenience when building a large
    graph, collections can store groups of related objects: for
    example, the `tf.Variable` uses a collection (named
    `tf.GraphKeys.GLOBAL_VARIABLES`) for
    all variables that are created during the construction of a graph. The caller
    may define additional collections by specifying a new name.
    """
    def add_to_collection(self, name: str, value: object) -> None:
        """
        Stores `value` in the collection with the given `name`.

        Note that collections are not sets, so it is possible to add a value to
        a collection several times.

        Args:
          name: The key for the collection. The `GraphKeys` class contains many
            standard names for collections.
          value: The value to add to the collection.
        """
        ...
    def add_to_collections(self, names: Iterable[str] | str, value: object) -> None:
        """
        Stores `value` in the collections given by `names`.

        Note that collections are not sets, so it is possible to add a value to
        a collection several times. This function makes sure that duplicates in
        `names` are ignored, but it will not check for pre-existing membership of
        `value` in any of the collections in `names`.

        `names` can be any iterable, but if `names` is a string, it is treated as a
        single collection name.

        Args:
          names: The keys for the collections to add to. The `GraphKeys` class
            contains many standard names for collections.
          value: The value to add to the collections.
        """
        ...
    @contextmanager
    def as_default(self) -> Generator[Self]:
        """
        Returns a context manager that makes this `Graph` the default graph.

        This method should be used if you want to create multiple graphs
        in the same process. For convenience, a global default graph is
        provided, and all ops will be added to this graph if you do not
        create a new graph explicitly.

        Use this method with the `with` keyword to specify that ops created within
        the scope of a block should be added to this graph. In this case, once
        the scope of the `with` is exited, the previous default graph is set again
        as default. There is a stack, so it's ok to have multiple nested levels
        of `as_default` calls.

        The default graph is a property of the current thread. If you
        create a new thread, and wish to use the default graph in that
        thread, you must explicitly add a `with g.as_default():` in that
        thread's function.

        The following code examples are equivalent:

        ```python
        # 1. Using Graph.as_default():
        g = tf.Graph()
        with g.as_default():
          c = tf.constant(5.0)
          assert c.graph is g

        # 2. Constructing and making default:
        with tf.Graph().as_default() as g:
          c = tf.constant(5.0)
          assert c.graph is g
        ```

        If eager execution is enabled ops created under this context manager will be
        added to the graph instead of executed eagerly.

        Returns:
          A context manager for using this graph as the default graph.
        """
        ...
    def finalize(self) -> None:
        """
        Finalizes this graph, making it read-only.

        After calling `g.finalize()`, no new operations can be added to
        `g`.  This method is used to ensure that no operations are added
        to a graph when it is shared between multiple threads, for example
        when using a `tf.compat.v1.train.QueueRunner`.
        """
        ...
    def get_tensor_by_name(self, name: str) -> Tensor:
        """
        Returns the `Tensor` with the given `name`.

        This method may be called concurrently from multiple threads.

        Args:
          name: The name of the `Tensor` to return.

        Returns:
          The `Tensor` with the given `name`.

        Raises:
          TypeError: If `name` is not a string.
          KeyError: If `name` does not correspond to a tensor in this graph.
        """
        ...
    def get_operation_by_name(self, name: str) -> Operation:
        """
        Returns the `Operation` with the given `name`.

        This method may be called concurrently from multiple threads.

        Args:
          name: The name of the `Operation` to return.

        Returns:
          The `Operation` with the given `name`.

        Raises:
          TypeError: If `name` is not a string.
          KeyError: If `name` does not correspond to an operation in this graph.
        """
        ...
    def get_operations(self) -> list[Operation]:
        """(self: object) -> list"""
        ...
    def get_name_scope(self) -> str:
        """
        Returns the current name scope.

        For example:

        ```python
        with tf.name_scope('scope1'):
          with tf.name_scope('scope2'):
            print(tf.compat.v1.get_default_graph().get_name_scope())
        ```
        would print the string `scope1/scope2`.

        Returns:
          A string representing the current name scope.
        """
        ...
    def __getattr__(self, name: str) -> Incomplete: ...

class IndexedSlices(metaclass=ABCMeta):
    """
    A sparse representation of a set of tensor slices at given indices.

    This class is a simple wrapper for a pair of `Tensor` objects:

    * `values`: A `Tensor` of any dtype with shape `[D0, D1, ..., Dn]`.
    * `indices`: A 1-D integer `Tensor` with shape `[D0]`.

    An `IndexedSlices` is typically used to represent a subset of a larger
    tensor `dense` of shape `[LARGE0, D1, .. , DN]` where `LARGE0 >> D0`.
    The values in `indices` are the indices in the first dimension of
    the slices that have been extracted from the larger tensor.

    The dense tensor `dense` represented by an `IndexedSlices` `slices` has

    ```python
    dense[slices.indices[i], :, :, :, ...] = slices.values[i, :, :, :, ...]
    ```

    The `IndexedSlices` class is used principally in the definition of
    gradients for operations that have sparse gradients
    (e.g. `tf.gather`).

    >>> v = tf.Variable([[0.,1, 2], [2, 3, 4], [4, 5, 6], [6, 7, 8]])
    >>> with tf.GradientTape() as tape:
    ...   r = tf.gather(v, [1,3])
    >>> index_slices = tape.gradient(r,v)
    >>> index_slices
    <...IndexedSlices object ...>
    >>> index_slices.indices.numpy()
    array([1, 3], dtype=int32)
    >>> index_slices.values.numpy()
    array([[1., 1., 1.],
           [1., 1., 1.]], dtype=float32)

    Contrast this representation with
    `tf.sparse.SparseTensor`,
    which uses multi-dimensional indices and scalar values.
    """
    def __init__(self, values: Tensor, indices: Tensor, dense_shape: None | Tensor = None) -> None:
        """Creates an `IndexedSlices`."""
        ...
    @property
    def values(self) -> Tensor:
        """A `Tensor` containing the values of the slices."""
        ...
    @property
    def indices(self) -> Tensor:
        """A 1-D `Tensor` containing the indices of the slices."""
        ...
    @property
    def dense_shape(self) -> None | Tensor:
        """A 1-D `Tensor` containing the shape of the corresponding dense tensor."""
        ...
    @property
    def shape(self) -> TensorShape:
        """
        Gets the `tf.TensorShape` representing the shape of the dense tensor.

        Returns:
          A `tf.TensorShape` object.
        """
        ...
    @property
    def dtype(self) -> DType:
        """The `DType` of elements in this tensor."""
        ...
    @property
    def name(self) -> str:
        """The name of this `IndexedSlices`."""
        ...
    @property
    def op(self) -> Operation:
        """The `Operation` that produces `values` as an output."""
        ...
    @property
    def graph(self) -> Graph:
        """The `Graph` that contains the values, indices, and shape tensors."""
        ...
    @property
    def device(self) -> str:
        """The name of the device on which `values` will be produced, or `None`."""
        ...
    def __neg__(self) -> IndexedSlices: ...
    def consumers(self) -> list[Operation]: ...

class name_scope(metaclass=abc.ABCMeta):
    """
    A context manager for use when defining a Python op.

    This context manager pushes a name scope, which will make the name of all
    operations added within it have a prefix.

    For example, to define a new Python op called `my_op`:

    ```python
    def my_op(a, b, c, name=None):
      with tf.name_scope("MyOp") as scope:
        a = tf.convert_to_tensor(a, name="a")
        b = tf.convert_to_tensor(b, name="b")
        c = tf.convert_to_tensor(c, name="c")
        # Define some computation that uses `a`, `b`, and `c`.
        return foo_op(..., name=scope)
    ```

    When executed, the Tensors `a`, `b`, `c`, will have names `MyOp/a`, `MyOp/b`,
    and `MyOp/c`.

    Inside a `tf.function`, if the scope name already exists, the name will be
    made unique by appending `_n`. For example, calling `my_op` the second time
    will generate `MyOp_1/a`, etc.
    """
    def __init__(self, name: str) -> None:
        """
        Initialize the context manager.

        Args:
          name: The prefix to use on all names created within the name scope.

        Raises:
          ValueError: If name is not a string.
        """
        ...
    def __enter__(self) -> str:
        """
        Start the scope block.

        Returns:
          The scope name.
        """
        ...
    def __exit__(self, typ: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None: ...

_P = ParamSpec("_P")
_R = TypeVar("_R")

class Module(AutoTrackable):
    """
    Base neural network module class.

    A module is a named container for `tf.Variable`s, other `tf.Module`s and
    functions which apply to user input. For example a dense layer in a neural
    network might be implemented as a `tf.Module`:

    >>> class Dense(tf.Module):
    ...   def __init__(self, input_dim, output_size, name=None):
    ...     super().__init__(name=name)
    ...     self.w = tf.Variable(
    ...       tf.random.normal([input_dim, output_size]), name='w')
    ...     self.b = tf.Variable(tf.zeros([output_size]), name='b')
    ...   def __call__(self, x):
    ...     y = tf.matmul(x, self.w) + self.b
    ...     return tf.nn.relu(y)

    You can use the Dense layer as you would expect:

    >>> d = Dense(input_dim=3, output_size=2)
    >>> d(tf.ones([1, 3]))
    <tf.Tensor: shape=(1, 2), dtype=float32, numpy=..., dtype=float32)>


    By subclassing `tf.Module` instead of `object` any `tf.Variable` or
    `tf.Module` instances assigned to object properties can be collected using
    the `variables`, `trainable_variables` or `submodules` property:

    >>> d.variables
        (<tf.Variable 'b:0' shape=(2,) dtype=float32, numpy=...,
        dtype=float32)>,
        <tf.Variable 'w:0' shape=(3, 2) dtype=float32, numpy=..., dtype=float32)>)


    Subclasses of `tf.Module` can also take advantage of the `_flatten` method
    which can be used to implement tracking of any other types.

    All `tf.Module` classes have an associated `tf.name_scope` which can be used
    to group operations in TensorBoard and create hierarchies for variable names
    which can help with debugging. We suggest using the name scope when creating
    nested submodules/parameters or for forward methods whose graph you might want
    to inspect in TensorBoard. You can enter the name scope explicitly using
    `with self.name_scope:` or you can annotate methods (apart from `__init__`)
    with `@tf.Module.with_name_scope`.

    >>> class MLP(tf.Module):
    ...   def __init__(self, input_size, sizes, name=None):
    ...     super().__init__(name=name)
    ...     self.layers = []
    ...     with self.name_scope:
    ...       for size in sizes:
    ...         self.layers.append(Dense(input_dim=input_size, output_size=size))
    ...         input_size = size
    ...   @tf.Module.with_name_scope
    ...   def __call__(self, x):
    ...     for layer in self.layers:
    ...       x = layer(x)
    ...     return x

    >>> module = MLP(input_size=5, sizes=[5, 5])
    >>> module.variables
    (<tf.Variable 'mlp/b:0' shape=(5,) dtype=float32, numpy=..., dtype=float32)>,
    <tf.Variable 'mlp/w:0' shape=(5, 5) dtype=float32, numpy=...,
       dtype=float32)>,
    <tf.Variable 'mlp/b:0' shape=(5,) dtype=float32, numpy=..., dtype=float32)>,
    <tf.Variable 'mlp/w:0' shape=(5, 5) dtype=float32, numpy=...,
       dtype=float32)>)
    """
    def __init__(self, name: str | None = None) -> None: ...
    @property
    def name(self) -> str:
        """
        Returns the name of this module as passed or determined in the ctor.

        NOTE: This is not the same as the `self.name_scope.name` which includes
        parent module names.
        """
        ...
    @property
    def name_scope(self) -> name_scope:
        """Returns a `tf.name_scope` instance for this class."""
        ...
    # Documentation only specifies these as returning Sequence. Actual
    # implementation does tuple.
    @property
    def variables(self) -> Sequence[Variable]:
        """
        Sequence of variables owned by this module and its submodules.

        Note: this method uses reflection to find variables on the current instance
        and submodules. For performance reasons you may wish to cache the result
        of calling this method if you don't expect the return value to change.

        Returns:
          A sequence of variables for the current module (sorted by attribute
          name) followed by variables from all submodules recursively (breadth
          first).
        """
        ...
    @property
    def trainable_variables(self) -> Sequence[Variable]:
        """
        Sequence of trainable variables owned by this module and its submodules.

        Note: this method uses reflection to find variables on the current instance
        and submodules. For performance reasons you may wish to cache the result
        of calling this method if you don't expect the return value to change.

        Returns:
          A sequence of variables for the current module (sorted by attribute
          name) followed by variables from all submodules recursively (breadth
          first).
        """
        ...
    @property
    def non_trainable_variables(self) -> Sequence[Variable]:
        """
        Sequence of non-trainable variables owned by this module and its submodules.

        Note: this method uses reflection to find variables on the current instance
        and submodules. For performance reasons you may wish to cache the result
        of calling this method if you don't expect the return value to change.

        Returns:
          A sequence of variables for the current module (sorted by attribute
          name) followed by variables from all submodules recursively (breadth
          first).
        """
        ...
    @property
    def submodules(self) -> Sequence[Module]:
        """
        Sequence of all sub-modules.

        Submodules are modules which are properties of this module, or found as
        properties of modules which are properties of this module (and so on).

        >>> a = tf.Module()
        >>> b = tf.Module()
        >>> c = tf.Module()
        >>> a.b = b
        >>> b.c = c
        >>> list(a.submodules) == [b, c]
        True
        >>> list(b.submodules) == [c]
        True
        >>> list(c.submodules) == []
        True

        Returns:
          A sequence of all submodules.
        """
        ...
    @classmethod
    def with_name_scope(cls, method: Callable[_P, _R]) -> Callable[_P, _R]:
        """
        Decorator to automatically enter the module name scope.

        >>> class MyModule(tf.Module):
        ...   @tf.Module.with_name_scope
        ...   def __call__(self, x):
        ...     if not hasattr(self, 'w'):
        ...       self.w = tf.Variable(tf.random.normal([x.shape[1], 3]))
        ...     return tf.matmul(x, self.w)

        Using the above module would produce `tf.Variable`s and `tf.Tensor`s whose
        names included the module name:

        >>> mod = MyModule()
        >>> mod(tf.ones([1, 2]))
        <tf.Tensor: shape=(1, 3), dtype=float32, numpy=..., dtype=float32)>
        >>> mod.w
        <tf.Variable 'my_module/Variable:0' shape=(2, 3) dtype=float32,
        numpy=..., dtype=float32)>

        Args:
          method: The method to wrap.

        Returns:
          The original method wrapped such that it enters the module's name scope.
        """
        ...

class UnconnectedGradients(Enum):
    """
    Controls how gradient computation behaves when y does not depend on x.

    The gradient of y with respect to x can be zero in two different ways: there
    could be no differentiable path in the graph connecting x to y (and so we can
    statically prove that the gradient is zero) or it could be that runtime values
    of tensors in a particular execution lead to a gradient of zero (say, if a
    relu unit happens to not be activated). To allow you to distinguish between
    these two cases you can choose what value gets returned for the gradient when
    there is no path in the graph from x to y:

    * `NONE`: Indicates that [None] will be returned if there is no path from x
      to y
    * `ZERO`: Indicates that a zero tensor will be returned in the shape of x.
    """
    NONE = "none"
    ZERO = "zero"

_SpecProto = TypeVar("_SpecProto", bound=Message)

class TypeSpec(ABC, Generic[_SpecProto]):
    """
    Specifies a TensorFlow value type.

    A `tf.TypeSpec` provides metadata describing an object accepted or returned
    by TensorFlow APIs.  Concrete subclasses, such as `tf.TensorSpec` and
    `tf.RaggedTensorSpec`, are used to describe different value types.

    For example, `tf.function`'s `input_signature` argument accepts a list
    (or nested structure) of `TypeSpec`s.

    Creating new subclasses of `TypeSpec` (outside of TensorFlow core) is not
    currently supported.  In particular, we may make breaking changes to the
    private methods and properties defined by this base class.

    Example:

    >>> spec = tf.TensorSpec(shape=[None, None], dtype=tf.int32)
    >>> @tf.function(input_signature=[spec])
    ... def double(x):
    ...   return x * 2
    >>> double(tf.constant([[1, 2], [3, 4]]))
    <tf.Tensor: shape=(2, 2), dtype=int32,
        numpy=array([[2, 4], [6, 8]], dtype=int32)>
    """
    __slots__ = ["_cached_cmp_key"]
    @property
    @abstractmethod
    def value_type(self) -> Any:
        """
        The Python type for values that are compatible with this TypeSpec.

        In particular, all values that are compatible with this TypeSpec must be an
        instance of this type.
        """
        ...
    def experimental_as_proto(self) -> _SpecProto:
        """
        Returns a proto representation of the TypeSpec instance.

        Do NOT override for custom non-TF types.
        """
        ...
    @classmethod
    def experimental_from_proto(cls, proto: _SpecProto) -> Self:
        """
        Returns a TypeSpec instance based on the serialized proto.

        Do NOT override for custom non-TF types.

        Args:
          proto: Proto generated using 'experimental_as_proto'.
        """
        ...
    @classmethod
    def experimental_type_proto(cls) -> type[_SpecProto]:
        """
        Returns the type of proto associated with TypeSpec serialization.

        Do NOT override for custom non-TF types.
        """
        ...
    def is_compatible_with(self, spec_or_value: Self | TensorCompatible | SparseTensor | RaggedTensor) -> _bool:
        """
        Returns true if `spec_or_value` is compatible with this TypeSpec.

        Prefer using "is_subtype_of" and "most_specific_common_supertype" wherever
        possible.

        Args:
          spec_or_value: A TypeSpec or TypeSpec associated value to compare against.
        """
        ...
    # Incomplete as tf.types is not yet covered.
    def is_subtype_of(self, other) -> _bool:
        """
        Returns True if `self` is a subtype of `other`.

        Implements the tf.types.experimental.func.TraceType interface.

        If not overridden by a subclass, the default behavior is to assume the
        TypeSpec is covariant upon attributes that implement TraceType and
        invariant upon rest of the attributes as well as the structure and type
        of the TypeSpec.

        Args:
          other: A TraceType object.
        """
        ...
    def most_specific_common_supertype(self, others: Sequence[Incomplete]) -> Self | None:
        """
        Returns the most specific supertype TypeSpec  of `self` and `others`.

        Implements the tf.types.experimental.func.TraceType interface.

        If not overridden by a subclass, the default behavior is to assume the
        TypeSpec is covariant upon attributes that implement TraceType and
        invariant upon rest of the attributes as well as the structure and type
        of the TypeSpec.

        Args:
          others: A sequence of TraceTypes.
        """
        ...
    def most_specific_compatible_type(self, other: Self) -> Self:
        """
        Returns the most specific TypeSpec compatible with `self` and `other`. (deprecated)

        Deprecated: THIS FUNCTION IS DEPRECATED. It will be removed in a future version.
        Instructions for updating:
        Use most_specific_common_supertype instead.

        Deprecated. Please use `most_specific_common_supertype` instead.
        Do not override this function.

        Args:
          other: A `TypeSpec`.

        Raises:
          ValueError: If there is no TypeSpec that is compatible with both `self`
            and `other`.
        """
        ...

class TensorSpec(TypeSpec[struct_pb2.TensorSpecProto]):
    """
    Describes the type of a tf.Tensor.

    >>> t = tf.constant([[1,2,3],[4,5,6]])
    >>> tf.TensorSpec.from_tensor(t)
    TensorSpec(shape=(2, 3), dtype=tf.int32, name=None)

    Contains metadata for describing the nature of `tf.Tensor` objects
    accepted or returned by some TensorFlow APIs.

    For example, it can be used to constrain the type of inputs accepted by
    a tf.function:

    >>> @tf.function(input_signature=[tf.TensorSpec([1, None])])
    ... def constrained_foo(t):
    ...   print("tracing...")
    ...   return t

    Now the `tf.function` is able to assume that `t` is always of the type
    `tf.TensorSpec([1, None])` which will avoid retracing as well as enforce the
    type restriction on inputs.

    As a result, the following call with tensor of type `tf.TensorSpec([1, 2])`
    triggers a trace and succeeds:
    >>> constrained_foo(tf.constant([[1., 2]])).numpy()
    tracing...
    array([[1., 2.]], dtype=float32)

    The following subsequent call with tensor of type `tf.TensorSpec([1, 4])`
    does not trigger a trace and succeeds:
    >>> constrained_foo(tf.constant([[1., 2, 3, 4]])).numpy()
    array([[1., 2., 3., 4.], dtype=float32)

    But the following call with tensor of type `tf.TensorSpec([2, 2])` fails:
    >>> constrained_foo(tf.constant([[1., 2], [3, 4]])).numpy()
    Traceback (most recent call last):
    ...
    TypeError: Binding inputs to tf.function `constrained_foo` failed ...
    """
    __slots__: list[str] = []
    def __init__(self, shape: ShapeLike, dtype: DTypeLike = ..., name: str | None = None) -> None:
        """
        Creates a TensorSpec.

        Args:
          shape: Value convertible to `tf.TensorShape`. The shape of the tensor.
          dtype: Value convertible to `tf.DType`. The type of the tensor values.
          name: Optional name for the Tensor.

        Raises:
          TypeError: If shape is not convertible to a `tf.TensorShape`, or dtype is
            not convertible to a `tf.DType`.
        """
        ...
    @property
    def value_type(self) -> Tensor:
        """The Python type for values that are compatible with this TypeSpec."""
        ...
    @property
    def shape(self) -> TensorShape:
        """Returns the `TensorShape` that represents the shape of the tensor."""
        ...
    @property
    def dtype(self) -> DType:
        """Returns the `dtype` of elements in the tensor."""
        ...
    @property
    def name(self) -> str | None:
        """Returns the (optionally provided) name of the described tensor."""
        ...
    @classmethod
    def from_spec(cls, spec: TypeSpec[Any], name: str | None = None) -> Self:
        """
        Returns a `TensorSpec` with the same shape and dtype as `spec`.

        >>> spec = tf.TensorSpec(shape=[8, 3], dtype=tf.int32, name="OriginalName")
        >>> tf.TensorSpec.from_spec(spec, "NewName")
        TensorSpec(shape=(8, 3), dtype=tf.int32, name='NewName')

        Args:
          spec: The `TypeSpec` used to create the new `TensorSpec`.
          name: The name for the new `TensorSpec`.  Defaults to `spec.name`.
        """
        ...
    @classmethod
    def from_tensor(cls, tensor: Tensor, name: str | None = None) -> Self:
        """
        Returns a `TensorSpec` that describes `tensor`.

        >>> tf.TensorSpec.from_tensor(tf.constant([1, 2, 3]))
        TensorSpec(shape=(3,), dtype=tf.int32, name=None)

        Args:
          tensor: The `tf.Tensor` that should be described.
          name: A name for the `TensorSpec`.  Defaults to `tensor.op.name`.

        Returns:
          A `TensorSpec` that describes `tensor`.
        """
        ...
    def is_compatible_with(self, spec_or_tensor: Self | TensorCompatible) -> _bool:
        """
        Returns True if spec_or_tensor is compatible with this TensorSpec.

        Two tensors are considered compatible if they have the same dtype
        and their shapes are compatible (see `tf.TensorShape.is_compatible_with`).

        Args:
          spec_or_tensor: A tf.TensorSpec or a tf.Tensor

        Returns:
          True if spec_or_tensor is compatible with self.
        """
        ...

class SparseTensorSpec(TypeSpec[struct_pb2.TypeSpecProto]):
    """Type specification for a `tf.sparse.SparseTensor`."""
    __slots__ = ["_shape", "_dtype"]
    def __init__(self, shape: ShapeLike | None = None, dtype: DTypeLike = ...) -> None:
        """
        Constructs a type specification for a `tf.sparse.SparseTensor`.

        Args:
          shape: The dense shape of the `SparseTensor`, or `None` to allow any dense
            shape.
          dtype: `tf.DType` of values in the `SparseTensor`.
        """
        ...
    @property
    def value_type(self) -> SparseTensor: ...
    @property
    def shape(self) -> TensorShape:
        """The `tf.TensorShape` specified by this type for the SparseTensor."""
        ...
    @property
    def dtype(self) -> DType:
        """The `tf.dtypes.DType` specified by this type for the SparseTensor."""
        ...
    @classmethod
    def from_value(cls, value: SparseTensor) -> Self: ...

class RaggedTensorSpec(TypeSpec[struct_pb2.TypeSpecProto]):
    """Type specification for a `tf.RaggedTensor`."""
    __slots__ = ["_shape", "_dtype", "_ragged_rank", "_row_splits_dtype", "_flat_values_spec"]
    def __init__(
        self,
        shape: ShapeLike | None = None,
        dtype: DTypeLike = ...,
        ragged_rank: int | None = None,
        row_splits_dtype: DTypeLike = ...,
        flat_values_spec: TypeSpec[Any] | None = None,
    ) -> None:
        """
        Constructs a type specification for a `tf.RaggedTensor`.

        Args:
          shape: The shape of the RaggedTensor, or `None` to allow any shape.  If a
            shape is specified, then all ragged dimensions must have size `None`.
          dtype: `tf.DType` of values in the RaggedTensor.
          ragged_rank: Python integer, the number of times the RaggedTensor's
            flat_values is partitioned.  Defaults to `shape.ndims - 1`.
          row_splits_dtype: `dtype` for the RaggedTensor's `row_splits` tensor. One
            of `tf.int32` or `tf.int64`.
          flat_values_spec: TypeSpec for flat_value of the RaggedTensor. It shall be
            provided when the flat_values is a CompositeTensor rather then Tensor.
            If both `dtype` and `flat_values_spec` and  are provided, `dtype` must
            be the same as `flat_values_spec.dtype`. (experimental)
        """
        ...
    @property
    def value_type(self) -> RaggedTensor: ...
    @property
    def shape(self) -> TensorShape:
        """
        The statically known shape of the RaggedTensor.

        Examples:

        >>> rt = tf.ragged.constant([[0], [1, 2]])
        >>> tf.type_spec_from_value(rt).shape
        TensorShape([2, None])

        >>> rt = tf.ragged.constant([[[0, 1]], [[1, 2], [3, 4]]], ragged_rank=1)
        >>> tf.type_spec_from_value(rt).shape
        TensorShape([2, None, 2])

        Returns:
          A `tf.TensorShape` containing the statically known shape of the
          RaggedTensor. Ragged dimensions have a size of `None`.
        """
        ...
    @property
    def dtype(self) -> DType:
        """
        The `tf.dtypes.DType` specified by this type for the RaggedTensor.

        Examples:

        >>> rt = tf.ragged.constant([["a"], ["b", "c"]], dtype=tf.string)
        >>> tf.type_spec_from_value(rt).dtype
        tf.string

        Returns:
          A `tf.dtypes.DType` of the values in the RaggedTensor.
        """
        ...
    @classmethod
    def from_value(cls, value: RaggedTensor) -> Self: ...

def convert_to_tensor(
    value: TensorCompatible | IndexedSlices,
    dtype: DTypeLike | None = None,
    dtype_hint: DTypeLike | None = None,
    name: str | None = None,
) -> Tensor:
    """
    Converts the given `value` to a `Tensor`.

    This function converts Python objects of various types to `Tensor`
    objects. It accepts `Tensor` objects, numpy arrays, Python lists,
    and Python scalars.

    For example:

    >>> import numpy as np
    >>> def my_func(arg):
    ...   arg = tf.convert_to_tensor(arg, dtype=tf.float32)
    ...   return arg

    >>> # The following calls are equivalent.
    ...
    >>> value_1 = my_func(tf.constant([[1.0, 2.0], [3.0, 4.0]]))
    >>> print(value_1)
    tf.Tensor(
      [[1. 2.]
       [3. 4.]], shape=(2, 2), dtype=float32)
    >>> value_2 = my_func([[1.0, 2.0], [3.0, 4.0]])
    >>> print(value_2)
    tf.Tensor(
      [[1. 2.]
       [3. 4.]], shape=(2, 2), dtype=float32)
    >>> value_3 = my_func(np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32))
    >>> print(value_3)
    tf.Tensor(
      [[1. 2.]
       [3. 4.]], shape=(2, 2), dtype=float32)

    This function can be useful when composing a new operation in Python
    (such as `my_func` in the example above). All standard Python op
    constructors apply this function to each of their Tensor-valued
    inputs, which allows those ops to accept numpy arrays, Python lists,
    and scalars in addition to `Tensor` objects.

    Note: This function diverges from default Numpy behavior for `float` and
      `string` types when `None` is present in a Python list or scalar. Rather
      than silently converting `None` values, an error will be thrown.

    Args:
      value: An object whose type has a registered `Tensor` conversion function.
      dtype: Optional element type for the returned tensor. If missing, the type
        is inferred from the type of `value`.
      dtype_hint: Optional element type for the returned tensor, used when dtype
        is None. In some cases, a caller may not have a dtype in mind when
        converting to a tensor, so dtype_hint can be used as a soft preference. If
        the conversion to `dtype_hint` is not possible, this argument has no
        effect.
      name: Optional name to use if a new `Tensor` is created.

    Returns:
      A `Tensor` based on `value`.

    Raises:
      TypeError: If no conversion function is registered for `value` to `dtype`.
      RuntimeError: If a registered conversion function returns an invalid value.
      ValueError: If the `value` is a tensor not of given `dtype` in graph mode.
    """
    ...
@overload
def expand_dims(input: TensorCompatible, axis: int, name: str | None = None) -> Tensor:
    """
    Returns a tensor with a length 1 axis inserted at index `axis`.

    Given a tensor `input`, this operation inserts a dimension of length 1 at the
    dimension index `axis` of `input`'s shape. The dimension index follows Python
    indexing rules: It's zero-based, and a negative index is counted backward
    from the end.

    This operation is useful to:

    * Add an outer "batch" dimension to a single element.
    * Align axes for broadcasting.
    * To add an inner vector length axis to a tensor of scalars.

    For example:

    If you have a single image of shape `[height, width, channels]`:

    >>> image = tf.zeros([10,10,3])

    You can add an outer `batch` axis by passing `axis=0`:

    >>> tf.expand_dims(image, axis=0).shape.as_list()
    [1, 10, 10, 3]

    The new axis location matches Python `list.insert(axis, 1)`:

    >>> tf.expand_dims(image, axis=1).shape.as_list()
    [10, 1, 10, 3]

    Following standard Python indexing rules, a negative `axis` counts from the
    end so `axis=-1` adds an inner most dimension:

    >>> tf.expand_dims(image, -1).shape.as_list()
    [10, 10, 3, 1]

    This operation requires that `axis` is a valid index for `input.shape`,
    following Python indexing rules:

    ```
    -1-tf.rank(input) <= axis <= tf.rank(input)
    ```

    This operation is related to:

    * `tf.squeeze`, which removes dimensions of size 1.
    * `tf.reshape`, which provides more flexible reshaping capability.
    * `tf.sparse.expand_dims`, which provides this functionality for
      `tf.SparseTensor`

    Args:
      input: A `Tensor`.
      axis: Integer specifying the dimension index at which to expand the
        shape of `input`. Given an input of D dimensions, `axis` must be in range
        `[-(D+1), D]` (inclusive).
      name: Optional string. The name of the output `Tensor`.

    Returns:
      A tensor with the same data as `input`, with an additional dimension
      inserted at the index specified by `axis`.

    Raises:
      TypeError: If `axis` is not specified.
      InvalidArgumentError: If `axis` is out of range `[-(D+1), D]`.
    """
    ...
@overload
def expand_dims(input: RaggedTensor, axis: int, name: str | None = None) -> RaggedTensor:
    """
    Returns a tensor with a length 1 axis inserted at index `axis`.

    Given a tensor `input`, this operation inserts a dimension of length 1 at the
    dimension index `axis` of `input`'s shape. The dimension index follows Python
    indexing rules: It's zero-based, and a negative index is counted backward
    from the end.

    This operation is useful to:

    * Add an outer "batch" dimension to a single element.
    * Align axes for broadcasting.
    * To add an inner vector length axis to a tensor of scalars.

    For example:

    If you have a single image of shape `[height, width, channels]`:

    >>> image = tf.zeros([10,10,3])

    You can add an outer `batch` axis by passing `axis=0`:

    >>> tf.expand_dims(image, axis=0).shape.as_list()
    [1, 10, 10, 3]

    The new axis location matches Python `list.insert(axis, 1)`:

    >>> tf.expand_dims(image, axis=1).shape.as_list()
    [10, 1, 10, 3]

    Following standard Python indexing rules, a negative `axis` counts from the
    end so `axis=-1` adds an inner most dimension:

    >>> tf.expand_dims(image, -1).shape.as_list()
    [10, 10, 3, 1]

    This operation requires that `axis` is a valid index for `input.shape`,
    following Python indexing rules:

    ```
    -1-tf.rank(input) <= axis <= tf.rank(input)
    ```

    This operation is related to:

    * `tf.squeeze`, which removes dimensions of size 1.
    * `tf.reshape`, which provides more flexible reshaping capability.
    * `tf.sparse.expand_dims`, which provides this functionality for
      `tf.SparseTensor`

    Args:
      input: A `Tensor`.
      axis: Integer specifying the dimension index at which to expand the
        shape of `input`. Given an input of D dimensions, `axis` must be in range
        `[-(D+1), D]` (inclusive).
      name: Optional string. The name of the output `Tensor`.

    Returns:
      A tensor with the same data as `input`, with an additional dimension
      inserted at the index specified by `axis`.

    Raises:
      TypeError: If `axis` is not specified.
      InvalidArgumentError: If `axis` is out of range `[-(D+1), D]`.
    """
    ...
@overload
def concat(values: TensorCompatible, axis: int, name: str | None = "concat") -> Tensor:
    """
    Concatenates tensors along one dimension.

    See also `tf.tile`, `tf.stack`, `tf.repeat`.

    Concatenates the list of tensors `values` along dimension `axis`.  If
    `values[i].shape = [D0, D1, ... Daxis(i), ...Dn]`, the concatenated
    result has shape

        [D0, D1, ... Raxis, ...Dn]

    where

        Raxis = sum(Daxis(i))

    That is, the data from the input tensors is joined along the `axis`
    dimension.

    The number of dimensions of the input tensors must match, and all dimensions
    except the `axis` must be equal.

    For example:

    >>> t1 = [[1, 2, 3], [4, 5, 6]]
    >>> t2 = [[7, 8, 9], [10, 11, 12]]
    >>> tf.concat([t1, t2], 0)
    <tf.Tensor: shape=(4, 3), dtype=int32, numpy=
    array([[ 1,  2,  3],
           [ 4,  5,  6],
           [ 7,  8,  9],
           [10, 11, 12]], dtype=int32)>

    >>> tf.concat([t1, t2], 1)
    <tf.Tensor: shape=(2, 6), dtype=int32, numpy=
    array([[ 1,  2,  3,  7,  8,  9],
           [ 4,  5,  6, 10, 11, 12]], dtype=int32)>

    As in Python, the `axis` could also be negative numbers. Negative `axis`
    are interpreted as counting from the end of the rank, i.e.,
     `axis + rank(values)`-th dimension.

    For example:

    >>> t1 = [[[1, 2], [2, 3]], [[4, 4], [5, 3]]]
    >>> t2 = [[[7, 4], [8, 4]], [[2, 10], [15, 11]]]
    >>> tf.concat([t1, t2], -1)
    <tf.Tensor: shape=(2, 2, 4), dtype=int32, numpy=
      array([[[ 1,  2,  7,  4],
              [ 2,  3,  8,  4]],
             [[ 4,  4,  2, 10],
              [ 5,  3, 15, 11]]], dtype=int32)>

    Note: If you are concatenating along a new axis consider using stack.
    E.g.

    ```python
    tf.concat([tf.expand_dims(t, axis) for t in tensors], axis)
    ```

    can be rewritten as

    ```python
    tf.stack(tensors, axis=axis)
    ```

    Args:
      values: A list of `Tensor` objects or a single `Tensor`.
      axis: 0-D `int32` `Tensor`.  Dimension along which to concatenate. Must be
        in the range `[-rank(values), rank(values))`. As in Python, indexing for
        axis is 0-based. Positive axis in the rage of `[0, rank(values))` refers
        to `axis`-th dimension. And negative axis refers to `axis +
        rank(values)`-th dimension.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` resulting from concatenation of the input tensors.
    """
    ...
@overload
def concat(values: Sequence[RaggedTensor], axis: int, name: str | None = "concat") -> RaggedTensor:
    """
    Concatenates tensors along one dimension.

    See also `tf.tile`, `tf.stack`, `tf.repeat`.

    Concatenates the list of tensors `values` along dimension `axis`.  If
    `values[i].shape = [D0, D1, ... Daxis(i), ...Dn]`, the concatenated
    result has shape

        [D0, D1, ... Raxis, ...Dn]

    where

        Raxis = sum(Daxis(i))

    That is, the data from the input tensors is joined along the `axis`
    dimension.

    The number of dimensions of the input tensors must match, and all dimensions
    except the `axis` must be equal.

    For example:

    >>> t1 = [[1, 2, 3], [4, 5, 6]]
    >>> t2 = [[7, 8, 9], [10, 11, 12]]
    >>> tf.concat([t1, t2], 0)
    <tf.Tensor: shape=(4, 3), dtype=int32, numpy=
    array([[ 1,  2,  3],
           [ 4,  5,  6],
           [ 7,  8,  9],
           [10, 11, 12]], dtype=int32)>

    >>> tf.concat([t1, t2], 1)
    <tf.Tensor: shape=(2, 6), dtype=int32, numpy=
    array([[ 1,  2,  3,  7,  8,  9],
           [ 4,  5,  6, 10, 11, 12]], dtype=int32)>

    As in Python, the `axis` could also be negative numbers. Negative `axis`
    are interpreted as counting from the end of the rank, i.e.,
     `axis + rank(values)`-th dimension.

    For example:

    >>> t1 = [[[1, 2], [2, 3]], [[4, 4], [5, 3]]]
    >>> t2 = [[[7, 4], [8, 4]], [[2, 10], [15, 11]]]
    >>> tf.concat([t1, t2], -1)
    <tf.Tensor: shape=(2, 2, 4), dtype=int32, numpy=
      array([[[ 1,  2,  7,  4],
              [ 2,  3,  8,  4]],
             [[ 4,  4,  2, 10],
              [ 5,  3, 15, 11]]], dtype=int32)>

    Note: If you are concatenating along a new axis consider using stack.
    E.g.

    ```python
    tf.concat([tf.expand_dims(t, axis) for t in tensors], axis)
    ```

    can be rewritten as

    ```python
    tf.stack(tensors, axis=axis)
    ```

    Args:
      values: A list of `Tensor` objects or a single `Tensor`.
      axis: 0-D `int32` `Tensor`.  Dimension along which to concatenate. Must be
        in the range `[-rank(values), rank(values))`. As in Python, indexing for
        axis is 0-based. Positive axis in the rage of `[0, rank(values))` refers
        to `axis`-th dimension. And negative axis refers to `axis +
        rank(values)`-th dimension.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` resulting from concatenation of the input tensors.
    """
    ...
@overload
def squeeze(
    input: TensorCompatible, axis: int | tuple[int, ...] | list[int] | None = None, name: str | None = None
) -> Tensor:
    """
    Removes dimensions of size 1 from the shape of a tensor.

    Given a tensor `input`, this operation returns a tensor of the same type with
    all dimensions of size 1 removed. If you don't want to remove all size 1
    dimensions, you can remove specific size 1 dimensions by specifying
    `axis`.

    For example:

    ```python
    # 't' is a tensor of shape [1, 2, 1, 3, 1, 1]
    tf.shape(tf.squeeze(t))  # [2, 3]
    ```

    Or, to remove specific size 1 dimensions:

    ```python
    # 't' is a tensor of shape [1, 2, 1, 3, 1, 1]
    tf.shape(tf.squeeze(t, [2, 4]))  # [1, 2, 3, 1]
    ```

    Unlike the older op `tf.compat.v1.squeeze`, this op does not accept a
    deprecated `squeeze_dims` argument.

    Note: if `input` is a `tf.RaggedTensor`, then this operation takes `O(N)`
    time, where `N` is the number of elements in the squeezed dimensions.

    Note: If squeeze is performed on dimensions of unknown sizes, then the
    returned Tensor will be of unknown shape. A common situation is when the
    first (batch) dimension is of size `None`, `tf.squeeze` returns
    `<unknown>` shape which may be a surprise. Specify the `axis=` argument
    to get the expected result, as illustrated in the following example:

    ```python
    @tf.function
    def func(x):
      print('x.shape:', x.shape)
      known_axes = [i for i, size in enumerate(x.shape) if size == 1]
      y = tf.squeeze(x, axis=known_axes)
      print('shape of tf.squeeze(x, axis=known_axes):', y.shape)
      y = tf.squeeze(x)
      print('shape of tf.squeeze(x):', y.shape)
      return 0

    _ = func.get_concrete_function(tf.TensorSpec([None, 1, 2], dtype=tf.int32))
    # Output is.
    # x.shape: (None, 1, 2)
    # shape of tf.squeeze(x, axis=known_axes): (None, 2)
    # shape of tf.squeeze(x): <unknown>
    ```

    Args:
      input: A `Tensor`. The `input` to squeeze.
      axis: An optional list of `ints`. Defaults to `[]`. If specified, only
        squeezes the dimensions listed. The dimension index starts at 0. It is an
        error to squeeze a dimension that is not 1. Must be in the range
        `[-rank(input), rank(input))`. Must be specified if `input` is a
        `RaggedTensor`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `input`.
      Contains the same data as `input`, but has one or more dimensions of
      size 1 removed.

    Raises:
      ValueError: The input cannot be converted to a tensor, or the specified
        axis cannot be squeezed.
    """
    ...
@overload
def squeeze(input: RaggedTensor, axis: int | tuple[int, ...] | list[int], name: str | None = None) -> RaggedTensor:
    """
    Removes dimensions of size 1 from the shape of a tensor.

    Given a tensor `input`, this operation returns a tensor of the same type with
    all dimensions of size 1 removed. If you don't want to remove all size 1
    dimensions, you can remove specific size 1 dimensions by specifying
    `axis`.

    For example:

    ```python
    # 't' is a tensor of shape [1, 2, 1, 3, 1, 1]
    tf.shape(tf.squeeze(t))  # [2, 3]
    ```

    Or, to remove specific size 1 dimensions:

    ```python
    # 't' is a tensor of shape [1, 2, 1, 3, 1, 1]
    tf.shape(tf.squeeze(t, [2, 4]))  # [1, 2, 3, 1]
    ```

    Unlike the older op `tf.compat.v1.squeeze`, this op does not accept a
    deprecated `squeeze_dims` argument.

    Note: if `input` is a `tf.RaggedTensor`, then this operation takes `O(N)`
    time, where `N` is the number of elements in the squeezed dimensions.

    Note: If squeeze is performed on dimensions of unknown sizes, then the
    returned Tensor will be of unknown shape. A common situation is when the
    first (batch) dimension is of size `None`, `tf.squeeze` returns
    `<unknown>` shape which may be a surprise. Specify the `axis=` argument
    to get the expected result, as illustrated in the following example:

    ```python
    @tf.function
    def func(x):
      print('x.shape:', x.shape)
      known_axes = [i for i, size in enumerate(x.shape) if size == 1]
      y = tf.squeeze(x, axis=known_axes)
      print('shape of tf.squeeze(x, axis=known_axes):', y.shape)
      y = tf.squeeze(x)
      print('shape of tf.squeeze(x):', y.shape)
      return 0

    _ = func.get_concrete_function(tf.TensorSpec([None, 1, 2], dtype=tf.int32))
    # Output is.
    # x.shape: (None, 1, 2)
    # shape of tf.squeeze(x, axis=known_axes): (None, 2)
    # shape of tf.squeeze(x): <unknown>
    ```

    Args:
      input: A `Tensor`. The `input` to squeeze.
      axis: An optional list of `ints`. Defaults to `[]`. If specified, only
        squeezes the dimensions listed. The dimension index starts at 0. It is an
        error to squeeze a dimension that is not 1. Must be in the range
        `[-rank(input), rank(input))`. Must be specified if `input` is a
        `RaggedTensor`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `input`.
      Contains the same data as `input`, but has one or more dimensions of
      size 1 removed.

    Raises:
      ValueError: The input cannot be converted to a tensor, or the specified
        axis cannot be squeezed.
    """
    ...
def split(
    value: TensorCompatible,
    num_or_size_splits: int | TensorCompatible,
    axis: int | Tensor = 0,
    num: int | None = None,
    name: str | None = "split",
) -> list[Tensor]:
    """
    Splits a tensor `value` into a list of sub tensors.

    See also `tf.unstack`.

    If `num_or_size_splits` is an `int`,  then it splits `value` along the
    dimension `axis` into `num_or_size_splits` smaller tensors. This requires that
    `value.shape[axis]` is divisible by `num_or_size_splits`.

    If `num_or_size_splits` is a 1-D Tensor (or list), then `value` is split into
    `len(num_or_size_splits)` elements. The shape of the `i`-th
    element has the same size as the `value` except along dimension `axis` where
    the size is `num_or_size_splits[i]`.

    For example:

    >>> x = tf.Variable(tf.random.uniform([5, 30], -1, 1))
    >>>
    >>> # Split `x` into 3 tensors along dimension 1
    >>> s0, s1, s2 = tf.split(x, num_or_size_splits=3, axis=1)
    >>> tf.shape(s0).numpy()
    array([ 5, 10], dtype=int32)
    >>>
    >>> # Split `x` into 3 tensors with sizes [4, 15, 11] along dimension 1
    >>> split0, split1, split2 = tf.split(x, [4, 15, 11], 1)
    >>> tf.shape(split0).numpy()
    array([5, 4], dtype=int32)
    >>> tf.shape(split1).numpy()
    array([ 5, 15], dtype=int32)
    >>> tf.shape(split2).numpy()
    array([ 5, 11], dtype=int32)

    Args:
      value: The `Tensor` to split.
      num_or_size_splits: Either an `int` indicating the number of splits
        along `axis` or a 1-D integer `Tensor` or Python list containing the sizes
        of each output tensor along `axis`. If an `int`, then it must evenly
        divide `value.shape[axis]`; otherwise the sum of sizes along the split
        axis must match that of the `value`.
      axis: An `int` or scalar `int32` `Tensor`. The dimension along which
        to split. Must be in the range `[-rank(value), rank(value))`. Defaults to
        0.
      num: Optional, an `int`, used to specify the number of outputs when it
        cannot be inferred from the shape of `size_splits`.
      name: A name for the operation (optional).

    Returns:
      if `num_or_size_splits` is an `int` returns a list of
      `num_or_size_splits` `Tensor` objects; if `num_or_size_splits` is a 1-D
      list or 1-D `Tensor` returns `num_or_size_splits.get_shape[0]`
      `Tensor` objects resulting from splitting `value`.

    Raises:
      ValueError: If `num` is unspecified and cannot be inferred.
      ValueError: If `num_or_size_splits` is a scalar `Tensor`.
    """
    ...
def tensor_scatter_nd_update(
    tensor: TensorCompatible, indices: TensorCompatible, updates: TensorCompatible, name: str | None = None
) -> Tensor:
    """
    Scatter `updates` into an existing tensor according to `indices`.

    This operation creates a new tensor by applying sparse `updates` to the
    input `tensor`. This is similar to an index assignment.

    ```
    # Not implemented: tensors cannot be updated inplace.
    tensor[indices] = updates
    ```

    If an out of bound index is found on CPU, an error is returned.

    > **WARNING**: There are some GPU specific semantics for this operation.
    >
    > - If an out of bound index is found, the index is ignored.
    > - The order in which updates are applied is nondeterministic, so the output
    >   will be nondeterministic if `indices` contains duplicates.

    This operation is very similar to `tf.scatter_nd`, except that the updates are
    scattered onto an existing tensor (as opposed to a zero-tensor). If the memory
    for the existing tensor cannot be re-used, a copy is made and updated.

    In general:

    * `indices` is an integer tensor - the indices to update in `tensor`.
    * `indices` has **at least two** axes, the last axis is the depth of the
      index vectors.
    * For each index vector in `indices` there is a corresponding entry in
      `updates`.
    * If the length of the index vectors matches the rank of the `tensor`, then
      the index vectors each point to scalars in `tensor` and each update is a
      scalar.
    * If the length of the index vectors is less than the rank of `tensor`, then
      the index vectors each point to the slices of `tensor` and shape of the updates
      must match that slice.

    Overall this leads to the following shape constraints:

    ```
    assert tf.rank(indices) >= 2
    index_depth = indices.shape[-1]
    batch_shape = indices.shape[:-1]
    assert index_depth <= tf.rank(tensor)
    outer_shape = tensor.shape[:index_depth]
    inner_shape = tensor.shape[index_depth:]
    assert updates.shape == batch_shape + inner_shape
    ```

    Typical usage is often much simpler than this general form, and it
    can be better understood starting with simple examples:

    ### Scalar updates

    The simplest usage inserts scalar elements into a tensor by index.
    In this case, the `index_depth` must equal the rank of the
    input `tensor`, slice each column of `indices` is an index into an axis of the
    input `tensor`.

    In this simplest case the shape constraints are:

    ```
    num_updates, index_depth = indices.shape.as_list()
    assert updates.shape == [num_updates]
    assert index_depth == tf.rank(tensor)`
    ```

    For example, to insert 4 scattered elements in a rank-1 tensor with
    8 elements.

    <div style="width:70%; margin:auto; margin-bottom:10px; margin-top:20px;">
    <img style="width:100%"
      src="https://www.tensorflow.org/images/ScatterNd1.png">
    </div>

    This scatter operation would look like this:

    >>> tensor = [0, 0, 0, 0, 0, 0, 0, 0]    # tf.rank(tensor) == 1
    >>> indices = [[1], [3], [4], [7]]       # num_updates == 4, index_depth == 1
    >>> updates = [9, 10, 11, 12]            # num_updates == 4
    >>> print(tf.tensor_scatter_nd_update(tensor, indices, updates))
    tf.Tensor([ 0 9  0 10  11  0  0 12], shape=(8,), dtype=int32)

    The length (first axis) of `updates` must equal the length of the `indices`:
    `num_updates`. This is the number of updates being inserted. Each scalar
    update is inserted into `tensor` at the indexed location.

    For a higher rank input `tensor` scalar updates can be inserted by using an
    `index_depth` that matches `tf.rank(tensor)`:

    >>> tensor = [[1, 1], [1, 1], [1, 1]]    # tf.rank(tensor) == 2
    >>> indices = [[0, 1], [2, 0]]           # num_updates == 2, index_depth == 2
    >>> updates = [5, 10]                    # num_updates == 2
    >>> print(tf.tensor_scatter_nd_update(tensor, indices, updates))
    tf.Tensor(
        [[ 1  5]
         [ 1  1]
         [10  1]], shape=(3, 2), dtype=int32)

    ### Slice updates

    When the input `tensor` has more than one axis scatter can be used to update
    entire slices.

    In this case it's helpful to think of the input `tensor` as being a two level
    array-of-arrays. The shape of this two level array is split into the
    `outer_shape` and the `inner_shape`.

    `indices` indexes into the outer level of the input tensor (`outer_shape`).
    and replaces the sub-array at that location with the corresponding item from
    the `updates` list. The shape of each update is `inner_shape`.

    When updating a list of slices the shape constraints are:

    ```
    num_updates, index_depth = indices.shape.as_list()
    outer_shape = tensor.shape[:index_depth]
    inner_shape = tensor.shape[index_depth:]
    assert updates.shape == [num_updates, inner_shape]
    ```

    For example, to update rows of a `(6, 3)` `tensor`:

    >>> tensor = tf.zeros([6, 3], dtype=tf.int32)

    Use an index depth of one.

    >>> indices = tf.constant([[2], [4]])     # num_updates == 2, index_depth == 1
    >>> num_updates, index_depth = indices.shape.as_list()

    The `outer_shape` is `6`, the inner shape is `3`:

    >>> outer_shape = tensor.shape[:index_depth]
    >>> inner_shape = tensor.shape[index_depth:]

    2 rows are being indexed so 2 `updates` must be supplied.
    Each update must be shaped to match the `inner_shape`.

    >>> # num_updates == 2, inner_shape==3
    >>> updates = tf.constant([[1, 2, 3],
    ...                        [4, 5, 6]])

    Altogether this gives:

    >>> tf.tensor_scatter_nd_update(tensor, indices, updates).numpy()
    array([[0, 0, 0],
           [0, 0, 0],
           [1, 2, 3],
           [0, 0, 0],
           [4, 5, 6],
           [0, 0, 0]], dtype=int32)

    #### More slice update examples

    A tensor representing a batch of uniformly sized video clips naturally has 5
    axes: `[batch_size, time, width, height, channels]`.

    For example:

    >>> batch_size, time, width, height, channels = 13,11,7,5,3
    >>> video_batch = tf.zeros([batch_size, time, width, height, channels])

    To replace a selection of video clips:
      * Use an `index_depth` of 1 (indexing the `outer_shape`: `[batch_size]`)
      * Provide updates each with a shape matching the `inner_shape`:
        `[time, width, height, channels]`.

    To replace the first two clips with ones:

    >>> indices = [[0],[1]]
    >>> new_clips = tf.ones([2, time, width, height, channels])
    >>> tf.tensor_scatter_nd_update(video_batch, indices, new_clips)

    To replace a selection of frames in the videos:

    * `indices` must have an `index_depth` of 2 for the `outer_shape`:
      `[batch_size, time]`.
    * `updates` must be shaped like a list of images.  Each update must have a
      shape, matching the `inner_shape`: `[width, height, channels]`.

    To replace the first frame of the first three video clips:

    >>> indices = [[0, 0], [1, 0], [2, 0]] # num_updates=3, index_depth=2
    >>> new_images = tf.ones([
    ...   # num_updates=3, inner_shape=(width, height, channels)
    ...   3, width, height, channels])
    >>> tf.tensor_scatter_nd_update(video_batch, indices, new_images)

    ### Folded indices

    In simple cases it's convenient to think of `indices` and `updates` as
    lists, but this is not a strict requirement. Instead of a flat `num_updates`,
    the `indices` and `updates` can be folded into a `batch_shape`. This
    `batch_shape` is all axes of the `indices`, except for the innermost
    `index_depth` axis.

    ```
    index_depth = indices.shape[-1]
    batch_shape = indices.shape[:-1]
    ```

    Note: The one exception is that the `batch_shape` cannot be `[]`. You can't
    update a single index by passing indices with shape `[index_depth]`.

    `updates` must have a matching `batch_shape` (the axes before `inner_shape`).

    ```
    assert updates.shape == batch_shape + inner_shape
    ```

    Note: The result is equivalent to flattening the `batch_shape` axes of
    `indices` and `updates`. This generalization just avoids the need
    for reshapes when it is more natural to construct "folded" indices and
    updates.

    With this generalization the full shape constraints are:

    ```
    assert tf.rank(indices) >= 2
    index_depth = indices.shape[-1]
    batch_shape = indices.shape[:-1]
    assert index_depth <= tf.rank(tensor)
    outer_shape = tensor.shape[:index_depth]
    inner_shape = tensor.shape[index_depth:]
    assert updates.shape == batch_shape + inner_shape
    ```

    For example, to draw an `X` on a `(5,5)` matrix start with these indices:

    >>> tensor = tf.zeros([5,5])
    >>> indices = tf.constant([
    ...  [[0,0],
    ...   [1,1],
    ...   [2,2],
    ...   [3,3],
    ...   [4,4]],
    ...  [[0,4],
    ...   [1,3],
    ...   [2,2],
    ...   [3,1],
    ...   [4,0]],
    ... ])
    >>> indices.shape.as_list()  # batch_shape == [2, 5], index_depth == 2
    [2, 5, 2]

    Here the `indices` do not have a shape of `[num_updates, index_depth]`, but a
    shape of `batch_shape+[index_depth]`.

    Since the `index_depth` is equal to the rank of `tensor`:

    * `outer_shape` is `(5,5)`
    * `inner_shape` is `()` - each update is scalar
    * `updates.shape` is `batch_shape + inner_shape == (5,2) + ()`

    >>> updates = [
    ...   [1,1,1,1,1],
    ...   [1,1,1,1,1],
    ... ]

    Putting this together gives:

    >>> tf.tensor_scatter_nd_update(tensor, indices, updates).numpy()
    array([[1., 0., 0., 0., 1.],
           [0., 1., 0., 1., 0.],
           [0., 0., 1., 0., 0.],
           [0., 1., 0., 1., 0.],
           [1., 0., 0., 0., 1.]], dtype=float32)

    Args:
      tensor: Tensor to copy/update.
      indices: Indices to update.
      updates: Updates to apply at the indices.
      name: Optional name for the operation.

    Returns:
      A new tensor with the given shape and updates applied according to the
      indices.
    """
    ...
def constant(
    value: TensorCompatible, dtype: DTypeLike | None = None, shape: ShapeLike | None = None, name: str | None = "Const"
) -> Tensor:
    """
    Creates a constant tensor from a tensor-like object.

    Note: All eager `tf.Tensor` values are immutable (in contrast to
    `tf.Variable`). There is nothing especially _constant_ about the value
    returned from `tf.constant`. This function is not fundamentally different from
    `tf.convert_to_tensor`. The name `tf.constant` comes from the `value` being
    embedded in a `Const` node in the `tf.Graph`. `tf.constant` is useful
    for asserting that the value can be embedded that way.

    If the argument `dtype` is not specified, then the type is inferred from
    the type of `value`.

    >>> # Constant 1-D Tensor from a python list.
    >>> tf.constant([1, 2, 3, 4, 5, 6])
    <tf.Tensor: shape=(6,), dtype=int32,
        numpy=array([1, 2, 3, 4, 5, 6], dtype=int32)>
    >>> # Or a numpy array
    >>> a = np.array([[1, 2, 3], [4, 5, 6]])
    >>> tf.constant(a)
    <tf.Tensor: shape=(2, 3), dtype=int64, numpy=
      array([[1, 2, 3],
             [4, 5, 6]])>

    If `dtype` is specified, the resulting tensor values are cast to the requested
    `dtype`.

    >>> tf.constant([1, 2, 3, 4, 5, 6], dtype=tf.float64)
    <tf.Tensor: shape=(6,), dtype=float64,
        numpy=array([1., 2., 3., 4., 5., 6.])>

    If `shape` is set, the `value` is reshaped to match. Scalars are expanded to
    fill the `shape`:

    >>> tf.constant(0, shape=(2, 3))
      <tf.Tensor: shape=(2, 3), dtype=int32, numpy=
      array([[0, 0, 0],
             [0, 0, 0]], dtype=int32)>
    >>> tf.constant([1, 2, 3, 4, 5, 6], shape=[2, 3])
    <tf.Tensor: shape=(2, 3), dtype=int32, numpy=
      array([[1, 2, 3],
             [4, 5, 6]], dtype=int32)>

    `tf.constant` has no effect if an eager Tensor is passed as the `value`, it
    even transmits gradients:

    >>> v = tf.Variable([0.0])
    >>> with tf.GradientTape() as g:
    ...     loss = tf.constant(v + v)
    >>> g.gradient(loss, v).numpy()
    array([2.], dtype=float32)

    But, since `tf.constant` embeds the value in the `tf.Graph` this fails for
    symbolic tensors:

    >>> with tf.compat.v1.Graph().as_default():
    ...   i = tf.compat.v1.placeholder(shape=[None, None], dtype=tf.float32)
    ...   t = tf.constant(i)
    Traceback (most recent call last):
    ...
    TypeError: ...

    `tf.constant` will create tensors on the current device. Inputs which are
    already tensors maintain their placements unchanged.

    Related Ops:

    * `tf.convert_to_tensor` is similar but:
      * It has no `shape` argument.
      * Symbolic tensors are allowed to pass through.

      >>> with tf.compat.v1.Graph().as_default():
      ...   i = tf.compat.v1.placeholder(shape=[None, None], dtype=tf.float32)
      ...   t = tf.convert_to_tensor(i)

    * `tf.fill`: differs in a few ways:
      *   `tf.constant` supports arbitrary constants, not just uniform scalar
          Tensors like `tf.fill`.
      *   `tf.fill` creates an Op in the graph that is expanded at runtime, so it
          can efficiently represent large tensors.
      *   Since `tf.fill` does not embed the value, it can produce dynamically
          sized outputs.

    Args:
      value: A constant value (or list) of output type `dtype`.
      dtype: The type of the elements of the resulting tensor.
      shape: Optional dimensions of resulting tensor.
      name: Optional name for the tensor.

    Returns:
      A Constant Tensor.

    Raises:
      TypeError: if shape is incorrectly specified or unsupported.
      ValueError: if called on a symbolic tensor.
    """
    ...
@overload
def cast(x: TensorCompatible, dtype: DTypeLike, name: str | None = None) -> Tensor:
    """
    Casts a tensor to a new type.

    The operation casts `x` (in case of `Tensor`) or `x.values`
    (in case of `SparseTensor` or `IndexedSlices`) to `dtype`.

    For example:

    >>> x = tf.constant([1.8, 2.2], dtype=tf.float32)
    >>> tf.cast(x, tf.int32)
    <tf.Tensor: shape=(2,), dtype=int32, numpy=array([1, 2], dtype=int32)>

    Notice `tf.cast` has an alias `tf.dtypes.cast`:

    >>> x = tf.constant([1.8, 2.2], dtype=tf.float32)
    >>> tf.dtypes.cast(x, tf.int32)
    <tf.Tensor: shape=(2,), dtype=int32, numpy=array([1, 2], dtype=int32)>

    The operation supports data types (for `x` and `dtype`) of
    `uint8`, `uint16`, `uint32`, `uint64`, `int8`, `int16`, `int32`, `int64`,
    `float16`, `float32`, `float64`, `complex64`, `complex128`, `bfloat16`.
    In case of casting from complex types (`complex64`, `complex128`) to real
    types, only the real part of `x` is returned. In case of casting from real
    types to complex types (`complex64`, `complex128`), the imaginary part of the
    returned value is set to `0`. The handling of complex types here matches the
    behavior of numpy.

    Note casting nan and inf values to integral types has undefined behavior.

    Note this operation can lead to a loss of precision when converting native
    Python `float` and `complex` variables to `tf.float64` or `tf.complex128`
    tensors, since the input is first converted to the `float32` data type and
    then widened. It is recommended to use `tf.convert_to_tensor` instead of
    `tf.cast` for any non-tensor inputs.

    Args:
      x: A `Tensor` or `SparseTensor` or `IndexedSlices` of numeric type. It could
        be `uint8`, `uint16`, `uint32`, `uint64`, `int8`, `int16`, `int32`,
        `int64`, `float16`, `float32`, `float64`, `complex64`, `complex128`,
        `bfloat16`.
      dtype: The destination type. The list of supported dtypes is the same as
        `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` or `SparseTensor` or `IndexedSlices` with same shape as `x` and
        same type as `dtype`.

    Raises:
      TypeError: If `x` cannot be cast to the `dtype`.
    """
    ...
@overload
def cast(x: SparseTensor, dtype: DTypeLike, name: str | None = None) -> SparseTensor:
    """
    Casts a tensor to a new type.

    The operation casts `x` (in case of `Tensor`) or `x.values`
    (in case of `SparseTensor` or `IndexedSlices`) to `dtype`.

    For example:

    >>> x = tf.constant([1.8, 2.2], dtype=tf.float32)
    >>> tf.cast(x, tf.int32)
    <tf.Tensor: shape=(2,), dtype=int32, numpy=array([1, 2], dtype=int32)>

    Notice `tf.cast` has an alias `tf.dtypes.cast`:

    >>> x = tf.constant([1.8, 2.2], dtype=tf.float32)
    >>> tf.dtypes.cast(x, tf.int32)
    <tf.Tensor: shape=(2,), dtype=int32, numpy=array([1, 2], dtype=int32)>

    The operation supports data types (for `x` and `dtype`) of
    `uint8`, `uint16`, `uint32`, `uint64`, `int8`, `int16`, `int32`, `int64`,
    `float16`, `float32`, `float64`, `complex64`, `complex128`, `bfloat16`.
    In case of casting from complex types (`complex64`, `complex128`) to real
    types, only the real part of `x` is returned. In case of casting from real
    types to complex types (`complex64`, `complex128`), the imaginary part of the
    returned value is set to `0`. The handling of complex types here matches the
    behavior of numpy.

    Note casting nan and inf values to integral types has undefined behavior.

    Note this operation can lead to a loss of precision when converting native
    Python `float` and `complex` variables to `tf.float64` or `tf.complex128`
    tensors, since the input is first converted to the `float32` data type and
    then widened. It is recommended to use `tf.convert_to_tensor` instead of
    `tf.cast` for any non-tensor inputs.

    Args:
      x: A `Tensor` or `SparseTensor` or `IndexedSlices` of numeric type. It could
        be `uint8`, `uint16`, `uint32`, `uint64`, `int8`, `int16`, `int32`,
        `int64`, `float16`, `float32`, `float64`, `complex64`, `complex128`,
        `bfloat16`.
      dtype: The destination type. The list of supported dtypes is the same as
        `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` or `SparseTensor` or `IndexedSlices` with same shape as `x` and
        same type as `dtype`.

    Raises:
      TypeError: If `x` cannot be cast to the `dtype`.
    """
    ...
@overload
def cast(x: RaggedTensor, dtype: DTypeLike, name: str | None = None) -> RaggedTensor:
    """
    Casts a tensor to a new type.

    The operation casts `x` (in case of `Tensor`) or `x.values`
    (in case of `SparseTensor` or `IndexedSlices`) to `dtype`.

    For example:

    >>> x = tf.constant([1.8, 2.2], dtype=tf.float32)
    >>> tf.cast(x, tf.int32)
    <tf.Tensor: shape=(2,), dtype=int32, numpy=array([1, 2], dtype=int32)>

    Notice `tf.cast` has an alias `tf.dtypes.cast`:

    >>> x = tf.constant([1.8, 2.2], dtype=tf.float32)
    >>> tf.dtypes.cast(x, tf.int32)
    <tf.Tensor: shape=(2,), dtype=int32, numpy=array([1, 2], dtype=int32)>

    The operation supports data types (for `x` and `dtype`) of
    `uint8`, `uint16`, `uint32`, `uint64`, `int8`, `int16`, `int32`, `int64`,
    `float16`, `float32`, `float64`, `complex64`, `complex128`, `bfloat16`.
    In case of casting from complex types (`complex64`, `complex128`) to real
    types, only the real part of `x` is returned. In case of casting from real
    types to complex types (`complex64`, `complex128`), the imaginary part of the
    returned value is set to `0`. The handling of complex types here matches the
    behavior of numpy.

    Note casting nan and inf values to integral types has undefined behavior.

    Note this operation can lead to a loss of precision when converting native
    Python `float` and `complex` variables to `tf.float64` or `tf.complex128`
    tensors, since the input is first converted to the `float32` data type and
    then widened. It is recommended to use `tf.convert_to_tensor` instead of
    `tf.cast` for any non-tensor inputs.

    Args:
      x: A `Tensor` or `SparseTensor` or `IndexedSlices` of numeric type. It could
        be `uint8`, `uint16`, `uint32`, `uint64`, `int8`, `int16`, `int32`,
        `int64`, `float16`, `float32`, `float64`, `complex64`, `complex128`,
        `bfloat16`.
      dtype: The destination type. The list of supported dtypes is the same as
        `x`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` or `SparseTensor` or `IndexedSlices` with same shape as `x` and
        same type as `dtype`.

    Raises:
      TypeError: If `x` cannot be cast to the `dtype`.
    """
    ...
def zeros(shape: ShapeLike, dtype: DTypeLike = ..., name: str | None = None, layout: Layout | None = None) -> Tensor:
    """
    Creates a tensor with all elements set to zero.

    See also `tf.zeros_like`, `tf.ones`, `tf.fill`, `tf.eye`.

    This operation returns a tensor of type `dtype` with shape `shape` and
    all elements set to zero.

    >>> tf.zeros([3, 4], tf.int32)
    <tf.Tensor: shape=(3, 4), dtype=int32, numpy=
    array([[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]], dtype=int32)>

    Args:
      shape: A `list` of integers, a `tuple` of integers, or a 1-D `Tensor` of
        type `int32`.
      dtype: The DType of an element in the resulting `Tensor`.
      name: Optional string. A name for the operation.
      layout: Optional, `tf.experimental.dtensor.Layout`. If provided, the result
        is a [DTensor](https://www.tensorflow.org/guide/dtensor_overview) with the
        provided layout.

    Returns:
      A `Tensor` with all elements set to zero.
    """
    ...
def ones(shape: ShapeLike, dtype: DTypeLike = ..., name: str | None = None, layout: Layout | None = None) -> Tensor:
    """
    Creates a tensor with all elements set to one (1).

    See also `tf.ones_like`, `tf.zeros`, `tf.fill`, `tf.eye`.

    This operation returns a tensor of type `dtype` with shape `shape` and
    all elements set to one.

    >>> tf.ones([3, 4], tf.int32)
    <tf.Tensor: shape=(3, 4), dtype=int32, numpy=
    array([[1, 1, 1, 1],
           [1, 1, 1, 1],
           [1, 1, 1, 1]], dtype=int32)>

    Args:
      shape: A `list` of integers, a `tuple` of integers, or a 1-D `Tensor` of
        type `int32`.
      dtype: Optional DType of an element in the resulting `Tensor`. Default is
        `tf.float32`.
      name: Optional string. A name for the operation.
      layout: Optional, `tf.experimental.dtensor.Layout`. If provided, the result
        is a [DTensor](https://www.tensorflow.org/guide/dtensor_overview) with the
        provided layout.

    Returns:
      A `Tensor` with all elements set to one (1).
    """
    ...
@overload
def zeros_like(
    input: TensorCompatible | IndexedSlices, dtype: DTypeLike | None = None, name: str | None = None, layout: Layout | None = None
) -> Tensor:
    """
    Creates a tensor with all elements set to zero.

    See also `tf.zeros`.

    Given a single tensor or array-like object (`input`), this operation returns
    a tensor of the same type and shape as `input` with all elements set to zero.
    Optionally, you can use `dtype` to specify a new type for the returned tensor.

    Note that the layout of the input tensor is not preserved if the op
    is used inside tf.function. To obtain a tensor with the same layout as the
    input, chain the returned value to a `dtensor.relayout_like`.

    Examples:

      >>> tensor = tf.constant([[1, 2, 3], [4, 5, 6]])
      >>> tf.zeros_like(tensor)
      <tf.Tensor: shape=(2, 3), dtype=int32, numpy=
      array([[0, 0, 0],
             [0, 0, 0]], dtype=int32)>

      >>> tf.zeros_like(tensor, dtype=tf.float32)
      <tf.Tensor: shape=(2, 3), dtype=float32, numpy=
      array([[0., 0., 0.],
             [0., 0., 0.]], dtype=float32)>

      >>> tf.zeros_like([[1, 2, 3], [4, 5, 6]])
      <tf.Tensor: shape=(2, 3), dtype=int32, numpy=
      array([[0, 0, 0],
             [0, 0, 0]], dtype=int32)>

    Args:
      input: A `Tensor` or array-like object.
      dtype: A type for the returned `Tensor`. Must be `float16`, `float32`,
        `float64`, `int8`, `uint8`, `int16`, `uint16`, `int32`, `int64`,
        `complex64`, `complex128`, `bool` or `string` (optional).
      name: A name for the operation (optional).
      layout: Optional, `tf.experimental.dtensor.Layout`. If provided, the result
        is a [DTensor](https://www.tensorflow.org/guide/dtensor_overview) with the
        provided layout.

    Returns:
      A `Tensor` with all elements set to zero.
    """
    ...
@overload
def zeros_like(
    input: RaggedTensor, dtype: DTypeLike | None = None, name: str | None = None, layout: Layout | None = None
) -> RaggedTensor:
    """
    Creates a tensor with all elements set to zero.

    See also `tf.zeros`.

    Given a single tensor or array-like object (`input`), this operation returns
    a tensor of the same type and shape as `input` with all elements set to zero.
    Optionally, you can use `dtype` to specify a new type for the returned tensor.

    Note that the layout of the input tensor is not preserved if the op
    is used inside tf.function. To obtain a tensor with the same layout as the
    input, chain the returned value to a `dtensor.relayout_like`.

    Examples:

      >>> tensor = tf.constant([[1, 2, 3], [4, 5, 6]])
      >>> tf.zeros_like(tensor)
      <tf.Tensor: shape=(2, 3), dtype=int32, numpy=
      array([[0, 0, 0],
             [0, 0, 0]], dtype=int32)>

      >>> tf.zeros_like(tensor, dtype=tf.float32)
      <tf.Tensor: shape=(2, 3), dtype=float32, numpy=
      array([[0., 0., 0.],
             [0., 0., 0.]], dtype=float32)>

      >>> tf.zeros_like([[1, 2, 3], [4, 5, 6]])
      <tf.Tensor: shape=(2, 3), dtype=int32, numpy=
      array([[0, 0, 0],
             [0, 0, 0]], dtype=int32)>

    Args:
      input: A `Tensor` or array-like object.
      dtype: A type for the returned `Tensor`. Must be `float16`, `float32`,
        `float64`, `int8`, `uint8`, `int16`, `uint16`, `int32`, `int64`,
        `complex64`, `complex128`, `bool` or `string` (optional).
      name: A name for the operation (optional).
      layout: Optional, `tf.experimental.dtensor.Layout`. If provided, the result
        is a [DTensor](https://www.tensorflow.org/guide/dtensor_overview) with the
        provided layout.

    Returns:
      A `Tensor` with all elements set to zero.
    """
    ...
@overload
def ones_like(
    input: TensorCompatible, dtype: DTypeLike | None = None, name: str | None = None, layout: Layout | None = None
) -> Tensor:
    """
    Creates a tensor of all ones that has the same shape as the input.

    See also `tf.ones`.

    Given a single tensor (`tensor`), this operation returns a tensor of the
    same type and shape as `tensor` with all elements set to 1. Optionally,
    you can use `dtype` to specify a new type for the returned tensor.

    For example:

    >>> tensor = tf.constant([[1, 2, 3], [4, 5, 6]])
    >>> tf.ones_like(tensor)
    <tf.Tensor: shape=(2, 3), dtype=int32, numpy=
      array([[1, 1, 1],
             [1, 1, 1]], dtype=int32)>

    Note that the layout of the input tensor is not preserved if the op
    is used inside tf.function. To obtain a tensor with the same layout as the
    input, chain the returned value to a `dtensor.relayout_like`.

    Args:
      input: A `Tensor`.
      dtype: A type for the returned `Tensor`. Must be `float16`, `float32`,
        `float64`, `int8`, `uint8`, `int16`, `uint16`, `int32`, `int64`,
        `complex64`, `complex128`, `bool` or `string`.
      name: A name for the operation (optional).
      layout: Optional, `tf.experimental.dtensor.Layout`. If provided, the result
        is a [DTensor](https://www.tensorflow.org/guide/dtensor_overview) with the
        provided layout.

    Returns:
      A `Tensor` with all elements set to one.
    """
    ...
@overload
def ones_like(
    input: RaggedTensor, dtype: DTypeLike | None = None, name: str | None = None, layout: Layout | None = None
) -> RaggedTensor:
    """
    Creates a tensor of all ones that has the same shape as the input.

    See also `tf.ones`.

    Given a single tensor (`tensor`), this operation returns a tensor of the
    same type and shape as `tensor` with all elements set to 1. Optionally,
    you can use `dtype` to specify a new type for the returned tensor.

    For example:

    >>> tensor = tf.constant([[1, 2, 3], [4, 5, 6]])
    >>> tf.ones_like(tensor)
    <tf.Tensor: shape=(2, 3), dtype=int32, numpy=
      array([[1, 1, 1],
             [1, 1, 1]], dtype=int32)>

    Note that the layout of the input tensor is not preserved if the op
    is used inside tf.function. To obtain a tensor with the same layout as the
    input, chain the returned value to a `dtensor.relayout_like`.

    Args:
      input: A `Tensor`.
      dtype: A type for the returned `Tensor`. Must be `float16`, `float32`,
        `float64`, `int8`, `uint8`, `int16`, `uint16`, `int32`, `int64`,
        `complex64`, `complex128`, `bool` or `string`.
      name: A name for the operation (optional).
      layout: Optional, `tf.experimental.dtensor.Layout`. If provided, the result
        is a [DTensor](https://www.tensorflow.org/guide/dtensor_overview) with the
        provided layout.

    Returns:
      A `Tensor` with all elements set to one.
    """
    ...
def reshape(tensor: TensorCompatible, shape: ShapeLike | Tensor, name: str | None = None) -> Tensor:
    """
    Reshapes a tensor.

    Given `tensor`, this operation returns a new `tf.Tensor` that has the same
    values as `tensor` in the same order, except with a new shape given by
    `shape`.

    >>> t1 = [[1, 2, 3],
    ...       [4, 5, 6]]
    >>> print(tf.shape(t1).numpy())
    [2 3]
    >>> t2 = tf.reshape(t1, [6])
    >>> t2
    <tf.Tensor: shape=(6,), dtype=int32,
      numpy=array([1, 2, 3, 4, 5, 6], dtype=int32)>
    >>> tf.reshape(t2, [3, 2])
    <tf.Tensor: shape=(3, 2), dtype=int32, numpy=
      array([[1, 2],
             [3, 4],
             [5, 6]], dtype=int32)>

    The `tf.reshape` does not change the order of or the total number of elements
    in the tensor, and so it can reuse the underlying data buffer. This makes it
    a fast operation independent of how big of a tensor it is operating on.

    >>> tf.reshape([1, 2, 3], [2, 2])
    Traceback (most recent call last):
    ...
    InvalidArgumentError: Input to reshape is a tensor with 3 values, but the
    requested shape has 4

    To instead reorder the data to rearrange the dimensions of a tensor, see
    `tf.transpose`.

    >>> t = [[1, 2, 3],
    ...      [4, 5, 6]]
    >>> tf.reshape(t, [3, 2]).numpy()
    array([[1, 2],
           [3, 4],
           [5, 6]], dtype=int32)
    >>> tf.transpose(t, perm=[1, 0]).numpy()
    array([[1, 4],
           [2, 5],
           [3, 6]], dtype=int32)

    If one component of `shape` is the special value -1, the size of that
    dimension is computed so that the total size remains constant.  In particular,
    a `shape` of `[-1]` flattens into 1-D.  At most one component of `shape` can
    be -1.

    >>> t = [[1, 2, 3],
    ...      [4, 5, 6]]
    >>> tf.reshape(t, [-1])
    <tf.Tensor: shape=(6,), dtype=int32,
      numpy=array([1, 2, 3, 4, 5, 6], dtype=int32)>
    >>> tf.reshape(t, [3, -1])
    <tf.Tensor: shape=(3, 2), dtype=int32, numpy=
      array([[1, 2],
             [3, 4],
             [5, 6]], dtype=int32)>
    >>> tf.reshape(t, [-1, 2])
    <tf.Tensor: shape=(3, 2), dtype=int32, numpy=
      array([[1, 2],
             [3, 4],
             [5, 6]], dtype=int32)>

    `tf.reshape(t, [])` reshapes a tensor `t` with one element to a scalar.

    >>> tf.reshape([7], []).numpy().item()
    7

    More examples:

    >>> t = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> print(tf.shape(t).numpy())
    [9]
    >>> tf.reshape(t, [3, 3])
    <tf.Tensor: shape=(3, 3), dtype=int32, numpy=
      array([[1, 2, 3],
             [4, 5, 6],
             [7, 8, 9]], dtype=int32)>

    >>> t = [[[1, 1], [2, 2]],
    ...      [[3, 3], [4, 4]]]
    >>> print(tf.shape(t).numpy())
    [2 2 2]
    >>> tf.reshape(t, [2, 4])
    <tf.Tensor: shape=(2, 4), dtype=int32, numpy=
      array([[1, 1, 2, 2],
             [3, 3, 4, 4]], dtype=int32)>

    >>> t = [[[1, 1, 1],
    ...       [2, 2, 2]],
    ...      [[3, 3, 3],
    ...       [4, 4, 4]],
    ...      [[5, 5, 5],
    ...       [6, 6, 6]]]
    >>> print(tf.shape(t).numpy())
    [3 2 3]
    >>> # Pass '[-1]' to flatten 't'.
    >>> tf.reshape(t, [-1])
    <tf.Tensor: shape=(18,), dtype=int32,
      numpy=array([1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
      dtype=int32)>
    >>> # -- Using -1 to infer the shape --
    >>> # Here -1 is inferred to be 9:
    >>> tf.reshape(t, [2, -1])
    <tf.Tensor: shape=(2, 9), dtype=int32, numpy=
      array([[1, 1, 1, 2, 2, 2, 3, 3, 3],
             [4, 4, 4, 5, 5, 5, 6, 6, 6]], dtype=int32)>
    >>> # -1 is inferred to be 2:
    >>> tf.reshape(t, [-1, 9])
    <tf.Tensor: shape=(2, 9), dtype=int32, numpy=
      array([[1, 1, 1, 2, 2, 2, 3, 3, 3],
             [4, 4, 4, 5, 5, 5, 6, 6, 6]], dtype=int32)>
    >>> # -1 is inferred to be 3:
    >>> tf.reshape(t, [ 2, -1, 3])
    <tf.Tensor: shape=(2, 3, 3), dtype=int32, numpy=
      array([[[1, 1, 1],
              [2, 2, 2],
              [3, 3, 3]],
             [[4, 4, 4],
              [5, 5, 5],
              [6, 6, 6]]], dtype=int32)>

    Args:
      tensor: A `Tensor`.
      shape: A `Tensor`. Must be one of the following types: `int32`, `int64`.
        Defines the shape of the output tensor.
      name: Optional string. A name for the operation.

    Returns:
      A `Tensor`. Has the same type as `tensor`.
    """
    ...
def pad(
    tensor: TensorCompatible,
    paddings: Tensor | IntArray | Iterable[Iterable[int]],
    mode: Literal["CONSTANT", "constant", "REFLECT", "reflect", "SYMMETRIC", "symmetric"] = "CONSTANT",
    constant_values: ScalarTensorCompatible = 0,
    name: str | None = None,
) -> Tensor:
    """
    Pads a tensor.

    This operation pads a `tensor` according to the `paddings` you specify.
    `paddings` is an integer tensor with shape `[n, 2]`, where n is the rank of
    `tensor`. For each dimension D of `input`, `paddings[D, 0]` indicates how
    many values to add before the contents of `tensor` in that dimension, and
    `paddings[D, 1]` indicates how many values to add after the contents of
    `tensor` in that dimension. If `mode` is "REFLECT" then both `paddings[D, 0]`
    and `paddings[D, 1]` must be no greater than `tensor.dim_size(D) - 1`. If
    `mode` is "SYMMETRIC" then both `paddings[D, 0]` and `paddings[D, 1]` must be
    no greater than `tensor.dim_size(D)`.

    The padded size of each dimension D of the output is:

    `paddings[D, 0] + tensor.dim_size(D) + paddings[D, 1]`

    For example:

    ```python
    t = tf.constant([[1, 2, 3], [4, 5, 6]])
    paddings = tf.constant([[1, 1,], [2, 2]])
    # 'constant_values' is 0.
    # rank of 't' is 2.
    tf.pad(t, paddings, "CONSTANT")  # [[0, 0, 0, 0, 0, 0, 0],
                                     #  [0, 0, 1, 2, 3, 0, 0],
                                     #  [0, 0, 4, 5, 6, 0, 0],
                                     #  [0, 0, 0, 0, 0, 0, 0]]

    tf.pad(t, paddings, "REFLECT")  # [[6, 5, 4, 5, 6, 5, 4],
                                    #  [3, 2, 1, 2, 3, 2, 1],
                                    #  [6, 5, 4, 5, 6, 5, 4],
                                    #  [3, 2, 1, 2, 3, 2, 1]]

    tf.pad(t, paddings, "SYMMETRIC")  # [[2, 1, 1, 2, 3, 3, 2],
                                      #  [2, 1, 1, 2, 3, 3, 2],
                                      #  [5, 4, 4, 5, 6, 6, 5],
                                      #  [5, 4, 4, 5, 6, 6, 5]]
    ```

    Args:
      tensor: A `Tensor`.
      paddings: A `Tensor` of type `int32`.
      mode: One of "CONSTANT", "REFLECT", or "SYMMETRIC" (case-insensitive)
      constant_values: In "CONSTANT" mode, the scalar pad value to use. Must be
        same type as `tensor`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `tensor`.

    Raises:
      ValueError: When mode is not one of "CONSTANT", "REFLECT", or "SYMMETRIC".
    """
    ...
def shape(input: SparseTensorCompatible, out_type: DTypeLike | None = None, name: str | None = None) -> Tensor:
    """
    Returns a tensor containing the shape of the input tensor.

    See also `tf.size`, `tf.rank`.

    `tf.shape` returns a 1-D integer tensor representing the shape of `input`.
    For a scalar input, the tensor returned has a shape of (0,) and its value is
    the empty vector (i.e. []).

    For example:

    >>> tf.shape(1.)
    <tf.Tensor: shape=(0,), dtype=int32, numpy=array([], dtype=int32)>

    >>> t = tf.constant([[[1, 1, 1], [2, 2, 2]], [[3, 3, 3], [4, 4, 4]]])
    >>> tf.shape(t)
    <tf.Tensor: shape=(3,), dtype=int32, numpy=array([2, 2, 3], dtype=int32)>

    Note: When using symbolic tensors, such as when using the Keras API,
    tf.shape() will return the shape of the symbolic tensor.

    >>> a = tf.keras.layers.Input((None, 10))
    >>> tf.shape(a)
    <... shape=(3,) dtype=int32...>

    In these cases, using `tf.Tensor.shape` will return more informative results.

    >>> a.shape
    TensorShape([None, None, 10])

    (The first `None` represents the as yet unknown batch size.)

    `tf.shape` and `Tensor.shape` should be identical in eager mode.  Within
    `tf.function` or within a `compat.v1` context, not all dimensions may be
    known until execution time. Hence, when defining custom layers and models
    for graph mode, prefer the dynamic `tf.shape(x)` over the static `x.shape`.

    Args:
      input: A `Tensor` or `SparseTensor`.
      out_type: (Optional) The specified output type of the operation (`int32` or
        `int64`). Defaults to `tf.int32`. (Note: there is an experimental
        flag, `tf_shape_default_int64` that changes the default to `tf.int64`.
        This is an unsupported, experimental setting that causes known breakages.)
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of type `out_type`.
    """
    ...
def where(
    condition: TensorCompatible, x: TensorCompatible | None = None, y: TensorCompatible | None = None, name: str | None = None
) -> Tensor:
    """
    Returns the indices of non-zero elements, or multiplexes `x` and `y`.

    This operation has two modes:

    1. **Return the indices of non-zero elements** - When only
       `condition` is provided the result is an `int64` tensor where each row is
       the index of a non-zero element of `condition`. The result's shape
       is `[tf.math.count_nonzero(condition), tf.rank(condition)]`.
    2. **Multiplex `x` and `y`** - When both `x` and `y` are provided the
       result has the shape of `x`, `y`, and `condition` broadcast together. The
       result is taken from `x` where `condition` is non-zero
       or `y` where `condition` is zero.

    #### 1. Return the indices of non-zero elements

    Note: In this mode `condition` can have a dtype of `bool` or any numeric
    dtype.

    If `x` and `y` are not provided (both are None):

    `tf.where` will return the indices of `condition` that are non-zero,
    in the form of a 2-D tensor with shape `[n, d]`, where `n` is the number of
    non-zero elements in `condition` (`tf.count_nonzero(condition)`), and `d` is
    the number of axes of `condition` (`tf.rank(condition)`).

    Indices are output in row-major order. The `condition` can have a `dtype` of
    `tf.bool`, or any numeric `dtype`.

    Here `condition` is a 1-axis `bool` tensor with 2 `True` values. The result
    has a shape of `[2,1]`

    >>> tf.where([True, False, False, True]).numpy()
    array([[0],
           [3]])

    Here `condition` is a 2-axis integer tensor, with 3 non-zero values. The
    result has a shape of `[3, 2]`.

    >>> tf.where([[1, 0, 0], [1, 0, 1]]).numpy()
    array([[0, 0],
           [1, 0],
           [1, 2]])

    Here `condition` is a 3-axis float tensor, with 5 non-zero values. The output
    shape is `[5, 3]`.

    >>> float_tensor = [[[0.1, 0], [0, 2.2], [3.5, 1e6]],
    ...                 [[0,   0], [0,   0], [99,    0]]]
    >>> tf.where(float_tensor).numpy()
    array([[0, 0, 0],
           [0, 1, 1],
           [0, 2, 0],
           [0, 2, 1],
           [1, 2, 0]])

    These indices are the same that `tf.sparse.SparseTensor` would use to
    represent the condition tensor:

    >>> sparse = tf.sparse.from_dense(float_tensor)
    >>> sparse.indices.numpy()
    array([[0, 0, 0],
           [0, 1, 1],
           [0, 2, 0],
           [0, 2, 1],
           [1, 2, 0]])

    A complex number is considered non-zero if either the real or imaginary
    component is non-zero:

    >>> tf.where([complex(0.), complex(1.), 0+1j, 1+1j]).numpy()
    array([[1],
           [2],
           [3]])

    #### 2. Multiplex `x` and `y`

    Note: In this mode `condition` must have a dtype of `bool`.

    If `x` and `y` are also provided (both have non-None values) the `condition`
    tensor acts as a mask that chooses whether the corresponding
    element / row in the output should be taken from `x` (if the element in
    `condition` is `True`) or `y` (if it is `False`).

    The shape of the result is formed by
    [broadcasting](https://docs.scipy.org/doc/numpy/reference/ufuncs.html)
    together the shapes of `condition`, `x`, and `y`.

    When all three inputs have the same size, each is handled element-wise.

    >>> tf.where([True, False, False, True],
    ...          [1, 2, 3, 4],
    ...          [100, 200, 300, 400]).numpy()
    array([  1, 200, 300,   4], dtype=int32)

    There are two main rules for broadcasting:

    1. If a tensor has fewer axes than the others, length-1 axes are added to the
       left of the shape.
    2. Axes with length-1 are streched to match the coresponding axes of the other
       tensors.

    A length-1 vector is streched to match the other vectors:

    >>> tf.where([True, False, False, True], [1, 2, 3, 4], [100]).numpy()
    array([  1, 100, 100,   4], dtype=int32)

    A scalar is expanded to match the other arguments:

    >>> tf.where([[True, False], [False, True]], [[1, 2], [3, 4]], 100).numpy()
    array([[  1, 100], [100,   4]], dtype=int32)
    >>> tf.where([[True, False], [False, True]], 1, 100).numpy()
    array([[  1, 100], [100,   1]], dtype=int32)

    A scalar `condition` returns the complete `x` or `y` tensor, with
    broadcasting applied.

    >>> tf.where(True, [1, 2, 3, 4], 100).numpy()
    array([1, 2, 3, 4], dtype=int32)
    >>> tf.where(False, [1, 2, 3, 4], 100).numpy()
    array([100, 100, 100, 100], dtype=int32)

    For a non-trivial example of broadcasting, here `condition` has a shape of
    `[3]`, `x` has a shape of `[3,3]`, and `y` has a shape of `[3,1]`.
    Broadcasting first expands the shape of `condition` to `[1,3]`. The final
    broadcast shape is `[3,3]`. `condition` will select columns from `x` and `y`.
    Since `y` only has one column, all columns from `y` will be identical.

    >>> tf.where([True, False, True],
    ...          x=[[1, 2, 3],
    ...             [4, 5, 6],
    ...             [7, 8, 9]],
    ...          y=[[100],
    ...             [200],
    ...             [300]]
    ... ).numpy()
    array([[ 1, 100, 3],
           [ 4, 200, 6],
           [ 7, 300, 9]], dtype=int32)

    Note that if the gradient of either branch of the `tf.where` generates
    a `NaN`, then the gradient of the entire `tf.where` will be `NaN`. This is
    because the gradient calculation for `tf.where` combines the two branches, for
    performance reasons.

    A workaround is to use an inner `tf.where` to ensure the function has
    no asymptote, and to avoid computing a value whose gradient is `NaN` by
    replacing dangerous inputs with safe inputs.

    Instead of this,

    >>> x = tf.constant(0., dtype=tf.float32)
    >>> with tf.GradientTape() as tape:
    ...   tape.watch(x)
    ...   y = tf.where(x < 1., 0., 1. / x)
    >>> print(tape.gradient(y, x))
    tf.Tensor(nan, shape=(), dtype=float32)

    Although, the `1. / x` values are never used, its gradient is a `NaN` when
    `x = 0`. Instead, we should guard that with another `tf.where`

    >>> x = tf.constant(0., dtype=tf.float32)
    >>> with tf.GradientTape() as tape:
    ...   tape.watch(x)
    ...   safe_x = tf.where(tf.equal(x, 0.), 1., x)
    ...   y = tf.where(x < 1., 0., 1. / safe_x)
    >>> print(tape.gradient(y, x))
    tf.Tensor(0.0, shape=(), dtype=float32)

    See also:

    * `tf.sparse` - The indices returned by the first form of `tf.where` can be
       useful in `tf.sparse.SparseTensor` objects.
    * `tf.gather_nd`, `tf.scatter_nd`, and related ops - Given the
      list of indices returned from `tf.where` the `scatter` and `gather` family
      of ops can be used fetch values or insert values at those indices.
    * `tf.strings.length` - `tf.string` is not an allowed dtype for the
      `condition`. Use the string length instead.

    Args:
      condition: A `tf.Tensor` of dtype bool, or any numeric dtype. `condition`
        must have dtype `bool` when `x` and `y` are provided.
      x: If provided, a Tensor which is of the same type as `y`, and has a shape
        broadcastable with `condition` and `y`.
      y: If provided, a Tensor which is of the same type as `x`, and has a shape
        broadcastable with `condition` and `x`.
      name: A name of the operation (optional).

    Returns:
      If `x` and `y` are provided:
        A `Tensor` with the same type as `x` and `y`, and shape that
        is broadcast from `condition`, `x`, and `y`.
      Otherwise, a `Tensor` with shape `[tf.math.count_nonzero(condition),
      tf.rank(condition)]`.

    Raises:
      ValueError: When exactly one of `x` or `y` is non-None, or the shapes
        are not all broadcastable.
    """
    ...
def gather_nd(
    params: TensorCompatible,
    indices: UIntTensorCompatible,
    batch_dims: UIntTensorCompatible = 0,
    name: str | None = None,
    bad_indices_policy: Literal["", "DEFAULT", "ERROR", "IGNORE"] = "",
) -> Tensor:
    """
    Gather slices from `params` into a Tensor with shape specified by `indices`.

    `indices` is a `Tensor` of indices into `params`. The index vectors are
    arranged along the last axis of `indices`.

    This is similar to `tf.gather`, in which `indices` defines slices into the
    first dimension of `params`. In `tf.gather_nd`, `indices` defines slices into
    the first `N` dimensions of `params`, where `N = indices.shape[-1]`.

    ## Gathering scalars

    In the simplest case the vectors in `indices` index the full rank of `params`:

    >>> tf.gather_nd(
    ...     indices=[[0, 0],
    ...              [1, 1]],
    ...     params = [['a', 'b'],
    ...               ['c', 'd']]).numpy()
    array([b'a', b'd'], dtype=object)

    In this case the result has 1-axis fewer than `indices`, and each index vector
    is replaced by the scalar indexed from `params`.

    In this case the shape relationship is:

    ```
    index_depth = indices.shape[-1]
    assert index_depth == params.shape.rank
    result_shape = indices.shape[:-1]
    ```

    If `indices` has a rank of `K`, it is helpful to think `indices` as a
    (K-1)-dimensional tensor of indices into `params`.

    ## Gathering slices

    If the index vectors do not index the full rank of `params` then each location
    in the result contains a slice of params. This example collects rows from a
    matrix:

    >>> tf.gather_nd(
    ...     indices = [[1],
    ...                [0]],
    ...     params = [['a', 'b', 'c'],
    ...               ['d', 'e', 'f']]).numpy()
    array([[b'd', b'e', b'f'],
           [b'a', b'b', b'c']], dtype=object)

    Here `indices` contains `[2]` index vectors, each with a length of `1`.
    The index vectors each refer to rows of the `params` matrix. Each
    row has a shape of `[3]` so the output shape is `[2, 3]`.

    In this case, the relationship between the shapes is:

    ```
    index_depth = indices.shape[-1]
    outer_shape = indices.shape[:-1]
    assert index_depth <= params.shape.rank
    inner_shape = params.shape[index_depth:]
    output_shape = outer_shape + inner_shape
    ```

    It is helpful to think of the results in this case as tensors-of-tensors.
    The shape of the outer tensor is set by the leading dimensions of `indices`.
    While the shape of the inner tensors is the shape of a single slice.

    ## Batches

    Additionally, both `params` and `indices` can have `M` leading batch
    dimensions that exactly match. In this case `batch_dims` must be set to `M`.

    For example, to collect one row from each of a batch of matrices you could
    set the leading elements of the index vectors to be their location in the
    batch:

    >>> tf.gather_nd(
    ...     indices = [[0, 1],
    ...                [1, 0],
    ...                [2, 4],
    ...                [3, 2],
    ...                [4, 1]],
    ...     params=tf.zeros([5, 7, 3])).shape.as_list()
    [5, 3]

    The `batch_dims` argument lets you omit those leading location dimensions
    from the index:

    >>> tf.gather_nd(
    ...     batch_dims=1,
    ...     indices = [[1],
    ...                [0],
    ...                [4],
    ...                [2],
    ...                [1]],
    ...     params=tf.zeros([5, 7, 3])).shape.as_list()
    [5, 3]

    This is equivalent to caling a separate `gather_nd` for each location in the
    batch dimensions.


    >>> params=tf.zeros([5, 7, 3])
    >>> indices=tf.zeros([5, 1])
    >>> batch_dims = 1
    >>>
    >>> index_depth = indices.shape[-1]
    >>> batch_shape = indices.shape[:batch_dims]
    >>> assert params.shape[:batch_dims] == batch_shape
    >>> outer_shape = indices.shape[batch_dims:-1]
    >>> assert index_depth <= params.shape.rank
    >>> inner_shape = params.shape[batch_dims + index_depth:]
    >>> output_shape = batch_shape + outer_shape + inner_shape
    >>> output_shape.as_list()
    [5, 3]

    ### More examples

    Indexing into a 3-tensor:

    >>> tf.gather_nd(
    ...     indices = [[1]],
    ...     params = [[['a0', 'b0'], ['c0', 'd0']],
    ...               [['a1', 'b1'], ['c1', 'd1']]]).numpy()
    array([[[b'a1', b'b1'],
            [b'c1', b'd1']]], dtype=object)



    >>> tf.gather_nd(
    ...     indices = [[0, 1], [1, 0]],
    ...     params = [[['a0', 'b0'], ['c0', 'd0']],
    ...               [['a1', 'b1'], ['c1', 'd1']]]).numpy()
    array([[b'c0', b'd0'],
           [b'a1', b'b1']], dtype=object)


    >>> tf.gather_nd(
    ...     indices = [[0, 0, 1], [1, 0, 1]],
    ...     params = [[['a0', 'b0'], ['c0', 'd0']],
    ...               [['a1', 'b1'], ['c1', 'd1']]]).numpy()
    array([b'b0', b'b1'], dtype=object)

    The examples below are for the case when only indices have leading extra
    dimensions. If both 'params' and 'indices' have leading batch dimensions, use
    the 'batch_dims' parameter to run gather_nd in batch mode.

    Batched indexing into a matrix:

    >>> tf.gather_nd(
    ...     indices = [[[0, 0]], [[0, 1]]],
    ...     params = [['a', 'b'], ['c', 'd']]).numpy()
    array([[b'a'],
           [b'b']], dtype=object)



    Batched slice indexing into a matrix:

    >>> tf.gather_nd(
    ...     indices = [[[1]], [[0]]],
    ...     params = [['a', 'b'], ['c', 'd']]).numpy()
    array([[[b'c', b'd']],
           [[b'a', b'b']]], dtype=object)


    Batched indexing into a 3-tensor:

    >>> tf.gather_nd(
    ...     indices = [[[1]], [[0]]],
    ...     params = [[['a0', 'b0'], ['c0', 'd0']],
    ...               [['a1', 'b1'], ['c1', 'd1']]]).numpy()
    array([[[[b'a1', b'b1'],
             [b'c1', b'd1']]],
           [[[b'a0', b'b0'],
             [b'c0', b'd0']]]], dtype=object)


    >>> tf.gather_nd(
    ...     indices = [[[0, 1], [1, 0]], [[0, 0], [1, 1]]],
    ...     params = [[['a0', 'b0'], ['c0', 'd0']],
    ...               [['a1', 'b1'], ['c1', 'd1']]]).numpy()
    array([[[b'c0', b'd0'],
            [b'a1', b'b1']],
           [[b'a0', b'b0'],
            [b'c1', b'd1']]], dtype=object)

    >>> tf.gather_nd(
    ...     indices = [[[0, 0, 1], [1, 0, 1]], [[0, 1, 1], [1, 1, 0]]],
    ...     params = [[['a0', 'b0'], ['c0', 'd0']],
    ...               [['a1', 'b1'], ['c1', 'd1']]]).numpy()
    array([[b'b0', b'b1'],
           [b'd0', b'c1']], dtype=object)


    Examples with batched 'params' and 'indices':

    >>> tf.gather_nd(
    ...     batch_dims = 1,
    ...     indices = [[1],
    ...                [0]],
    ...     params = [[['a0', 'b0'],
    ...                ['c0', 'd0']],
    ...               [['a1', 'b1'],
    ...                ['c1', 'd1']]]).numpy()
    array([[b'c0', b'd0'],
           [b'a1', b'b1']], dtype=object)


    >>> tf.gather_nd(
    ...     batch_dims = 1,
    ...     indices = [[[1]], [[0]]],
    ...     params = [[['a0', 'b0'], ['c0', 'd0']],
    ...               [['a1', 'b1'], ['c1', 'd1']]]).numpy()
    array([[[b'c0', b'd0']],
           [[b'a1', b'b1']]], dtype=object)

    >>> tf.gather_nd(
    ...     batch_dims = 1,
    ...     indices = [[[1, 0]], [[0, 1]]],
    ...     params = [[['a0', 'b0'], ['c0', 'd0']],
    ...               [['a1', 'b1'], ['c1', 'd1']]]).numpy()
    array([[b'c0'],
           [b'b1']], dtype=object)


    See also `tf.gather`.

    Args:
      params: A `Tensor`. The tensor from which to gather values.
      indices: A `Tensor`. Must be one of the following types: `int32`, `int64`.
        Index tensor.
      name: A name for the operation (optional).
      batch_dims: An integer or a scalar 'Tensor'. The number of batch dimensions.
      bad_indices_policy: A string. If `""` or `"DEFAULT"`, the default behavior
        is used (error on CPU and ignore on GPU). If `"IGNORE"`, the bad indices
        are ignored and 0 is stored in the corresponding output value. If
        `"ERROR"`, an error is raised. Accelerators generally don't support
        `"ERROR"`.

    Returns:
      A `Tensor`. Has the same type as `params`.
    """
    ...
def transpose(
    a: Tensor, perm: Sequence[int] | IntArray | None = None, conjugate: _bool = False, name: str = "transpose"
) -> Tensor:
    """
    Transposes `a`, where `a` is a Tensor.

    Permutes the dimensions according to the value of `perm`.

    The returned tensor's dimension `i` will correspond to the input dimension
    `perm[i]`. If `perm` is not given, it is set to (n-1...0), where n is the rank
    of the input tensor. Hence, by default, this operation performs a regular
    matrix transpose on 2-D input Tensors.

    If conjugate is `True` and `a.dtype` is either `complex64` or `complex128`
    then the values of `a` are conjugated and transposed.

    @compatibility(numpy)
    In `numpy` transposes are memory-efficient constant time operations as they
    simply return a new view of the same data with adjusted `strides`.

    TensorFlow does not support strides, so `transpose` returns a new tensor with
    the items permuted.
    @end_compatibility

    For example:

    >>> x = tf.constant([[1, 2, 3], [4, 5, 6]])
    >>> tf.transpose(x)
    <tf.Tensor: shape=(3, 2), dtype=int32, numpy=
    array([[1, 4],
           [2, 5],
           [3, 6]], dtype=int32)>

    Equivalently, you could call `tf.transpose(x, perm=[1, 0])`.

    If `x` is complex, setting conjugate=True gives the conjugate transpose:

    >>> x = tf.constant([[1 + 1j, 2 + 2j, 3 + 3j],
    ...                  [4 + 4j, 5 + 5j, 6 + 6j]])
    >>> tf.transpose(x, conjugate=True)
    <tf.Tensor: shape=(3, 2), dtype=complex128, numpy=
    array([[1.-1.j, 4.-4.j],
           [2.-2.j, 5.-5.j],
           [3.-3.j, 6.-6.j]])>

    'perm' is more useful for n-dimensional tensors where n > 2:

    >>> x = tf.constant([[[ 1,  2,  3],
    ...                   [ 4,  5,  6]],
    ...                  [[ 7,  8,  9],
    ...                   [10, 11, 12]]])

    As above, simply calling `tf.transpose` will default to `perm=[2,1,0]`.

    To take the transpose of the matrices in dimension-0 (such as when you are
    transposing matrices where 0 is the batch dimension), you would set
    `perm=[0,2,1]`.

    >>> tf.transpose(x, perm=[0, 2, 1])
    <tf.Tensor: shape=(2, 3, 2), dtype=int32, numpy=
    array([[[ 1,  4],
            [ 2,  5],
            [ 3,  6]],
            [[ 7, 10],
            [ 8, 11],
            [ 9, 12]]], dtype=int32)>

    Note: This has a shorthand `linalg.matrix_transpose`):

    Args:
      a: A `Tensor`.
      perm: A permutation of the dimensions of `a`.  This should be a vector.
      conjugate: Optional bool. Setting it to `True` is mathematically equivalent
        to tf.math.conj(tf.transpose(input)).
      name: A name for the operation (optional).

    Returns:
      A transposed `Tensor`.
    """
    ...
def clip_by_value(
    t: Tensor | IndexedSlices, clip_value_min: TensorCompatible, clip_value_max: TensorCompatible, name: str | None = None
) -> Tensor:
    """
    Clips tensor values to a specified min and max.

    Given a tensor `t`, this operation returns a tensor of the same type and
    shape as `t` with its values clipped to `clip_value_min` and `clip_value_max`.
    Any values less than `clip_value_min` are set to `clip_value_min`. Any values
    greater than `clip_value_max` are set to `clip_value_max`.

    Note: `clip_value_min` needs to be smaller or equal to `clip_value_max` for
    correct results.

    For example:

    Basic usage passes a scalar as the min and max value.

    >>> t = tf.constant([[-10., -1., 0.], [0., 2., 10.]])
    >>> t2 = tf.clip_by_value(t, clip_value_min=-1, clip_value_max=1)
    >>> t2.numpy()
    array([[-1., -1.,  0.],
           [ 0.,  1.,  1.]], dtype=float32)

    The min and max can be the same size as `t`, or broadcastable to that size.

    >>> t = tf.constant([[-1, 0., 10.], [-1, 0, 10]])
    >>> clip_min = [[2],[1]]
    >>> t3 = tf.clip_by_value(t, clip_value_min=clip_min, clip_value_max=100)
    >>> t3.numpy()
    array([[ 2.,  2., 10.],
           [ 1.,  1., 10.]], dtype=float32)

    Broadcasting fails, intentionally, if you would expand the dimensions of `t`

    >>> t = tf.constant([[-1, 0., 10.], [-1, 0, 10]])
    >>> clip_min = [[[2, 1]]] # Has a third axis
    >>> t4 = tf.clip_by_value(t, clip_value_min=clip_min, clip_value_max=100)
    Traceback (most recent call last):
    ...
    InvalidArgumentError: Incompatible shapes: [2,3] vs. [1,1,2]

    It throws a `TypeError` if you try to clip an `int` to a `float` value
    (`tf.cast` the input to `float` first).

    >>> t = tf.constant([[1, 2], [3, 4]], dtype=tf.int32)
    >>> t5 = tf.clip_by_value(t, clip_value_min=-3.1, clip_value_max=3.1)
    Traceback (most recent call last):
    ...
    TypeError: Cannot convert ...


    Args:
      t: A `Tensor` or `IndexedSlices`.
      clip_value_min: The minimum value to clip to. A scalar `Tensor` or one that
        is broadcastable to the shape of `t`.
      clip_value_max: The maximum value to clip to. A scalar `Tensor` or one that
        is broadcastable to the shape of `t`.
      name: A name for the operation (optional).

    Returns:
      A clipped `Tensor` or `IndexedSlices`.

    Raises:
      `tf.errors.InvalidArgumentError`: If the clip tensors would trigger array
        broadcasting that would make the returned tensor larger than the input.
      TypeError: If dtype of the input is `int32` and dtype of
        the `clip_value_min` or `clip_value_max` is `float32`
    """
    ...
def tile(input: RaggedTensorLike, multiples: Tensor | Sequence[int], name: str | None = None) -> Tensor:
    """
    Constructs a tensor by tiling a given tensor.

    This operation creates a new tensor by replicating `input` `multiples` times.
    The output tensor's i'th dimension has `input.dims(i) * multiples[i]` elements,
    and the values of `input` are replicated `multiples[i]` times along the 'i'th
    dimension. For example, tiling `[a b c d]` by `[2]` produces
    `[a b c d a b c d]`.

    >>> a = tf.constant([[1,2,3],[4,5,6]], tf.int32)
    >>> b = tf.constant([1,2], tf.int32)
    >>> tf.tile(a, b)
    <tf.Tensor: shape=(2, 6), dtype=int32, numpy=
    array([[1, 2, 3, 1, 2, 3],
           [4, 5, 6, 4, 5, 6]], dtype=int32)>
    >>> c = tf.constant([2,1], tf.int32)
    >>> tf.tile(a, c)
    <tf.Tensor: shape=(4, 3), dtype=int32, numpy=
    array([[1, 2, 3],
           [4, 5, 6],
           [1, 2, 3],
           [4, 5, 6]], dtype=int32)>
    >>> d = tf.constant([2,2], tf.int32)
    >>> tf.tile(a, d)
    <tf.Tensor: shape=(4, 6), dtype=int32, numpy=
    array([[1, 2, 3, 1, 2, 3],
           [4, 5, 6, 4, 5, 6],
           [1, 2, 3, 1, 2, 3],
           [4, 5, 6, 4, 5, 6]], dtype=int32)>

    Args:
      input: A `Tensor`. Can be of any rank.
      multiples: A `Tensor`. Must be one of the following types: `int32`, `int64`.
        1-D. Length must be the same as the number of dimensions in `input`
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `input`.
    """
    ...
def __getattr__(name: str): ...  # incomplete module

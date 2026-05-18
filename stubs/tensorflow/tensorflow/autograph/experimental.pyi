"""Public API for tf._api.v2.autograph.experimental namespace"""

from collections.abc import Callable, Iterable
from enum import Enum
from typing import ParamSpec, TypeVar, overload

import tensorflow as tf
from tensorflow._aliases import Integer

_Param = ParamSpec("_Param")
_RetType = TypeVar("_RetType")

class Feature(Enum):
    """
    This enumeration represents optional conversion options.

    These conversion options are experimental. They are subject to change without
    notice and offer no guarantees.

    _Example Usage_

    ```python
    optionals= tf.autograph.experimental.Feature.EQUALITY_OPERATORS
    @tf.function(experimental_autograph_options=optionals)
    def f(i):
      if i == 0:  # EQUALITY_OPERATORS allows the use of == here.
        tf.print('i is zero')
    ```

    Attributes:
      ALL: Enable all features.
      AUTO_CONTROL_DEPS: Insert of control dependencies in the generated code.
      ASSERT_STATEMENTS: Convert Tensor-dependent assert statements to tf.Assert.
      BUILTIN_FUNCTIONS: Convert builtin functions applied to Tensors to
        their TF counterparts.
      EQUALITY_OPERATORS: Whether to convert the equality operator ('==') to
        tf.math.equal.
      LISTS: Convert list idioms, like initializers, slices, append, etc.
      NAME_SCOPES: Insert name scopes that name ops according to context, like the
        function they were defined in.
    """
    ALL = "ALL"
    ASSERT_STATEMENTS = "ASSERT_STATEMENTS"
    AUTO_CONTROL_DEPS = "AUTO_CONTROL_DEPS"
    BUILTIN_FUNCTIONS = "BUILTIN_FUNCTIONS"
    EQUALITY_OPERATORS = "EQUALITY_OPERATORS"
    LISTS = "LISTS"
    NAME_SCOPES = "NAME_SCOPES"

@overload
def do_not_convert(func: Callable[_Param, _RetType]) -> Callable[_Param, _RetType]:
    """
    Decorator that suppresses the conversion of a function.

    Args:
      func: function to decorate.

    Returns:
      If `func` is not None, returns a `Callable` which is equivalent to
      `func`, but is not converted by AutoGraph.
      If `func` is None, returns a decorator that, when invoked with a
      single `func` argument, returns a `Callable` equivalent to the
      above case.
    """
    ...
@overload
def do_not_convert(func: None = None) -> Callable[[Callable[_Param, _RetType]], Callable[_Param, _RetType]]: ...

def set_loop_options(
    parallel_iterations: Integer = ...,
    swap_memory: bool = ...,
    maximum_iterations: Integer = ...,
    shape_invariants: Iterable[tuple[tf.Tensor, tf.TensorShape]] = ...,
) -> None:
    """
    Specifies additional arguments to be passed to the enclosing while_loop.

    The parameters apply to and only to the immediately enclosing loop. It only
    has effect if the loop is staged as a TF while_loop; otherwise the parameters
    have no effect.

    Usage:

      >>> @tf.function(autograph=True)
      ... def f():
      ...   n = 0
      ...   for i in tf.range(10):
      ...     tf.autograph.experimental.set_loop_options(maximum_iterations=3)
      ...     n += 1
      ...   return n

      >>> @tf.function(autograph=True)
      ... def f():
      ...   v = tf.constant((0,))
      ...   for i in tf.range(3):
      ...     tf.autograph.experimental.set_loop_options(
      ...         shape_invariants=[(v, tf.TensorShape([None]))]
      ...     )
      ...     v = tf.concat((v, [i]), 0)
      ...   return v

    Also see tf.while_loop.

    Args:
      parallel_iterations: The maximum number of iterations allowed to run in
          parallel at any given time. Note that this does not guarantee parallel
          execution.
      swap_memory: Whether to store intermediate values needed for
          gradients on the CPU instead of GPU.
      maximum_iterations: Allows limiting the total number of iterations executed
          by the loop.
      shape_invariants: Allows controlling the argument with the same name passed
          to tf.while_loop. Unlike tf.while_loop, this is a list of
          `(tensor, shape)` pairs.
    """
    ...

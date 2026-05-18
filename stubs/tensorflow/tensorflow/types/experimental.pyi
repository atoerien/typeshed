"""Public API for tf._api.v2.types.experimental namespace"""

import abc
from typing import Any, Generic, ParamSpec, TypeVar, overload

import tensorflow as tf
from tensorflow._aliases import ContainerGeneric

_P = ParamSpec("_P")
_R_co = TypeVar("_R_co", covariant=True)

class Callable(Generic[_P, _R_co], metaclass=abc.ABCMeta):
    """
    Base class for TF callables like those created by tf.function.

    Note: Callables are conceptually very similar to `tf.Operation`: a
    `tf.Operation` is a kind of callable.
    """
    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _R_co:
        """
        Executes this callable.

        This behaves like a regular op - in eager mode, it immediately starts
        execution, returning results. In graph mode, it creates ops which return
        symbolic TensorFlow values (like `tf.Tensor`, `tf.data.Dataset`,
        etc.). For example, `tf.function` callables typically generate a
        `tf.raw_ops.PartitionedCall` op, but not always - the
        exact operations being generated are an internal implementation detail.

        Args:
          *args: positional argument for this call
          **kwargs: keyword arguments for this call
        Returns:
          The execution results.
        """
        ...

class ConcreteFunction(Callable[_P, _R_co], metaclass=abc.ABCMeta):
    """
    Base class for differentiable graph functions.

    A `ConcreteFunction` encapsulates the original graph function definition with
    support for differentiability under `tf.GradientTape` contexts. In the
    process, it may generate new graph functions (using the original) to
    efficiently perform forwards and backwards passes.
    """
    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _R_co:
        """
        Executes this callable.

        This behaves like a regular op - in eager mode, it immediately starts
        execution, returning results. In graph mode, it creates ops which return
        symbolic TensorFlow values (like `tf.Tensor`, `tf.data.Dataset`,
        etc.). For example, `tf.function` callables typically generate a
        `tf.raw_ops.PartitionedCall` op, but not always - the
        exact operations being generated are an internal implementation detail.

        Args:
          *args: positional argument for this call
          **kwargs: keyword arguments for this call
        Returns:
          The execution results.
        """
        ...

class PolymorphicFunction(Callable[_P, _R_co], metaclass=abc.ABCMeta):
    """
    Base class for polymorphic graph functions.

    Graph functions are Python callable objects that dispatch calls to a
    TensorFlow graph. Polymorphic graph functions can be backed by multiple TF
    graphs, and automatically select the appropriate specialization based on the
    type of input they were called with. They may also create specializations on
    the fly if necessary, for example by tracing.

    Also see `tf.function`.
    """
    @overload
    @abc.abstractmethod
    def get_concrete_function(self, *args: _P.args, **kwargs: _P.kwargs) -> ConcreteFunction[_P, _R_co]:
        """
        Returns a `ConcreteFunction` specialized to input types.

        The arguments specified by `args` and `kwargs` follow normal function call
        rules. The returned `ConcreteFunction` has the same set of positional and
        keyword arguments as `self`, but their types are compatible to the types
        specified by `args` and `kwargs` (though not neccessarily equal).

        >>> @tf.function
        ... def f(x):
        ...   return x
        >>> f_concrete = f.get_concrete_function(tf.constant(1.0))
        >>> f_concrete = f.get_concrete_function(x=tf.constant(1.0))

        Unlike normal calls, `get_concrete_function` allow type specifiers instead
        of TensorFlow objects, so for example `tf.Tensor`s may be replaced with
        `tf.TensorSpec`s.

        >>> @tf.function
        ... def f(x):
        ...   return x
        >>> f_concrete = f.get_concrete_function(tf.TensorSpec([], tf.float64))

        If the function definition allows only one specialization, `args` and
        `kwargs` may be omitted altogether.

        >>> @tf.function(input_signature=[tf.TensorSpec(None, tf.float32)])
        ... def f(x):
        ...   return x
        >>> f_concrete = f.get_concrete_function()

        The returned `ConcreteFunction` can be called normally:

        >>> f_concrete(tf.constant(1.0))
        <tf.Tensor: shape=(), dtype=float32, numpy=1.0>
        >>> f_concrete(x=tf.constant(1.0))
        <tf.Tensor: shape=(), dtype=float32, numpy=1.0>

        Args:
          *args: inputs to specialize on.
          **kwargs: inputs to specialize on.

        Returns:
          A `ConcreteFunction`.
        """
        ...
    @overload
    @abc.abstractmethod
    def get_concrete_function(
        self, *args: ContainerGeneric[tf.TypeSpec[Any]], **kwargs: ContainerGeneric[tf.TypeSpec[Any]]
    ) -> ConcreteFunction[_P, _R_co]: ...

    def experimental_get_compiler_ir(self, *args, **kwargs): ...

GenericFunction = PolymorphicFunction

def __getattr__(name: str): ...  # incomplete module

"""Public API for tf._api.v2.autodiff namespace"""

from _typeshed import Incomplete
from builtins import bool as _bool
from collections.abc import Generator, Mapping, Sequence
from contextlib import contextmanager
from types import TracebackType
from typing import overload
from typing_extensions import Self

import tensorflow as tf
from tensorflow import Tensor, UnconnectedGradients, Variable
from tensorflow._aliases import ContainerGradients, ContainerTensors, ContainerTensorsLike, Gradients, TensorLike

class ForwardAccumulator:
    """
    Computes Jacobian-vector products ("JVP"s) using forward-mode autodiff.

    Compare to `tf.GradientTape` which computes vector-Jacobian products ("VJP"s)
    using reverse-mode autodiff (backprop). Reverse mode is more attractive when
    computing gradients of a scalar-valued function with respect to many inputs
    (e.g. a neural network with many parameters and a scalar loss). Forward mode
    works best on functions with many outputs and few inputs. Since it does not
    hold on to intermediate activations, it is much more memory efficient than
    backprop where it is applicable.

    Consider a simple linear regression:

    >>> x = tf.constant([[2.0, 3.0], [1.0, 4.0]])
    >>> targets = tf.constant([[1.], [-1.]])
    >>> dense = tf.keras.layers.Dense(1)
    >>> dense.build([None, 2])
    >>> with tf.autodiff.ForwardAccumulator(
    ...    primals=dense.kernel,
    ...    tangents=tf.constant([[1.], [0.]])) as acc:
    ...   loss = tf.reduce_sum((dense(x) - targets) ** 2.)
    >>> acc.jvp(loss)
    <tf.Tensor: shape=(), dtype=float32, numpy=...>

    The example has two variables containing parameters, `dense.kernel` (2
    parameters) and `dense.bias` (1 parameter). Considering the training data `x`
    as a constant, this means the Jacobian matrix for the function mapping from
    parameters to loss has one row and three columns.

    With forwardprop, we specify a length-three vector in advance which multiplies
    the Jacobian. The `primals` constructor argument is the parameter (a
    `tf.Tensor` or `tf.Variable`) we're specifying a vector for, and the
    `tangents` argument is the "vector" in Jacobian-vector product. If our goal is
    to compute the entire Jacobian matrix, forwardprop computes one column at a
    time while backprop computes one row at a time. Since the Jacobian in the
    linear regression example has only one row, backprop requires fewer
    invocations:

    >>> x = tf.constant([[2.0, 3.0], [1.0, 4.0]])
    >>> targets = tf.constant([[1.], [-1.]])
    >>> dense = tf.keras.layers.Dense(1)
    >>> dense.build([None, 2])
    >>> loss_fn = lambda: tf.reduce_sum((dense(x) - targets) ** 2.)
    >>> kernel_fprop = []
    >>> with tf.autodiff.ForwardAccumulator(
    ...     dense.kernel, tf.constant([[1.], [0.]])) as acc:
    ...   kernel_fprop.append(acc.jvp(loss_fn()))
    >>> with tf.autodiff.ForwardAccumulator(
    ...     dense.kernel, tf.constant([[0.], [1.]])) as acc:
    ...   kernel_fprop.append(acc.jvp(loss_fn()))
    >>> with tf.autodiff.ForwardAccumulator(dense.bias, tf.constant([1.])) as acc:
    ...   bias_fprop = acc.jvp(loss_fn())
    >>> with tf.GradientTape() as tape:
    ...   loss = loss_fn()
    >>> kernel_grad, bias_grad = tape.gradient(loss, (dense.kernel, dense.bias))
    >>> np.testing.assert_allclose(
    ...     kernel_grad, tf.stack(kernel_fprop)[:, tf.newaxis])
    >>> np.testing.assert_allclose(bias_grad, bias_fprop[tf.newaxis])

    Implicit in the `tape.gradient` call is a length-one vector which
    left-multiplies the Jacobian, a vector-Jacobian product.

    `ForwardAccumulator` maintains JVPs corresponding primal tensors it is
    watching, derived from the original `primals` specified in the constructor. As
    soon as a primal tensor is deleted, `ForwardAccumulator` deletes the
    corresponding JVP.

    `acc.jvp(x)` retrieves `acc`'s JVP corresponding to the primal tensor `x`. It
    does not perform any computation. `acc.jvp` calls can be repeated as long as
    `acc` is accessible, whether the context manager is active or not. New JVPs
    are only computed while the context manager is active.

    Note that `ForwardAccumulator`s are always applied in the order their context
    managers were entered, so inner accumulators will not see JVP computation from
    outer accumulators. Take higher-order JVPs from outer accumulators:

    >>> primal = tf.constant(1.1)
    >>> with tf.autodiff.ForwardAccumulator(primal, tf.constant(1.)) as outer:
    ...   with tf.autodiff.ForwardAccumulator(primal, tf.constant(1.)) as inner:
    ...     primal_out = primal ** tf.constant(3.5)
    >>> inner_jvp = inner.jvp(primal_out)
    >>> inner_jvp  # 3.5 * 1.1 ** 2.5
    <tf.Tensor: shape=(), dtype=float32, numpy=4.4417057>
    >>> outer.jvp(inner_jvp)  # 3.5 * 2.5 * 1.1 ** 1.5
    <tf.Tensor: shape=(), dtype=float32, numpy=10.094786>

    Reversing the collection in the last line to instead retrieve
    `inner.jvp(outer.jvp(primal_out))` will not work.

    Strict nesting also applies to combinations of `ForwardAccumulator` and
    `tf.GradientTape`. More deeply nested `GradientTape` objects will ignore the
    products of outer `ForwardAccumulator` objects. This allows (for example)
    memory-efficient forward-over-backward computation of Hessian-vector products,
    where the inner `GradientTape` would otherwise hold on to all intermediate
    JVPs:

    >>> v = tf.Variable([1., 2.])
    >>> with tf.autodiff.ForwardAccumulator(
    ...     v,
    ...     # The "vector" in Hessian-vector product.
    ...     tf.constant([1., 0.])) as acc:
    ...   with tf.GradientTape() as tape:
    ...     y = tf.reduce_sum(v ** 3.)
    ...   backward = tape.gradient(y, v)
    >>> backward  # gradient from backprop
    <tf.Tensor: shape=(2,), dtype=float32, numpy=array([ 3., 12.], dtype=float32)>
    >>> acc.jvp(backward)  # forward-over-backward Hessian-vector product
    <tf.Tensor: shape=(2,), dtype=float32, numpy=array([6., 0.], dtype=float32)>
    """
    def __init__(self, primals: Tensor, tangents: Tensor) -> None:
        """
        Specify tensors to watch and their Jacobian-vector products.

        Mathematically, `tangents` is a vector right-multiplying the Jacobian matrix
        (a Jacobian-vector product) for the function computed while this accumulator
        is active. Since JVPs are computed in forward mode as the computation
        happens, this vector must be supplied in advance.

        Listing a single tensor multiple times in `primals` raises an
        exception. Excluding a tensor from `primals` is equivalent to watching it
        with a tangent tensor of zeros.

        Args:
          primals: A tensor or nested structure of tensors to watch.
          tangents: A tensor or nested structure of tensors, with the same nesting
            structure as `primals`, with each element being a vector with the same
            size as the corresponding primal element.

        Raises:
          ValueError: If the same tensor or variable is specified multiple times in
            `primals`.
        """
        ...
    def jvp(
        self, primals: Tensor, unconnected_gradients: tf.UnconnectedGradients = tf.UnconnectedGradients.NONE  # noqa: Y011
    ) -> Tensor | None:
        """
        Fetches the Jacobian-vector product computed for `primals`.

        Note that this method performs no computation, and simply looks up a JVP
        that was already computed (unlike backprop using a `tf.GradientTape`, where
        the computation happens on the call to `tape.gradient`).

        Args:
          primals: A watched Tensor or structure of Tensors to fetch the JVPs for.
          unconnected_gradients: A value which can either hold 'none' or 'zero' and
            alters the value which will be returned if no JVP was computed for
            `primals`. The possible values and effects are detailed in
            'tf.UnconnectedGradients' and it defaults to 'none'.

        Returns:
          Tensors with the same shapes and dtypes as `primals`, or None if no JVP
          is available.
        """
        ...
    def __enter__(self) -> Self: ...
    def __exit__(self, typ: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None: ...

class GradientTape:
    def __init__(self, persistent: _bool = False, watch_accessed_variables: _bool = True) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, typ: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None: ...

    # Higher kinded types would be nice here and these overloads are a way to simulate some of them.
    @overload
    def gradient(
        self,
        target: ContainerTensors,
        sources: TensorLike,
        output_gradients: list[Tensor] | None = None,
        unconnected_gradients: UnconnectedGradients = ...,
    ) -> Gradients:
        """
        Computes the gradient using operations recorded in context of this tape.

        Note: Unless you set `persistent=True` a GradientTape can only be used to
        compute one set of gradients (or jacobians).

        In addition to Tensors, gradient also supports RaggedTensors. For example,

        >>> x = tf.ragged.constant([[1.0, 2.0], [3.0]])
        >>> with tf.GradientTape() as g:
        ...   g.watch(x)
        ...   y = x * x
        >>> g.gradient(y, x)
        <tf.RaggedTensor [[2.0, 4.0], [6.0]]>

        Args:
          target: a list or nested structure of Tensors or Variables or
            CompositeTensors to be differentiated.
          sources: a list or nested structure of Tensors or Variables or
            CompositeTensors. `target` will be differentiated against elements in
            `sources`.
          output_gradients: a list of gradients, one for each differentiable
            element of target. Defaults to None.
          unconnected_gradients: a value which can either hold 'none' or 'zero' and
            alters the value which will be returned if the target and sources are
            unconnected. The possible values and effects are detailed in
            'UnconnectedGradients' and it defaults to 'none'.

        Returns:
          a list or nested structure of Tensors (or IndexedSlices, or None, or
          CompositeTensor), one for each element in `sources`. Returned structure
          is the same as the structure of `sources`.

        Raises:
          RuntimeError: If called on a used, non-persistent tape.
          RuntimeError: If called inside the context of the tape.
          TypeError: If the target is a None object.
          ValueError: If the target is a variable or if unconnected gradients is
           called with an unknown value.
        """
        ...
    @overload
    def gradient(
        self,
        target: ContainerTensors,
        sources: Sequence[Tensor],
        output_gradients: list[Tensor] | None = None,
        unconnected_gradients: UnconnectedGradients = ...,
    ) -> list[Gradients]:
        """
        Computes the gradient using operations recorded in context of this tape.

        Note: Unless you set `persistent=True` a GradientTape can only be used to
        compute one set of gradients (or jacobians).

        In addition to Tensors, gradient also supports RaggedTensors. For example,

        >>> x = tf.ragged.constant([[1.0, 2.0], [3.0]])
        >>> with tf.GradientTape() as g:
        ...   g.watch(x)
        ...   y = x * x
        >>> g.gradient(y, x)
        <tf.RaggedTensor [[2.0, 4.0], [6.0]]>

        Args:
          target: a list or nested structure of Tensors or Variables or
            CompositeTensors to be differentiated.
          sources: a list or nested structure of Tensors or Variables or
            CompositeTensors. `target` will be differentiated against elements in
            `sources`.
          output_gradients: a list of gradients, one for each differentiable
            element of target. Defaults to None.
          unconnected_gradients: a value which can either hold 'none' or 'zero' and
            alters the value which will be returned if the target and sources are
            unconnected. The possible values and effects are detailed in
            'UnconnectedGradients' and it defaults to 'none'.

        Returns:
          a list or nested structure of Tensors (or IndexedSlices, or None, or
          CompositeTensor), one for each element in `sources`. Returned structure
          is the same as the structure of `sources`.

        Raises:
          RuntimeError: If called on a used, non-persistent tape.
          RuntimeError: If called inside the context of the tape.
          TypeError: If the target is a None object.
          ValueError: If the target is a variable or if unconnected gradients is
           called with an unknown value.
        """
        ...
    @overload
    def gradient(
        self,
        target: ContainerTensors,
        sources: Mapping[str, Tensor],
        output_gradients: list[Tensor] | None = None,
        unconnected_gradients: UnconnectedGradients = ...,
    ) -> dict[str, Gradients]:
        """
        Computes the gradient using operations recorded in context of this tape.

        Note: Unless you set `persistent=True` a GradientTape can only be used to
        compute one set of gradients (or jacobians).

        In addition to Tensors, gradient also supports RaggedTensors. For example,

        >>> x = tf.ragged.constant([[1.0, 2.0], [3.0]])
        >>> with tf.GradientTape() as g:
        ...   g.watch(x)
        ...   y = x * x
        >>> g.gradient(y, x)
        <tf.RaggedTensor [[2.0, 4.0], [6.0]]>

        Args:
          target: a list or nested structure of Tensors or Variables or
            CompositeTensors to be differentiated.
          sources: a list or nested structure of Tensors or Variables or
            CompositeTensors. `target` will be differentiated against elements in
            `sources`.
          output_gradients: a list of gradients, one for each differentiable
            element of target. Defaults to None.
          unconnected_gradients: a value which can either hold 'none' or 'zero' and
            alters the value which will be returned if the target and sources are
            unconnected. The possible values and effects are detailed in
            'UnconnectedGradients' and it defaults to 'none'.

        Returns:
          a list or nested structure of Tensors (or IndexedSlices, or None, or
          CompositeTensor), one for each element in `sources`. Returned structure
          is the same as the structure of `sources`.

        Raises:
          RuntimeError: If called on a used, non-persistent tape.
          RuntimeError: If called inside the context of the tape.
          TypeError: If the target is a None object.
          ValueError: If the target is a variable or if unconnected gradients is
           called with an unknown value.
        """
        ...
    @overload
    def gradient(
        self,
        target: ContainerTensors,
        sources: ContainerTensors,
        output_gradients: list[Tensor] | None = None,
        unconnected_gradients: UnconnectedGradients = ...,
    ) -> ContainerGradients: ...

    @contextmanager
    def stop_recording(self) -> Generator[None]:
        """
        Temporarily stops recording operations on this tape.

        Operations executed while this context manager is active will not be
        recorded on the tape. This is useful for reducing the memory used by tracing
        all computations.

        For example:

        >>> x = tf.constant(4.0)
        >>> with tf.GradientTape() as tape:
        ...   with tape.stop_recording():
        ...     y = x ** 2
        >>> dy_dx = tape.gradient(y, x)
        >>> print(dy_dx)
        None

        Yields:
          None
        Raises:
          RuntimeError: if the tape is not currently recording.
        """
        ...
    def reset(self) -> None:
        """
        Clears all information stored in this tape.

        Equivalent to exiting and reentering the tape context manager with a new
        tape. For example, the two following code blocks are equivalent:

        ```
        with tf.GradientTape() as t:
          loss = loss_fn()
        with tf.GradientTape() as t:
          loss += other_loss_fn()
        t.gradient(loss, ...)  # Only differentiates other_loss_fn, not loss_fn


        # The following is equivalent to the above
        with tf.GradientTape() as t:
          loss = loss_fn()
          t.reset()
          loss += other_loss_fn()
        t.gradient(loss, ...)  # Only differentiates other_loss_fn, not loss_fn
        ```

        This is useful if you don't want to exit the context manager for the tape,
        or can't because the desired reset point is inside a control flow construct:

        ```
        with tf.GradientTape() as t:
          loss = ...
          if loss > k:
            t.reset()
        ```
        """
        ...
    def watch(self, tensor: ContainerTensorsLike) -> None:
        """
        Ensures that `tensor` is being traced by this tape.

        Args:
          tensor: a Tensor/Variable or list of Tensors/Variables.

        Raises:
          ValueError: if it encounters something that is not a tensor.
        """
        ...
    def watched_variables(self) -> tuple[Variable, ...]:
        """Returns variables watched by this tape in order of construction."""
        ...
    def __getattr__(self, name: str) -> Incomplete: ...

"""Public API for tf._api.v2.debugging namespace"""

from tensorflow._aliases import FloatTensorCompatible

def assert_greater_equal(
    x: FloatTensorCompatible,
    y: FloatTensorCompatible,
    message: str | None = None,
    summarize: int | None = None,
    name: str | None = None,
) -> None:
    """
    Assert the condition `x >= y` holds element-wise.

    This Op checks that `x[i] >= y[i]` holds for every pair of (possibly
    broadcast) elements of `x` and `y`. If both `x` and `y` are empty, this is
    trivially satisfied.

    If `x` >= `y` does not hold, `message`, as well as the first `summarize`
    entries of `x` and `y` are printed, and `InvalidArgumentError` is raised.

    When using inside `tf.function`, this API takes effects during execution.
    It's recommended to use this API with `tf.control_dependencies` to
    ensure the correct execution order.

    In the following example, without `tf.control_dependencies`, errors may
    not be raised at all.
    Check `tf.control_dependencies` for more details.

    >>> def check_size(x):
    ...   with tf.control_dependencies([
    ...       tf.debugging.assert_greater_equal(tf.size(x), 9,
    ...                       message='Bad tensor size')]):
    ...     return x

    >>> check_size(tf.ones([2, 3], tf.float32))
    Traceback (most recent call last):
       ...
    InvalidArgumentError: ...

    Args:
      x:  Numeric `Tensor`.
      y:  Numeric `Tensor`, same dtype as and broadcastable to `x`.
      message: A string to prefix to the default message. (optional)
      summarize: Print this many entries of each tensor. (optional)
      name: A name for this operation (optional).  Defaults to "assert_greater_equal".

    Returns:
      Op that raises `InvalidArgumentError` if `x >= y` is False. This can
        be used with `tf.control_dependencies` inside of `tf.function`s to
        block followup computation until the check has executed.
      @compatibility(eager)
      returns None
      @end_compatibility

    Raises:
      InvalidArgumentError: if the check can be performed immediately and
        `x == y` is False. The check can be performed immediately during eager
        execution or if `x` and `y` are statically known.
    """
    ...
def __getattr__(name: str): ...  # incomplete module

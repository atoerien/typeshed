"""Public API for tf._api.v2.image namespace"""

import tensorflow as tf
from tensorflow._aliases import IntTensorCompatible, TensorCompatible

def random_crop(
    value: TensorCompatible, size: IntTensorCompatible, seed: int | None = None, name: str | None = None
) -> tf.Tensor:
    """
    Randomly crops a tensor to a given size.

    Slices a shape `size` portion out of `value` at a uniformly chosen offset.
    Requires `value.shape >= size`.

    If a dimension should not be cropped, pass the full size of that dimension.
    For example, RGB images can be cropped with
    `size = [crop_height, crop_width, 3]`.

    Example usage:

    >>> image = [[1, 2, 3], [4, 5, 6]]
    >>> result = tf.image.random_crop(value=image, size=(1, 3))
    >>> result.shape.as_list()
    [1, 3]

    For producing deterministic results given a `seed` value, use
    `tf.image.stateless_random_crop`. Unlike using the `seed` param with
    `tf.image.random_*` ops, `tf.image.stateless_random_*` ops guarantee the same
    results given the same seed independent of how many times the function is
    called, and independent of global seed settings (e.g. tf.random.set_seed).

    Args:
      value: Input tensor to crop.
      size: 1-D tensor with size the rank of `value`.
      seed: Python integer. Used to create a random seed. See
        `tf.random.set_seed`
        for behavior.
      name: A name for this operation (optional).

    Returns:
      A cropped tensor of the same rank as `value` and shape `size`.
    """
    ...
def __getattr__(name: str): ...  # incomplete module

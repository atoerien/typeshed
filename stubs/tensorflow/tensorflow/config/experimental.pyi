"""Public API for tf._api.v2.config.experimental namespace"""

import typing_extensions
from typing import TypedDict, type_check_only

from tensorflow.config import PhysicalDevice

@type_check_only
class _MemoryInfo(TypedDict):
    current: int
    peak: int

def get_memory_info(device: str) -> _MemoryInfo:
    """
    Get memory info for the chosen device, as a dict.

    This function returns a dict containing information about the device's memory
    usage. For example:

    >>> if tf.config.list_physical_devices('GPU'):
    ...   # Returns a dict in the form {'current': <current mem usage>,
    ...   #                             'peak': <peak mem usage>}
    ...   tf.config.experimental.get_memory_info('GPU:0')

    Currently returns the following keys:
      - `'current'`: The current memory used by the device, in bytes.
      - `'peak'`: The peak memory used by the device across the run of the
          program, in bytes. Can be reset with
          `tf.config.experimental.reset_memory_stats`.

    More keys may be added in the future, including device-specific keys.

    Currently only supports GPU and TPU. If called on a CPU device, an exception
    will be raised.

    For GPUs, TensorFlow will allocate all the memory by default, unless changed
    with `tf.config.experimental.set_memory_growth`. The dict specifies only the
    current and peak memory that TensorFlow is actually using, not the memory that
    TensorFlow has allocated on the GPU.

    Args:
      device: Device string to get the memory information for, e.g. `"GPU:0"`,
      `"TPU:0"`. See https://www.tensorflow.org/api_docs/python/tf/device for
        specifying device strings.

    Returns:
      A dict with keys `'current'` and `'peak'`, specifying the current and peak
      memory usage respectively.

    Raises:
      ValueError: No device found with the device name, like '"nonexistent"'.
      ValueError: Invalid device name, like '"GPU"', '"CPU:GPU"', '"CPU:"'.
      ValueError: Multiple devices matched with the device name.
      ValueError: Memory statistics not tracked, like '"CPU:0"'.
    """
    ...
def reset_memory_stats(device: str) -> None:
    """
    Resets the tracked memory stats for the chosen device.

    This function sets the tracked peak memory for a device to the device's
    current memory usage. This allows you to measure the peak memory usage for a
    specific part of your program. For example:

    >>> if tf.config.list_physical_devices('GPU'):
    ...   # Sets the peak memory to the current memory.
    ...   tf.config.experimental.reset_memory_stats('GPU:0')
    ...   # Creates the first peak memory usage.
    ...   x1 = tf.ones(1000 * 1000, dtype=tf.float64)
    ...   del x1 # Frees the memory referenced by `x1`.
    ...   peak1 = tf.config.experimental.get_memory_info('GPU:0')['peak']
    ...   # Sets the peak memory to the current memory again.
    ...   tf.config.experimental.reset_memory_stats('GPU:0')
    ...   # Creates the second peak memory usage.
    ...   x2 = tf.ones(1000 * 1000, dtype=tf.float32)
    ...   del x2
    ...   peak2 = tf.config.experimental.get_memory_info('GPU:0')['peak']
    ...   assert peak2 < peak1  # tf.float32 consumes less memory than tf.float64.

    Currently only supports GPU and TPU. If called on a CPU device, an exception
    will be raised.

    Args:
      device: Device string to reset the memory stats, e.g. `"GPU:0"`, `"TPU:0"`.
        See https://www.tensorflow.org/api_docs/python/tf/device for specifying
        device strings.

    Raises:
      ValueError: No device found with the device name, like '"nonexistent"'.
      ValueError: Invalid device name, like '"GPU"', '"CPU:GPU"', '"CPU:"'.
      ValueError: Multiple devices matched with the device name.
      ValueError: Memory statistics not tracked or clearing memory statistics not
        supported, like '"CPU:0"'.
    """
    ...
@typing_extensions.deprecated("This function is deprecated in favor of tf.config.experimental.get_memory_info")
def get_memory_usage(device: PhysicalDevice) -> int:
    """
    Get the current memory usage, in bytes, for the chosen device. (deprecated)

    Deprecated: THIS FUNCTION IS DEPRECATED. It will be removed in a future version.
    Instructions for updating:
    Use tf.config.experimental.get_memory_info(device)['current'] instead.

    This function is deprecated in favor of
    `tf.config.experimental.get_memory_info`. Calling this function is equivalent
    to calling `tf.config.experimental.get_memory_info()['current']`.

    See https://www.tensorflow.org/api_docs/python/tf/device for specifying device
    strings.

    For example:

    >>> gpu_devices = tf.config.list_physical_devices('GPU')
    >>> if gpu_devices:
    ...   tf.config.experimental.get_memory_usage('GPU:0')

    Does not work for CPU.

    For GPUs, TensorFlow will allocate all the memory by default, unless changed
    with `tf.config.experimental.set_memory_growth`. This function only returns
    the memory that TensorFlow is actually using, not the memory that TensorFlow
    has allocated on the GPU.

    Args:
      device: Device string to get the bytes in use for, e.g. `"GPU:0"`

    Returns:
      Total memory usage in bytes.

    Raises:
      ValueError: Non-existent or CPU device specified.
    """
    ...
def get_memory_growth(device: PhysicalDevice) -> bool:
    """
    Get if memory growth is enabled for a `PhysicalDevice`.

    If memory growth is enabled for a `PhysicalDevice`, the runtime initialization
    will not allocate all memory on the device.

    For example:

    >>> physical_devices = tf.config.list_physical_devices('GPU')
    >>> try:
    ...   tf.config.experimental.set_memory_growth(physical_devices[0], True)
    ...   assert tf.config.experimental.get_memory_growth(physical_devices[0])
    ... except:
    ...   # Invalid device or cannot modify virtual devices once initialized.
    ...   pass

    Args:
      device: `PhysicalDevice` to query

    Returns:
      A boolean indicating the memory growth setting for the `PhysicalDevice`.

    Raises:
      ValueError: Invalid `PhysicalDevice` specified.
    """
    ...
def set_memory_growth(device: PhysicalDevice, enable: bool) -> None:
    """
    Set if memory growth should be enabled for a `PhysicalDevice`.

    If memory growth is enabled for a `PhysicalDevice`, the runtime initialization
    will not allocate all memory on the device. Memory growth cannot be configured
    on a `PhysicalDevice` with virtual devices configured.

    For example:

    >>> physical_devices = tf.config.list_physical_devices('GPU')
    >>> try:
    ...   tf.config.experimental.set_memory_growth(physical_devices[0], True)
    ... except:
    ...   # Invalid device or cannot modify virtual devices once initialized.
    ...   pass

    Args:
      device: `PhysicalDevice` to configure
      enable: (Boolean) Whether to enable or disable memory growth

    Raises:
      ValueError: Invalid `PhysicalDevice` specified.
      RuntimeError: Runtime is already initialized.
    """
    ...
def __getattr__(name: str): ...  # incomplete module

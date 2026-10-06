"""Public API for tf._api.v2.config namespace"""

from typing import NamedTuple

from tensorflow.config import experimental as experimental

class PhysicalDevice(NamedTuple):
    """
    Abstraction for a locally visible physical device.

    TensorFlow can utilize various devices such as the CPU or multiple GPUs
    for computation. Before initializing a local device for use, the user can
    customize certain properties of the device such as it's visibility or memory
    configuration.

    Once a visible `tf.config.PhysicalDevice` is initialized one or more
    `tf.config.LogicalDevice` objects are created. Use
    `tf.config.set_visible_devices` to configure the visibility of a physical
    device and `tf.config.set_logical_device_configuration` to configure multiple
    `tf.config.LogicalDevice` objects for a `tf.config.PhysicalDevice`. This is
    useful when separation between models is needed or to simulate a multi-device
    environment.

    Fields:
      name: Unique identifier for device.
      device_type: String declaring the type of device such as "CPU" or "GPU".
    """
    name: str
    device_type: str

def list_physical_devices(device_type: str | None = None) -> list[PhysicalDevice]:
    """
    Return a list of physical devices visible to the host runtime.

    Physical devices are hardware devices present on the host machine. By default
    all discovered CPU and GPU devices are considered visible.

    This API allows querying the physical hardware resources prior to runtime
    initialization. Thus, giving an opportunity to call any additional
    configuration APIs. This is in contrast to `tf.config.list_logical_devices`,
    which triggers runtime initialization in order to list the configured devices.

    The following example lists the number of visible GPUs on the host.

    >>> physical_devices = tf.config.list_physical_devices('GPU')
    >>> print("Num GPUs:", len(physical_devices))
    Num GPUs: ...

    However, the number of GPUs available to the runtime may change during runtime
    initialization due to marking certain devices as not visible or configuring
    multiple logical devices.

    Args:
      device_type: (optional string) Only include devices matching this device
        type. For example "CPU" or "GPU".
      Notes: 1. If provided with any numerical values or any string other than
        supported device type such as 'CPU' it returns an empty list instead of
        raising error. 2. For default value it returns all physical devices

    Returns:
      List of discovered `tf.config.PhysicalDevice` objects
    """
    ...
def get_visible_devices(device_type: str | None = None) -> list[PhysicalDevice]:
    """
    Get the list of visible physical devices.

    Returns the list of `PhysicalDevice`s currently marked as visible to the
    runtime. A visible device will have at least one `LogicalDevice` associated
    with it once the runtime is initialized.

    The following example verifies all visible GPUs have been disabled:

    >>> physical_devices = tf.config.list_physical_devices('GPU')
    >>> try:
    ...   # Disable all GPUS
    ...   tf.config.set_visible_devices([], 'GPU')
    ...   visible_devices = tf.config.get_visible_devices()
    ...   for device in visible_devices:
    ...     assert device.device_type != 'GPU'
    ... except:
    ...   # Invalid device or cannot modify virtual devices once initialized.
    ...   pass

    Args:
      device_type: (optional string) Only include devices matching this device
        type. For example "CPU" or "GPU".

    Returns:
      List of visible `PhysicalDevice`s
    """
    ...
def set_visible_devices(devices: list[PhysicalDevice] | PhysicalDevice, device_type: str | None = None) -> None:
    """
    Set the list of visible devices.

    Specifies which `PhysicalDevice` objects are visible to the runtime.
    TensorFlow will only allocate memory and place operations on visible
    physical devices, as otherwise no `LogicalDevice` will be created on them.
    By default all discovered devices are marked as visible.

    The following example demonstrates disabling the first GPU on the machine.

    >>> physical_devices = tf.config.list_physical_devices('GPU')
    >>> try:
    ...   # Disable first GPU
    ...   tf.config.set_visible_devices(physical_devices[1:], 'GPU')
    ...   logical_devices = tf.config.list_logical_devices('GPU')
    ...   # Logical device was not created for first GPU
    ...   assert len(logical_devices) == len(physical_devices) - 1
    ... except:
    ...   # Invalid device or cannot modify virtual devices once initialized.
    ...   pass

    Args:
      devices: List of `PhysicalDevice`s to make visible
      device_type: (optional) Only configure devices matching this device type.
        For example "CPU" or "GPU". Other devices will be left unaltered.

    Raises:
      ValueError: If argument validation fails.
      RuntimeError: Runtime is already initialized.
    """
    ...
def __getattr__(name: str): ...  # incomplete module

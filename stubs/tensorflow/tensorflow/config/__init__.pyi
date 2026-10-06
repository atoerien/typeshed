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

def list_physical_devices(device_type: str | None = None) -> list[PhysicalDevice]: ...
def get_visible_devices(device_type: str | None = None) -> list[PhysicalDevice]: ...
def set_visible_devices(devices: list[PhysicalDevice] | PhysicalDevice, device_type: str | None = None) -> None: ...
def __getattr__(name: str): ...  # incomplete module

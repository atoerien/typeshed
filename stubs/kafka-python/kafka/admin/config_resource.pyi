from collections.abc import Mapping
from enum import IntEnum

class ConfigResourceType(IntEnum):
    """An enumerated type of config resources"""
    BROKER = 4
    TOPIC = 2

class ConfigResource:
    """
    A class for specifying config resources.
    Arguments:
        resource_type (ConfigResourceType): the type of kafka resource
        name (string): The name of the kafka resource
        configs ({key : value}): A  maps of config keys to values.
    """
    resource_type: ConfigResourceType
    name: str
    configs: Mapping[str, str] | None
    def __init__(self, resource_type: ConfigResourceType, name: str, configs: Mapping[str, str] | None = None) -> None: ...

"""
Configuration management mixin for KafkaAdminClient.

Also defines ConfigResource and ConfigResourceType data classes.
"""

from _typeshed import Incomplete
from collections.abc import Mapping, Sequence
from enum import IntEnum

from kafka.util import EnumHelper

class ConfigAdminMixin:
    """Mixin providing configuration management methods for KafkaAdminClient."""
    config: dict[Incomplete, Incomplete]
    def describe_configs(
        self,
        config_resources: Sequence[ConfigResource],
        include_synonyms: bool = False,
        config_filter: ConfigFilterType | str = "modified",
    ):
        """
        Fetch configuration parameters for one or more Kafka resources.

        Arguments:
            config_resources: An list of ConfigResource objects.
                Any keys in ConfigResource.configs dict will be used to filter the
                result. Setting the configs dict to None will get all values. An
                empty dict will get zero values (as per Kafka protocol).

        Keyword Arguments:
            include_synonyms (bool, optional): If True, return synonyms in response. Not
                supported by all versions. Default: False.
            config_filter (ConfigFilterType or str): Modified returns only keys that have
                non-default values; Dynamic returns all keys that can be modified with
                alter_configs; All returns all available keys. Default: Modified.

        Returns:
            dict of {resource_type (str): {resource_name (str): {config_key: {config data}}}}
        """
        ...
    def list_config_resources(self, resource_types: Sequence[ConfigResourceType | str] | None = None):
        """
        List config resources known to the cluster.

        Useful for discovering resource types that have no separate enumeration
        API (e.g. ``CLIENT_METRICS``, ``GROUP``). For ``TOPIC`` and ``BROKER``
        the data is also available via ``Metadata`` / cluster descriptions.

        Keyword Arguments:
            resource_types (list, optional): Filter by resource type. Each entry
                may be a :class:`ConfigResourceType` or its name (e.g. ``'TOPIC'``).
                If None or empty, the broker returns all supported types.
                Requires broker >= 4.1 for anything other than ``CLIENT_METRICS``.

        Returns:
            dict of {resource_type (str): [resource_name (str)]}
        """
        ...
    def alter_configs(
        self,
        config_resources: Sequence[ConfigResource],
        validate_only: bool = False,
        raise_on_unknown: bool = True,
        incremental: bool | None = None,
    ):
        """
        Alter configuration parameters of one or more Kafka resources.

        Arguments:
            config_resources: A list of ConfigResource objects. Each resource's
                ``configs`` must be a dict mapping config key to either
                ``(op, value)`` (where ``op`` is an :class:`AlterConfigOp`,
                its name, or its int value) or a bare value (interpreted as SET).
                For DELETE operations the value is ignored and sent as null.
                APPEND/SUBTRACT require broker >= 2.3. On older brokers only
                SET is supported; non-SET ops raise ValueError. On older brokers
                the client also fills in all other modified dynamic keys before
                submitting, since AlterConfigsRequest resets any omitted key to
                its default (be aware of the inherent race in that approach).
            validate_only (bool, optional): If True, changes are sent to broker for
                validation only. Changes will not be applied. Default: False
            raise_on_unknown (bool, optional): If True, raises ValueError if any
                config key is not recognized as a dynamic config for the resource.
            incremental (bool, optional): Set to True/False to force use of
                IncrementalAlterConfigs (True) or AlterConfigs (False).
                By Default, the admin client will use IncrementalAlterConfigs
                if supported by the broker, otherwise AlterConfigs.

        Returns:
            dict of {resource_type (str): {resource_name (str): Error/Result}}
        """
        ...
    def reset_configs(
        self,
        config_resources: Sequence[ConfigResource],
        validate_only: bool = False,
        raise_on_unknown: bool = True,
        incremental: bool | None = None,
    ):
        """
        Reset configuration parameters of one or more Kafka resources to defaults.

        On 2.3+ brokers, the client will submit an IncrementalAlterConfigsRequest
        with op DELETE for each resource/key. On older brokers, the client will
        use submit an AlterConfigsRequest and attempt to include all modified
        dynamic config values for each resource except the keys marked for reset.
        (AlterConfigsRequest will reset any missing config key to its default).

        Arguments:
            config_resources: A list of ConfigResource objects. Each resource's
                ``configs`` should be a list or dict of config keys to reset.
                (if dict, the values are ignored).

        Returns:
            dict of {resource_type (str): {resource_name (str): Error/Result}}
        """
        ...

class AlterConfigOp(EnumHelper, IntEnum):
    """An enumeration."""
    SET = 0
    DELETE = 1
    APPEND = 2
    SUBTRACT = 3

class ConfigFilterType(EnumHelper, IntEnum):
    """An enumeration."""
    ALL = 0
    DYNAMIC = 1
    MODIFIED = 2
    DEFAULT = 3
    STATIC = 4
    def should_skip(self, config_source: ConfigSourceType) -> bool: ...

class ConfigResourceType(EnumHelper, IntEnum):
    """An enumeration."""
    UNKNOWN = 0
    TOPIC = 2
    BROKER = 4
    BROKER_LOGGER = 8
    CLIENT_METRICS = 16
    GROUP = 32

class ConfigResource:
    """
    A class for specifying config resources.

    Arguments:
        resource_type (ConfigResourceType): the type of kafka resource
        name (string): The name of the kafka resource
        configs ([key] or {key : value}): config keys (values required to alter)
    """
    resource_type: ConfigResourceType
    name: str
    configs: Mapping[str, str] | None
    def __init__(self, resource_type: ConfigResourceType | str, name: str, configs: Mapping[str, str] | None = None) -> None: ...

class ConfigType(EnumHelper, IntEnum):
    """An enumeration."""
    UNKNOWN = 0
    BOOLEAN = 1
    STRING = 2
    INT = 3
    SHORT = 4
    LONG = 5
    DOUBLE = 6
    LIST = 7
    CLASS = 8
    PASSWORD = 9

class ConfigSourceType(EnumHelper, IntEnum):
    """An enumeration."""
    UNKNOWN = 0
    DYNAMIC_TOPIC_CONFIG = 1
    DYNAMIC_BROKER_CONFIG = 2
    DYNAMIC_DEFAULT_BROKER_CONFIG = 3
    STATIC_BROKER_CONFIG = 4
    DEFAULT_CONFIG = 5
    DYNAMIC_BROKER_LOGGER_CONFIG = 6
    DYNAMIC_CLIENT_METRICS_CONFIG = 7
    DYNAMIC_GROUP_CONFIG = 8
    def is_modified(self) -> bool: ...
    @classmethod
    def dynamic_for_resource_type(cls, resource_type: ConfigResourceType) -> ConfigSourceType: ...

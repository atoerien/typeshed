from _typeshed import Incomplete

from kafka.protocol.api_message import ApiMessage
from kafka.protocol.data_container import DataContainer

class AlterConfigsRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 is the same as version 0.
      // Version 2 enables flexible versions.
    """
    class AlterConfigsResource(DataContainer):
        class AlterableConfig(DataContainer):
            name: str
            value: str | None
            def __init__(self, *args, name: str = ..., value: str | None = ..., version: int | None = None, **kwargs) -> None: ...
            @property
            def version(self) -> int | None: ...
            def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
                """
                Use meta=True to include top-level version; meta='all' to include all internal versions
                json=False to return raw encoding; json=True (default) to convert values to be json-serializable
                """
                ...

        resource_type: int
        resource_name: str
        configs: list[AlterableConfig]
        def __init__(
            self,
            *args,
            resource_type: int = ...,
            resource_name: str = ...,
            configs: list[AlterableConfig] = ...,
            version: int | None = None,
            **kwargs,
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    resources: list[AlterConfigsResource]
    validate_only: bool
    def __init__(
        self, *args, resources: list[AlterConfigsResource] = ..., validate_only: bool = ..., version: int | None = None, **kwargs
    ) -> None: ...
    @property
    def version(self) -> int | None: ...
    def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
        """
        Use meta=True to include top-level version; meta='all' to include all internal versions
        json=False to return raw encoding; json=True (default) to convert values to be json-serializable
        """
        ...
    name: str
    type: str
    API_KEY: int
    API_VERSION: int
    valid_versions: tuple[int, int]
    min_version: int
    max_version: int
    @property
    def header(self): ...
    @classmethod
    def is_request(cls) -> bool: ...
    def expect_response(self) -> bool: ...
    def with_header(self, correlation_id: int = 0, client_id: str = "kafka-python") -> None: ...

class AlterConfigsResponse(ApiMessage):
    """
    Notes from json schema:
      // Starting in version 1, on quota violation brokers send out responses before throttling.
      // Version 2 enables flexible versions.
    """
    class AlterConfigsResourceResponse(DataContainer):
        error_code: int
        error_message: str | None
        resource_type: int
        resource_name: str
        def __init__(
            self,
            *args,
            error_code: int = ...,
            error_message: str | None = ...,
            resource_type: int = ...,
            resource_name: str = ...,
            version: int | None = None,
            **kwargs,
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    throttle_time_ms: int
    responses: list[AlterConfigsResourceResponse]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        responses: list[AlterConfigsResourceResponse] = ...,
        version: int | None = None,
        **kwargs,
    ) -> None: ...
    @property
    def version(self) -> int | None: ...
    def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
        """
        Use meta=True to include top-level version; meta='all' to include all internal versions
        json=False to return raw encoding; json=True (default) to convert values to be json-serializable
        """
        ...
    name: str
    type: str
    API_KEY: int
    API_VERSION: int
    valid_versions: tuple[int, int]
    min_version: int
    max_version: int
    @property
    def header(self): ...
    @classmethod
    def is_request(cls) -> bool: ...
    def expect_response(self) -> bool: ...
    def with_header(self, correlation_id: int = 0, client_id: str = "kafka-python") -> None: ...

class DescribeConfigsRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 0 was removed in Apache Kafka 4.0, Version 1 is the new baseline.
      // Version 1 adds IncludeSynonyms and removes IsDefault.
      // Version 2 is the same as version 1.
      // Version 4 enables flexible versions.
    """
    class DescribeConfigsResource(DataContainer):
        resource_type: int
        resource_name: str
        configuration_keys: list[str] | None
        def __init__(
            self,
            *args,
            resource_type: int = ...,
            resource_name: str = ...,
            configuration_keys: list[str] | None = ...,
            version: int | None = None,
            **kwargs,
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    resources: list[DescribeConfigsResource]
    include_synonyms: bool
    include_documentation: bool
    def __init__(
        self,
        *args,
        resources: list[DescribeConfigsResource] = ...,
        include_synonyms: bool = ...,
        include_documentation: bool = ...,
        version: int | None = None,
        **kwargs,
    ) -> None: ...
    @property
    def version(self) -> int | None: ...
    def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
        """
        Use meta=True to include top-level version; meta='all' to include all internal versions
        json=False to return raw encoding; json=True (default) to convert values to be json-serializable
        """
        ...
    name: str
    type: str
    API_KEY: int
    API_VERSION: int
    valid_versions: tuple[int, int]
    min_version: int
    max_version: int
    @property
    def header(self): ...
    @classmethod
    def is_request(cls) -> bool: ...
    def expect_response(self) -> bool: ...
    def with_header(self, correlation_id: int = 0, client_id: str = "kafka-python") -> None: ...

class DescribeConfigsResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 0 was removed in Apache Kafka 4.0, Version 1 is the new baseline.
      // Version 1 adds ConfigSource and the synonyms.
      // Starting in version 2, on quota violation, brokers send out responses before throttling.
      // Version 4 enables flexible versions.
    """
    class DescribeConfigsResult(DataContainer):
        class DescribeConfigsResourceResult(DataContainer):
            class DescribeConfigsSynonym(DataContainer):
                name: str
                value: str | None
                source: int
                def __init__(
                    self, *args, name: str = ..., value: str | None = ..., source: int = ..., version: int | None = None, **kwargs
                ) -> None: ...
                @property
                def version(self) -> int | None: ...
                def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
                    """
                    Use meta=True to include top-level version; meta='all' to include all internal versions
                    json=False to return raw encoding; json=True (default) to convert values to be json-serializable
                    """
                    ...

            name: str
            value: str | None
            read_only: bool
            config_source: int
            is_default: bool
            is_sensitive: bool
            synonyms: list[DescribeConfigsSynonym]
            config_type: int
            documentation: str | None
            def __init__(
                self,
                *args,
                name: str = ...,
                value: str | None = ...,
                read_only: bool = ...,
                config_source: int = ...,
                is_default: bool = ...,
                is_sensitive: bool = ...,
                synonyms: list[DescribeConfigsSynonym] = ...,
                config_type: int = ...,
                documentation: str | None = ...,
                version: int | None = None,
                **kwargs,
            ) -> None: ...
            @property
            def version(self) -> int | None: ...
            def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
                """
                Use meta=True to include top-level version; meta='all' to include all internal versions
                json=False to return raw encoding; json=True (default) to convert values to be json-serializable
                """
                ...

        error_code: int
        error_message: str | None
        resource_type: int
        resource_name: str
        configs: list[DescribeConfigsResourceResult]
        def __init__(
            self,
            *args,
            error_code: int = ...,
            error_message: str | None = ...,
            resource_type: int = ...,
            resource_name: str = ...,
            configs: list[DescribeConfigsResourceResult] = ...,
            version: int | None = None,
            **kwargs,
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    throttle_time_ms: int
    results: list[DescribeConfigsResult]
    def __init__(
        self, *args, throttle_time_ms: int = ..., results: list[DescribeConfigsResult] = ..., version: int | None = None, **kwargs
    ) -> None: ...
    @property
    def version(self) -> int | None: ...
    def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
        """
        Use meta=True to include top-level version; meta='all' to include all internal versions
        json=False to return raw encoding; json=True (default) to convert values to be json-serializable
        """
        ...
    name: str
    type: str
    API_KEY: int
    API_VERSION: int
    valid_versions: tuple[int, int]
    min_version: int
    max_version: int
    @property
    def header(self): ...
    @classmethod
    def is_request(cls) -> bool: ...
    def expect_response(self) -> bool: ...
    def with_header(self, correlation_id: int = 0, client_id: str = "kafka-python") -> None: ...

class IncrementalAlterConfigsRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 is the first flexible version.
    """
    class AlterConfigsResource(DataContainer):
        class AlterableConfig(DataContainer):
            name: str
            config_operation: int
            value: str | None
            def __init__(
                self,
                *args,
                name: str = ...,
                config_operation: int = ...,
                value: str | None = ...,
                version: int | None = None,
                **kwargs,
            ) -> None: ...
            @property
            def version(self) -> int | None: ...
            def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
                """
                Use meta=True to include top-level version; meta='all' to include all internal versions
                json=False to return raw encoding; json=True (default) to convert values to be json-serializable
                """
                ...

        resource_type: int
        resource_name: str
        configs: list[AlterableConfig]
        def __init__(
            self,
            *args,
            resource_type: int = ...,
            resource_name: str = ...,
            configs: list[AlterableConfig] = ...,
            version: int | None = None,
            **kwargs,
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    resources: list[AlterConfigsResource]
    validate_only: bool
    def __init__(
        self, *args, resources: list[AlterConfigsResource] = ..., validate_only: bool = ..., version: int | None = None, **kwargs
    ) -> None: ...
    @property
    def version(self) -> int | None: ...
    def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
        """
        Use meta=True to include top-level version; meta='all' to include all internal versions
        json=False to return raw encoding; json=True (default) to convert values to be json-serializable
        """
        ...
    name: str
    type: str
    API_KEY: int
    API_VERSION: int
    valid_versions: tuple[int, int]
    min_version: int
    max_version: int
    @property
    def header(self): ...
    @classmethod
    def is_request(cls) -> bool: ...
    def expect_response(self) -> bool: ...
    def with_header(self, correlation_id: int = 0, client_id: str = "kafka-python") -> None: ...

class IncrementalAlterConfigsResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 1 is the first flexible version.
    """
    class AlterConfigsResourceResponse(DataContainer):
        error_code: int
        error_message: str | None
        resource_type: int
        resource_name: str
        def __init__(
            self,
            *args,
            error_code: int = ...,
            error_message: str | None = ...,
            resource_type: int = ...,
            resource_name: str = ...,
            version: int | None = None,
            **kwargs,
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    throttle_time_ms: int
    responses: list[AlterConfigsResourceResponse]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        responses: list[AlterConfigsResourceResponse] = ...,
        version: int | None = None,
        **kwargs,
    ) -> None: ...
    @property
    def version(self) -> int | None: ...
    def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
        """
        Use meta=True to include top-level version; meta='all' to include all internal versions
        json=False to return raw encoding; json=True (default) to convert values to be json-serializable
        """
        ...
    name: str
    type: str
    API_KEY: int
    API_VERSION: int
    valid_versions: tuple[int, int]
    min_version: int
    max_version: int
    @property
    def header(self): ...
    @classmethod
    def is_request(cls) -> bool: ...
    def expect_response(self) -> bool: ...
    def with_header(self, correlation_id: int = 0, client_id: str = "kafka-python") -> None: ...

class ListConfigResourcesRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 0 is used as ListClientMetricsResourcesRequest which only lists client metrics resources.
      // Version 1 adds ResourceTypes field (KIP-1142). If there is no specified ResourceTypes, it should return all configuration resources.
    """
    resource_types: list[int]
    def __init__(self, *args, resource_types: list[int] = ..., version: int | None = None, **kwargs) -> None: ...
    @property
    def version(self) -> int | None: ...
    def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
        """
        Use meta=True to include top-level version; meta='all' to include all internal versions
        json=False to return raw encoding; json=True (default) to convert values to be json-serializable
        """
        ...
    name: str
    type: str
    API_KEY: int
    API_VERSION: int
    valid_versions: tuple[int, int]
    min_version: int
    max_version: int
    @property
    def header(self): ...
    @classmethod
    def is_request(cls) -> bool: ...
    def expect_response(self) -> bool: ...
    def with_header(self, correlation_id: int = 0, client_id: str = "kafka-python") -> None: ...

class ListConfigResourcesResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 0 is used as ListClientMetricsResourcesResponse which returns all client metrics resources.
      // Version 1 adds ResourceType to ConfigResources (KIP-1142).
    """
    class ConfigResource(DataContainer):
        resource_name: str
        resource_type: int
        def __init__(
            self, *args, resource_name: str = ..., resource_type: int = ..., version: int | None = None, **kwargs
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    throttle_time_ms: int
    error_code: int
    config_resources: list[ConfigResource]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        error_code: int = ...,
        config_resources: list[ConfigResource] = ...,
        version: int | None = None,
        **kwargs,
    ) -> None: ...
    @property
    def version(self) -> int | None: ...
    def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
        """
        Use meta=True to include top-level version; meta='all' to include all internal versions
        json=False to return raw encoding; json=True (default) to convert values to be json-serializable
        """
        ...
    name: str
    type: str
    API_KEY: int
    API_VERSION: int
    valid_versions: tuple[int, int]
    min_version: int
    max_version: int
    @property
    def header(self): ...
    @classmethod
    def is_request(cls) -> bool: ...
    def expect_response(self) -> bool: ...
    def with_header(self, correlation_id: int = 0, client_id: str = "kafka-python") -> None: ...

__all__ = [
    "AlterConfigsRequest",
    "AlterConfigsResponse",
    "DescribeConfigsRequest",
    "DescribeConfigsResponse",
    "IncrementalAlterConfigsRequest",
    "IncrementalAlterConfigsResponse",
    "ListConfigResourcesRequest",
    "ListConfigResourcesResponse",
]

from _typeshed import Incomplete

from kafka.protocol.api_message import ApiMessage
from kafka.protocol.data_container import DataContainer

class ApiVersionsRequest(ApiMessage):
    """
    Notes from json schema:
      // Versions 0 through 2 of ApiVersionsRequest are the same.
      //
      // Version 3 is the first flexible version and adds ClientSoftwareName and ClientSoftwareVersion.
      //
      // Version 4 fixes KAFKA-17011, which blocked SupportedFeatures.MinVersion in the response from being 0.
    """
    client_software_name: str
    client_software_version: str
    def __init__(
        self, *args, client_software_name: str = ..., client_software_version: str = ..., version: int | None = None, **kwargs
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

class ApiVersionsResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 1 adds throttle time to the response.
      //
      // Starting in version 2, on quota violation, brokers send out responses before throttling.
      //
      // Version 3 is the first flexible version. Tagged fields are only supported in the body but
      // not in the header. The length of the header must not change in order to guarantee the
      // backward compatibility.
      //
      // Starting from Apache Kafka 2.4 (KIP-511), ApiKeys field is populated with the supported
      // versions of the ApiVersionsRequest when an UNSUPPORTED_VERSION error is returned.
      //
      // Version 4 fixes KAFKA-17011, which blocked SupportedFeatures.MinVersion from being 0.
    """
    class ApiVersion(DataContainer):
        api_key: int
        min_version: int
        max_version: int
        def __init__(
            self, *args, api_key: int = ..., min_version: int = ..., max_version: int = ..., version: int | None = None, **kwargs
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    class SupportedFeatureKey(DataContainer):
        name: str
        min_version: int
        max_version: int
        def __init__(
            self, *args, name: str = ..., min_version: int = ..., max_version: int = ..., version: int | None = None, **kwargs
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    class FinalizedFeatureKey(DataContainer):
        name: str
        max_version_level: int
        min_version_level: int
        def __init__(
            self,
            *args,
            name: str = ...,
            max_version_level: int = ...,
            min_version_level: int = ...,
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
    api_keys: list[ApiVersion]
    throttle_time_ms: int
    supported_features: list[SupportedFeatureKey]
    finalized_features_epoch: int
    finalized_features: list[FinalizedFeatureKey]
    zk_migration_ready: bool
    def __init__(
        self,
        *args,
        error_code: int = ...,
        api_keys: list[ApiVersion] = ...,
        throttle_time_ms: int = ...,
        supported_features: list[SupportedFeatureKey] = ...,
        finalized_features_epoch: int = ...,
        finalized_features: list[FinalizedFeatureKey] = ...,
        zk_migration_ready: bool = ...,
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
    @classmethod
    def parse_header(cls, data, version=None): ...
    def encode_header(self, flexible: bool = False): ...
    @classmethod
    def decode(cls, data, version=None, header: bool = False, framed: bool = False): ...  # type: ignore[override]

__all__ = ["ApiVersionsRequest", "ApiVersionsResponse"]

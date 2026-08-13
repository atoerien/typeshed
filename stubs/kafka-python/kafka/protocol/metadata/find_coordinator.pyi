from _typeshed import Incomplete
from enum import IntEnum

from kafka.protocol.api_message import ApiMessage
from kafka.protocol.data_container import DataContainer
from kafka.util import EnumHelper

class CoordinatorType(EnumHelper, IntEnum):
    """An enumeration."""
    GROUP = 0
    TRANSACTION = 1
    SHARE = 2

class FindCoordinatorRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 adds KeyType.
      //
      // Version 2 is the same as version 1.
      //
      // Version 3 is the first flexible version.
      //
      // Version 4 adds support for batching via CoordinatorKeys (KIP-699)
      //
      // Version 5 adds support for new error code TRANSACTION_ABORTABLE (KIP-890).
      //
      // Version 6 adds support for share groups (KIP-932).
      // For key type SHARE (2), the coordinator key format is "groupId:topicId:partition".
    """
    key: str
    key_type: int
    coordinator_keys: list[str]
    def __init__(
        self, *args, key: str = ..., key_type: int = ..., coordinator_keys: list[str] = ..., version: int | None = None, **kwargs
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

class FindCoordinatorResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 1 adds throttle time and error messages.
      //
      // Starting in version 2, on quota violation, brokers send out responses before throttling.
      //
      // Version 3 is the first flexible version.
      //
      // Version 4 adds support for batching via Coordinators (KIP-699)
      //
      // Version 5 adds support for new error code TRANSACTION_ABORTABLE (KIP-890).
      //
      // Version 6 adds support for share groups (KIP-932).
    """
    class Coordinator(DataContainer):
        key: str
        node_id: int
        host: str
        port: int
        error_code: int
        error_message: str | None
        def __init__(
            self,
            *args,
            key: str = ...,
            node_id: int = ...,
            host: str = ...,
            port: int = ...,
            error_code: int = ...,
            error_message: str | None = ...,
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
    error_code: int
    error_message: str | None
    node_id: int
    host: str
    port: int
    coordinators: list[Coordinator]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        error_code: int = ...,
        error_message: str | None = ...,
        node_id: int = ...,
        host: str = ...,
        port: int = ...,
        coordinators: list[Coordinator] = ...,
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

__all__ = ["CoordinatorType", "FindCoordinatorRequest", "FindCoordinatorResponse"]

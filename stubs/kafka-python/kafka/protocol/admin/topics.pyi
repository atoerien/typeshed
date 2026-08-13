import uuid
from _typeshed import Incomplete
from enum import IntEnum

from kafka.protocol.api_message import ApiMessage
from kafka.protocol.data_container import DataContainer

class CreateTopicsRequest(ApiMessage):
    """
    Notes from json schema:
      // Versions 0-1 were removed in Apache Kafka 4.0, Version 2 is the new baseline.
      //
      // Version 1 adds validateOnly.
      //
      // Version 4 makes partitions/replicationFactor optional even when assignments are not present (KIP-464)
      //
      // Version 5 is the first flexible version.
      // Version 5 also returns topic configs in the response (KIP-525).
      //
      // Version 6 is identical to version 5 but may return a THROTTLING_QUOTA_EXCEEDED error
      // in the response if the topics creation is throttled (KIP-599).
      //
      // Version 7 is the same as version 6.
    """
    class CreatableTopic(DataContainer):
        class CreatableReplicaAssignment(DataContainer):
            partition_index: int
            broker_ids: list[int]
            def __init__(
                self, *args, partition_index: int = ..., broker_ids: list[int] = ..., version: int | None = None, **kwargs
            ) -> None: ...
            @property
            def version(self) -> int | None: ...
            def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
                """
                Use meta=True to include top-level version; meta='all' to include all internal versions
                json=False to return raw encoding; json=True (default) to convert values to be json-serializable
                """
                ...

        class CreatableTopicConfig(DataContainer):
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

        name: str
        num_partitions: int
        replication_factor: int
        assignments: list[CreatableReplicaAssignment]
        configs: list[CreatableTopicConfig]
        def __init__(
            self,
            *args,
            name: str = ...,
            num_partitions: int = ...,
            replication_factor: int = ...,
            assignments: list[CreatableReplicaAssignment] = ...,
            configs: list[CreatableTopicConfig] = ...,
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

    topics: list[CreatableTopic]
    timeout_ms: int
    validate_only: bool
    def __init__(
        self,
        *args,
        topics: list[CreatableTopic] = ...,
        timeout_ms: int = ...,
        validate_only: bool = ...,
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

class CreateTopicsResponse(ApiMessage):
    """
    Notes from json schema:
      // Versions 0-1 were removed in Apache Kafka 4.0, Version 2 is the new baseline.
      //
      // Version 1 adds a per-topic error message string.
      //
      // Version 2 adds the throttle time.
      //
      // Starting in version 3, on quota violation, brokers send out responses before throttling.
      //
      // Version 4 makes partitions/replicationFactor optional even when assignments are not present (KIP-464).
      //
      // Version 5 is the first flexible version.
      // Version 5 also returns topic configs in the response (KIP-525).
      //
      // Version 6 is identical to version 5 but may return a THROTTLING_QUOTA_EXCEEDED error
      // in the response if the topics creation is throttled (KIP-599).
      //
      // Version 7 returns the topic ID of the newly created topic if creation is successful.
    """
    class CreatableTopicResult(DataContainer):
        class CreatableTopicConfigs(DataContainer):
            name: str
            value: str | None
            read_only: bool
            config_source: int
            is_sensitive: bool
            def __init__(
                self,
                *args,
                name: str = ...,
                value: str | None = ...,
                read_only: bool = ...,
                config_source: int = ...,
                is_sensitive: bool = ...,
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
        topic_id: uuid.UUID
        error_code: int
        error_message: str | None
        topic_config_error_code: int
        num_partitions: int
        replication_factor: int
        configs: list[CreatableTopicConfigs] | None
        def __init__(
            self,
            *args,
            name: str = ...,
            topic_id: uuid.UUID = ...,
            error_code: int = ...,
            error_message: str | None = ...,
            topic_config_error_code: int = ...,
            num_partitions: int = ...,
            replication_factor: int = ...,
            configs: list[CreatableTopicConfigs] | None = ...,
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
    topics: list[CreatableTopicResult]
    def __init__(
        self, *args, throttle_time_ms: int = ..., topics: list[CreatableTopicResult] = ..., version: int | None = None, **kwargs
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

class DeleteTopicsRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 0 was removed in Apache Kafka 4.0, Version 1 is the new baseline.
      // Versions 0, 1, 2, and 3 are the same.
      //
      // Version 4 is the first flexible version.
      //
      // Version 5 adds ErrorMessage in the response and may return a THROTTLING_QUOTA_EXCEEDED error
      // in the response if the topics deletion is throttled (KIP-599).
      //
      // Version 6 reorganizes topics, adds topic IDs and allows topic names to be null.
    """
    class DeleteTopicState(DataContainer):
        name: str | None
        topic_id: uuid.UUID
        def __init__(
            self, *args, name: str | None = ..., topic_id: uuid.UUID = ..., version: int | None = None, **kwargs
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    topics: list[DeleteTopicState]
    topic_names: list[str]
    timeout_ms: int
    def __init__(
        self,
        *args,
        topics: list[DeleteTopicState] = ...,
        topic_names: list[str] = ...,
        timeout_ms: int = ...,
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
    def encode(self, version=None, header=False, framed=False): ...

class DeleteTopicsResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 0 was removed in Apache Kafka 4.0, Version 1 is the new baseline.
      //
      // Version 1 adds the throttle time.
      //
      // Starting in version 2, on quota violation, brokers send out responses before throttling.
      //
      // Starting in version 3, a TOPIC_DELETION_DISABLED error code may be returned.
      //
      // Version 4 is the first flexible version.
      //
      // Version 5 adds ErrorMessage in the response and may return a THROTTLING_QUOTA_EXCEEDED error
      // in the response if the topics deletion is throttled (KIP-599).
      //
      // Version 6 adds topic ID to responses. An UNSUPPORTED_VERSION error code will be returned when attempting to
      // delete using topic IDs when IBP < 2.8. UNKNOWN_TOPIC_ID error code will be returned when IBP is at least 2.8, but
      // the topic ID was not found.
    """
    class DeletableTopicResult(DataContainer):
        name: str | None
        topic_id: uuid.UUID
        error_code: int
        error_message: str | None
        def __init__(
            self,
            *args,
            name: str | None = ...,
            topic_id: uuid.UUID = ...,
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
    responses: list[DeletableTopicResult]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        responses: list[DeletableTopicResult] = ...,
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

class CreatePartitionsRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 is the same as version 0.
      //
      // Version 2 adds flexible version support
      //
      // Version 3 is identical to version 2 but may return a THROTTLING_QUOTA_EXCEEDED error
      // in the response if the partitions creation is throttled (KIP-599).
    """
    class CreatePartitionsTopic(DataContainer):
        class CreatePartitionsAssignment(DataContainer):
            broker_ids: list[int]
            def __init__(self, *args, broker_ids: list[int] = ..., version: int | None = None, **kwargs) -> None: ...
            @property
            def version(self) -> int | None: ...
            def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
                """
                Use meta=True to include top-level version; meta='all' to include all internal versions
                json=False to return raw encoding; json=True (default) to convert values to be json-serializable
                """
                ...

        name: str
        count: int
        assignments: list[CreatePartitionsAssignment] | None
        def __init__(
            self,
            *args,
            name: str = ...,
            count: int = ...,
            assignments: list[CreatePartitionsAssignment] | None = ...,
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

    topics: list[CreatePartitionsTopic]
    timeout_ms: int
    validate_only: bool
    def __init__(
        self,
        *args,
        topics: list[CreatePartitionsTopic] = ...,
        timeout_ms: int = ...,
        validate_only: bool = ...,
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

class CreatePartitionsResponse(ApiMessage):
    """
    Notes from json schema:
      // Starting in version 1, on quota violation, brokers send out responses before throttling.
      //
      // Version 2 adds flexible version support
      //
      // Version 3 is identical to version 2 but may return a THROTTLING_QUOTA_EXCEEDED error
      // in the response if the partitions creation is throttled (KIP-599).
    """
    class CreatePartitionsTopicResult(DataContainer):
        name: str
        error_code: int
        error_message: str | None
        def __init__(
            self,
            *args,
            name: str = ...,
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
    results: list[CreatePartitionsTopicResult]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        results: list[CreatePartitionsTopicResult] = ...,
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

class AlterPartitionReassignmentsRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 adds the ability to allow/disallow changing the replication factor as part of the request.
    """
    class ReassignableTopic(DataContainer):
        class ReassignablePartition(DataContainer):
            partition_index: int
            replicas: list[int] | None
            def __init__(
                self, *args, partition_index: int = ..., replicas: list[int] | None = ..., version: int | None = None, **kwargs
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
        partitions: list[ReassignablePartition]
        def __init__(
            self, *args, name: str = ..., partitions: list[ReassignablePartition] = ..., version: int | None = None, **kwargs
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    timeout_ms: int
    allow_replication_factor_change: bool
    topics: list[ReassignableTopic]
    def __init__(
        self,
        *args,
        timeout_ms: int = ...,
        allow_replication_factor_change: bool = ...,
        topics: list[ReassignableTopic] = ...,
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

class AlterPartitionReassignmentsResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 1 adds the ability to allow/disallow changing the replication factor as part of the request.
    """
    class ReassignableTopicResponse(DataContainer):
        class ReassignablePartitionResponse(DataContainer):
            partition_index: int
            error_code: int
            error_message: str | None
            def __init__(
                self,
                *args,
                partition_index: int = ...,
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

        name: str
        partitions: list[ReassignablePartitionResponse]
        def __init__(
            self,
            *args,
            name: str = ...,
            partitions: list[ReassignablePartitionResponse] = ...,
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
    allow_replication_factor_change: bool
    error_code: int
    error_message: str | None
    responses: list[ReassignableTopicResponse]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        allow_replication_factor_change: bool = ...,
        error_code: int = ...,
        error_message: str | None = ...,
        responses: list[ReassignableTopicResponse] = ...,
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

class ListPartitionReassignmentsRequest(ApiMessage):
    class ListPartitionReassignmentsTopics(DataContainer):
        name: str
        partition_indexes: list[int]
        def __init__(
            self, *args, name: str = ..., partition_indexes: list[int] = ..., version: int | None = None, **kwargs
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    timeout_ms: int
    topics: list[ListPartitionReassignmentsTopics] | None
    def __init__(
        self,
        *args,
        timeout_ms: int = ...,
        topics: list[ListPartitionReassignmentsTopics] | None = ...,
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

class ListPartitionReassignmentsResponse(ApiMessage):
    class OngoingTopicReassignment(DataContainer):
        class OngoingPartitionReassignment(DataContainer):
            partition_index: int
            replicas: list[int]
            adding_replicas: list[int]
            removing_replicas: list[int]
            def __init__(
                self,
                *args,
                partition_index: int = ...,
                replicas: list[int] = ...,
                adding_replicas: list[int] = ...,
                removing_replicas: list[int] = ...,
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
        partitions: list[OngoingPartitionReassignment]
        def __init__(
            self,
            *args,
            name: str = ...,
            partitions: list[OngoingPartitionReassignment] = ...,
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
    topics: list[OngoingTopicReassignment]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        error_code: int = ...,
        error_message: str | None = ...,
        topics: list[OngoingTopicReassignment] = ...,
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

class DescribeTopicPartitionsRequest(ApiMessage):
    class TopicRequest(DataContainer):
        name: str
        def __init__(self, *args, name: str = ..., version: int | None = None, **kwargs) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    class Cursor(DataContainer):
        topic_name: str
        partition_index: int
        def __init__(
            self, *args, topic_name: str = ..., partition_index: int = ..., version: int | None = None, **kwargs
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    topics: list[TopicRequest]
    response_partition_limit: int
    cursor: Cursor | None
    def __init__(
        self,
        *args,
        topics: list[TopicRequest] = ...,
        response_partition_limit: int = ...,
        cursor: Cursor | None = ...,
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

class DescribeTopicPartitionsResponse(ApiMessage):
    class DescribeTopicPartitionsResponseTopic(DataContainer):
        class DescribeTopicPartitionsResponsePartition(DataContainer):
            error_code: int
            partition_index: int
            leader_id: int
            leader_epoch: int
            replica_nodes: list[int]
            isr_nodes: list[int]
            eligible_leader_replicas: list[int] | None
            last_known_elr: list[int] | None
            offline_replicas: list[int]
            def __init__(
                self,
                *args,
                error_code: int = ...,
                partition_index: int = ...,
                leader_id: int = ...,
                leader_epoch: int = ...,
                replica_nodes: list[int] = ...,
                isr_nodes: list[int] = ...,
                eligible_leader_replicas: list[int] | None = ...,
                last_known_elr: list[int] | None = ...,
                offline_replicas: list[int] = ...,
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
        name: str | None
        topic_id: uuid.UUID
        is_internal: bool
        partitions: list[DescribeTopicPartitionsResponsePartition]
        topic_authorized_operations: int
        def __init__(
            self,
            *args,
            error_code: int = ...,
            name: str | None = ...,
            topic_id: uuid.UUID = ...,
            is_internal: bool = ...,
            partitions: list[DescribeTopicPartitionsResponsePartition] = ...,
            topic_authorized_operations: int = ...,
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

    class Cursor(DataContainer):
        topic_name: str
        partition_index: int
        def __init__(
            self, *args, topic_name: str = ..., partition_index: int = ..., version: int | None = None, **kwargs
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
    topics: list[DescribeTopicPartitionsResponseTopic]
    next_cursor: Cursor | None
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        topics: list[DescribeTopicPartitionsResponseTopic] = ...,
        next_cursor: Cursor | None = ...,
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

class DeleteRecordsRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 is the same as version 0.

      // Version 2 is the first flexible version.
    """
    class DeleteRecordsTopic(DataContainer):
        class DeleteRecordsPartition(DataContainer):
            partition_index: int
            offset: int
            def __init__(
                self, *args, partition_index: int = ..., offset: int = ..., version: int | None = None, **kwargs
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
        partitions: list[DeleteRecordsPartition]
        def __init__(
            self, *args, name: str = ..., partitions: list[DeleteRecordsPartition] = ..., version: int | None = None, **kwargs
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    topics: list[DeleteRecordsTopic]
    timeout_ms: int
    def __init__(
        self, *args, topics: list[DeleteRecordsTopic] = ..., timeout_ms: int = ..., version: int | None = None, **kwargs
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

class DeleteRecordsResponse(ApiMessage):
    """
    Notes from json schema:
      // Starting in version 1, on quota violation, brokers send out responses before throttling.

      // Version 2 is the first flexible version.
    """
    class DeleteRecordsTopicResult(DataContainer):
        class DeleteRecordsPartitionResult(DataContainer):
            partition_index: int
            low_watermark: int
            error_code: int
            def __init__(
                self,
                *args,
                partition_index: int = ...,
                low_watermark: int = ...,
                error_code: int = ...,
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
        partitions: list[DeleteRecordsPartitionResult]
        def __init__(
            self,
            *args,
            name: str = ...,
            partitions: list[DeleteRecordsPartitionResult] = ...,
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
    topics: list[DeleteRecordsTopicResult]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        topics: list[DeleteRecordsTopicResult] = ...,
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

class ElectLeadersRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 implements multiple leader election types, as described by KIP-460.
      //
      // Version 2 is the first flexible version.
    """
    class TopicPartitions(DataContainer):
        topic: str
        partitions: list[int]
        def __init__(
            self, *args, topic: str = ..., partitions: list[int] = ..., version: int | None = None, **kwargs
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    election_type: int
    topic_partitions: list[TopicPartitions] | None
    timeout_ms: int
    def __init__(
        self,
        *args,
        election_type: int = ...,
        topic_partitions: list[TopicPartitions] | None = ...,
        timeout_ms: int = ...,
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

class ElectLeadersResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 1 adds a top-level error code.
      //
      // Version 2 is the first flexible version.
    """
    class ReplicaElectionResult(DataContainer):
        class PartitionResult(DataContainer):
            partition_id: int
            error_code: int
            error_message: str | None
            def __init__(
                self,
                *args,
                partition_id: int = ...,
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

        topic: str
        partition_result: list[PartitionResult]
        def __init__(
            self, *args, topic: str = ..., partition_result: list[PartitionResult] = ..., version: int | None = None, **kwargs
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
    replica_election_results: list[ReplicaElectionResult]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        error_code: int = ...,
        replica_election_results: list[ReplicaElectionResult] = ...,
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

class ElectionType(IntEnum):
    """Leader election type"""
    PREFERRED = 0
    UNCLEAN = 1

__all__ = [
    "CreateTopicsRequest",
    "CreateTopicsResponse",
    "DeleteTopicsRequest",
    "DeleteTopicsResponse",
    "CreatePartitionsRequest",
    "CreatePartitionsResponse",
    "AlterPartitionReassignmentsRequest",
    "AlterPartitionReassignmentsResponse",
    "ListPartitionReassignmentsRequest",
    "ListPartitionReassignmentsResponse",
    "DescribeTopicPartitionsRequest",
    "DescribeTopicPartitionsResponse",
    "DeleteRecordsRequest",
    "DeleteRecordsResponse",
    "ElectLeadersRequest",
    "ElectLeadersResponse",
    "ElectionType",
]

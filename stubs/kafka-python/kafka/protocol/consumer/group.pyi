import uuid
from _typeshed import Incomplete
from typing import Final

from kafka.protocol.api_data import ApiData
from kafka.protocol.api_message import ApiMessage
from kafka.protocol.data_container import DataContainer

DEFAULT_GENERATION_ID: Final = -1
UNKNOWN_MEMBER_ID: Final = ""

class JoinGroupRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 adds RebalanceTimeoutMs. Version 2 and 3 are the same as version 1.
      //
      // Starting from version 4, the client needs to issue a second request to join group
      //
      // Starting from version 5, we add a new field called groupInstanceId to indicate member identity across restarts.
      // with assigned id.
      //
      // Version 6 is the first flexible version.
      //
      // Version 7 is the same as version 6.
      //
      // Version 8 adds the Reason field (KIP-800).
      //
      // Version 9 is the same as version 8.
    """
    class JoinGroupRequestProtocol(DataContainer):
        name: str
        metadata: bytes | ApiData
        def __init__(
            self, *args, name: str = ..., metadata: bytes | ApiData = ..., version: int | None = None, **kwargs
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    group_id: str
    session_timeout_ms: int
    rebalance_timeout_ms: int
    member_id: str
    group_instance_id: str | None
    protocol_type: str
    protocols: list[JoinGroupRequestProtocol]
    reason: str | None
    def __init__(
        self,
        *args,
        group_id: str = ...,
        session_timeout_ms: int = ...,
        rebalance_timeout_ms: int = ...,
        member_id: str = ...,
        group_instance_id: str | None = ...,
        protocol_type: str = ...,
        protocols: list[JoinGroupRequestProtocol] = ...,
        reason: str | None = ...,
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

class JoinGroupResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 1 is the same as version 0.
      //
      // Version 2 adds throttle time.
      //
      // Starting in version 3, on quota violation, brokers send out responses before throttling.
      //
      // Starting in version 4, the client needs to issue a second request to join group
      // with assigned id.
      //
      // Version 5 is bumped to apply group.instance.id to identify member across restarts.
      //
      // Version 6 is the first flexible version.
      //
      // Starting from version 7, the broker sends back the Protocol Type to the client (KIP-559).
      //
      // Version 8 is the same as version 7.
      //
      // Version 9 adds the SkipAssignment field.
    """
    class JoinGroupResponseMember(DataContainer):
        member_id: str
        group_instance_id: str | None
        metadata: bytes | ApiData
        def __init__(
            self,
            *args,
            member_id: str = ...,
            group_instance_id: str | None = ...,
            metadata: bytes | ApiData = ...,
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
    generation_id: int
    protocol_type: str | None
    protocol_name: str | None
    leader: str
    skip_assignment: bool
    member_id: str
    members: list[JoinGroupResponseMember]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        error_code: int = ...,
        generation_id: int = ...,
        protocol_type: str | None = ...,
        protocol_name: str | None = ...,
        leader: str = ...,
        skip_assignment: bool = ...,
        member_id: str = ...,
        members: list[JoinGroupResponseMember] = ...,
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

class SyncGroupRequest(ApiMessage):
    """
    Notes from json schema:
      // Versions 1 and 2 are the same as version 0.
      //
      // Starting from version 3, we add a new field called groupInstanceId to indicate member identity across restarts.
      //
      // Version 4 is the first flexible version.
      //
      // Starting from version 5, the client sends the Protocol Type and the Protocol Name
      // to the broker (KIP-559). The broker will reject the request if they are inconsistent
      // with the Type and Name known by the broker.
    """
    class SyncGroupRequestAssignment(DataContainer):
        member_id: str
        assignment: bytes | ApiData
        def __init__(
            self, *args, member_id: str = ..., assignment: bytes | ApiData = ..., version: int | None = None, **kwargs
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    group_id: str
    generation_id: int
    member_id: str
    group_instance_id: str | None
    protocol_type: str | None
    protocol_name: str | None
    assignments: list[SyncGroupRequestAssignment]
    def __init__(
        self,
        *args,
        group_id: str = ...,
        generation_id: int = ...,
        member_id: str = ...,
        group_instance_id: str | None = ...,
        protocol_type: str | None = ...,
        protocol_name: str | None = ...,
        assignments: list[SyncGroupRequestAssignment] = ...,
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

class SyncGroupResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 1 adds throttle time.
      //
      // Starting in version 2, on quota violation, brokers send out responses before throttling.
      //
      // Starting from version 3, syncGroupRequest supports a new field called groupInstanceId to indicate member identity across restarts.
      //
      // Version 4 is the first flexible version.
      //
      // Starting from version 5, the broker sends back the Protocol Type and the Protocol Name
      // to the client (KIP-559).
    """
    throttle_time_ms: int
    error_code: int
    protocol_type: str | None
    protocol_name: str | None
    assignment: bytes | ApiData
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        error_code: int = ...,
        protocol_type: str | None = ...,
        protocol_name: str | None = ...,
        assignment: bytes | ApiData = ...,
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

class LeaveGroupRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 and 2 are the same as version 0.
      //
      // Version 3 defines batch processing scheme with group.instance.id + member.id for identity
      //
      // Version 4 is the first flexible version.
      //
      // Version 5 adds the Reason field (KIP-800).
    """
    class MemberIdentity(DataContainer):
        member_id: str
        group_instance_id: str | None
        reason: str | None
        def __init__(
            self,
            *args,
            member_id: str = ...,
            group_instance_id: str | None = ...,
            reason: str | None = ...,
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

    group_id: str
    member_id: str
    members: list[MemberIdentity]
    def __init__(
        self,
        *args,
        group_id: str = ...,
        member_id: str = ...,
        members: list[MemberIdentity] = ...,
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

class LeaveGroupResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 1 adds the throttle time.
      //
      // Starting in version 2, on quota violation, brokers send out responses before throttling.
      //
      // Starting in version 3, we will make leave group request into batch mode and add group.instance.id.
      //
      // Version 4 is the first flexible version.
      //
      // Version 5 is the same as version 4.
    """
    class MemberResponse(DataContainer):
        member_id: str
        group_instance_id: str | None
        error_code: int
        def __init__(
            self,
            *args,
            member_id: str = ...,
            group_instance_id: str | None = ...,
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

    throttle_time_ms: int
    error_code: int
    members: list[MemberResponse]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        error_code: int = ...,
        members: list[MemberResponse] = ...,
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

class HeartbeatRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 and version 2 are the same as version 0.
      //
      // Starting from version 3, we add a new field called groupInstanceId to indicate member identity across restarts.
      //
      // Version 4 is the first flexible version.
    """
    group_id: str
    generation_id: int
    member_id: str
    group_instance_id: str | None
    def __init__(
        self,
        *args,
        group_id: str = ...,
        generation_id: int = ...,
        member_id: str = ...,
        group_instance_id: str | None = ...,
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

class HeartbeatResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 1 adds throttle time.
      //
      // Starting in version 2, on quota violation, brokers send out responses before throttling.
      //
      // Starting from version 3, heartbeatRequest supports a new field called groupInstanceId to indicate member identity across restarts.
      //
      // Version 4 is the first flexible version.
    """
    throttle_time_ms: int
    error_code: int
    def __init__(
        self, *args, throttle_time_ms: int = ..., error_code: int = ..., version: int | None = None, **kwargs
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

class OffsetFetchRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 0 was removed in Apache Kafka 4.0, Version 1 is the new baseline.
      //
      // In version 0, the request read offsets from ZK.
      //
      // Starting in version 1, the broker supports fetching offsets from the internal __consumer_offsets topic.
      //
      // Starting in version 2, the request can contain a null topics array to indicate that offsets
      // for all topics should be fetched. It also returns a top level error code
      // for group or coordinator level errors.
      //
      // Version 3, 4, and 5 are the same as version 2.
      //
      // Version 6 is the first flexible version.
      //
      // Version 7 is adding the require stable flag.
      //
      // Version 8 is adding support for fetching offsets for multiple groups at a time.
      //
      // Version 9 is the first version that can be used with the new consumer group protocol (KIP-848). It adds
      // the MemberId and MemberEpoch fields. Those are filled in and validated when the new consumer protocol is used.
      //
      // Version 10 adds support for topic ids and removes support for topic names (KIP-848).
    """
    class OffsetFetchRequestTopic(DataContainer):
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

    class OffsetFetchRequestGroup(DataContainer):
        class OffsetFetchRequestTopics(DataContainer):
            name: str
            topic_id: uuid.UUID
            partition_indexes: list[int]
            def __init__(
                self,
                *args,
                name: str = ...,
                topic_id: uuid.UUID = ...,
                partition_indexes: list[int] = ...,
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

        group_id: str
        member_id: str | None
        member_epoch: int
        topics: list[OffsetFetchRequestTopics] | None
        def __init__(
            self,
            *args,
            group_id: str = ...,
            member_id: str | None = ...,
            member_epoch: int = ...,
            topics: list[OffsetFetchRequestTopics] | None = ...,
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

    group_id: str
    topics: list[OffsetFetchRequestTopic] | None
    groups: list[OffsetFetchRequestGroup]
    require_stable: bool
    def __init__(
        self,
        *args,
        group_id: str = ...,
        topics: list[OffsetFetchRequestTopic] | None = ...,
        groups: list[OffsetFetchRequestGroup] = ...,
        require_stable: bool = ...,
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

class OffsetFetchResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 0 was removed in Apache Kafka 4.0, Version 1 is the new baseline.
      //
      // Version 1 is the same as version 0.
      //
      // Version 2 adds a top-level error code.
      //
      // Version 3 adds the throttle time.
      //
      // Starting in version 4, on quota violation, brokers send out responses before throttling.
      //
      // Version 5 adds the leader epoch to the committed offset.
      //
      // Version 6 is the first flexible version.
      //
      // Version 7 adds pending offset commit as new error response on partition level.
      //
      // Version 8 is adding support for fetching offsets for multiple groups
      //
      // Version 9 is the first version that can be used with the new consumer group protocol (KIP-848). The response is
      // the same as version 8 but can return STALE_MEMBER_EPOCH and UNKNOWN_MEMBER_ID errors when the new consumer group
      // protocol is used.
      //
      // Version 10 adds support for topic ids and removes support for topic names (KIP-848).
      // It can return UNKNOWN_TOPIC_ID if topic IDs used and the topic is not found in metadata.
    """
    class OffsetFetchResponseTopic(DataContainer):
        class OffsetFetchResponsePartition(DataContainer):
            partition_index: int
            committed_offset: int
            committed_leader_epoch: int
            metadata: str | None
            error_code: int
            def __init__(
                self,
                *args,
                partition_index: int = ...,
                committed_offset: int = ...,
                committed_leader_epoch: int = ...,
                metadata: str | None = ...,
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
        partitions: list[OffsetFetchResponsePartition]
        def __init__(
            self,
            *args,
            name: str = ...,
            partitions: list[OffsetFetchResponsePartition] = ...,
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

    class OffsetFetchResponseGroup(DataContainer):
        class OffsetFetchResponseTopics(DataContainer):
            class OffsetFetchResponsePartitions(DataContainer):
                partition_index: int
                committed_offset: int
                committed_leader_epoch: int
                metadata: str | None
                error_code: int
                def __init__(
                    self,
                    *args,
                    partition_index: int = ...,
                    committed_offset: int = ...,
                    committed_leader_epoch: int = ...,
                    metadata: str | None = ...,
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
            topic_id: uuid.UUID
            partitions: list[OffsetFetchResponsePartitions]
            def __init__(
                self,
                *args,
                name: str = ...,
                topic_id: uuid.UUID = ...,
                partitions: list[OffsetFetchResponsePartitions] = ...,
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

        group_id: str
        topics: list[OffsetFetchResponseTopics]
        error_code: int
        def __init__(
            self,
            *args,
            group_id: str = ...,
            topics: list[OffsetFetchResponseTopics] = ...,
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

    throttle_time_ms: int
    topics: list[OffsetFetchResponseTopic]
    error_code: int
    groups: list[OffsetFetchResponseGroup]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        topics: list[OffsetFetchResponseTopic] = ...,
        error_code: int = ...,
        groups: list[OffsetFetchResponseGroup] = ...,
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

class OffsetCommitRequest(ApiMessage):
    """
    Notes from json schema:
      // Versions 0-1 were removed in Apache Kafka 4.0, Version 2 is the new baseline.
      //
      // Version 1 adds timestamp and group membership information, as well as the commit timestamp.
      //
      // Version 2 adds retention time.  It removes the commit timestamp added in version 1.
      //
      // Version 3 and 4 are the same as version 2. 
      //
      // Version 5 removes the retention time, which is now controlled only by a broker configuration.
      //
      // Version 6 adds the leader epoch for fencing.
      //
      // version 7 adds a new field called groupInstanceId to indicate member identity across restarts.
      //
      // Version 8 is the first flexible version.
      //
      // Version 9 is the first version that can be used with the new consumer group protocol (KIP-848). The
      // request is the same as version 8.
      //
      // Version 10 adds support for topic ids and removes support for topic names (KIP-848).
    """
    class OffsetCommitRequestTopic(DataContainer):
        class OffsetCommitRequestPartition(DataContainer):
            partition_index: int
            committed_offset: int
            committed_leader_epoch: int
            commit_timestamp: int
            committed_metadata: str | None
            def __init__(
                self,
                *args,
                partition_index: int = ...,
                committed_offset: int = ...,
                committed_leader_epoch: int = ...,
                commit_timestamp: int = ...,
                committed_metadata: str | None = ...,
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
        partitions: list[OffsetCommitRequestPartition]
        def __init__(
            self,
            *args,
            name: str = ...,
            topic_id: uuid.UUID = ...,
            partitions: list[OffsetCommitRequestPartition] = ...,
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

    group_id: str
    generation_id_or_member_epoch: int
    member_id: str
    group_instance_id: str | None
    retention_time_ms: int
    topics: list[OffsetCommitRequestTopic]
    def __init__(
        self,
        *args,
        group_id: str = ...,
        generation_id_or_member_epoch: int = ...,
        member_id: str = ...,
        group_instance_id: str | None = ...,
        retention_time_ms: int = ...,
        topics: list[OffsetCommitRequestTopic] = ...,
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

class OffsetCommitResponse(ApiMessage):
    """
    Notes from json schema:
      // Versions 0-1 were removed in Apache Kafka 4.0, Version 2 is the new baseline.
      //
      // Versions 1 and 2 are the same as version 0.
      //
      // Version 3 adds the throttle time to the response.
      //
      // Starting in version 4, on quota violation, brokers send out responses before throttling.
      //
      // Versions 5 and 6 are the same as version 4.
      //
      // Version 7 offsetCommitRequest supports a new field called groupInstanceId to indicate member identity across restarts.
      //
      // Version 8 is the first flexible version.
      //
      // Version 9 is the first version that can be used with the new consumer group protocol (KIP-848). The response is
      // the same as version 8 but can return STALE_MEMBER_EPOCH when the new consumer group protocol is used and
      // GROUP_ID_NOT_FOUND when the group does not exist for both protocols.
      //
      // Version 10 adds support for topic ids and removes support for topic names (KIP-848).
    """
    class OffsetCommitResponseTopic(DataContainer):
        class OffsetCommitResponsePartition(DataContainer):
            partition_index: int
            error_code: int
            def __init__(
                self, *args, partition_index: int = ..., error_code: int = ..., version: int | None = None, **kwargs
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
        partitions: list[OffsetCommitResponsePartition]
        def __init__(
            self,
            *args,
            name: str = ...,
            topic_id: uuid.UUID = ...,
            partitions: list[OffsetCommitResponsePartition] = ...,
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
    topics: list[OffsetCommitResponseTopic]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        topics: list[OffsetCommitResponseTopic] = ...,
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

class OffsetDeleteRequest(ApiMessage):
    class OffsetDeleteRequestTopic(DataContainer):
        class OffsetDeleteRequestPartition(DataContainer):
            partition_index: int
            def __init__(self, *args, partition_index: int = ..., version: int | None = None, **kwargs) -> None: ...
            @property
            def version(self) -> int | None: ...
            def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
                """
                Use meta=True to include top-level version; meta='all' to include all internal versions
                json=False to return raw encoding; json=True (default) to convert values to be json-serializable
                """
                ...

        name: str
        partitions: list[OffsetDeleteRequestPartition]
        def __init__(
            self,
            *args,
            name: str = ...,
            partitions: list[OffsetDeleteRequestPartition] = ...,
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

    group_id: str
    topics: list[OffsetDeleteRequestTopic]
    def __init__(
        self, *args, group_id: str = ..., topics: list[OffsetDeleteRequestTopic] = ..., version: int | None = None, **kwargs
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

class OffsetDeleteResponse(ApiMessage):
    class OffsetDeleteResponseTopic(DataContainer):
        class OffsetDeleteResponsePartition(DataContainer):
            partition_index: int
            error_code: int
            def __init__(
                self, *args, partition_index: int = ..., error_code: int = ..., version: int | None = None, **kwargs
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
        partitions: list[OffsetDeleteResponsePartition]
        def __init__(
            self,
            *args,
            name: str = ...,
            partitions: list[OffsetDeleteResponsePartition] = ...,
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
    throttle_time_ms: int
    topics: list[OffsetDeleteResponseTopic]
    def __init__(
        self,
        *args,
        error_code: int = ...,
        throttle_time_ms: int = ...,
        topics: list[OffsetDeleteResponseTopic] = ...,
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
    "DEFAULT_GENERATION_ID",
    "UNKNOWN_MEMBER_ID",
    "JoinGroupRequest",
    "JoinGroupResponse",
    "SyncGroupRequest",
    "SyncGroupResponse",
    "LeaveGroupRequest",
    "LeaveGroupResponse",
    "HeartbeatRequest",
    "HeartbeatResponse",
    "OffsetFetchRequest",
    "OffsetFetchResponse",
    "OffsetCommitRequest",
    "OffsetCommitResponse",
    "OffsetDeleteRequest",
    "OffsetDeleteResponse",
]

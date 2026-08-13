from _typeshed import Incomplete
from enum import IntEnum
from typing import Final

from kafka.protocol.api_message import ApiMessage
from kafka.protocol.data_container import DataContainer
from kafka.util import EnumHelper

UNKNOWN_OFFSET: Final = -1

class OffsetResetStrategy:
    LATEST: Final = -1
    EARLIEST: Final = -2
    NONE: Final = 0

class IsolationLevel(EnumHelper, IntEnum):
    """An enumeration."""
    READ_UNCOMMITTED = 0
    READ_COMMITTED = 1

class OffsetSpec(EnumHelper, IntEnum):
    """An enumeration."""
    LATEST = -1
    EARLIEST = -2
    MAX_TIMESTAMP = -3
    EARLIEST_LOCAL = -4
    LATEST_TIERED = -5

class OffsetTimestamp(int):
    """
    Millisecond-timestamp spec for partition offset lookup.

    Wraps an int so it can be distinguished from a bare offset. Use with
    :meth:`KafkaAdminClient.reset_group_offsets` (and anywhere else a spec
    may be mixed with explicit offsets) to request "earliest offset whose
    timestamp is >= N ms".
    """
    __slots__ = ()

class ListOffsetsRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 0 was removed in Apache Kafka 4.0, Version 1 is the new baseline.
      //
      // Version 1 removes MaxNumOffsets.  From this version forward, only a single
      // offset can be returned.
      //
      // Version 2 adds the isolation level, which is used for transactional reads.
      //
      // Version 3 is the same as version 2.
      //
      // Version 4 adds the current leader epoch, which is used for fencing.
      //
      // Version 5 is the same as version 4.
      //
      // Version 6 enables flexible versions.
      //
      // Version 7 enables listing offsets by max timestamp (KIP-734).
      //
      // Version 8 enables listing offsets by local log start offset (KIP-405).
      //
      // Version 9 enables listing offsets by last tiered offset (KIP-1005).
      //
      // Version 10 enables async remote list offsets support (KIP-1075)
      //
      // Version 11 enables listing offsets by earliest pending upload offset (KIP-1023)
    """
    class ListOffsetsTopic(DataContainer):
        class ListOffsetsPartition(DataContainer):
            partition_index: int
            current_leader_epoch: int
            timestamp: int
            max_num_offsets: int
            def __init__(
                self,
                *args,
                partition_index: int = ...,
                current_leader_epoch: int = ...,
                timestamp: int = ...,
                max_num_offsets: int = ...,
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
        partitions: list[ListOffsetsPartition]
        def __init__(
            self, *args, name: str = ..., partitions: list[ListOffsetsPartition] = ..., version: int | None = None, **kwargs
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    replica_id: int
    isolation_level: int
    topics: list[ListOffsetsTopic]
    timeout_ms: int
    def __init__(
        self,
        *args,
        replica_id: int = ...,
        isolation_level: int = ...,
        topics: list[ListOffsetsTopic] = ...,
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
    @classmethod
    def min_version_for_timestamp(cls, ts): ...
    @classmethod
    def min_version_for_isolation_level(cls, il): ...

class ListOffsetsResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 0 was removed in Apache Kafka 4.0, Version 1 is the new baseline.
      //
      // Version 1 removes the offsets array in favor of returning a single offset.
      // Version 1 also adds the timestamp associated with the returned offset.
      //
      // Version 2 adds the throttle time.
      //
      // Starting in version 3, on quota violation, brokers send out responses before throttling.
      //
      // Version 4 adds the leader epoch, which is used for fencing.
      //
      // Version 5 adds a new error code, OFFSET_NOT_AVAILABLE.
      //
      // Version 6 enables flexible versions.
      //
      // Version 7 is the same as version 6 (KIP-734).
      //
      // Version 8 enables listing offsets by local log start offset.
      // This is the earliest log start offset in the local log. (KIP-405).
      //
      // Version 9 enables listing offsets by last tiered offset (KIP-1005).
      //
      // Version 10 enables async remote list offsets support (KIP-1075)
      //
      // Version 11 enables listing offsets by earliest pending upload offset (KIP-1023)
    """
    class ListOffsetsTopicResponse(DataContainer):
        class ListOffsetsPartitionResponse(DataContainer):
            partition_index: int
            error_code: int
            old_style_offsets: list[int]
            timestamp: int
            offset: int
            leader_epoch: int
            def __init__(
                self,
                *args,
                partition_index: int = ...,
                error_code: int = ...,
                old_style_offsets: list[int] = ...,
                timestamp: int = ...,
                offset: int = ...,
                leader_epoch: int = ...,
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
        partitions: list[ListOffsetsPartitionResponse]
        def __init__(
            self,
            *args,
            name: str = ...,
            partitions: list[ListOffsetsPartitionResponse] = ...,
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
    topics: list[ListOffsetsTopicResponse]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        topics: list[ListOffsetsTopicResponse] = ...,
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

class OffsetForLeaderEpochRequest(ApiMessage):
    """
    Notes from json schema:
      // Versions 0-1 were removed in Apache Kafka 4.0, Version 2 is the new baseline.
      //
      // Version 1 is the same as version 0.
      //
      // Version 2 adds the current leader epoch to support fencing.
      //
      // Version 3 adds ReplicaId (the default is -2 which conventionally represents a
      //    "debug" consumer which is allowed to see offsets beyond the high watermark).
      //    Followers will use this replicaId when using an older version of the protocol.
      //
      // Version 4 enables flexible versions.
    """
    class OffsetForLeaderTopic(DataContainer):
        class OffsetForLeaderPartition(DataContainer):
            partition: int
            current_leader_epoch: int
            leader_epoch: int
            def __init__(
                self,
                *args,
                partition: int = ...,
                current_leader_epoch: int = ...,
                leader_epoch: int = ...,
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
        partitions: list[OffsetForLeaderPartition]
        def __init__(
            self, *args, topic: str = ..., partitions: list[OffsetForLeaderPartition] = ..., version: int | None = None, **kwargs
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    replica_id: int
    topics: list[OffsetForLeaderTopic]
    def __init__(
        self, *args, replica_id: int = ..., topics: list[OffsetForLeaderTopic] = ..., version: int | None = None, **kwargs
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

class OffsetForLeaderEpochResponse(ApiMessage):
    """
    Notes from json schema:
      // Versions 0-1 were removed in Apache Kafka 4.0, Version 2 is the new baseline.
      //
      // Version 1 added the leader epoch to the response.
      //
      // Version 2 added the throttle time.
      //
      // Version 3 is the same as version 2.
      //
      // Version 4 enables flexible versions.
    """
    class OffsetForLeaderTopicResult(DataContainer):
        class EpochEndOffset(DataContainer):
            error_code: int
            partition: int
            leader_epoch: int
            end_offset: int
            def __init__(
                self,
                *args,
                error_code: int = ...,
                partition: int = ...,
                leader_epoch: int = ...,
                end_offset: int = ...,
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
        partitions: list[EpochEndOffset]
        def __init__(
            self, *args, topic: str = ..., partitions: list[EpochEndOffset] = ..., version: int | None = None, **kwargs
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
    topics: list[OffsetForLeaderTopicResult]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        topics: list[OffsetForLeaderTopicResult] = ...,
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
    "UNKNOWN_OFFSET",
    "OffsetResetStrategy",
    "IsolationLevel",
    "OffsetSpec",
    "OffsetTimestamp",
    "ListOffsetsRequest",
    "ListOffsetsResponse",
    "OffsetForLeaderEpochRequest",
    "OffsetForLeaderEpochResponse",
]

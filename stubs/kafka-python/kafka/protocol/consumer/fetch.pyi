import uuid
from _typeshed import Incomplete

from kafka.protocol.api_data import ApiData
from kafka.protocol.api_message import ApiMessage
from kafka.protocol.data_container import DataContainer

class FetchRequest(ApiMessage):
    """
    Notes from json schema:
      // Versions 0-3 were removed in Apache Kafka 4.0, Version 4 is the new baseline.
      //
      // Version 1 is the same as version 0.
      // Starting in Version 2, the requester must be able to handle Kafka Log
      // Message format version 1.
      // Version 3 adds MaxBytes.  Starting in version 3, the partition ordering in
      // the request is now relevant.  Partitions will be processed in the order
      // they appear in the request.
      //
      // Version 4 adds IsolationLevel.  Starting in version 4, the requestor must be
      // able to handle Kafka log message format version 2.
      //
      // Version 5 adds LogStartOffset to indicate the earliest available offset of
      // partition data that can be consumed.
      //
      // Version 6 is the same as version 5.
      //
      // Version 7 adds incremental fetch request support.
      //
      // Version 8 is the same as version 7.
      //
      // Version 9 adds CurrentLeaderEpoch, as described in KIP-320.
      //
      // Version 10 indicates that we can use the ZStd compression algorithm, as
      // described in KIP-110.
      // Version 12 adds flexible versions support as well as epoch validation through
      // the `LastFetchedEpoch` field
      //
      // Version 13 replaces topic names with topic IDs (KIP-516). May return UNKNOWN_TOPIC_ID error code.
      //
      // Version 14 is the same as version 13 but it also receives a new error called OffsetMovedToTieredStorageException(KIP-405)
      //
      // Version 15 adds the ReplicaState which includes new field ReplicaEpoch and the ReplicaId. Also,
      // deprecate the old ReplicaId field and set its default value to -1. (KIP-903)
      //
      // Version 16 is the same as version 15 (KIP-951).
      //
      // Version 17 adds directory id support from KIP-853
      //
      // Version 18 adds high-watermark from KIP-1166
    """
    class ReplicaState(DataContainer):
        replica_id: int
        replica_epoch: int
        def __init__(
            self, *args, replica_id: int = ..., replica_epoch: int = ..., version: int | None = None, **kwargs
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    class FetchTopic(DataContainer):
        class FetchPartition(DataContainer):
            partition: int
            current_leader_epoch: int
            fetch_offset: int
            last_fetched_epoch: int
            log_start_offset: int
            partition_max_bytes: int
            replica_directory_id: uuid.UUID
            high_watermark: int
            def __init__(
                self,
                *args,
                partition: int = ...,
                current_leader_epoch: int = ...,
                fetch_offset: int = ...,
                last_fetched_epoch: int = ...,
                log_start_offset: int = ...,
                partition_max_bytes: int = ...,
                replica_directory_id: uuid.UUID = ...,
                high_watermark: int = ...,
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
        topic_id: uuid.UUID
        partitions: list[FetchPartition]
        def __init__(
            self,
            *args,
            topic: str = ...,
            topic_id: uuid.UUID = ...,
            partitions: list[FetchPartition] = ...,
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

    class ForgottenTopic(DataContainer):
        topic: str
        topic_id: uuid.UUID
        partitions: list[int]
        def __init__(
            self,
            *args,
            topic: str = ...,
            topic_id: uuid.UUID = ...,
            partitions: list[int] = ...,
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

    cluster_id: str | None
    replica_id: int
    replica_state: ReplicaState
    max_wait_ms: int
    min_bytes: int
    max_bytes: int
    isolation_level: int
    session_id: int
    session_epoch: int
    topics: list[FetchTopic]
    forgotten_topics_data: list[ForgottenTopic]
    rack_id: str
    def __init__(
        self,
        *args,
        cluster_id: str | None = ...,
        replica_id: int = ...,
        replica_state: ReplicaState = ...,
        max_wait_ms: int = ...,
        min_bytes: int = ...,
        max_bytes: int = ...,
        isolation_level: int = ...,
        session_id: int = ...,
        session_epoch: int = ...,
        topics: list[FetchTopic] = ...,
        forgotten_topics_data: list[ForgottenTopic] = ...,
        rack_id: str = ...,
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
    def min_version_for_isolation_level(cls, il): ...

class FetchResponse(ApiMessage):
    """
    Notes from json schema:
      // Versions 0-3 were removed in Apache Kafka 4.0, Version 4 is the new baseline.
      //
      // Version 1 adds throttle time. Version 2 and 3 are the same as version 1.
      //
      // Version 4 adds features for transactional consumption.
      //
      // Version 5 adds LogStartOffset to indicate the earliest available offset of
      // partition data that can be consumed.
      //
      // Starting in version 6, we may return KAFKA_STORAGE_ERROR as an error code.
      //
      // Version 7 adds incremental fetch request support.
      //
      // Starting in version 8, on quota violation, brokers send out responses before throttling.
      //
      // Version 9 is the same as version 8.
      //
      // Version 10 indicates that the response data can use the ZStd compression
      // algorithm, as described in KIP-110.
      // Version 12 adds support for flexible versions, epoch detection through the `TruncationOffset` field,
      // and leader discovery through the `CurrentLeader` field
      //
      // Version 13 replaces the topic name field with topic ID (KIP-516).
      //
      // Version 14 is the same as version 13 but it also receives a new error called OffsetMovedToTieredStorageException (KIP-405)
      //
      // Version 15 is the same as version 14 (KIP-903).
      //
      // Version 16 adds the 'NodeEndpoints' field (KIP-951).
      //
      // Version 17 no changes to the response (KIP-853).
      //
      // Version 18 no changes to the response (KIP-1166)
    """
    class FetchableTopicResponse(DataContainer):
        class PartitionData(DataContainer):
            class EpochEndOffset(DataContainer):
                epoch: int
                end_offset: int
                def __init__(
                    self, *args, epoch: int = ..., end_offset: int = ..., version: int | None = None, **kwargs
                ) -> None: ...
                @property
                def version(self) -> int | None: ...
                def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
                    """
                    Use meta=True to include top-level version; meta='all' to include all internal versions
                    json=False to return raw encoding; json=True (default) to convert values to be json-serializable
                    """
                    ...

            class LeaderIdAndEpoch(DataContainer):
                leader_id: int
                leader_epoch: int
                def __init__(
                    self, *args, leader_id: int = ..., leader_epoch: int = ..., version: int | None = None, **kwargs
                ) -> None: ...
                @property
                def version(self) -> int | None: ...
                def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
                    """
                    Use meta=True to include top-level version; meta='all' to include all internal versions
                    json=False to return raw encoding; json=True (default) to convert values to be json-serializable
                    """
                    ...

            class SnapshotId(DataContainer):
                end_offset: int
                epoch: int
                def __init__(
                    self, *args, end_offset: int = ..., epoch: int = ..., version: int | None = None, **kwargs
                ) -> None: ...
                @property
                def version(self) -> int | None: ...
                def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
                    """
                    Use meta=True to include top-level version; meta='all' to include all internal versions
                    json=False to return raw encoding; json=True (default) to convert values to be json-serializable
                    """
                    ...

            class AbortedTransaction(DataContainer):
                producer_id: int
                first_offset: int
                def __init__(
                    self, *args, producer_id: int = ..., first_offset: int = ..., version: int | None = None, **kwargs
                ) -> None: ...
                @property
                def version(self) -> int | None: ...
                def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
                    """
                    Use meta=True to include top-level version; meta='all' to include all internal versions
                    json=False to return raw encoding; json=True (default) to convert values to be json-serializable
                    """
                    ...

            partition_index: int
            error_code: int
            high_watermark: int
            last_stable_offset: int
            log_start_offset: int
            diverging_epoch: EpochEndOffset
            current_leader: LeaderIdAndEpoch
            snapshot_id: SnapshotId
            aborted_transactions: list[AbortedTransaction] | None
            preferred_read_replica: int
            records: bytes | ApiData | None
            def __init__(
                self,
                *args,
                partition_index: int = ...,
                error_code: int = ...,
                high_watermark: int = ...,
                last_stable_offset: int = ...,
                log_start_offset: int = ...,
                diverging_epoch: EpochEndOffset = ...,
                current_leader: LeaderIdAndEpoch = ...,
                snapshot_id: SnapshotId = ...,
                aborted_transactions: list[AbortedTransaction] | None = ...,
                preferred_read_replica: int = ...,
                records: bytes | ApiData | None = ...,
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
        topic_id: uuid.UUID
        partitions: list[PartitionData]
        def __init__(
            self,
            *args,
            topic: str = ...,
            topic_id: uuid.UUID = ...,
            partitions: list[PartitionData] = ...,
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

    class NodeEndpoint(DataContainer):
        node_id: int
        host: str
        port: int
        rack: str | None
        def __init__(
            self,
            *args,
            node_id: int = ...,
            host: str = ...,
            port: int = ...,
            rack: str | None = ...,
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
    session_id: int
    responses: list[FetchableTopicResponse]
    node_endpoints: list[NodeEndpoint]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        error_code: int = ...,
        session_id: int = ...,
        responses: list[FetchableTopicResponse] = ...,
        node_endpoints: list[NodeEndpoint] = ...,
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

__all__ = ["FetchRequest", "FetchResponse"]

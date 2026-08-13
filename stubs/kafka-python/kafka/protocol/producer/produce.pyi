import uuid
from _typeshed import Incomplete

from kafka.protocol.api_data import ApiData
from kafka.protocol.api_message import ApiMessage
from kafka.protocol.data_container import DataContainer

class ProduceRequest(ApiMessage):
    """
    Notes from json schema:
      // Versions 0-2 were removed in Apache Kafka 4.0, version 3 is the new baseline. Due to a bug in librdkafka,
      // these versions have to be included in the api versions response (see KAFKA-18659), but are rejected otherwise.
      // See `ApiKeys.PRODUCE_API_VERSIONS_RESPONSE_MIN_VERSION` for more details.
      //
      // Version 1 and 2 are the same as version 0.
      //
      // Version 3 adds the transactional ID, which is used for authorization when attempting to write
      // transactional data.  Version 3 also adds support for Kafka Message Format v2.
      //
      // Version 4 is the same as version 3, but the requester must be prepared to handle a
      // KAFKA_STORAGE_ERROR.
      //
      // Version 5 and 6 are the same as version 3.
      //
      // Starting in version 7, records can be produced using ZStandard compression.  See KIP-110.
      //
      // Starting in Version 8, response has RecordErrors and ErrorMessage. See KIP-467.
      //
      // Version 9 enables flexible versions.
      //
      // Version 10 is the same as version 9 (KIP-951).
      //
      // Version 11 adds support for new error code TRANSACTION_ABORTABLE (KIP-890).
      //
      // Version 12 is the same as version 11 (KIP-890). Note when produce requests are used in transaction, if
      // transaction V2 (KIP_890 part 2) is enabled, the produce request will also include the function for a
      // AddPartitionsToTxn call. If V2 is disabled, the client can't use produce request version higher than 11 within
      // a transaction.
      // Version 13 replaces topic names with topic IDs (KIP-516). May return UNKNOWN_TOPIC_ID error code.
    """
    class TopicProduceData(DataContainer):
        class PartitionProduceData(DataContainer):
            index: int
            records: bytes | ApiData | None
            def __init__(
                self, *args, index: int = ..., records: bytes | ApiData | None = ..., version: int | None = None, **kwargs
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
        partition_data: list[PartitionProduceData]
        def __init__(
            self,
            *args,
            name: str = ...,
            topic_id: uuid.UUID = ...,
            partition_data: list[PartitionProduceData] = ...,
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

    transactional_id: str | None
    acks: int
    timeout_ms: int
    topic_data: list[TopicProduceData]
    def __init__(
        self,
        *args,
        transactional_id: str | None = ...,
        acks: int = ...,
        timeout_ms: int = ...,
        topic_data: list[TopicProduceData] = ...,
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
    def with_header(self, correlation_id: int = 0, client_id: str = "kafka-python") -> None: ...
    def expect_response(self) -> bool: ...

class ProduceResponse(ApiMessage):
    """
    Notes from json schema:
      // Versions 0-2 were removed in Apache Kafka 4.0, version 3 is the new baseline. Due to a bug in librdkafka,
      // these versions have to be included in the api versions response (see KAFKA-18659), but are rejected otherwise.
      // See `ApiKeys.PRODUCE_API_VERSIONS_RESPONSE_MIN_VERSION` for more details.
      //
      // Version 1 added the throttle time.
      // Version 2 added the log append time.
      //
      // Version 3 is the same as version 2.
      //
      // Version 4 added KAFKA_STORAGE_ERROR as a possible error code.
      //
      // Version 5 added LogStartOffset to filter out spurious OutOfOrderSequenceExceptions on the client.
      //
      // Version 8 added RecordErrors and ErrorMessage to include information about
      // records that cause the whole batch to be dropped.  See KIP-467 for details.
      //
      // Version 9 enables flexible versions.
      //
      // Version 10 adds 'CurrentLeader' and 'NodeEndpoints' as tagged fields (KIP-951)
      //
      // Version 11 adds support for new error code TRANSACTION_ABORTABLE (KIP-890).
      //
      // Version 12 is the same as version 10 (KIP-890).
      // Version 13 replaces topic names with topic IDs (KIP-516). May return UNKNOWN_TOPIC_ID error code.
    """
    class TopicProduceResponse(DataContainer):
        class PartitionProduceResponse(DataContainer):
            class BatchIndexAndErrorMessage(DataContainer):
                batch_index: int
                batch_index_error_message: str | None
                def __init__(
                    self,
                    *args,
                    batch_index: int = ...,
                    batch_index_error_message: str | None = ...,
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

            index: int
            error_code: int
            base_offset: int
            log_append_time_ms: int
            log_start_offset: int
            record_errors: list[BatchIndexAndErrorMessage]
            error_message: str | None
            current_leader: LeaderIdAndEpoch
            def __init__(
                self,
                *args,
                index: int = ...,
                error_code: int = ...,
                base_offset: int = ...,
                log_append_time_ms: int = ...,
                log_start_offset: int = ...,
                record_errors: list[BatchIndexAndErrorMessage] = ...,
                error_message: str | None = ...,
                current_leader: LeaderIdAndEpoch = ...,
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
        partition_responses: list[PartitionProduceResponse]
        def __init__(
            self,
            *args,
            name: str = ...,
            topic_id: uuid.UUID = ...,
            partition_responses: list[PartitionProduceResponse] = ...,
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

    responses: list[TopicProduceResponse]
    throttle_time_ms: int
    node_endpoints: list[NodeEndpoint]
    def __init__(
        self,
        *args,
        responses: list[TopicProduceResponse] = ...,
        throttle_time_ms: int = ...,
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

__all__ = ["ProduceRequest", "ProduceResponse"]

from _typeshed import Incomplete

from kafka.protocol.api_message import ApiMessage
from kafka.protocol.data_container import DataContainer

class InitProducerIdRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 is the same as version 0.
      //
      // Version 2 is the first flexible version.
      //
      // Version 3 adds ProducerId and ProducerEpoch, allowing producers to try to resume after an INVALID_PRODUCER_EPOCH error
      //
      // Version 4 adds the support for new error code PRODUCER_FENCED.
      //
      // Version 5 adds support for new error code TRANSACTION_ABORTABLE (KIP-890).
      //
      // Version 6 adds support for 2PC (KIP-939).
    """
    transactional_id: str | None
    transaction_timeout_ms: int
    producer_id: int
    producer_epoch: int
    enable2_pc: bool
    keep_prepared_txn: bool
    def __init__(
        self,
        *args,
        transactional_id: str | None = ...,
        transaction_timeout_ms: int = ...,
        producer_id: int = ...,
        producer_epoch: int = ...,
        enable2_pc: bool = ...,
        keep_prepared_txn: bool = ...,
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

class InitProducerIdResponse(ApiMessage):
    """
    Notes from json schema:
      // Starting in version 1, on quota violation, brokers send out responses before throttling.
      //
      // Version 2 is the first flexible version.
      //
      // Version 3 is the same as version 2.
      //
      // Version 4 adds the support for new error code PRODUCER_FENCED.
      //
      // Version 5 adds support for new error code TRANSACTION_ABORTABLE (KIP-890).
      //
      // Version 6 adds support for 2PC (KIP-939).
    """
    throttle_time_ms: int
    error_code: int
    producer_id: int
    producer_epoch: int
    ongoing_txn_producer_id: int
    ongoing_txn_producer_epoch: int
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        error_code: int = ...,
        producer_id: int = ...,
        producer_epoch: int = ...,
        ongoing_txn_producer_id: int = ...,
        ongoing_txn_producer_epoch: int = ...,
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

class AddPartitionsToTxnRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 is the same as version 0.
      //
      // Version 2 adds the support for new error code PRODUCER_FENCED.
      //
      // Version 3 enables flexible versions.
      //
      // Version 4 adds VerifyOnly field to check if partitions are already in transaction and adds support to batch multiple transactions.
      //
      // Version 5 adds support for new error code TRANSACTION_ABORTABLE (KIP-890).
      // Versions 3 and below will be exclusively used by clients and versions 4 and above will be used by brokers.
    """
    class AddPartitionsToTxnTransaction(DataContainer):
        class AddPartitionsToTxnTopic(DataContainer):
            name: str
            partitions: list[int]
            def __init__(
                self, *args, name: str = ..., partitions: list[int] = ..., version: int | None = None, **kwargs
            ) -> None: ...
            @property
            def version(self) -> int | None: ...
            def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
                """
                Use meta=True to include top-level version; meta='all' to include all internal versions
                json=False to return raw encoding; json=True (default) to convert values to be json-serializable
                """
                ...

        transactional_id: str
        producer_id: int
        producer_epoch: int
        verify_only: bool
        topics: list[AddPartitionsToTxnTopic]
        def __init__(
            self,
            *args,
            transactional_id: str = ...,
            producer_id: int = ...,
            producer_epoch: int = ...,
            verify_only: bool = ...,
            topics: list[AddPartitionsToTxnTopic] = ...,
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

    class AddPartitionsToTxnTopic(DataContainer):
        name: str
        partitions: list[int]
        def __init__(self, *args, name: str = ..., partitions: list[int] = ..., version: int | None = None, **kwargs) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    transactions: list[AddPartitionsToTxnTransaction]
    v3_and_below_transactional_id: str
    v3_and_below_producer_id: int
    v3_and_below_producer_epoch: int
    v3_and_below_topics: list[AddPartitionsToTxnTopic]
    def __init__(
        self,
        *args,
        transactions: list[AddPartitionsToTxnTransaction] = ...,
        v3_and_below_transactional_id: str = ...,
        v3_and_below_producer_id: int = ...,
        v3_and_below_producer_epoch: int = ...,
        v3_and_below_topics: list[AddPartitionsToTxnTopic] = ...,
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

class AddPartitionsToTxnResponse(ApiMessage):
    """
    Notes from json schema:
      // Starting in version 1, on quota violation brokers send out responses before throttling.
      //
      // Version 2 adds the support for new error code PRODUCER_FENCED.
      //
      // Version 3 enables flexible versions.
      //
      // Version 4 adds support to batch multiple transactions and a top level error code.
      //
      // Version 5 adds support for new error code TRANSACTION_ABORTABLE (KIP-890).
    """
    class AddPartitionsToTxnResult(DataContainer):
        class AddPartitionsToTxnTopicResult(DataContainer):
            class AddPartitionsToTxnPartitionResult(DataContainer):
                partition_index: int
                partition_error_code: int
                def __init__(
                    self, *args, partition_index: int = ..., partition_error_code: int = ..., version: int | None = None, **kwargs
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
            results_by_partition: list[AddPartitionsToTxnPartitionResult]
            def __init__(
                self,
                *args,
                name: str = ...,
                results_by_partition: list[AddPartitionsToTxnPartitionResult] = ...,
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

        transactional_id: str
        topic_results: list[AddPartitionsToTxnTopicResult]
        def __init__(
            self,
            *args,
            transactional_id: str = ...,
            topic_results: list[AddPartitionsToTxnTopicResult] = ...,
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

    class AddPartitionsToTxnTopicResult(DataContainer):
        class AddPartitionsToTxnPartitionResult(DataContainer):
            partition_index: int
            partition_error_code: int
            def __init__(
                self, *args, partition_index: int = ..., partition_error_code: int = ..., version: int | None = None, **kwargs
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
        results_by_partition: list[AddPartitionsToTxnPartitionResult]
        def __init__(
            self,
            *args,
            name: str = ...,
            results_by_partition: list[AddPartitionsToTxnPartitionResult] = ...,
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
    results_by_transaction: list[AddPartitionsToTxnResult]
    results_by_topic_v3_and_below: list[AddPartitionsToTxnTopicResult]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        error_code: int = ...,
        results_by_transaction: list[AddPartitionsToTxnResult] = ...,
        results_by_topic_v3_and_below: list[AddPartitionsToTxnTopicResult] = ...,
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

class AddOffsetsToTxnRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 is the same as version 0.
      //
      // Version 2 adds the support for new error code PRODUCER_FENCED.
      //
      // Version 3 enables flexible versions.
      //
      // Version 4 adds support for new error code TRANSACTION_ABORTABLE (KIP-890).
    """
    transactional_id: str
    producer_id: int
    producer_epoch: int
    group_id: str
    def __init__(
        self,
        *args,
        transactional_id: str = ...,
        producer_id: int = ...,
        producer_epoch: int = ...,
        group_id: str = ...,
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

class AddOffsetsToTxnResponse(ApiMessage):
    """
    Notes from json schema:
      // Starting in version 1, on quota violation brokers send out responses before throttling.
      //
      // Version 2 adds the support for new error code PRODUCER_FENCED.
      //
      // Version 3 enables flexible versions.
      //
      // Version 4 adds support for new error code TRANSACTION_ABORTABLE (KIP-890).
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

class EndTxnRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 is the same as version 0.
      //
      // Version 2 adds the support for new error code PRODUCER_FENCED.
      //
      // Version 3 enables flexible versions.
      //
      // Version 4 adds support for new error code TRANSACTION_ABORTABLE (KIP-890).
      //
      // Version 5 enables bumping epoch on every transaction (KIP-890 Part 2)
    """
    transactional_id: str
    producer_id: int
    producer_epoch: int
    committed: bool
    def __init__(
        self,
        *args,
        transactional_id: str = ...,
        producer_id: int = ...,
        producer_epoch: int = ...,
        committed: bool = ...,
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

class EndTxnResponse(ApiMessage):
    """
    Notes from json schema:
      // Starting in version 1, on quota violation, brokers send out responses before throttling.
      //
      // Version 2 adds the support for new error code PRODUCER_FENCED.
      //
      // Version 3 enables flexible versions.
      //
      // Version 4 adds support for new error code TRANSACTION_ABORTABLE (KIP-890).
      //
      // Version 5 enables bumping epoch on every transaction (KIP-890 Part 2), so producer ID and epoch are included in the response.
    """
    throttle_time_ms: int
    error_code: int
    producer_id: int
    producer_epoch: int
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        error_code: int = ...,
        producer_id: int = ...,
        producer_epoch: int = ...,
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

class TxnOffsetCommitRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 is the same as version 0.
      //
      // Version 2 adds the committed leader epoch.
      //
      // Version 3 adds the member.id, group.instance.id and generation.id.
      //
      // Version 4 adds support for new error code TRANSACTION_ABORTABLE (KIP-890).
      //
      // Version 5 is the same as version 4 (KIP-890). Note when TxnOffsetCommit requests are used in transaction, if
      // transaction V2 (KIP_890 part 2) is enabled, the TxnOffsetCommit request will also include the function for a
      // AddOffsetsToTxn call. If V2 is disabled, the client can't use TxnOffsetCommit request version higher than 4 within
      // a transaction.
    """
    class TxnOffsetCommitRequestTopic(DataContainer):
        class TxnOffsetCommitRequestPartition(DataContainer):
            partition_index: int
            committed_offset: int
            committed_leader_epoch: int
            committed_metadata: str | None
            def __init__(
                self,
                *args,
                partition_index: int = ...,
                committed_offset: int = ...,
                committed_leader_epoch: int = ...,
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
        partitions: list[TxnOffsetCommitRequestPartition]
        def __init__(
            self,
            *args,
            name: str = ...,
            partitions: list[TxnOffsetCommitRequestPartition] = ...,
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

    transactional_id: str
    group_id: str
    producer_id: int
    producer_epoch: int
    generation_id: int
    member_id: str
    group_instance_id: str | None
    topics: list[TxnOffsetCommitRequestTopic]
    def __init__(
        self,
        *args,
        transactional_id: str = ...,
        group_id: str = ...,
        producer_id: int = ...,
        producer_epoch: int = ...,
        generation_id: int = ...,
        member_id: str = ...,
        group_instance_id: str | None = ...,
        topics: list[TxnOffsetCommitRequestTopic] = ...,
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

class TxnOffsetCommitResponse(ApiMessage):
    """
    Notes from json schema:
      // Starting in version 1, on quota violation, brokers send out responses before throttling.
      //
      // Version 2 is the same as version 1.
      //
      // Version 3 adds illegal generation, fenced instance id, and unknown member id errors.
      //
      // Version 4 adds support for new error code TRANSACTION_ABORTABLE (KIP-890).
      //
      // Version 5 is the same with version 3 (KIP-890).
    """
    class TxnOffsetCommitResponseTopic(DataContainer):
        class TxnOffsetCommitResponsePartition(DataContainer):
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
        partitions: list[TxnOffsetCommitResponsePartition]
        def __init__(
            self,
            *args,
            name: str = ...,
            partitions: list[TxnOffsetCommitResponsePartition] = ...,
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
    topics: list[TxnOffsetCommitResponseTopic]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        topics: list[TxnOffsetCommitResponseTopic] = ...,
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

class WriteTxnMarkersRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 0 was removed in Apache Kafka 4.0, Version 1 is the new baseline.
      //
      // Version 1 enables flexible versions.
      // Version 2 adds TransactionVersion field to the WritableTxnMarker (KIP-1228).
    """
    class WritableTxnMarker(DataContainer):
        class WritableTxnMarkerTopic(DataContainer):
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

        producer_id: int
        producer_epoch: int
        transaction_result: bool
        topics: list[WritableTxnMarkerTopic]
        coordinator_epoch: int
        transaction_version: int
        def __init__(
            self,
            *args,
            producer_id: int = ...,
            producer_epoch: int = ...,
            transaction_result: bool = ...,
            topics: list[WritableTxnMarkerTopic] = ...,
            coordinator_epoch: int = ...,
            transaction_version: int = ...,
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

    markers: list[WritableTxnMarker]
    def __init__(self, *args, markers: list[WritableTxnMarker] = ..., version: int | None = None, **kwargs) -> None: ...
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

class WriteTxnMarkersResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 0 was removed in Apache Kafka 4.0, Version 1 is the new baseline.
      //
      // Version 1 enables flexible versions.
      // Version 2 matches WriteTxnMarkersRequest version 2 (KIP-1228).
    """
    class WritableTxnMarkerResult(DataContainer):
        class WritableTxnMarkerTopicResult(DataContainer):
            class WritableTxnMarkerPartitionResult(DataContainer):
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
            partitions: list[WritableTxnMarkerPartitionResult]
            def __init__(
                self,
                *args,
                name: str = ...,
                partitions: list[WritableTxnMarkerPartitionResult] = ...,
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

        producer_id: int
        topics: list[WritableTxnMarkerTopicResult]
        def __init__(
            self,
            *args,
            producer_id: int = ...,
            topics: list[WritableTxnMarkerTopicResult] = ...,
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

    markers: list[WritableTxnMarkerResult]
    def __init__(self, *args, markers: list[WritableTxnMarkerResult] = ..., version: int | None = None, **kwargs) -> None: ...
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
    "InitProducerIdRequest",
    "InitProducerIdResponse",
    "AddPartitionsToTxnRequest",
    "AddPartitionsToTxnResponse",
    "AddOffsetsToTxnRequest",
    "AddOffsetsToTxnResponse",
    "EndTxnRequest",
    "EndTxnResponse",
    "TxnOffsetCommitRequest",
    "TxnOffsetCommitResponse",
    "WriteTxnMarkersRequest",
    "WriteTxnMarkersResponse",
]

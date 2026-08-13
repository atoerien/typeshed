import abc
from _typeshed import Incomplete
from enum import IntEnum
from typing import Final, Literal

from kafka.protocol.producer import InitProducerIdRequest
from kafka.structs import ConsumerGroupMetadata

NO_PRODUCER_ID: Final = -1
NO_PRODUCER_EPOCH: Final = -1
NO_SEQUENCE: Final = -1

class ProducerIdAndEpoch:
    __slots__ = ("producer_id", "epoch")
    producer_id: Incomplete
    epoch: Incomplete
    def __init__(self, producer_id, epoch) -> None: ...
    @property
    def is_valid(self): ...
    def match(self, batch): ...
    def __eq__(self, other): ...

class TransactionState(IntEnum):
    """An enumeration."""
    UNINITIALIZED = 0
    INITIALIZING = 1
    READY = 2
    IN_TRANSACTION = 3
    COMMITTING_TRANSACTION = 4
    ABORTING_TRANSACTION = 5
    ABORTABLE_ERROR = 6
    FATAL_ERROR = 7
    BUMPING_PRODUCER_EPOCH = 8
    @classmethod
    def is_transition_valid(cls, source, target): ...

class Priority(IntEnum):
    """An enumeration."""
    FIND_COORDINATOR = 0
    INIT_PRODUCER_ID = 1
    ADD_PARTITIONS_OR_OFFSETS = 2
    END_TXN = 3

class TransactionManager:
    """A class which maintains state for transactions. Also keeps the state necessary to ensure idempotent production."""
    NO_INFLIGHT_REQUEST_CORRELATION_ID: int
    ADD_PARTITIONS_RETRY_BACKOFF_MS: int
    transactional_id: Incomplete
    transaction_timeout_ms: Incomplete
    producer_id_and_epoch: Incomplete
    retry_backoff_ms: Incomplete
    def __init__(
        self,
        transactional_id=None,
        transaction_timeout_ms: int = 0,
        retry_backoff_ms: int = 100,
        api_version=(0, 11),
        metadata=None,
    ) -> None: ...
    def initialize_transactions(self): ...
    def init_producer_id(self) -> None:
        """
        Idempotent (non-transactional) producer: enqueue an InitProducerIdHandler.

        Drives UNINITIALIZED -> INITIALIZING; the handler completes the
        transition to READY on success. No-op outside UNINITIALIZED so
        repeated calls from the sender's run loop are safe.
        """
        ...
    def begin_transaction(self) -> None: ...
    def begin_commit(self): ...
    def begin_abort(self): ...
    def send_offsets_to_transaction(self, offsets, group_metadata: str | ConsumerGroupMetadata):
        """
        Send consumer-group offsets as part of the current transaction.

        Arguments:
            offsets ({TopicPartition: OffsetAndMetadata}): offsets to commit.
            group_metadata (ConsumerGroupMetadata or str): full group metadata
                from KafkaConsumer.group_metadata() (preferred - enables
                broker-side fencing per KIP-447), or a bare group_id string
                for backwards compatibility (broker treats it as v0-v2).

        Returns:
            FutureRecordMetadata-style Future that completes once the offsets
            are durably committed (or fails fatally).
        """
        ...
    def maybe_add_partition_to_transaction(self, topic_partition) -> None: ...
    def is_send_to_partition_allowed(self, tp): ...
    def has_producer_id(self, producer_id=None) -> bool: ...
    def is_transactional(self) -> bool: ...
    def has_partitions_to_add(self) -> bool: ...
    def is_completing(self) -> bool: ...
    @property
    def last_error(self): ...
    def has_error(self) -> bool: ...
    def is_bumping_epoch(self) -> bool: ...
    ERROR_CLASS_RETRIABLE: Final = "RETRIABLE"
    ERROR_CLASS_ABORTABLE: Final = "ABORTABLE"
    ERROR_CLASS_FATAL: Final = "FATAL"
    ERROR_CLASS_NEEDS_EPOCH_BUMP: Final = "NEEDS_EPOCH_BUMP"
    ERROR_CLASS_NEEDS_PRODUCER_ID_RESET: Final = "NEEDS_PRODUCER_ID_RESET"
    def classify_batch_error(
        self, error, batch, log_start_offset=-1
    ) -> Literal["FATAL", "RETRIABLE", "NEEDS_EPOCH_BUMP", "NEEDS_PRODUCER_ID_RESET", "ABORTABLE"]:
        """
        Categorize a batch-completion error into a recovery outcome.

        Used by the Sender to decide what to do with a failed batch. This
        method does not mutate any state - it is a pure classification
        helper. The caller is responsible for dispatching to the
        appropriate recovery path.

        Arguments:
            error (type or BaseException): The error class or instance.
            batch (ProducerBatch): The batch that failed.
            log_start_offset (int): log_start_offset from the broker's
                PartitionProduceResponse, or -1 if unknown / client-side
                failure. Used for KAFKA-5793 retention detection.

        Returns one of:
            ERROR_CLASS_RETRIABLE          - caller should retry the batch
            ERROR_CLASS_ABORTABLE          - transactional producer only;
                                              abort the transaction
            ERROR_CLASS_FATAL              - unrecoverable; transition to
                                              fatal error and fail the batch
            ERROR_CLASS_NEEDS_EPOCH_BUMP   - recoverable via KIP-360 epoch
                                              bump (only when broker supports
                                              InitProducerIdRequest v3+)
            ERROR_CLASS_NEEDS_PRODUCER_ID_RESET - non-transactional pre-KIP-360
                                                   fallback: reset the
                                                   producer id entirely

        Note: this classification is for transactional/idempotent producers
        only. Non-idempotent producers don't call this; the Sender uses
        simpler retry/fail logic for them.
        """
        ...
    def is_aborting(self) -> bool: ...
    def transition_to_abortable_error(self, exc) -> None: ...
    def transition_to_fatal_error(self, exc) -> None: ...
    def is_partition_added(self, partition) -> bool: ...
    def is_partition_pending_add(self, partition) -> bool: ...
    def has_producer_id_and_epoch(self, producer_id, producer_epoch) -> bool: ...
    def set_producer_id_and_epoch(self, producer_id_and_epoch) -> None: ...
    def reset_producer_id(self) -> None:
        """
        This method is used when the producer needs to reset its internal state because of an irrecoverable exception
        from the broker.

        We need to reset the producer id and associated state when we have sent a batch to the broker, but we either get
        a non-retriable exception or we run out of retries, or the batch expired in the producer queue after it was already
        sent to the broker.

        In all of these cases, we don't know whether batch was actually committed on the broker, and hence whether the
        sequence number was actually updated. If we don't reset the producer state, we risk the chance that all future
        messages will return an OutOfOrderSequenceNumberError.

        Note that we can't reset the producer state for the transactional producer as this would mean bumping the epoch
        for the same producer id. This might involve aborting the ongoing transaction during the initProducerIdRequest,
        and the user would not have any way of knowing this happened. So for the transactional producer,
        it's best to return the produce error to the user and let them abort the transaction and close the producer explicitly.
        """
        ...
    def bump_producer_id_and_epoch(self) -> None:
        """
        KIP-360: recover from a transient producer-state error by bumping
        the epoch.

        Transitions to BUMPING_PRODUCER_EPOCH and enqueues an
        InitProducerIdRequest v3+ carrying the current producer_id/epoch.
        When the broker responds with the bumped epoch, _complete_epoch_bump
        transitions back to READY and the sender resumes producing under
        the new epoch. Records in the accumulator that haven't been drained
        yet will be stamped with the new epoch on the next drain.

        TODO (KAFKA-5793 full): in-flight batches at the moment of the bump
        are lost--their futures fail. Adding in-place rewrite of the
        closed batch buffer (producer_id/epoch/base_sequence fields + CRC
        recompute) would let us retry them under the new epoch without
        losing records.

        Requires broker >= 2.5 (InitProducerIdRequest v3+). On older
        brokers, Sender falls back to reset_producer_id / fatal instead
        via classify_batch_error.

        Idempotent: if we're already in BUMPING_PRODUCER_EPOCH, this is a
        no-op. This matters because with max_in_flight > 1, multiple
        in-flight batches may all fail with the same epoch-bump-triggering
        error in quick succession; only the first should drive the bump.
        """
        ...
    def sequence_number(self, tp): ...
    def increment_sequence_number(self, tp, increment) -> None: ...
    def set_sequence_number(self, tp, sequence) -> None: ...
    def reset_sequence_for_partition(self, tp) -> None: ...
    def update_last_acked_offset(self, tp, base_offset, record_count) -> None:
        """
        Record the offset of the last successfully-produced record for tp.

        Called from the sender on each successful batch completion. The
        last acked offset is used to detect whether a subsequent
        UnknownProducerIdError reflects retention (safe to retry) vs. real
        data loss (fatal). See KAFKA-5793.
        """
        ...
    def last_acked_offset(self, tp): ...
    def next_request_handler(self, has_incomplete_batches): ...
    def retry(self, request) -> None: ...
    def authentication_failed(self, exc) -> None: ...
    def coordinator(self, coord_type): ...
    def lookup_coordinator_for_request(self, request) -> None: ...
    def next_in_flight_request_correlation_id(self): ...
    def clear_in_flight_transactional_request_correlation_id(self) -> None: ...
    def has_in_flight_transactional_request(self): ...
    def has_fatal_error(self): ...
    def has_abortable_error(self): ...

class TransactionalRequestResult:
    def __init__(self) -> None: ...
    def done(self, error=None) -> None: ...
    def wait(self, timeout_ms=None): ...
    @property
    def is_done(self): ...
    @property
    def succeeded(self): ...
    @property
    def failed(self): ...
    @property
    def exception(self): ...

class TxnRequestHandler(metaclass=abc.ABCMeta):
    transaction_manager: Incomplete
    retry_backoff_ms: Incomplete
    request: Incomplete
    def __init__(self, transaction_manager, result=None) -> None: ...
    @property
    def transactional_id(self): ...
    @property
    def producer_id(self): ...
    @property
    def producer_epoch(self): ...
    def fatal_error(self, exc) -> None: ...
    def abortable_error(self, exc) -> None: ...
    def fail(self, exc) -> None: ...
    def reenqueue(self) -> None: ...
    def on_complete(self, correlation_id, response_or_exc) -> None: ...
    def needs_coordinator(self): ...
    @property
    def result(self): ...
    @property
    def coordinator_type(self): ...
    @property
    def coordinator_key(self): ...
    def set_retry(self) -> None: ...
    @property
    def is_retry(self): ...
    @abc.abstractmethod
    def handle_response(self, response): ...
    @property
    @abc.abstractmethod
    def priority(self): ...

class InitProducerIdHandler(TxnRequestHandler):
    request: InitProducerIdRequest
    def __init__(self, transaction_manager, transaction_timeout_ms, is_epoch_bump: bool = False) -> None: ...
    @property
    def priority(self): ...
    @property
    def coordinator_type(self): ...
    def handle_response(self, response) -> None: ...

class AddPartitionsToTxnHandler(TxnRequestHandler):
    request: Incomplete
    def __init__(self, transaction_manager, topic_partitions) -> None: ...
    @property
    def priority(self): ...
    retry_backoff_ms: Incomplete
    def handle_response(self, response) -> None: ...
    def maybe_override_retry_backoff_ms(self) -> None: ...

class FindCoordinatorHandler(TxnRequestHandler):
    request: Incomplete
    def __init__(self, transaction_manager, coord_type, coord_key) -> None: ...
    @property
    def priority(self): ...
    @property
    def coordinator_type(self) -> None: ...
    @property
    def coordinator_key(self) -> None: ...
    def handle_response(self, response) -> None: ...

class EndTxnHandler(TxnRequestHandler):
    request: Incomplete
    def __init__(self, transaction_manager, committed) -> None: ...
    @property
    def priority(self): ...
    def handle_response(self, response) -> None: ...

class AddOffsetsToTxnHandler(TxnRequestHandler):
    group_metadata: Incomplete
    consumer_group_id: Incomplete
    offsets: Incomplete
    request: Incomplete
    def __init__(self, transaction_manager, group_metadata, offsets) -> None: ...
    @property
    def priority(self): ...
    def handle_response(self, response) -> None: ...

class TxnOffsetCommitHandler(TxnRequestHandler):
    group_metadata: Incomplete
    consumer_group_id: Incomplete
    offsets: Incomplete
    request: Incomplete
    def __init__(self, transaction_manager, group_metadata, offsets, result) -> None: ...
    @property
    def priority(self): ...
    @property
    def coordinator_type(self): ...
    @property
    def coordinator_key(self): ...
    def handle_response(self, response) -> None: ...

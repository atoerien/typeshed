from _typeshed import Incomplete
from enum import IntEnum

log: Incomplete

class FinalState(IntEnum):
    """An enumeration."""
    ABORTED = 0
    FAILED = 1
    SUCCEEDED = 2

class ProducerBatch:
    max_record_size: int
    created: Incomplete
    drained: Incomplete
    attempts: int
    last_attempt: Incomplete
    last_append: Incomplete
    records: Incomplete
    topic_partition: Incomplete
    produce_future: Incomplete
    def __init__(self, tp, records, now=None) -> None: ...
    @property
    def final_state(self): ...
    @property
    def record_count(self): ...
    @property
    def producer_id(self): ...
    @property
    def producer_epoch(self): ...
    @property
    def has_sequence(self): ...
    def try_append(self, timestamp_ms, key, value, headers, now=None): ...
    def abort(self, exception):
        """Abort the batch and complete the future and callbacks."""
        ...
    def complete(self, base_offset, log_append_time):
        """
        Complete the batch successfully.

        Arguments:
            base_offset (int): The base offset of the messages assigned by the server
            log_append_time (int): The log append time or -1 if CreateTime is being used

        Returns: True if the batch was completed as a result of this call, and False
            if it had been completed previously.
        """
        ...
    def complete_exceptionally(self, top_level_exception, record_exceptions_fn):
        """
        Complete the batch exceptionally. The provided top-level exception will be used
        for each record future contained in the batch.

        Arguments:
            top_level_exception (Exception): top-level partition error.
            record_exceptions_fn (callable int -> Exception): Record exception function mapping
                batch_index to the respective record exception.
        Returns: True if the batch was completed as a result of this call, and False
            if it had been completed previously.
        """
        ...
    def done(self, base_offset=None, timestamp_ms=None, top_level_exception=None, record_exceptions_fn=None):
        """
        Finalize the state of a batch. Final state, once set, is immutable. This function may be called
        once or twice on a batch. It may be called twice if
            1. An inflight batch expires before a response from the broker is received. The batch's final
            state is set to FAILED. But it could succeed on the broker and second time around batch.done() may
            try to set SUCCEEDED final state.

            2. If a transaction abortion happens or if the producer is closed forcefully, the final state is
            ABORTED but again it could succeed if broker responds with a success.

        Attempted transitions from [FAILED | ABORTED] --> SUCCEEDED are logged.
        Attempted transitions from one failure state to the same or a different failed state are ignored.
        Attempted transitions from SUCCEEDED to the same or a failed state throw an exception.
        """
        ...
    def has_reached_delivery_timeout(self, delivery_timeout_ms, now=None): ...
    def in_retry(self): ...
    def retry(self, now=None) -> None: ...
    @property
    def is_done(self): ...
    def __lt__(self, other): ...

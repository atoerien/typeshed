import threading
from _typeshed import Incomplete

class Sender(threading.Thread):
    """
    The background thread that handles the sending of produce requests to the
    Kafka cluster. This thread makes metadata requests to renew its view of the
    cluster and then sends produce requests to the appropriate nodes.
    """
    DEFAULT_CONFIG: dict[str, Incomplete]
    config: dict[str, Incomplete]
    name: Incomplete
    def __init__(self, client, metadata, accumulator, **configs) -> None: ...
    def run(self) -> None:
        """The main run loop for the sender thread."""
        ...
    def run_once(self) -> None:
        """Run a single iteration of sending."""
        ...
    def initiate_close(self) -> None:
        """Start closing the sender (won't complete until all data is sent)."""
        ...
    def force_close(self) -> None:
        """Closes the sender without sending out any pending messages."""
        ...
    def add_topic(self, topic) -> None: ...
    def wakeup(self) -> None:
        """Wake up the selector associated with this send thread."""
        ...
    def bootstrap_connected(self): ...

class SenderMetrics:
    metrics: Incomplete
    batch_size_sensor: Incomplete
    compression_rate_sensor: Incomplete
    queue_time_sensor: Incomplete
    records_per_request_sensor: Incomplete
    byte_rate_sensor: Incomplete
    retry_sensor: Incomplete
    error_sensor: Incomplete
    max_record_size_sensor: Incomplete
    def __init__(self, metrics, client, metadata) -> None: ...
    def add_metric(
        self, metric_name, measurable, group_name: str = "producer-metrics", description=None, tags=None, sensor_name=None
    ) -> None: ...
    def maybe_register_topic_metrics(self, topic) -> None: ...
    def update_produce_request_metrics(self, batches_map) -> None: ...
    def record_retries(self, topic, count) -> None: ...
    def record_errors(self, topic, count) -> None: ...

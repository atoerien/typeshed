"""Metrics for kafka.net connection manager and connections."""

from _typeshed import Incomplete

class KafkaManagerMetrics:
    """
    Metrics for KafkaConnectionManager (equivalent to KafkaClientMetrics).
    Note that kafka.net does not track select_time or io_time.
    """
    metrics: Incomplete
    connection_closed: Incomplete
    connection_created: Incomplete
    def __init__(self, metrics, metric_group_prefix: str, conns) -> None: ...

class KafkaConnectionMetrics:
    """Metrics for a single KafkaConnection (equivalent to BrokerConnectionMetrics)."""
    metrics: Incomplete
    bytes_sent: Incomplete
    bytes_received: Incomplete
    request_time: Incomplete
    throttle_time: Incomplete
    def __init__(self, metrics, metric_group_prefix: str, node_id) -> None: ...

from kafka.metrics.metrics_reporter import AbstractMetricsReporter

class DictReporter(AbstractMetricsReporter):
    """
    A basic dictionary based metrics reporter.

    Store all metrics in a two level dictionary of category > name > metric.
    """
    def __init__(self, prefix: str = "") -> None: ...
    def snapshot(self):
        """
        Return a nested dictionary snapshot of all metrics and their
        values at this time. Example:
        {
            'category': {
                'metric1_name': 42.0,
                'metric2_name': 'foo'
            }
        }
        """
        ...
    def init(self, metrics) -> None: ...
    def metric_change(self, metric) -> None: ...
    def metric_removal(self, metric): ...
    def get_category(self, metric) -> str: ...
    def configure(self, configs) -> None: ...
    def close(self) -> None: ...

from _typeshed import Incomplete

class MetricConfig:
    """Configuration values for metrics"""
    quota: Incomplete
    event_window: Incomplete
    time_window_ms: Incomplete
    tags: Incomplete
    def __init__(self, quota=None, samples: int = 2, event_window=..., time_window_ms=30000, tags=None) -> None:
        """
        Arguments:
            quota (Quota, optional): Upper or lower bound of a value.
            samples (int, optional): Max number of samples kept per metric.
            event_window (int, optional): Max number of values per sample.
            time_window_ms (int, optional): Max age of an individual sample.
            tags (dict of {str: str}, optional): Tags for each metric.
        """
        ...

    @property
    def samples(self): ...
    @samples.setter
    def samples(self, value) -> None: ...

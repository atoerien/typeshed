import abc

from kafka.metrics.stat import AbstractStat

class AbstractCompoundStat(AbstractStat, metaclass=abc.ABCMeta):
    """
    A compound stat is a stat where a single measurement and associated
    data structure feeds many metrics. This is the example for a
    histogram which has many associated percentiles.
    """
    def stats(self) -> None:
        """Return list of NamedMeasurable"""
        ...

class NamedMeasurable:
    def __init__(self, metric_name, measurable_stat) -> None: ...
    @property
    def name(self): ...
    @property
    def stat(self): ...

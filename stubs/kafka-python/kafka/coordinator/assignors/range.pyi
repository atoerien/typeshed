from _typeshed import Incomplete

from kafka.coordinator.assignors.abstract import AbstractPartitionAssignor

log: Incomplete

class RangePartitionAssignor(AbstractPartitionAssignor):
    """
    The range assignor works on a per-topic basis. For each topic, we lay out
    the available partitions in numeric order and the consumers in
    lexicographic order. We then divide the number of partitions by the total
    number of consumers to determine the number of partitions to assign to each
    consumer. If it does not evenly divide, then the first few consumers will
    have one extra partition.

    For example, suppose there are two consumers C0 and C1, two topics t0 and
    t1, and each topic has 3 partitions, resulting in partitions t0p0, t0p1,
    t0p2, t1p0, t1p1, and t1p2.

    The assignment will be:
        C0: [t0p0, t0p1, t1p0, t1p1]
        C1: [t0p2, t1p2]
    """
    name: str
    version: int
    @classmethod
    def assign(cls, cluster, group_subscriptions): ...
    @classmethod
    def metadata(cls, topics): ...
    @classmethod
    def on_assignment(cls, assignment) -> None: ...

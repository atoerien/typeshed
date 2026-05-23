from collections.abc import Mapping, Sequence

class NewTopic:
    """
    A class for new topic creation
    Arguments:
        name (string): name of the topic
        num_partitions (int): number of partitions
            or -1 if replica_assignment has been specified
        replication_factor (int): replication factor or -1 if
            replica assignment is specified
        replica_assignment (dict of int: [int]): A mapping containing
            partition id and replicas to assign to it.
        topic_configs (dict of str: str): A mapping of config key
            and value for the topic.
    """
    name: str
    num_partitions: int
    replication_factor: int
    replica_assignments: Mapping[int, Sequence[int]] | None
    topic_configs: Mapping[str, str] | None
    def __init__(
        self,
        name: str,
        num_partitions: int = -1,
        replication_factor: int = -1,
        replica_assignments: Mapping[int, Sequence[int]] | None = None,
        topic_configs: Mapping[str, str] | None = None,
    ) -> None: ...

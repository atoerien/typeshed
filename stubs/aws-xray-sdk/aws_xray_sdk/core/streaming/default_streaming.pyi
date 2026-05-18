from _typeshed import Unused
from collections.abc import Callable

from aws_xray_sdk.core.models.entity import Entity
from aws_xray_sdk.core.models.segment import Segment

class DefaultStreaming:
    """
    The default streaming strategy. It uses the total count of a
    segment's children subsegments as a threshold. If the threshold is
    breached, it uses subtree streaming to stream out.
    """
    def __init__(self, streaming_threshold: int = 30) -> None: ...
    def is_eligible(self, segment: Segment) -> bool: ...
    def stream(self, entity: Entity, callback: Callable[..., Unused]) -> None: ...

    @property
    def streaming_threshold(self) -> int: ...
    @streaming_threshold.setter
    def streaming_threshold(self, value: int) -> None: ...

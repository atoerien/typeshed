from _typeshed import Incomplete
from typing import Final

from kafka.protocol.api_data import ApiData
from kafka.protocol.data_container import DataContainer

ConsumerProtocolType: Final = "consumer"

class ConsumerProtocolSubscription(ApiData):
    """
    Notes from json schema:
      // Subscription part of the Consumer Protocol.
      //
      // The current implementation assumes that future versions will not break compatibility. When
      // it encounters a newer version, it parses it using the current format. This basically means
      // that new versions cannot remove or reorder any of the existing fields.

      // Version 1 added the "OwnedPartitions" field to allow assigner know what partitions each member owned
      // Version 2 added a new field "GenerationId" to indicate if the member has out-of-date ownedPartitions.
      // Version 3 adds rack id to enable rack-aware assignment.
    """
    class TopicPartition(DataContainer):
        topic: str
        partitions: list[int]
        def __init__(
            self, *args, topic: str = ..., partitions: list[int] = ..., version: int | None = None, **kwargs
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    topics: list[str]
    user_data: bytes | ApiData | None
    owned_partitions: list[TopicPartition]
    generation_id: int
    rack_id: str | None
    def __init__(
        self,
        *args,
        topics: list[str] = ...,
        user_data: bytes | ApiData | None = ...,
        owned_partitions: list[TopicPartition] = ...,
        generation_id: int = ...,
        rack_id: str | None = ...,
        version: int | None = None,
        **kwargs,
    ) -> None: ...
    @property
    def version(self) -> int | None: ...
    def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
        """
        Use meta=True to include top-level version; meta='all' to include all internal versions
        json=False to return raw encoding; json=True (default) to convert values to be json-serializable
        """
        ...
    name: str
    type: str
    valid_versions: tuple[int, int]
    min_version: int
    max_version: int

class ConsumerProtocolAssignment(ApiData):
    """
    Notes from json schema:
      // Assignment part of the Consumer Protocol.
      //
      // The current implementation assumes that future versions will not break compatibility. When
      // it encounters a newer version, it parses it using the current format. This basically means
      // that new versions cannot remove or reorder any of the existing fields.
      //
      // Version 2 is to support a new field "GenerationId" in ConsumerProtocolSubscription.
      // Version 3 adds rack id to ConsumerProtocolSubscription.
    """
    class TopicPartition(DataContainer):
        topic: str
        partitions: list[int]
        def __init__(
            self, *args, topic: str = ..., partitions: list[int] = ..., version: int | None = None, **kwargs
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    assigned_partitions: list[TopicPartition]
    user_data: bytes | ApiData | None
    def __init__(
        self,
        *args,
        assigned_partitions: list[TopicPartition] = ...,
        user_data: bytes | ApiData | None = ...,
        version: int | None = None,
        **kwargs,
    ) -> None: ...
    @property
    def version(self) -> int | None: ...
    def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
        """
        Use meta=True to include top-level version; meta='all' to include all internal versions
        json=False to return raw encoding; json=True (default) to convert values to be json-serializable
        """
        ...
    name: str
    type: str
    valid_versions: tuple[int, int]
    min_version: int
    max_version: int

    @property
    def assignment(self) -> list[TopicPartition]: ...
    @assignment.setter
    def assignment(self, value: list[TopicPartition]) -> None: ...

    def partitions(self) -> list[TopicPartition]: ...

__all__ = ["ConsumerProtocolSubscription", "ConsumerProtocolAssignment", "ConsumerProtocolType"]

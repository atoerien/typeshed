import uuid
from _typeshed import Incomplete

from kafka.protocol.api_message import ApiMessage
from kafka.protocol.data_container import DataContainer

class MetadataRequest(ApiMessage):
    """
    Notes from json schema:
        // In version 0, an empty array indicates "request metadata for all topics."  In version 1 and
        // higher, an empty array indicates "request metadata for no topics," and a null array is used to
        // indicate "request metadata for all topics."
        //
        // Version 2 and 3 are the same as version 1.
        //
        // Version 4 adds AllowAutoTopicCreation.
        //
        // Starting in version 8, authorized operations can be requested for cluster and topic resource.
        //
        // Version 9 is the first flexible version.
        //
        // Version 10 adds topicId and allows name field to be null. However, this functionality was not implemented on the server.
        // Versions 10 and 11 should not use the topicId field or set topic name to null.
        //
        // Version 11 deprecates IncludeClusterAuthorizedOperations field. This is now exposed
        // by the DescribeCluster API (KIP-700).
        // Version 12 supports topic Id.
        // Version 13 supports top-level error code in the response.
    """
    ALL_TOPICS: Incomplete | None
    NO_TOPICS: list[Incomplete]

    class MetadataRequestTopic(DataContainer):
        topic_id: uuid.UUID
        name: str | None
        def __init__(
            self, *args, topic_id: uuid.UUID = ..., name: str | None = ..., version: int | None = None, **kwargs
        ) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    topics: list[MetadataRequestTopic] | None
    allow_auto_topic_creation: bool
    include_cluster_authorized_operations: bool
    include_topic_authorized_operations: bool
    def __init__(
        self,
        *args,
        topics: list[MetadataRequestTopic] | None = ...,
        allow_auto_topic_creation: bool = ...,
        include_cluster_authorized_operations: bool = ...,
        include_topic_authorized_operations: bool = ...,
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
    API_KEY: int
    API_VERSION: int
    valid_versions: tuple[int, int]
    min_version: int
    max_version: int
    @property
    def header(self): ...
    @classmethod
    def is_request(cls) -> bool: ...
    def expect_response(self) -> bool: ...
    def with_header(self, correlation_id: int = 0, client_id: str = "kafka-python") -> None: ...
    def encode(self, version=None, header=False, framed=False): ...

class MetadataResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 1 adds fields for the rack of each broker, the controller id, and whether or not the topic is internal.
      //
      // Version 2 adds the cluster ID field.
      //
      // Version 3 adds the throttle time.
      //
      // Version 4 is the same as version 3.
      //
      // Version 5 adds a per-partition offline_replicas field. This field specifies
      // the list of replicas that are offline.
      //
      // Starting in version 6, on quota violation, brokers send out responses before throttling.
      //
      // Version 7 adds the leader epoch to the partition metadata.
      //
      // Starting in version 8, brokers can send authorized operations for topic and cluster.
      //
      // Version 9 is the first flexible version.
      //
      // Version 10 adds topicId.
      //
      // Version 11 deprecates ClusterAuthorizedOperations. This is now exposed
      // by the DescribeCluster API (KIP-700).
      // Version 12 supports topicId.
      // Version 13 supports top-level error code in the response.
    """
    class MetadataResponseBroker(DataContainer):
        node_id: int
        host: str
        port: int
        rack: str | None
        def __init__(
            self,
            *args,
            node_id: int = ...,
            host: str = ...,
            port: int = ...,
            rack: str | None = ...,
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

    class MetadataResponseTopic(DataContainer):
        class MetadataResponsePartition(DataContainer):
            error_code: int
            partition_index: int
            leader_id: int
            leader_epoch: int
            replica_nodes: list[int]
            isr_nodes: list[int]
            offline_replicas: list[int]
            def __init__(
                self,
                *args,
                error_code: int = ...,
                partition_index: int = ...,
                leader_id: int = ...,
                leader_epoch: int = ...,
                replica_nodes: list[int] = ...,
                isr_nodes: list[int] = ...,
                offline_replicas: list[int] = ...,
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

        error_code: int
        name: str | None
        topic_id: uuid.UUID
        is_internal: bool
        partitions: list[MetadataResponsePartition]
        authorized_operations: set[int]
        def __init__(
            self,
            *args,
            error_code: int = ...,
            name: str | None = ...,
            topic_id: uuid.UUID = ...,
            is_internal: bool = ...,
            partitions: list[MetadataResponsePartition] = ...,
            authorized_operations: set[int] = ...,
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

    throttle_time_ms: int
    brokers: list[MetadataResponseBroker]
    cluster_id: str | None
    controller_id: int
    topics: list[MetadataResponseTopic]
    authorized_operations: set[int]
    error_code: int
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        brokers: list[MetadataResponseBroker] = ...,
        cluster_id: str | None = ...,
        controller_id: int = ...,
        topics: list[MetadataResponseTopic] = ...,
        authorized_operations: set[int] = ...,
        error_code: int = ...,
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
    API_KEY: int
    API_VERSION: int
    valid_versions: tuple[int, int]
    min_version: int
    max_version: int
    @property
    def header(self): ...
    @classmethod
    def is_request(cls) -> bool: ...
    def expect_response(self) -> bool: ...
    def with_header(self, correlation_id: int = 0, client_id: str = "kafka-python") -> None: ...
    @classmethod
    def json_patch(cls, json): ...

__all__ = ["MetadataRequest", "MetadataResponse"]

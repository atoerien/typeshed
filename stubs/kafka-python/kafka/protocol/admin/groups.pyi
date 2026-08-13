from _typeshed import Incomplete

from kafka.protocol.api_data import ApiData
from kafka.protocol.api_message import ApiMessage
from kafka.protocol.data_container import DataContainer

class DescribeGroupsRequest(ApiMessage):
    """
    Notes from json schema:
      // Versions 1 and 2 are the same as version 0.
      //
      // Starting in version 3, authorized operations can be requested.
      //
      // Starting in version 4, the response will include group.instance.id info for members.
      //
      // Version 5 is the first flexible version.
      //
      // Version 6 returns error code GROUP_ID_NOT_FOUND if the group ID is not found (KIP-1043).
    """
    groups: list[str]
    include_authorized_operations: bool
    def __init__(
        self, *args, groups: list[str] = ..., include_authorized_operations: bool = ..., version: int | None = None, **kwargs
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

class DescribeGroupsResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 1 added throttle time.
      //
      // Starting in version 2, on quota violation, brokers send out responses before throttling.
      //
      // Starting in version 3, brokers can send authorized operations.
      //
      // Starting in version 4, the response will optionally include group.instance.id info for members.
      //
      // Version 5 is the first flexible version.
      //
      // Version 6 returns error code GROUP_ID_NOT_FOUND if the group ID is not found (KIP-1043).
    """
    class DescribedGroup(DataContainer):
        class DescribedGroupMember(DataContainer):
            member_id: str
            group_instance_id: str | None
            client_id: str
            client_host: str
            member_metadata: bytes | ApiData
            member_assignment: bytes | ApiData
            def __init__(
                self,
                *args,
                member_id: str = ...,
                group_instance_id: str | None = ...,
                client_id: str = ...,
                client_host: str = ...,
                member_metadata: bytes | ApiData = ...,
                member_assignment: bytes | ApiData = ...,
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
        error_message: str | None
        group_id: str
        group_state: str
        protocol_type: str
        protocol_data: str
        members: list[DescribedGroupMember]
        authorized_operations: set[int]
        def __init__(
            self,
            *args,
            error_code: int = ...,
            error_message: str | None = ...,
            group_id: str = ...,
            group_state: str = ...,
            protocol_type: str = ...,
            protocol_data: str = ...,
            members: list[DescribedGroupMember] = ...,
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
    groups: list[DescribedGroup]
    def __init__(
        self, *args, throttle_time_ms: int = ..., groups: list[DescribedGroup] = ..., version: int | None = None, **kwargs
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

class ListGroupsRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 and 2 are the same as version 0.
      //
      // Version 3 is the first flexible version.
      //
      // Version 4 adds the StatesFilter field (KIP-518).
      //
      // Version 5 adds the TypesFilter field (KIP-848).
    """
    states_filter: list[str]
    types_filter: list[str]
    def __init__(
        self, *args, states_filter: list[str] = ..., types_filter: list[str] = ..., version: int | None = None, **kwargs
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

class ListGroupsResponse(ApiMessage):
    """
    Notes from json schema:
      // Version 1 adds the throttle time.
      //
      // Starting in version 2, on quota violation, brokers send out
      // responses before throttling.
      //
      // Version 3 is the first flexible version.
      //
      // Version 4 adds the GroupState field (KIP-518).
      //
      // Version 5 adds the GroupType field (KIP-848).
    """
    class ListedGroup(DataContainer):
        group_id: str
        protocol_type: str
        group_state: str
        group_type: str
        def __init__(
            self,
            *args,
            group_id: str = ...,
            protocol_type: str = ...,
            group_state: str = ...,
            group_type: str = ...,
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
    error_code: int
    groups: list[ListedGroup]
    def __init__(
        self,
        *args,
        throttle_time_ms: int = ...,
        error_code: int = ...,
        groups: list[ListedGroup] = ...,
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

class DeleteGroupsRequest(ApiMessage):
    """
    Notes from json schema:
      // Version 1 is the same as version 0.
      //
      // Version 2 is the first flexible version.
    """
    groups_names: list[str]
    def __init__(self, *args, groups_names: list[str] = ..., version: int | None = None, **kwargs) -> None: ...
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

class DeleteGroupsResponse(ApiMessage):
    """
    Notes from json schema:
      // Starting in version 1, on quota violation, brokers send out responses before throttling.
      //
      // Version 2 is the first flexible version.
    """
    class DeletableGroupResult(DataContainer):
        group_id: str
        error_code: int
        def __init__(self, *args, group_id: str = ..., error_code: int = ..., version: int | None = None, **kwargs) -> None: ...
        @property
        def version(self) -> int | None: ...
        def to_dict(self, meta: bool = False, json: bool = True) -> dict[Incomplete, Incomplete]:
            """
            Use meta=True to include top-level version; meta='all' to include all internal versions
            json=False to return raw encoding; json=True (default) to convert values to be json-serializable
            """
            ...

    throttle_time_ms: int
    results: list[DeletableGroupResult]
    def __init__(
        self, *args, throttle_time_ms: int = ..., results: list[DeletableGroupResult] = ..., version: int | None = None, **kwargs
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

__all__ = [
    "DescribeGroupsRequest",
    "DescribeGroupsResponse",
    "ListGroupsRequest",
    "ListGroupsResponse",
    "DeleteGroupsRequest",
    "DeleteGroupsResponse",
]

"""
ACL management mixin for KafkaAdminClient.

Also defines ACL data types: ResourceType, ACLOperation, ACLPermissionType,
ACLResourcePatternType, ACLFilter, ACL, ResourcePatternFilter, ResourcePattern.
"""

from _typeshed import Incomplete
from collections.abc import Sequence
from enum import IntEnum
from typing import TypedDict, type_check_only

from kafka.errors import KafkaError

@type_check_only
class _CreateAclsResult(TypedDict):
    succeeded: list[ACL]
    failed: list[type[KafkaError]]

class ACLAdminMixin:
    """Mixin providing ACL management methods for KafkaAdminClient."""
    config: dict[Incomplete, Incomplete]
    def describe_acls(self, acl_filter: ACLFilter) -> tuple[list[ACL], type[KafkaError]]:
        """
        Describe a set of ACLs

        Used to return a set of ACLs matching the supplied ACLFilter.
        The cluster must be configured with an authorizer for this to work, or
        you will get a SecurityDisabledError

        Arguments:
            acl_filter: an ACLFilter object

        Returns:
            tuple of a list of matching ACL objects and a KafkaError (NoError if successful)
        """
        ...
    def create_acls(self, acls: Sequence[ACL]) -> _CreateAclsResult:
        """
        Create a list of ACLs

        This endpoint only accepts a list of concrete ACL objects, no ACLFilters.
        Throws TopicAlreadyExistsError if topic is already present.

        Arguments:
            acls: a list of ACL objects

        Returns:
            dict of successes and failures
        """
        ...
    def delete_acls(self, acl_filters: Sequence[ACLFilter]) -> list[tuple[ACLFilter, list[ACL], type[KafkaError]]]:
        """
        Delete a set of ACLs

        Deletes all ACLs matching the list of input ACLFilter

        Arguments:
            acl_filters: a list of ACLFilter

        Returns:
            a list of 3-tuples corresponding to the list of input filters.
                 The tuples hold (the input ACLFilter, list of affected ACLs, KafkaError instance)
        """
        ...

class ResourceType(IntEnum):
    """
    Type of kafka resource to set ACL for.

    The ANY value is only valid in a filter context.
    """
    UNKNOWN = 0
    ANY = 1
    TOPIC = 2
    GROUP = 3
    CLUSTER = 4
    TRANSACTIONAL_ID = 5
    DELEGATION_TOKEN = 6
    USER = 7

class ACLOperation(IntEnum):
    """
    Type of operation.

    The ANY value is only valid in a filter context.
    """
    UNKNOWN = 0
    ANY = 1
    ALL = 2
    READ = 3
    WRITE = 4
    CREATE = 5
    DELETE = 6
    ALTER = 7
    DESCRIBE = 8
    CLUSTER_ACTION = 9
    DESCRIBE_CONFIGS = 10
    ALTER_CONFIGS = 11
    IDEMPOTENT_WRITE = 12
    CREATE_TOKENS = 13
    DESCRIBE_TOKENS = 14

class ACLPermissionType(IntEnum):
    """
    An enumerated type of permissions.

    The ANY value is only valid in a filter context.
    """
    UNKNOWN = 0
    ANY = 1
    DENY = 2
    ALLOW = 3

class ACLResourcePatternType(IntEnum):
    """
    An enumerated type of resource patterns.

    More details on the pattern types and how they work
    can be found in KIP-290 (Support for prefixed ACLs).
    """
    UNKNOWN = 0
    ANY = 1
    MATCH = 2
    LITERAL = 3
    PREFIXED = 4

class ResourcePatternFilter:
    resource_type: ResourceType
    resource_name: str | None
    pattern_type: ACLResourcePatternType
    def __init__(self, resource_type: ResourceType, resource_name: str | None, pattern_type: ACLResourcePatternType) -> None: ...
    def validate(self) -> None: ...
    def __eq__(self, other: ResourcePatternFilter) -> bool: ...  # type: ignore[override]
    def __hash__(self) -> int: ...

class ResourcePattern(ResourcePatternFilter):
    """A resource pattern to apply the ACL to."""
    resource_name: str
    def __init__(
        self,
        resource_type: ResourceType,
        resource_name: str,
        pattern_type: ACLResourcePatternType = ACLResourcePatternType.LITERAL,
    ) -> None: ...
    def validate(self) -> None: ...

class ACLFilter:
    """Represents a filter to use with describing and deleting ACLs."""
    principal: str | None
    host: str | None
    operation: ACLOperation
    permission_type: ACLPermissionType
    resource_pattern: ResourcePatternFilter
    def __init__(
        self,
        principal: str | None,
        host: str | None,
        operation: ACLOperation,
        permission_type: ACLPermissionType,
        resource_pattern: ResourcePatternFilter,
    ) -> None: ...
    def validate(self) -> None: ...
    def __eq__(self, other: ACLFilter) -> bool: ...  # type: ignore[override]
    def __hash__(self) -> int: ...

class ACL(ACLFilter):
    """Represents a concrete ACL for a specific ResourcePattern."""
    resource_pattern: ResourcePattern
    def __init__(
        self,
        principal: str,
        host: str,
        operation: ACLOperation,
        permission_type: ACLPermissionType,
        resource_pattern: ResourcePattern,
    ) -> None: ...
    def validate(self) -> None: ...

def valid_acl_operations(int_vals) -> set[ACLOperation]: ...

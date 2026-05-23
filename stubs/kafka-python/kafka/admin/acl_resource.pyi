from enum import IntEnum

class ResourceType(IntEnum):
    """
    Type of kafka resource to set ACL for

    The ANY value is only valid in a filter context
    """
    UNKNOWN = 0
    ANY = 1
    CLUSTER = 4
    DELEGATION_TOKEN = 6
    GROUP = 3
    TOPIC = 2
    TRANSACTIONAL_ID = 5

class ACLOperation(IntEnum):
    """
    Type of operation

    The ANY value is only valid in a filter context
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
    DESCRIBE_TOKENS = 13

class ACLPermissionType(IntEnum):
    """
    An enumerated type of permissions

    The ANY value is only valid in a filter context
    """
    UNKNOWN = 0
    ANY = 1
    DENY = 2
    ALLOW = 3

class ACLResourcePatternType(IntEnum):
    """
    An enumerated type of resource patterns

    More details on the pattern types and how they work
    can be found in KIP-290 (Support for prefixed ACLs)
    https://cwiki.apache.org/confluence/display/KAFKA/KIP-290%3A+Support+for+Prefixed+ACLs
    """
    UNKNOWN = 0
    ANY = 1
    MATCH = 2
    LITERAL = 3
    PREFIXED = 4

class ACLFilter:
    """
    Represents a filter to use with describing and deleting ACLs

    The difference between this class and the ACL class is mainly that
    we allow using ANY with the operation, permission, and resource type objects
    to fetch ALCs matching any of the properties.

    To make a filter matching any principal, set principal to None
    """
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
    def __eq__(self, other): ...
    def __hash__(self): ...

class ACL(ACLFilter):
    """
    Represents a concrete ACL for a specific ResourcePattern

    In kafka an ACL is a 4-tuple of (principal, host, operation, permission_type)
    that limits who can do what on a specific resource (or since KIP-290 a resource pattern)

    Terminology:
    Principal -> This is the identifier for the user. Depending on the authorization method used (SSL, SASL etc)
        the principal will look different. See http://kafka.apache.org/documentation/#security_authz for details.
        The principal must be on the format "User:<name>" or kafka will treat it as invalid. It's possible to use
        other principal types than "User" if using a custom authorizer for the cluster.
    Host -> This must currently be an IP address. It cannot be a range, and it cannot be a domain name.
        It can be set to "*", which is special cased in kafka to mean "any host"
    Operation -> Which client operation this ACL refers to. Has different meaning depending
        on the resource type the ACL refers to. See https://docs.confluent.io/current/kafka/authorization.html#acl-format
        for a list of which combinations of resource/operation that unlocks which kafka APIs
    Permission Type: Whether this ACL is allowing or denying access
    Resource Pattern -> This is a representation of the resource or resource pattern that the ACL
        refers to. See the ResourcePattern class for details.
    """
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

class ResourcePatternFilter:
    resource_type: ResourceType
    resource_name: str | None
    pattern_type: ACLResourcePatternType
    def __init__(self, resource_type: ResourceType, resource_name: str | None, pattern_type: ACLResourcePatternType) -> None: ...
    def validate(self) -> None: ...
    def __eq__(self, other): ...
    def __hash__(self): ...

class ResourcePattern(ResourcePatternFilter):
    """
    A resource pattern to apply the ACL to

    Resource patterns are used to be able to specify which resources an ACL
    describes in a more flexible way than just pointing to a literal topic name for example.
    Since KIP-290 (kafka 2.0) it's possible to set an ACL for a prefixed resource name, which
    can cut down considerably on the number of ACLs needed when the number of topics and
    consumer groups start to grow.
    The default pattern_type is LITERAL, and it describes a specific resource. This is also how
    ACLs worked before the introduction of prefixed ACLs
    """
    resource_name: str
    def __init__(
        self,
        resource_type: ResourceType,
        resource_name: str,
        pattern_type: ACLResourcePatternType = ACLResourcePatternType.LITERAL,
    ) -> None: ...
    def validate(self) -> None: ...

def valid_acl_operations(int_vals) -> set[ACLOperation]: ...

from _typeshed import Incomplete

class BrokerVersionData:
    __slots__ = ("broker_version", "api_versions")
    broker_version: Incomplete
    api_versions: Incomplete
    def __init__(self, broker_version=None, api_versions=None) -> None: ...
    def api_version(self, operation, min_version: int = 0, max_version: int = ...) -> int:
        """
        Find the latest version of the protocol operation supported by both
        this library and the broker.

        This resolves to the lesser of the latest api version this
        library supports, the max version supported by the broker,
        or optionally a max_version provided by the caller, or specified on
        the request instance.

        Arguments:
            operation: A protocol request class or instance from kafka.protocol.

        Keyword Arguments:
            min_version (int, optional): Provide an alternate minimum api version.
            max_version (int, optional): Provide an alternate maximum api version.
                to reflect limitations in user code.

        Returns:
            int: The highest api version number compatible between client and broker.

        Raises:
            IncompatibleBrokerVersion: if no matching version is found.
            ValueError: if min_version > max_version.
        """
        ...
    @property
    def broker_version_str(self) -> str: ...
    def __eq__(self, other) -> bool: ...
    def __lt__(self, other) -> bool: ...
    def __le__(self, other) -> bool:
        """Return a <= b.  Computed by @total_ordering from (a < b) or (a == b)."""
        ...
    def __gt__(self, other) -> bool:
        """Return a > b.  Computed by @total_ordering from (not a < b) and (a != b)."""
        ...
    def __ge__(self, other) -> bool:
        """Return a >= b.  Computed by @total_ordering from (not a < b)."""
        ...

def infer_broker_version_from_api_versions(api_versions): ...

VERSION_CHECKS: tuple[tuple[tuple[int, ...], Incomplete], ...]
BROKER_API_VERSIONS: dict[tuple[int, ...], dict[int, tuple[int, ...]]]

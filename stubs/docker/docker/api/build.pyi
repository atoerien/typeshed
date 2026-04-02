from collections.abc import Generator
from io import StringIO
from logging import Logger
from typing import IO, Any, TypedDict, type_check_only

log: Logger

@type_check_only
class _ContainerLimits(TypedDict, total=False):
    memory: int
    memswap: int
    cpushares: int
    cpusetcpus: str

@type_check_only
class _Filers(TypedDict, total=False):
    dangling: bool
    until: str

class BuildApiMixin:
    def build(
        self,
        path: str | None = None,
        tag: str | None = None,
        quiet: bool = False,
        fileobj: StringIO | IO[bytes] | None = None,
        nocache: bool = False,
        rm: bool = False,
        timeout: int | None = None,
        custom_context: bool = False,
        encoding: str | None = None,
        pull: bool = False,
        forcerm: bool = False,
        dockerfile: str | None = None,
        container_limits: _ContainerLimits | None = None,
        decode: bool = False,
        buildargs: dict[str, Any] | None = None,
        gzip: bool = False,
        shmsize: int | None = None,
        labels: dict[str, Any] | None = None,
        # need to use list, because the type must be json serializable
        cache_from: list[str] | None = None,
        target: str | None = None,
        network_mode: str | None = None,
        squash: bool | None = None,
        extra_hosts: list[str] | dict[str, str] | None = None,
        platform: str | None = None,
        isolation: str | None = None,
        use_config_proxy: bool = True,
    ) -> Generator[Any]: ...
    def prune_builds(
        self, filters: _Filers | None = None, keep_storage: int | None = None, all: bool | None = None
    ) -> dict[str, Any]:
        """
        Delete the builder cache

        Args:
            filters (dict): Filters to process on the prune list.
                Needs Docker API v1.39+
                Available filters:
                - dangling (bool):  When set to true (or 1), prune only
                unused and untagged images.
                - until (str): Can be Unix timestamps, date formatted
                timestamps, or Go duration strings (e.g. 10m, 1h30m) computed
                relative to the daemon's local time.
            keep_storage (int): Amount of disk space in bytes to keep for cache.
                Needs Docker API v1.39+
            all (bool): Remove all types of build cache.
                Needs Docker API v1.39+

        Returns:
            (dict): A dictionary containing information about the operation's
                    result. The ``SpaceReclaimed`` key indicates the amount of
                    bytes of disk space reclaimed.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...

def process_dockerfile(dockerfile: str | None, path: str) -> tuple[str | None, str | None]: ...

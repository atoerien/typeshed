from _typeshed import Incomplete
from collections.abc import Iterable, Mapping
from datetime import datetime
from typing import Any, Literal, NoReturn, Protocol, overload, type_check_only

from docker import APIClient
from docker.models.configs import ConfigCollection
from docker.models.containers import ContainerCollection
from docker.models.images import ImageCollection
from docker.models.networks import NetworkCollection
from docker.models.nodes import NodeCollection
from docker.models.plugins import PluginCollection
from docker.models.secrets import SecretCollection
from docker.models.services import ServiceCollection
from docker.models.swarm import Swarm
from docker.models.volumes import VolumeCollection
from docker.tls import TLSConfig
from docker.types import CancellableStream

@type_check_only
class _Environ(Protocol):
    def __getitem__(self, k: str, /) -> str: ...
    def keys(self) -> Iterable[str]: ...

class DockerClient:
    """
    A client for communicating with a Docker server.

    Example:

        >>> import docker
        >>> client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    Args:
        base_url (str): URL to the Docker server. For example,
            ``unix:///var/run/docker.sock`` or ``tcp://127.0.0.1:1234``.
        version (str): The version of the API to use. Set to ``auto`` to
            automatically detect the server's version. Default: ``1.35``
        timeout (int): Default timeout for API calls, in seconds.
        tls (bool or :py:class:`~docker.tls.TLSConfig`): Enable TLS. Pass
            ``True`` to enable it with default options, or pass a
            :py:class:`~docker.tls.TLSConfig` object to use custom
            configuration.
        user_agent (str): Set a custom user agent for requests to the server.
        credstore_env (dict): Override environment variables when calling the
            credential store process.
        use_ssh_client (bool): If set to `True`, an ssh connection is made
            via shelling out to the ssh client. Ensure the ssh client is
            installed and configured on the host.
        max_pool_size (int): The maximum number of connections
            to save in the pool.
    """
    api: APIClient
    # Please keep in sync with docker.APIClient
    def __init__(
        self,
        base_url: str | None = None,
        version: str | None = None,
        timeout: int = 60,
        tls: bool | TLSConfig = False,
        user_agent: str = ...,
        num_pools: int | None = None,
        credstore_env: Mapping[Incomplete, Incomplete] | None = None,
        use_ssh_client: bool = False,
        max_pool_size: int = 10,
    ) -> None: ...
    @classmethod
    def from_env(
        cls,
        *,
        version: str | None = None,
        timeout: int = 60,
        max_pool_size: int = 10,
        environment: _Environ | None = None,
        use_ssh_client: bool = False,
        use_context: bool = True,
    ) -> DockerClient:
        """
        Return a client configured from environment variables.

        The environment variables used are the same as those used by the
        Docker command-line client. They are:

        .. envvar:: DOCKER_HOST

            The URL to the Docker host.

        .. envvar:: DOCKER_TLS_VERIFY

            Verify the host against a CA certificate.

        .. envvar:: DOCKER_CERT_PATH

            A path to a directory containing TLS certificates to use when
            connecting to the Docker host.

        Args:
            version (str): The version of the API to use. Set to ``auto`` to
                automatically detect the server's version. Default: ``auto``
            timeout (int): Default timeout for API calls, in seconds.
            max_pool_size (int): The maximum number of connections
                to save in the pool.
            environment (dict): The environment to read environment variables
                from. Default: the value of ``os.environ``
            credstore_env (dict): Override environment variables when calling
                the credential store process.
            use_ssh_client (bool): If set to `True`, an ssh connection is
                made via shelling out to the ssh client. Ensure the ssh
                client is installed and configured on the host.
            use_context (bool): If ``True`` (the default), fall back to the
                current Docker CLI context (``~/.docker/config.json`` /
                ``DOCKER_CONTEXT``) when ``DOCKER_HOST`` is not set. This
                allows the client to talk to Docker Desktop out of the box.

        Example:

            >>> import docker
            >>> client = docker.from_env()

        .. _`SSL version`:
            https://docs.python.org/3.5/library/ssl.html#ssl.PROTOCOL_TLSv1
        """
        ...
    @classmethod
    def from_context(
        cls,
        name=None,
        *,
        version: str | None = None,
        timeout: int = 60,
        max_pool_size: int = 10,
        use_ssh_client: bool = False,
        base_url: str | None = None,
        tls: bool | TLSConfig = False,
        user_agent: str = ...,
        num_pools: int | None = None,
        credstore_env: Mapping[Incomplete, Incomplete] | None = None,
    ):
        """
        Return a client configured from a Docker CLI context.

        With no ``name``, resolves the current context the same way the
        Docker CLI does: ``DOCKER_CONTEXT`` env var, then the
        ``currentContext`` field in ``~/.docker/config.json``, falling back
        to the built-in ``default`` context. On a machine with Docker
        Desktop installed this typically resolves to ``desktop-linux``.

        Args:
            name (str): Name of the context to load. ``None`` (the default)
                means "use the current context".
            version (str): The version of the API to use. Set to ``auto`` to
                automatically detect the server's version.
            timeout (int): Default timeout for API calls, in seconds.
            max_pool_size (int): The maximum number of connections to save in
                the pool.
            use_ssh_client (bool): If ``True``, shell out to the ssh client
                for ssh:// contexts.

        Example:

            >>> import docker
            >>> client = docker.DockerClient.from_context()
            >>> # or, pick a specific context:
            >>> client = docker.DockerClient.from_context('desktop-linux')
        """
        ...
    @property
    def configs(self) -> ConfigCollection:
        """
        An object for managing configs on the server. See the
        :doc:`configs documentation <configs>` for full details.
        """
        ...
    @property
    def containers(self) -> ContainerCollection:
        """
        An object for managing containers on the server. See the
        :doc:`containers documentation <containers>` for full details.
        """
        ...
    @property
    def images(self) -> ImageCollection:
        """
        An object for managing images on the server. See the
        :doc:`images documentation <images>` for full details.
        """
        ...
    @property
    def networks(self) -> NetworkCollection:
        """
        An object for managing networks on the server. See the
        :doc:`networks documentation <networks>` for full details.
        """
        ...
    @property
    def nodes(self) -> NodeCollection:
        """
        An object for managing nodes on the server. See the
        :doc:`nodes documentation <nodes>` for full details.
        """
        ...
    @property
    def plugins(self) -> PluginCollection:
        """
        An object for managing plugins on the server. See the
        :doc:`plugins documentation <plugins>` for full details.
        """
        ...
    @property
    def secrets(self) -> SecretCollection:
        """
        An object for managing secrets on the server. See the
        :doc:`secrets documentation <secrets>` for full details.
        """
        ...
    @property
    def services(self) -> ServiceCollection:
        """
        An object for managing services on the server. See the
        :doc:`services documentation <services>` for full details.
        """
        ...
    @property
    def swarm(self) -> Swarm:
        """
        An object for managing a swarm on the server. See the
        :doc:`swarm documentation <swarm>` for full details.
        """
        ...
    @property
    def volumes(self) -> VolumeCollection:
        """
        An object for managing volumes on the server. See the
        :doc:`volumes documentation <volumes>` for full details.
        """
        ...

    # Please keep in sync with docker.api.daemon.DaemonApiMixin.events
    @overload
    def events(
        self,
        since: datetime | int | None = None,
        until: datetime | int | None = None,
        filters: dict[str, Any] | None = None,
        decode: Literal[False] | None = None,
    ) -> CancellableStream[str]: ...
    @overload
    def events(
        self,
        since: datetime | int | None = None,
        until: datetime | int | None = None,
        filters: dict[str, Any] | None = None,
        decode: Literal[True] = ...,
    ) -> CancellableStream[dict[str, Any]]: ...

    def df(self) -> dict[str, Any]: ...
    # Please keep in sync with docker.api.daemon.DaemonApiMixin.info
    def info(self) -> dict[str, Any]: ...
    # Please keep in sync with docker.api.daemon.DaemonApiMixin.login
    def login(
        self,
        username: str,
        password: str | None = None,
        email: str | None = None,
        registry: str | None = None,
        reauth: bool = False,
        dockercfg_path: str | None = None,
    ) -> dict[str, Any]: ...
    # Please keep in sync with docker.api.daemon.DaemonApiMixin.ping
    def ping(self) -> bool: ...
    # Please keep in sync with docker.api.daemon.DaemonApiMixin.version
    def version(self, api_version: bool = True) -> dict[str, Any]: ...
    def close(self) -> None: ...
    def __getattr__(self, name: str) -> NoReturn: ...

from_env = DockerClient.from_env
from_context = DockerClient.from_context

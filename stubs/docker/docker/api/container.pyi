import datetime
from _typeshed import Incomplete
from collections.abc import Iterable, Mapping
from typing import Any, Literal, TypeAlias, TypedDict, overload, type_check_only
from typing_extensions import NotRequired

from docker._types import ContainerWeightDevice, WaitContainerResponse
from docker.types.containers import DeviceRequest, LogConfig, Ulimit
from docker.types.daemon import CancellableStream
from docker.types.healthcheck import Healthcheck
from docker.types.services import Mount

from ..types import ContainerConfig, EndpointConfig, HostConfig, NetworkingConfig

@type_check_only
class _RestartPolicy(TypedDict):
    MaximumRetryCount: NotRequired[int]
    Name: NotRequired[Literal["always", "on-failure"]]

@type_check_only
class _HasId(TypedDict):
    Id: str

@type_check_only
class _HasID(TypedDict):
    ID: str

@type_check_only
class _TopResult(TypedDict):
    Titles: list[str]
    Processes: list[list[str]]

_Container: TypeAlias = _HasId | _HasID | str

class ContainerApiMixin:
    @overload
    def attach(
        self,
        container: _Container,
        stdout: bool = True,
        stderr: bool = True,
        stream: Literal[False] = False,
        logs: bool = False,
        demux: Literal[False] = False,
    ) -> bytes:
        """
        Attach to a container.

        The ``.logs()`` function is a wrapper around this method, which you can
        use instead if you want to fetch/stream container output without first
        retrieving the entire backlog.

        Args:
            container (str): The container to attach to.
            stdout (bool): Include stdout.
            stderr (bool): Include stderr.
            stream (bool): Return container output progressively as an iterator
                of strings, rather than a single string.
            logs (bool): Include the container's previous output.
            demux (bool): Keep stdout and stderr separate.

        Returns:
            By default, the container's output as a single string (two if
            ``demux=True``: one for stdout and one for stderr).

            If ``stream=True``, an iterator of output strings. If
            ``demux=True``, two iterators are returned: one for stdout and one
            for stderr.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    @overload
    def attach(
        self,
        container: _Container,
        stdout: bool = True,
        stderr: bool = True,
        stream: Literal[False] = False,
        logs: bool = False,
        *,
        demux: Literal[True],
    ) -> tuple[bytes | None, bytes | None]:
        """
        Attach to a container.

        The ``.logs()`` function is a wrapper around this method, which you can
        use instead if you want to fetch/stream container output without first
        retrieving the entire backlog.

        Args:
            container (str): The container to attach to.
            stdout (bool): Include stdout.
            stderr (bool): Include stderr.
            stream (bool): Return container output progressively as an iterator
                of strings, rather than a single string.
            logs (bool): Include the container's previous output.
            demux (bool): Keep stdout and stderr separate.

        Returns:
            By default, the container's output as a single string (two if
            ``demux=True``: one for stdout and one for stderr).

            If ``stream=True``, an iterator of output strings. If
            ``demux=True``, two iterators are returned: one for stdout and one
            for stderr.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    @overload
    def attach(
        self,
        container: _Container,
        stdout: bool = True,
        stderr: bool = True,
        *,
        stream: Literal[True],
        logs: bool = False,
        demux: Literal[False] = False,
    ) -> CancellableStream[bytes]:
        """
        Attach to a container.

        The ``.logs()`` function is a wrapper around this method, which you can
        use instead if you want to fetch/stream container output without first
        retrieving the entire backlog.

        Args:
            container (str): The container to attach to.
            stdout (bool): Include stdout.
            stderr (bool): Include stderr.
            stream (bool): Return container output progressively as an iterator
                of strings, rather than a single string.
            logs (bool): Include the container's previous output.
            demux (bool): Keep stdout and stderr separate.

        Returns:
            By default, the container's output as a single string (two if
            ``demux=True``: one for stdout and one for stderr).

            If ``stream=True``, an iterator of output strings. If
            ``demux=True``, two iterators are returned: one for stdout and one
            for stderr.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    @overload
    def attach(
        self,
        container: _Container,
        stdout: bool = True,
        stderr: bool = True,
        *,
        stream: Literal[True],
        logs: bool = False,
        demux: Literal[True],
    ) -> CancellableStream[tuple[bytes | None, bytes | None]]:
        """
        Attach to a container.

        The ``.logs()`` function is a wrapper around this method, which you can
        use instead if you want to fetch/stream container output without first
        retrieving the entire backlog.

        Args:
            container (str): The container to attach to.
            stdout (bool): Include stdout.
            stderr (bool): Include stderr.
            stream (bool): Return container output progressively as an iterator
                of strings, rather than a single string.
            logs (bool): Include the container's previous output.
            demux (bool): Keep stdout and stderr separate.

        Returns:
            By default, the container's output as a single string (two if
            ``demux=True``: one for stdout and one for stderr).

            If ``stream=True``, an iterator of output strings. If
            ``demux=True``, two iterators are returned: one for stdout and one
            for stderr.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...

    def attach_socket(self, container: _Container, params=None, ws: bool = False):
        """
        Like ``attach``, but returns the underlying socket-like object for the
        HTTP request.

        Args:
            container (str): The container to attach to.
            params (dict): Dictionary of request parameters (e.g. ``stdout``,
                ``stderr``, ``stream``).
                For ``detachKeys``, ~/.docker/config.json is used by default.
            ws (bool): Use websockets instead of raw HTTP.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def commit(
        self,
        container: _Container,
        repository: str | None = None,
        tag: str | None = None,
        message=None,
        author=None,
        pause: bool = True,
        changes=None,
        conf=None,
    ):
        """
        Commit a container to an image. Similar to the ``docker commit``
        command.

        Args:
            container (str): The image hash of the container
            repository (str): The repository to push the image to
            tag (str): The tag to push
            message (str): A commit message
            author (str): The name of the author
            pause (bool): Whether to pause the container before committing
            changes (str): Dockerfile instructions to apply while committing
            conf (dict): The configuration for the container. See the
                `Engine API documentation
                <https://docs.docker.com/reference/api/docker_remote_api/>`_
                for full details.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def containers(
        self,
        quiet: bool = False,
        all: bool = False,
        trunc: bool = False,
        latest: bool = False,
        since: str | None = None,
        before: str | None = None,
        limit: int = -1,
        size: bool = False,
        filters=None,
    ):
        """
        List containers. Similar to the ``docker ps`` command.

        Args:
            quiet (bool): Only display numeric Ids
            all (bool): Show all containers. Only running containers are shown
                by default
            trunc (bool): Truncate output
            latest (bool): Show only the latest created container, include
                non-running ones.
            since (str): Show only containers created since Id or Name, include
                non-running ones
            before (str): Show only container created before Id or Name,
                include non-running ones
            limit (int): Show `limit` last created containers, include
                non-running ones
            size (bool): Display sizes
            filters (dict): Filters to be processed on the image list.
                Available filters:

                - `exited` (int): Only containers with specified exit code
                - `status` (str): One of ``restarting``, ``running``,
                    ``paused``, ``exited``
                - `label` (str|list): format either ``"key"``, ``"key=value"``
                    or a list of such.
                - `id` (str): The id of the container.
                - `name` (str): The name of the container.
                - `ancestor` (str): Filter by container ancestor. Format of
                    ``<image-name>[:tag]``, ``<image-id>``, or
                    ``<image@digest>``.
                - `before` (str): Only containers created before a particular
                    container. Give the container name or id.
                - `since` (str): Only containers created after a particular
                    container. Give container name or id.

                A comprehensive list can be found in the documentation for
                `docker ps
                <https://docs.docker.com/engine/reference/commandline/ps>`_.

        Returns:
            A list of dicts, one per container

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def create_container(
        self,
        image,
        command: str | list[str] | None = None,
        hostname: str | None = None,
        user: str | int | None = None,
        detach: bool = False,
        stdin_open: bool = False,
        tty: bool = False,
        # list is invariant, enumerating all possible union combination would be too complex for:
        # list[str | int | tuple[int | str, str] | tuple[int | str, ...]]
        ports: dict[str, dict[Incomplete, Incomplete]] | list[Any] | None = None,
        environment: dict[str, str] | list[str] | None = None,
        volumes: str | list[str] | None = None,
        network_disabled: bool = False,
        name: str | None = None,
        entrypoint: str | list[str] | None = None,
        working_dir: str | None = None,
        domainname: str | None = None,
        host_config=None,
        mac_address: str | None = None,
        labels: dict[str, str] | list[str] | None = None,
        stop_signal: str | None = None,
        networking_config=None,
        healthcheck=None,
        stop_timeout: int | None = None,
        runtime: str | None = None,
        use_config_proxy: bool = True,
        platform: str | None = None,
    ): ...
    # Please keep in sync with docker.types.ContainerConfig
    def create_container_config(
        self,
        image: str,
        command: str | list[str],
        hostname: str | None = None,
        user: str | int | None = None,
        detach: bool = False,
        stdin_open: bool = False,
        tty: bool = False,
        # list is invariant, enumerating all possible union combination would be too complex for:
        # list[str | int | tuple[int | str, str] | tuple[int | str, ...]]
        ports: dict[str, dict[str, str]] | list[Any] | None = None,
        environment: dict[str, str] | list[str] | None = None,
        volumes: str | list[str] | None = None,
        network_disabled: bool = False,
        entrypoint: str | list[str] | None = None,
        working_dir: str | None = None,
        domainname: str | None = None,
        host_config: HostConfig | None = None,
        mac_address: str | None = None,
        labels: dict[str, str] | list[str] | None = None,
        stop_signal: str | None = None,
        networking_config: NetworkingConfig | None = None,
        healthcheck: Healthcheck | None = None,
        stop_timeout: int | None = None,
        runtime: str | None = None,
    ) -> ContainerConfig: ...
    def create_container_from_config(self, config, name=None, platform=None): ...
    # Please keep in sync with docker.types.HostConfig
    def create_host_config(
        self,
        binds: dict[str, Mapping[str, str]] | list[str] | None = None,
        port_bindings: Mapping[int | str, Any] | None = None,  # Any: int, str, tuple, dict, or list
        lxc_conf: dict[str, str] | list[dict[str, str]] | None = None,
        publish_all_ports: bool = False,
        links: dict[str, str] | dict[str, None] | dict[str, str | None] | Iterable[tuple[str, str | None]] | None = None,
        privileged: bool = False,
        dns: list[str] | None = None,
        dns_search: list[str] | None = None,
        volumes_from: list[str] | None = None,
        network_mode: str | None = None,
        restart_policy: Mapping[str, str | int] | None = None,
        cap_add: list[str] | None = None,
        cap_drop: list[str] | None = None,
        devices: list[str] | None = None,
        extra_hosts: dict[str, str] | list[str] | None = None,
        read_only: bool | None = None,
        pid_mode: str | None = None,
        ipc_mode: str | None = None,
        security_opt: list[str] | None = None,
        ulimits: list[Ulimit] | None = None,
        log_config: LogConfig | None = None,
        mem_limit: str | int | None = None,
        memswap_limit: str | int | None = None,
        mem_reservation: str | int | None = None,
        kernel_memory: str | int | None = None,
        mem_swappiness: int | None = None,
        cgroup_parent: str | None = None,
        group_add: Iterable[str | int] | None = None,
        cpu_quota: int | None = None,
        cpu_period: int | None = None,
        blkio_weight: int | None = None,
        blkio_weight_device: list[ContainerWeightDevice] | None = None,
        device_read_bps: list[Mapping[str, str | int]] | None = None,
        device_write_bps: list[Mapping[str, str | int]] | None = None,
        device_read_iops: list[Mapping[str, str | int]] | None = None,
        device_write_iops: list[Mapping[str, str | int]] | None = None,
        oom_kill_disable: bool = False,
        shm_size: str | int | None = None,
        sysctls: dict[str, str] | None = None,
        tmpfs: dict[str, str] | None = None,
        oom_score_adj: int | None = None,
        dns_opt: list[str] | None = None,
        cpu_shares: int | None = None,
        cpuset_cpus: str | None = None,
        userns_mode: str | None = None,
        uts_mode: str | None = None,
        pids_limit: int | None = None,
        isolation: str | None = None,
        auto_remove: bool = False,
        storage_opt: dict[str, str] | None = None,
        init: bool | None = None,
        init_path: str | None = None,
        volume_driver: str | None = None,
        cpu_count: int | None = None,
        cpu_percent: int | None = None,
        nano_cpus: int | None = None,
        cpuset_mems: str | None = None,
        runtime: str | None = None,
        mounts: list[Mount] | None = None,
        cpu_rt_period: int | None = None,
        cpu_rt_runtime: int | None = None,
        device_cgroup_rules: list[str] | None = None,
        device_requests: list[DeviceRequest] | None = None,
        cgroupns: Literal["private", "host"] | None = None,
    ) -> HostConfig: ...
    # Please keep in sync with docker.types.NetworkingConfig
    def create_networking_config(self, endpoints_config: EndpointConfig | None = None) -> NetworkingConfig: ...
    # Please keep in sync with docker.types.EndpointConfig
    def create_endpoint_config(
        self,
        aliases: list[str] | None = None,
        links: dict[str, str] | dict[str, None] | dict[str, str | None] | Iterable[tuple[str, str | None]] | None = None,
        ipv4_address: str | None = None,
        ipv6_address: str | None = None,
        link_local_ips: list[str] | None = None,
        driver_opt: dict[str, str] | None = None,
        mac_address: str | None = None,
    ) -> EndpointConfig: ...
    def diff(self, container: _Container) -> list[dict[Incomplete, Incomplete]]: ...
    def export(self, container: _Container, chunk_size: int | None = 2097152): ...
    def get_archive(
        self, container: _Container, path, chunk_size: int | None = 2097152, encode_stream: bool = False
    ) -> tuple[Incomplete, Incomplete]:
        """
        Retrieve a file or folder from a container in the form of a tar
        archive.

        Args:
            container (str): The container where the file is located
            path (str): Path to the file or folder to retrieve
            chunk_size (int): The number of bytes returned by each iteration
                of the generator. If ``None``, data will be streamed as it is
                received. Default: 2 MB
            encode_stream (bool): Determines if data should be encoded
                (gzip-compressed) during transmission. Default: False

        Returns:
            (tuple): First element is a raw tar data stream. Second element is
            a dict containing ``stat`` information on the specified ``path``.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.

        Example:

            >>> c = docker.APIClient()
            >>> f = open('./sh_bin.tar', 'wb')
            >>> bits, stat = c.api.get_archive(container, '/bin/sh')
            >>> print(stat)
            {'name': 'sh', 'size': 1075464, 'mode': 493,
             'mtime': '2018-10-01T15:37:48-07:00', 'linkTarget': ''}
            >>> for chunk in bits:
            ...    f.write(chunk)
            >>> f.close()
        """
        ...
    def inspect_container(self, container: _Container):
        """
        Identical to the `docker inspect` command, but only for containers.

        Args:
            container (str): The container to inspect

        Returns:
            (dict): Similar to the output of `docker inspect`, but as a
            single dict

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def kill(self, container: _Container, signal: str | int | None = None) -> None:
        """
        Kill a container or send a signal to a container.

        Args:
            container (str): The container to kill
            signal (str or int): The signal to send. Defaults to ``SIGKILL``

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...

    @overload
    def logs(
        self,
        container: _Container,
        stdout: bool = True,
        stderr: bool = True,
        *,
        stream: Literal[True],
        timestamps: bool = False,
        tail: Literal["all"] | int = "all",
        since: datetime.datetime | float | None = None,
        follow: bool | None = None,
        until: datetime.datetime | float | None = None,
    ) -> CancellableStream[bytes]:
        """
        Get logs from a container. Similar to the ``docker logs`` command.

        The ``stream`` parameter makes the ``logs`` function return a blocking
        generator you can iterate over to retrieve log output as it happens.

        Args:
            container (str): The container to get logs from
            stdout (bool): Get ``STDOUT``. Default ``True``
            stderr (bool): Get ``STDERR``. Default ``True``
            stream (bool): Stream the response. Default ``False``
            timestamps (bool): Show timestamps. Default ``False``
            tail (str or int): Output specified number of lines at the end of
                logs. Either an integer of number of lines or the string
                ``all``. Default ``all``
            since (datetime, int, or float): Show logs since a given datetime,
                integer epoch (in seconds) or float (in fractional seconds)
            follow (bool): Follow log output. Default ``False``
            until (datetime, int, or float): Show logs that occurred before
                the given datetime, integer epoch (in seconds), or
                float (in fractional seconds)

        Returns:
            (generator of bytes or bytes)

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    @overload
    def logs(
        self,
        container: _Container,
        stdout: bool,
        stderr: bool,
        stream: Literal[True],
        timestamps: bool = False,
        tail: Literal["all"] | int = "all",
        since: datetime.datetime | float | None = None,
        follow: bool | None = None,
        until: datetime.datetime | float | None = None,
    ) -> CancellableStream[bytes]:
        """
        Get logs from a container. Similar to the ``docker logs`` command.

        The ``stream`` parameter makes the ``logs`` function return a blocking
        generator you can iterate over to retrieve log output as it happens.

        Args:
            container (str): The container to get logs from
            stdout (bool): Get ``STDOUT``. Default ``True``
            stderr (bool): Get ``STDERR``. Default ``True``
            stream (bool): Stream the response. Default ``False``
            timestamps (bool): Show timestamps. Default ``False``
            tail (str or int): Output specified number of lines at the end of
                logs. Either an integer of number of lines or the string
                ``all``. Default ``all``
            since (datetime, int, or float): Show logs since a given datetime,
                integer epoch (in seconds) or float (in fractional seconds)
            follow (bool): Follow log output. Default ``False``
            until (datetime, int, or float): Show logs that occurred before
                the given datetime, integer epoch (in seconds), or
                float (in fractional seconds)

        Returns:
            (generator of bytes or bytes)

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    @overload
    def logs(
        self,
        container: _Container,
        stdout: bool = True,
        stderr: bool = True,
        stream: Literal[False] = False,
        timestamps: bool = False,
        tail: Literal["all"] | int = "all",
        since: datetime.datetime | float | None = None,
        follow: bool | None = None,
        until: datetime.datetime | float | None = None,
    ) -> bytes:
        """
        Get logs from a container. Similar to the ``docker logs`` command.

        The ``stream`` parameter makes the ``logs`` function return a blocking
        generator you can iterate over to retrieve log output as it happens.

        Args:
            container (str): The container to get logs from
            stdout (bool): Get ``STDOUT``. Default ``True``
            stderr (bool): Get ``STDERR``. Default ``True``
            stream (bool): Stream the response. Default ``False``
            timestamps (bool): Show timestamps. Default ``False``
            tail (str or int): Output specified number of lines at the end of
                logs. Either an integer of number of lines or the string
                ``all``. Default ``all``
            since (datetime, int, or float): Show logs since a given datetime,
                integer epoch (in seconds) or float (in fractional seconds)
            follow (bool): Follow log output. Default ``False``
            until (datetime, int, or float): Show logs that occurred before
                the given datetime, integer epoch (in seconds), or
                float (in fractional seconds)

        Returns:
            (generator of bytes or bytes)

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...

    def pause(self, container: _Container) -> None:
        """
        Pauses all processes within a container.

        Args:
            container (str): The container to pause

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def port(self, container: _Container, private_port: int):
        """
        Lookup the public-facing port that is NAT-ed to ``private_port``.
        Identical to the ``docker port`` command.

        Args:
            container (str): The container to look up
            private_port (int): The private port to inspect

        Returns:
            (list of dict): The mapping for the host ports

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.

        Example:
            .. code-block:: bash

                $ docker run -d -p 80:80 ubuntu:14.04 /bin/sleep 30
                7174d6347063a83f412fad6124c99cffd25ffe1a0807eb4b7f9cec76ac8cb43b

            .. code-block:: python

                >>> client.api.port('7174d6347063', 80)
                [{'HostIp': '0.0.0.0', 'HostPort': '80'}]
        """
        ...
    def put_archive(self, container: _Container, path: str, data) -> bool:
        """
        Insert a file or folder in an existing container using a tar archive as
        source.

        Args:
            container (str): The container where the file(s) will be extracted
            path (str): Path inside the container where the file(s) will be
                extracted. Must exist.
            data (bytes or stream): tar data to be extracted

        Returns:
            (bool): True if the call succeeds.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def prune_containers(self, filters=None):
        """
        Delete stopped containers

        Args:
            filters (dict): Filters to process on the prune list.

        Returns:
            (dict): A dict containing a list of deleted container IDs and
                the amount of disk space reclaimed in bytes.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def remove_container(self, container: _Container, v: bool = False, link: bool = False, force: bool = False) -> None:
        """
        Remove a container. Similar to the ``docker rm`` command.

        Args:
            container (str): The container to remove
            v (bool): Remove the volumes associated with the container
            link (bool): Remove the specified link and not the underlying
                container
            force (bool): Force the removal of a running container (uses
                ``SIGKILL``)

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def rename(self, container: _Container, name: str) -> None:
        """
        Rename a container. Similar to the ``docker rename`` command.

        Args:
            container (str): ID of the container to rename
            name (str): New name for the container

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def resize(self, container: _Container, height: int, width: int) -> None:
        """
        Resize the tty session.

        Args:
            container (str or dict): The container to resize
            height (int): Height of tty session
            width (int): Width of tty session

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def restart(self, container: _Container, timeout: int = 10) -> None:
        """
        Restart a container. Similar to the ``docker restart`` command.

        Args:
            container (str or dict): The container to restart. If a dict, the
                ``Id`` key is used.
            timeout (int): Number of seconds to try to stop for before killing
                the container. Once killed it will then be restarted. Default
                is 10 seconds.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def start(self, container: _Container) -> None:
        """
        Start a container. Similar to the ``docker start`` command, but
        doesn't support attach options.

        **Deprecation warning:** Passing configuration options in ``start`` is
        no longer supported. Users are expected to provide host config options
        in the ``host_config`` parameter of
        :py:meth:`~ContainerApiMixin.create_container`.


        Args:
            container (str): The container to start

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
            :py:class:`docker.errors.DeprecatedMethod`
                If any argument besides ``container`` are provided.

        Example:

            >>> container = client.api.create_container(
            ...     image='busybox:latest',
            ...     command='/bin/sleep 30')
            >>> client.api.start(container=container.get('Id'))
        """
        ...
    def stats(self, container: _Container, decode: bool | None = None, stream: bool = True, one_shot: bool | None = None):
        """
        Stream statistics for a specific container. Similar to the
        ``docker stats`` command.

        Args:
            container (str): The container to stream statistics from
            decode (bool): If set to true, stream will be decoded into dicts
                on the fly. Only applicable if ``stream`` is True.
                False by default.
            stream (bool): If set to false, only the current stats will be
                returned instead of a stream. True by default.
            one_shot (bool): If set to true, Only get a single stat instead of
                waiting for 2 cycles. Must be used with stream=false. False by
                default.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def stop(self, container: _Container, timeout: int | None = None) -> None:
        """
        Stops a container. Similar to the ``docker stop`` command.

        Args:
            container (str): The container to stop
            timeout (int): Timeout in seconds to wait for the container to
                stop before sending a ``SIGKILL``. If None, then the
                StopTimeout value of the container will be used.
                Default: None

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def top(self, container: _Container, ps_args: str | None = None) -> _TopResult:
        """
        Display the running processes of a container.

        Args:
            container (str): The container to inspect
            ps_args (str): An optional arguments passed to ps (e.g. ``aux``)

        Returns:
            (str): The output of the top

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def unpause(self, container: _Container) -> None:
        """
        Unpause all processes within a container.

        Args:
            container (str): The container to unpause
        """
        ...
    def update_container(
        self,
        container: _Container,
        blkio_weight: int | None = None,
        cpu_period: int | None = None,
        cpu_quota: int | None = None,
        cpu_shares: int | None = None,
        cpuset_cpus: str | None = None,
        cpuset_mems: str | None = None,
        mem_limit: float | str | None = None,
        mem_reservation: float | str | None = None,
        memswap_limit: int | str | None = None,
        kernel_memory: int | str | None = None,
        restart_policy: _RestartPolicy | None = None,
    ): ...
    def wait(
        self,
        container: _Container,
        timeout: int | None = None,
        condition: Literal["not-running", "next-exit", "removed"] | None = None,
    ) -> WaitContainerResponse:
        """
        Block until a container stops, then return its exit code. Similar to
        the ``docker wait`` command.

        Args:
            container (str or dict): The container to wait on. If a dict, the
                ``Id`` key is used.
            timeout (int): Request timeout
            condition (str): Wait until a container state reaches the given
                condition, either ``not-running`` (default), ``next-exit``,
                or ``removed``

        Returns:
            (dict): The API's response as a Python dictionary, including
                the container's exit code under the ``StatusCode`` attribute.

        Raises:
            :py:class:`requests.exceptions.ReadTimeout`
                If the timeout is exceeded.
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...

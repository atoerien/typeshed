from .resource import Collection, Model

class Service(Model):
    """A service."""
    id_attribute: str
    @property
    def name(self):
        """The service's name."""
        ...
    @property
    def version(self):
        """
        The version number of the service. If this is not the same as the
        server, the :py:meth:`update` function will not work and you will
        need to call :py:meth:`reload` before calling it again.
        """
        ...
    def remove(self):
        """
        Stop and remove the service.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def tasks(self, filters=None):
        """
        List the tasks in this service.

        Args:
            filters (dict): A map of filters to process on the tasks list.
                Valid filters: ``id``, ``name``, ``node``,
                ``label``, and ``desired-state``.

        Returns:
            :py:class:`list`: List of task dictionaries.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def update(self, **kwargs):
        """
        Update a service's configuration. Similar to the ``docker service
        update`` command.

        Takes the same parameters as :py:meth:`~ServiceCollection.create`.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def logs(self, **kwargs):
        """
        Get log stream for the service.
        Note: This method works only for services with the ``json-file``
        or ``journald`` logging drivers.

        Args:
            details (bool): Show extra details provided to logs.
                Default: ``False``
            follow (bool): Keep connection open to read logs as they are
                sent by the Engine. Default: ``False``
            stdout (bool): Return logs from ``stdout``. Default: ``False``
            stderr (bool): Return logs from ``stderr``. Default: ``False``
            since (int): UNIX timestamp for the logs staring point.
                Default: 0
            timestamps (bool): Add timestamps to every log line.
            tail (string or int): Number of log lines to be returned,
                counting from the current end of the logs. Specify an
                integer or ``'all'`` to output all log lines.
                Default: ``all``

        Returns:
            generator: Logs for the service.
        """
        ...
    def scale(self, replicas):
        """
        Scale service container.

        Args:
            replicas (int): The number of containers that should be running.

        Returns:
            bool: ``True`` if successful.
        """
        ...
    def force_update(self):
        """
        Force update the service even if no changes require it.

        Returns:
            bool: ``True`` if successful.
        """
        ...

class ServiceCollection(Collection[Service]):
    """Services on the Docker server."""
    model: type[Service]
    def create(self, image, command=None, **kwargs): ...  # type: ignore[override]
    def get(self, service_id, insert_defaults=None): ...
    def list(self, **kwargs): ...

CONTAINER_SPEC_KWARGS: list[str]
TASK_TEMPLATE_KWARGS: list[str]
CREATE_SERVICE_KWARGS: list[str]
PLACEMENT_KWARGS: list[str]

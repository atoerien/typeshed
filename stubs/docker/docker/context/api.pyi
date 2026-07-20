from _typeshed import Incomplete
from collections.abc import Mapping, Sequence

from docker.context.context import Context
from docker.tls import TLSConfig

class ContextAPI:
    """
    Context API.
    Contains methods for context management:
    create, list, remove, get, inspect.
    """
    DEFAULT_CONTEXT: Context
    @classmethod
    def create_context(
        cls,
        name: str,
        orchestrator: str | None = None,
        host: str | None = None,
        tls_cfg: TLSConfig | None = None,
        default_namespace: str | None = None,
        skip_tls_verify: bool = False,
    ) -> Context:
        """
        Creates a new context.
        Returns:
            (Context): a Context object.
        Raises:
            :py:class:`docker.errors.MissingContextParameter`
                If a context name is not provided.
            :py:class:`docker.errors.ContextAlreadyExists`
                If a context with the name already exists.
            :py:class:`docker.errors.ContextException`
                If name is default.

        Example:

        >>> from docker.context import ContextAPI
        >>> ctx = ContextAPI.create_context(name='test')
        >>> print(ctx.Metadata)
        {
            "Name": "test",
            "Metadata": {},
            "Endpoints": {
                "docker": {
                    "Host": "unix:///var/run/docker.sock",
                    "SkipTLSVerify": false
                }
            }
        }
        """
        ...
    @classmethod
    def get_context(cls, name: str | None = None) -> Context:
        """
        Retrieves a context object.
        Args:
            name (str): The name of the context

        Example:

        >>> from docker.context import ContextAPI
        >>> ctx = ContextAPI.get_context(name='test')
        >>> print(ctx.Metadata)
        {
            "Name": "test",
            "Metadata": {},
            "Endpoints": {
                "docker": {
                "Host": "unix:///var/run/docker.sock",
                "SkipTLSVerify": false
                }
            }
        }
        """
        ...
    @classmethod
    def contexts(cls) -> Sequence[Context]:
        """
        Context list.
        Returns:
            (Context): List of context objects.
        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    @classmethod
    def get_current_context(cls) -> Context:
        """
        Get current context.
        Returns:
            (Context): current context object.
        """
        ...
    @classmethod
    def kwargs_from_context(
        cls, name: str | None = None, environment: Mapping[str, str | None] | None = None
    ) -> dict[str, Incomplete]:
        """
        Build ``base_url`` / ``tls`` kwargs from a Docker CLI context.

        Mirrors the Docker CLI: if ``name`` is not given, honours the
        ``DOCKER_CONTEXT`` env var, then the ``currentContext`` field in
        ``~/.docker/config.json``, defaulting to the built-in ``default``
        context (local socket / named pipe). On a host with Docker Desktop
        this resolves to the ``desktop-linux`` (or equivalent) context, so
        client construction targets Docker Desktop out of the box.
        """
        ...
    @classmethod
    def set_current_context(cls, name: str = "default") -> None: ...
    @classmethod
    def remove_context(cls, name: str) -> None:
        """
        Remove a context. Similar to the ``docker context rm`` command.

        Args:
            name (str): The name of the context

        Raises:
            :py:class:`docker.errors.MissingContextParameter`
                If a context name is not provided.
            :py:class:`docker.errors.ContextNotFound`
                If a context with the name does not exist.
            :py:class:`docker.errors.ContextException`
                If name is default.

        Example:

        >>> from docker.context import ContextAPI
        >>> ContextAPI.remove_context(name='test')
        >>>
        """
        ...
    @classmethod
    def inspect_context(cls, name: str = "default") -> Context:
        """
        Remove a context. Similar to the ``docker context inspect`` command.

        Args:
            name (str): The name of the context

        Raises:
            :py:class:`docker.errors.MissingContextParameter`
                If a context name is not provided.
            :py:class:`docker.errors.ContextNotFound`
                If a context with the name does not exist.

        Example:

        >>> from docker.context import ContextAPI
        >>> ContextAPI.remove_context(name='test')
        >>>
        """
        ...

from collections.abc import Generator
from typing import Any
from typing_extensions import override

from .resource import Collection, Model

class Plugin(Model):
    """A plugin on the server."""
    @property
    def name(self) -> str | None:
        """The plugin's name."""
        ...
    @property
    def enabled(self) -> bool | None:
        """Whether the plugin is enabled."""
        ...
    @property
    def settings(self) -> dict[str, Any] | None: ...
    def configure(self, options: dict[str, Any]) -> None: ...
    def disable(self, force: bool = False) -> None: ...
    def enable(self, timeout: int = 0) -> None: ...
    def push(self) -> Generator[dict[str, Any]]: ...
    def remove(self, force: bool = False) -> bool: ...
    def upgrade(self, remote: str | None = None) -> Generator[dict[str, Any]]: ...

class PluginCollection(Collection[Plugin]):
    model: type[Plugin]
    @override
    def create(self, name, plugin_data_dir, gzip: bool = False): ...  # type: ignore[override]
    @override
    def get(self, name):
        """
        Gets a plugin.

        Args:
            name (str): The name of the plugin.

        Returns:
            (:py:class:`Plugin`): The plugin.

        Raises:
            :py:class:`docker.errors.NotFound` If the plugin does not
            exist.
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def install(self, remote_name, local_name=None):
        """
        Pull and install a plugin.

        Args:
            remote_name (string): Remote reference for the plugin to
                install. The ``:latest`` tag is optional, and is the
                default if omitted.
            local_name (string): Local name for the pulled plugin.
                The ``:latest`` tag is optional, and is the default if
                omitted. Optional.

        Returns:
            (:py:class:`Plugin`): The installed plugin
        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    @override
    def list(self):
        """
        List plugins installed on the server.

        Returns:
            (list of :py:class:`Plugin`): The plugins.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...

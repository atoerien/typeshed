from builtins import list as _list
from collections.abc import Generator
from typing import Any

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
    def settings(self) -> dict[str, Any] | None:
        """A dictionary representing the plugin's configuration."""
        ...
    def configure(self, options: dict[str, Any]) -> None:
        """
        Update the plugin's settings.

        Args:
            options (dict): A key-value mapping of options.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def disable(self, force: bool = False) -> None:
        """
        Disable the plugin.

        Args:
            force (bool): Force disable. Default: False

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def enable(self, timeout: int = 0) -> None:
        """
        Enable the plugin.

        Args:
            timeout (int): Timeout in seconds. Default: 0

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def push(self) -> Generator[dict[str, Any]]:
        """
        Push the plugin to a remote registry.

        Returns:
            A dict iterator streaming the status of the upload.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def remove(self, force: bool = False) -> bool:
        """
        Remove the plugin from the server.

        Args:
            force (bool): Remove even if the plugin is enabled.
                Default: False

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def upgrade(self, remote: str | None = None) -> Generator[dict[str, Any]]:
        """
        Upgrade the plugin.

        Args:
            remote (string): Remote reference to upgrade to. The
                ``:latest`` tag is optional and is the default if omitted.
                Default: this plugin's name.

        Returns:
            A generator streaming the decoded API logs
        """
        ...

class PluginCollection(Collection[Plugin]):
    model: type[Plugin]
    def create(self, name, plugin_data_dir, gzip: bool = False): ...  # type: ignore[override]
    def get(self, name): ...
    def install(self, remote_name, local_name=None): ...
    def list(self) -> _list[Plugin]: ...

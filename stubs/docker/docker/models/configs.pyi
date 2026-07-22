from _typeshed import Incomplete
from builtins import list as _list

from .resource import Collection, Model

class Config(Model):
    """A config."""
    id_attribute: str
    @property
    def name(self) -> str: ...
    def remove(self) -> bool:
        """
        Remove this config.

        Raises:
            :py:class:`docker.errors.APIError`
                If config failed to remove.
        """
        ...

class ConfigCollection(Collection[Config]):
    """Configs on the Docker server."""
    model: type[Config]
    # Please keep in sync with docker.api.config.ConfigApiMixin.create_config
    def create(  # type: ignore[override]
        self,
        *,
        name: str,
        data: bytes,
        labels: dict[Incomplete, Incomplete] | None = None,
        templating: dict[Incomplete, Incomplete] | None = None,
    ) -> Config: ...
    def get(self, config_id: str) -> Config: ...
    # Please keep in sync with docker.api.config.ConfigApiMixin.configs
    def list(self, *, filters=None) -> _list[Config]: ...

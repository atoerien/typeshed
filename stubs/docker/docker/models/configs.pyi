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
    def create(self, **kwargs) -> Config: ...  # type: ignore[override]
    def get(self, config_id: str) -> Config: ...
    def list(self, **kwargs) -> list[Config]: ...

from _typeshed import Incomplete
from builtins import list as _list

from docker.types import DriverConfig

from .resource import Collection, Model

class Secret(Model):
    """A secret."""
    id_attribute: str
    @property
    def name(self) -> str: ...
    def remove(self) -> bool: ...

class SecretCollection(Collection[Secret]):
    """Secrets on the Docker server."""
    model: type[Secret]
    # Please keep in sync with docker.api.secret.SecretApiMixin.create_secret
    def create(  # type: ignore[override]
        self, *, name: str, data: bytes, labels: dict[str, Incomplete] | None = None, driver: DriverConfig | None = None
    ) -> Secret: ...
    def get(self, secret_id: str) -> Secret: ...
    # Please keep in sync with docker.api.secret.SecretApiMixin.secrets
    def list(self, *, filters: dict[str, Incomplete] | None = None) -> _list[Secret]:
        """
        List secrets. Similar to the ``docker secret ls`` command.

        Args:
            filters (dict): Server-side list filtering options.

        Returns:
            (list of :py:class:`Secret`): The secrets.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...

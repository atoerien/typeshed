from typing import Any

from .resource import Collection, Model

class Volume(Model):
    """A volume."""
    id_attribute: str
    @property
    def name(self) -> str:
        """The name of the volume."""
        ...
    def remove(self, force: bool = False) -> None:
        """
        Remove this volume.

        Args:
            force (bool): Force removal of volumes that were already removed
                out of band by the volume driver plugin.
        Raises:
            :py:class:`docker.errors.APIError`
                If volume failed to remove.
        """
        ...

class VolumeCollection(Collection[Volume]):
    """Volumes on the Docker server."""
    model: type[Volume]
    def create(self, name: str | None = None, **kwargs) -> Volume: ...  # type: ignore[override]
    def get(self, volume_id: str) -> Volume: ...
    def list(self, **kwargs) -> list[Volume]: ...
    def prune(self, filters: dict[str, Any] | None = None) -> dict[str, Any]: ...

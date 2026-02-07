from logging import Logger
from typing import ClassVar

log: Logger

class XRayConfig:
    name: ClassVar[str]
    def ready(self) -> None:
        """
        Configure global XRay recorder based on django settings
        under XRAY_RECORDER namespace.
        This method could be called twice during server startup
        because of base command and reload command.
        So this function must be idempotent
        """
        ...

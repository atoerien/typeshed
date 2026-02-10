from _typeshed import Incomplete
from typing import Final

DEFAULTS: dict[str, str | bool | tuple[Incomplete] | list[Incomplete] | None]
XRAY_NAMESPACE: Final = "XRAY_RECORDER"
SUPPORTED_ENV_VARS: tuple[str, ...]

class XRaySettings:
    """
    A object of Django settings to easily modify certain fields.
    The precedence for configurations at different places is as follows:
    environment variables > user settings in settings.py > default settings
    """
    defaults: dict[str, str | bool | tuple[Incomplete] | list[Incomplete] | None]
    def __init__(self, user_settings=None) -> None: ...
    @property
    def user_settings(self): ...
    def __getattr__(self, attr): ...

settings: XRaySettings

def reload_settings(*, settings: str | None = None, value=None) -> None:
    """Reload X-Ray user settings upon Django server hot restart"""
    ...

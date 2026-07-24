"""
GDAL and OGR driver and configuration management

The main thread always utilizes CPLSetConfigOption. Child threads
utilize CPLSetThreadLocalConfigOption instead. All threads use
CPLGetConfigOption and not CPLGetThreadLocalConfigOption, thus child
threads will inherit config options from the main thread unless the
option is set to a new value inside the thread.
"""

from contextlib import AbstractContextManager
from typing import Final

from rasterio._typing import _GDALOption as _GDALOption

ca_bundle: Final[str]
code_map: Final[dict[int, int]]
level_map: Final[dict[int, int]]

def gdal_version() -> str:
    """Return the version as a major.minor.patchlevel string."""
    ...
def get_gdal_config(key: str, normalize: bool = True) -> _GDALOption:
    """
    Get the value of a GDAL configuration option.  When requesting
    ``GDAL_CACHEMAX`` the value is returned unaltered.

    Parameters
    ----------
    key : str
        Name of config option.
    normalize : bool, optional
        Convert values of ``"ON"'`` and ``"OFF"`` to ``True`` and ``False``.
    """
    ...
def set_gdal_config(key: str, val: _GDALOption, normalize: bool = True) -> None:
    """
    Set a GDAL configuration option's value.

    Parameters
    ----------
    key : str
        Name of config option.
    normalize : bool, optional
        Convert ``True`` to `"ON"` and ``False`` to `"OFF"``.
    """
    ...
def del_gdal_config(key: str) -> None:
    """
    Delete a GDAL configuration option.

    Parameters
    ----------
    key : str
        Name of config option.
    """
    ...
def get_gdal_data() -> str | None:
    """
    Get the GDAL DATA path.

    Returns
    -------
    str
    """
    ...
def get_proj_data_search_paths() -> list[str]:
    """
    Get the PROJ DATA search paths.

    Returns
    -------
    List[str]
    """
    ...
def set_proj_data_search_path(path: str) -> None:
    """Set PROJ data search path."""
    ...
def driver_count() -> int:
    """Return the count of all drivers"""
    ...
def catch_errors() -> AbstractContextManager[None]:
    """Intercept GDAL errors"""
    ...

class ConfigEnv:
    """Configuration option management"""
    options: dict[str, _GDALOption]
    def __init__(self, **options: _GDALOption) -> None: ...
    def update_config_options(self, **kwargs: _GDALOption) -> None:
        """Update GDAL config options."""
        ...
    def clear_config_options(self) -> None:
        """Clear GDAL config options."""
        ...
    def get_config_options(self) -> dict[str, _GDALOption]: ...

class GDALEnv(ConfigEnv):
    """Configuration and driver management"""
    def __init__(self, **options: _GDALOption) -> None: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...

class GDALDataFinder:
    """
    Finds GDAL data files

    Note: this is not part of the public API in 1.0.x.
    """
    def find_file(self, basename: str) -> str | None:
        """
        Returns path of a GDAL data file or None

        Parameters
        ----------
        basename : str
            Basename of a data file such as "gdalvrt.xsd"

        Returns
        -------
        str (on success) or None (on failure)
        """
        ...
    def search(self, prefix: str | None = None) -> str | None:
        """
        Returns GDAL data directory

        Note well that os.environ is not consulted.

        Returns
        -------
        str or None
        """
        ...
    def search_wheel(self, prefix: str | None = None) -> str | None:
        """Check wheel location"""
        ...
    def search_prefix(self, prefix: str) -> str | None:
        """Check sys.prefix location"""
        ...
    def search_debian(self, prefix: str) -> str | None:
        """Check Debian locations"""
        ...

class PROJDataFinder:
    """
    Finds PROJ data files

    Note: this is not part of the public API in 1.0.x.
    """
    def has_data(self) -> bool:
        """
        Returns True if PROJ's data files can be found

        Returns
        -------
        bool
        """
        ...
    def search(self, prefix: str | None = None) -> str | None:
        """
        Returns PROJ data directory

        Note well that os.environ is not consulted.

        Returns
        -------
        str or None
        """
        ...
    def search_wheel(self, prefix: str | None = None) -> str | None:
        """Check wheel location"""
        ...
    def search_prefix(self, prefix: str) -> str | None:
        """Check sys.prefix location"""
        ...

"""Methods accessing GDAL and its libraries version information."""

def gdal_version() -> str:
    """Return the version as a major.minor.patchlevel string."""
    ...
def get_gdal_version_info(key: str) -> str:
    """
    See: :c:func:`GDALVersionInfo`

    Available keys:

        - VERSION_NUM: Returns GDAL_VERSION_NUM formatted as a string.
        - RELEASE_DATE: Returns GDAL_RELEASE_DATE formatted as a string.
          i.e. “20020416”.
        - RELEASE_NAME: Returns the GDAL_RELEASE_NAME. ie. “1.1.7”
        - --version: Returns one line version message suitable for use
          in response to version requests. i.e. “GDAL 1.1.7, released 2002/04/16”
        - LICENSE: Returns the content of the LICENSE.TXT file
          from the GDAL_DATA directory.
        - BUILD_INFO: List of NAME=VALUE pairs separated by newlines with
          information on build time options.

    Parameters
    ----------
    key: str
        The type of version info.

    Returns
    -------
    Optional[str]:
        The version information if available.
    """
    ...
def check_gdal_version(major: int, minor: int) -> bool:
    """Return True if the major and minor versions match."""
    ...
def get_geos_version() -> tuple[int, int, int]:
    """
    Get GEOS Version

    Returns
    -------
    major: int
    minor: int
    patch: int
    """
    ...
def get_proj_version() -> tuple[int, int, int]:
    """
    Get PROJ Version

    Returns
    -------
    major: int
    minor: int
    patch: int
    """
    ...

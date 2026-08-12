"""Platform identification used to select and configure compilers."""

def get_host_platform() -> str:
    """A string identifying the platform the build is running on."""
    ...
def get_platform() -> str:
    """
    The platform being built for.

    Matches :func:`get_host_platform` except on Windows, where the MSVC
    target architecture (``VSCMD_ARG_TGT_ARCH``) takes precedence to support
    cross-compilation.
    """
    ...
def is_mingw() -> bool:
    """
    Whether the current platform is mingw.

    Python compiled with Mingw-w64 has ``sys.platform == 'win32'`` and
    ``get_platform()`` starts with ``'mingw'``.
    """
    ...

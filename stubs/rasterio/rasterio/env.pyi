"""Rasterio's GDAL/AWS environment"""

import logging
import threading
from collections.abc import Callable, Iterable
from types import TracebackType
from typing import Any, Final, TypeVar
from typing_extensions import Self, deprecated

from rasterio._env import (
    GDALDataFinder as GDALDataFinder,
    GDALEnv as GDALEnv,
    PROJDataFinder as PROJDataFinder,
    _GDALOption,
    get_gdal_config as get_gdal_config,
    set_gdal_config as set_gdal_config,
    set_proj_data_search_path as set_proj_data_search_path,
)
from rasterio.errors import (
    EnvError as EnvError,
    GDALVersionError as GDALVersionError,
    RasterioDeprecationWarning as RasterioDeprecationWarning,
)
from rasterio.session import DummySession as DummySession, Session as Session

_F = TypeVar("_F", bound=Callable[..., Any])

class ThreadEnv(threading.local):
    def __init__(self) -> None: ...

local: ThreadEnv
log: logging.Logger

class Env:
    """
    Abstraction for GDAL and AWS configuration

    The GDAL library is stateful: it has a registry of format drivers,
    an error stack, and dozens of configuration options.

    Rasterio's approach to working with GDAL is to wrap all the state
    up using a Python context manager (see PEP 343,
    https://www.python.org/dev/peps/pep-0343/). When the context is
    entered GDAL drivers are registered, error handlers are
    configured, and configuration options are set. When the context
    is exited, drivers are removed from the registry and other
    configurations are removed.

    Example
    -------
    .. code-block:: python

        with rasterio.Env(GDAL_CACHEMAX=128000000) as env:
            # All drivers are registered, GDAL's raster block cache
            # size is set to 128 MB.
            # Commence processing...
            ...
            # End of processing.

        # At this point, configuration options are set to their
        # previous (possible unset) values.

    A boto3 session or boto3 session constructor arguments
    `aws_access_key_id`, `aws_secret_access_key`, `aws_session_token`
    may be passed to Env's constructor. In the latter case, a session
    will be created as soon as needed. AWS credentials are configured
    for GDAL as needed.
    """
    session: Session
    options: dict[str, _GDALOption]
    context_options: dict[str, _GDALOption]
    def __init__(
        self,
        session: Session | None = None,
        aws_unsigned: bool = False,
        profile_name: str | None = None,
        session_class: Callable[..., Session] = ...,
        **options: _GDALOption,
    ) -> None:
        """
        Create a new GDAL/AWS environment.

        Note: this class is a context manager. GDAL isn't configured
        until the context is entered via `with rasterio.Env():`

        Parameters
        ----------
        session : optional
            A Session object.
        aws_unsigned : bool, optional
            Do not sign cloud requests.
        profile_name : str, optional
            A shared credentials profile name, as per boto3.
        session_class : Session, optional
            A sub-class of Session.
        **options : optional
            A mapping of GDAL configuration options, e.g.,
            `CPL_DEBUG=True, CHECK_WITH_INVERT_PROJ=False`.

        Returns
        -------
        Env

        Notes
        -----
        We raise EnvError if the GDAL config options
        AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY are given. AWS
        credentials are handled exclusively by boto3.

        Examples
        --------

        >>> with Env(CPL_DEBUG=True, CPL_CURL_VERBOSE=True):
        ...     with rasterio.open("https://example.com/a.tif") as src:
        ...         print(src.profile)

        For access to secured cloud resources, a Rasterio Session or a
        foreign session object may be passed to the constructor.

        >>> import boto3
        >>> from rasterio.session import AWSSession
        >>> boto3_session = boto3.Session(...)
        >>> with Env(AWSSession(boto3_session)):
        ...     with rasterio.open("s3://mybucket/a.tif") as src:
        ...         print(src.profile)
        """
        ...
    @classmethod
    def default_options(cls) -> dict[str, _GDALOption]:
        """
        Default configuration options

        Parameters
        ----------
        None

        Returns
        -------
        dict
        """
        ...
    # Forwarded to `cls(...)` after merging in default_options(); see __init__.
    @classmethod
    def from_defaults(cls, *args: Any, **kwargs: _GDALOption) -> Self:
        """
        Create an environment with default config options

        Parameters
        ----------
        args : optional
            Positional arguments for Env()
        kwargs : optional
            Keyword arguments for Env()

        Returns
        -------
        Env

        Notes
        -----
        The items in kwargs will be overlaid on the default values.
        """
        ...
    def credentialize(self) -> None:
        """
        Get credentials and configure GDAL

        Note well: this method is a no-op if the GDAL environment
        already has credentials, unless session is not None.

        Returns
        -------
        None
        """
        ...
    def aws_creds_from_context_options(self) -> dict[str, str]: ...
    def drivers(self) -> dict[str, str]:
        """Return a mapping of registered drivers."""
        ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_val: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None: ...

def defenv(**options: _GDALOption) -> None:
    """Create a default environment if necessary."""
    ...
def getenv() -> dict[str, _GDALOption]:
    """Get a mapping of current options."""
    ...
def hasenv() -> bool: ...
def setenv(**options: _GDALOption) -> None:
    """Set options in the existing environment."""
    ...
@deprecated("Please use Env.session.hascreds() instead.")
def hascreds() -> bool: ...
def delenv() -> None:
    """Delete options in the existing environment."""
    ...

class NullContextManager:
    def __init__(self) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, *args: object) -> None: ...

def env_ctx_if_needed() -> Env | NullContextManager:
    """
    Return an Env if one does not exist

    Returns
    -------
    Env or a do-nothing context manager
    """
    ...
def ensure_env(f: _F) -> _F:
    """
    A decorator that ensures an env exists before a function
    calls any GDAL C functions.
    """
    ...
@deprecated("ensure_env_credentialled is a deprecated alias; use ensure_env_with_credentials instead.")
def ensure_env_credentialled(f: _F) -> _F:
    """DEPRECATED alias for ensure_env_with_credentials"""
    ...
def ensure_env_with_credentials(f: _F) -> _F:
    """
    Ensures a config environment exists and is credentialized

    Parameters
    ----------
    f : function
        A function.

    Returns
    -------
    A function wrapper.

    Notes
    -----
    The function wrapper checks the first argument of f and
    credentializes the environment if the first argument is a URI with
    scheme "s3".
    """
    ...
def gdal_version() -> str:
    """Return the version as a major.minor.patchlevel string."""
    ...

class GDALVersion:
    """
    Convenience class for obtaining GDAL major and minor version components
    and comparing between versions.  This is highly simplistic and assumes a
    very normal numbering scheme for versions and ignores everything except
    the major and minor components.
    """
    major: int
    minor: int
    patch: int
    def __init__(self, major: int = 0, minor: int = 0, patch: int = 0) -> None:
        """Method generated by attrs for class GDALVersion."""
        ...
    def __eq__(self, other: object) -> bool:
        """Method generated by attrs for class GDALVersion."""
        ...
    def __lt__(self, other: GDALVersion) -> bool:
        """Method generated by attrs for class GDALVersion."""
        ...
    @classmethod
    def parse(cls, input: str | GDALVersion, include_patch: bool = False) -> Self:
        """
        Parses input tuple or string to GDALVersion. If input is a GDALVersion
        instance, it is returned.

        Parameters
        ----------
        input: tuple of (major, minor, patch), string, or instance of GDALVersion
        include_patch: bool, optional
            If True, patch version is included with comparisons.

        Returns
        -------
        GDALVersion instance
        """
        ...
    @classmethod
    def runtime(cls, include_patch: bool = False) -> Self:
        """Return GDALVersion of current GDAL runtime"""
        ...
    def at_least(self, other: str | GDALVersion, include_patch: bool = False) -> bool: ...

def require_gdal_version(
    version: str | GDALVersion,
    param: str | None = None,
    # `values` are matched against the decorated function's `param` argument; types depend on that argument.
    values: Iterable[Any] | None = None,
    is_max_version: bool = False,
    reason: str = "",
) -> Callable[[_F], _F]:
    """
    A decorator that ensures the called function or parameters are supported
    by the runtime version of GDAL.  Raises GDALVersionError if conditions
    are not met.

    Examples
    --------

    .. code-block:: python

        @require_gdal_version('2.2')
        def some_func():

    calling `some_func` with a runtime version of GDAL that is < 2.2 raises a
    GDALVersionErorr.

    .. code-block:: python

        @require_gdal_version('2.2', param='foo')
        def some_func(foo='bar'):

    calling `some_func` with parameter `foo` of any value on GDAL < 2.2 raises
    a GDALVersionError.

    .. code-block:: python

        @require_gdal_version('2.2', param='foo', values=('bar',))
        def some_func(foo=None):

    calling `some_func` with parameter `foo` and value `bar` on GDAL < 2.2
    raises a GDALVersionError.


    Parameters
    ------------
    version: tuple, string, or GDALVersion
    param: string (optional, default: None)
        If `values` are absent, then all use of this parameter with a value
        other than default value requires at least GDAL `version`.
    values: tuple, list, or set (optional, default: None)
        contains values that require at least GDAL `version`.  `param`
        is required for `values`.
    is_max_version: bool (optional, default: False)
        if `True` indicates that the version provided is the maximum version
        allowed, instead of requiring at least that version.
    reason: string (optional: default: '')
        custom error message presented to user in addition to message about
        GDAL version.  Use this to provide an explanation of what changed
        if necessary context to the user.

    Returns
    ---------
    wrapped function
    """
    ...

path: Final[str | None]

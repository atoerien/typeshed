"""Abstraction for sessions in various clouds."""

import logging
from typing import Any, Final

log: Final[logging.Logger]

def parse_bool(v: bool | str | int) -> bool:
    """CPLTestBool equivalent"""
    ...

class Session:
    """
    Base for classes that configure access to secured resources.

    Attributes
    ----------
    credentials : dict
        Keys and values for session credentials.

    Notes
    -----
    This class is not intended to be instantiated.
    """
    @classmethod
    def hascreds(cls, config: dict[str, Any]) -> bool:
        """
        Determine if the given configuration has proper credentials

        Parameters
        ----------
        cls : class
            A Session class.
        config : dict
            GDAL configuration as a dict.

        Returns
        -------
        bool
        """
        ...
    def get_credential_options(self) -> dict[str, str]:
        """
        Get credentials as GDAL configuration options

        Returns
        -------
        dict
        """
        ...
    # `session` is a foreign session object (e.g. boto3.session.Session,
    # google.auth.credentials.Credentials); the runtime dispatches by isinstance.
    @staticmethod
    def from_foreign_session(session: Any, cls: type[Session] | None = None) -> Session:
        """
        Create a session object matching the foreign `session`.

        Parameters
        ----------
        session : obj
            A foreign session object.
        cls : Session class, optional
            The class to return.

        Returns
        -------
        Session
        """
        ...
    @staticmethod
    def cls_from_path(path: str) -> type[Session]:
        """
        Find the session class suited to the data at `path`.

        Parameters
        ----------
        path : str
            A dataset path or identifier.

        Returns
        -------
        class
        """
        ...
    # Forwarded to the resolved session class' __init__; see its signature.
    @staticmethod
    def from_path(path: str, *args: Any, **kwargs: Any) -> Session:
        """
        Create a session object suited to the data at `path`.

        Parameters
        ----------
        path : str
            A dataset path or identifier.
        args : sequence
            Positional arguments for the foreign session constructor.
        kwargs : dict
            Keyword arguments for the foreign session constructor.

        Returns
        -------
        Session
        """
        ...
    @staticmethod
    def aws_or_dummy(*args: Any, **kwargs: Any) -> Session:
        """
        Create an AWSSession if boto3 is available, else DummySession

        Parameters
        ----------
        path : str
            A dataset path or identifier.
        args : sequence
            Positional arguments for the foreign session constructor.
        kwargs : dict
            Keyword arguments for the foreign session constructor.

        Returns
        -------
        Session
        """
        ...
    @staticmethod
    def from_environ(*args: Any, **kwargs: Any) -> Session:
        """
        Create a session object suited to the environment.

        Parameters
        ----------
        path : str
            A dataset path or identifier.
        args : sequence
            Positional arguments for the foreign session constructor.
        kwargs : dict
            Keyword arguments for the foreign session constructor.

        Returns
        -------
        Session
        """
        ...

class DummySession(Session):
    """
    A dummy session.

    Attributes
    ----------
    credentials : dict
        The session credentials.
    """
    credentials: dict[str, str]
    # Accepts and ignores any args (no credentials are configured).
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    @classmethod
    def hascreds(cls, config: dict[str, Any]) -> bool:
        """
        Determine if the given configuration has proper credentials

        Parameters
        ----------
        cls : class
            A Session class.
        config : dict
            GDAL configuration as a dict.

        Returns
        -------
        bool
        """
        ...
    def get_credential_options(self) -> dict[str, str]:
        """
        Get credentials as GDAL configuration options

        Returns
        -------
        dict
        """
        ...

class AWSSession(Session):
    """
    Configures access to secured resources stored in AWS S3.
    
    """
    requester_pays: bool
    unsigned: bool
    endpoint_url: str | None
    def __init__(
        self,
        # A `boto3.session.Session` instance, or None to construct one from the other kwargs.
        session: Any | None = None,
        aws_unsigned: bool | None = None,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        aws_session_token: str | None = None,
        region_name: str | None = None,
        profile_name: str | None = None,
        endpoint_url: str | None = None,
        requester_pays: bool = False,
    ) -> None:
        """
        Create a new AWS session

        Parameters
        ----------
        session : optional
            A boto3 session object.
        aws_unsigned : bool, optional (default: False)
            If True, requests will be unsigned.
        aws_access_key_id : str, optional
            An access key id, as per boto3.
        aws_secret_access_key : str, optional
            A secret access key, as per boto3.
        aws_session_token : str, optional
            A session token, as per boto3.
        region_name : str, optional
            A region name, as per boto3.
        profile_name : str, optional
            A shared credentials profile name, as per boto3.
        endpoint_url: str, optional
            An endpoint_url, as per GDAL's AWS_S3_ENPOINT
        requester_pays : bool, optional
            True if the requester agrees to pay transfer costs (default:
            False)
        """
        ...
    @classmethod
    def hascreds(cls, config: dict[str, Any]) -> bool:
        """
        Determine if the given configuration has proper credentials

        Parameters
        ----------
        cls : class
            A Session class.
        config : dict
            GDAL configuration as a dict.

        Returns
        -------
        bool
        """
        ...
    @property
    def credentials(self) -> dict[str, str]:
        """The session credentials as a dict"""
        ...
    def get_credential_options(self) -> dict[str, str]:
        """
        Get credentials as GDAL configuration options

        Returns
        -------
        dict
        """
        ...

class OSSSession(Session):
    """
    Configures access to secured resources stored in Alibaba Cloud OSS.
    
    """
    def __init__(
        self, oss_access_key_id: str | None = None, oss_secret_access_key: str | None = None, oss_endpoint: str | None = None
    ) -> None:
        """
        Create new Alibaba Cloud OSS session

        Parameters
        ----------
        oss_access_key_id: string, optional (default: None)
            An access key id
        oss_secret_access_key: string, optional (default: None)
            An secret access key
        oss_endpoint: string, optional (default: None)
            the region attached to the bucket
        """
        ...
    @classmethod
    def hascreds(cls, config: dict[str, Any]) -> bool:
        """
        Determine if the given configuration has proper credentials

        Parameters
        ----------
        cls : class
            A Session class.
        config : dict
            GDAL configuration as a dict.

        Returns
        -------
        bool
        """
        ...
    @property
    def credentials(self) -> dict[str, str]:
        """The session credentials as a dict"""
        ...
    def get_credential_options(self) -> dict[str, str]:
        """
        Get credentials as GDAL configuration options

        Returns
        -------
        dict
        """
        ...

class GSSession(Session):
    """
    Configures access to secured resources stored in Google Cloud Storage
    
    """
    def __init__(self, google_application_credentials: str | None = None) -> None:
        """
        Create new Google Cloud Storage session

        Parameters
        ----------
        google_application_credentials: string
            Path to the google application credentials JSON file.
        """
        ...
    @classmethod
    def hascreds(cls, config: dict[str, Any]) -> bool:
        """
        Determine if the given configuration has proper credentials

        Parameters
        ----------
        cls : class
            A Session class.
        config : dict
            GDAL configuration as a dict.

        Returns
        -------
        bool
        """
        ...
    @property
    def credentials(self) -> dict[str, str]:
        """The session credentials as a dict"""
        ...
    def get_credential_options(self) -> dict[str, str]:
        """
        Get credentials as GDAL configuration options

        Returns
        -------
        dict
        """
        ...

class SwiftSession(Session):
    """
    Configures access to secured resources stored in OpenStack Swift Object Storage.
    
    """
    def __init__(
        self,
        # A `swiftclient.Connection` instance, or None to construct one from the other kwargs.
        session: Any | None = None,
        swift_storage_url: str | None = None,
        swift_auth_token: str | None = None,
        swift_auth_v1_url: str | None = None,
        swift_user: str | None = None,
        swift_key: str | None = None,
    ) -> None:
        """
        Create new OpenStack Swift Object Storage Session.

        Three methods are possible:
            1. Create session by the swiftclient library.
            2. The SWIFT_STORAGE_URL and SWIFT_AUTH_TOKEN (this method is recommended by GDAL docs).
            3. The SWIFT_AUTH_V1_URL, SWIFT_USER and SWIFT_KEY (This depends on the swiftclient library).

        Parameters
        ----------
        session: optional
            A swiftclient connection object
        swift_storage_url:
            the storage URL
        swift_auth_token:
            the value of the x-auth-token authorization token
        swift_storage_url: string, optional
            authentication URL
        swift_user: string, optional
            user name to authenticate as
        swift_key: string, optional
            key/password to authenticate with

        Examples
        --------
        >>> import rasterio
        >>> from rasterio.session import SwiftSession
        >>> fp = '/vsiswift/bucket/key.tif'
        >>> conn = Connection(authurl='http://127.0.0.1:7777/auth/v1.0', user='test:tester', key='testing')
        >>> session = SwiftSession(conn)
        >>> with rasterio.Env(session):
        >>>     with rasterio.open(fp) as src:
        >>>         print(src.profile)
        """
        ...
    @classmethod
    def hascreds(cls, config: dict[str, Any]) -> bool:
        """
        Determine if the given configuration has proper credentials
        Parameters
        ----------
        cls : class
            A Session class.
        config : dict
            GDAL configuration as a dict.
        Returns
        -------
        bool
        """
        ...
    @property
    def credentials(self) -> dict[str, str]:
        """The session credentials as a dict"""
        ...
    def get_credential_options(self) -> dict[str, str]:
        """
        Get credentials as GDAL configuration options
        Returns
        -------
        dict
        """
        ...

class AzureSession(Session):
    """
    Configures access to secured resources stored in Microsoft Azure Blob Storage.
    
    """
    unsigned: bool
    storage_account: str | None
    def __init__(
        self,
        azure_storage_connection_string: str | None = None,
        azure_storage_account: str | None = None,
        azure_storage_access_token: str | None = None,
        azure_storage_access_key: str | None = None,
        azure_storage_sas_token: str | None = None,
        azure_unsigned: bool = False,
        azure_tenant_id: str | None = None,
        azure_client_id: str | None = None,
        azure_federated_token_file: str | None = None,
        azure_authority_host: str | None = None,
    ) -> None:
        """
        Create new Microsoft Azure Blob Storage session

        Authentication defaults to parameters first. If parameters do not
        result in a valid credentials object, environment variables are used.

        Parameters
        ----------
        azure_storage_connection_string: string
            A connection string contains both an account name and a secret key.
        azure_storage_account: string
            An account name
        azure_storage_access_token: string
            An access token
        azure_storage_access_key: string
            A secret key
        azure_storage_sas_token: string
            A sas token
        azure_unsigned : bool, optional (default: False)
            If True, requests will be unsigned.
        azure_tenant_id: str, optional (default: None)
            A tenant id
        azure_client_id: str, optional (default: None)
            A client id
        azure_federated_token_file: str, optional (default: None)
            The path to a token file.
        azure_authority_host: str, optional (default: None)
            The url of an authority host.
        """
        ...
    @classmethod
    def hascreds(cls, config: dict[str, Any]) -> bool:
        """
        Determine if the given configuration has proper credentials

        Parameters
        ----------
        cls : class
            A Session class.
        config : dict
            GDAL configuration as a dict.

        Returns
        -------
        bool
        """
        ...
    @property
    def credentials(self) -> dict[str, str]:
        """The session credentials as a dict"""
        ...
    def get_credential_options(self) -> dict[str, str]:
        """
        Get credentials as GDAL configuration options

        Returns
        -------
        dict
        """
        ...

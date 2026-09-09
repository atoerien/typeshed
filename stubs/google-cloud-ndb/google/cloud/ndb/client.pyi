"""A client for NDB which manages credentials, project, namespace, and database."""

from _typeshed import Incomplete
from collections.abc import Callable, Generator
from contextlib import contextmanager
from typing import ClassVar

from google.cloud.ndb import context as context_module, key

DATASTORE_API_HOST: str

class Client:
    """
    An NDB client.

    The NDB client must be created in order to use NDB, and any use of NDB must
    be within the context of a call to :meth:`context`.

    The Datastore Emulator is used for the client if and only if the
    DATASTORE_EMULATOR_HOST environment variable is set.

    Arguments:
        project (Optional[str]): The project to pass to proxied API methods. If
            not passed, falls back to the default inferred from the
            environment.
        namespace (Optional[str]): Namespace to pass to proxied API methods.
        credentials (Optional[:class:`~google.auth.credentials.Credentials`]):
            The OAuth2 Credentials to use for this client. If not passed, falls
            back to the default inferred from the environment.
        client_options (Optional[:class:`~google.api_core.client_options.ClientOptions` or :class:`dict`])
            Client options used to set user options on the client.
            API Endpoint should be set through client_options.
        database (Optional[str]): Database to access. Defaults to the (default) database.
    """
    SCOPE: ClassVar[tuple[str, ...]]
    namespace: str | None
    host: str
    client_info: Incomplete
    secure: bool
    stub: Incomplete
    database: str | None
    def __init__(
        self,
        project: str | None = None,
        namespace: str | None = None,
        credentials=None,
        client_options=None,
        database: str | None = None,
    ) -> None: ...
    @contextmanager
    def context(
        self,
        namespace=...,
        cache_policy: Callable[[key.Key], bool] | None = None,
        global_cache=None,
        global_cache_policy: Callable[[key.Key], bool] | None = None,
        global_cache_timeout_policy: Callable[[key.Key], int] | None = None,
        legacy_data: bool = True,
    ) -> Generator[context_module.Context]: ...

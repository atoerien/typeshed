from _typeshed import Incomplete
from collections.abc import Callable
from typing import type_check_only

from authlib.oauth2.rfc6750 import BearerTokenValidator
from authlib.oauth2.rfc7009 import RevocationEndpoint

@type_check_only
class _RevocationEndpoint(RevocationEndpoint):
    def query_token(self, token, token_type_hint): ...
    def revoke_token(self, token, request) -> None: ...

@type_check_only
class _BearerTokenValidator(BearerTokenValidator):
    def authenticate_token(self, token_string): ...

def create_query_client_func(session, client_model) -> Callable[[Incomplete], Incomplete]:
    """
    Create an ``query_client`` function that can be used in authorization
    server.

    :param session: SQLAlchemy session
    :param client_model: Client model class
    """
    ...
def create_save_token_func(session, token_model) -> Callable[[Incomplete, Incomplete], None]:
    """
    Create an ``save_token`` function that can be used in authorization
    server.

    :param session: SQLAlchemy session
    :param token_model: Token model class
    """
    ...
def create_query_token_func(session, token_model) -> Callable[[Incomplete, Incomplete], Incomplete]:
    """
    Create an ``query_token`` function for revocation, introspection
    token endpoints.

    :param session: SQLAlchemy session
    :param token_model: Token model class
    """
    ...
def create_revocation_endpoint(session, token_model) -> type[_RevocationEndpoint]:
    """
    Create a revocation endpoint class with SQLAlchemy session
    and token model.

    :param session: SQLAlchemy session
    :param token_model: Token model class
    """
    ...
def create_bearer_token_validator(session, token_model) -> type[_BearerTokenValidator]:
    """
    Create an bearer token validator class with SQLAlchemy session
    and token model.

    :param session: SQLAlchemy session
    :param token_model: Token model class
    """
    ...

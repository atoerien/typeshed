from _typeshed import Incomplete
from collections.abc import Callable

def register_temporary_credential_hooks(authorization_server, cache, key_prefix: str = "temporary_credential:") -> None:
    """
    Register temporary credential related hooks to authorization server.

    :param authorization_server: AuthorizationServer instance
    :param cache: Cache instance
    :param key_prefix: key prefix for temporary credential
    """
    ...
def create_exists_nonce_func(
    cache, key_prefix="nonce:", expires=86400
) -> Callable[[Incomplete, Incomplete, Incomplete, Incomplete], Incomplete]:
    """
    Create an ``exists_nonce`` function that can be used in hooks and
    resource protector.

    :param cache: Cache instance
    :param key_prefix: key prefix for temporary credential
    :param expires: Expire time for nonce
    """
    ...
def register_nonce_hooks(authorization_server, cache, key_prefix: str = "nonce:", expires=86400) -> None:
    """
    Register nonce related hooks to authorization server.

    :param authorization_server: AuthorizationServer instance
    :param cache: Cache instance
    :param key_prefix: key prefix for temporary credential
    :param expires: Expire time for nonce
    """
    ...

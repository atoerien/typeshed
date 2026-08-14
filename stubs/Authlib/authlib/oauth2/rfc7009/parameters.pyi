from typing import TypeVar

_K = TypeVar("_K")

def prepare_revoke_token_request(
    token: str, token_type_hint: str | None = None, body: str | None = None, headers: dict[str, _K] | None = None
) -> tuple[str, dict[str, _K | str]]:
    """
    Construct request body and headers for revocation endpoint.

    :param token: access_token or refresh_token string.
    :param token_type_hint: Optional, `access_token` or `refresh_token`.
    :param body: current request body.
    :param headers: current request headers.
    :return: tuple of (body, headers)

    https://tools.ietf.org/html/rfc7009#section-2.1
    """
    ...

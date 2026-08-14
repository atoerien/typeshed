from typing import Literal, TypeVar

_K = TypeVar("_K")

def add_to_uri(token: str, uri: str) -> str:
    """
    Add a Bearer Token to the request URI.
    Not recommended, use only if client can't use authorization header or body.

    http://www.example.com/path?access_token=h480djs93hd8
    """
    ...
def add_to_headers(token: str, headers: dict[str, _K] | None = None) -> dict[str, _K | str]:
    """
    Add a Bearer Token to the request URI.
    Recommended method of passing bearer tokens.

    Authorization: Bearer h480djs93hd8
    """
    ...
def add_to_body(token: str, body: str | None = None) -> str:
    """
    Add a Bearer Token to the request body.

    access_token=h480djs93hd8
    """
    ...
def add_bearer_token(
    token: str,
    uri: str,
    headers: dict[str, _K],
    body: str,
    placement: Literal["uri", "url", "query", "header", "headers", "body"] = "header",
) -> tuple[str, dict[str, _K | str], str]: ...

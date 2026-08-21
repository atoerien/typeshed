from _typeshed import Incomplete

from authlib.oauth2.rfc6750 import BearerTokenGenerator

class JWTBearerTokenGenerator(BearerTokenGenerator):
    r"""
    A JWT formatted access token generator.

    :param issuer: The issuer identifier. Will appear in the JWT ``iss`` claim.

    :param \\*\\*kwargs: Other parameters are inherited from
        :class:`~authlib.oauth2.rfc6750.token.BearerTokenGenerator`.

    This token generator can be registered into the authorization server::

        class MyJWTBearerTokenGenerator(JWTBearerTokenGenerator):
            def get_jwks(self): ...

            def get_extra_claims(self, client, grant_type, user, scope): ...


        authorization_server.register_token_generator(
            "default",
            MyJWTBearerTokenGenerator(
                issuer="https://authorization-server.example.org"
            ),
        )
    """
    issuer: Incomplete
    alg: Incomplete
    def __init__(self, issuer, alg: str = "RS256", refresh_token_generator=None, expires_generator=None) -> None: ...
    def get_jwks(self): ...
    def get_extra_claims(self, client, grant_type, user, scope): ...
    def get_audiences(self, client, user, scope) -> str | list[str]: ...
    def get_acr(self, user) -> str | None: ...
    def get_auth_time(self, user) -> int | None: ...
    def get_amr(self, user) -> list[str] | None: ...
    def get_jti(self, client, grant_type, user, scope) -> str: ...
    # Override seems safe, but mypy doesn't like that it's a callable protocol in the base
    def access_token_generator(self, client, grant_type, user, scope) -> str: ...  # type: ignore[override]

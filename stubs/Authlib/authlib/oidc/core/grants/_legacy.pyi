from _typeshed import Incomplete

from authlib.oauth2 import OAuth2Request

class LegacyMixin:
    DEFAULT_EXPIRES_IN: int
    def resolve_client_private_key(self, client):
        """
        Resolve the client private key for encoding ``id_token`` Developers
        MUST implement this method in subclass, e.g.::

            import json
            from joserfc.jwk import KeySet


            def resolve_client_private_key(self, client):
                with open(jwks_file_path) as f:
                    data = json.load(f)
                return KeySet.import_key_set(data)
        """
        ...
    def get_client_algorithm(self, client):
        """
        Return the algorithm for encoding ``id_token``.

        Per `OpenID Connect Registration 1.0 Section 2
        <https://openid.net/specs/openid-connect-registration-1_0.html#ClientMetadata>`_,
        the client metadata ``id_token_signed_response_alg`` takes precedence.
        It falls back to ``get_jwt_config()["alg"]`` (acting as a server-wide
        default) and finally to ``RS256``.
        """
        ...
    def get_client_claims(self, client) -> dict[str, Incomplete]:
        """
        Return the default client claims for encoding the ``id_token``. Developers
        MUST implement this method in subclass, e.g.::

            def get_client_claims(self, client):
                return {
                    "iss": "your-service-url",
                    "aud": [client.get_client_id()],
                }
        """
        ...
    def get_encode_header(self, client) -> dict[str, Incomplete]: ...
    def get_compatible_claims(self, request: OAuth2Request) -> dict[str, Incomplete]: ...

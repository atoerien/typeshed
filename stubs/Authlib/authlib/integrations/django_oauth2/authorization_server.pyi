from _typeshed import Incomplete

from authlib.oauth2 import AuthorizationServer as _AuthorizationServer
from authlib.oauth2.rfc6750 import BearerTokenGenerator

from .requests import DjangoJsonRequest, DjangoOAuth2Request

class AuthorizationServer(_AuthorizationServer):
    """
    Django implementation of :class:`authlib.oauth2.rfc6749.AuthorizationServer`.
    Initialize it with client model and token model::

        from authlib.integrations.django_oauth2 import AuthorizationServer
        from your_project.models import OAuth2Client, OAuth2Token

        server = AuthorizationServer(OAuth2Client, OAuth2Token)
    """
    client_model: Incomplete
    token_model: Incomplete
    def __init__(self, client_model, token_model) -> None: ...
    config: Incomplete
    scopes_supported: Incomplete
    def load_config(self, config) -> None: ...
    def query_client(self, client_id):
        """
        Default method for ``AuthorizationServer.query_client``. Developers MAY
        rewrite this function to meet their own needs.
        """
        ...
    def save_token(self, token, request):
        """
        Default method for ``AuthorizationServer.save_token``. Developers MAY
        rewrite this function to meet their own needs.
        """
        ...
    def create_oauth2_request(self, request) -> DjangoOAuth2Request: ...
    def create_json_request(self, request) -> DjangoJsonRequest: ...
    def handle_response(self, status_code, payload, headers): ...
    def send_signal(self, name, *args, **kwargs) -> None: ...
    def create_bearer_token_generator(self) -> BearerTokenGenerator:
        """Default method to create BearerToken generator."""
        ...

def create_token_generator(token_generator_conf, length: int = 42): ...
def create_token_expires_in_generator(expires_in_conf=None): ...

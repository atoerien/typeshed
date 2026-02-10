from _typeshed import Incomplete

from authlib.oauth2 import AuthorizationServer as _AuthorizationServer
from authlib.oauth2.rfc6750 import BearerTokenGenerator

from .requests import FlaskJsonRequest, FlaskOAuth2Request

class AuthorizationServer(_AuthorizationServer):
    """
    Flask implementation of :class:`authlib.oauth2.rfc6749.AuthorizationServer`.
    Initialize it with ``query_client``, ``save_token`` methods and Flask
    app instance::

        def query_client(client_id):
            return Client.query.filter_by(client_id=client_id).first()


        def save_token(token, request):
            if request.user:
                user_id = request.user.id
            else:
                user_id = None
            client = request.client
            tok = Token(client_id=client.client_id, user_id=user.id, **token)
            db.session.add(tok)
            db.session.commit()


        server = AuthorizationServer(app, query_client, save_token)
        # or initialize lazily
        server = AuthorizationServer()
        server.init_app(app, query_client, save_token)
    """
    def __init__(self, app=None, query_client=None, save_token=None) -> None: ...
    def init_app(self, app, query_client=None, save_token=None) -> None:
        """Initialize later with Flask app instance."""
        ...
    scopes_supported: Incomplete
    def load_config(self, config) -> None: ...
    def query_client(self, client_id): ...
    def save_token(self, token, request): ...
    def get_error_uri(self, request, error): ...
    def create_oauth2_request(self, request) -> FlaskOAuth2Request: ...
    def create_json_request(self, request) -> FlaskJsonRequest: ...
    def handle_response(self, status_code, payload, headers): ...
    def send_signal(self, name, *args, **kwargs) -> None: ...
    def create_bearer_token_generator(self, config) -> BearerTokenGenerator:
        """
        Create a generator function for generating ``token`` value. This
        method will create a Bearer Token generator with
        :class:`authlib.oauth2.rfc6750.BearerToken`.

        Configurable settings:

        1. OAUTH2_ACCESS_TOKEN_GENERATOR: Boolean or import string, default is True.
        2. OAUTH2_REFRESH_TOKEN_GENERATOR: Boolean or import string, default is False.
        3. OAUTH2_TOKEN_EXPIRES_IN: Dict or import string, default is None.

        By default, it will not generate ``refresh_token``, which can be turn on by
        configure ``OAUTH2_REFRESH_TOKEN_GENERATOR``.

        Here are some examples of the token generator::

            OAUTH2_ACCESS_TOKEN_GENERATOR = "your_project.generators.gen_token"

            # and in module `your_project.generators`, you can define:


            def gen_token(client, grant_type, user, scope):
                # generate token according to these parameters
                token = create_random_token()
                return f"{client.id}-{user.id}-{token}"

        Here is an example of ``OAUTH2_TOKEN_EXPIRES_IN``::

            OAUTH2_TOKEN_EXPIRES_IN = {
                "authorization_code": 864000,
                "urn:ietf:params:oauth:grant-type:jwt-bearer": 3600,
            }
        """
        ...

def create_token_expires_in_generator(expires_in_conf=None): ...
def create_token_generator(token_generator_conf, length: int = 42): ...

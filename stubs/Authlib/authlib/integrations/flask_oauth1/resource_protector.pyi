from _typeshed import Incomplete

from authlib.oauth1 import ResourceProtector as _ResourceProtector

class ResourceProtector(_ResourceProtector):
    """
    A protecting method for resource servers. Initialize a resource
    protector with the these method:

    1. query_client
    2. query_token,
    3. exists_nonce

    Usually, a ``query_client`` method would look like (if using SQLAlchemy)::

        def query_client(client_id):
            return Client.query.filter_by(client_id=client_id).first()

    A ``query_token`` method accept two parameters, ``client_id`` and ``oauth_token``::

        def query_token(client_id, oauth_token):
            return Token.query.filter_by(
                client_id=client_id, oauth_token=oauth_token
            ).first()

    And for ``exists_nonce``, if using cache, we have a built-in hook to create this method::

        from authlib.integrations.flask_oauth1 import create_exists_nonce_func

        exists_nonce = create_exists_nonce_func(cache)

    Then initialize the resource protector with those methods::

        require_oauth = ResourceProtector(
            app,
            query_client=query_client,
            query_token=query_token,
            exists_nonce=exists_nonce,
        )
    """
    app: Incomplete
    query_client: Incomplete
    query_token: Incomplete
    def __init__(self, app=None, query_client=None, query_token=None, exists_nonce=None) -> None: ...
    SUPPORTED_SIGNATURE_METHODS: Incomplete
    def init_app(self, app, query_client=None, query_token=None, exists_nonce=None): ...
    def get_client_by_id(self, client_id): ...
    def get_token_credential(self, request): ...
    def exists_nonce(self, nonce, request): ...
    def acquire_credential(self): ...
    def __call__(self, scope=None): ...

current_credential: Incomplete

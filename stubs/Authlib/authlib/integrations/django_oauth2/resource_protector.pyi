from _typeshed import Incomplete

from authlib.oauth2 import ResourceProtector as _ResourceProtector
from authlib.oauth2.rfc6750 import BearerTokenValidator as _BearerTokenValidator

class ResourceProtector(_ResourceProtector):
    def acquire_token(self, request, scopes=None, **kwargs):
        """
        A method to acquire current valid token with the given scope.

        :param request: Django HTTP request instance
        :param scopes: a list of scope values
        :return: token object
        """
        ...
    def __call__(self, scopes=None, optional=False, **kwargs): ...

class BearerTokenValidator(_BearerTokenValidator):
    token_model: Incomplete
    def __init__(self, token_model, realm=None, **extra_attributes): ...
    def authenticate_token(self, token_string): ...

def return_error_response(error): ...

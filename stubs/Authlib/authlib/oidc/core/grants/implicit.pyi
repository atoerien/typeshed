from _typeshed import Incomplete
from logging import Logger

from authlib.oauth2.rfc6749 import ImplicitGrant
from authlib.oidc.core import UserInfo

from ._legacy import LegacyMixin

log: Logger

class OpenIDImplicitGrant(LegacyMixin, ImplicitGrant):
    RESPONSE_TYPES: Incomplete
    DEFAULT_RESPONSE_MODE: str
    def exists_nonce(self, nonce, request) -> bool:
        """
        Check if the given nonce is existing in your database. Developers
        should implement this method in subclass, e.g.::

            def exists_nonce(self, nonce, request):
                exists = AuthorizationCode.query.filter_by(
                    client_id=request.payload.client_id, nonce=nonce
                ).first()
                return bool(exists)

        :param nonce: A string of "nonce" parameter in request
        :param request: OAuth2Request instance
        :return: Boolean
        """
        ...
    def generate_user_info(self, user, scope) -> UserInfo:
        """
        Provide user information for the given scope. Developers
        MUST implement this method in subclass, e.g.::

            from authlib.oidc.core import UserInfo


            def generate_user_info(self, user, scope):
                user_info = UserInfo(sub=user.id, name=user.name)
                if "email" in scope:
                    user_info["email"] = user.email
                return user_info

        :param user: user instance
        :param scope: scope of the token
        :return: ``authlib.oidc.core.UserInfo`` instance
        """
        ...
    def get_audiences(self, request) -> list[Incomplete]:
        """
        Parse `aud` value for id_token, default value is client id. Developers
        MAY rewrite this method to provide a customized audience value.
        """
        ...
    def validate_authorization_request(self) -> str: ...
    def validate_consent_request(self) -> str: ...
    def create_authorization_response(self, redirect_uri, grant_user): ...
    def create_granted_params(self, grant_user) -> list[tuple[str, Incomplete]]: ...
    def process_implicit_token(self, token, code=None): ...

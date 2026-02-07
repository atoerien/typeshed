from ..base_client import BaseApp, OAuth1Mixin, OAuth2Mixin, OpenIDMixin
from ..requests_client import OAuth1Session, OAuth2Session

class FlaskAppMixin:
    @property
    def token(self): ...
    @token.setter
    def token(self, token): ...
    def save_authorize_data(self, **kwargs) -> None: ...
    def authorize_redirect(self, redirect_uri=None, **kwargs):
        """
        Create a HTTP Redirect for Authorization Endpoint.

        :param redirect_uri: Callback or redirect URI for authorization.
        :param kwargs: Extra parameters to include.
        :return: A HTTP redirect response.
        """
        ...

class FlaskOAuth1App(FlaskAppMixin, OAuth1Mixin, BaseApp):
    client_cls = OAuth1Session
    def authorize_access_token(self, **kwargs):
        """
        Fetch access token in one step.

        :return: A token dict.
        """
        ...

class FlaskOAuth2App(FlaskAppMixin, OAuth2Mixin, OpenIDMixin, BaseApp):
    client_cls = OAuth2Session
    def authorize_access_token(self, **kwargs):
        """
        Fetch access token in one step.

        :return: A token dict.
        """
        ...

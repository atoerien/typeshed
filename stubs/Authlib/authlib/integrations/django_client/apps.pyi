from ..base_client import BaseApp, OAuth1Mixin, OAuth2Mixin, OpenIDMixin
from ..requests_client import OAuth1Session, OAuth2Session

class DjangoAppMixin:
    def save_authorize_data(self, request, **kwargs) -> None: ...
    def authorize_redirect(self, request, redirect_uri=None, **kwargs):
        """
        Create a HTTP Redirect for Authorization Endpoint.

        :param request: HTTP request instance from Django view.
        :param redirect_uri: Callback or redirect URI for authorization.
        :param kwargs: Extra parameters to include.
        :return: A HTTP redirect response.
        """
        ...

class DjangoOAuth1App(DjangoAppMixin, OAuth1Mixin, BaseApp):
    client_cls = OAuth1Session
    def authorize_access_token(self, request, **kwargs):
        """
        Fetch access token in one step.

        :param request: HTTP request instance from Django view.
        :return: A token dict.
        """
        ...

class DjangoOAuth2App(DjangoAppMixin, OAuth2Mixin, OpenIDMixin, BaseApp):
    client_cls = OAuth2Session
    def authorize_access_token(self, request, **kwargs):
        """
        Fetch access token in one step.

        :param request: HTTP request instance from Django view.
        :return: A token dict.
        """
        ...

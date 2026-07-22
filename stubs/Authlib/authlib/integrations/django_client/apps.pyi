from _typeshed import Incomplete
from typing import TypeAlias

from ..base_client import BaseApp, OAuth1Mixin, OAuth2Mixin, OpenIDMixin
from ..requests_client import OAuth1Session, OAuth2Session

_HttpResponseRedirect: TypeAlias = Incomplete  # actual type is django.http.response.HttpResponseRedirect

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
    def logout_redirect(
        self,
        request,
        post_logout_redirect_uri=None,
        id_token_hint=None,
        *,
        state=None,
        client_id=None,
        logout_hint=None,
        ui_locales=None,
    ) -> _HttpResponseRedirect:
        """
        Create a HTTP Redirect for End Session Endpoint (RP-Initiated Logout).

        :param request: HTTP request instance from Django view.
        :param post_logout_redirect_uri: URI to redirect after logout.
        :param id_token_hint: ID Token previously issued to the RP.
        :param kwargs: Extra parameters (state, client_id, logout_hint, ui_locales).
        :return: A HTTP redirect response.
        """
        ...
    def validate_logout_response(self, request):
        """
        Validate the state parameter from the logout callback.

        :param request: HTTP request instance from Django view.
        :return: The state data dict.
        :raises OAuthError: If state is missing or invalid.
        """
        ...
    def authorize_access_token(self, request, **kwargs):
        """
        Fetch access token in one step.

        :param request: HTTP request instance from Django view.
        :return: A token dict.
        """
        ...

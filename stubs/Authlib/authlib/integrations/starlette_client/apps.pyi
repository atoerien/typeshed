from _typeshed import Incomplete
from typing import TypeAlias

from ..base_client import BaseApp
from ..base_client.async_app import AsyncOAuth1Mixin, AsyncOAuth2Mixin
from ..base_client.async_openid import AsyncOpenIDMixin
from ..httpx_client import AsyncOAuth1Client, AsyncOAuth2Client

_RedirectResponse: TypeAlias = Incomplete  # actual type is starlette.responses.RedirectResponse

class StarletteAppMixin:
    async def save_authorize_data(self, request, **kwargs) -> None: ...
    async def authorize_redirect(self, request, redirect_uri=None, **kwargs) -> _RedirectResponse:
        """
        Create a HTTP Redirect for Authorization Endpoint.

        :param request: HTTP request instance from Starlette view.
        :param redirect_uri: Callback or redirect URI for authorization.
        :param kwargs: Extra parameters to include.
        :return: A HTTP redirect response.
        """
        ...

class StarletteOAuth1App(StarletteAppMixin, AsyncOAuth1Mixin, BaseApp):
    client_cls = AsyncOAuth1Client
    async def authorize_access_token(self, request, **kwargs): ...

class StarletteOAuth2App(StarletteAppMixin, AsyncOAuth2Mixin, AsyncOpenIDMixin, BaseApp):
    client_cls = AsyncOAuth2Client
    async def logout_redirect(
        self,
        request,
        post_logout_redirect_uri=None,
        id_token_hint=None,
        *,
        state=None,
        client_id=None,
        logout_hint=None,
        ui_locales=None,
    ) -> _RedirectResponse:
        """
        Create a HTTP Redirect for End Session Endpoint (RP-Initiated Logout).

        :param request: HTTP request instance from Starlette view.
        :param post_logout_redirect_uri: URI to redirect after logout.
        :param id_token_hint: ID Token previously issued to the RP.
        :param kwargs: Extra parameters (state, client_id, logout_hint, ui_locales).
        :return: A HTTP redirect response.
        """
        ...
    async def validate_logout_response(self, request):
        """
        Validate the state parameter from the logout callback.

        :param request: HTTP request instance from Starlette view.
        :return: The state data dict.
        :raises OAuthError: If state is missing or invalid.
        """
        ...
    async def authorize_access_token(self, request, **kwargs): ...

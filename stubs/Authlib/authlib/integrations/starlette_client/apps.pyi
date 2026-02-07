from ..base_client import BaseApp
from ..base_client.async_app import AsyncOAuth1Mixin, AsyncOAuth2Mixin
from ..base_client.async_openid import AsyncOpenIDMixin
from ..httpx_client import AsyncOAuth1Client, AsyncOAuth2Client

class StarletteAppMixin:
    async def save_authorize_data(self, request, **kwargs) -> None: ...
    async def authorize_redirect(self, request, redirect_uri=None, **kwargs):
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
    async def authorize_access_token(self, request, **kwargs): ...

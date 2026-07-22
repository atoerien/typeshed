from _typeshed import Incomplete
from typing import TypedDict, type_check_only

from authlib.oidc.core.claims import UserInfo

@type_check_only
class _LogoutData(TypedDict):
    url: str
    state: Incomplete

class OpenIDMixin:
    def fetch_jwk_set(self, force: bool = False): ...
    def userinfo(self, **kwargs) -> UserInfo:
        """Fetch user info from ``userinfo_endpoint``."""
        ...
    def parse_id_token(self, token, nonce, claims_options=None, claims_cls=None, leeway: int = 120) -> UserInfo | None:
        """Return an instance of UserInfo from token's ``id_token``."""
        ...
    def create_logout_url(
        self, post_logout_redirect_uri=None, id_token_hint=None, state=None, *, client_id=None, logout_hint=None, ui_locales=None
    ) -> _LogoutData:
        """
        Generate the end session URL for RP-Initiated Logout.

        :param post_logout_redirect_uri: URI to redirect after logout.
        :param id_token_hint: ID Token previously issued to the RP.
        :param state: Opaque value for maintaining state.
        :param kwargs: Extra parameters (client_id, logout_hint, ui_locales).
        :return: dict with 'url' and 'state' keys.
        """
        ...

from _typeshed import Incomplete
from collections.abc import Generator
from contextlib import contextmanager
from typing import NoReturn

from authlib.oauth2 import ResourceProtector as _ResourceProtector

class ResourceProtector(_ResourceProtector):
    """
    A protecting method for resource servers. Creating a ``require_oauth``
    decorator easily with ResourceProtector::

        from authlib.integrations.flask_oauth2 import ResourceProtector

        require_oauth = ResourceProtector()

        # add bearer token validator
        from authlib.oauth2.rfc6750 import BearerTokenValidator
        from project.models import Token


        class MyBearerTokenValidator(BearerTokenValidator):
            def authenticate_token(self, token_string):
                return Token.query.filter_by(access_token=token_string).first()


        require_oauth.register_token_validator(MyBearerTokenValidator())

        # protect resource with require_oauth


        @app.route("/user")
        @require_oauth(["profile"])
        def user_profile():
            user = User.get(current_token.user_id)
            return jsonify(user.to_dict())
    """
    def raise_error_response(self, error) -> NoReturn:
        """
        Raise HTTPException for OAuth2Error. Developers can re-implement
        this method to customize the error response.

        :param error: OAuth2Error
        :raise: HTTPException
        """
        ...
    def acquire_token(self, scopes=None, **kwargs):
        """
        A method to acquire current valid token with the given scope.

        :param scopes: a list of scope values
        :return: token object
        """
        ...
    @contextmanager
    def acquire(self, scopes=None) -> Generator[Incomplete]:
        """
        The with statement of ``require_oauth``. Instead of using a
        decorator, you can use a with statement instead::

            @app.route("/api/user")
            def user_api():
                with require_oauth.acquire("profile") as token:
                    user = User.get(token.user_id)
                    return jsonify(user.to_dict())
        """
        ...
    def __call__(self, scopes=None, optional=False, **kwargs): ...

current_token: Incomplete

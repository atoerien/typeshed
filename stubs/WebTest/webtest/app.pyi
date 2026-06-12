"""
Routines for testing WSGI applications.

Most interesting is TestApp
"""

import json
from _typeshed import SupportsItems, SupportsKeysAndGetItem
from _typeshed.wsgi import WSGIApplication, WSGIEnvironment
from collections.abc import Iterable, Sequence
from http.cookiejar import CookieJar, DefaultCookiePolicy
from typing import Any, Generic, Literal, TypeAlias, TypeVar

from webob.request import BaseRequest
from webtest.forms import File, Upload
from webtest.response import TestResponse

# NOTE: While it is possible to pass different kinds of values depending on
#       the exact configuration of the request, it seems more robust to
#       restrict them to the types that are supported by all code paths.
#       I don't expect anyone to try to pass different kinds of values
#       in a non-JSON request.
_ParamValue: TypeAlias = File | Upload | int | bytes | str
_Params: TypeAlias = SupportsItems[str | bytes, _ParamValue] | Sequence[tuple[str | bytes, _ParamValue]]
# NOTE: Using `Collection` rather than `Iterable` would probably be slightly
#       safer since WebTest will check this parameter for truthyness. But since
#       objects are truthy by default, this should only lead to issues in truly
#       exotic cases.
_ExtraEnviron: TypeAlias = SupportsKeysAndGetItem[str, Any] | Iterable[tuple[str, Any]]
_Files: TypeAlias = Sequence[tuple[str, str] | tuple[str, str, bytes]]
_AppT = TypeVar("_AppT", bound=WSGIApplication, default=WSGIApplication)

__all__ = ["TestApp", "TestRequest"]

class AppError(Exception):
    def __init__(self, message: str, *args: object) -> None: ...

class CookiePolicy(DefaultCookiePolicy):
    """
    A subclass of DefaultCookiePolicy to allow cookie set for
    Domain=localhost.
    """
    ...

class TestRequest(BaseRequest):
    """A subclass of webob.Request"""
    ResponseClass: type[TestResponse]
    __test__: Literal[False]

class TestApp(Generic[_AppT]):
    """
    Wraps a WSGI application in a more convenient interface for
    testing. It uses extended version of :class:`webob.BaseRequest`
    and :class:`webob.Response`.

    :param app:
        May be an WSGI application or Paste Deploy app,
        like ``'config:filename.ini#test'``.

        .. versionadded:: 2.0

        It can also be an actual full URL to an http server and webtest
        will proxy requests with `WSGIProxy2
        <https://pypi.org/project/WSGIProxy2/>`_.
    :type app:
        WSGI application
    :param extra_environ:
        A dictionary of values that should go
        into the environment for each request. These can provide a
        communication channel with the application.
    :type extra_environ:
        dict
    :param relative_to:
        A directory used for file
        uploads are calculated relative to this.  Also ``config:``
        URIs that aren't absolute.
    :type relative_to:
        string
    :param cookiejar:
        :class:`cookielib.CookieJar` alike API that keeps cookies
        across requests.
    :type cookiejar:
        CookieJar instance

    .. attribute:: cookies

        A convenient shortcut for a dict of all cookies in
        ``cookiejar``.

    :param parser_features:
        Passed to BeautifulSoup when parsing responses.
    :type parser_features:
        string or list
    :param json_encoder:
        Passed to json.dumps when encoding json
    :type json_encoder:
        A subclass of json.JSONEncoder
    :param lint:
        If True (default) then check that the application is WSGI compliant
    :type lint:
        A boolean
    """
    RequestClass: type[TestRequest]
    app: _AppT
    lint: bool
    relative_to: str | None
    extra_environ: WSGIEnvironment
    use_unicode: bool
    cookiejar: CookieJar
    JSONEncoder: json.JSONEncoder
    __test__: Literal[False]
    def __init__(
        self,
        app: _AppT,
        # NOTE: this extra_environ is different from the others and needs to
        #       support __delitem__, it seems easiest to just treat this like
        #       a regular WSGIEnvironment. The docs also say that this should
        #       be a dictionary.
        extra_environ: WSGIEnvironment | None = None,
        relative_to: str | None = None,
        use_unicode: bool = True,
        cookiejar: CookieJar | None = None,
        parser_features: Sequence[str] | str | None = None,
        json_encoder: json.JSONEncoder | None = None,
        lint: bool = True,
    ) -> None: ...
    def get_authorization(self) -> tuple[str, str | tuple[str, str]]:
        """
        Allow to set the HTTP_AUTHORIZATION environ key. Value should look
        like one of the following:

        * ``('Basic', ('user', 'password'))``
        * ``('Bearer', 'mytoken')``
        * ``('JWT', 'myjwt')``

        If value is None the the HTTP_AUTHORIZATION is removed
        """
        ...
    def set_authorization(self, value: tuple[str, str | tuple[str, str]]) -> None: ...

    @property
    def authorization(self) -> tuple[str, str | tuple[str, str]]:
        """
        Allow to set the HTTP_AUTHORIZATION environ key. Value should look
        like one of the following:

        * ``('Basic', ('user', 'password'))``
        * ``('Bearer', 'mytoken')``
        * ``('JWT', 'myjwt')``

        If value is None the the HTTP_AUTHORIZATION is removed
        """
        ...
    @authorization.setter
    def authorization(self, value: tuple[str, str | tuple[str, str]]) -> None:
        """
        Allow to set the HTTP_AUTHORIZATION environ key. Value should look
        like one of the following:

        * ``('Basic', ('user', 'password'))``
        * ``('Bearer', 'mytoken')``
        * ``('JWT', 'myjwt')``

        If value is None the the HTTP_AUTHORIZATION is removed
        """
        ...

    @property
    def cookies(self) -> dict[str, str | None]: ...
    def set_cookie(self, name: str, value: str | None) -> None:
        """Sets a cookie to be passed through with requests."""
        ...
    def reset(self) -> None:
        """
        Resets the state of the application; currently just clears
        saved cookies.
        """
        ...
    def set_parser_features(self, parser_features: Sequence[str] | str) -> None:
        """
        Changes the parser used by BeautifulSoup. See its documentation to
        know the supported parsers.
        """
        ...
    def get(
        self,
        url: str,
        params: _Params | str | None = None,
        headers: dict[str, str] | None = None,
        extra_environ: _ExtraEnviron | None = None,
        status: int | str | None = None,
        expect_errors: bool = False,
        xhr: bool = False,
    ) -> TestResponse:
        """
        Do a GET request given the url path.

        :param params:
            A query string, or a dictionary that will be encoded
            into a query string.  You may also include a URL query
            string on the ``url``.
        :param headers:
            Extra headers to send.
        :type headers:
            dictionary
        :param extra_environ:
            Environmental variables that should be added to the request.
        :type extra_environ:
            dictionary
        :param status:
            The HTTP status code you expect in response (if not 200 or 3xx).
            You can also use a wildcard, like ``'3*'`` or ``'*'``.
        :type status:
            integer or string
        :param expect_errors:
            If this is False, then if anything is written to
            environ ``wsgi.errors`` it will be an error.
            If it is True, then non-200/3xx responses are also okay.
        :type expect_errors:
            boolean
        :param xhr:
            If this is true, then marks response as ajax. The same as
            headers={'X-REQUESTED-WITH': 'XMLHttpRequest', }
        :type xhr:
            boolean

        :returns: :class:`webtest.TestResponse` instance.
        """
        ...
    def post(
        self,
        url: str,
        params: _Params | str = "",
        headers: dict[str, str] | None = None,
        extra_environ: _ExtraEnviron | None = None,
        status: int | str | None = None,
        upload_files: _Files | None = None,
        expect_errors: bool = False,
        content_type: str | None = None,
        xhr: bool = False,
    ) -> TestResponse:
        """
        Do a POST request. Similar to :meth:`~webtest.TestApp.get`.

        :param params:
            Are put in the body of the request. If params is an
            iterator, it will be urlencoded. If it is a string, it will not
            be encoded, but placed in the body directly.

            Can be a :class:`python:collections.OrderedDict` with
            :class:`webtest.forms.Upload` fields included::

                app.post('/myurl', collections.OrderedDict([
                    ('textfield1', 'value1'),
                    ('uploadfield', webapp.Upload('filename.txt', 'contents'),
                    ('textfield2', 'value2')])))

        :param upload_files:
            It should be a list of ``(fieldname, filename, file_content)``.
            You can also use just ``(fieldname, filename)`` and the file
            contents will be read from disk.
        :type upload_files:
            list
        :param content_type:
            HTTP content type, for example `application/json`.
        :type content_type:
            string

        :param xhr:
            If this is true, then marks response as ajax. The same as
            headers={'X-REQUESTED-WITH': 'XMLHttpRequest', }
        :type xhr:
            boolean

        :returns: :class:`webtest.TestResponse` instance.
        """
        ...
    def put(
        self,
        url: str,
        params: _Params | str = "",
        headers: dict[str, str] | None = None,
        extra_environ: _ExtraEnviron | None = None,
        status: int | str | None = None,
        upload_files: _Files | None = None,
        expect_errors: bool = False,
        content_type: str | None = None,
        xhr: bool = False,
    ) -> TestResponse:
        """
        Do a PUT request. Similar to :meth:`~webtest.TestApp.post`.

        :returns: :class:`webtest.TestResponse` instance.
        """
        ...
    def patch(
        self,
        url: str,
        params: _Params | str = "",
        headers: dict[str, str] | None = None,
        extra_environ: _ExtraEnviron | None = None,
        status: int | str | None = None,
        upload_files: _Files | None = None,
        expect_errors: bool = False,
        content_type: str | None = None,
        xhr: bool = False,
    ) -> TestResponse:
        """
        Do a PATCH request. Similar to :meth:`~webtest.TestApp.post`.

        :returns: :class:`webtest.TestResponse` instance.
        """
        ...
    def delete(
        self,
        url: str,
        params: _Params | str = "",
        headers: dict[str, str] | None = None,
        extra_environ: _ExtraEnviron | None = None,
        status: int | str | None = None,
        expect_errors: bool = False,
        content_type: str | None = None,
        xhr: bool = False,
    ) -> TestResponse:
        """
        Do a DELETE request. Similar to :meth:`~webtest.TestApp.get`.

        :returns: :class:`webtest.TestResponse` instance.
        """
        ...
    def options(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        extra_environ: _ExtraEnviron | None = None,
        status: int | str | None = None,
        expect_errors: bool = False,
        xhr: bool = False,
    ) -> TestResponse:
        """
        Do a OPTIONS request. Similar to :meth:`~webtest.TestApp.get`.

        :returns: :class:`webtest.TestResponse` instance.
        """
        ...
    def head(
        self,
        url: str,
        params: _Params | str | None = None,
        headers: dict[str, str] | None = None,
        extra_environ: _ExtraEnviron | None = None,
        status: int | str | None = None,
        expect_errors: bool = False,
        xhr: bool = False,
    ) -> TestResponse:
        """
        Do a HEAD request. Similar to :meth:`~webtest.TestApp.get`.

        :returns: :class:`webtest.TestResponse` instance.
        """
        ...
    def post_json(
        self,
        url: str,
        params: Any = ...,
        *,
        headers: dict[str, str] | None = None,
        extra_environ: _ExtraEnviron | None = None,
        status: int | str | None = None,
        expect_errors: bool = False,
        content_type: str | None = None,
        xhr: bool = False,
    ) -> TestResponse:
        """
        Do a POST request.  Very like the
        :class:`~webtest.TestApp.post` method.

        ``params`` are dumped to json and put in the body of the request.
        Content-Type is set to ``application/json``.

        Returns a :class:`webtest.TestResponse` object.
        """
        ...
    def put_json(
        self,
        url: str,
        params: Any = ...,
        *,
        headers: dict[str, str] | None = None,
        extra_environ: _ExtraEnviron | None = None,
        status: int | str | None = None,
        expect_errors: bool = False,
        content_type: str | None = None,
        xhr: bool = False,
    ) -> TestResponse:
        """
        Do a PUT request.  Very like the
        :class:`~webtest.TestApp.put` method.

        ``params`` are dumped to json and put in the body of the request.
        Content-Type is set to ``application/json``.

        Returns a :class:`webtest.TestResponse` object.
        """
        ...
    def patch_json(
        self,
        url: str,
        params: Any = ...,
        *,
        headers: dict[str, str] | None = None,
        extra_environ: _ExtraEnviron | None = None,
        status: int | str | None = None,
        expect_errors: bool = False,
        content_type: str | None = None,
        xhr: bool = False,
    ) -> TestResponse:
        """
        Do a PATCH request.  Very like the
        :class:`~webtest.TestApp.patch` method.

        ``params`` are dumped to json and put in the body of the request.
        Content-Type is set to ``application/json``.

        Returns a :class:`webtest.TestResponse` object.
        """
        ...
    def delete_json(
        self,
        url: str,
        params: Any = ...,
        *,
        headers: dict[str, str] | None = None,
        extra_environ: _ExtraEnviron | None = None,
        status: int | str | None = None,
        expect_errors: bool = False,
        content_type: str | None = None,
        xhr: bool = False,
    ) -> TestResponse:
        """
        Do a DELETE request.  Very like the
        :class:`~webtest.TestApp.delete` method.

        ``params`` are dumped to json and put in the body of the request.
        Content-Type is set to ``application/json``.

        Returns a :class:`webtest.TestResponse` object.
        """
        ...
    def encode_multipart(self, params: Iterable[tuple[str | bytes, _ParamValue]], files: _Files) -> tuple[str, bytes]:
        """
        Encodes a set of parameters (typically a name/value list) and
        a set of files (a list of (name, filename, file_body, mimetype)) into a
        typical POST body, returning the (content_type, body).
        """
        ...
    def request(
        self, url_or_req: str | TestRequest, status: int | str | None = None, expect_errors: bool = False, **req_params: Any
    ) -> TestResponse:
        """
        Creates and executes a request. You may either pass in an
        instantiated :class:`TestRequest` object, or you may pass in a
        URL and keyword arguments to be passed to
        :meth:`TestRequest.blank`.

        You can use this to run a request without the intermediary
        functioning of :meth:`TestApp.get` etc.  For instance, to
        test a WebDAV method::

            resp = app.request('/new-col', method='MKCOL')

        Note that the request won't have a body unless you specify it,
        like::

            resp = app.request('/test.txt', method='PUT', body='test')

        You can use :class:`webtest.TestRequest`::

            req = webtest.TestRequest.blank('/url/', method='GET')
            resp = app.do_request(req)
        """
        ...
    def do_request(
        self, req: TestRequest, status: int | str | None = None, expect_errors: bool | None = None
    ) -> TestResponse:
        """
        Executes the given webob Request (``req``), with the expected
        ``status``.  Generally :meth:`~webtest.TestApp.get` and
        :meth:`~webtest.TestApp.post` are used instead.

        To use this::

            req = webtest.TestRequest.blank('url', ...args...)
            resp = app.do_request(req)

        .. note::

            You can pass any keyword arguments to
            ``TestRequest.blank()``, which will be set on the request.
            These can be arguments like ``content_type``, ``accept``, etc.
        """
        ...

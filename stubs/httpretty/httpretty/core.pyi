import re
from collections.abc import Callable, Iterable, Mapping
from contextlib import AbstractContextManager
from http.client import HTTPMessage
from types import TracebackType
from typing import Any, Protocol, TypeAlias, overload, type_check_only
from typing_extensions import ParamSpec, TypeVar

from .http import HttpBaseClass, _HTTPMethod

_P = ParamSpec("_P")
_R = TypeVar("_R")

@type_check_only
class _WritableFileobj(Protocol):
    def write(self, b: bytes, /) -> object: ...
    def seek(self, offset: int, /) -> object: ...

_URI: TypeAlias = str | re.Pattern[str]
_HeaderValue: TypeAlias = str | int | bool | None
_Headers: TypeAlias = Mapping[str, _HeaderValue]
_Body: TypeAlias = str | bytes
_ResponseBody: TypeAlias = _Body | Callable[[HTTPrettyRequest, str, _Headers], tuple[int, _Headers, _Body]]

def set_default_thread_timeout(timeout: float) -> None:
    """
    sets the default thread timeout for HTTPretty threads

    :param timeout: int
    """
    ...
def get_default_thread_timeout() -> float:
    """
    sets the default thread timeout for HTTPretty threads

    :returns: int
    """
    ...

class HTTPrettyRequest(HttpBaseClass):
    r"""
    Represents a HTTP request. It takes a valid multi-line,
    ``\r\n`` separated string with HTTP headers and parse them out using
    the internal `parse_request` method.

    It also replaces the `rfile` and `wfile` attributes with :py:class:`io.BytesIO`
    instances so that we guarantee that it won't make any I/O, neither
    for writing nor reading.

    It has some convenience attributes:

    ``headers`` -> a mimetype object that can be cast into a dictionary,
    contains all the request headers

    ``protocol`` -> the protocol of this host, inferred from the port
    of the underlying fake TCP socket.

    ``host`` -> the hostname of this request.

    ``url`` -> the full url of this request.

    ``path`` -> the path of the request.

    ``method`` -> the HTTP method used in this request.

    ``querystring`` -> a dictionary containing lists with the
    attributes. Please notice that if you need a single value from a
    query string you will need to get it manually like:

    ``body`` -> the request body as a string.

    ``parsed_body`` -> the request body parsed by ``parse_request_body``.

    .. testcode::

      >>> request.querystring
      {'name': ['Gabriel Falcao']}
      >>> print request.querystring['name'][0]
    """
    headers: HTTPMessage
    raw_headers: str
    path: str
    querystring: dict[str, list[str]]
    parsed_body: Any  # It can be any object after parsing raw (str) body
    created_at: float
    def __init__(
        self, headers: str | bytes, body: _Body = "", sock: object | None = None, path_encoding: str = "iso-8859-1"
    ) -> None: ...
    @property
    def method(self) -> str:
        """the HTTP method used in this request"""
        ...
    @property
    def protocol(self) -> str:
        """the protocol used in this request"""
        ...

    @property
    def body(self) -> str: ...
    @body.setter
    def body(self, value: _Body) -> None: ...

    @property
    def url(self) -> str:
        """the full url of this recorded request"""
        ...
    @property
    def host(self) -> str: ...
    def parse_querystring(self, qs: str) -> dict[str, list[str]]:
        """
        parses an UTF-8 encoded query string into a dict of string lists

        :param qs: a querystring
        :returns: a dict of lists
        """
        ...
    def parse_request_body(self, body: str) -> Any:
        """
        Attempt to parse the post based on the content-type passed.
        Return the regular body if not

        :param body: string
        :returns: a python object such as dict or list in case the deserialization suceeded. Else returns the given param ``body``
        """
        ...

class EmptyRequestHeaders(dict[str, str]):
    """
    A dict subclass used as internal representation of empty request
    headers
    """
    ...

class HTTPrettyRequestEmpty:
    """
    Represents an empty :py:class:`~httpretty.core.HTTPrettyRequest`
    where all its properties are somehow empty or ``None``
    """
    method: str | None
    url: str | None
    body: str
    headers: EmptyRequestHeaders

class Entry(HttpBaseClass):
    """
    Created by :py:meth:`~httpretty.core.httpretty.register_uri` and
    stored in memory as internal representation of a HTTP
    request/response definition.

    Args:
        method (str): One of ``httpretty.GET``, ``httpretty.PUT``, ``httpretty.POST``, ``httpretty.DELETE``, ``httpretty.HEAD``, ``httpretty.PATCH``, ``httpretty.OPTIONS``, ``httpretty.CONNECT``.
        uri (str|re.Pattern): The URL to match
        adding_headers (dict): Extra headers to be added to the response
        forcing_headers (dict): Overwrite response headers.
        status (int): The status code for the response, defaults to ``200``.
        streaming (bool): Whether should stream the response into chunks via generator.
        headers: Headers to inject in the faked response.

    Returns:
        httpretty.Entry: containing the request-matching metadata.


    .. warning:: When using the ``forcing_headers`` option make sure to add the header ``Content-Length`` to match at most the total body length, otherwise some HTTP clients can hang indefinitely.
    """
    method: _HTTPMethod
    uri: str
    request: HTTPrettyRequest
    body: _Body
    status: int
    streaming: bool
    adding_headers: dict[str, str]
    forcing_headers: dict[str, str]
    def __init__(
        self,
        method: str,
        uri: str,
        body: _ResponseBody,
        adding_headers: _Headers | None = None,
        forcing_headers: _Headers | None = None,
        status: int = 200,
        streaming: bool = False,
        **headers: str,
    ) -> None: ...
    def validate(self) -> None:
        """
        validates the body size with the value of the ``Content-Length``
        header
        """
        ...
    def normalize_headers(self, headers: _Headers) -> dict[str, str]:
        """
        Normalize keys in header names so that ``COntent-tyPe`` becomes ``content-type``

        :param headers: dict

        :returns: dict
        """
        ...
    def fill_filekind(self, fk: _WritableFileobj) -> None:
        """
        writes HTTP Response data to a file descriptor

        :parm fk: a file-like object

        .. warning:: **side-effect:** this method moves the cursor of the given file object to zero
        """
        ...

class URIInfo(HttpBaseClass):
    """
    Internal representation of `URIs <https://en.wikipedia.org/wiki/Uniform_Resource_Identifier>`_

    .. tip:: all arguments are optional

    :param username:
    :param password:
    :param hostname:
    :param port:
    :param path:
    :param query:
    :param fragment:
    :param scheme:
    :param last_request:
    """
    default_str_attrs: tuple[str, ...]
    username: str
    password: str
    hostname: str
    port: int
    path: str
    query: str
    scheme: str
    fragment: str
    last_request: HTTPrettyRequest | None
    def __init__(
        self,
        username: str = "",
        password: str = "",
        hostname: str = "",
        port: int = 80,
        path: str = "/",
        query: str = "",
        fragment: str = "",
        scheme: str = "",
        last_request: HTTPrettyRequest | None = None,
    ) -> None: ...
    def to_str(self, attrs: Iterable[str]) -> str: ...
    def str_with_query(self) -> str: ...
    def full_url(self, use_querystring: bool = True) -> str:
        """
        :param use_querystring: bool
        :returns: a string with the full url with the format ``{scheme}://{credentials}{domain}{path}{query}``
        """
        ...
    def get_full_domain(self) -> str:
        """:returns: a string in the form ``{domain}:{port}`` or just the domain if the port is 80 or 443"""
        ...
    @classmethod
    def from_uri(cls, uri: str, entry: Entry) -> URIInfo:
        """
        :param uri: string
        :param entry: an instance of :py:class:`~httpretty.core.Entry`
        """
        ...

class URIMatcher:
    regex: re.Pattern[str] | None
    info: URIInfo | None
    entries: list[Entry]
    priority: int
    uri: _URI
    def __init__(self, uri: _URI, entries: Iterable[Entry], match_querystring: bool = False, priority: int = 0) -> None: ...
    def matches(self, info: URIInfo) -> bool: ...
    def get_next_entry(self, method: _HTTPMethod, info: URIInfo, request: HTTPrettyRequest) -> Entry:
        """
        Cycle through available responses, but only once.
        Any subsequent requests will receive the last response
        """
        ...

class httpretty(HttpBaseClass):
    """
    manages HTTPretty's internal request/response registry and request matching.
    
    """
    METHODS: tuple[_HTTPMethod, ...]
    latest_requests: list[HTTPrettyRequest]
    last_request: HTTPrettyRequest | HTTPrettyRequestEmpty
    allow_net_connect: bool
    @classmethod
    def match_uriinfo(cls, info: URIInfo) -> tuple[Entry | None, list[str]]:
        """
        :param info: an :py:class:`~httpretty.core.URIInfo`
        :returns: a 2-item tuple: (:py:class:`~httpretty.core.URLMatcher`, :py:class:`~httpretty.core.URIInfo`) or ``(None, [])``
        """
        ...
    @classmethod
    def match_https_hostname(cls, hostname: str) -> bool:
        """
        :param hostname: a string
        :returns: an :py:class:`~httpretty.core.URLMatcher` or ``None``
        """
        ...
    @classmethod
    def match_http_address(cls, hostname: str, port: int) -> bool:
        """
        :param hostname: a string
        :param port: an integer
        :returns: an :py:class:`~httpretty.core.URLMatcher` or ``None``
        """
        ...
    @classmethod
    def record(
        cls,
        filename: str,
        indentation: int = 4,
        encoding: str = "utf-8",
        verbose: bool = False,
        allow_net_connect: bool = True,
        # Passed to urllib3.PoolManager as kwargs, and connection pool's parameters have various types
        pool_manager_params: Mapping[str, Any] | None = None,
    ) -> AbstractContextManager[None]:
        """
        .. testcode::

           import io
           import json
           import requests
           import httpretty

           with httpretty.record('/tmp/ip.json'):
               data = requests.get('https://httpbin.org/ip').json()

           with io.open('/tmp/ip.json') as fd:
               assert data == json.load(fd)

        :param filename: a string
        :param indentation: an integer, defaults to **4**
        :param encoding: a string, defaults to **"utf-8"**

        :returns: a `context-manager <https://docs.python.org/3/reference/datamodel.html#context-managers>`_
        """
        ...
    @classmethod
    def playback(cls, filename: str, allow_net_connect: bool = True, verbose: bool = False) -> AbstractContextManager[None]:
        """
        .. testcode::

           import io
           import json
           import requests
           import httpretty

           with httpretty.record('/tmp/ip.json'):
               data = requests.get('https://httpbin.org/ip').json()

           with io.open('/tmp/ip.json') as fd:
               assert data == json.load(fd)

        :param filename: a string
        :returns: a `context-manager <https://docs.python.org/3/reference/datamodel.html#context-managers>`_
        """
        ...
    @classmethod
    def reset(cls) -> None:
        """
        resets the internal state of HTTPretty, unregistering all URLs
        
        """
        ...
    @classmethod
    def historify_request(cls, headers: str | bytes, body: _Body = "", sock: object | None = None) -> HTTPrettyRequest:
        """
        appends request to a list for later retrieval

        .. testcode::

           import httpretty

           httpretty.register_uri(httpretty.GET, 'https://httpbin.org/ip', body='')
           with httpretty.enabled():
               requests.get('https://httpbin.org/ip')

           assert httpretty.latest_requests[-1].url == 'https://httpbin.org/ip'
        """
        ...
    @classmethod
    def register_uri(
        cls,
        method: str,
        uri: _URI,
        body: _ResponseBody = '{"message": "HTTPretty :)"}',
        adding_headers: _Headers | None = None,
        forcing_headers: _Headers | None = None,
        status: int = 200,
        responses: Iterable[Entry] | None = None,
        match_querystring: bool = False,
        priority: int = 0,
        **headers: str,
    ) -> None:
        """
        .. testcode::

           import httpretty


           def request_callback(request, uri, response_headers):
               content_type = request.headers.get('Content-Type')
               assert request.body == '{"nothing": "here"}', 'unexpected body: {}'.format(request.body)
               assert content_type == 'application/json', 'expected application/json but received Content-Type: {}'.format(content_type)
               return [200, response_headers, json.dumps({"hello": "world"})]

           httpretty.register_uri(
               HTTPretty.POST, "https://httpretty.example.com/api",
               body=request_callback)


           with httpretty.enabled():
               requests.post('https://httpretty.example.com/api', data='{"nothing": "here"}', headers={'Content-Type': 'application/json'})

           assert httpretty.latest_requests[-1].url == 'https://httpbin.org/ip'

        :param method: one of ``httpretty.GET``, ``httpretty.PUT``, ``httpretty.POST``, ``httpretty.DELETE``, ``httpretty.HEAD``, ``httpretty.PATCH``, ``httpretty.OPTIONS``, ``httpretty.CONNECT``
        :param uri: a string or regex pattern (e.g.: **"https://httpbin.org/ip"**)
        :param body: a string, defaults to ``{"message": "HTTPretty :)"}``
        :param adding_headers: dict - headers to be added to the response
        :param forcing_headers: dict - headers to be forcefully set in the response
        :param status: an integer, defaults to **200**
        :param responses: a list of entries, ideally each created with :py:meth:`~httpretty.core.httpretty.Response`
        :param priority: an integer, useful for setting higher priority over previously registered urls. defaults to zero
        :param match_querystring: bool - whether to take the querystring into account when matching an URL
        :param headers: headers to be added to the response

        .. warning:: When using a port in the request, add a trailing slash if no path is provided otherwise Httpretty will not catch the request.  Ex: ``httpretty.register_uri(httpretty.GET, 'http://fakeuri.com:8080/', body='{"hello":"world"}')``
        """
        ...
    @classmethod
    def Response(
        cls,
        body: _ResponseBody,
        method: _HTTPMethod | None = None,
        uri: str | None = None,
        adding_headers: _Headers | None = None,
        forcing_headers: _Headers | None = None,
        status: int = 200,
        streaming: bool = False,
        **headers: str,
    ) -> Entry:
        """
        Shortcut to create an :py:class:`~httpretty.core.Entry` that takes
        the body as first positional argument.

        .. seealso:: the parameters of this function match those of
                     the :py:class:`~httpretty.core.Entry` constructor.

        Args:
            body (str): The body to return as response..
            method (str): One of ``httpretty.GET``, ``httpretty.PUT``, ``httpretty.POST``, ``httpretty.DELETE``, ``httpretty.HEAD``, ``httpretty.PATCH``, ``httpretty.OPTIONS``, ``httpretty.CONNECT``.
            uri (str|re.Pattern): The URL to match
            adding_headers (dict): Extra headers to be added to the response
            forcing_headers (dict): Overwrite **any** response headers, even "Content-Length".
            status (int): The status code for the response, defaults to ``200``.
            streaming (bool): Whether should stream the response into chunks via generator.
            kwargs: Keyword-arguments are forwarded to :py:class:`~httpretty.core.Entry`

        Returns:
            httpretty.Entry: containing the request-matching metadata.
        """
        ...
    @classmethod
    def disable(cls) -> None:
        """
        Disables HTTPretty entirely, putting the original :py:mod:`socket`
        module back in its place.


        .. code::

           import re, json
           import httpretty

           httpretty.enable()
           # request passes through fake socket
           response = requests.get('https://httpbin.org')

           httpretty.disable()
           # request uses real python socket module
           response = requests.get('https://httpbin.org')

        .. note:: This method does not call :py:meth:`httpretty.core.reset` automatically.
        """
        ...
    @classmethod
    def is_enabled(cls) -> bool:
        """
        Check if HTTPretty is enabled

        :returns: bool

        .. testcode::

           import httpretty

           httpretty.enable()
           assert httpretty.is_enabled() == True

           httpretty.disable()
           assert httpretty.is_enabled() == False
        """
        ...
    @classmethod
    def enable(cls, allow_net_connect: bool = True, verbose: bool = False) -> None:
        """
        Enables HTTPretty.

        :param allow_net_connect: boolean to determine if unmatched requests are forwarded to a real network connection OR throw :py:class:`httpretty.errors.UnmockedError`.
        :param verbose: boolean to set HTTPretty's logging level to DEBUG

        .. testcode::

           import re, json
           import httpretty

           httpretty.enable(allow_net_connect=True, verbose=True)

           httpretty.register_uri(
               httpretty.GET,
               re.compile(r'http://.*'),
               body=json.dumps({'man': 'in', 'the': 'middle'})
           )

           response = requests.get('https://foo.bar/foo/bar')

           response.json().should.equal({
               "man": "in",
               "the": "middle",
           })

        .. warning:: after calling this method the original :py:mod:`socket` is replaced with :py:class:`httpretty.core.fakesock`. Make sure to call :py:meth:`~httpretty.disable` after done with your tests or use the :py:class:`httpretty.enabled` as decorator or `context-manager <https://docs.python.org/3/reference/datamodel.html#context-managers>`_
        """
        ...

class httprettized:
    """
    `context-manager <https://docs.python.org/3/reference/datamodel.html#context-managers>`_ for enabling HTTPretty.

    .. tip:: Also available under the alias :py:func:`httpretty.enabled`

    .. testcode::

       import json
       import httpretty

       httpretty.register_uri(httpretty.GET, 'https://httpbin.org/ip', body=json.dumps({'origin': '42.42.42.42'}))
       with httpretty.enabled():
           response = requests.get('https://httpbin.org/ip')

       assert httpretty.latest_requests[-1].url == 'https://httpbin.org/ip'
       assert response.json() == {'origin': '42.42.42.42'}
    """
    allow_net_connect: bool
    verbose: bool
    def __init__(self, allow_net_connect: bool = True, verbose: bool = False) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> None: ...

@overload
def httprettified(test: Callable[_P, _R]) -> Callable[_P, _R]:
    """
    decorator for test functions

    .. tip:: Also available under the alias :py:func:`httpretty.activate`

    :param test: a callable


    example usage with `nosetests <https://nose.readthedocs.io/en/latest/>`_

    .. testcode::

       import sure
       from httpretty import httprettified

       @httprettified
       def test_using_nosetests():
           httpretty.register_uri(
               httpretty.GET,
               'https://httpbin.org/ip'
           )

           response = requests.get('https://httpbin.org/ip')

           response.json().should.equal({
               "message": "HTTPretty :)"
           })

    example usage with `unittest module <https://docs.python.org/3/library/unittest.html>`_

    .. testcode::

       import unittest
       from sure import expect
       from httpretty import httprettified

       @httprettified
       class TestWithPyUnit(unittest.TestCase):
           def test_httpbin(self):
               httpretty.register_uri(httpretty.GET, 'https://httpbin.org/ip')
               response = requests.get('https://httpbin.org/ip')
               expect(response.json()).to.equal({
                   "message": "HTTPretty :)"
               })
    """
    ...
@overload
def httprettified(
    test: None = None, allow_net_connect: bool = True, verbose: bool = False
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
    """
    decorator for test functions

    .. tip:: Also available under the alias :py:func:`httpretty.activate`

    :param test: a callable


    example usage with `nosetests <https://nose.readthedocs.io/en/latest/>`_

    .. testcode::

       import sure
       from httpretty import httprettified

       @httprettified
       def test_using_nosetests():
           httpretty.register_uri(
               httpretty.GET,
               'https://httpbin.org/ip'
           )

           response = requests.get('https://httpbin.org/ip')

           response.json().should.equal({
               "message": "HTTPretty :)"
           })

    example usage with `unittest module <https://docs.python.org/3/library/unittest.html>`_

    .. testcode::

       import unittest
       from sure import expect
       from httpretty import httprettified

       @httprettified
       class TestWithPyUnit(unittest.TestCase):
           def test_httpbin(self):
               httpretty.register_uri(httpretty.GET, 'https://httpbin.org/ip')
               response = requests.get('https://httpbin.org/ip')
               expect(response.json()).to.equal({
                   "message": "HTTPretty :)"
               })
    """
    ...

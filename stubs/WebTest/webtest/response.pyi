import re
from _typeshed.wsgi import WSGIApplication
from collections.abc import Callable, Mapping, Sequence
from typing import Any, Literal, TypeAlias, TypedDict, overload, type_check_only
from typing_extensions import Unpack
from xml.etree import ElementTree

from bs4 import BeautifulSoup
from webob import Response
from webtest.app import TestApp, TestRequest, _Files
from webtest.forms import Form

_Pattern: TypeAlias = str | bytes | re.Pattern[str] | Callable[[str], bool]
# NOTE: These are optional dependencies, so we don't want to depend on them
#       in the stubs either. Also there are no stubs for pyquery anyways.
_PyQuery: TypeAlias = Any
_PyQueryParams: TypeAlias = Any
_LxmlElement: TypeAlias = Any

@type_check_only
class _GetParams(TypedDict, total=False):
    params: Mapping[str, str] | str
    headers: Mapping[str, str]
    extra_environ: Mapping[str, Any]
    status: int | str | None
    expect_errors: bool
    xhr: bool

@type_check_only
class _PostParams(_GetParams, total=False):
    upload_files: _Files
    content_type: str

class TestResponse(Response):
    """
    Instances of this class are returned by
    :class:`~webtest.app.TestApp` methods.
    """
    # NOTE: The way WebTest creates reponses the request is always set
    #       we could've used `MaybeNone`, but it seems more pragmatic
    #       to just assume that this is always set.
    request: TestRequest  # type: ignore[assignment]
    app: WSGIApplication
    test_app: TestApp
    parser_features: str | Sequence[str]
    __test__: Literal[False]
    @property
    def forms(self) -> dict[str | int, Form]:
        """
        Returns a dictionary containing all the forms in the pages as
        :class:`~webtest.forms.Form` objects. Indexes are both in
        order (from zero) and by form id (if the form is given an id).

        See :doc:`forms` for more info on form objects.
        """
        ...
    @property
    def form(self) -> Form:
        """
        If there is only one form on the page, return it as a
        :class:`~webtest.forms.Form` object; raise a TypeError is
        there are no form or multiple forms.
        """
        ...
    @property
    def testbody(self) -> str: ...
    def follow(self, **kw: Unpack[_GetParams]) -> TestResponse:
        """
        If this response is a redirect, follow that redirect.  It is an
        error if it is not a redirect response. Any keyword
        arguments are passed to :class:`webtest.app.TestApp.get`. Returns
        another :class:`TestResponse` object.
        """
        ...
    def maybe_follow(self, **kw: Unpack[_GetParams]) -> TestResponse:
        """
        Follow all redirects. If this response is not a redirect, do nothing.
        Any keyword arguments are passed to :class:`webtest.app.TestApp.get`.
        Returns another :class:`TestResponse` object.
        """
        ...
    def click(
        self,
        description: _Pattern | None = None,
        linkid: _Pattern | None = None,
        href: _Pattern | None = None,
        index: int | None = None,
        verbose: bool = False,
        extra_environ: dict[str, Any] | None = None,
    ) -> TestResponse:
        """
        Click the link as described.  Each of ``description``,
        ``linkid``, and ``url`` are *patterns*, meaning that they are
        either strings (regular expressions), compiled regular
        expressions (objects with a ``search`` method), or callables
        returning true or false.

        All the given patterns are ANDed together:

        * ``description`` is a pattern that matches the contents of the
          anchor (HTML and all -- everything between ``<a...>`` and
          ``</a>``)

        * ``linkid`` is a pattern that matches the ``id`` attribute of
          the anchor.  It will receive the empty string if no id is
          given.

        * ``href`` is a pattern that matches the ``href`` of the anchor;
          the literal content of that attribute, not the fully qualified
          attribute.

        If more than one link matches, then the ``index`` link is
        followed.  If ``index`` is not given and more than one link
        matches, or if no link matches, then ``IndexError`` will be
        raised.

        If you give ``verbose`` then messages will be printed about
        each link, and why it does or doesn't match.  If you use
        ``app.click(verbose=True)`` you'll see a list of all the
        links.

        You can use multiple criteria to essentially assert multiple
        aspects about the link, e.g., where the link's destination is.
        """
        ...
    def clickbutton(
        self,
        description: _Pattern | None = None,
        buttonid: _Pattern | None = None,
        href: _Pattern | None = None,
        onclick: str | None = None,
        index: int | None = None,
        verbose: bool = False,
    ) -> TestResponse:
        """
        Like :meth:`~webtest.response.TestResponse.click`, except looks
        for link-like buttons.
        This kind of button should look like
        ``<button onclick="...location.href='url'...">``.
        """
        ...

    @overload
    def goto(self, href: str, method: Literal["get"] = "get", **args: Unpack[_GetParams]) -> TestResponse:
        """
        Go to the (potentially relative) link ``href``, using the
        given method (``'get'`` or ``'post'``) and any extra arguments
        you want to pass to the :meth:`webtest.app.TestApp.get` or
        :meth:`webtest.app.TestApp.post` methods.

        All hostnames and schemes will be ignored.
        """
        ...
    @overload
    def goto(self, href: str, method: Literal["post"], **args: Unpack[_PostParams]) -> TestResponse:
        """
        Go to the (potentially relative) link ``href``, using the
        given method (``'get'`` or ``'post'``) and any extra arguments
        you want to pass to the :meth:`webtest.app.TestApp.get` or
        :meth:`webtest.app.TestApp.post` methods.

        All hostnames and schemes will be ignored.
        """
        ...

    @property
    def normal_body(self) -> bytes:
        """Return the whitespace-normalized body"""
        ...
    @property
    def unicode_normal_body(self) -> str:
        """Return the whitespace-normalized body, as unicode"""
        ...
    def __contains__(self, s: str) -> bool:
        """
        A response 'contains' a string if it is present in the body
        of the response.  Whitespace is normalized when searching
        for a string.
        """
        ...
    def mustcontain(self, *strings: str, no: Sequence[str] | str = ...) -> None:
        """
        mustcontain(*strings, no=[])

        Assert that the response contains all of the strings passed
        in as arguments.

        Equivalent to::

            assert string in res

        Can take a `no` keyword argument that can be a string or a
        list of strings which must not be present in the response.
        """
        ...
    @property
    def html(self) -> BeautifulSoup:
        """
        Returns the response as a `BeautifulSoup
        <https://www.crummy.com/software/BeautifulSoup/bs3/documentation.html>`_
        object.

        Only works with HTML responses; other content-types raise
        AttributeError.
        """
        ...
    @property
    def xml(self) -> ElementTree.Element:
        """
        Returns the response as an :mod:`ElementTree
        <python:xml.etree.ElementTree>` object.

        Only works with XML responses; other content-types raise
        AttributeError
        """
        ...
    @property
    def lxml(self) -> _LxmlElement:
        """
        Returns the response as an `lxml object <https://lxml.de/>`_.
        You must have lxml installed to use this.

        If this is an HTML response and you have lxml 2.x installed,
        then an ``lxml.html.HTML`` object will be returned; if you
        have an earlier version of lxml then a ``lxml.HTML`` object
        will be returned.
        """
        ...
    @property
    def json(self) -> Any:
        """
        Return the response as a JSON response.
        The content type must be one of json type to use this.
        """
        ...
    @property
    def pyquery(self) -> _PyQuery:
        """
        Returns the response as a `PyQuery
        <https://pypi.org/project/pyquery/>`_ object.

        Only works with HTML and XML responses; other content-types raise
        AttributeError.
        """
        ...
    def PyQuery(self, **kwargs: _PyQueryParams) -> _PyQuery:
        """
        Same as `pyquery` but allow to pass arguments to initialize the
        `PyQuery` instance::

            pq = resp.PyQuery(parser='xml', remove_namespaces=True)
        """
        ...
    def showbrowser(self) -> None:
        """
        Show this response in a browser window (for debugging purposes,
        when it's hard to read the HTML).
        """
        ...
    def __str__(self) -> str: ...  # type: ignore[override]  # noqa: Y029

"""
A **fixture** provides a concept to simplify test support functionality
that needs a setup/cleanup cycle per scenario, feature or test-run.
A fixture is provided as fixture-function that contains the setup part and
cleanup part similar to :func:`contextlib.contextmanager` or `pytest.fixture`_.

.. _pytest.fixture: https://docs.pytest.org/en/latest/fixture.html

A fixture is used when:

* the (registered) fixture tag is used for a scenario or feature
* the :func:`.use_fixture()` is called in the environment file (normally)

.. sourcecode:: python

    # -- FILE: behave4my_project/fixtures.py (or: features/environment.py)
    from behave import fixture
    from somewhere.browser.firefox import FirefoxBrowser

    @fixture
    def browser_firefox(context, timeout=30, **kwargs):
        # -- SETUP-FIXTURE PART:
        context.browser = FirefoxBrowser(timeout, *args, **kwargs)
        yield context.browser
        # -- CLEANUP-FIXTURE PART:
        context.browser.shutdown()

.. sourcecode:: gherkin

    # -- FILE: features/use_fixture.feature
    Feature: Use Fixture in Scenario

        @fixture.browser.firefox
        Scenario: Use browser=firefox
          Given I use the browser
          ...
        # -- AFTER-SCENEARIO: Cleanup fixture.browser.firefox

.. sourcecode:: python

    # -- FILE: features/environment.py
    from behave import use_fixture
    from behave4my_project.fixtures import browser_firefox

    def before_tag(context, tag):
        if tag == "fixture.browser.firefox":
            # -- Performs fixture setup and registers fixture cleanup
            use_fixture(browser_firefox, context, timeout=10)

.. hidden:

    BEHAVIORAL DECISIONS:

    * Should scenario/feature be executed when fixture-setup fails
      (similar to before-hook failures) ?
      NO, scope is skipped, but after-hooks and cleanups are executed.

    * Should remaining fixture-setups be performed after first fixture fails?
      NO, first setup-error aborts the setup and execution of the scope.

    * Should remaining fixture-cleanups be performed when first cleanup-error
      occurs?
      YES, try to perform all fixture-cleanups and then reraise the
      first cleanup-error.


    OPEN ISSUES:

    * AUTO_CALL_REGISTERED_FIXTURE (planned in future):
        Run fixture setup before or after before-hooks?

    IDEAS:

    * Fixture registers itself in fixture registry (runtime context).
    * Code in before_tag() will either be replaced w/ fixture processing function
      or will be automatically be executed (AUTO_CALL_REGISTERED_FIXTURE)
    * Support fixture tags w/ parameters that are automatically parsed and
      passed to fixture function, like:
      @fixture(name="foo", pattern="{name}={browser}")
"""

from _typeshed import Incomplete
from collections.abc import Callable
from typing import Any, Concatenate, ParamSpec, TypeVar

from behave.runner import Context

_T = TypeVar("_T")
_F = TypeVar("_F", bound=Callable[..., Any])
_P = ParamSpec("_P")

def use_fixture(
    fixture_func: Callable[Concatenate[Context, _P], _T], context: Context, *fixture_args: _P.args, **fixture_kwargs: _P.kwargs
) -> _T:
    """
    Use fixture (function) and call it to perform its setup-part.

    The fixture-function is similar to a :func:`contextlib.contextmanager`
    (and contains a yield-statement to separate setup and cleanup part).
    If it contains a yield-statement, it registers a context-cleanup function
    to the context object to perform the fixture-cleanup at the end of the
    current scoped when the context layer is removed
    (and all context-cleanup functions are called).

    Therefore, fixture-cleanup is performed after scenario, feature or test-run
    (depending when its fixture-setup is performed).

    .. code-block:: python

        # -- FILE: behave4my_project/fixtures.py (or: features/environment.py)
        from behave import fixture
        from somewhere.browser import FirefoxBrowser

        @fixture(name="fixture.browser.firefox")
        def browser_firefox(context, *args, **kwargs):
            # -- SETUP-FIXTURE PART:
            context.browser = FirefoxBrowser(*args, **kwargs)
            yield context.browser
            # -- CLEANUP-FIXTURE PART:
            context.browser.shutdown()

    .. code-block:: python

        # -- FILE: features/environment.py
        from behave import use_fixture
        from behave4my_project.fixtures import browser_firefox

        def before_tag(context, tag):
            if tag == "fixture.browser.firefox":
                use_fixture(browser_firefox, context, timeout=10)


    :param fixture_func: Fixture function to use.
    :param context: Context object to use
    :param fixture_kwargs: Positional args, passed to the fixture function.
    :param fixture_kwargs: Additional kwargs, passed to the fixture function.
    :return: Setup result object (may be None).
    """
    ...
def fixture(func: _F | None = None, name: str | None = None, pattern: str | None = None) -> _F:
    """
    Fixture decorator (currently mostly syntactic sugar).

    .. code-block:: python

        # -- FILE: features/environment.py
        # CASE FIXTURE-GENERATOR-FUNCTION (like @contextlib.contextmanager):
        @fixture
        def foo(context, *args, **kwargs):
            the_fixture = setup_fixture_foo(*args, **kwargs)
            context.foo = the_fixture
            yield the_fixture
            cleanup_fixture_foo(the_fixture)

        # CASE FIXTURE-FUNCTION: No cleanup or cleanup via context-cleanup.
        @fixture(name="fixture.bar")
        def bar(context, *args, **kwargs):
            the_fixture = setup_fixture_bar(*args, **kwargs)
            context.bar = the_fixture
            context.add_cleanup(cleanup_fixture_bar, the_fixture.cleanup)
            return the_fixture

    :param name:    Specifies the fixture tag name (as string).

    .. seealso::

        * :func:`contextlib.contextmanager` decorator
        * `@pytest.fixture`_
    """
    ...
def __getattr__(name: str) -> Incomplete: ...

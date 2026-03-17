"""This module provides Runner class to run behave feature files (or model elements)."""

from _typeshed import Incomplete
from collections.abc import Callable
from contextlib import AbstractContextManager
from typing import ClassVar, ParamSpec

_P = ParamSpec("_P")

class Context:
    """
    Hold contextual information during the running of tests.

    This object is a place to store information related to the tests you're
    running. You may add arbitrary attributes to it of whatever value you need.

    During the running of your tests the object will have additional layers of
    namespace added and removed automatically. There is a "root" namespace and
    additional namespaces for features and scenarios.

    Certain names are used by *behave*; be wary of using them yourself as
    *behave* may overwrite the value you set. These names are:

    .. attribute:: feature

      This is set when we start testing a new feature and holds a
      :class:`~behave.model.Feature`. It will not be present outside of a
      feature (i.e. within the scope of the environment before_all and
      after_all).

    .. attribute:: scenario

      This is set when we start testing a new scenario (including the
      individual scenarios of a scenario outline) and holds a
      :class:`~behave.model.Scenario`. It will not be present outside of the
      scope of a scenario.

    .. attribute:: tags

      The current set of active tags (as a Python set containing instances of
      :class:`~behave.model.Tag` which are basically just glorified strings)
      combined from the feature and scenario. This attribute will not be
      present outside of a feature scope.

    .. attribute:: aborted

      This is set to true in the root namespace when the user aborts a test run
      (:exc:`KeyboardInterrupt` exception). Initially: False.

    .. attribute:: failed

      This is set to true in the root namespace as soon as a step fails.
      Initially: False.

    .. attribute:: table

      This is set at the step level and holds any :class:`~behave.model.Table`
      associated with the step.

    .. attribute:: text

      This is set at the step level and holds any multiline text associated
      with the step.

    .. attribute:: config

      The configuration of *behave* as determined by configuration files and
      command-line options. The attributes of this object are the same as the
      `configuration file section names`_.

    .. attribute:: active_outline

      This is set for each scenario in a scenario outline and references the
      :class:`~behave.model.Row` that is active for the current scenario. It is
      present mostly for debugging, but may be useful otherwise.

    .. attribute:: captured

        If any output capture is enabled, provides access to a
        :class:`~behave.capture.Captured` object that contains a snapshot
        of all captured data (stdout/stderr/log).

        .. versionadded:: 1.3.0

    A :class:`behave.runner.ContextMaskWarning` warning will be raised if user
    code attempts to overwrite one of these variables, or if *behave* itself
    tries to overwrite a user-set variable.

    You may use the "in" operator to test whether a certain value has been set
    on the context, for example::

        "feature" in context

    checks whether there is a "feature" value in the context.

    Values may be deleted from the context using "del" but only at the level
    they are set. You can't delete a value set by a feature at a scenario level
    but you can delete a value set for a scenario in that scenario.

    .. _`configuration file section names`: behave.html#configuration-files
    """
    LAYER_NAMES: ClassVar[list[str]]
    FAIL_ON_CLEANUP_ERRORS: ClassVar[bool]

    feature: Incomplete | None
    scenario: Incomplete
    tags: set[str]
    aborted: bool
    failed: bool
    table: Incomplete | None
    text: str | None
    config: Incomplete
    active_outline: Incomplete
    fail_on_cleanup_errors: bool

    def __init__(self, runner) -> None: ...
    def __getattr__(self, name: str) -> Incomplete: ...
    def __setattr__(self, name: str, value) -> None: ...
    def __delattr__(self, name: str) -> None: ...
    def __contains__(self, name: str) -> bool: ...
    def abort(self, reason: str | None = None) -> None:
        """
        Abort the test run.

        This sets the :attr:`aborted` attribute to true.
        Any test runner evaluates this attribute to abort a test run.

        .. versionadded:: 1.2.7
        """
        ...
    def use_or_assign_param(self, name: str, value):
        """
        Use an existing context parameter (aka: attribute) or
        assign a value to new context parameter (if it does not exist yet).

        :param name:   Context parameter name (as string)
        :param value:  Parameter value for new parameter.
        :return: Existing or newly created parameter.

        .. versionadded:: 1.2.7
        """
        ...
    def use_or_create_param(self, name: str, factory_func: Callable[_P, Incomplete], *args: _P.args, **kwargs: _P.kwargs):
        """
        Use an existing context parameter (aka: attribute) or
        create a new parameter if it does not exist yet.

        :param name:   Context parameter name (as string)
        :param factory_func: Factory function, used if parameter is created.
        :param args: Positional args for ``factory_func()`` on create.
        :param kwargs: Named args for ``factory_func()`` on create.
        :return: Existing or newly created parameter.

        .. versionadded:: 1.2.7
        """
        ...
    def use_with_user_mode(self) -> AbstractContextManager[None]:
        """Provides a context manager for using the context in USER mode."""
        ...
    def execute_steps(self, steps_text: str) -> bool:
        """
        The steps identified in the "steps" text string will be parsed and
        executed in turn just as though they were defined in a feature file.

        If the execute_steps call fails (either through error or failure
        assertion) then the step invoking it will need to catch the resulting
        exceptions.

        :param steps_text:  Text with the Gherkin steps to execute (as string).
        :returns: True, if the steps executed successfully.
        :raises: AssertionError, if a step failure occurs.
        :raises: ValueError, if invoked without a feature context.
        """
        ...
    def add_cleanup(self, cleanup_func: Callable[_P, Incomplete], *args: _P.args, **kwargs: _P.kwargs) -> None:
        """
        Adds a cleanup function that is called when :meth:`Context._pop()`
        is called. This is intended for user-cleanups.

        :param cleanup_func:    Callable function
        :param args:            Args for cleanup_func() call (optional).
        :param kwargs:          Kwargs for cleanup_func() call (optional).

        .. note:: RESERVED :obj:`layer` : optional-string

            The keyword argument ``layer="LAYER_NAME"`` can to be used to
            assign the :obj:`cleanup_func` to specific a layer on the context stack
            (instead of the current layer).

            Known layer names are: "testrun", "feature", "rule", "scenario"

        .. seealso:: :attr:`.Context.LAYER_NAMES`
        """
        ...
    @property
    def captured(self): ...
    def attach(self, mime_type: str, data: bytes) -> None:
        """
        Embeds data (e.g. a screenshot) in reports for all
        formatters that support it, such as the JSON formatter.

        :param mime_type:       MIME type of the binary data.
        :param data:            Bytes-like object to embed.
        """
        ...

def __getattr__(name: str) -> Incomplete: ...

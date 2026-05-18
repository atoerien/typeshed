import weakref
from collections.abc import Callable, Iterable, Sequence
from types import FrameType, TracebackType
from typing import Any, ClassVar, Generic, ParamSpec, TypeVar, overload
from typing_extensions import Self, disjoint_base

import greenlet
from gevent._types import _Loop
from gevent._util import readproperty

_T = TypeVar("_T")
_G = TypeVar("_G", bound=greenlet.greenlet)
_P = ParamSpec("_P")

@disjoint_base
class Greenlet(greenlet.greenlet, Generic[_P, _T]):
    """
    Greenlet(run=None, *args, **kwargs)

    A light-weight cooperatively-scheduled execution unit.
    """
    # we can't use _P.args/_P.kwargs here because pyright will complain
    # mypy doesn't seem to mind though
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    value: _T | None

    @overload
    def __init__(
        self: Greenlet[_P, _T],  # pyright: ignore[reportInvalidTypeVarUse]  #11780
        run: Callable[_P, _T],
        *args: _P.args,
        **kwargs: _P.kwargs,
    ) -> None:
        """
        :param args: The arguments passed to the ``run`` function.
        :param kwargs: The keyword arguments passed to the ``run`` function.
        :keyword callable run: The callable object to run. If not given, this object's
            `_run` method will be invoked (typically defined by subclasses).

        .. versionchanged:: 1.1b1
            The ``run`` argument to the constructor is now verified to be a callable
            object. Previously, passing a non-callable object would fail after the greenlet
            was spawned.

        .. versionchanged:: 1.3b1
           The ``GEVENT_TRACK_GREENLET_TREE`` configuration value may be set to
           a false value to disable ``spawn_tree_locals``, ``spawning_greenlet``,
           and ``spawning_stack``. The first two will be None in that case, and the
           latter will be empty.

        .. versionchanged:: 1.5
           Greenlet objects are now more careful to verify that their ``parent`` is really
           a gevent hub, raising a ``TypeError`` earlier instead of an ``AttributeError`` later.

        .. versionchanged:: 20.12.1
           Greenlet objects now function as context managers. Exiting the ``with`` suite
           ensures that the greenlet has completed by :meth:`joining <join>`
           the greenlet (blocking, with
           no timeout). If the body of the suite raises an exception, the greenlet is
           :meth:`killed <kill>` with the default arguments and not joined in that case.
        """
        ...
    @overload
    def __init__(self: Greenlet[[], None]) -> None: ...

    @readproperty
    def name(self) -> str:
        """
        Greenlet.name(self)

        The greenlet name. By default, a unique name is constructed using
        the :attr:`minimal_ident`. You can assign a string to this
        value to change it. It is shown in the `repr` of this object if it
        has been assigned to or if the `minimal_ident` has already been generated.

        .. versionadded:: 1.3a2
        .. versionchanged:: 1.4
           Stop showing generated names in the `repr` when the ``minimal_ident``
           hasn't been requested. This reduces overhead and may be less confusing,
           since ``minimal_ident`` can get reused.
        """
        ...
    @property
    def minimal_ident(self) -> int:
        """
        A small, unique non-negative integer that identifies this object.

        This is similar to :attr:`threading.Thread.ident` (and `id`)
        in that as long as this object is alive, no other greenlet *in
        this hub* will have the same id, but it makes a stronger
        guarantee that the assigned values will be small and
        sequential. Sometime after this object has died, the value
        will be available for reuse.

        To get ids that are unique across all hubs, combine this with
        the hub's (``self.parent``) ``minimal_ident``.

        Accessing this property from threads other than the thread running
        this greenlet is not defined.

        .. versionadded:: 1.3a2
        """
        ...
    @property
    def loop(self) -> _Loop: ...
    @property
    def dead(self) -> bool:
        """
        Boolean indicating that the greenlet is dead and will not run again.

        This is true if:

        1. We were never started, but were :meth:`killed <kill>`
           immediately after creation (not possible with :meth:`spawn`); OR
        2. We were started, but were killed before running; OR
        3. We have run and terminated (by raising an exception out of the
           started function or by reaching the end of the started function).
        """
        ...
    @property
    def started(self) -> bool: ...
    @property
    def exception(self) -> BaseException | None:
        """
        Holds the exception instance raised by the function if the
        greenlet has finished with an error. Otherwise ``None``.
        """
        ...
    @property
    def exc_info(self) -> tuple[type[BaseException], BaseException, TracebackType | None] | None:
        """
        Holds the exc_info three-tuple raised by the function if the
        greenlet finished with an error. Otherwise a false value.

        .. note:: This is a provisional API and may change.

        .. versionadded:: 1.1
        """
        ...
    @staticmethod
    def add_spawn_callback(callback: Callable[[Greenlet[..., Any]], object]) -> None:
        """
        Greenlet.add_spawn_callback(callback)

        add_spawn_callback(callback) -> None

        Set up a *callback* to be invoked when :class:`Greenlet` objects
        are started.

        The invocation order of spawn callbacks is unspecified.  Adding the
        same callback more than one time will not cause it to be called more
        than once.

        .. versionadded:: 1.4.0
        """
        ...
    @staticmethod
    def remove_spawn_callback(callback: Callable[[Greenlet[..., Any]], object]) -> None:
        """
        Greenlet.remove_spawn_callback(callback)

        remove_spawn_callback(callback) -> None

        Remove *callback* function added with :meth:`Greenlet.add_spawn_callback`.
        This function will not fail if *callback* has been already removed or
        if *callback* was never added.

        .. versionadded:: 1.4.0
        """
        ...
    def get(self, block: bool = True, timeout: float | None = None) -> _T:
        """
        Greenlet.get(self, block=True, timeout=None)

        get(block=True, timeout=None) -> object

        Return the result the greenlet has returned or re-raise the
        exception it has raised.

        If block is ``False``, raise :class:`gevent.Timeout` if the
        greenlet is still alive. If block is ``True``, unschedule the
        current greenlet until the result is available or the timeout
        expires. In the latter case, :class:`gevent.Timeout` is
        raised.
        """
        ...
    def has_links(self) -> bool:
        """Greenlet.has_links(self) -> bool"""
        ...
    def join(self, timeout: float | None = None) -> None:
        """
        Greenlet.join(self, timeout=None)

        join(timeout=None) -> None

        Wait until the greenlet finishes or *timeout* expires. Return
        ``None`` regardless.
        """
        ...
    def kill(
        self, exception: type[BaseException] | BaseException = ..., block: bool = True, timeout: float | None = None
    ) -> None: ...
    def link(self, callback: Callable[[Self], object]) -> None: ...
    def link_exception(self, callback: Callable[[Self], object]) -> None: ...
    def link_value(self, callback: Callable[[Self], object]) -> None: ...
    def rawlink(self, callback: Callable[[Self], object]) -> None: ...
    def unlink(self, callback: Callable[[Self], Any]) -> None: ...
    def unlink_all(self) -> None: ...
    def ready(self) -> bool: ...
    def run(self) -> Any: ...

    @overload
    @classmethod
    def spawn(cls, run: Callable[_P, _T], /, *args: _P.args, **kwargs: _P.kwargs) -> Self:
        """
        Greenlet.spawn(cls, *args, **kwargs)

        spawn(function, *args, **kwargs) -> Greenlet

        Create a new :class:`Greenlet` object and schedule it to run ``function(*args, **kwargs)``.
        This can be used as ``gevent.spawn`` or ``Greenlet.spawn``.

        The arguments are passed to :meth:`Greenlet.__init__`.

        .. versionchanged:: 1.1b1
            If a *function* is given that is not callable, immediately raise a :exc:`TypeError`
            instead of spawning a greenlet that will raise an uncaught TypeError.
        """
        ...
    @overload
    @classmethod
    def spawn(cls) -> Greenlet[[], None]: ...

    @overload
    @classmethod
    def spawn_later(cls, seconds: float, run: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs) -> Self:
        """
        Greenlet.spawn_later(cls, seconds, *args, **kwargs)

        spawn_later(seconds, function, *args, **kwargs) -> Greenlet

        Create and return a new `Greenlet` object scheduled to run ``function(*args, **kwargs)``
        in a future loop iteration *seconds* later. This can be used as ``Greenlet.spawn_later``
        or ``gevent.spawn_later``.

        The arguments are passed to :meth:`Greenlet.__init__`.

        .. versionchanged:: 1.1b1
           If an argument that's meant to be a function (the first argument in *args*, or the ``run`` keyword )
           is given to this classmethod (and not a classmethod of a subclass),
           it is verified to be callable. Previously, the spawned greenlet would have failed
           when it started running.
        """
        ...
    @overload
    @classmethod
    def spawn_later(cls, seconds: float) -> Greenlet[[], None]: ...

    def start(self) -> None: ...
    def start_later(self, seconds: float) -> None: ...
    def successful(self) -> bool: ...
    def __bool__(self) -> bool: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, t: type[BaseException] | None, v: BaseException | None, tb: TracebackType | None) -> None: ...

    # since these are for instrumentation which is disabled by default, we could
    # consider just not annotating them...
    spawning_stack_limit: ClassVar[int]
    spawn_tree_locals: dict[str, Any] | None
    spawning_greenlet: weakref.ref[greenlet.greenlet] | None
    # not quite accurate, since it may be an internal dummy type instead
    # but since it has all the same fields as FrameType we shouldn't care
    spawning_stack: FrameType | None

def joinall(
    greenlets: Sequence[_G], timeout: float | None = None, raise_error: bool = False, count: int | None = None
) -> list[_G]:
    """
    joinall(greenlets, timeout=None, raise_error=False, count=None)

    Wait for the ``greenlets`` to finish.

    :param greenlets: A sequence (supporting :func:`len`) of greenlets to wait for.
    :keyword float timeout: If given, the maximum number of seconds to wait.
    :keyword bool raise_error: If True, immediately raise the first exception
        encountered in any greenlet. If False (default), exceptions are
        stored in the greenlet and not raised.
    :keyword int count: If not `None`, then a number specifying the maximum number
        of greenlets to wait for. If ``None`` (the default), all greenlets
        are waited for.
    :return: A sequence of the greenlets that finished before the timeout (if any)
        expired.
    """
    ...
def killall(
    greenlets: Iterable[greenlet.greenlet],
    exception: type[BaseException] | BaseException = ...,
    block: bool = True,
    timeout: float | None = None,
) -> None:
    """
    killall(greenlets, exception=GreenletExit, block=True, timeout=None)

    Forceably terminate all the *greenlets* by causing them to raise *exception*.

    .. caution:: Use care when killing greenlets. If they are not prepared for exceptions,
       this could result in corrupted state.

    :param greenlets: A **bounded** iterable of the non-None greenlets to terminate.
       *All* the items in this iterable must be greenlets that belong to the same hub,
       which should be the hub for this current thread. If this is a generator or iterator
       that switches greenlets, the results are undefined.
    :keyword exception: The type of exception to raise in the greenlets. By default this is
        :class:`GreenletExit`.
    :keyword bool block: If True (the default) then this function only returns when all the
        greenlets are dead; the current greenlet is unscheduled during that process.
        If greenlets ignore the initial exception raised in them,
        then they will be joined (with :func:`gevent.joinall`) and allowed to die naturally.
        If False, this function returns immediately and greenlets will raise
        the exception asynchronously.
    :keyword float timeout: A time in seconds to wait for greenlets to die. If given, it is
        only honored when ``block`` is True.
    :raise Timeout: If blocking and a timeout is given that elapses before
        all the greenlets are dead.

    .. versionchanged:: 1.1a2
        *greenlets* can be any iterable of greenlets, like an iterator or a set.
        Previously it had to be a list or tuple.
    .. versionchanged:: 1.5a3
        Any :class:`Greenlet` in the *greenlets* list that hadn't been switched to before
        calling this method will never be switched to. This makes this function
        behave like :meth:`Greenlet.kill`. This does not apply to raw greenlets.
    .. versionchanged:: 1.5a3
        Now accepts raw greenlets created by :func:`gevent.spawn_raw`.
    """
    ...

__all__ = ["Greenlet", "joinall", "killall"]

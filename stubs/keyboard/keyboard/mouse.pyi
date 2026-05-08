import sys
from collections.abc import Callable, Iterable
from ctypes import c_long
from typing import Literal, SupportsInt, TypeAlias, TypeVar

from ._generic import GenericListener as _GenericListener
from ._mouse_event import (
    DOUBLE as DOUBLE,
    DOWN as DOWN,
    LEFT as LEFT,
    MIDDLE as MIDDLE,
    RIGHT as RIGHT,
    UP as UP,
    X2 as X2,
    ButtonEvent as ButtonEvent,
    MoveEvent as MoveEvent,
    WheelEvent as WheelEvent,
    X as X,
    _MouseButton,
    _MouseEvent,
    _MouseEventType,
)

# mypy doesn't support PEP 646's TypeVarTuple yet: https://github.com/python/mypy/issues/12280
# _Ts = TypeVarTuple("_Ts")
_Ts: TypeAlias = tuple[object, ...]
_Callback: TypeAlias = Callable[[_MouseEvent], bool | None]
_C = TypeVar("_C", bound=_Callback)

class _MouseListener(_GenericListener):
    def init(self) -> None: ...
    def pre_process_event(  # type: ignore[override]  # Mouse specific events and return
        self, event: _MouseEvent
    ) -> Literal[True]: ...
    def listen(self) -> None: ...

def is_pressed(button: _MouseButton = "left") -> bool:
    """Returns True if the given button is currently pressed. """
    ...
def press(button: _MouseButton = "left") -> None:
    """Presses the given button (but doesn't release). """
    ...
def release(button: _MouseButton = "left") -> None:
    """Releases the given button. """
    ...
def click(button: _MouseButton = "left") -> None:
    """Sends a click with the given button. """
    ...
def double_click(button: _MouseButton = "left") -> None:
    """Sends a double click with the given button. """
    ...
def right_click() -> None:
    """Sends a right click with the given button. """
    ...
def wheel(delta: int = 1) -> None:
    """Scrolls the wheel `delta` clicks. Sign indicates direction. """
    ...
def move(x: SupportsInt, y: SupportsInt, absolute: bool = True, duration: float = 0) -> None:
    """
    Moves the mouse. If `absolute`, to position (x, y), otherwise move relative
    to the current position. If `duration` is non-zero, animates the movement.
    """
    ...
def drag(start_x: int, start_y: int, end_x: int, end_y: int, absolute: bool = True, duration: float = 0) -> None:
    """
    Holds the left mouse button, moving from start to end position, then
    releases. `absolute` and `duration` are parameters regarding the mouse
    movement.
    """
    ...
def on_button(
    callback: Callable[..., None],
    args: _Ts = (),
    # Omitting default: Darwin has no x and x2
    buttons: list[_MouseButton] | tuple[_MouseButton, ...] | _MouseButton = ...,
    # Omitting default: Darwin and Linux don't have "double", yet the defaults includes it
    types: list[_MouseEventType] | tuple[_MouseEventType, ...] | _MouseEventType = ...,
) -> _Callback:
    """Invokes `callback` with `args` when the specified event happens. """
    ...
def on_click(callback: Callable[..., None], args: _Ts = ()) -> _Callback:
    """Invokes `callback` with `args` when the left button is clicked. """
    ...
def on_double_click(callback: Callable[..., None], args: _Ts = ()) -> _Callback:
    """Invokes `callback` with `args` when the left button is double clicked."""
    ...
def on_right_click(callback: Callable[..., None], args: _Ts = ()) -> _Callback:
    """Invokes `callback` with `args` when the right button is clicked. """
    ...
def on_middle_click(callback: Callable[..., None], args: _Ts = ()) -> _Callback:
    """Invokes `callback` with `args` when the middle button is clicked. """
    ...
def wait(
    button: _MouseButton = "left",
    # Omitting default: Darwin and Linux don't have "double", yet the defaults includes it
    target_types: tuple[_MouseEventType, ...] = ...,
) -> None:
    """Blocks program execution until the given button performs an event."""
    ...

if sys.platform == "win32":
    def get_position() -> tuple[c_long, c_long]: ...

else:
    def get_position() -> tuple[int, int]:
        """Returns the (x, y) mouse position. """
        ...

def hook(callback: _C) -> _C:
    """
    Installs a global listener on all available mouses, invoking `callback`
    each time it is moved, a key status changes or the wheel is spun. A mouse
    event is passed as argument, with type either `mouse.ButtonEvent`,
    `mouse.WheelEvent` or `mouse.MoveEvent`.

    Returns the given callback for easier development.
    """
    ...
def unhook(callback: _Callback) -> None:
    """Removes a previously installed hook."""
    ...
def unhook_all() -> None:
    """
    Removes all hooks registered by this application. Note this may include
    hooks installed by high level functions, such as `record`.
    """
    ...
def record(button: _MouseButton = "right", target_types: tuple[_MouseEventType] = ("down",)) -> _MouseEvent:
    """
    Records all mouse events until the user presses the given button.
    Then returns the list of events recorded. Pairs well with `play(events)`.

    Note: this is a blocking function.
    Note: for more details on the mouse hook and events see `hook`.
    """
    ...
def play(
    events: Iterable[_MouseEvent],
    speed_factor: float = 1.0,
    include_clicks: bool = True,
    include_moves: bool = True,
    include_wheel: bool = True,
) -> None:
    """
    Plays a sequence of recorded events, maintaining the relative time
    intervals. If speed_factor is <= 0 then the actions are replayed as fast
    as the OS allows. Pairs well with `record()`.

    The parameters `include_*` define if events of that type should be inluded
    in the replay or ignored.
    """
    ...

replay = play
hold = press

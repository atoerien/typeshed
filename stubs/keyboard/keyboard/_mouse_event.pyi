import sys
from typing import Literal, NamedTuple, TypeAlias

_MouseEvent: TypeAlias = ButtonEvent | WheelEvent | MoveEvent  # noqa: Y047  # Used outside

LEFT: Literal["left"]
RIGHT: Literal["right"]
MIDDLE: Literal["middle"]
X: Literal["x"]
X2: Literal["x2"]

UP: Literal["up"]
DOWN: Literal["down"]
DOUBLE: Literal["double"]
WHEEL: Literal["wheel"]

VERTICAL: Literal["vertical"]
HORIZONTAL: Literal["horizontal"]

if sys.platform == "linux" or sys.platform == "win32":
    _MouseButton: TypeAlias = Literal["left", "right", "middle", "x", "x2"]
else:
    _MouseButton: TypeAlias = Literal["left", "right", "middle"]

if sys.platform == "win32":
    _MouseEventType: TypeAlias = Literal["up", "down", "double", "wheel"]
else:
    _MouseEventType: TypeAlias = Literal["up", "down"]

class ButtonEvent(NamedTuple):
    """ButtonEvent(event_type, button, time)"""
    event_type: _MouseEventType
    button: _MouseButton
    time: float

class WheelEvent(NamedTuple):
    """WheelEvent(delta, time)"""
    delta: int
    time: float

class MoveEvent(NamedTuple):
    """MoveEvent(x, y, time)"""
    x: int
    y: int
    time: float

"""
keyboard
========

Take full control of your keyboard with this small Python library. Hook global events, register hotkeys, simulate key presses and much more.

## Features

- **Global event hook** on all keyboards (captures keys regardless of focus).
- **Listen** and **send** keyboard events.
- Works with **Windows** and **Linux** (requires sudo), with experimental **OS X** support (thanks @glitchassassin!).
- **Pure Python**, no C modules to be compiled.
- **Zero dependencies**. Trivial to install and deploy, just copy the files.
- **Python 2 and 3**.
- Complex hotkey support (e.g. `ctrl+shift+m, ctrl+space`) with controllable timeout.
- Includes **high level API** (e.g. [record](#keyboard.record) and [play](#keyboard.play), [add_abbreviation](#keyboard.add_abbreviation)).
- Maps keys as they actually are in your layout, with **full internationalization support** (e.g. `Ctrl+ç`).
- Events automatically captured in separate thread, doesn't block main program.
- Tested and documented.
- Doesn't break accented dead keys (I'm looking at you, pyHook).
- Mouse support available via project [mouse](https://github.com/boppreh/mouse) (`pip install mouse`).

## Usage

Install the [PyPI package](https://pypi.python.org/pypi/keyboard/):

    pip install keyboard

or clone the repository (no installation required, source files are sufficient):

    git clone https://github.com/boppreh/keyboard

or [download and extract the zip](https://github.com/boppreh/keyboard/archive/master.zip) into your project folder.

Then check the [API docs below](https://github.com/boppreh/keyboard#api) to see what features are available.


## Example


```py
import keyboard

keyboard.press_and_release('shift+s, space')

keyboard.write('The quick brown fox jumps over the lazy dog.')

keyboard.add_hotkey('ctrl+shift+a', print, args=('triggered', 'hotkey'))

# Press PAGE UP then PAGE DOWN to type "foobar".
keyboard.add_hotkey('page up, page down', lambda: keyboard.write('foobar'))

# Blocks until you press esc.
keyboard.wait('esc')

# Record events until 'esc' is pressed.
recorded = keyboard.record(until='esc')
# Then replay back at three times the speed.
keyboard.play(recorded, speed_factor=3)

# Type @@ then press space to replace with abbreviation.
keyboard.add_abbreviation('@@', 'my.long.email@example.com')

# Block forever, like `while True`.
keyboard.wait()
```

## Known limitations:

- Events generated under Windows don't report device id (`event.device == None`). [#21](https://github.com/boppreh/keyboard/issues/21)
- Media keys on Linux may appear nameless (scan-code only) or not at all. [#20](https://github.com/boppreh/keyboard/issues/20)
- Key suppression/blocking only available on Windows. [#22](https://github.com/boppreh/keyboard/issues/22)
- To avoid depending on X, the Linux parts reads raw device files (`/dev/input/input*`)
but this requires root.
- Other applications, such as some games, may register hooks that swallow all 
key events. In this case `keyboard` will be unable to report events.
- This program makes no attempt to hide itself, so don't use it for keyloggers or online gaming bots. Be responsible.
"""

from collections.abc import Callable, Generator, Iterable, Sequence
from queue import Queue
from threading import Event as _UninterruptibleEvent
from typing_extensions import TypeAlias

from ._canonical_names import all_modifiers as all_modifiers, sided_modifiers as sided_modifiers
from ._keyboard_event import KEY_DOWN as KEY_DOWN, KEY_UP as KEY_UP, KeyboardEvent as KeyboardEvent

_Key: TypeAlias = int | str
_ScanCodeList: TypeAlias = list[int] | tuple[int, ...]
_ParseableHotkey: TypeAlias = _Key | list[int | _ScanCodeList] | tuple[int | _ScanCodeList, ...]
_Callback: TypeAlias = Callable[[KeyboardEvent], bool | None] | Callable[[], bool | None]
# mypy doesn't support PEP 646's TypeVarTuple yet: https://github.com/python/mypy/issues/12280
# _Ts = TypeVarTuple("_Ts")
_Ts: TypeAlias = tuple[object, ...]

version: str

class _Event(_UninterruptibleEvent):
    def wait(self) -> None: ...  # type: ignore[override]  # Actual implementation

def is_modifier(key: _Key | None) -> bool:
    """Returns True if `key` is a scan code or name of a modifier key."""
    ...
def key_to_scan_codes(key: _ParseableHotkey, error_if_missing: bool = True) -> tuple[int, ...]:
    """Returns a list of scan codes associated with this key (name or scan code)."""
    ...
def parse_hotkey(hotkey: _ParseableHotkey) -> tuple[tuple[tuple[int, ...], ...], ...]:
    """
    Parses a user-provided hotkey into nested tuples representing the
    parsed structure, with the bottom values being lists of scan codes.
    Also accepts raw scan codes, which are then wrapped in the required
    number of nestings.

    Example:

        parse_hotkey("alt+shift+a, alt+b, c")
        #    Keys:    ^~^ ^~~~^ ^  ^~^ ^  ^
        #    Steps:   ^~~~~~~~~~^  ^~~~^  ^

        # ((alt_codes, shift_codes, a_codes), (alt_codes, b_codes), (c_codes,))
    """
    ...
def send(hotkey: _ParseableHotkey, do_press: bool = True, do_release: bool = True) -> None:
    """
    Sends OS events that perform the given *hotkey* hotkey.

    - `hotkey` can be either a scan code (e.g. 57 for space), single key
    (e.g. 'space') or multi-key, multi-step hotkey (e.g. 'alt+F4, enter').
    - `do_press` if true then press events are sent. Defaults to True.
    - `do_release` if true then release events are sent. Defaults to True.

        send(57)
        send('ctrl+alt+del')
        send('alt+F4, enter')
        send('shift+s')

    Note: keys are released in the opposite order they were pressed.
    """
    ...

press_and_release = send

def press(hotkey: _ParseableHotkey) -> None:
    """Presses and holds down a hotkey (see `send`). """
    ...
def release(hotkey: _ParseableHotkey) -> None:
    """Releases a hotkey (see `send`). """
    ...

# is_pressed cannot check multi-step hotkeys, so not using _ParseableHotkey

def is_pressed(hotkey: _Key | _ScanCodeList) -> bool:
    """
    Returns True if the key is pressed.

        is_pressed(57) #-> True
        is_pressed('space') #-> True
        is_pressed('ctrl+space') #-> True
    """
    ...
def call_later(fn: Callable[..., None], args: _Ts = (), delay: float = 0.001) -> None:
    """
    Calls the provided function in a new thread after waiting some time.
    Useful for giving the system some time to process an event, without blocking
    the current execution flow.
    """
    ...
def hook(callback: _Callback, suppress: bool = False, on_remove: Callable[[], None] = ...) -> Callable[[], None]:
    """
    Installs a global listener on all available keyboards, invoking `callback`
    each time a key is pressed or released.

    The event passed to the callback is of type `keyboard.KeyboardEvent`,
    with the following attributes:

    - `name`: an Unicode representation of the character (e.g. "&") or
    description (e.g.  "space"). The name is always lower-case.
    - `scan_code`: number representing the physical key, e.g. 55.
    - `time`: timestamp of the time the event occurred, with as much precision
    as given by the OS.

    Returns the given callback for easier development.
    """
    ...
def on_press(callback: _Callback, suppress: bool = False) -> Callable[[], None]:
    """Invokes `callback` for every KEY_DOWN event. For details see `hook`."""
    ...
def on_release(callback: _Callback, suppress: bool = False) -> Callable[[], None]:
    """Invokes `callback` for every KEY_UP event. For details see `hook`."""
    ...
def hook_key(key: _ParseableHotkey, callback: _Callback, suppress: bool = False) -> Callable[[], None]:
    """
    Hooks key up and key down events for a single key. Returns the event handler
    created. To remove a hooked key use `unhook_key(key)` or
    `unhook_key(handler)`.

    Note: this function shares state with hotkeys, so `clear_all_hotkeys`
    affects it as well.
    """
    ...
def on_press_key(key: _ParseableHotkey, callback: _Callback, suppress: bool = False) -> Callable[[], None]:
    """Invokes `callback` for KEY_DOWN event related to the given key. For details see `hook`."""
    ...
def on_release_key(key: _ParseableHotkey, callback: _Callback, suppress: bool = False) -> Callable[[], None]:
    """Invokes `callback` for KEY_UP event related to the given key. For details see `hook`."""
    ...
def unhook(remove: _Callback) -> None:
    """
    Removes a previously added hook, either by callback or by the return value
    of `hook`.
    """
    ...

unhook_key = unhook

def unhook_all() -> None:
    """
    Removes all keyboard hooks in use, including hotkeys, abbreviations, word
    listeners, `record`ers and `wait`s.
    """
    ...
def block_key(key: _ParseableHotkey) -> Callable[[], None]:
    """Suppresses all key events of the given key, regardless of modifiers."""
    ...

unblock_key = unhook_key

def remap_key(src: _ParseableHotkey, dst: _ParseableHotkey) -> Callable[[], None]:
    """
    Whenever the key `src` is pressed or released, regardless of modifiers,
    press or release the hotkey `dst` instead.
    """
    ...

unremap_key = unhook_key

def parse_hotkey_combinations(hotkey: _ParseableHotkey) -> tuple[tuple[tuple[int, ...], ...], ...]:
    """
    Parses a user-provided hotkey. Differently from `parse_hotkey`,
    instead of each step being a list of the different scan codes for each key,
    each step is a list of all possible combinations of those scan codes.
    """
    ...
def add_hotkey(
    hotkey: _ParseableHotkey,
    callback: Callable[..., bool | None],
    args: _Ts = (),
    suppress: bool = False,
    timeout: float = 1,
    trigger_on_release: bool = False,
) -> Callable[[], None]:
    """
    Invokes a callback every time a hotkey is pressed. The hotkey must
    be in the format `ctrl+shift+a, s`. This would trigger when the user holds
    ctrl, shift and "a" at once, releases, and then presses "s". To represent
    literal commas, pluses, and spaces, use their names ('comma', 'plus',
    'space').

    - `args` is an optional list of arguments to passed to the callback during
    each invocation.
    - `suppress` defines if successful triggers should block the keys from being
    sent to other programs.
    - `timeout` is the amount of seconds allowed to pass between key presses.
    - `trigger_on_release` if true, the callback is invoked on key release instead
    of key press.

    The event handler function is returned. To remove a hotkey call
    `remove_hotkey(hotkey)` or `remove_hotkey(handler)`.
    before the hotkey state is reset.

    Note: hotkeys are activated when the last key is *pressed*, not released.
    Note: the callback is executed in a separate thread, asynchronously. For an
    example of how to use a callback synchronously, see `wait`.

    Examples:

        # Different but equivalent ways to listen for a spacebar key press.
        add_hotkey(' ', print, args=['space was pressed'])
        add_hotkey('space', print, args=['space was pressed'])
        add_hotkey('Space', print, args=['space was pressed'])
        # Here 57 represents the keyboard code for spacebar; so you will be
        # pressing 'spacebar', not '57' to activate the print function.
        add_hotkey(57, print, args=['space was pressed'])

        add_hotkey('ctrl+q', quit)
        add_hotkey('ctrl+alt+enter, space', some_callback)
    """
    ...

register_hotkey = add_hotkey

def remove_hotkey(hotkey_or_callback: _ParseableHotkey | _Callback) -> None:
    """
    Removes a previously hooked hotkey. Must be called with the value returned
    by `add_hotkey`.
    """
    ...

unregister_hotkey = remove_hotkey
clear_hotkey = remove_hotkey

def unhook_all_hotkeys() -> None:
    """
    Removes all keyboard hotkeys in use, including abbreviations, word listeners,
    `record`ers and `wait`s.
    """
    ...

unregister_all_hotkeys = unhook_all_hotkeys
remove_all_hotkeys = unhook_all_hotkeys
clear_all_hotkeys = unhook_all_hotkeys

def remap_hotkey(
    src: _ParseableHotkey, dst: _ParseableHotkey, suppress: bool = True, trigger_on_release: bool = False
) -> Callable[[], None]:
    """
    Whenever the hotkey `src` is pressed, suppress it and send
    `dst` instead.

    Example:

        remap('alt+w', 'ctrl+up')
    """
    ...

unremap_hotkey = remove_hotkey

def stash_state() -> list[int]: ...
def restore_state(scan_codes: Iterable[int]) -> None: ...
def restore_modifiers(scan_codes: Iterable[int]) -> None: ...
def write(text: str, delay: float = 0, restore_state_after: bool = True, exact: bool | None = None) -> None: ...
def wait(hotkey: _ParseableHotkey | None = None, suppress: bool = False, trigger_on_release: bool = False) -> None: ...
def get_hotkey_name(names: Iterable[str] | None = None) -> str: ...
def read_event(suppress: bool = False) -> KeyboardEvent: ...
def read_key(suppress: bool = False) -> _Key: ...
def read_hotkey(suppress: bool = True) -> str: ...
def get_typed_strings(events: Iterable[KeyboardEvent], allow_backspace: bool = True) -> Generator[str]: ...
def start_recording(
    recorded_events_queue: Queue[KeyboardEvent] | None = None,
) -> tuple[Queue[KeyboardEvent], Callable[[], None]]:
    """
    Starts recording all keyboard events into a global variable, or the given
    queue if any. Returns the queue of events and the hooked function.

    Use `stop_recording()` or `unhook(hooked_function)` to stop.
    """
    ...
def stop_recording() -> list[KeyboardEvent]:
    """
    Stops the global recording of events and returns a list of the events
    captured.
    """
    ...
def record(until: str = "escape", suppress: bool = False, trigger_on_release: bool = False) -> list[KeyboardEvent]:
    """
    Records all keyboard events from all keyboards until the user presses the
    given hotkey. Then returns the list of events recorded, of type
    `keyboard.KeyboardEvent`. Pairs well with
    `play(events)`.

    Note: this is a blocking function.
    Note: for more details on the keyboard hook and events see `hook`.
    """
    ...
def play(events: Iterable[KeyboardEvent], speed_factor: float = 1.0) -> None:
    """
    Plays a sequence of recorded events, maintaining the relative time
    intervals. If speed_factor is <= 0 then the actions are replayed as fast
    as the OS allows. Pairs well with `record()`.

    Note: the current keyboard state is cleared at the beginning and restored at
    the end of the function.
    """
    ...

replay = play

def add_word_listener(
    word: str, callback: _Callback, triggers: Sequence[str] = ["space"], match_suffix: bool = False, timeout: float = 2
) -> Callable[[], None]:
    """
    Invokes a callback every time a sequence of characters is typed (e.g. 'pet')
    and followed by a trigger key (e.g. space). Modifiers (e.g. alt, ctrl,
    shift) are ignored.

    - `word` the typed text to be matched. E.g. 'pet'.
    - `callback` is an argument-less function to be invoked each time the word
    is typed.
    - `triggers` is the list of keys that will cause a match to be checked. If
    the user presses some key that is not a character (len>1) and not in
    triggers, the characters so far will be discarded. By default the trigger
    is only `space`.
    - `match_suffix` defines if endings of words should also be checked instead
    of only whole words. E.g. if true, typing 'carpet'+space will trigger the
    listener for 'pet'. Defaults to false, only whole words are checked.
    - `timeout` is the maximum number of seconds between typed characters before
    the current word is discarded. Defaults to 2 seconds.

    Returns the event handler created. To remove a word listener use
    `remove_word_listener(word)` or `remove_word_listener(handler)`.

    Note: all actions are performed on key down. Key up events are ignored.
    Note: word matches are **case sensitive**.
    """
    ...
def remove_word_listener(word_or_handler: str | _Callback) -> None:
    """
    Removes a previously registered word listener. Accepts either the word used
    during registration (exact string) or the event handler returned by the
    `add_word_listener` or `add_abbreviation` functions.
    """
    ...
def add_abbreviation(
    source_text: str, replacement_text: str, match_suffix: bool = False, timeout: float = 2
) -> Callable[[], None]:
    """
    Registers a hotkey that replaces one typed text with another. For example

        add_abbreviation('tm', u'™')

    Replaces every "tm" followed by a space with a ™ symbol (and no space). The
    replacement is done by sending backspace events.

    - `match_suffix` defines if endings of words should also be checked instead
    of only whole words. E.g. if true, typing 'carpet'+space will trigger the
    listener for 'pet'. Defaults to false, only whole words are checked.
    - `timeout` is the maximum number of seconds between typed characters before
    the current word is discarded. Defaults to 2 seconds.

    For more details see `add_word_listener`.
    """
    ...

register_word_listener = add_word_listener
register_abbreviation = add_abbreviation
remove_abbreviation = remove_word_listener

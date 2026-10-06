"""Public API for tf._api.v2.autograph namespace"""

from collections.abc import Callable
from typing import Any, TypeVar

from tensorflow.autograph.experimental import Feature

_Type = TypeVar("_Type")

def set_verbosity(level: int, alsologtostdout: bool = False) -> None:
    """
    Sets the AutoGraph verbosity level.

    _Debug logging in AutoGraph_

    More verbose logging is useful to enable when filing bug reports or doing
    more in-depth debugging.

    There are two means to control the logging verbosity:

     * The `set_verbosity` function

     * The `AUTOGRAPH_VERBOSITY` environment variable

    `set_verbosity` takes precedence over the environment variable.

    For example:

    ```python
    import os
    import tensorflow as tf

    os.environ['AUTOGRAPH_VERBOSITY'] = '5'
    # Verbosity is now 5

    tf.autograph.set_verbosity(0)
    # Verbosity is now 0

    os.environ['AUTOGRAPH_VERBOSITY'] = '1'
    # No effect, because set_verbosity was already called.
    ```

    Logs entries are output to [absl](https://abseil.io)'s
    [default output](https://abseil.io/docs/python/guides/logging),
    with `INFO` level.
    Logs can be mirrored to stdout by using the `alsologtostdout` argument.
    Mirroring is enabled by default when Python runs in interactive mode.

    Args:
      level: int, the verbosity level; larger values specify increased verbosity;
        0 means no logging. When reporting bugs, it is recommended to set this
        value to a larger number, like 10.
      alsologtostdout: bool, whether to also output log messages to `sys.stdout`.
    """
    ...
def to_code(
    entity: Callable[..., Any],
    recursive: bool = True,
    experimental_optional_features: Feature | tuple[Feature, ...] | None = None,
) -> str: ...
def to_graph(
    entity: _Type, recursive: bool = True, experimental_optional_features: Feature | tuple[Feature, ...] | None = None
) -> _Type: ...
def trace(*args: Any) -> None: ...

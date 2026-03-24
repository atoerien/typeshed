"""
Implements signals based on blinker if available, otherwise
falls silently back to a noop. Shamelessly stolen from flask.signals:
https://github.com/mitsuhiko/flask/blob/master/flask/signals.py
"""

from _typeshed import Incomplete

signals_available: bool

class Namespace:
    def signal(self, name: str, doc: str | None = None) -> _FakeSignal: ...

class _FakeSignal:
    """
    If blinker is unavailable, create a fake class with the same
    interface that allows sending of signals but will fail with an
    error on anything else.  Instead of doing anything on send, it
    will just ignore the arguments and do nothing instead.
    """
    name: str
    __doc__: str | None
    def __init__(self, name: str, doc: str | None = None) -> None: ...
    send: Incomplete
    connect: Incomplete
    disconnect: Incomplete
    has_receivers_for: Incomplete
    receivers_for: Incomplete
    temporarily_connected_to: Incomplete
    connected_to: Incomplete

scope_changed: _FakeSignal

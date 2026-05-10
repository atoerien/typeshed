from collections.abc import Callable
from logging import Logger
from typing import Literal, TypeAlias

from .amqp_object import AMQPObject

AMQPValue: TypeAlias = type[AMQPObject] | AMQPObject | int | str

LOGGER: Logger

def name_or_value(value: AMQPValue) -> str: ...
def sanitize_prefix(function): ...
def check_for_prefix_and_key(function): ...

class CallbackManager:
    """
    CallbackManager is a global callback system designed to be a single place
    where Pika can manage callbacks and process them. It should be referenced
    by the CallbackManager.instance() method instead of constructing new
    instances of it.
    """
    CALLS: str
    ARGUMENTS: str
    DUPLICATE_WARNING: str
    CALLBACK: str
    ONE_SHOT: str
    ONLY_CALLER: str
    def __init__(self) -> None:
        """Create an instance of the CallbackManager"""
        ...
    def add(
        self,
        prefix: str | int,
        key: AMQPValue,
        # Parameter type must match arguments passed to process()
        callback: Callable[..., object],
        one_shot: bool = True,
        only_caller: object | None = None,
        arguments=None,
    ) -> tuple[str | int, str | object]: ...
    def clear(self) -> None: ...
    def cleanup(self, prefix: str | int) -> bool: ...
    def pending(self, prefix: str | int, key: str | object) -> int | None: ...
    def process(self, prefix: str | int, key: AMQPValue, caller, *args, **keywords) -> bool: ...
    def remove(
        self, prefix: str | int, key: AMQPValue, callback_value: Callable[..., object] | None = None, arguments=None
    ) -> Literal[True]: ...
    def remove_all(self, prefix: str | int, key: AMQPValue) -> None: ...

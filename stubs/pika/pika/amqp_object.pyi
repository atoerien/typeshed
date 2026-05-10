"""
Base classes that are extended by low level AMQP frames and higher level
AMQP classes and methods.
"""

from typing import ClassVar

class AMQPObject:
    """
    Base object that is extended by AMQP low level frames and AMQP classes
    and methods.
    """
    NAME: ClassVar[str]
    INDEX: ClassVar[int | None]
    def __eq__(self, other: AMQPObject | None) -> bool: ...  # type: ignore[override]

class Class(AMQPObject):
    """Is extended by AMQP classes"""
    ...

class Method(AMQPObject):
    """Is extended by AMQP methods"""
    # This is a class attribute in the implementation, but subclasses use @property,
    # so it's more convenient to use that here as well.
    @property
    def synchronous(self) -> bool: ...
    def get_properties(self) -> Properties: ...
    def get_body(self) -> bytes: ...
    def encode(self) -> list[bytes]: ...
    def decode(self, encoded: bytes, offset: int = 0) -> Method: ...

        :rtype: pika.frame.Properties
        """
        ...
    def get_body(self) -> str:
        """
        Return the message body if it is set.

        :rtype: str|unicode
        """
        ...

class Properties(AMQPObject):
    """Class to encompass message properties (AMQP Basic.Properties)"""
    ...

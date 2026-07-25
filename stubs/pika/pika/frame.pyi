"""Frame objects that do the frame demarshaling and marshaling."""

from abc import abstractmethod
from logging import Logger
from typing import Generic, TypeVar

from . import amqp_object
from .spec import BasicProperties

_M = TypeVar("_M", bound=amqp_object.Method)

LOGGER: Logger

class Frame(amqp_object.AMQPObject):
    frame_type: int
    channel_number: int
    def __init__(self, frame_type: int, channel_number: int) -> None:
        """
        Create a new instance of a frame

        :param int frame_type: The frame type
        :param int channel_number: The channel number for the frame
        """
        ...
    @abstractmethod
    def marshal(self) -> bytes:
        """
        To be ended by child classes

        :raises NotImplementedError
        """
        ...

class Method(Frame, Generic[_M]):
    """
    Base Method frame object mapping. AMQP method frames are mapped on top
    of this class for creating or accessing their data and attributes.
    """
    method: _M
    def __init__(self, channel_number: int, method: _M) -> None:
        """
        Create a new instance of a frame

        :param int channel_number: The frame type
        :param pika.Spec.Class.Method method: The AMQP Class.Method
        """
        ...
    def marshal(self) -> bytes:
        """
        Return the AMQP binary encoded value of the frame

        :rtype: bytes
        """
        ...

class Header(Frame):
    """
    Header frame object mapping. AMQP content header frames are mapped
    on top of this class for creating or accessing their data and attributes.
    """
    body_size: int
    properties: BasicProperties
    def __init__(self, channel_number: int, body_size: int, props: BasicProperties) -> None:
        """
        Create a new instance of a AMQP ContentHeader object

        :param int channel_number: The channel number for the frame
        :param int body_size: The number of bytes for the body
        :param pika.spec.BasicProperties props: Basic.Properties object
        """
        ...
    def marshal(self) -> bytes:
        """
        Return the AMQP binary encoded value of the frame

        :rtype: bytes
        """
        ...

class Body(Frame):
    """
    Body frame object mapping class. AMQP content body frames are mapped on
    to this base class for getting/setting of attributes/data.
    """
    fragment: bytes
    def __init__(self, channel_number: int, fragment: bytes) -> None:
        """
        Parameters:

        - channel_number: int
        - fragment: bytes
        """
        ...
    def marshal(self) -> bytes:
        """
        Return the AMQP binary encoded value of the frame

        :rtype: bytes
        """
        ...

class Heartbeat(Frame):
    """
    Heartbeat frame object mapping class. AMQP Heartbeat frames are mapped
    on to this class for a common access structure to the attributes/data
    values.
    """
    def __init__(self) -> None:
        """Create a new instance of the Heartbeat frame"""
        ...
    def marshal(self) -> bytes:
        """
        Return the AMQP binary encoded value of the frame

        :rtype: bytes
        """
        ...

class ProtocolHeader(amqp_object.AMQPObject):
    frame_type: int
    major: int
    minor: int
    revision: int
    def __init__(self, major: int | None = None, minor: int | None = None, revision: int | None = None) -> None:
        """
        Construct a Protocol Header frame object for the specified AMQP
        version

def decode_frame(data_in: bytes) -> tuple[int, Frame | ProtocolHeader | None]: ...

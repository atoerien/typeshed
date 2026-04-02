"""
Provides a factory class for generating dynamic messages.

The easiest way to use this class is if you have access to the FileDescriptor
protos containing the messages you want to create you can just do the following:

message_classes = message_factory.GetMessages(iterable_of_file_descriptors)
my_proto_instance = message_classes['some.proto.package.MessageName']()
"""

from collections.abc import Iterable

from google.protobuf.descriptor import Descriptor
from google.protobuf.descriptor_pb2 import FileDescriptorProto
from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.message import Message

def GetMessageClass(descriptor: Descriptor) -> type[Message]: ...
def GetMessageClassesForFiles(files: Iterable[str], pool: DescriptorPool) -> dict[str, type[Message]]: ...

class MessageFactory:
    pool: DescriptorPool
    def __init__(self, pool: DescriptorPool | None = None) -> None: ...

def GetMessages(file_protos: Iterable[FileDescriptorProto], pool: DescriptorPool | None = None) -> dict[str, type[Message]]: ...

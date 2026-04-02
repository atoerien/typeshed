"""
Builds descriptors, message classes and services for generated _pb2.py.

This file is only called in python generated _pb2.py files. It builds
descriptors, message classes and services that users can directly use
in generated code.
"""

from types import ModuleType
from typing import Any

from google.protobuf.descriptor import FileDescriptor

def BuildMessageAndEnumDescriptors(file_des: FileDescriptor, module: dict[str, Any]) -> None:
    """
    Builds message and enum descriptors.

    Args:
      file_des: FileDescriptor of the .proto file
      module: Generated _pb2 module
    """
    ...
def BuildTopDescriptorsAndMessages(file_des: FileDescriptor, module_name: str, module: dict[str, Any]) -> None:
    """
    Builds top level descriptors and message classes.

    Args:
      file_des: FileDescriptor of the .proto file
      module_name: str, the name of generated _pb2 module
      module: Generated _pb2 module
    """
    ...
def AddHelpersToExtensions(file_des: FileDescriptor) -> None:
    """
    no-op to keep old generated code work with new runtime.

    Args:
      file_des: FileDescriptor of the .proto file
    """
    ...
def BuildServices(file_des: FileDescriptor, module_name: str, module: ModuleType) -> None:
    """
    Builds services classes and services stub class.

    Args:
      file_des: FileDescriptor of the .proto file
      module_name: str, the name of generated _pb2 module
      module: Generated _pb2 module
    """
    ...

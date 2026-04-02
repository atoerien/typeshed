"""
Contains metaclasses used to create protocol service and service stub
classes from ServiceDescriptor objects at runtime.

The GeneratedServiceType and GeneratedServiceStubType metaclasses are used to
inject all useful functionality into the classes output by the protocol
compiler at compile-time.
"""

from typing import Any

class GeneratedServiceType(type):
    """
    Metaclass for service classes created at runtime from ServiceDescriptors.

    Implementations for all methods described in the Service class are added here
    by this class. We also create properties to allow getting/setting all fields
    in the protocol message.

    The protocol compiler currently uses this metaclass to create protocol service
    classes at runtime. Clients can also manually create their own classes at
    runtime, as in this example::

      mydescriptor = ServiceDescriptor(.....)
      class MyProtoService(service.Service):
        __metaclass__ = GeneratedServiceType
        DESCRIPTOR = mydescriptor
      myservice_instance = MyProtoService()
      # ...
    """
    def __init__(cls, name: str, bases: tuple[type, ...], dictionary: dict[str, Any]) -> None:
        """
        Creates a message service class.

        Args:
          name: Name of the class (ignored, but required by the metaclass
            protocol).
          bases: Base classes of the class being constructed.
          dictionary: The class dictionary of the class being constructed.
            dictionary[_DESCRIPTOR_KEY] must contain a ServiceDescriptor object
            describing this protocol service type.
        """
        ...

class GeneratedServiceStubType(GeneratedServiceType):
    """
    Metaclass for service stubs created at runtime from ServiceDescriptors.

    This class has similar responsibilities as GeneratedServiceType, except that
    it creates the service stub classes.
    """
    def __init__(cls, name: str, bases: tuple[type, ...], dictionary: dict[str, Any]) -> None:
        """
        Creates a message service stub class.

        Args:
          name: Name of the class (ignored, here).
          bases: Base classes of the class being constructed.
          dictionary: The class dictionary of the class being constructed.
            dictionary[_DESCRIPTOR_KEY] must contain a ServiceDescriptor object
            describing this protocol service type.
        """
        ...

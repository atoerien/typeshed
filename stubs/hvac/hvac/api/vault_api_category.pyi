"""Base class used by all hvac api "category" classes."""

from abc import ABCMeta, abstractmethod
from logging import Logger
from typing import Any

from hvac.adapters import Adapter
from hvac.api.vault_api_base import VaultApiBase

logger: Logger

class VaultApiCategory(VaultApiBase, metaclass=ABCMeta):
    """Base class for API categories."""
    implemented_class_names: list[str]
    def __init__(self, adapter: Adapter[Any]) -> None: ...
    def __getattr__(self, item): ...

    @property
    def adapter(self) -> Adapter[Any]:
        """
        Retrieve the adapter instance under the "_adapter" property in use by this class.

        :return: The adapter instance in use by this class.
        :rtype: hvac.adapters.Adapter
        """
        ...
    @adapter.setter
    def adapter(self, adapter: Adapter[Any]) -> None: ...

    @property
    @abstractmethod
    def implemented_classes(self):
        """
        List of implemented classes under this category.

        :return: List of implemented classes under this category.
        :rtype: List[hvac.api.VaultApiBase]
        """
        ...
    @property
    def unimplemented_classes(self) -> list[str]:
        """
        List of known unimplemented classes under this category.

        :return: List of known unimplemented classes under this category.
        :rtype: List[str]
        """
        ...
    @staticmethod
    def get_private_attr_name(class_name):
        """
        Helper method to prepend a leading underscore to a provided class name.

        :param class_name: Name of a class under this category.
        :type class_name: str|unicode
        :return: The private attribute label for the provided class.
        :rtype: str
        """
        ...

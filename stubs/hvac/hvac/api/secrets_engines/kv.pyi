"""Kv secret backend methods module."""

import logging

from hvac.api.vault_api_base import VaultApiBase

logger: logging.Logger

class Kv(VaultApiBase):
    """
    Class containing methods for the key/value secrets_engines backend API routes.
    Reference: https://www.vaultproject.io/docs/secrets/kv/index.html
    """
    allowed_kv_versions: list[str]
    def __init__(self, adapter, default_kv_version: str = "2") -> None:
        """
        Create a new Kv instance.

        :param adapter: Instance of :py:class:`hvac.adapters.Adapter`; used for performing HTTP requests.
        :type adapter: hvac.adapters.Adapter
        :param default_kv_version: KV version number (e.g., '1') to use as the default when accessing attributes/methods
            under this class.
        :type default_kv_version: str | unicode
        """
        ...
    @property
    def v1(self):
        """
        Accessor for kv version 1 class / method. Provided via the :py:class:`hvac.api.secrets_engines.kv_v1.KvV1` class.

        :return: This Kv instance's associated KvV1 instance.
        :rtype: hvac.api.secrets_engines.kv_v1.KvV1
        """
        ...
    @property
    def v2(self): ...

    @property
    def default_kv_version(self): ...
    @default_kv_version.setter
    def default_kv_version(self, default_kv_version) -> None: ...

    def __getattr__(self, item): ...

from typing import Any

from hvac.api.vault_api_base import VaultApiBase

DEFAULT_MOUNT_POINT: str

class KvV1(VaultApiBase):
    """
    KV Secrets Engine - Version 1 (API).

    Reference: https://www.vaultproject.io/api/secrets/kv/kv-v1.html
    """
    def read_secret(self, path: str, mount_point: str = "secret"):
        """
        Retrieve the secret at the specified location.

        Supported methods:
            GET: /{mount_point}/{path}. Produces: 200 application/json


        :param path: Specifies the path of the secret to read. This is specified as part of the URL.
        :type path: str | unicode
        :param mount_point: The "path" the secret engine was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the read_secret request.
        :rtype: dict
        """
        ...
    def list_secrets(self, path: str, mount_point: str = "secret"):
        """
        Return a list of key names at the specified location.

        Folders are suffixed with /. The input must be a folder; list on a file will not return a value. Note that no
        policy-based filtering is performed on keys; do not encode sensitive information in key names. The values
        themselves are not accessible via this command.

        Supported methods:
            LIST: /{mount_point}/{path}. Produces: 200 application/json

        :param path: Specifies the path of the secrets to list.
            This is specified as part of the URL.
        :type path: str | unicode
        :param mount_point: The "path" the secret engine was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the list_secrets request.
        :rtype: dict
        """
        ...
    def create_or_update_secret(
        self, path: str, secret: dict[str, Any], method: str | None = None, mount_point: str = "secret"
    ): ...
    def delete_secret(self, path: str, mount_point: str = "secret"): ...

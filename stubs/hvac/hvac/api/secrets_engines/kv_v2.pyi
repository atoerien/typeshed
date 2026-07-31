from typing import Any

from hvac.api.vault_api_base import VaultApiBase

DEFAULT_MOUNT_POINT: str

class KvV2(VaultApiBase):
    """
    KV Secrets Engine - Version 2 (API).

    Reference: https://www.vaultproject.io/api/secret/kv/kv-v2.html
    """
    def configure(
        self,
        max_versions: int = 10,
        cas_required: bool | None = None,
        delete_version_after: str = "0s",
        mount_point: str = "secret",
    ):
        """
        Configure backend level settings that are applied to every key in the key-value store.

        Supported methods:
            POST: /{mount_point}/config. Produces: 204 (empty body)


        :param max_versions: The number of versions to keep per key. This value applies to all keys, but a key's
            metadata setting can overwrite this value. Once a key has more than the configured allowed versions the
            oldest version will be permanently deleted. Defaults to 10.
        :type max_versions: int
        :param cas_required: If true all keys will require the cas parameter to be set on all write requests.
        :type cas_required: bool
        :param mount_point: The "path" the secret engine was mounted on.
        :type mount_point: str | unicode
        :param delete_version_after: Specifies the length of time before a version is deleted. Accepts Go duration format string.
            Defaults to "0s" (i.e., disabled).
        :type delete_version_after: str
        :return: The response of the request.
        :rtype: requests.Response
        """
        ...
    def read_configuration(self, mount_point: str = "secret"):
        """
        Read the KV Version 2 configuration.

        Supported methods:
            GET: /auth/{mount_point}/config. Produces: 200 application/json


        :param mount_point: The "path" the secret engine was mounted on.
        :type mount_point: str | unicode
        :return: The JSON response of the request.
        :rtype: dict
        """
        ...
    def read_secret(self, path: str, mount_point: str = "secret", raise_on_deleted_version: bool | None = None):
        """
        Retrieve the secret at the specified location.

        Equivalent to calling read_secret_version with version=None.

        Supported methods:
            GET: /{mount_point}/data/{path}. Produces: 200 application/json


        :param path: Specifies the path of the secret to read. This is specified as part of the URL.
        :type path: str | unicode
        :param mount_point: The "path" the secret engine was mounted on.
        :type mount_point: str | unicode
        :param raise_on_deleted_version: Changes the behavior when the requested version is deleted.
            If True an exception will be raised.
            If False, some metadata about the deleted secret is returned.
            If None (pre-v3), a default of True will be used and a warning will be issued.
        :type raise_on_deleted_version: bool
        :return: The JSON response of the request.
        :rtype: dict
        """
        ...
    def read_secret_version(
        self, path: str, version: int | None = None, mount_point: str = "secret", raise_on_deleted_version: bool | None = None
    ): ...
    def create_or_update_secret(self, path: str, secret: dict[str, Any], cas: int | None = None, mount_point: str = "secret"): ...
    def patch(self, path: str, secret: dict[str, str], mount_point: str = "secret"): ...
    def delete_latest_version_of_secret(self, path: str, mount_point: str = "secret"): ...
    def delete_secret_versions(self, path: str, versions: list[int], mount_point: str = "secret"): ...
    def undelete_secret_versions(self, path: str, versions: list[int], mount_point: str = "secret"): ...
    def destroy_secret_versions(self, path: str, versions: list[int], mount_point: str = "secret"): ...
    def list_secrets(self, path: str, mount_point: str = "secret"): ...
    def read_secret_metadata(self, path: str, mount_point: str = "secret"): ...
    def update_metadata(
        self,
        path: str,
        max_versions: int | None = None,
        cas_required: bool | None = None,
        delete_version_after: str = "0s",
        mount_point: str = "secret",
        custom_metadata: dict[str, str] | None = None,
    ):
        """
        Updates the max_versions of cas_required setting on an existing path.

        Supported methods:
            POST: /{mount_point}/metadata/{path}. Produces: 204 (empty body)


        :param path: Path
        :type path: str | unicode
        :param max_versions: The number of versions to keep per key. If not set, the backend's configured max version is
            used. Once a key has more than the configured allowed versions the oldest version will be permanently
            deleted.
        :type max_versions: int
        :param cas_required: If true the key will require the cas parameter to be set on all write requests. If false,
            the backend's configuration will be used.
        :type cas_required: bool
        :param delete_version_after: Specifies the length of time before a version is deleted. Accepts Go duration format string.
            Defaults to "0s" (i.e., disabled).
        :type delete_version_after: str
        :param mount_point: The "path" the secret engine was mounted on.
        :type mount_point: str | unicode
        :param custom_metadata: A dictionary of key/value metadata to describe the secret. Requires Vault 1.9.0 or greater.
        :type custom_metadata: dict
        :return: The response of the request.
        :rtype: requests.Response
        """
        ...
    def delete_metadata_and_all_versions(self, path: str, mount_point: str = "secret"):
        """
        Delete (permanently) the key metadata and all version data for the specified key.

        All version history will be removed.

        Supported methods:
            DELETE: /{mount_point}/metadata/{path}. Produces: 204 (empty body)


        :param path: Specifies the path of the secret to delete. This is specified as part of the URL.
        :type path: str | unicode
        :param mount_point: The "path" the secret engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the request.
        :rtype: requests.Response
        """
        ...

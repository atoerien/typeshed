import logging
from typing import Any

log: logging.Logger

class ImageApiMixin:
    def get_image(self, image: str, chunk_size: int | None = 2097152):
        """
        Get a tarball of an image. Similar to the ``docker save`` command.

        Args:
            image (str): Image name to get
            chunk_size (int): The number of bytes returned by each iteration
                of the generator. If ``None``, data will be streamed as it is
                received. Default: 2 MB

        Returns:
            (generator): A stream of raw archive data.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.

        Example:

            >>> image = client.api.get_image("busybox:latest")
            >>> f = open('/tmp/busybox-latest.tar', 'wb')
            >>> for chunk in image:
            >>>   f.write(chunk)
            >>> f.close()
        """
        ...
    def history(self, image):
        """
        Show the history of an image.

        Args:
            image (str): The image to show history for

        Returns:
            (list): The history of the image

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def images(self, name: str | None = None, quiet: bool = False, all: bool = False, filters=None):
        """
        List images. Similar to the ``docker images`` command.

        Args:
            name (str): Only show images belonging to the repository ``name``
            quiet (bool): Only return numeric IDs as a list.
            all (bool): Show intermediate image layers. By default, these are
                filtered out.
            filters (dict): Filters to be processed on the image list.
                Available filters:
                - ``dangling`` (bool)
                - `label` (str|list): format either ``"key"``, ``"key=value"``
                    or a list of such.

        Returns:
            (dict or list): A list if ``quiet=True``, otherwise a dict.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def import_image(
        self,
        src=None,
        repository: str | None = None,
        tag: str | None = None,
        image: str | None = None,
        changes=None,
        stream_src: bool = False,
    ):
        """
        Import an image. Similar to the ``docker import`` command.

        If ``src`` is a string or unicode string, it will first be treated as a
        path to a tarball on the local system. If there is an error reading
        from that file, ``src`` will be treated as a URL instead to fetch the
        image from. You can also pass an open file handle as ``src``, in which
        case the data will be read from that file.

        If ``src`` is unset but ``image`` is set, the ``image`` parameter will
        be taken as the name of an existing image to import from.

        Args:
            src (str or file): Path to tarfile, URL, or file-like object
            repository (str): The repository to create
            tag (str): The tag to apply
            image (str): Use another image like the ``FROM`` Dockerfile
                parameter
        """
        ...
    def import_image_from_data(self, data, repository: str | None = None, tag: str | None = None, changes=None):
        """
        Like :py:meth:`~docker.api.image.ImageApiMixin.import_image`, but
        allows importing in-memory bytes data.

        Args:
            data (bytes collection): Bytes collection containing valid tar data
            repository (str): The repository to create
            tag (str): The tag to apply
        """
        ...
    def import_image_from_file(self, filename: str, repository: str | None = None, tag: str | None = None, changes=None):
        """
        Like :py:meth:`~docker.api.image.ImageApiMixin.import_image`, but only
        supports importing from a tar file on disk.

        Args:
            filename (str): Full path to a tar file.
            repository (str): The repository to create
            tag (str): The tag to apply

        Raises:
            IOError: File does not exist.
        """
        ...
    def import_image_from_stream(self, stream, repository: str | None = None, tag: str | None = None, changes=None): ...
    def import_image_from_url(self, url, repository: str | None = None, tag: str | None = None, changes=None):
        """
        Like :py:meth:`~docker.api.image.ImageApiMixin.import_image`, but only
        supports importing from a URL.

        Args:
            url (str): A URL pointing to a tar file.
            repository (str): The repository to create
            tag (str): The tag to apply
        """
        ...
    def import_image_from_image(self, image, repository: str | None = None, tag: str | None = None, changes=None):
        """
        Like :py:meth:`~docker.api.image.ImageApiMixin.import_image`, but only
        supports importing from another image, like the ``FROM`` Dockerfile
        parameter.

        Args:
            image (str): Image name to import from
            repository (str): The repository to create
            tag (str): The tag to apply
        """
        ...
    def inspect_image(self, image):
        """
        Get detailed information about an image. Similar to the ``docker
        inspect`` command, but only for images.

        Args:
            image (str): The image to inspect

        Returns:
            (dict): Similar to the output of ``docker inspect``, but as a
        single dict

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def inspect_distribution(self, image, auth_config=None):
        """
        Get image digest and platform information by contacting the registry.

        Args:
            image (str): The image name to inspect
            auth_config (dict): Override the credentials that are found in the
                config for this request.  ``auth_config`` should contain the
                ``username`` and ``password`` keys to be valid.

        Returns:
            (dict): A dict containing distribution data

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def load_image(self, data, quiet=None):
        """
        Load an image that was previously saved using
        :py:meth:`~docker.api.image.ImageApiMixin.get_image` (or ``docker
        save``). Similar to ``docker load``.

        Args:
            data (binary): Image data to be loaded.
            quiet (boolean): Suppress progress details in response.

        Returns:
            (generator): Progress output as JSON objects. Only available for
                         API version >= 1.23

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def prune_images(self, filters=None):
        """
        Delete unused images

        Args:
            filters (dict): Filters to process on the prune list.
                Available filters:
                - dangling (bool):  When set to true (or 1), prune only
                unused and untagged images.

        Returns:
            (dict): A dict containing a list of deleted image IDs and
                the amount of disk space reclaimed in bytes.

        Raises:
            :py:class:`docker.errors.APIError`
                If the server returns an error.
        """
        ...
    def pull(
        self,
        repository: str,
        tag: str | None = None,
        stream: bool = False,
        auth_config: dict[str, Any] | None = None,
        decode: bool = False,
        platform: str | None = None,
        all_tags: bool = False,
    ): ...
    def push(self, repository: str, tag: str | None = None, stream: bool = False, auth_config=None, decode: bool = False): ...
    def remove_image(self, image: str, force: bool = False, noprune: bool = False): ...
    def search(self, term: str, limit: int | None = None): ...
    def tag(self, image, repository, tag: str | None = None, force: bool = False) -> bool: ...

def is_file(src: str) -> bool: ...

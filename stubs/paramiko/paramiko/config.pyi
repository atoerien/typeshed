"""Configuration file (aka ``ssh_config``) support."""

from _typeshed import FileDescriptorOrPath
from collections.abc import Iterable
from re import Pattern
from typing_extensions import Self

from paramiko.ssh_exception import ConfigParseError as ConfigParseError, CouldNotCanonicalize as CouldNotCanonicalize

invoke_import_error: ImportError | None
SSH_PORT: int

class SSHConfig:
    """
    Representation of config information as stored in the format used by
    OpenSSH. Queries can be made via `lookup`. The format is described in
    OpenSSH's ``ssh_config`` man page. This class is provided primarily as a
    convenience to posix users (since the OpenSSH format is a de-facto
    standard on posix) but should work fine on Windows too.

    .. versionadded:: 1.6
    """
    SETTINGS_REGEX: Pattern[str]
    TOKENS_BY_CONFIG_KEY: dict[str, list[str]]
    def __init__(self) -> None:
        r"""
        Create a new OpenSSH config object.

        Note: the newer alternate constructors `from_path`, `from_file` and
        `from_text` are simpler to use, as they parse on instantiation. For
        example, instead of::

            config = SSHConfig()
            config.parse(open("some-path.config")

        you could::

            config = SSHConfig.from_file(open("some-path.config"))
            # Or more directly:
            config = SSHConfig.from_path("some-path.config")
            # Or if you have arbitrary ssh_config text from some other source:
            config = SSHConfig.from_text("Host foo\n\tUser bar")
        """
        ...
    @classmethod
    def from_text(cls, text: str) -> Self:
        """
        Create a new, parsed `SSHConfig` from ``text`` string.

        .. versionadded:: 2.7
        """
        ...
    @classmethod
    def from_path(cls, path: FileDescriptorOrPath) -> Self:
        """
        Create a new, parsed `SSHConfig` from the file found at ``path``.

        .. versionadded:: 2.7
        """
        ...
    @classmethod
    def from_file(cls, flo: Iterable[str]) -> Self: ...
    def parse(self, file_obj: Iterable[str]) -> None: ...
    def lookup(self, hostname: str) -> SSHConfigDict: ...
    def canonicalize(self, hostname: str, options: SSHConfigDict, domains: Iterable[str]) -> str: ...
    def get_hostnames(self) -> set[str]: ...

class LazyFqdn:
    """Returns the host's fqdn on request as string."""
    fqdn: str | None
    config: SSHConfig
    host: str | None
    def __init__(self, config: SSHConfigDict, host: str | None = None) -> None: ...

class SSHConfigDict(dict[str, str]):
    """
    A dictionary wrapper/subclass for per-host configuration structures.

    This class introduces some usage niceties for consumers of `SSHConfig`,
    specifically around the issue of variable type conversions: normal value
    access yields strings, but there are now methods such as `as_bool` and
    `as_int` that yield casted values instead.

    For example, given the following ``ssh_config`` file snippet::

        Host foo.example.com
            PasswordAuthentication no
            Compression yes
            ServerAliveInterval 60

    the following code highlights how you can access the raw strings as well as
    usefully Python type-casted versions (recalling that keys are all
    normalized to lowercase first)::

        my_config = SSHConfig()
        my_config.parse(open('~/.ssh/config'))
        conf = my_config.lookup('foo.example.com')

        assert conf['passwordauthentication'] == 'no'
        assert conf.as_bool('passwordauthentication') is False
        assert conf['compression'] == 'yes'
        assert conf.as_bool('compression') is True
        assert conf['serveraliveinterval'] == '60'
        assert conf.as_int('serveraliveinterval') == 60

    .. versionadded:: 2.5
    """
    def as_bool(self, key: str) -> bool:
        """
        Express given key's value as a boolean type.

        Typically, this is used for ``ssh_config``'s pseudo-boolean values
        which are either ``"yes"`` or ``"no"``. In such cases, ``"yes"`` yields
        ``True`` and any other value becomes ``False``.

        .. note::
            If (for whatever reason) the stored value is already boolean in
            nature, it's simply returned.

        .. versionadded:: 2.5
        """
        ...
    def as_int(self, key: str) -> int:
        """
        Express given key's value as an integer, if possible.

        This method will raise ``ValueError`` or similar if the value is not
        int-appropriate, same as the builtin `int` type.

        .. versionadded:: 2.5
        """
        ...

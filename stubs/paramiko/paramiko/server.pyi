"""`.ServerInterface` is an interface to override for server support."""

import threading

from paramiko.channel import Channel
from paramiko.message import Message
from paramiko.pkey import PKey
from paramiko.transport import Transport

class ServerInterface:
    def check_channel_request(self, kind: str, chanid: int) -> int: ...
    def get_allowed_auths(self, username: str) -> str: ...
    def check_auth_none(self, username: str) -> int: ...
    def check_auth_password(self, username: str, password: str) -> int: ...
    def check_auth_publickey(self, username: str, key: PKey) -> int: ...
    def check_auth_interactive(self, username: str, submethods: str) -> int | InteractiveQuery: ...
    def check_auth_interactive_response(self, responses: list[str]) -> int | InteractiveQuery: ...
    def check_port_forward_request(self, address: str, port: int) -> int: ...
    def cancel_port_forward_request(self, address: str, port: int) -> None: ...
    def check_global_request(self, kind: str, msg: Message) -> bool | tuple[bool | int | str, ...]: ...
    def check_channel_pty_request(
        self, channel: Channel, term: bytes, width: int, height: int, pixelwidth: int, pixelheight: int, modes: bytes
    ) -> bool:
        """
        Determine if a pseudo-terminal of the given dimensions (usually
        requested for shell access) can be provided on the given channel.

        The default implementation always returns ``False``.

        :param .Channel channel: the `.Channel` the pty request arrived on.
        :param str term: type of terminal requested (for example, ``"vt100"``).
        :param int width: width of screen in characters.
        :param int height: height of screen in characters.
        :param int pixelwidth:
            width of screen in pixels, if known (may be ``0`` if unknown).
        :param int pixelheight:
            height of screen in pixels, if known (may be ``0`` if unknown).
        :return:
            ``True`` if the pseudo-terminal has been allocated; ``False``
            otherwise.
        """
        ...
    def check_channel_shell_request(self, channel: Channel) -> bool:
        """
        Determine if a shell will be provided to the client on the given
        channel.  If this method returns ``True``, the channel should be
        connected to the stdin/stdout of a shell (or something that acts like
        a shell).

        The default implementation always returns ``False``.

        :param .Channel channel: the `.Channel` the request arrived on.
        :return:
            ``True`` if this channel is now hooked up to a shell; ``False`` if
            a shell can't or won't be provided.
        """
        ...
    def check_channel_exec_request(self, channel: Channel, command: bytes) -> bool:
        """
        Determine if a shell command will be executed for the client.  If this
        method returns ``True``, the channel should be connected to the stdin,
        stdout, and stderr of the shell command.

        The default implementation always returns ``False``.

        :param .Channel channel: the `.Channel` the request arrived on.
        :param str command: the command to execute.
        :return:
            ``True`` if this channel is now hooked up to the stdin, stdout, and
            stderr of the executing command; ``False`` if the command will not
            be executed.

        .. versionadded:: 1.1
        """
        ...
    def check_channel_subsystem_request(self, channel: Channel, name: str) -> bool:
        """
        Determine if a requested subsystem will be provided to the client on
        the given channel.  If this method returns ``True``, all future I/O
        through this channel will be assumed to be connected to the requested
        subsystem.  An example of a subsystem is ``sftp``.

        The default implementation checks for a subsystem handler assigned via
        `.Transport.set_subsystem_handler`.
        If one has been set, the handler is invoked and this method returns
        ``True``.  Otherwise it returns ``False``.

        .. note:: Because the default implementation uses the `.Transport` to
            identify valid subsystems, you probably won't need to override this
            method.

        :param .Channel channel: the `.Channel` the pty request arrived on.
        :param str name: name of the requested subsystem.
        :return:
            ``True`` if this channel is now hooked up to the requested
            subsystem; ``False`` if that subsystem can't or won't be provided.
        """
        ...
    def check_channel_window_change_request(
        self, channel: Channel, width: int, height: int, pixelwidth: int, pixelheight: int
    ) -> bool:
        """
        Determine if the pseudo-terminal on the given channel can be resized.
        This only makes sense if a pty was previously allocated on it.

        The default implementation always returns ``False``.

        :param .Channel channel: the `.Channel` the pty request arrived on.
        :param int width: width of screen in characters.
        :param int height: height of screen in characters.
        :param int pixelwidth:
            width of screen in pixels, if known (may be ``0`` if unknown).
        :param int pixelheight:
            height of screen in pixels, if known (may be ``0`` if unknown).
        :return: ``True`` if the terminal was resized; ``False`` if not.
        """
        ...
    def check_channel_x11_request(
        self, channel: Channel, single_connection: bool, auth_protocol: str, auth_cookie: bytes, screen_number: int
    ) -> bool:
        """
        Determine if the client will be provided with an X11 session.  If this
        method returns ``True``, X11 applications should be routed through new
        SSH channels, using `.Transport.open_x11_channel`.

        The default implementation always returns ``False``.

        :param .Channel channel: the `.Channel` the X11 request arrived on
        :param bool single_connection:
            ``True`` if only a single X11 channel should be opened, else
            ``False``.
        :param str auth_protocol: the protocol used for X11 authentication
        :param str auth_cookie: the cookie used to authenticate to X11
        :param int screen_number: the number of the X11 screen to connect to
        :return: ``True`` if the X11 session was opened; ``False`` if not
        """
        ...
    def check_channel_forward_agent_request(self, channel: Channel) -> bool:
        """
        Determine if the client will be provided with an forward agent session.
        If this method returns ``True``, the server will allow SSH Agent
        forwarding.

        The default implementation always returns ``False``.

        :param .Channel channel: the `.Channel` the request arrived on
        :return: ``True`` if the AgentForward was loaded; ``False`` if not

        If ``True`` is returned, the server should create an
        :class:`AgentServerProxy` to access the agent.
        """
        ...
    def check_channel_direct_tcpip_request(self, chanid: int, origin: tuple[str, int], destination: tuple[str, int]) -> int:
        """
        Determine if a local port forwarding channel will be granted, and
        return ``OPEN_SUCCEEDED`` or an error code.  This method is
        called in server mode when the client requests a channel, after
        authentication is complete.

        The ``chanid`` parameter is a small number that uniquely identifies the
        channel within a `.Transport`.  A `.Channel` object is not created
        unless this method returns ``OPEN_SUCCEEDED`` -- once a
        `.Channel` object is created, you can call `.Channel.get_id` to
        retrieve the channel ID.

        The origin and destination parameters are (ip_address, port) tuples
        that correspond to both ends of the TCP connection in the forwarding
        tunnel.

        The return value should either be ``OPEN_SUCCEEDED`` (or
        ``0``) to allow the channel request, or one of the following error
        codes to reject it:

            - ``OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED``
            - ``OPEN_FAILED_CONNECT_FAILED``
            - ``OPEN_FAILED_UNKNOWN_CHANNEL_TYPE``
            - ``OPEN_FAILED_RESOURCE_SHORTAGE``

        The default implementation always returns
        ``OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED``.

        :param int chanid: ID of the channel
        :param tuple origin:
            2-tuple containing the IP address and port of the originator
            (client side)
        :param tuple destination:
            2-tuple containing the IP address and port of the destination
            (server side)
        :return: an `int` success or failure code (listed above)
        """
        ...
    def check_channel_env_request(self, channel: Channel, name: bytes, value: bytes) -> bool:
        """
        Check whether a given environment variable can be specified for the
        given channel.  This method should return ``True`` if the server
        is willing to set the specified environment variable.  Note that
        some environment variables (e.g., PATH) can be exceedingly
        dangerous, so blindly allowing the client to set the environment
        is almost certainly not a good idea.

        The default implementation always returns ``False``.

        :param channel: the `.Channel` the env request arrived on
        :param str name: name
        :param str value: Channel value
        :returns: A boolean
        """
        ...
    def get_banner(self) -> tuple[str | None, str | None]:
        """
        A pre-login banner to display to the user. The message may span
        multiple lines separated by crlf pairs. The language should be in
        rfc3066 style, for example: en-US

        The default implementation always returns ``(None, None)``.

        :returns: A tuple containing the banner and language code.

        .. versionadded:: 2.3
        """
        ...

class InteractiveQuery:
    """A query (set of prompts) for a user during interactive authentication."""
    name: str
    instructions: str
    prompts: list[tuple[str, bool]]
    def __init__(self, name: str = "", instructions: str = "", *prompts: str | tuple[str, bool]) -> None:
        """
        Create a new interactive query to send to the client.  The name and
        instructions are optional, but are generally displayed to the end
        user.  A list of prompts may be included, or they may be added via
        the `add_prompt` method.

        :param str name: name of this query
        :param str instructions:
            user instructions (usually short) about this query
        :param str prompts: one or more authentication prompts
        """
        ...
    def add_prompt(self, prompt: str, echo: bool = True) -> None:
        """
        Add a prompt to this query.  The prompt should be a (reasonably short)
        string.  Multiple prompts can be added to the same query.

        :param str prompt: the user prompt
        :param bool echo:
            ``True`` (default) if the user's response should be echoed;
            ``False`` if not (for a password or similar)
        """
        ...

class SubsystemHandler(threading.Thread):
    """
    Handler for a subsystem in server mode.  If you create a subclass of this
    class and pass it to `.Transport.set_subsystem_handler`, an object of this
    class will be created for each request for this subsystem.  Each new object
    will be executed within its own new thread by calling `start_subsystem`.
    When that method completes, the channel is closed.

    For example, if you made a subclass ``MP3Handler`` and registered it as the
    handler for subsystem ``"mp3"``, then whenever a client has successfully
    authenticated and requests subsystem ``"mp3"``, an object of class
    ``MP3Handler`` will be created, and `start_subsystem` will be called on
    it from a new thread.
    """
    def __init__(self, channel: Channel, name: str, server: ServerInterface) -> None:
        """
        Create a new handler for a channel.  This is used by `.ServerInterface`
        to start up a new handler when a channel requests this subsystem.  You
        don't need to override this method, but if you do, be sure to pass the
        ``channel`` and ``name`` parameters through to the original
        ``__init__`` method here.

        :param .Channel channel: the channel associated with this
            subsystem request.
        :param str name: name of the requested subsystem.
        :param .ServerInterface server:
            the server object for the session that started this subsystem
        """
        ...
    def get_server(self) -> ServerInterface:
        """
        Return the `.ServerInterface` object associated with this channel and
        subsystem.
        """
        ...
    def start_subsystem(self, name: str, transport: Transport, channel: Channel) -> None:
        """
        Process an ssh subsystem in server mode.  This method is called on a
        new object (and in a new thread) for each subsystem request.  It is
        assumed that all subsystem logic will take place here, and when the
        subsystem is finished, this method will return.  After this method
        returns, the channel is closed.

        The combination of ``transport`` and ``channel`` are unique; this
        handler corresponds to exactly one `.Channel` on one `.Transport`.

        .. note::
            It is the responsibility of this method to exit if the underlying
            `.Transport` is closed.  This can be done by checking
            `.Transport.is_active` or noticing an EOF on the `.Channel`.  If
            this method loops forever without checking for this case, your
            Python interpreter may refuse to exit because this thread will
            still be running.

        :param str name: name of the requested subsystem.
        :param .Transport transport: the server-mode `.Transport`.
        :param .Channel channel: the channel associated with this subsystem
            request.
        """
        ...
    def finish_subsystem(self) -> None:
        """
        Perform any cleanup at the end of a subsystem.  The default
        implementation just closes the channel.

        .. versionadded:: 1.1
        """
        ...

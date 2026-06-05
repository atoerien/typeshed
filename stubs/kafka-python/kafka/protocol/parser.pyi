from _typeshed import Incomplete
from collections import deque
from logging import Logger

log: Logger

class KafkaProtocol:
    """
    Manage the kafka network protocol

    Use an instance of KafkaProtocol to manage bytes send/recv'd
    from a network socket to a broker.

    Arguments:
        client_id (str): identifier string to be included in each request
        api_version (tuple): Optional tuple to specify api_version to use.
            Currently only used to check for 0.8.2 protocol quirks, but
            may be used for more in the future.
        max_frame_size (int): Maximum allowed message frame size.
            Default: 100000000 (100MB).
    """
    in_flight_requests: deque[tuple[int, Incomplete]]
    bytes_to_send: list[bytes]
    def __init__(
        self, client_id: str | None = None, api_version: tuple[int, int, int] | None = None, max_frame_size: int = 100000000
    ) -> None: ...
    def send_request(self, request, correlation_id: int | None = None) -> int:
        """
        Encode and queue a kafka api request for sending.

        Arguments:
            request (object): An un-encoded kafka request.
            correlation_id (int, optional): Optionally specify an ID to
                correlate requests with responses. If not provided, an ID will
                be generated automatically.

        Returns:
            correlation_id
        """
        ...
    def send_bytes(self) -> bytes:
        """Retrieve all pending bytes to send on the network"""
        ...
    def receive_bytes(self, data: bytes) -> list[Incomplete]:
        """
        Process bytes received from the network.

        Arguments:
            data (bytes): any length bytes received from a network connection
                to a kafka broker.

        Returns:
            responses (list of (correlation_id, response)): any/all completed
                responses, decoded from bytes to python objects.

        Raises:
             KafkaProtocolError: if the bytes received could not be decoded.
             CorrelationIdError: if the response does not match the request
                 correlation id.
        """
        ...

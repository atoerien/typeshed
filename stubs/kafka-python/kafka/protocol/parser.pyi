from _typeshed import Incomplete
from collections import deque

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
    def __init__(self, *, client_id: str = ..., ident: str = "", receive_message_max_bytes: int = 100000000) -> None: ...
    def send_request(self, request, correlation_id: int | None = None) -> int: ...
    def send_bytes(self) -> bytes: ...
    def receive_bytes(self, data: bytes) -> list[tuple[Incomplete, Incomplete]]: ...

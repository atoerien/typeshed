from _typeshed import Incomplete

log: Incomplete

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
    """
    in_flight_requests: Incomplete
    bytes_to_send: Incomplete
    def __init__(self, client_id=None, api_version=None) -> None: ...
    def send_request(self, request, correlation_id=None):
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
    def send_bytes(self):
        """Retrieve all pending bytes to send on the network"""
        ...
    def receive_bytes(self, data):
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

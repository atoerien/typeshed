from _typeshed import Incomplete

from kafka.sasl.abc import SaslMechanism

log: Incomplete

class SaslMechanismAwsMskIam(SaslMechanism):
    host: Incomplete
    def __init__(self, **config) -> None: ...
    def auth_bytes(self): ...
    def receive(self, auth_bytes) -> None: ...
    def is_done(self): ...
    def is_authenticated(self): ...
    def auth_details(self): ...

class AwsMskIamClient:
    UNRESERVED_CHARS: Incomplete
    algorithm: str
    expires: str
    hashfunc: Incomplete
    headers: Incomplete
    version: str
    service: str
    action: Incomplete
    datestamp: Incomplete
    timestamp: Incomplete
    host: Incomplete
    access_key: Incomplete
    secret_key: Incomplete
    region: Incomplete
    token: Incomplete
    def __init__(self, host, access_key, secret_key, region, token=None) -> None:
        """
        Arguments:
            host (str): The hostname of the broker.
            access_key (str): An AWS_ACCESS_KEY_ID.
            secret_key (str): An AWS_SECRET_ACCESS_KEY.
            region (str): An AWS_REGION.
            token (Optional[str]): An AWS_SESSION_TOKEN if using temporary
                credentials.
        """
        ...
    def first_message(self):
        """
        Returns (bytes):
            An encoded JSON authentication payload that can be sent to the
            broker.
        """
        ...

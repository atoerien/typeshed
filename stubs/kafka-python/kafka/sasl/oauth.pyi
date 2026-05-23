import abc
from _typeshed import Incomplete

from kafka.sasl.abc import SaslMechanism

log: Incomplete

class SaslMechanismOAuth(SaslMechanism):
    token_provider: Incomplete
    def __init__(self, **config) -> None: ...
    def auth_bytes(self): ...
    def receive(self, auth_bytes) -> None: ...
    def is_done(self): ...
    def is_authenticated(self): ...
    def auth_details(self): ...

ABC: Incomplete

class AbstractTokenProvider(ABC, metaclass=abc.ABCMeta):
    """
    A Token Provider must be used for the SASL OAuthBearer protocol.

    The implementation should ensure token reuse so that multiple
    calls at connect time do not create multiple tokens. The implementation
    should also periodically refresh the token in order to guarantee
    that each call returns an unexpired token. A timeout error should
    be returned after a short period of inactivity so that the
    broker can log debugging info and retry.

    Token Providers MUST implement the token() method
    """
    def __init__(self, **config) -> None: ...
    @abc.abstractmethod
    def token(self):
        """
        Returns a (str) ID/Access Token to be sent to the Kafka
        client.
        """
        ...
    def extensions(self):
        """
        This is an OPTIONAL method that may be implemented.

        Returns a map of key-value pairs that can
        be sent with the SASL/OAUTHBEARER initial client request. If
        not implemented, the values are ignored. This feature is only available
        in Kafka >= 2.1.0.

        All returned keys and values should be type str
        """
        ...

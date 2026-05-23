import logging

from kafka.admin import KafkaAdminClient as KafkaAdminClient
from kafka.client_async import KafkaClient as KafkaClient
from kafka.conn import BrokerConnection as BrokerConnection
from kafka.consumer import KafkaConsumer as KafkaConsumer
from kafka.consumer.subscription_state import ConsumerRebalanceListener as ConsumerRebalanceListener
from kafka.producer import KafkaProducer as KafkaProducer

__all__ = ["BrokerConnection", "ConsumerRebalanceListener", "KafkaAdminClient", "KafkaClient", "KafkaConsumer", "KafkaProducer"]

class NullHandler(logging.Handler):
    """
    This handler does nothing. It's intended to be used to avoid the
    "No handlers could be found for logger XXX" one-off warning. This is
    important for library code, which may contain code to log events. If a user
    of the library does not configure logging, the one-off warning might be
    produced; to avoid this, the library developer simply needs to instantiate
    a NullHandler and add it to the top-level logger of the library module or
    package.
    """
    def emit(self, record) -> None:
        """Stub."""
        ...

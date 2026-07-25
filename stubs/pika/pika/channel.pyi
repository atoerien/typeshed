"""
The Channel class provides a wrapper for interacting with RabbitMQ
implementing the methods and behaviors for an AMQP Channel.
"""

from _typeshed import Incomplete
from collections.abc import Callable, Iterable, Mapping
from logging import Logger
from typing import Final, TypeVar
from typing_extensions import Self

from . import amqp_object
from .callback import CallbackManager
from .connection import Connection
from .exchange_type import ExchangeType
from .frame import Body, Header, Method
from .spec import Basic, BasicProperties, Confirm, Exchange, Queue, Tx

_Method = TypeVar("_Method", bound=amqp_object.Method)

LOGGER: Logger
MAX_CHANNELS: Final = 65535

class Channel:
    """
    A Channel is the primary communication method for interacting with
    RabbitMQ. It is recommended that you do not directly invoke the creation of
    a channel object in your application code but rather construct a channel by
    calling the active connection's channel() method.
    """
    CLOSED: Final = 0
    OPENING: Final = 1
    OPEN: Final = 2
    CLOSING: Final = 3

    channel_number: int
    callbacks: CallbackManager
    connection: Connection
    flow_active: bool

    def __init__(self, connection: Connection, channel_number: int, on_open_callback: Callable[[Self], object]) -> None: ...
    def __int__(self) -> int: ...
    def add_callback(self, callback: Callable[..., object], replies: Iterable[Incomplete], one_shot: bool = True) -> None: ...
    def add_on_cancel_callback(self, callback: Callable[[Method[Basic.Cancel]], object]) -> None: ...
    def add_on_close_callback(self, callback: Callable[[Channel, Exception], object]) -> None: ...
    def add_on_flow_callback(self, callback: Callable[[bool], object]) -> None: ...
    def add_on_return_callback(self, callback: Callable[[Channel, Basic.Return, BasicProperties, bytes], object]) -> None: ...
    def basic_ack(self, delivery_tag: int = 0, multiple: bool = False) -> None: ...
    def basic_cancel(
        self, consumer_tag: str = "", callback: Callable[[Method[Basic.CancelOk]], object] | None = None
    ) -> None:
        """
        This method cancels a consumer. This does not affect already
        delivered messages, but it does mean the server will not send any more
        messages for that consumer. The client may receive an arbitrary number
        of messages in between sending the cancel method and receiving the
        cancel-ok reply. It may also be sent from the server to the client in
        the event of the consumer being unexpectedly cancelled (i.e. cancelled
        for any reason other than the server receiving the corresponding
        basic.cancel from the client). This allows clients to be notified of
        the loss of consumers due to events such as queue deletion.

        :param str consumer_tag: Identifier for the consumer
        :param callable callback: callback(pika.frame.Method) for method
            Basic.CancelOk. If None, do not expect a Basic.CancelOk response,
            otherwise, callback must be callable

        :raises ValueError:
        """
        ...
    def basic_consume(
        self,
        queue: str,
        on_message_callback: Callable[[Channel, Basic.Deliver, BasicProperties, bytes], object],
        auto_ack: bool = False,
        exclusive: bool = False,
        consumer_tag: str | None = None,
        arguments: Mapping[str, Incomplete] | None = None,
        callback: Callable[[Method[Basic.ConsumeOk]], object] | None = None,
    ) -> str:
        """
        Sends the AMQP 0-9-1 command Basic.Consume to the broker and binds messages
        for the consumer_tag to the consumer callback. If you do not pass in
        a consumer_tag, one will be automatically generated for you. Returns
        the consumer tag.

        For more information on basic_consume, see:
        Tutorial 2 at https://www.rabbitmq.com/getstarted.html
        https://www.rabbitmq.com/confirms.html
        https://www.rabbitmq.com/amqp-0-9-1-reference.html#basic.consume

        :param str queue: The queue to consume from. Use the empty string to
            specify the most recent server-named queue for this channel
        :param callable on_message_callback: The function to call when
            consuming with the signature
            on_message_callback(channel, method, properties, body), where
            - channel: pika.channel.Channel
            - method: pika.spec.Basic.Deliver
            - properties: pika.spec.BasicProperties
            - body: bytes
        :param bool auto_ack: if set to True, automatic acknowledgement mode
            will be used (see https://www.rabbitmq.com/confirms.html).
            This corresponds with the 'no_ack' parameter in the basic.consume
            AMQP 0.9.1 method
        :param bool exclusive: Don't allow other consumers on the queue
        :param str consumer_tag: Specify your own consumer tag
        :param dict arguments: Custom key/value pair arguments for the consumer
        :param callable callback: callback(pika.frame.Method) for method
          Basic.ConsumeOk.
        :returns: Consumer tag which may be used to cancel the consumer.
        :rtype: str
        :raises ValueError:
        """
        ...
    def basic_get(
        self, queue: str, callback: Callable[[Channel, Basic.GetOk, BasicProperties, bytes], object], auto_ack: bool = False
    ) -> None:
        """
        Get a single message from the AMQP broker. If you want to
        be notified of Basic.GetEmpty, use the Channel.add_callback method
        adding your Basic.GetEmpty callback which should expect only one
        parameter, frame. Due to implementation details, this cannot be called
        a second time until the callback is executed.  For more information on
        basic_get and its parameters, see:

        https://www.rabbitmq.com/amqp-0-9-1-reference.html#basic.get

        :param str queue: The queue from which to get a message. Use the empty
            string to specify the most recent server-named queue for this
            channel
        :param callable callback: The callback to call with a message that has
            the signature callback(channel, method, properties, body), where:
            - channel: pika.channel.Channel
            - method: pika.spec.Basic.GetOk
            - properties: pika.spec.BasicProperties
            - body: bytes
        :param bool auto_ack: Tell the broker to not expect a reply
        :raises ValueError:
        """
        ...
    def basic_nack(self, delivery_tag: int = 0, multiple: bool = False, requeue: bool = True) -> None:
        """
        This method allows a client to reject one or more incoming messages.
        It can be used to interrupt and cancel large incoming messages, or
        return untreatable messages to their original queue.

        :param integer delivery_tag: int/long The server-assigned delivery tag
        :param bool multiple: If set to True, the delivery tag is treated as
                              "up to and including", so that multiple messages
                              can be acknowledged with a single method. If set
                              to False, the delivery tag refers to a single
                              message. If the multiple field is 1, and the
                              delivery tag is zero, this indicates
                              acknowledgement of all outstanding messages.
        :param bool requeue: If requeue is true, the server will attempt to
                             requeue the message. If requeue is false or the
                             requeue attempt fails the messages are discarded or
                             dead-lettered.
        """
        ...
    def basic_publish(
        self,
        exchange: str,
        routing_key: str,
        body: str | bytes,
        properties: BasicProperties | None = None,
        mandatory: bool = False,
    ) -> None:
        """
        Publish to the channel with the given exchange, routing key and body.
        For more information on basic_publish and what the parameters do, see:

        https://www.rabbitmq.com/amqp-0-9-1-reference.html#basic.publish

        :param str exchange: The exchange to publish to
        :param str routing_key: The routing key to bind on
        :param bytes body: The message body
        :param pika.spec.BasicProperties properties: Basic.properties
        :param bool mandatory: The mandatory flag
        """
        ...
    def basic_qos(
        self,
        prefetch_size: int = 0,
        prefetch_count: int = 0,
        global_qos: bool = False,
        callback: Callable[[Method[Basic.QosOk]], object] | None = None,
    ) -> None:
        """
        Specify quality of service. This method requests a specific quality
        of service. The client can request that messages be sent in advance
        so that when the client finishes processing a message, the following
        message is already held locally, rather than needing to be sent down
        the channel. The QoS can be applied separately to each new consumer on
        channel or shared across all consumers on the channel. Prefetching
        gives a performance improvement.

        :param int prefetch_size:  This field specifies the prefetch window
                                   size. The server will send a message in
                                   advance if it is equal to or smaller in size
                                   than the available prefetch size (and also
                                   falls into other prefetch limits). May be set
                                   to zero, meaning "no specific limit",
                                   although other prefetch limits may still
                                   apply. The prefetch-size is ignored by
                                   consumers who have enabled the no-ack option.
        :param int prefetch_count: Specifies a prefetch window in terms of whole
                                   messages. This field may be used in
                                   combination with the prefetch-size field; a
                                   message will only be sent in advance if both
                                   prefetch windows (and those at the channel
                                   and connection level) allow it. The
                                   prefetch-count is ignored by consumers who
                                   have enabled the no-ack option.
        :param bool global_qos:    Should the QoS be shared across all
                                   consumers on the channel.
        :param callable callback: The callback to call for Basic.QosOk response
        :returns: ``None``. Method frame from the Basic.Qos-ok response is delivered
            to ``callback`` when provided.
        :raises ValueError:
        """
        ...
    def basic_reject(self, delivery_tag: int = 0, requeue: bool = True) -> None:
        """
        Reject an incoming message. This method allows a client to reject a
        message. It can be used to interrupt and cancel large incoming messages,
        or return untreatable messages to their original queue.

        :param integer delivery_tag: int/long The server-assigned delivery tag
        :param bool requeue: If requeue is true, the server will attempt to
                             requeue the message. If requeue is false or the
                             requeue attempt fails the messages are discarded or
                             dead-lettered.
        :raises: TypeError
        """
        ...
    def basic_recover(
        self, requeue: bool = False, callback: Callable[[Method[Basic.RecoverOk]], object] | None = None
    ) -> None:
        """
        This method asks the server to redeliver all unacknowledged messages
        on a specified channel. Zero or more messages may be redelivered. This
        method replaces the asynchronous Recover.

        :param bool requeue: If False, the message will be redelivered to the
                             original recipient. If True, the server will
                             attempt to requeue the message, potentially then
                             delivering it to an alternative subscriber.
        :param callable callback: callback(pika.frame.Method) for method
            Basic.RecoverOk
        :returns: ``None``. Method frame from the Basic.Recover-ok response is
            delivered to ``callback`` when provided.
        :raises ValueError:
        """
        ...
    def close(self, reply_code: int = 0, reply_text: str = "Normal shutdown") -> None:
        """
        Invoke a graceful shutdown of the channel with the AMQP Broker.

        If channel is OPENING, transition to CLOSING and suppress the incoming
        Channel.OpenOk, if any.

        :param int reply_code: The reason code to send to broker
        :param str reply_text: The reason text to send to broker

        :raises ChannelWrongStateError: if channel is closed or closing
        """
        ...
    def confirm_delivery(
        self,
        ack_nack_callback: Callable[[Method[Basic.Ack | Basic.Nack]], object],
        callback: Callable[[Method[Confirm.SelectOk]], object] | None = None,
    ) -> None:
        """
        Turn on Confirm mode in the channel. Pass in a callback to be
        notified by the Broker when a message has been confirmed as received or
        rejected (Basic.Ack, Basic.Nack) from the broker to the publisher.

        For more information see:
            https://www.rabbitmq.com/confirms.html

        :param callable ack_nack_callback: Required callback for delivery
            confirmations that has the following signature:
            callback(pika.frame.Method), where method_frame contains
            either method `spec.Basic.Ack` or `spec.Basic.Nack`.
        :param callable callback: callback(pika.frame.Method) for method
            Confirm.SelectOk
        :raises ValueError:
        """
        ...
    @property
    def consumer_tags(self) -> list[str]:
        """
        Property method that returns a list of currently active consumers

        :rtype: list
        """
        ...
    def exchange_bind(
        self,
        destination: str,
        source: str,
        routing_key: str = "",
        arguments: Mapping[str, Incomplete] | None = None,
        callback: Callable[[Method[Exchange.BindOk]], object] | None = None,
    ) -> None:
        """
        Bind an exchange to another exchange.

        :param str destination: The destination exchange to bind
        :param str source: The source exchange to bind to
        :param str routing_key: The routing key to bind on
        :param dict arguments: Custom key/value pair arguments for the binding
        :param callable callback: callback(pika.frame.Method) for method Exchange.BindOk
        :returns: ``None``. Method frame from the Exchange.Bind-ok response is
            delivered to ``callback`` when synchronous (no ok frame in nowait
            mode).
        :raises ValueError:
        """
        ...
    def exchange_declare(
        self,
        exchange: str,
        exchange_type: ExchangeType | str = ...,
        passive: bool = False,
        durable: bool = False,
        auto_delete: bool = False,
        internal: bool = False,
        arguments: Mapping[str, Incomplete] | None = None,
        callback: Callable[[Method[Exchange.DeclareOk]], object] | None = None,
    ) -> None:
        """
        This method creates an exchange if it does not already exist, and if
        the exchange exists, verifies that it is of the correct and expected
        class.

        If passive set, the server will reply with Declare-Ok if the exchange
        already exists with the same name, and raise an error if not and if the
        exchange does not already exist, the server MUST raise a channel
        exception with reply code 404 (not found).

        :param str exchange: The exchange name consists of a non-empty sequence
            of these characters: letters, digits, hyphen, underscore, period,
            or colon
        :param str exchange_type: The exchange type to use
        :param bool passive: Perform a declare or just check to see if it exists
        :param bool durable: Survive a reboot of RabbitMQ
        :param bool auto_delete: Remove when no more queues are bound to it
        :param bool internal: Can only be published to by other exchanges
        :param dict arguments: Custom key/value pair arguments for the exchange
        :param callable callback: callback(pika.frame.Method) for method Exchange.DeclareOk
        :returns: ``None``. Method frame from the Exchange.Declare-ok response is
            delivered to ``callback`` when synchronous (no ok frame in nowait
            mode).
        :raises ValueError:
        """
        ...
    def exchange_delete(
        self,
        exchange: str | None = None,
        if_unused: bool = False,
        callback: Callable[[Method[Exchange.DeleteOk]], object] | None = None,
    ) -> None:
        """
        Delete the exchange.

        :param str exchange: The exchange name
        :param bool if_unused: only delete if the exchange is unused
        :param callable callback: callback(pika.frame.Method) for method Exchange.DeleteOk
        :returns: ``None``. Method frame from the Exchange.Delete-ok response is
            delivered to ``callback`` when synchronous (no ok frame in nowait
            mode).
        :raises ValueError:
        """
        ...
    def exchange_unbind(
        self,
        destination: str | None = None,
        source: str | None = None,
        routing_key: str = "",
        arguments: Mapping[str, Incomplete] | None = None,
        callback: Callable[[Method[Exchange.UnbindOk]], object] | None = None,
    ) -> None:
        """
        Unbind an exchange from another exchange.

        :param str destination: The destination exchange to unbind
        :param str source: The source exchange to unbind from
        :param str routing_key: The routing key to unbind
        :param dict arguments: Custom key/value pair arguments for the binding
        :param callable callback: callback(pika.frame.Method) for method Exchange.UnbindOk
        :returns: ``None``. Method frame from the Exchange.Unbind-ok response is
            delivered to ``callback`` when synchronous (no ok frame in nowait
            mode).
        :raises ValueError:
        """
        ...
    def flow(self, active: bool, callback: Callable[[bool], object] | None = None) -> None:
        """
        Turn Channel flow control off and on. Pass a callback to be notified
        of the response from the server. active is a bool. Callback should
        expect a bool in response indicating channel flow state. For more
        information, please reference:

        https://www.rabbitmq.com/amqp-0-9-1-reference.html#channel.flow

        :param bool active: Turn flow on or off
        :param callable callback: callback(bool) upon completion
        :raises ValueError:
        """
        ...
    @property
    def is_closed(self) -> bool:
        """
        Returns True if the channel is closed.

        :rtype: bool
        """
        ...
    @property
    def is_closing(self) -> bool:
        """
        Returns True if client-initiated closing of the channel is in
        progress.

        :rtype: bool
        """
        ...
    @property
    def is_open(self) -> bool:
        """
        Returns True if the channel is open.

        :rtype: bool
        """
        ...
    @property
    def is_opening(self) -> bool:
        """
        Returns True if the channel is opening.

        :rtype: bool
        """
        ...
    def open(self) -> None:
        """Open the channel"""
        ...
    def queue_bind(
        self,
        queue: str,
        exchange: str,
        routing_key: str | None = None,
        arguments: Mapping[str, Incomplete] | None = None,
        callback: Callable[[Method[Queue.BindOk]], object] | None = None,
    ) -> None:
        """
        Bind the queue to the specified exchange

        :param str queue: The queue to bind to the exchange
        :param str exchange: The source exchange to bind to
        :param str routing_key: The routing key to bind on
        :param dict arguments: Custom key/value pair arguments for the binding
        :param callable callback: callback(pika.frame.Method) for method Queue.BindOk
        :returns: ``None``. Method frame from the Queue.Bind-ok response is delivered
            to ``callback`` when synchronous (no ok frame in nowait mode).
        :raises ValueError:
        """
        ...
    def queue_declare(
        self,
        queue: str,
        passive: bool = False,
        durable: bool = False,
        exclusive: bool = False,
        auto_delete: bool = False,
        arguments: Mapping[str, Incomplete] | None = None,
        callback: Callable[[Method[Queue.DeclareOk]], object] | None = None,
    ) -> None:
        """
        Declare queue, create if needed. This method creates or checks a
        queue. When creating a new queue the client can specify various
        properties that control the durability of the queue and its contents,
        and the level of sharing for the queue.

        Use an empty string as the queue name for the broker to auto-generate
        one

        :param str queue: The queue name; if empty string, the broker will
            create a unique queue name
        :param bool passive: Only check to see if the queue exists
        :param bool durable: Survive reboots of the broker
        :param bool exclusive: Only allow access by the current connection
        :param bool auto_delete: Delete after consumer cancels or disconnects
        :param dict arguments: Custom key/value arguments for the queue
        :param callable callback: callback(pika.frame.Method) for method Queue.DeclareOk
        :returns: ``None``. Method frame from the Queue.Declare-ok response is
            delivered to ``callback`` when synchronous (no ok frame in nowait
            mode).
        :raises ValueError:
        """
        ...
    def queue_delete(
        self,
        queue: str,
        if_unused: bool = False,
        if_empty: bool = False,
        callback: Callable[[Method[Queue.DeleteOk]], object] | None = None,
    ) -> None:
        """
        Delete a queue from the broker.

        :param str queue: The queue to delete
        :param bool if_unused: only delete if it's unused
        :param bool if_empty: only delete if the queue is empty
        :param callable callback: callback(pika.frame.Method) for method Queue.DeleteOk
        :returns: ``None``. Method frame from the Queue.Delete-ok response is
            delivered to ``callback`` when synchronous (no ok frame in nowait
            mode).
        :raises ValueError:
        """
        ...
    def queue_purge(self, queue: str, callback: Callable[[Method[Queue.PurgeOk]], object] | None = None) -> None:
        """
        Purge all of the messages from the specified queue

        :param str queue: The queue to purge
        :param callable callback: callback(pika.frame.Method) for method Queue.PurgeOk
        :returns: ``None``. Method frame from the Queue.Purge-ok response is
            delivered to ``callback`` when synchronous (no ok frame in nowait
            mode).
        :raises ValueError:
        """
        ...
    def queue_unbind(
        self,
        queue: str,
        exchange: str | None = None,
        routing_key: str | None = None,
        arguments: Mapping[str, Incomplete] | None = None,
        callback: Callable[[Method[Queue.UnbindOk]], object] | None = None,
    ):
        """
        Unbind a queue from an exchange.

        :param str queue: The queue to unbind from the exchange
        :param str exchange: The source exchange to bind from
        :param str routing_key: The routing key to unbind
        :param dict arguments: Custom key/value pair arguments for the binding
        :param callable callback: callback(pika.frame.Method) for method Queue.UnbindOk
        :returns: ``None``. Method frame from the Queue.Unbind-ok response is
            delivered to ``callback`` when provided.
        :raises ValueError:
        """
        ...
    def tx_commit(self, callback: Callable[[Method[Tx.CommitOk]], object] | None = None) -> None:
        """
        Commit a transaction

        :param callable callback: callback(pika.frame.Method) for method Tx.CommitOk
        :returns: ``None``. Method frame from the Tx.Commit-ok response is delivered
            to ``callback`` when provided.
        :raises ValueError:
        """
        ...
    def tx_rollback(self, callback: Callable[[Method[Tx.RollbackOk]], object] | None = None) -> None:
        """
        Rollback a transaction.

        :param callable callback: callback(pika.frame.Method) for method Tx.RollbackOk
        :returns: ``None``. Method frame from the Tx.Rollback-ok response is delivered
            to ``callback`` when provided.
        :raises ValueError:
        """
        ...
    def tx_select(self, callback: Callable[[Method[Tx.SelectOk]], object] | None = None) -> None:
        """
        Select standard transaction mode. This method sets the channel to use
        standard transactions. The client must use this method at least once on
        a channel before using the Commit or Rollback methods.

        :param callable callback: callback(pika.frame.Method) for method Tx.SelectOk
        :returns: ``None``. Method frame from the Tx.Select-ok response is delivered
            to ``callback`` when provided.
        :raises ValueError:
        """
        ...

class ContentFrameAssembler:
    def __init__(self) -> None: ...
    def process(self, frame_value: Method[_Method] | Header | Body) -> tuple[Method[_Method], Header, bytes] | None: ...

from _typeshed import Incomplete

from braintree.attribute_getter import AttributeGetter

class LocalPaymentContext(AttributeGetter):
    """Represents a local payment context."""
    def __init__(self, attributes: dict[str, Incomplete] | None = None) -> None: ...

from _typeshed import Incomplete

from braintree.error_result import ErrorResult
from braintree.graphql import CreateLocalPaymentContextInput
from braintree.successful_result import SuccessfulResult

class LocalPaymentContextGateway:
    """Creates and manages local payment contexts."""
    CREATE_LOCAL_PAYMENT_CONTEXT: str
    FIND_LOCAL_PAYMENT_CONTEXT: str
    gateway: Incomplete
    graphql_client: Incomplete
    def __init__(self, gateway) -> None: ...
    def create(self, input: CreateLocalPaymentContextInput) -> SuccessfulResult | ErrorResult:
        """
        Creates a local payment context.

        Args:
            input: CreateLocalPaymentContextInput object

        Returns:
            SuccessfulResult or ErrorResult
        """
        ...
    def find(self, id) -> SuccessfulResult | ErrorResult:
        """
        Finds a local payment context by ID.

        Args:
            id: The payment context ID

        Returns:
            SuccessfulResult or ErrorResult

        Raises:
            NotFoundError: If the payment context is not found
        """
        ...

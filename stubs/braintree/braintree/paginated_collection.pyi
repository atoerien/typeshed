from _typeshed import Incomplete
from collections.abc import Generator

class PaginatedCollection:
    """
    A class representing results from a paginated list. Supports the iterator protocol::

        results = braintree.MerchantAccount.all()
        for merchant_account in results.items:
            print merchant_account.id
    """
    def __init__(self, method) -> None: ...
    @property
    def items(self) -> Generator[Incomplete]: ...
    def __iter__(self): ...

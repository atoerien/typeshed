"""
oauthlib.oauth1.rfc5849.endpoints.base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module is an implementation of various logic needed
for signing and checking OAuth 1.0 RFC 5849 requests.
"""

from _typeshed import Incomplete

class BaseEndpoint:
    request_validator: Incomplete
    token_generator: Incomplete
    def __init__(self, request_validator, token_generator=None) -> None: ...

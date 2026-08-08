from typing import TypedDict, type_check_only
from typing_extensions import Self

@type_check_only
class _GraphqlVariables(TypedDict, total=False):
    countryPhoneCode: str
    phoneNumber: str
    extensionNumber: str

class PhoneInput:
    """Phone number input for PayPal customer session."""
    def __init__(
        self, country_phone_code: str | None = None, phone_number: str | None = None, extension_number: str | None = None
    ) -> None: ...
    def to_graphql_variables(self) -> _GraphqlVariables: ...
    @staticmethod
    def builder() -> Builder:
        """Creates a builder instance for fluent construction of PhoneInput objects."""
        ...

    class Builder:
        def __init__(self) -> None: ...
        def country_phone_code(self, country_phone_code: str) -> Self:
            """Sets the country phone code for the phone number."""
            ...
        def phone_number(self, phone_number: str) -> Self:
            """Sets the phone number."""
            ...
        def extension_number(self, extension_number: str) -> Self:
            """Sets the extension number."""
            ...
        def build(self) -> PhoneInput: ...

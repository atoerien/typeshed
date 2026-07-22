from _typeshed import Incomplete

class AuthorizationServerMetadata(dict[str, Incomplete]):
    """
    Authorization Server Metadata extension for RFC9207.

    This class can be used with
    :meth:`~authlib.oauth2.rfc8414.AuthorizationServerMetadata.validate`
    to validate RFC9207-specific metadata::

        from authlib.oauth2 import rfc8414, rfc9207

        metadata = rfc8414.AuthorizationServerMetadata(data)
        metadata.validate(metadata_classes=[rfc9207.AuthorizationServerMetadata])
    """
    REGISTRY_KEYS: list[str]
    def validate_authorization_response_iss_parameter_supported(self) -> None:
        """
        Boolean parameter indicating whether the authorization server
        provides the iss parameter in the authorization response.

        If omitted, the default value is false.
        """
        ...

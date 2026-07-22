class AuthorizationServerMetadata(dict[str, object]):
    """
    Authorization Server Metadata extension for RFC9101 (JAR).

    This class can be used with
    :meth:`~authlib.oauth2.rfc8414.AuthorizationServerMetadata.validate`
    to validate JAR-specific metadata::

        from authlib.oauth2 import rfc8414, rfc9101

        metadata = rfc8414.AuthorizationServerMetadata(data)
        metadata.validate(metadata_classes=[rfc9101.AuthorizationServerMetadata])
    """
    REGISTRY_KEYS: list[str]
    def validate_require_signed_request_object(self) -> None:
        """Indicates where authorization request needs to be protected as Request Object and provided through either request or request_uri parameter."""
        ...

"""
Generate flat encode/decode functions for a StructField + version.

Given a StructField and a protocol version, generates Python functions
that encode/decode directly with zero dispatch overhead - no intermediate
SimpleField/ArrayField/StructField method calls.

Usage:
    from kafka.protocol.schemas.fields.codegen import CodegenContext
    # Encode: see StructField.compiled_encode_into()
    # Decode: see StructField.compiled_decode_from()
"""

from _typeshed import Incomplete

class CodegenContext:
    """Shared state for code generation."""
    lines: list[str]
    globs: dict[str, Incomplete]
    def __init__(self) -> None: ...
    def next_var(self, prefix: str = "v") -> str: ...
    def emit(self, indent, line) -> None: ...
    def emit_reserve(self, indent, nbytes) -> None:
        """
        Emit an inline capacity check before a write of up to ``nbytes`` bytes.

        Generated encode functions keep three locals in sync:

          * ``buf``  - the destination bytearray (``out.buf``),
          * ``pos``  - the current write offset,
          * ``_cap`` - ``len(buf)``, the cached capacity.

        These are not set up per fragment: they are declared once by the
        ``def _encode(item, out):`` preamble in
        ``StructField.encode_into__optimized_context`` (the sole generator of
        the compiled encode function), and every emitted fragment - including
        this one - is spliced into that function body. Emit fragments are
        therefore only valid inside that body; they cannot stand alone.

        ``nbytes`` is the MAXIMUM number of bytes the following write can
        consume (an ``int`` for fixed/varint fields, or a string expression
        such as ``'len(_bv1)'`` for a variable payload). The fast path is a
        single comparison; only on overflow do we sync ``out.pos``, grow via
        :meth:`EncodeBuffer.ensure`, and re-read the (possibly reallocated)
        buffer back into ``buf``/``_cap``.

        Because :meth:`EncodeBuffer.ensure` may rebind ``out.buf``, code that
        instead delegates to a runtime ``encode_into`` (e.g. tagged fields)
        must re-bind ``buf``/``_cap`` itself afterwards - ``emit_reserve`` only
        covers writes emitted inline.
        """
        ...
    def source(self) -> None: ...
    def print(self) -> None: ...

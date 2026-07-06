def decompose(path): ...
def normalize(text):
    """
    Return *text* in a canonical Unicode form (NFC) so that names which are
    visually identical but encoded differently compare equal.

    macOS APFS/HFS+ store file names in decomposed form (NFD), while patterns
    in ``MANIFEST.in`` are typically authored composed (NFC). The two denote
    the same file but differ byte-for-byte, so matching them directly lets an
    exclusion silently fail. Normalizing both the walked path and the pattern
    to a single form before matching avoids that (GHSA-h35f-9h28-mq5c).
    """
    ...
def filesys_decode(path):
    """
    Ensure that the given path is decoded,
    ``None`` when no expected encoding works
    """
    ...
def try_encode(string, enc):
    """turn unicode encoding into a functional routine"""
    ...

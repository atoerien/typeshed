"""
Rasterio caches HTTP responses using GDAL's VSI CURL cache.

A global LRU cache of 16 MB shared among all downloaded content is
enabled by default, and content in it may be reused after a dataset has
been closed and reopened. Responses from FTP and HTTP servers, including
cloud storage like AWS S3 and Microsoft Azure, are stored in this cache.
Responses from HTTP servers used by Rasterio's Python openers are not.

The size of the cache and which responses are stored can be controlled
by GDAL's CPL_VSIL_CURL_CACHE_SIZE and CPL_VSIL_CURL_NON_CACHED
configuration options. For details See
https://gdal.org/en/latest/user/configoptions.html.
"""

def invalidate(pattern: str) -> None:
    """
    Invalidate responses in Rasterio's HTTP cache

    Parameters
    ----------
    pattern : str
        All responses beginning with this pattern will be invalidated.
        Responses served from a particular website can be invalidated
        using a pattern like "https://example.com". Responses served
        from an S3 bucket can be invalidated using a pattern like
        "s3://example.com", where "example.com" is the bucket name.
        Invalidation can be made more selective by appending path
        segments to the pattern. "s3://example.com/prefix" will
        invalidate only responses served for requests for objects in the
        "example.com" bucket that have a key beginning with "prefix".

    Returns
    -------
    None
    """
    ...
def invalidate_all() -> None:
    """
    Invalidate all responses in Rasterio's HTTP cache

    Returns
    -------
    None
    """
    ...

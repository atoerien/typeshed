"""
Rasterio tools module

See this RFC about Rasterio tools:
https://github.com/rasterio/rasterio/issues/1300.
"""

import os
from collections.abc import Callable, Iterable
from typing import Any, Final

class JSONSequenceTool:
    """
    Extracts data from a dataset file and saves a JSON sequence
    
    """
    func: Callable[..., Iterable[Any]]
    def __init__(self, func: Callable[..., Iterable[Any]]) -> None:
        """
        Initialize tool

        Parameters
        ----------
        func : callable
            A function or other callable object that takes a dataset and
            yields JSON serializable objects.
        """
        ...
    def __call__(
        self,
        src_path: str | os.PathLike[str],
        dst_path: str | os.PathLike[str],
        src_kwargs: dict[str, Any] | None = None,
        dst_kwargs: dict[str, Any] | None = None,
        func_args: Iterable[Any] | None = None,
        func_kwargs: dict[str, Any] | None = None,
        config: dict[str, Any] | None = None,
    ) -> None:
        """
        Execute the tool's primary function and perform file I/O

        Parameters
        ----------
        src_path : str or PathLike object
            A dataset path or URL. Will be opened in "r" mode using
            src_opts.
        dst_path : str or Path-like object
            A path or or PathLike object. Will be opened in "w" mode.
        src_kwargs : dict
            Options that will be passed to rasterio.open when opening
            src.
        dst_kwargs : dict
            Options that will be passed to json.dumps when serializing
            output.
        func_args : sequence
            Extra positional arguments for the tool's primary function.
        func_kwargs : dict
            Extra keyword arguments for the tool's primary function.
        config : dict
            Rasterio Env options.

        Returns
        -------
        None

        Side effects
        ------------
        Writes sequences of JSON texts to the named output file.
        """
        ...

dataset_features_tool: Final[JSONSequenceTool]

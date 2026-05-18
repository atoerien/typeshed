"""Public API for tf._api.v2.data namespace"""

from _typeshed import Incomplete
from abc import ABC, abstractmethod
from collections.abc import Callable, Collection, Iterator as _Iterator, Sequence
from typing import Any, Generic, TypeVar, overload
from typing_extensions import Self, Unpack

import numpy as np
import tensorflow as tf
from tensorflow import TypeSpec
from tensorflow._aliases import ContainerGeneric, ScalarTensorCompatible, TensorCompatible
from tensorflow.data import experimental as experimental
from tensorflow.data.experimental import AUTOTUNE as AUTOTUNE
from tensorflow.dtypes import DType
from tensorflow.io import _CompressionTypes
from tensorflow.python.trackable.base import Trackable

_T1_co = TypeVar("_T1_co", covariant=True)
_T2 = TypeVar("_T2")
_T3 = TypeVar("_T3")

class Iterator(_Iterator[_T1_co], Trackable, ABC):
    """
    Represents an iterator of a `tf.data.Dataset`.

    `tf.data.Iterator` is the primary mechanism for enumerating elements of a
    `tf.data.Dataset`. It supports the Python Iterator protocol, which means
    it can be iterated over using a for-loop:

    >>> dataset = tf.data.Dataset.range(2)
    >>> for element in dataset:
    ...   print(element)
    tf.Tensor(0, shape=(), dtype=int64)
    tf.Tensor(1, shape=(), dtype=int64)

    or by fetching individual elements explicitly via `get_next()`:

    >>> dataset = tf.data.Dataset.range(2)
    >>> iterator = iter(dataset)
    >>> print(iterator.get_next())
    tf.Tensor(0, shape=(), dtype=int64)
    >>> print(iterator.get_next())
    tf.Tensor(1, shape=(), dtype=int64)

    In addition, non-raising iteration is supported via `get_next_as_optional()`,
    which returns the next element (if available) wrapped in a
    `tf.experimental.Optional`.

    >>> dataset = tf.data.Dataset.from_tensors(42)
    >>> iterator = iter(dataset)
    >>> optional = iterator.get_next_as_optional()
    >>> print(optional.has_value())
    tf.Tensor(True, shape=(), dtype=bool)
    >>> optional = iterator.get_next_as_optional()
    >>> print(optional.has_value())
    tf.Tensor(False, shape=(), dtype=bool)
    """
    @property
    @abstractmethod
    def element_spec(self) -> ContainerGeneric[TypeSpec[Any]]:
        """
        The type specification of an element of this iterator.

        >>> dataset = tf.data.Dataset.from_tensors(42)
        >>> iterator = iter(dataset)
        >>> iterator.element_spec
        tf.TensorSpec(shape=(), dtype=tf.int32, name=None)

        For more information,
        read [this guide](https://www.tensorflow.org/guide/data#dataset_structure).

        Returns:
          A (nested) structure of `tf.TypeSpec` objects matching the structure of an
          element of this iterator, specifying the type of individual components.
        """
        ...
    @abstractmethod
    def get_next(self) -> _T1_co:
        """
        Returns the next element.

        >>> dataset = tf.data.Dataset.from_tensors(42)
        >>> iterator = iter(dataset)
        >>> print(iterator.get_next())
        tf.Tensor(42, shape=(), dtype=int32)

        Returns:
          A (nested) structure of values matching `tf.data.Iterator.element_spec`.

        Raises:
          `tf.errors.OutOfRangeError`: If the end of the iterator has been reached.
        """
        ...
    @abstractmethod
    def get_next_as_optional(self) -> tf.experimental.Optional[_T1_co]:
        """
        Returns the next element wrapped in `tf.experimental.Optional`.

        If the iterator has reached the end of the sequence, the returned
        `tf.experimental.Optional` will have no value.

        >>> dataset = tf.data.Dataset.from_tensors(42)
        >>> iterator = iter(dataset)
        >>> optional = iterator.get_next_as_optional()
        >>> print(optional.has_value())
        tf.Tensor(True, shape=(), dtype=bool)
        >>> print(optional.get_value())
        tf.Tensor(42, shape=(), dtype=int32)
        >>> optional = iterator.get_next_as_optional()
        >>> print(optional.has_value())
        tf.Tensor(False, shape=(), dtype=bool)

        Returns:
          A `tf.experimental.Optional` object representing the next element.
        """
        ...

class Dataset(ABC, Generic[_T1_co]):
    """
    Represents a potentially large set of elements.

    The `tf.data.Dataset` API supports writing descriptive and efficient input
    pipelines. `Dataset` usage follows a common pattern:

    1. Create a source dataset from your input data.
    2. Apply dataset transformations to preprocess the data.
    3. Iterate over the dataset and process the elements.

    Iteration happens in a streaming fashion, so the full dataset does not need to
    fit into memory.

    Source Datasets:

    The simplest way to create a dataset is to create it from a python `list`:

    >>> dataset = tf.data.Dataset.from_tensor_slices([1, 2, 3])
    >>> for element in dataset:
    ...   print(element)
    tf.Tensor(1, shape=(), dtype=int32)
    tf.Tensor(2, shape=(), dtype=int32)
    tf.Tensor(3, shape=(), dtype=int32)

    To process lines from files, use `tf.data.TextLineDataset`:

    >>> dataset = tf.data.TextLineDataset(["file1.txt", "file2.txt"])

    To process records written in the `TFRecord` format, use `TFRecordDataset`:

    >>> dataset = tf.data.TFRecordDataset(["file1.tfrecords", "file2.tfrecords"])

    To create a dataset of all files matching a pattern, use
    `tf.data.Dataset.list_files`:

    ```python
    dataset = tf.data.Dataset.list_files("/path/*.txt")
    ```

    See `tf.data.FixedLengthRecordDataset` and `tf.data.Dataset.from_generator`
    for more ways to create datasets.

    Transformations:

    Once you have a dataset, you can apply transformations to prepare the data for
    your model:

    >>> dataset = tf.data.Dataset.from_tensor_slices([1, 2, 3])
    >>> dataset = dataset.map(lambda x: x*2)
    >>> [a.item() for a in dataset.as_numpy_iterator()]
    [2, 4, 6]

    Common Terms:

    **Element**: A single output from calling `next()` on a dataset iterator.
      Elements may be nested structures containing multiple components. For
      example, the element `(1, (3, "apple"))` has one tuple nested in another
      tuple. The components are `1`, `3`, and `"apple"`.

    **Component**: The leaf in the nested structure of an element.

    Supported types:

    Elements can be nested structures of tuples, named tuples, and dictionaries.
    Note that Python lists are *not* treated as nested structures of components.
    Instead, lists are converted to tensors and treated as components. For
    example, the element `(1, [1, 2, 3])` has only two components; the tensor `1`
    and the tensor `[1, 2, 3]`. Element components can be of any type
    representable by `tf.TypeSpec`, including `tf.Tensor`, `tf.data.Dataset`,
    `tf.sparse.SparseTensor`, `tf.RaggedTensor`, and `tf.TensorArray`.

    ```python
    a = 1 # Integer element
    b = 2.0 # Float element
    c = (1, 2) # Tuple element with 2 components
    d = {"a": (2, 2), "b": 3} # Dict element with 3 components
    Point = collections.namedtuple("Point", ["x", "y"])
    e = Point(1, 2) # Named tuple
    f = tf.data.Dataset.range(10) # Dataset element
    ```

    For more information,
    read [this guide](https://www.tensorflow.org/guide/data).
    """
    def apply(self, transformation_func: Callable[[Dataset[_T1_co]], Dataset[_T2]]) -> Dataset[_T2]:
        """
        Applies a transformation function to this dataset.

        `apply` enables chaining of custom `Dataset` transformations, which are
        represented as functions that take one `Dataset` argument and return a
        transformed `Dataset`.

        >>> dataset = tf.data.Dataset.range(100)
        >>> def dataset_fn(ds):
        ...   return ds.filter(lambda x: x < 5)
        >>> dataset = dataset.apply(dataset_fn)
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [0, 1, 2, 3, 4]

        Args:
          transformation_func: A function that takes one `Dataset` argument and
            returns a `Dataset`.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def as_numpy_iterator(self) -> Iterator[np.ndarray[Any, Any]]:
        """
        Returns an iterator which converts all elements of the dataset to numpy.

        Use `as_numpy_iterator` to inspect the content of your dataset. To see
        element shapes and types, print dataset elements directly instead of using
        `as_numpy_iterator`.

        >>> dataset = tf.data.Dataset.from_tensor_slices([1, 2, 3])
        >>> for element in dataset:
        ...   print(element)
        tf.Tensor(1, shape=(), dtype=int32)
        tf.Tensor(2, shape=(), dtype=int32)
        tf.Tensor(3, shape=(), dtype=int32)

        This method requires that you are running in eager mode and the dataset's
        element_spec contains only `TensorSpec` components.

        >>> dataset = tf.data.Dataset.from_tensor_slices([1, 2, 3])
        >>> for element in dataset.as_numpy_iterator():
        ...   print(element)
        1
        2
        3

        >>> dataset = tf.data.Dataset.from_tensor_slices([1, 2, 3])
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [1, 2, 3]

        `as_numpy_iterator()` will preserve the nested structure of dataset
        elements.

        >>> dataset = tf.data.Dataset.from_tensor_slices({'a': ([1, 2], [3, 4]),
        ...                                               'b': [5, 6]})
        >>> list(dataset.as_numpy_iterator()) == [{'a': (1, 3), 'b': 5},
        ...                                       {'a': (2, 4), 'b': 6}]
        True

        Returns:
          An iterable over the elements of the dataset, with their tensors converted
          to numpy arrays.

        Raises:
          TypeError: if an element contains a non-`Tensor` value.
          RuntimeError: if eager execution is not enabled.
        """
        ...
    def batch(
        self,
        batch_size: ScalarTensorCompatible,
        drop_remainder: bool = False,
        num_parallel_calls: int | None = None,
        deterministic: bool | None = None,
        name: str | None = None,
    ) -> Dataset[_T1_co]:
        """
        Combines consecutive elements of this dataset into batches.

        >>> dataset = tf.data.Dataset.range(8)
        >>> dataset = dataset.batch(3)
        >>> list(dataset.as_numpy_iterator())
        [array([0, 1, 2]), array([3, 4, 5]), array([6, 7])]

        >>> dataset = tf.data.Dataset.range(8)
        >>> dataset = dataset.batch(3, drop_remainder=True)
        >>> list(dataset.as_numpy_iterator())
        [array([0, 1, 2]), array([3, 4, 5])]

        The components of the resulting element will have an additional outer
        dimension, which will be `batch_size` (or `N % batch_size` for the last
        element if `batch_size` does not divide the number of input elements `N`
        evenly and `drop_remainder` is `False`). If your program depends on the
        batches having the same outer dimension, you should set the `drop_remainder`
        argument to `True` to prevent the smaller batch from being produced.

        Note: If your program requires data to have a statically known shape (e.g.,
        when using XLA), you should use `drop_remainder=True`. Without
        `drop_remainder=True` the shape of the output dataset will have an unknown
        leading dimension due to the possibility of a smaller final batch.

        Args:
          batch_size: A `tf.int64` scalar `tf.Tensor`, representing the number of
            consecutive elements of this dataset to combine in a single batch.
          drop_remainder: (Optional.) A `tf.bool` scalar `tf.Tensor`, representing
            whether the last batch should be dropped in the case it has fewer than
            `batch_size` elements; the default behavior is not to drop the smaller
            batch.
          num_parallel_calls: (Optional.) A `tf.int64` scalar `tf.Tensor`,
            representing the number of batches to compute asynchronously in
            parallel.
            If not specified, batches will be computed sequentially. If the value
            `tf.data.AUTOTUNE` is used, then the number of parallel
            calls is set dynamically based on available resources.
          deterministic: (Optional.) When `num_parallel_calls` is specified, if this
            boolean is specified (`True` or `False`), it controls the order in which
            the transformation produces elements. If set to `False`, the
            transformation is allowed to yield elements out of order to trade
            determinism for performance. If not specified, the
            `tf.data.Options.deterministic` option (`True` by default) controls the
            behavior.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def bucket_by_sequence_length(
        self,
        element_length_func: Callable[[_T1_co], ScalarTensorCompatible],
        bucket_boundaries: Sequence[int],
        bucket_batch_sizes: Sequence[int],
        padded_shapes: ContainerGeneric[tf.TensorShape | TensorCompatible] | None = None,
        padding_values: ContainerGeneric[ScalarTensorCompatible] | None = None,
        pad_to_bucket_boundary: bool = False,
        no_padding: bool = False,
        drop_remainder: bool = False,
        name: str | None = None,
    ) -> Dataset[_T1_co]:
        """
        A transformation that buckets elements in a `Dataset` by length.

        Elements of the `Dataset` are grouped together by length and then are padded
        and batched.

        This is useful for sequence tasks in which the elements have variable
        length. Grouping together elements that have similar lengths reduces the
        total fraction of padding in a batch which increases training step
        efficiency.

        Below is an example to bucketize the input data to the 3 buckets
        "[0, 3), [3, 5), [5, inf)" based on sequence length, with batch size 2.

        >>> elements = [
        ...   [0], [1, 2, 3, 4], [5, 6, 7],
        ...   [7, 8, 9, 10, 11], [13, 14, 15, 16, 19, 20], [21, 22]]
        >>> dataset = tf.data.Dataset.from_generator(
        ...     lambda: elements, tf.int64, output_shapes=[None])
        >>> dataset = dataset.bucket_by_sequence_length(
        ...         element_length_func=lambda elem: tf.shape(elem)[0],
        ...         bucket_boundaries=[3, 5],
        ...         bucket_batch_sizes=[2, 2, 2])
        >>> for elem in dataset.as_numpy_iterator():
        ...   print(elem)
        [[1 2 3 4]
        [5 6 7 0]]
        [[ 7  8  9 10 11  0]
        [13 14 15 16 19 20]]
        [[ 0  0]
        [21 22]]

        Args:
          element_length_func: function from element in `Dataset` to `tf.int32`,
            determines the length of the element, which will determine the bucket it
            goes into.
          bucket_boundaries: `list<int>`, upper length boundaries of the buckets.
          bucket_batch_sizes: `list<int>`, batch size per bucket. Length should be
            `len(bucket_boundaries) + 1`.
          padded_shapes: Nested structure of `tf.TensorShape` to pass to
            `tf.data.Dataset.padded_batch`. If not provided, will use
            `dataset.output_shapes`, which will result in variable length dimensions
            being padded out to the maximum length in each batch.
          padding_values: Values to pad with, passed to
            `tf.data.Dataset.padded_batch`. Defaults to padding with 0.
          pad_to_bucket_boundary: bool, if `False`, will pad dimensions with unknown
            size to maximum length in batch. If `True`, will pad dimensions with
            unknown size to bucket boundary minus 1 (i.e., the maximum length in
            each bucket), and caller must ensure that the source `Dataset` does not
            contain any elements with length longer than `max(bucket_boundaries)`.
          no_padding: `bool`, indicates whether to pad the batch features (features
            need to be either of type `tf.sparse.SparseTensor` or of same shape).
          drop_remainder: (Optional.) A `tf.bool` scalar `tf.Tensor`, representing
            whether the last batch should be dropped in the case it has fewer than
            `batch_size` elements; the default behavior is not to drop the smaller
            batch.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.

        Raises:
          ValueError: if `len(bucket_batch_sizes) != len(bucket_boundaries) + 1`.
        """
        ...
    def cache(self, filename: str = "", name: str | None = None) -> Dataset[_T1_co]:
        """
        Caches the elements in this dataset.

        The first time the dataset is iterated over, its elements will be cached
        either in the specified file or in memory. Subsequent iterations will
        use the cached data.

        Note: To guarantee that the cache gets finalized, the input dataset must be
        iterated through in its entirety, until it raises StopIteration. Otherwise,
        subsequent iterations may not use cached data.

        >>> dataset = tf.data.Dataset.range(5)
        >>> dataset = dataset.map(lambda x: x**2)
        >>> dataset = dataset.cache()
        >>> # The first time reading through the data will generate the data using
        >>> # `range` and `map`.
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [0, 1, 4, 9, 16]
        >>> # Subsequent iterations read from the cache.
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [0, 1, 4, 9, 16]

        When caching to a file, the cached data will persist across runs. Even the
        first iteration through the data will read from the cache file. Changing
        the input pipeline before the call to `.cache()` will have no effect until
        the cache file is removed or the filename is changed.

        ```python
        dataset = tf.data.Dataset.range(5)
        dataset = dataset.cache("/path/to/file")
        list(dataset.as_numpy_iterator())
        # [0, 1, 2, 3, 4]
        dataset = tf.data.Dataset.range(10)
        dataset = dataset.cache("/path/to/file")  # Same file!
        list(dataset.as_numpy_iterator())
        # [0, 1, 2, 3, 4]
        ```

        Note: `cache` will produce exactly the same elements during each iteration
        through the dataset. If you wish to randomize the iteration order, make sure
        to call `shuffle` *after* calling `cache`.

        Args:
          filename: A `tf.string` scalar `tf.Tensor`, representing the name of a
            directory on the filesystem to use for caching elements in this Dataset.
            If a filename is not provided, the dataset will be cached in memory.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def cardinality(self) -> int:
        """
        Returns the cardinality of the dataset, if known.

        `cardinality` may return `tf.data.INFINITE_CARDINALITY` if the dataset
        contains an infinite number of elements or `tf.data.UNKNOWN_CARDINALITY` if
        the analysis fails to determine the number of elements in the dataset
        (e.g. when the dataset source is a file).

        >>> dataset = tf.data.Dataset.range(42)
        >>> print(dataset.cardinality().numpy())
        42
        >>> dataset = dataset.repeat()
        >>> cardinality = dataset.cardinality()
        >>> print((cardinality == tf.data.INFINITE_CARDINALITY).numpy())
        True
        >>> dataset = dataset.filter(lambda x: True)
        >>> cardinality = dataset.cardinality()
        >>> print((cardinality == tf.data.UNKNOWN_CARDINALITY).numpy())
        True

        Returns:
          A scalar `tf.int64` `Tensor` representing the cardinality of the dataset.
          If the cardinality is infinite or unknown, `cardinality` returns the
          named constants `tf.data.INFINITE_CARDINALITY` and
          `tf.data.UNKNOWN_CARDINALITY` respectively.
        """
        ...
    @staticmethod
    def choose_from_datasets(
        datasets: Sequence[Dataset[_T2]], choice_dataset: Dataset[tf.Tensor], stop_on_empty_dataset: bool = True
    ) -> Dataset[_T2]:
        """
        Creates a dataset that deterministically chooses elements from `datasets`.

        For example, given the following datasets:

        ```python
        datasets = [tf.data.Dataset.from_tensors("foo").repeat(),
                    tf.data.Dataset.from_tensors("bar").repeat(),
                    tf.data.Dataset.from_tensors("baz").repeat()]

        # Define a dataset containing `[0, 1, 2, 0, 1, 2, 0, 1, 2]`.
        choice_dataset = tf.data.Dataset.range(3).repeat(3)

        result = tf.data.Dataset.choose_from_datasets(datasets, choice_dataset)
        ```

        The elements of `result` will be:

        ```
        "foo", "bar", "baz", "foo", "bar", "baz", "foo", "bar", "baz"
        ```

        Args:
          datasets: A non-empty list of `tf.data.Dataset` objects with compatible
            structure.
          choice_dataset: A `tf.data.Dataset` of scalar `tf.int64` tensors between
            `0` and `len(datasets) - 1`.
          stop_on_empty_dataset: If `True`, selection stops if it encounters an
            empty dataset. If `False`, it skips empty datasets. It is recommended to
            set it to `True`. Otherwise, the selected elements start off as the user
            intends, but may change as input datasets become empty. This can be
            difficult to detect since the dataset starts off looking correct.
            Defaults to `True`.

        Returns:
          A new `Dataset` with the transformation applied as described above.

        Raises:
          TypeError: If `datasets` or `choice_dataset` has the wrong type.
          ValueError: If `datasets` is empty.
        """
        ...
    def concatenate(self, dataset: Dataset[_T1_co], name: str | None = None) -> Dataset[_T1_co]:
        """
        Creates a `Dataset` by concatenating the given dataset with this dataset.

        >>> a = tf.data.Dataset.range(1, 4)  # ==> [ 1, 2, 3 ]
        >>> b = tf.data.Dataset.range(4, 8)  # ==> [ 4, 5, 6, 7 ]
        >>> ds = a.concatenate(b)
        >>> [a.item() for a in ds.as_numpy_iterator()]
        [1, 2, 3, 4, 5, 6, 7]
        >>> # The input dataset and dataset to be concatenated should have
        >>> # compatible element specs.
        >>> c = tf.data.Dataset.zip((a, b))
        >>> a.concatenate(c)
        Traceback (most recent call last):
        TypeError: Two datasets to concatenate have different types
        <dtype: 'int64'> and (tf.int64, tf.int64)
        >>> d = tf.data.Dataset.from_tensor_slices(["a", "b", "c"])
        >>> a.concatenate(d)
        Traceback (most recent call last):
        TypeError: Two datasets to concatenate have different types
        <dtype: 'int64'> and <dtype: 'string'>

        Args:
          dataset: `Dataset` to be concatenated.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    @staticmethod
    def counter(
        start: ScalarTensorCompatible = 0, step: ScalarTensorCompatible = 1, dtype: DType = ..., name: str | None = None
    ) -> Dataset[tf.Tensor]:
        """
        Creates a `Dataset` that counts from `start` in steps of size `step`.

        Unlike `tf.data.Dataset.range`, which stops at some ending number,
        `tf.data.Dataset.counter` produces elements indefinitely.

        >>> dataset = tf.data.experimental.Counter().take(5)
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [0, 1, 2, 3, 4]
        >>> dataset.element_spec
        TensorSpec(shape=(), dtype=tf.int64, name=None)
        >>> dataset = tf.data.experimental.Counter(dtype=tf.int32)
        >>> dataset.element_spec
        TensorSpec(shape=(), dtype=tf.int32, name=None)
        >>> dataset = tf.data.experimental.Counter(start=2).take(5)
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [2, 3, 4, 5, 6]
        >>> dataset = tf.data.experimental.Counter(start=2, step=5).take(5)
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [2, 7, 12, 17, 22]
        >>> dataset = tf.data.experimental.Counter(start=10, step=-1).take(5)
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [10, 9, 8, 7, 6]

        Args:
          start: (Optional.) The starting value for the counter. Defaults to 0.
          step: (Optional.) The step size for the counter. Defaults to 1.
          dtype: (Optional.) The data type for counter elements. Defaults to
            `tf.int64`.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A `Dataset` of scalar `dtype` elements.
        """
        ...
    @property
    @abstractmethod
    def element_spec(self) -> ContainerGeneric[TypeSpec[Any]]:
        """
        The type specification of an element of this dataset.

        >>> dataset = tf.data.Dataset.from_tensor_slices([1, 2, 3])
        >>> dataset.element_spec
        TensorSpec(shape=(), dtype=tf.int32, name=None)

        For more information,
        read [this guide](https://www.tensorflow.org/guide/data#dataset_structure).

        Returns:
          A (nested) structure of `tf.TypeSpec` objects matching the structure of an
          element of this dataset and specifying the type of individual components.
        """
        ...
    def enumerate(self, start: ScalarTensorCompatible = 0, name: str | None = None) -> Dataset[tuple[int, _T1_co]]:
        """
        Enumerates the elements of this dataset.

        It is similar to python's `enumerate`.

        >>> dataset = tf.data.Dataset.from_tensor_slices([1, 2, 3])
        >>> dataset = dataset.enumerate(start=5)
        >>> for pos, element in dataset.as_numpy_iterator():
        ...   print(tuple((pos.item(), element.item())))
        (5, 1)
        (6, 2)
        (7, 3)

        >>> # The (nested) structure of the input dataset determines the
        >>> # structure of elements in the resulting dataset.
        >>> dataset = tf.data.Dataset.from_tensor_slices([(7, 8), (9, 10)])
        >>> dataset = dataset.enumerate()
        >>> for pos, element in dataset.as_numpy_iterator():
        ...   print(tuple((pos.item(), element)))
        (0, array([7, 8], dtype=int32))
        (1, array([ 9, 10], dtype=int32))

        Args:
          start: A `tf.int64` scalar `tf.Tensor`, representing the start value for
            enumeration.
          name: Optional. A name for the tf.data operations used by `enumerate`.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def filter(self, predicate: Callable[[_T1_co], bool | tf.Tensor], name: str | None = None) -> Dataset[_T1_co]:
        """
        Filters this dataset according to `predicate`.

        >>> dataset = tf.data.Dataset.from_tensor_slices([1, 2, 3])
        >>> dataset = dataset.filter(lambda x: x < 3)
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [1, 2]
        >>> # `tf.math.equal(x, y)` is required for equality comparison
        >>> def filter_fn(x):
        ...   return tf.math.equal(x, 1)
        >>> dataset = dataset.filter(filter_fn)
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [1]

        Args:
          predicate: A function mapping a dataset element to a boolean.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def flat_map(self, map_func: Callable[[_T1_co], Dataset[_T2]], name: str | None = None) -> Dataset[_T2]:
        """
        Maps `map_func` across this dataset and flattens the result.

        The type signature is:

        ```
        def flat_map(
          self: Dataset[T],
          map_func: Callable[[T], Dataset[S]]
        ) -> Dataset[S]
        ```

        Use `flat_map` if you want to make sure that the order of your dataset
        stays the same. For example, to flatten a dataset of batches into a
        dataset of their elements:

        >>> dataset = tf.data.Dataset.from_tensor_slices(
        ...     [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> dataset = dataset.flat_map(tf.data.Dataset.from_tensor_slices)
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [1, 2, 3, 4, 5, 6, 7, 8, 9]

        `tf.data.Dataset.interleave()` is a generalization of `flat_map`, since
        `flat_map` produces the same output as
        `tf.data.Dataset.interleave(cycle_length=1)`

        Args:
          map_func: A function mapping a dataset element to a dataset.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    # PEP 646 can be used here for a more precise type when better supported.
    @staticmethod
    def from_generator(
        generator: Callable[..., _T2],
        output_types: ContainerGeneric[DType] | None = None,
        output_shapes: ContainerGeneric[tf.TensorShape | Sequence[int | None]] | None = None,
        args: tuple[object, ...] | None = None,
        output_signature: ContainerGeneric[TypeSpec[Any]] | None = None,
        name: str | None = None,
    ) -> Dataset[_T2]:
        """
        Creates a `Dataset` whose elements are generated by `generator`. (deprecated arguments)

        Deprecated: SOME ARGUMENTS ARE DEPRECATED: `(output_shapes, output_types)`. They will be removed in a future version.
        Instructions for updating:
        Use output_signature instead

        Note: The current implementation of `Dataset.from_generator()` uses
        `tf.numpy_function` and inherits the same constraints. In particular, it
        requires the dataset and iterator related operations to be placed
        on a device in the same process as the Python program that called
        `Dataset.from_generator()`. In particular, using `from_generator` will
        preclude the use of tf.data service for scaling out dataset processing.
        The body of `generator` will not be serialized in a `GraphDef`, and you
        should not use this method if you need to serialize your model and restore
        it in a different environment.

        The `generator` argument must be a callable object that returns
        an object that supports the `iter()` protocol (e.g. a generator function).

        The elements generated by `generator` must be compatible with either the
        given `output_signature` argument or with the given `output_types` and
        (optionally) `output_shapes` arguments, whichever was specified.

        The recommended way to call `from_generator` is to use the
        `output_signature` argument. In this case the output will be assumed to
        consist of objects with the classes, shapes and types defined by
        `tf.TypeSpec` objects from `output_signature` argument:

        >>> def gen():
        ...   ragged_tensor = tf.ragged.constant([[1, 2], [3]])
        ...   yield 42, ragged_tensor
        >>>
        >>> dataset = tf.data.Dataset.from_generator(
        ...      gen,
        ...      output_signature=(
        ...          tf.TensorSpec(shape=(), dtype=tf.int32),
        ...          tf.RaggedTensorSpec(shape=(2, None), dtype=tf.int32)))
        >>>
        >>> list(dataset.take(1))
        [(<tf.Tensor: shape=(), dtype=int32, numpy=42>,
        <tf.RaggedTensor [[1, 2], [3]]>)]

        There is also a deprecated way to call `from_generator` by either with
        `output_types` argument alone or together with `output_shapes` argument.
        In this case the output of the function will be assumed to consist of
        `tf.Tensor` objects with the types defined by `output_types` and with the
        shapes which are either unknown or defined by `output_shapes`.

        Note: If `generator` depends on mutable global variables or other external
        state, be aware that the runtime may invoke `generator` multiple times
        (in order to support repeating the `Dataset`) and at any time
        between the call to `Dataset.from_generator()` and the production of the
        first element from the generator. Mutating global variables or external
        state can cause undefined behavior, and we recommend that you explicitly
        cache any external state in `generator` before calling
        `Dataset.from_generator()`.

        Note: While the `output_signature` parameter makes it possible to yield
        `Dataset` elements, the scope of `Dataset.from_generator()` should be
        limited to logic that cannot be expressed through tf.data operations. Using
        tf.data operations within the generator function is an anti-pattern and may
        result in incremental memory growth.

        Args:
          generator: A callable object that returns an object that supports the
            `iter()` protocol. If `args` is not specified, `generator` must take no
            arguments; otherwise it must take as many arguments as there are values
            in `args`.
          output_types: (Optional.) A (nested) structure of `tf.DType` objects
            corresponding to each component of an element yielded by `generator`.
          output_shapes: (Optional.) A (nested) structure of `tf.TensorShape`
            objects corresponding to each component of an element yielded by
            `generator`.
          args: (Optional.) A tuple of `tf.Tensor` objects that will be evaluated
            and passed to `generator` as NumPy-array arguments.
          output_signature: (Optional.) A (nested) structure of `tf.TypeSpec`
            objects corresponding to each component of an element yielded by
            `generator`.
          name: (Optional.) A name for the tf.data operations used by
            `from_generator`.

        Returns:
          Dataset: A `Dataset`.
        """
        ...
    @staticmethod
    def from_tensors(tensors: Any, name: str | None = None) -> Dataset[Any]:
        """
        Creates a `Dataset` with a single element, comprising the given tensors.

        `from_tensors` produces a dataset containing only a single element. To slice
        the input tensor into multiple elements, use `from_tensor_slices` instead.

        >>> dataset = tf.data.Dataset.from_tensors([1, 2, 3])
        >>> list(dataset.as_numpy_iterator())
        [array([1, 2, 3], dtype=int32)]
        >>> dataset = tf.data.Dataset.from_tensors(([1, 2, 3], 'A'))
        >>> list(dataset.as_numpy_iterator())
        [(array([1, 2, 3], dtype=int32), b'A')]

        >>> # You can use `from_tensors` to produce a dataset which repeats
        >>> # the same example many times.
        >>> example = tf.constant([1,2,3])
        >>> dataset = tf.data.Dataset.from_tensors(example).repeat(2)
        >>> list(dataset.as_numpy_iterator())
        [array([1, 2, 3], dtype=int32), array([1, 2, 3], dtype=int32)]

        Note that if `tensors` contains a NumPy array, and eager execution is not
        enabled, the values will be embedded in the graph as one or more
        `tf.constant` operations. For large datasets (> 1 GB), this can waste
        memory and run into byte limits of graph serialization. If `tensors`
        contains one or more large NumPy arrays, consider the alternative described
        in [this
        guide](https://tensorflow.org/guide/data#consuming_numpy_arrays).

        Args:
          tensors: A dataset "element". Supported values are documented
            [here](https://www.tensorflow.org/guide/data#dataset_structure).
          name: (Optional.) A name for the tf.data operation.

        Returns:
          Dataset: A `Dataset`.
        """
        ...
    @staticmethod
    def from_tensor_slices(tensors: TensorCompatible, name: str | None = None) -> Dataset[Any]:
        """
        Creates a `Dataset` whose elements are slices of the given tensors.

        The given tensors are sliced along their first dimension. This operation
        preserves the structure of the input tensors, removing the first dimension
        of each tensor and using it as the dataset dimension. All input tensors
        must have the same size in their first dimensions.

        >>> # Slicing a 1D tensor produces scalar tensor elements.
        >>> dataset = tf.data.Dataset.from_tensor_slices([1, 2, 3])
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [1, 2, 3]

        >>> # Slicing a 2D tensor produces 1D tensor elements.
        >>> dataset = tf.data.Dataset.from_tensor_slices([[1, 2], [3, 4]])
        >>> list(dataset.as_numpy_iterator())
        [array([1, 2], dtype=int32), array([3, 4], dtype=int32)]

        >>> # Slicing a tuple of 1D tensors produces tuple elements containing
        >>> # scalar tensors.
        >>> dataset = tf.data.Dataset.from_tensor_slices(([1, 2], [3, 4], [5, 6]))
        >>> [(n0.item(), n1.item(), n2.item()) for n0, n1, n2 in
        ...        dataset.as_numpy_iterator()]
        [(1, 3, 5), (2, 4, 6)]

        >>> # Dictionary structure is also preserved.
        >>> dataset = tf.data.Dataset.from_tensor_slices({"a": [1, 2], "b": [3, 4]})
        >>> list(dataset.as_numpy_iterator()) == [{'a': 1, 'b': 3},
        ...                                       {'a': 2, 'b': 4}]
        True

        >>> # Two tensors can be combined into one Dataset object.
        >>> features = tf.constant([[1, 3], [2, 1], [3, 3]]) # ==> 3x2 tensor
        >>> labels = tf.constant(['A', 'B', 'A']) # ==> 3x1 tensor
        >>> dataset = Dataset.from_tensor_slices((features, labels))
        >>> # Both the features and the labels tensors can be converted
        >>> # to a Dataset object separately and combined after.
        >>> features_dataset = Dataset.from_tensor_slices(features)
        >>> labels_dataset = Dataset.from_tensor_slices(labels)
        >>> dataset = Dataset.zip((features_dataset, labels_dataset))
        >>> # A batched feature and label set can be converted to a Dataset
        >>> # in similar fashion.
        >>> batched_features = tf.constant([[[1, 3], [2, 3]],
        ...                                 [[2, 1], [1, 2]],
        ...                                 [[3, 3], [3, 2]]], shape=(3, 2, 2))
        >>> batched_labels = tf.constant([['A', 'A'],
        ...                               ['B', 'B'],
        ...                               ['A', 'B']], shape=(3, 2, 1))
        >>> dataset = Dataset.from_tensor_slices((batched_features, batched_labels))
        >>> for element in dataset.as_numpy_iterator():
        ...   print(element)
        (array([[1, 3],
               [2, 3]], dtype=int32), array([[b'A'],
               [b'A']], dtype=object))
        (array([[2, 1],
               [1, 2]], dtype=int32), array([[b'B'],
               [b'B']], dtype=object))
        (array([[3, 3],
               [3, 2]], dtype=int32), array([[b'A'],
               [b'B']], dtype=object))

        Note that if `tensors` contains a NumPy array, and eager execution is not
        enabled, the values will be embedded in the graph as one or more
        `tf.constant` operations. For large datasets (> 1 GB), this can waste
        memory and run into byte limits of graph serialization. If `tensors`
        contains one or more large NumPy arrays, consider the alternative described
        in [this guide](
        https://tensorflow.org/guide/data#consuming_numpy_arrays).

        Args:
          tensors: A dataset element, whose components have the same first
            dimension. Supported values are documented
            [here](https://www.tensorflow.org/guide/data#dataset_structure).
          name: (Optional.) A name for the tf.data operation.

        Returns:
          Dataset: A `Dataset`.
        """
        ...
    def get_single_element(self, name: str | None = None) -> _T1_co:
        """
        Returns the single element of the `dataset`.

        The function enables you to use a `tf.data.Dataset` in a stateless
        "tensor-in tensor-out" expression, without creating an iterator.
        This facilitates the ease of data transformation on tensors using the
        optimized `tf.data.Dataset` abstraction on top of them.

        For example, lets consider a `preprocessing_fn` which would take as an
        input the raw features and returns the processed feature along with
        it's label.

        ```python
        def preprocessing_fn(raw_feature):
          # ... the raw_feature is preprocessed as per the use-case
          return feature

        raw_features = ...  # input batch of BATCH_SIZE elements.
        dataset = (tf.data.Dataset.from_tensor_slices(raw_features)
                  .map(preprocessing_fn, num_parallel_calls=BATCH_SIZE)
                  .batch(BATCH_SIZE))

        processed_features = dataset.get_single_element()
        ```

        In the above example, the `raw_features` tensor of length=BATCH_SIZE
        was converted to a `tf.data.Dataset`. Next, each of the `raw_feature` was
        mapped using the `preprocessing_fn` and the processed features were
        grouped into a single batch. The final `dataset` contains only one element
        which is a batch of all the processed features.

        NOTE: The `dataset` should contain only one element.

        Now, instead of creating an iterator for the `dataset` and retrieving the
        batch of features, the `tf.data.get_single_element()` function is used
        to skip the iterator creation process and directly output the batch of
        features.

        This can be particularly useful when your tensor transformations are
        expressed as `tf.data.Dataset` operations, and you want to use those
        transformations while serving your model.

        #### Keras

        ```python

        model = ... # A pre-built or custom model

        class PreprocessingModel(tf.keras.Model):
          def __init__(self, model):
            super().__init__(self)
            self.model = model

          @tf.function(input_signature=[...])
          def serving_fn(self, data):
            ds = tf.data.Dataset.from_tensor_slices(data)
            ds = ds.map(preprocessing_fn, num_parallel_calls=BATCH_SIZE)
            ds = ds.batch(batch_size=BATCH_SIZE)
            return tf.argmax(self.model(ds.get_single_element()), axis=-1)

        preprocessing_model = PreprocessingModel(model)
        your_exported_model_dir = ... # save the model to this path.
        tf.saved_model.save(preprocessing_model, your_exported_model_dir,
                      signatures={'serving_default': preprocessing_model.serving_fn}
                      )
        ```

        Args:
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A nested structure of `tf.Tensor` objects, corresponding to the single
          element of `dataset`.

        Raises:
          InvalidArgumentError: (at runtime) if `dataset` does not contain exactly
            one element.
        """
        ...
    def group_by_window(
        self,
        key_func: Callable[[_T1_co], tf.Tensor],
        reduce_func: Callable[[tf.Tensor, Dataset[_T1_co]], Dataset[_T2]],
        window_size: ScalarTensorCompatible | None = None,
        window_size_func: Callable[[tf.Tensor], tf.Tensor] | None = None,
        name: str | None = None,
    ) -> Dataset[_T2]:
        """
        Groups windows of elements by key and reduces them.

        This transformation maps each consecutive element in a dataset to a key
        using `key_func` and groups the elements by key. It then applies
        `reduce_func` to at most `window_size_func(key)` elements matching the same
        key. All except the final window for each key will contain
        `window_size_func(key)` elements; the final window may be smaller.

        You may provide either a constant `window_size` or a window size determined
        by the key through `window_size_func`.

        >>> dataset = tf.data.Dataset.range(10)
        >>> window_size = 5
        >>> key_func = lambda x: x%2
        >>> reduce_func = lambda key, dataset: dataset.batch(window_size)
        >>> dataset = dataset.group_by_window(
        ...           key_func=key_func,
        ...           reduce_func=reduce_func,
        ...           window_size=window_size)
        >>> for elem in dataset.as_numpy_iterator():
        ...   print(elem)
        [0 2 4 6 8]
        [1 3 5 7 9]

        Args:
          key_func: A function mapping a nested structure of tensors (having shapes
            and types defined by `self.output_shapes` and `self.output_types`) to a
            scalar `tf.int64` tensor.
          reduce_func: A function mapping a key and a dataset of up to `window_size`
            consecutive elements matching that key to another dataset.
          window_size: A `tf.int64` scalar `tf.Tensor`, representing the number of
            consecutive elements matching the same key to combine in a single batch,
            which will be passed to `reduce_func`. Mutually exclusive with
            `window_size_func`.
          window_size_func: A function mapping a key to a `tf.int64` scalar
            `tf.Tensor`, representing the number of consecutive elements matching
            the same key to combine in a single batch, which will be passed to
            `reduce_func`. Mutually exclusive with `window_size`.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.

        Raises:
          ValueError: if neither or both of {`window_size`, `window_size_func`} are
            passed.
        """
        ...
    def ignore_errors(self, log_warning: bool = False, name: str | None = None) -> Dataset[_T1_co]:
        """
        Drops elements that cause errors.

        >>> dataset = tf.data.Dataset.from_tensor_slices([1., 2., 0., 4.])
        >>> dataset = dataset.map(lambda x: tf.debugging.check_numerics(1. / x, ""))
        >>> list(dataset.as_numpy_iterator())
        Traceback (most recent call last):
        ...
        InvalidArgumentError: ... Tensor had Inf values
        >>> dataset = dataset.ignore_errors()
        >>> list(dataset.as_numpy_iterator())
        [1.0, 0.5, 0.25]

        Args:
          log_warning: (Optional.) A bool indicating whether or not ignored errors
            should be logged to stderr. Defaults to `False`.
          name: (Optional.) A string indicating a name for the `tf.data` operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def interleave(
        self,
        map_func: Callable[[_T1_co], Dataset[_T2]],
        cycle_length: int | None = None,
        block_length: int | None = None,
        num_parallel_calls: int | None = None,
        deterministic: bool | None = None,
        name: str | None = None,
    ) -> Dataset[_T2]:
        """
        Maps `map_func` across this dataset, and interleaves the results.

        The type signature is:

        ```
        def interleave(
          self: Dataset[T],
          map_func: Callable[[T], Dataset[S]]
        ) -> Dataset[S]
        ```

        For example, you can use `Dataset.interleave()` to process many input files
        concurrently:

        >>> # Preprocess 4 files concurrently, and interleave blocks of 16 records
        >>> # from each file.
        >>> filenames = ["/var/data/file1.txt", "/var/data/file2.txt",
        ...              "/var/data/file3.txt", "/var/data/file4.txt"]
        >>> dataset = tf.data.Dataset.from_tensor_slices(filenames)
        >>> def parse_fn(filename):
        ...   return tf.data.Dataset.range(10)
        >>> dataset = dataset.interleave(lambda x:
        ...     tf.data.TextLineDataset(x).map(parse_fn, num_parallel_calls=1),
        ...     cycle_length=4, block_length=16)

        The `cycle_length` and `block_length` arguments control the order in which
        elements are produced. `cycle_length` controls the number of input elements
        that are processed concurrently. If you set `cycle_length` to 1, this
        transformation will handle one input element at a time, and will produce
        identical results to `tf.data.Dataset.flat_map`. In general,
        this transformation will apply `map_func` to `cycle_length` input elements,
        open iterators on the returned `Dataset` objects, and cycle through them
        producing `block_length` consecutive elements from each iterator, and
        consuming the next input element each time it reaches the end of an
        iterator.

        For example:

        >>> dataset = Dataset.range(1, 6)  # ==> [ 1, 2, 3, 4, 5 ]
        >>> # NOTE: New lines indicate "block" boundaries.
        >>> dataset = dataset.interleave(
        ...     lambda x: Dataset.from_tensors(x).repeat(6),
        ...     cycle_length=2, block_length=4)
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [1, 1, 1, 1,
         2, 2, 2, 2,
         1, 1,
         2, 2,
         3, 3, 3, 3,
         4, 4, 4, 4,
         3, 3,
         4, 4,
         5, 5, 5, 5,
         5, 5]

        Note: The order of elements yielded by this transformation is
        deterministic, as long as `map_func` is a pure function and
        `deterministic=True`. If `map_func` contains any stateful operations, the
        order in which that state is accessed is undefined.

        Performance can often be improved by setting `num_parallel_calls` so that
        `interleave` will use multiple threads to fetch elements. If determinism
        isn't required, it can also improve performance to set
        `deterministic=False`.

        >>> filenames = ["/var/data/file1.txt", "/var/data/file2.txt",
        ...              "/var/data/file3.txt", "/var/data/file4.txt"]
        >>> dataset = tf.data.Dataset.from_tensor_slices(filenames)
        >>> dataset = dataset.interleave(lambda x: tf.data.TFRecordDataset(x),
        ...     cycle_length=4, num_parallel_calls=tf.data.AUTOTUNE,
        ...     deterministic=False)

        Args:
          map_func: A function that takes a dataset element and returns a
            `tf.data.Dataset`.
          cycle_length: (Optional.) The number of input elements that will be
            processed concurrently. If not set, the tf.data runtime decides what it
            should be based on available CPU. If `num_parallel_calls` is set to
            `tf.data.AUTOTUNE`, the `cycle_length` argument identifies
            the maximum degree of parallelism.
          block_length: (Optional.) The number of consecutive elements to produce
            from each input element before cycling to another input element. If not
            set, defaults to 1.
          num_parallel_calls: (Optional.) If specified, the implementation creates a
            threadpool, which is used to fetch inputs from cycle elements
            asynchronously and in parallel. The default behavior is to fetch inputs
            from cycle elements synchronously with no parallelism. If the value
            `tf.data.AUTOTUNE` is used, then the number of parallel
            calls is set dynamically based on available CPU.
          deterministic: (Optional.) When `num_parallel_calls` is specified, if this
            boolean is specified (`True` or `False`), it controls the order in which
            the transformation produces elements. If set to `False`, the
            transformation is allowed to yield elements out of order to trade
            determinism for performance. If not specified, the
            `tf.data.Options.deterministic` option (`True` by default) controls the
            behavior.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def __iter__(self) -> Iterator[_T1_co]:
        """
        Creates an iterator for elements of this dataset.

        The returned iterator implements the Python Iterator protocol.

        Returns:
          An `tf.data.Iterator` for the elements of this dataset.

        Raises:
          RuntimeError: If not inside of tf.function and not executing eagerly.
        """
        ...
    @staticmethod
    def list_files(
        file_pattern: str | Sequence[str] | TensorCompatible,
        shuffle: bool | None = None,
        seed: int | None = None,
        name: str | None = None,
    ) -> Dataset[str]:
        """
        A dataset of all files matching one or more glob patterns.

        The `file_pattern` argument should be a small number of glob patterns.
        If your filenames have already been globbed, use
        `Dataset.from_tensor_slices(filenames)` instead, as re-globbing every
        filename with `list_files` may result in poor performance with remote
        storage systems.

        Note: The default behavior of this method is to return filenames in
        a non-deterministic random shuffled order. Pass a `seed` or `shuffle=False`
        to get results in a deterministic order.

        Example:
          If we had the following files on our filesystem:

            - /path/to/dir/a.txt
            - /path/to/dir/b.py
            - /path/to/dir/c.py

          If we pass "/path/to/dir/*.py" as the directory, the dataset
          would produce:

            - /path/to/dir/b.py
            - /path/to/dir/c.py

        Args:
          file_pattern: A string, a list of strings, or a `tf.Tensor` of string type
            (scalar or vector), representing the filename glob (i.e. shell wildcard)
            pattern(s) that will be matched.
          shuffle: (Optional.) If `True`, the file names will be shuffled randomly.
            Defaults to `True`.
          seed: (Optional.) A `tf.int64` scalar `tf.Tensor`, representing the random
            seed that will be used to create the distribution. See
            `tf.random.set_seed` for behavior.
          name: Optional. A name for the tf.data operations used by `list_files`.

        Returns:
         Dataset: A `Dataset` of strings corresponding to file names.
        """
        ...
    @staticmethod
    def load(
        path: str,
        element_spec: ContainerGeneric[tf.TypeSpec[Any]] | None = None,
        compression: _CompressionTypes = None,
        reader_func: Callable[[Dataset[Dataset[Any]]], Dataset[Any]] | None = None,
        wait: bool = False,
    ) -> Dataset[Any]:
        """
        Loads a previously saved dataset.

        Example usage:

        >>> import tempfile
        >>> path = os.path.join(tempfile.gettempdir(), "saved_data")
        >>> # Save a dataset
        >>> dataset = tf.data.Dataset.range(2)
        >>> tf.data.Dataset.save(dataset, path)
        >>> new_dataset = tf.data.Dataset.load(path)
        >>> for elem in new_dataset:
        ...   print(elem)
        tf.Tensor(0, shape=(), dtype=int64)
        tf.Tensor(1, shape=(), dtype=int64)


        If the default option of sharding the saved dataset was used, the element
        order of the saved dataset will be preserved when loading it.

        The `reader_func` argument can be used to specify a custom order in which
        elements should be loaded from the individual shards. The `reader_func` is
        expected to take a single argument -- a dataset of datasets, each containing
        elements of one of the shards -- and return a dataset of elements. For
        example, the order of shards can be shuffled when loading them as follows:

        ```python
        def custom_reader_func(datasets):
          datasets = datasets.shuffle(NUM_SHARDS)
          return datasets.interleave(lambda x: x, num_parallel_calls=AUTOTUNE)

        dataset = tf.data.Dataset.load(
            path="/path/to/data", ..., reader_func=custom_reader_func)
        ```

        Args:
          path: Required. A path pointing to a previously saved dataset.
          element_spec: Optional. A nested structure of `tf.TypeSpec` objects
            matching the structure of an element of the saved dataset and specifying
            the type of individual element components. If not provided, the nested
            structure of `tf.TypeSpec` saved with the saved dataset is used. Note
            that this argument is required in graph mode.
          compression: Optional. The algorithm to use to decompress the data when
            reading it. Supported options are `GZIP` and `NONE`. Defaults to `NONE`.
          reader_func: Optional. A function to control how to read data from shards.
            If present, the function will be traced and executed as graph
            computation.
          wait: If `True`, for snapshots written with `distributed_save`, it reads
            the snapshot while it is being written. For snapshots written with
            regular `save`, it waits for the snapshot until it's finished. The
            default is `False` for backward compatibility. Users of
            `distributed_save` are recommended to set it to `True`.

        Returns:
          A `tf.data.Dataset` instance.

        Raises:
          FileNotFoundError: If `element_spec` is not specified and the saved nested
            structure of `tf.TypeSpec` can not be located with the saved dataset.
          ValueError: If `element_spec` is not specified and the method is executed
            in graph mode.
        """
        ...
    # PEP 646 could be used here for a more precise type when better supported.
    def map(
        self,
        map_func: Callable[..., _T2],
        num_parallel_calls: int | None = None,
        deterministic: bool | None = None,
        synchronous: bool | None = None,
        use_unbounded_threadpool: bool = False,
        name: str | None = None,
    ) -> Dataset[_T2]:
        """
        Maps `map_func` across the elements of this dataset.

        This transformation applies `map_func` to each element of this dataset, and
        returns a new dataset containing the transformed elements, in the same
        order as they appeared in the input. `map_func` can be used to change both
        the values and the structure of a dataset's elements. Supported structure
        constructs are documented
        [here](https://www.tensorflow.org/guide/data#dataset_structure).

        For example, `map` can be used for adding 1 to each element, or projecting a
        subset of element components.

        >>> dataset = Dataset.range(1, 6)  # ==> [ 1, 2, 3, 4, 5 ]
        >>> dataset = dataset.map(lambda x: x + 1)
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [2, 3, 4, 5, 6]

        The input signature of `map_func` is determined by the structure of each
        element in this dataset.

        >>> dataset = Dataset.range(5)
        >>> # `map_func` takes a single argument of type `tf.Tensor` with the same
        >>> # shape and dtype.
        >>> result = dataset.map(lambda x: x + 1)

        >>> # Each element is a tuple containing two `tf.Tensor` objects.
        >>> elements = [(1, "foo"), (2, "bar"), (3, "baz")]
        >>> dataset = tf.data.Dataset.from_generator(
        ...     lambda: elements, (tf.int32, tf.string))
        >>> # `map_func` takes two arguments of type `tf.Tensor`. This function
        >>> # projects out just the first component.
        >>> result = dataset.map(lambda x_int, y_str: x_int)
        >>> [a.item() for a in result.as_numpy_iterator()]
        [1, 2, 3]

        >>> # Each element is a dictionary mapping strings to `tf.Tensor` objects.
        >>> elements =  ([{"a": 1, "b": "foo"},
        ...               {"a": 2, "b": "bar"},
        ...               {"a": 3, "b": "baz"}])
        >>> dataset = tf.data.Dataset.from_generator(
        ...     lambda: elements, {"a": tf.int32, "b": tf.string})
        >>> # `map_func` takes a single argument of type `dict` with the same keys
        >>> # as the elements.
        >>> result = dataset.map(lambda d: str(d["a"]) + d["b"])

        The value or values returned by `map_func` determine the structure of each
        element in the returned dataset.

        >>> dataset = tf.data.Dataset.range(3)
        >>> # `map_func` returns two `tf.Tensor` objects.
        >>> def g(x):
        ...   return tf.constant(37.0), tf.constant(["Foo", "Bar", "Baz"])
        >>> result = dataset.map(g)
        >>> result.element_spec
        (TensorSpec(shape=(), dtype=tf.float32, name=None), TensorSpec(shape=(3,), dtype=tf.string, name=None))
        >>> # Python primitives, lists, and NumPy arrays are implicitly converted to
        >>> # `tf.Tensor`.
        >>> def h(x):
        ...   return 37.0, ["Foo", "Bar"], np.array([1.0, 2.0], dtype=np.float64)
        >>> result = dataset.map(h)
        >>> result.element_spec
        (TensorSpec(shape=(), dtype=tf.float32, name=None), TensorSpec(shape=(2,), dtype=tf.string, name=None), TensorSpec(shape=(2,), dtype=tf.float64, name=None))
        >>> # `map_func` can return nested structures.
        >>> def i(x):
        ...   return (37.0, [42, 16]), "foo"
        >>> result = dataset.map(i)
        >>> result.element_spec
        ((TensorSpec(shape=(), dtype=tf.float32, name=None),
          TensorSpec(shape=(2,), dtype=tf.int32, name=None)),
         TensorSpec(shape=(), dtype=tf.string, name=None))

        `map_func` can accept as arguments and return any type of dataset element.

        Note that irrespective of the context in which `map_func` is defined (eager
        vs. graph), tf.data traces the function and executes it as a graph. To use
        Python code inside of the function you have a few options:

        1) Rely on AutoGraph to convert Python code into an equivalent graph
        computation. The downside of this approach is that AutoGraph can convert
        some but not all Python code.

        2) Use `tf.py_function`, which allows you to write arbitrary Python code but
        will generally result in worse performance than 1). For example:

        >>> d = tf.data.Dataset.from_tensor_slices(['hello', 'world'])
        >>> # transform a string tensor to upper case string using a Python function
        >>> def upper_case_fn(t: tf.Tensor):
        ...   return t.numpy().decode('utf-8').upper()
        >>> d = d.map(lambda x: tf.py_function(func=upper_case_fn,
        ...           inp=[x], Tout=tf.string))
        >>> list(d.as_numpy_iterator())
        [b'HELLO', b'WORLD']

        3) Use `tf.numpy_function`, which also allows you to write arbitrary
        Python code. Note that `tf.py_function` accepts `tf.Tensor` whereas
        `tf.numpy_function` accepts numpy arrays and returns only numpy arrays.
        For example:

        >>> d = tf.data.Dataset.from_tensor_slices(['hello', 'world'])
        >>> def upper_case_fn(t: np.ndarray):
        ...   return t.decode('utf-8').upper()
        >>> d = d.map(lambda x: tf.numpy_function(func=upper_case_fn,
        ...           inp=[x], Tout=tf.string))
        >>> list(d.as_numpy_iterator())
        [b'HELLO', b'WORLD']

        Note that the use of `tf.numpy_function` and `tf.py_function`
        in general precludes the possibility of executing user-defined
        transformations in parallel (because of Python GIL).

        Performance can often be improved by setting `num_parallel_calls` so that
        `map` will use multiple threads to process elements. If deterministic order
        isn't required, it can also improve performance to set
        `deterministic=False`.

        >>> dataset = Dataset.range(1, 6)  # ==> [ 1, 2, 3, 4, 5 ]
        >>> dataset = dataset.map(lambda x: x + 1,
        ...     num_parallel_calls=tf.data.AUTOTUNE,
        ...     deterministic=False)

        The order of elements yielded by this transformation is deterministic if
        `deterministic=True`. If `map_func` contains stateful operations and
        `num_parallel_calls > 1`, the order in which that state is accessed is
        undefined, so the values of output elements may not be deterministic
        regardless of the `deterministic` flag value.

        Args:
          map_func: A function mapping a dataset element to another dataset element.
          num_parallel_calls: (Optional.) A `tf.int64` scalar `tf.Tensor`,
            representing the number elements to process asynchronously in parallel.
            If the value `tf.data.AUTOTUNE` is used, then the number of parallel
            calls is set dynamically based on available CPU. If not specified, the
            `tf.data.Options.experimental_optimization.map_parallelization` option
            (`True` by default) controls whether the map will run as with
            `tf.data.AUTOTUNE` or run sequentially.
          deterministic: (Optional.) When `num_parallel_calls` is specified, if this
            boolean is specified (`True` or `False`), it controls the order in which
            the transformation produces elements. If set to `False`, the
            transformation is allowed to yield elements out of order to trade
            determinism for performance. If not specified, the
            `tf.data.Options.deterministic` option (`True` by default) controls the
            behavior.
          synchronous: (Optional.) Whether to force the map transformation to run
            synchronously. This only matters when
            `options.experimental_optimization.map_parallelization=True`. That
            option would normally change the map to run with
            `num_parallel_calls=tf.data.AUTOTUNE`, but if `synchronous=True` is
            specified, the map will not be parallelized at all. This is useful for
            saving memory, since even setting `num_parallel_calls=1` will cause one
            batch to be buffered, while with `synchronous=True` the map
            transformation doesn't buffer anything.
          use_unbounded_threadpool: (Optional.) By default, map functions run in a
            limited threadpool based on the number of cores on the machine. This
            efficient for CPU-heavy processing, but if the map function performs IO
            it is better to use an unbounded threadpool by setting it to `True`. It
            is `False` by default.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def options(self) -> Options:
        """
        Returns the options for this dataset and its inputs.

        Returns:
          A `tf.data.Options` object representing the dataset options.
        """
        ...
    def padded_batch(
        self,
        batch_size: ScalarTensorCompatible,
        padded_shapes: ContainerGeneric[tf.TensorShape | TensorCompatible] | None = None,
        padding_values: ContainerGeneric[ScalarTensorCompatible] | None = None,
        drop_remainder: bool = False,
        name: str | None = None,
    ) -> Dataset[_T1_co]:
        """
        Combines consecutive elements of this dataset into padded batches.

        This transformation combines multiple consecutive elements of the input
        dataset into a single element.

        Like `tf.data.Dataset.batch`, the components of the resulting element will
        have an additional outer dimension, which will be `batch_size` (or
        `N % batch_size` for the last element if `batch_size` does not divide the
        number of input elements `N` evenly and `drop_remainder` is `False`). If
        your program depends on the batches having the same outer dimension, you
        should set the `drop_remainder` argument to `True` to prevent the smaller
        batch from being produced.

        Unlike `tf.data.Dataset.batch`, the input elements to be batched may have
        different shapes, and this transformation will pad each component to the
        respective shape in `padded_shapes`. The `padded_shapes` argument
        determines the resulting shape for each dimension of each component in an
        output element:

        * If the dimension is a constant, the component will be padded out to that
          length in that dimension.
        * If the dimension is unknown, the component will be padded out to the
          maximum length of all elements in that dimension.

        >>> A = (tf.data.Dataset
        ...      .range(1, 5, output_type=tf.int32)
        ...      .map(lambda x: tf.fill([x], x)))
        >>> # Pad to the smallest per-batch size that fits all elements.
        >>> B = A.padded_batch(2)
        >>> for element in B.as_numpy_iterator():
        ...   print(element)
        [[1 0]
         [2 2]]
        [[3 3 3 0]
         [4 4 4 4]]
        >>> # Pad to a fixed size.
        >>> C = A.padded_batch(2, padded_shapes=5)
        >>> for element in C.as_numpy_iterator():
        ...   print(element)
        [[1 0 0 0 0]
         [2 2 0 0 0]]
        [[3 3 3 0 0]
         [4 4 4 4 0]]
        >>> # Pad with a custom value.
        >>> D = A.padded_batch(2, padded_shapes=5, padding_values=-1)
        >>> for element in D.as_numpy_iterator():
        ...   print(element)
        [[ 1 -1 -1 -1 -1]
         [ 2  2 -1 -1 -1]]
        [[ 3  3  3 -1 -1]
         [ 4  4  4  4 -1]]
        >>> # Components of nested elements can be padded independently.
        >>> elements = [([1, 2, 3], [10]),
        ...             ([4, 5], [11, 12])]
        >>> dataset = tf.data.Dataset.from_generator(
        ...     lambda: iter(elements), (tf.int32, tf.int32))
        >>> # Pad the first component of the tuple to length 4, and the second
        >>> # component to the smallest size that fits.
        >>> dataset = dataset.padded_batch(2,
        ...     padded_shapes=([4], [None]),
        ...     padding_values=(-1, 100))
        >>> list(dataset.as_numpy_iterator())
        [(array([[ 1,  2,  3, -1], [ 4,  5, -1, -1]], dtype=int32),
          array([[ 10, 100], [ 11,  12]], dtype=int32))]
        >>> # Pad with a single value and multiple components.
        >>> E = tf.data.Dataset.zip((A, A)).padded_batch(2, padding_values=-1)
        >>> for element in E.as_numpy_iterator():
        ...   print(element)
        (array([[ 1, -1],
               [ 2,  2]], dtype=int32), array([[ 1, -1],
               [ 2,  2]], dtype=int32))
        (array([[ 3,  3,  3, -1],
               [ 4,  4,  4,  4]], dtype=int32), array([[ 3,  3,  3, -1],
               [ 4,  4,  4,  4]], dtype=int32))

        See also `tf.data.experimental.dense_to_sparse_batch`, which combines
        elements that may have different shapes into a `tf.sparse.SparseTensor`.

        Args:
          batch_size: A `tf.int64` scalar `tf.Tensor`, representing the number of
            consecutive elements of this dataset to combine in a single batch.
          padded_shapes: (Optional.) A (nested) structure of `tf.TensorShape` or
            `tf.int64` vector tensor-like objects representing the shape to which
            the respective component of each input element should be padded prior
            to batching. Any unknown dimensions will be padded to the maximum size
            of that dimension in each batch. If unset, all dimensions of all
            components are padded to the maximum size in the batch. `padded_shapes`
            must be set if any component has an unknown rank.
          padding_values: (Optional.) A (nested) structure of scalar-shaped
            `tf.Tensor`, representing the padding values to use for the respective
            components. None represents that the (nested) structure should be padded
            with default values.  Defaults are `0` for numeric types and the empty
            string for string types. The `padding_values` should have the same
            (nested) structure as the input dataset. If `padding_values` is a single
            element and the input dataset has multiple components, then the same
            `padding_values` will be used to pad every component of the dataset.
            If `padding_values` is a scalar, then its value will be broadcasted
            to match the shape of each component.
          drop_remainder: (Optional.) A `tf.bool` scalar `tf.Tensor`, representing
            whether the last batch should be dropped in the case it has fewer than
            `batch_size` elements; the default behavior is not to drop the smaller
            batch.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.

        Raises:
          ValueError: If a component has an unknown rank, and the `padded_shapes`
            argument is not set.
          TypeError: If a component is of an unsupported type. The list of supported
            types is documented in
            https://www.tensorflow.org/guide/data#dataset_structure.
        """
        ...
    def prefetch(self, buffer_size: ScalarTensorCompatible, name: str | None = None) -> Dataset[_T1_co]:
        """
        Creates a `Dataset` that prefetches elements from this dataset.

        Most dataset input pipelines should end with a call to `prefetch`. This
        allows later elements to be prepared while the current element is being
        processed. This often improves latency and throughput, at the cost of
        using additional memory to store prefetched elements.

        Note: Like other `Dataset` methods, prefetch operates on the
        elements of the input dataset. It has no concept of examples vs. batches.
        `examples.prefetch(2)` will prefetch two elements (2 examples),
        while `examples.batch(20).prefetch(2)` will prefetch 2 elements
        (2 batches, of 20 examples each).

        >>> dataset = tf.data.Dataset.range(3)
        >>> dataset = dataset.prefetch(2)
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [0, 1, 2]

        Args:
          buffer_size: A `tf.int64` scalar `tf.Tensor`, representing the maximum
            number of elements that will be buffered when prefetching. If the value
            `tf.data.AUTOTUNE` is used, then the buffer size is dynamically tuned.
          name: Optional. A name for the tf.data transformation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def ragged_batch(
        self,
        batch_size: ScalarTensorCompatible,
        drop_remainder: bool = False,
        row_splits_dtype: DType = ...,
        name: str | None = None,
    ) -> Dataset[tf.RaggedTensor]:
        """
        Combines consecutive elements of this dataset into `tf.RaggedTensor`s.

        Like `tf.data.Dataset.batch`, the components of the resulting element will
        have an additional outer dimension, which will be `batch_size` (or
        `N % batch_size` for the last element if `batch_size` does not divide the
        number of input elements `N` evenly and `drop_remainder` is `False`). If
        your program depends on the batches having the same outer dimension, you
        should set the `drop_remainder` argument to `True` to prevent the smaller
        batch from being produced.

        Unlike `tf.data.Dataset.batch`, the input elements to be batched may have
        different shapes:

        *  If an input element is a `tf.Tensor` whose static `tf.TensorShape` is
        fully defined, then it is batched as normal.
        *  If an input element is a `tf.Tensor` whose static `tf.TensorShape`
        contains one or more axes with unknown size (i.e., `shape[i]=None`), then
        the output will contain a `tf.RaggedTensor` that is ragged up to any of such
        dimensions.
        *  If an input element is a `tf.RaggedTensor` or any other type, then it is
        batched as normal.

        Example:

        >>> dataset = tf.data.Dataset.range(6)
        >>> dataset = dataset.map(lambda x: tf.range(x))
        >>> dataset.element_spec.shape
        TensorShape([None])
        >>> dataset = dataset.ragged_batch(2)
        >>> for batch in dataset:
        ...   print(batch)
        <tf.RaggedTensor [[], [0]]>
        <tf.RaggedTensor [[0, 1], [0, 1, 2]]>
        <tf.RaggedTensor [[0, 1, 2, 3], [0, 1, 2, 3, 4]]>

        Args:
          batch_size: A `tf.int64` scalar `tf.Tensor`, representing the number of
            consecutive elements of this dataset to combine in a single batch.
          drop_remainder: (Optional.) A `tf.bool` scalar `tf.Tensor`, representing
            whether the last batch should be dropped in the case it has fewer than
            `batch_size` elements; the default behavior is not to drop the smaller
            batch.
          row_splits_dtype: The dtype that should be used for the `row_splits` of
            any new ragged tensors.  Existing `tf.RaggedTensor` elements do not have
            their row_splits dtype changed.
          name: (Optional.) A string indicating a name for the `tf.data` operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    @staticmethod
    def random(
        seed: int | None = None, rerandomize_each_iteration: bool | None = None, name: str | None = None
    ) -> Dataset[tf.Tensor]:
        """
        Creates a `Dataset` of pseudorandom values.

        The dataset generates a sequence of uniformly distributed integer values.

        `rerandomize_each_iteration` controls whether the sequence of random number
        generated should be re-randomized for each epoch. The default value is False
        where the dataset generates the same sequence of random numbers for each
        epoch.

        >>> ds1 = tf.data.Dataset.random(seed=4).take(10)
        >>> ds2 = tf.data.Dataset.random(seed=4).take(10)
        >>> print(list(ds1.as_numpy_iterator())==list(ds2.as_numpy_iterator()))
        True

        >>> ds3 = tf.data.Dataset.random(seed=4).take(10)
        >>> ds3_first_epoch = list(ds3.as_numpy_iterator())
        >>> ds3_second_epoch = list(ds3.as_numpy_iterator())
        >>> print(ds3_first_epoch == ds3_second_epoch)
        True

        >>> ds4 = tf.data.Dataset.random(
        ...     seed=4, rerandomize_each_iteration=True).take(10)
        >>> ds4_first_epoch = list(ds4.as_numpy_iterator())
        >>> ds4_second_epoch = list(ds4.as_numpy_iterator())
        >>> print(ds4_first_epoch == ds4_second_epoch)
        False

        Args:
          seed: (Optional) If specified, the dataset produces a deterministic
            sequence of values.
          rerandomize_each_iteration: (Optional) If set to False, the dataset
          generates the same sequence of random numbers for each epoch. If set to
          True, it generates a different deterministic sequence of random numbers
          for each epoch. It is defaulted to False if left unspecified.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          Dataset: A `Dataset`.
        """
        ...

    @staticmethod
    @overload
    def range(stop: ScalarTensorCompatible, /, output_type: DType = ..., name: str | None = None) -> Dataset[tf.Tensor]:
        """
        Creates a `Dataset` of a step-separated range of values.

        >>> ds = Dataset.range(5)
        >>> [a.item() for a in ds.as_numpy_iterator()]
        [0, 1, 2, 3, 4]
        >>> ds = Dataset.range(2, 5)
        >>> [a.item() for a in ds.as_numpy_iterator()]
        [2, 3, 4]
        >>> ds = Dataset.range(1, 5, 2)
        >>> [a.item() for a in ds.as_numpy_iterator()]
        [1, 3]
        >>> ds = Dataset.range(1, 5, -2)
        >>> [a.item() for a in ds.as_numpy_iterator()]
        []
        >>> ds = Dataset.range(5, 1)
        >>> [a.item() for a in ds.as_numpy_iterator()]
        []
        >>> ds = Dataset.range(5, 1, -2)
        >>> [a.item() for a in ds.as_numpy_iterator()]
        [5, 3]
        >>> ds = Dataset.range(2, 5, output_type=tf.int32)
        >>> [a.item() for a in ds.as_numpy_iterator()]
        [2, 3, 4]
        >>> ds = Dataset.range(1, 5, 2, output_type=tf.float32)
        >>> [a.item() for a in ds.as_numpy_iterator()]
        [1.0, 3.0]

        Args:
          *args: follows the same semantics as python's range.
            len(args) == 1 -> start = 0, stop = args[0], step = 1.
            len(args) == 2 -> start = args[0], stop = args[1], step = 1.
            len(args) == 3 -> start = args[0], stop = args[1], step = args[2].
          **kwargs:
            - output_type: Its expected dtype. (Optional, default: `tf.int64`).
            - name: (Optional.) A name for the tf.data operation.

        Returns:
          Dataset: A `RangeDataset`.

        Raises:
          ValueError: if len(args) == 0.
        """
        ...
    @staticmethod
    @overload
    def range(
        start: ScalarTensorCompatible,
        stop: ScalarTensorCompatible,
        step: ScalarTensorCompatible = 1,
        /,
        output_type: DType = ...,
        name: str | None = None,
    ) -> Dataset[tf.Tensor]:
        """
        Creates a `Dataset` of a step-separated range of values.

        >>> ds = Dataset.range(5)
        >>> [a.item() for a in ds.as_numpy_iterator()]
        [0, 1, 2, 3, 4]
        >>> ds = Dataset.range(2, 5)
        >>> [a.item() for a in ds.as_numpy_iterator()]
        [2, 3, 4]
        >>> ds = Dataset.range(1, 5, 2)
        >>> [a.item() for a in ds.as_numpy_iterator()]
        [1, 3]
        >>> ds = Dataset.range(1, 5, -2)
        >>> [a.item() for a in ds.as_numpy_iterator()]
        []
        >>> ds = Dataset.range(5, 1)
        >>> [a.item() for a in ds.as_numpy_iterator()]
        []
        >>> ds = Dataset.range(5, 1, -2)
        >>> [a.item() for a in ds.as_numpy_iterator()]
        [5, 3]
        >>> ds = Dataset.range(2, 5, output_type=tf.int32)
        >>> [a.item() for a in ds.as_numpy_iterator()]
        [2, 3, 4]
        >>> ds = Dataset.range(1, 5, 2, output_type=tf.float32)
        >>> [a.item() for a in ds.as_numpy_iterator()]
        [1.0, 3.0]

        Args:
          *args: follows the same semantics as python's range.
            len(args) == 1 -> start = 0, stop = args[0], step = 1.
            len(args) == 2 -> start = args[0], stop = args[1], step = 1.
            len(args) == 3 -> start = args[0], stop = args[1], step = args[2].
          **kwargs:
            - output_type: Its expected dtype. (Optional, default: `tf.int64`).
            - name: (Optional.) A name for the tf.data operation.

        Returns:
          Dataset: A `RangeDataset`.

        Raises:
          ValueError: if len(args) == 0.
        """
        ...

    def rebatch(
        self, batch_size: ScalarTensorCompatible, drop_remainder: bool = False, name: str | None = None
    ) -> Dataset[_T1_co]:
        """
        Creates a `Dataset` that rebatches the elements from this dataset.

        `rebatch(N)` is functionally equivalent to `unbatch().batch(N)`, but is
        more efficient, performing one copy instead of two.

        >>> ds = tf.data.Dataset.range(6)
        >>> ds = ds.batch(2)
        >>> ds = ds.rebatch(3)
        >>> list(ds.as_numpy_iterator())
        [array([0, 1, 2]), array([3, 4, 5])]

        >>> ds = tf.data.Dataset.range(7)
        >>> ds = ds.batch(4)
        >>> ds = ds.rebatch(3)
        >>> list(ds.as_numpy_iterator())
        [array([0, 1, 2]), array([3, 4, 5]), array([6])]

        >>> ds = tf.data.Dataset.range(7)
        >>> ds = ds.batch(2)
        >>> ds = ds.rebatch(3, drop_remainder=True)
        >>> list(ds.as_numpy_iterator())
        [array([0, 1, 2]), array([3, 4, 5])]

        If the `batch_size` argument is a list, `rebatch` cycles through the list
        to determine the size of each batch.

        >>> ds = tf.data.Dataset.range(8)
        >>> ds = ds.batch(4)
        >>> ds = ds.rebatch([2, 1, 1])
        >>> list(ds.as_numpy_iterator())
        [array([0, 1]), array([2]), array([3]), array([4, 5]), array([6]),
        array([7])]

        Args:
          batch_size: A `tf.int64` scalar or vector, representing the size of
            batches to produce. If this argument is a vector, these values are
            cycled through in round robin fashion.
          drop_remainder: (Optional.) A `tf.bool` scalar `tf.Tensor`, representing
            whether the last batch should be dropped in the case it has fewer than
            `batch_size[cycle_index]` elements; the default behavior is not to drop
            the smaller batch.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A `Dataset` of scalar `dtype` elements.
        """
        ...
    def reduce(self, initial_state: _T2, reduce_func: Callable[[_T2, _T1_co], _T2], name: str | None = None) -> _T2:
        """
        Reduces the input dataset to a single element.

        The transformation calls `reduce_func` successively on every element of
        the input dataset until the dataset is exhausted, aggregating information in
        its internal state. The `initial_state` argument is used for the initial
        state and the final state is returned as the result.

        >>> tf.data.Dataset.range(5).reduce(np.int64(0), lambda x, _: x +
        ...   1).numpy().item()
        5
        >>> tf.data.Dataset.range(5).reduce(np.int64(0), lambda x, y: x +
        ...   y).numpy().item()
        10

        Args:
          initial_state: An element representing the initial state of the
            transformation.
          reduce_func: A function that maps `(old_state, input_element)` to
            `new_state`. It must take two arguments and return a new element The
            structure of `new_state` must match the structure of `initial_state`.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A dataset element corresponding to the final state of the transformation.
        """
        ...
    def rejection_resample(
        self,
        class_func: Callable[[_T1_co], ScalarTensorCompatible],
        target_dist: TensorCompatible,
        initial_dist: TensorCompatible | None = None,
        seed: int | None = None,
        name: str | None = None,
    ) -> Dataset[_T1_co]:
        """
        Resamples elements to reach a target distribution.

        Note: This implementation can reject **or repeat** elements in order to
        reach the `target_dist`. So, in some cases, the output `Dataset` may be
        larger than the input `Dataset`.

        >>> initial_dist = [0.6, 0.4]
        >>> n = 1000
        >>> elems = np.random.choice(len(initial_dist), size=n, p=initial_dist)
        >>> dataset = tf.data.Dataset.from_tensor_slices(elems)
        >>> zero, one = np.bincount(list(dataset.as_numpy_iterator())) / n

        Following from `initial_dist`, `zero` is ~0.6 and `one` is ~0.4.

        >>> target_dist = [0.5, 0.5]
        >>> dataset = dataset.rejection_resample(
        ...    class_func=lambda x: x,
        ...    target_dist=target_dist,
        ...    initial_dist=initial_dist)
        >>> dataset = dataset.map(lambda class_func_result, data: data)
        >>> zero, one = np.bincount(list(dataset.as_numpy_iterator())) / n

        Following from `target_dist`, `zero` is ~0.5 and `one` is ~0.5.

        Args:
          class_func: A function mapping an element of the input dataset to a scalar
            `tf.int32` tensor. Values should be in `[0, num_classes)`.
          target_dist: A floating point type tensor, shaped `[num_classes]`.
          initial_dist: (Optional.)  A floating point type tensor, shaped
            `[num_classes]`.  If not provided, the true class distribution is
            estimated live in a streaming fashion.
          seed: (Optional.) Python integer seed for the resampler.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def repeat(self, count: ScalarTensorCompatible | None = None, name: str | None = None) -> Dataset[_T1_co]:
        """
        Repeats this dataset so each original value is seen `count` times.

        >>> dataset = tf.data.Dataset.from_tensor_slices([1, 2, 3])
        >>> dataset = dataset.repeat(3)
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [1, 2, 3, 1, 2, 3, 1, 2, 3]

        Note: If the input dataset depends on global state (e.g. a random number
        generator) or its output is non-deterministic (e.g. because of upstream
        `shuffle`), then different repetitions may produce different elements.

        Args:
          count: (Optional.) A `tf.int64` scalar `tf.Tensor`, representing the
            number of times the dataset should be repeated. The default behavior (if
            `count` is `None` or `-1`) is for the dataset be repeated indefinitely.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    @staticmethod
    def sample_from_datasets(
        datasets: Sequence[Dataset[_T1_co]],
        weights: TensorCompatible | None = None,
        seed: int | None = None,
        stop_on_empty_dataset: bool = False,
        rerandomize_each_iteration: bool | None = None,
    ) -> Dataset[_T1_co]:
        """
        Samples elements at random from the datasets in `datasets`.

        Creates a dataset by interleaving elements of `datasets` with `weight[i]`
        probability of picking an element from dataset `i`. Sampling is done without
        replacement. For example, suppose we have 2 datasets:

        ```python
        dataset1 = tf.data.Dataset.range(0, 3)
        dataset2 = tf.data.Dataset.range(100, 103)
        ```

        Suppose that we sample from these 2 datasets with the following weights:

        ```python
        sample_dataset = tf.data.Dataset.sample_from_datasets(
            [dataset1, dataset2], weights=[0.5, 0.5])
        ```

        One possible outcome of elements in sample_dataset is:

        ```
        print(list(sample_dataset.as_numpy_iterator()))
        # [100, 0, 1, 101, 2, 102]
        ```

        Args:
          datasets: A non-empty list of `tf.data.Dataset` objects with compatible
            structure.
          weights: (Optional.) A list or Tensor of `len(datasets)` floating-point
            values where `weights[i]` represents the probability to sample from
            `datasets[i]`, or a `tf.data.Dataset` object where each element is such
            a list. Defaults to a uniform distribution across `datasets`.
          seed: (Optional.) A `tf.int64` scalar `tf.Tensor`, representing the random
            seed that will be used to create the distribution. See
            `tf.random.set_seed` for behavior.
          stop_on_empty_dataset: If `True`, sampling stops if it encounters an empty
            dataset. If `False`, it continues sampling and skips any empty datasets.
            It is recommended to set it to `True`. Otherwise, the distribution of
            samples starts off as the user intends, but may change as input datasets
            become empty. This can be difficult to detect since the dataset starts
            off looking correct. Default to `False` for backward compatibility.
          rerandomize_each_iteration: An optional `bool`. The boolean argument
          controls whether the sequence of random numbers used to determine which
          dataset to sample from will be rerandomized each epoch. That is, it
          determinies whether datasets will be sampled in the same order across
          different epochs (the default behavior) or not.

        Returns:
          A dataset that interleaves elements from `datasets` at random, according
          to `weights` if provided, otherwise with uniform probability.

        Raises:
          TypeError: If the `datasets` or `weights` arguments have the wrong type.
          ValueError:
            - If `datasets` is empty, or
            - If `weights` is specified and does not match the length of `datasets`.
        """
        ...
    # Incomplete as tf.train.CheckpointOptions not yet covered.
    def save(
        self,
        path: str,
        compression: _CompressionTypes = None,
        shard_func: Callable[[_T1_co], int] | None = None,
        checkpoint_args=None,
    ) -> None:
        """
        Saves the content of the given dataset.

          Example usage:

          >>> import tempfile
          >>> path = os.path.join(tempfile.gettempdir(), "saved_data")
          >>> # Save a dataset
          >>> dataset = tf.data.Dataset.range(2)
          >>> dataset.save(path)
          >>> new_dataset = tf.data.Dataset.load(path)
          >>> for elem in new_dataset:
          ...   print(elem)
          tf.Tensor(0, shape=(), dtype=int64)
          tf.Tensor(1, shape=(), dtype=int64)

          The saved dataset is saved in multiple file "shards". By default, the
          dataset output is divided to shards in a round-robin fashion but custom
          sharding can be specified via the `shard_func` function. For example, you
          can save the dataset to using a single shard as follows:

          ```python
          dataset = make_dataset()
          def custom_shard_func(element):
            return np.int64(0)
          dataset.save(
              path="/path/to/data", ..., shard_func=custom_shard_func)
          ```

          To enable checkpointing, pass in `checkpoint_args` to the `save` method
          as follows:

          ```python
          dataset = tf.data.Dataset.range(100)
          save_dir = "..."
          checkpoint_prefix = "..."
          step_counter = tf.Variable(0, trainable=False)
          checkpoint_args = {
            "checkpoint_interval": 50,
            "step_counter": step_counter,
            "directory": checkpoint_prefix,
            "max_to_keep": 20,
          }
          dataset.save(dataset, save_dir, checkpoint_args=checkpoint_args)
          ```

          NOTE: The directory layout and file format used for saving the dataset is
          considered an implementation detail and may change. For this reason,
          datasets saved through `tf.data.Dataset.save` should only be consumed
          through `tf.data.Dataset.load`, which is guaranteed to be
          backwards compatible.

        Args:
         path: Required. A directory to use for saving the dataset.
         compression: Optional. The algorithm to use to compress data when writing
              it. Supported options are `GZIP` and `NONE`. Defaults to `NONE`.
         shard_func: Optional. A function to control the mapping of dataset
              elements to file shards. The function is expected to map elements of
              the input dataset to int64 shard IDs. If present, the function will be
              traced and executed as graph computation.
         checkpoint_args: Optional args for checkpointing which will be passed into
              the `tf.train.CheckpointManager`. If `checkpoint_args` are not
              specified, then checkpointing will not be performed. The `save()`
              implementation creates a `tf.train.Checkpoint` object internally, so
              users should not set the `checkpoint` argument in `checkpoint_args`.

        Returns:
          An operation which when executed performs the save. When writing
          checkpoints, returns None. The return value is useful in unit tests.

        Raises:
          ValueError if `checkpoint` is passed into `checkpoint_args`.
        """
        ...
    def scan(
        self, initial_state: _T2, scan_func: Callable[[_T2, _T1_co], tuple[_T2, _T3]], name: str | None = None
    ) -> Dataset[_T3]:
        """
        A transformation that scans a function across an input dataset.

        This transformation is a stateful relative of `tf.data.Dataset.map`.
        In addition to mapping `scan_func` across the elements of the input dataset,
        `scan()` accumulates one or more state tensors, whose initial values are
        `initial_state`.

        >>> dataset = tf.data.Dataset.range(10)
        >>> initial_state = tf.constant(0, dtype=tf.int64)
        >>> scan_func = lambda state, i: (state + i, state + i)
        >>> dataset = dataset.scan(initial_state=initial_state, scan_func=scan_func)
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [0, 1, 3, 6, 10, 15, 21, 28, 36, 45]

        Args:
          initial_state: A nested structure of tensors, representing the initial
            state of the accumulator.
          scan_func: A function that maps `(old_state, input_element)` to
            `(new_state, output_element)`. It must take two arguments and return a
            pair of nested structures of tensors. The `new_state` must match the
            structure of `initial_state`.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def shard(
        self, num_shards: ScalarTensorCompatible, index: ScalarTensorCompatible, name: str | None = None
    ) -> Dataset[_T1_co]:
        """
        Creates a `Dataset` that includes only 1/`num_shards` of this dataset.

        `shard` is deterministic. The Dataset produced by `A.shard(n, i)` will
        contain all elements of A whose index mod n = i.

        >>> A = tf.data.Dataset.range(10)
        >>> B = A.shard(num_shards=3, index=0)
        >>> [a.item() for a in B.as_numpy_iterator()]
        [0, 3, 6, 9]
        >>> C = A.shard(num_shards=3, index=1)
        >>> [a.item() for a in C.as_numpy_iterator()]
        [1, 4, 7]
        >>> D = A.shard(num_shards=3, index=2)
        >>> [a.item() for a in D.as_numpy_iterator()]
        [2, 5, 8]

        This dataset operator is very useful when running distributed training, as
        it allows each worker to read a unique subset.

        When reading a single input file, you can shard elements as follows:

        ```python
        d = tf.data.TFRecordDataset(input_file)
        d = d.shard(num_workers, worker_index)
        d = d.repeat(num_epochs)
        d = d.shuffle(shuffle_buffer_size)
        d = d.map(parser_fn, num_parallel_calls=num_map_threads)
        ```

        Important caveats:

        - Be sure to shard before you use any randomizing operator (such as
          shuffle).
        - Generally it is best if the shard operator is used early in the dataset
          pipeline. For example, when reading from a set of TFRecord files, shard
          before converting the dataset to input samples. This avoids reading every
          file on every worker. The following is an example of an efficient
          sharding strategy within a complete pipeline:

        ```python
        d = Dataset.list_files(pattern, shuffle=False)
        d = d.shard(num_workers, worker_index)
        d = d.repeat(num_epochs)
        d = d.shuffle(shuffle_buffer_size)
        d = d.interleave(tf.data.TFRecordDataset,
                         cycle_length=num_readers, block_length=1)
        d = d.map(parser_fn, num_parallel_calls=num_map_threads)
        ```

        Args:
          num_shards: A `tf.int64` scalar `tf.Tensor`, representing the number of
            shards operating in parallel.
          index: A `tf.int64` scalar `tf.Tensor`, representing the worker index.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.

        Raises:
          InvalidArgumentError: if `num_shards` or `index` are illegal values.

            Note: error checking is done on a best-effort basis, and errors aren't
            guaranteed to be caught upon dataset creation. (e.g. providing in a
            placeholder tensor bypasses the early checking, and will instead result
            in an error during a session.run call.)
        """
        ...
    def shuffle(
        self,
        buffer_size: ScalarTensorCompatible,
        seed: int | None = None,
        reshuffle_each_iteration: bool = True,
        name: str | None = None,
    ) -> Dataset[_T1_co]:
        """
        Randomly shuffles the elements of this dataset.

        This dataset fills a buffer with `buffer_size` elements, then randomly
        samples elements from this buffer, replacing the selected elements with new
        elements. For perfect shuffling, a buffer size greater than or equal to the
        full size of the dataset is required.

        For instance, if your dataset contains 10,000 elements but `buffer_size` is
        set to 1,000, then `shuffle` will initially select a random element from
        only the first 1,000 elements in the buffer. Once an element is selected,
        its space in the buffer is replaced by the next (i.e. 1,001-st) element,
        maintaining the 1,000 element buffer.

        `reshuffle_each_iteration` controls whether the shuffle order should be
        different for each epoch. However you should avoid using
        `shuffle(reshuffle_each_iteration=True)`, then `take` and `skip` to split
        a dataset into training and test sets, which would lead to data leakage (as
        the entire dataset would be re-shuffled then re-split after each epoch).
        Please use the `tf.keras.utils.split_dataset` method instead. In TF 1.X,
        the idiomatic way to create epochs was through the `repeat` transformation:

        ```python
        dataset = tf.data.Dataset.range(3)
        dataset = dataset.shuffle(3, reshuffle_each_iteration=True)
        dataset = dataset.repeat(2)
        # [1, 0, 2, 1, 2, 0]

        dataset = tf.data.Dataset.range(3)
        dataset = dataset.shuffle(3, reshuffle_each_iteration=False)
        dataset = dataset.repeat(2)
        # [1, 0, 2, 1, 0, 2]
        ```

        In TF 2.0, `tf.data.Dataset` objects are Python iterables which makes it
        possible to also create epochs through Python iteration:

        ```python
        dataset = tf.data.Dataset.range(3)
        dataset = dataset.shuffle(3, reshuffle_each_iteration=True)
        list(dataset.as_numpy_iterator())
        # [1, 0, 2]
        list(dataset.as_numpy_iterator())
        # [1, 2, 0]
        ```

        ```python
        dataset = tf.data.Dataset.range(3)
        dataset = dataset.shuffle(3, reshuffle_each_iteration=False)
        list(dataset.as_numpy_iterator())
        # [1, 0, 2]
        list(dataset.as_numpy_iterator())
        # [1, 0, 2]
        ```

        #### Fully shuffling all the data

        To shuffle an entire dataset, set `buffer_size=dataset.cardinality()`. This
        is equivalent to setting the `buffer_size` equal to the number of elements
        in the dataset, resulting in uniform shuffle.

        Note: `shuffle(dataset.cardinality())` loads the full dataset into memory so
        that it can be shuffled. This will cause a memory overflow (OOM) error if
        the dataset is too large, so full-shuffle should only be used for datasets
        that are known to fit in the memory, such as datasets of filenames or other
        small datasets.

        ```python
        dataset = tf.data.Dataset.range(20)
        dataset = dataset.shuffle(dataset.cardinality())
        # [18, 4, 9, 2, 17, 8, 5, 10, 0, 6, 16, 3, 19, 7, 14, 11, 15, 13, 12, 1]
        ```

        Args:
          buffer_size: An int or `tf.int64` scalar `tf.Tensor`, representing the
            number of elements from this dataset from which the new dataset will
            sample. To uniformly shuffle the entire dataset, use
            `buffer_size=dataset.cardinality()`.
          seed: (Optional.) An int or `tf.int64` scalar `tf.Tensor`, representing
            the random seed that will be used to create the distribution. See
            `tf.random.set_seed` for behavior.
          reshuffle_each_iteration: (Optional.) A boolean, which if true indicates
            that the dataset should be pseudorandomly reshuffled each time it is
            iterated over. (Defaults to `True`.)
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def skip(self, count: ScalarTensorCompatible, name: str | None = None) -> Dataset[_T1_co]:
        """
        Creates a `Dataset` that skips `count` elements from this dataset.

        >>> dataset = tf.data.Dataset.range(10)
        >>> dataset = dataset.skip(7)
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [7, 8, 9]

        Args:
          count: A `tf.int64` scalar `tf.Tensor`, representing the number of
            elements of this dataset that should be skipped to form the new dataset.
            If `count` is greater than the size of this dataset, the new dataset
            will contain no elements.  If `count` is -1, skips the entire dataset.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def snapshot(
        self,
        path: str,
        compression: _CompressionTypes = "AUTO",
        reader_func: Callable[[Dataset[Dataset[_T1_co]]], Dataset[_T1_co]] | None = None,
        shard_func: Callable[[_T1_co], ScalarTensorCompatible] | None = None,
        name: str | None = None,
    ) -> Dataset[_T1_co]:
        """
        API to persist the output of the input dataset.

        The snapshot API allows users to transparently persist the output of their
        preprocessing pipeline to disk, and materialize the pre-processed data on a
        different training run.

        This API enables repeated preprocessing steps to be consolidated, and allows
        re-use of already processed data, trading off disk storage and network
        bandwidth for freeing up more valuable CPU resources and accelerator compute
        time.

        https://github.com/tensorflow/community/blob/master/rfcs/20200107-tf-data-snapshot.md
        has detailed design documentation of this feature.

        Users can specify various options to control the behavior of snapshot,
        including how snapshots are read from and written to by passing in
        user-defined functions to the `reader_func` and `shard_func` parameters.

        `shard_func` is a user specified function that maps input elements to
        snapshot shards.

        Users may want to specify this function to control how snapshot files should
        be written to disk. Below is an example of how a potential `shard_func`
        could be written.

        ```python
        dataset = ...
        dataset = dataset.enumerate()
        dataset = dataset.snapshot("/path/to/snapshot/dir",
            shard_func=lambda x, y: x % NUM_SHARDS, ...)
        dataset = dataset.map(lambda x, y: y)
        ```

        `reader_func` is a user specified function that accepts a single argument:
        (1) a Dataset of Datasets, each representing a "split" of elements of the
        original dataset. The cardinality of the input dataset matches the
        number of the shards specified in the `shard_func` (see above). The function
        should return a Dataset of elements of the original dataset.

        Users may want specify this function to control how snapshot files should be
        read from disk, including the amount of shuffling and parallelism.

        Here is an example of a standard reader function a user can define. This
        function enables both dataset shuffling and parallel reading of datasets:

        ```python
        def user_reader_func(datasets):
          # shuffle the datasets splits
          datasets = datasets.shuffle(NUM_CORES)
          # read datasets in parallel and interleave their elements
          return datasets.interleave(lambda x: x, num_parallel_calls=AUTOTUNE)

        dataset = dataset.snapshot("/path/to/snapshot/dir",
            reader_func=user_reader_func)
        ```

        By default, snapshot parallelizes reads by the number of cores available on
        the system, but will not attempt to shuffle the data.

        Args:
          path: Required. A directory to use for storing / loading the snapshot to /
            from.
          compression: Optional. The type of compression to apply to the snapshot
            written to disk. Supported options are `GZIP`, `SNAPPY`, `AUTO` or None.
            Defaults to `AUTO`, which attempts to pick an appropriate compression
            algorithm for the dataset.
          reader_func: Optional. A function to control how to read data from
            snapshot shards.
          shard_func: Optional. A function to control how to shard data when writing
            a snapshot.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def sparse_batch(
        self, batch_size: ScalarTensorCompatible, row_shape: tf.TensorShape | TensorCompatible, name: str | None = None
    ) -> Dataset[tf.SparseTensor]:
        """
        Combines consecutive elements into `tf.sparse.SparseTensor`s.

        Like `Dataset.padded_batch()`, this transformation combines multiple
        consecutive elements of the dataset, which might have different
        shapes, into a single element. The resulting element has three
        components (`indices`, `values`, and `dense_shape`), which
        comprise a `tf.sparse.SparseTensor` that represents the same data. The
        `row_shape` represents the dense shape of each row in the
        resulting `tf.sparse.SparseTensor`, to which the effective batch size is
        prepended. For example:

        ```python
        # NOTE: The following examples use `{ ... }` to represent the
        # contents of a dataset.
        a = { ['a', 'b', 'c'], ['a', 'b'], ['a', 'b', 'c', 'd'] }

        a.apply(tf.data.experimental.dense_to_sparse_batch(
            batch_size=2, row_shape=[6])) ==
        {
            ([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1]],  # indices
             ['a', 'b', 'c', 'a', 'b'],                 # values
             [2, 6]),                                   # dense_shape
            ([[0, 0], [0, 1], [0, 2], [0, 3]],
             ['a', 'b', 'c', 'd'],
             [1, 6])
        }
        ```

        Args:
          batch_size: A `tf.int64` scalar `tf.Tensor`, representing the number of
            consecutive elements of this dataset to combine in a single batch.
          row_shape: A `tf.TensorShape` or `tf.int64` vector tensor-like object
            representing the equivalent dense shape of a row in the resulting
            `tf.sparse.SparseTensor`. Each element of this dataset must have the
            same rank as `row_shape`, and must have size less than or equal to
            `row_shape` in each dimension.
          name: (Optional.) A string indicating a name for the `tf.data` operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def take(self, count: ScalarTensorCompatible, name: str | None = None) -> Dataset[_T1_co]:
        """
        Creates a `Dataset` with at most `count` elements from this dataset.

        >>> dataset = tf.data.Dataset.range(10)
        >>> dataset = dataset.take(3)
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [0, 1, 2]

        Args:
          count: A `tf.int64` scalar `tf.Tensor`, representing the number of
            elements of this dataset that should be taken to form the new dataset.
            If `count` is -1, or if `count` is greater than the size of this
            dataset, the new dataset will contain all elements of this dataset.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def take_while(self, predicate: Callable[[_T1_co], ScalarTensorCompatible], name: str | None = None) -> Dataset[_T1_co]:
        """
        A transformation that stops dataset iteration based on a `predicate`.

        >>> dataset = tf.data.Dataset.range(10)
        >>> dataset = dataset.take_while(lambda x: x < 5)
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [0, 1, 2, 3, 4]

        Args:
          predicate: A function that maps a nested structure of tensors (having
            shapes and types defined by `self.output_shapes` and
            `self.output_types`) to a scalar `tf.bool` tensor.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def unbatch(self, name: str | None = None) -> Dataset[_T1_co]:
        """
        Splits elements of a dataset into multiple elements.

        For example, if elements of the dataset are shaped `[B, a0, a1, ...]`,
        where `B` may vary for each input element, then for each element in the
        dataset, the unbatched dataset will contain `B` consecutive elements
        of shape `[a0, a1, ...]`.

        >>> elements = [ [1, 2, 3], [1, 2], [1, 2, 3, 4] ]
        >>> dataset = tf.data.Dataset.from_generator(lambda: elements, tf.int64)
        >>> dataset = dataset.unbatch()
        >>> [a.item() for a in dataset.as_numpy_iterator()]
        [1, 2, 3, 1, 2, 1, 2, 3, 4]

        Note: `unbatch` requires a data copy to slice up the batched tensor into
        smaller, unbatched tensors. When optimizing performance, try to avoid
        unnecessary usage of `unbatch`.

        Args:
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def unique(self, name: str | None = None) -> Dataset[_T1_co]:
        """
        A transformation that discards duplicate elements of a `Dataset`.

        Use this transformation to produce a dataset that contains one instance of
        each unique element in the input. For example:

        >>> dataset = tf.data.Dataset.from_tensor_slices([1, 37, 2, 37, 2, 1])
        >>> dataset = dataset.unique()
        >>> sorted([a.item() for a in dataset.as_numpy_iterator()])
        [1, 2, 37]

        Note: This transformation only supports datasets which fit into memory
        and have elements of either `tf.int32`, `tf.int64` or `tf.string` type.

        Args:
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def window(
        self,
        size: ScalarTensorCompatible,
        shift: ScalarTensorCompatible | None = None,
        stride: ScalarTensorCompatible = 1,
        drop_remainder: bool = False,
        name: str | None = None,
    ) -> Dataset[Dataset[_T1_co]]:
        """
        Returns a dataset of "windows".

        Each "window" is a dataset that contains a subset of elements of the
        input dataset. These are finite datasets of size `size` (or possibly fewer
        if there are not enough input elements to fill the window and
        `drop_remainder` evaluates to `False`).

        For example:

        >>> dataset = tf.data.Dataset.range(7).window(3)
        >>> for window in dataset:
        ...   print(window)
        <...Dataset element_spec=TensorSpec(shape=(), dtype=tf.int64, name=None)>
        <...Dataset element_spec=TensorSpec(shape=(), dtype=tf.int64, name=None)>
        <...Dataset element_spec=TensorSpec(shape=(), dtype=tf.int64, name=None)>

        Since windows are datasets, they can be iterated over:

        >>> for window in dataset:
        ...   print([a.item() for a in window.as_numpy_iterator()])
        [0, 1, 2]
        [3, 4, 5]
        [6]

        #### Shift

        The `shift` argument determines the number of input elements to shift
        between the start of each window. If windows and elements are both numbered
        starting at 0, the first element in window `k` will be element `k * shift`
        of the input dataset. In particular, the first element of the first window
        will always be the first element of the input dataset.

        >>> dataset = tf.data.Dataset.range(7).window(3, shift=1,
        ...                                           drop_remainder=True)
        >>> for window in dataset:
        ...   print([a.item() for a in window.as_numpy_iterator()])
        [0, 1, 2]
        [1, 2, 3]
        [2, 3, 4]
        [3, 4, 5]
        [4, 5, 6]

        #### Stride

        The `stride` argument determines the stride between input elements within a
        window.

        >>> dataset = tf.data.Dataset.range(7).window(3, shift=1, stride=2,
        ...                                           drop_remainder=True)
        >>> for window in dataset:
        ...   print([a.item() for a in window.as_numpy_iterator()])
        [0, 2, 4]
        [1, 3, 5]
        [2, 4, 6]

        #### Nested elements

        When the `window` transformation is applied to a dataset whos elements are
        nested structures, it produces a dataset where the elements have the same
        nested structure but each leaf is replaced by a window. In other words,
        the nesting is applied outside of the windows as opposed inside of them.

        The type signature is:

        ```
        def window(
            self: Dataset[Nest[T]], ...
        ) -> Dataset[Nest[Dataset[T]]]
        ```

        Applying `window` to a `Dataset` of tuples gives a tuple of windows:

        >>> dataset = tf.data.Dataset.from_tensor_slices(([1, 2, 3, 4, 5],
        ...                                               [6, 7, 8, 9, 10]))
        >>> dataset = dataset.window(2)
        >>> windows = next(iter(dataset))
        >>> windows
        (<...Dataset element_spec=TensorSpec(shape=(), dtype=tf.int32, name=None)>,
         <...Dataset element_spec=TensorSpec(shape=(), dtype=tf.int32, name=None)>)

        >>> def to_numpy(ds):
        ...   return [a.item() for a in ds.as_numpy_iterator()]
        >>>
        >>> for windows in dataset:
        ...   print(to_numpy(windows[0]), to_numpy(windows[1]))
        [1, 2] [6, 7]
        [3, 4] [8, 9]
        [5] [10]

        Applying `window` to a `Dataset` of dictionaries gives a dictionary of
        `Datasets`:

        >>> dataset = tf.data.Dataset.from_tensor_slices({'a': [1, 2, 3],
        ...                                               'b': [4, 5, 6],
        ...                                               'c': [7, 8, 9]})
        >>> dataset = dataset.window(2)
        >>> def to_numpy(ds):
        ...   return [a.item() for a in ds.as_numpy_iterator()]
        >>>
        >>> for windows in dataset:
        ...   print(tf.nest.map_structure(to_numpy, windows))
        {'a': [1, 2], 'b': [4, 5], 'c': [7, 8]}
        {'a': [3], 'b': [6], 'c': [9]}

        #### Flatten a dataset of windows

        The `Dataset.flat_map` and `Dataset.interleave` methods can be used to
        flatten a dataset of windows into a single dataset.

        The argument to `flat_map` is a function that takes an element from the
        dataset and returns a `Dataset`. `flat_map` chains together the resulting
        datasets sequentially.

        For example, to turn each window into a dense tensor:

        >>> dataset = tf.data.Dataset.range(7).window(3, shift=1,
        ...                                           drop_remainder=True)
        >>> batched = dataset.flat_map(lambda x:x.batch(3))
        >>> for batch in batched:
        ...   print(batch.numpy())
        [0 1 2]
        [1 2 3]
        [2 3 4]
        [3 4 5]
        [4 5 6]

        Args:
          size: A `tf.int64` scalar `tf.Tensor`, representing the number of elements
            of the input dataset to combine into a window. Must be positive.
          shift: (Optional.) A `tf.int64` scalar `tf.Tensor`, representing the
            number of input elements by which the window moves in each iteration.
            Defaults to `size`. Must be positive.
          stride: (Optional.) A `tf.int64` scalar `tf.Tensor`, representing the
            stride of the input elements in the sliding window. Must be positive.
            The default value of 1 means "retain every input element".
          drop_remainder: (Optional.) A `tf.bool` scalar `tf.Tensor`, representing
            whether the last windows should be dropped if their size is smaller than
            `size`.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    def with_options(self, options: Options, name: str | None = None) -> Dataset[_T1_co]:
        """
        Returns a new `tf.data.Dataset` with the given options set.

        The options are "global" in the sense they apply to the entire dataset.
        If options are set multiple times, they are merged as long as different
        options do not use different non-default values.

        >>> ds = tf.data.Dataset.range(5)
        >>> ds = ds.interleave(lambda x: tf.data.Dataset.range(5),
        ...                    cycle_length=3,
        ...                    num_parallel_calls=3)
        >>> options = tf.data.Options()
        >>> # This will make the interleave order non-deterministic.
        >>> options.deterministic = False
        >>> ds = ds.with_options(options)

        Args:
          options: A `tf.data.Options` that identifies the options the use.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.

        Raises:
          ValueError: when an option is set more than once to a non-default value
        """
        ...

    @overload
    @staticmethod
    def zip(
        *args: Dataset[Any] | Collection[Dataset[Any]] | ContainerGeneric[Dataset[Any]], name: str | None = None
    ) -> Dataset[tuple[Any, ...]]:
        """
        Creates a `Dataset` by zipping together the given datasets.

        This method has similar semantics to the built-in `zip()` function
        in Python, with the main difference being that the `datasets`
        argument can be a (nested) structure of `Dataset` objects. The supported
        nesting mechanisms are documented
        [here] (https://www.tensorflow.org/guide/data#dataset_structure).

        >>> # The datasets or nested structure of datasets `*args` argument
        >>> # determines the structure of elements in the resulting dataset.
        >>> a = tf.data.Dataset.range(1, 4)  # ==> [ 1, 2, 3 ]
        >>> b = tf.data.Dataset.range(4, 7)  # ==> [ 4, 5, 6 ]
        >>> ds = tf.data.Dataset.zip(a, b)
        >>> [(i.item(), j.item()) for i, j in ds.as_numpy_iterator()]
        [(1, 4), (2, 5), (3, 6)]
        >>> ds = tf.data.Dataset.zip(b, a)
        >>> [(i.item(), j.item()) for i, j in ds.as_numpy_iterator()]
        [(4, 1), (5, 2), (6, 3)]
        >>>
        >>> # The `datasets` argument may contain an arbitrary number of datasets.
        >>> c = tf.data.Dataset.range(7, 13).batch(2)  # ==> [ [7, 8],
        ...                                            #       [9, 10],
        ...                                            #       [11, 12] ]
        >>> ds = tf.data.Dataset.zip(a, b, c)
        >>> for i, j, k in ds.as_numpy_iterator():
        ...   print(i.item(), j.item(), k)
        1 4 [7 8]
        2 5 [ 9 10]
        3 6 [11 12]
        >>>
        >>> # The number of elements in the resulting dataset is the same as
        >>> # the size of the smallest dataset in `datasets`.
        >>> d = tf.data.Dataset.range(13, 15)  # ==> [ 13, 14 ]
        >>> ds = tf.data.Dataset.zip(a, d)
        >>> [(i.item(), j.item()) for i, j in ds.as_numpy_iterator()]
        [(1, 13), (2, 14)]

        Args:
          *args: Datasets or nested structures of datasets to zip together. This
            can't be set if `datasets` is set.
          datasets: A (nested) structure of datasets. This can't be set if `*args`
            is set. Note that this exists only for backwards compatibility and it is
            preferred to use *args.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    @overload
    @staticmethod
    def zip(*args: Unpack[tuple[Dataset[_T2], Dataset[_T3]]], name: str | None = None) -> Dataset[tuple[_T2, _T3]]:
        """
        Creates a `Dataset` by zipping together the given datasets.

        This method has similar semantics to the built-in `zip()` function
        in Python, with the main difference being that the `datasets`
        argument can be a (nested) structure of `Dataset` objects. The supported
        nesting mechanisms are documented
        [here] (https://www.tensorflow.org/guide/data#dataset_structure).

        >>> # The datasets or nested structure of datasets `*args` argument
        >>> # determines the structure of elements in the resulting dataset.
        >>> a = tf.data.Dataset.range(1, 4)  # ==> [ 1, 2, 3 ]
        >>> b = tf.data.Dataset.range(4, 7)  # ==> [ 4, 5, 6 ]
        >>> ds = tf.data.Dataset.zip(a, b)
        >>> [(i.item(), j.item()) for i, j in ds.as_numpy_iterator()]
        [(1, 4), (2, 5), (3, 6)]
        >>> ds = tf.data.Dataset.zip(b, a)
        >>> [(i.item(), j.item()) for i, j in ds.as_numpy_iterator()]
        [(4, 1), (5, 2), (6, 3)]
        >>>
        >>> # The `datasets` argument may contain an arbitrary number of datasets.
        >>> c = tf.data.Dataset.range(7, 13).batch(2)  # ==> [ [7, 8],
        ...                                            #       [9, 10],
        ...                                            #       [11, 12] ]
        >>> ds = tf.data.Dataset.zip(a, b, c)
        >>> for i, j, k in ds.as_numpy_iterator():
        ...   print(i.item(), j.item(), k)
        1 4 [7 8]
        2 5 [ 9 10]
        3 6 [11 12]
        >>>
        >>> # The number of elements in the resulting dataset is the same as
        >>> # the size of the smallest dataset in `datasets`.
        >>> d = tf.data.Dataset.range(13, 15)  # ==> [ 13, 14 ]
        >>> ds = tf.data.Dataset.zip(a, d)
        >>> [(i.item(), j.item()) for i, j in ds.as_numpy_iterator()]
        [(1, 13), (2, 14)]

        Args:
          *args: Datasets or nested structures of datasets to zip together. This
            can't be set if `datasets` is set.
          datasets: A (nested) structure of datasets. This can't be set if `*args`
            is set. Note that this exists only for backwards compatibility and it is
            preferred to use *args.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...
    @overload
    @staticmethod
    def zip(
        *, datasets: tuple[Dataset[_T2], Dataset[_T3]] | None = None, name: str | None = None
    ) -> Dataset[tuple[_T2, _T3]]:
        """
        Creates a `Dataset` by zipping together the given datasets.

        This method has similar semantics to the built-in `zip()` function
        in Python, with the main difference being that the `datasets`
        argument can be a (nested) structure of `Dataset` objects. The supported
        nesting mechanisms are documented
        [here] (https://www.tensorflow.org/guide/data#dataset_structure).

        >>> # The datasets or nested structure of datasets `*args` argument
        >>> # determines the structure of elements in the resulting dataset.
        >>> a = tf.data.Dataset.range(1, 4)  # ==> [ 1, 2, 3 ]
        >>> b = tf.data.Dataset.range(4, 7)  # ==> [ 4, 5, 6 ]
        >>> ds = tf.data.Dataset.zip(a, b)
        >>> [(i.item(), j.item()) for i, j in ds.as_numpy_iterator()]
        [(1, 4), (2, 5), (3, 6)]
        >>> ds = tf.data.Dataset.zip(b, a)
        >>> [(i.item(), j.item()) for i, j in ds.as_numpy_iterator()]
        [(4, 1), (5, 2), (6, 3)]
        >>>
        >>> # The `datasets` argument may contain an arbitrary number of datasets.
        >>> c = tf.data.Dataset.range(7, 13).batch(2)  # ==> [ [7, 8],
        ...                                            #       [9, 10],
        ...                                            #       [11, 12] ]
        >>> ds = tf.data.Dataset.zip(a, b, c)
        >>> for i, j, k in ds.as_numpy_iterator():
        ...   print(i.item(), j.item(), k)
        1 4 [7 8]
        2 5 [ 9 10]
        3 6 [11 12]
        >>>
        >>> # The number of elements in the resulting dataset is the same as
        >>> # the size of the smallest dataset in `datasets`.
        >>> d = tf.data.Dataset.range(13, 15)  # ==> [ 13, 14 ]
        >>> ds = tf.data.Dataset.zip(a, d)
        >>> [(i.item(), j.item()) for i, j in ds.as_numpy_iterator()]
        [(1, 13), (2, 14)]

        Args:
          *args: Datasets or nested structures of datasets to zip together. This
            can't be set if `datasets` is set.
          datasets: A (nested) structure of datasets. This can't be set if `*args`
            is set. Note that this exists only for backwards compatibility and it is
            preferred to use *args.
          name: (Optional.) A name for the tf.data operation.

        Returns:
          A new `Dataset` with the transformation applied as described above.
        """
        ...

    def __len__(self) -> int:
        """
        Returns the length of the dataset if it is known and finite.

        This method requires that you are running in eager mode, and that the
        length of the dataset is known and non-infinite. When the length may be
        unknown or infinite, or if you are running in graph mode, use
        `tf.data.Dataset.cardinality` instead.

        Returns:
          An integer representing the length of the dataset.

        Raises:
          RuntimeError: If the dataset length is unknown or infinite, or if eager
            execution is not enabled.
        """
        ...
    def __nonzero__(self) -> bool: ...
    def __getattr__(self, name: str) -> Incomplete: ...

class Options:
    """
    Represents options for `tf.data.Dataset`.

    A `tf.data.Options` object can be, for instance, used to control which static
    optimizations to apply to the input pipeline graph or whether to use
    performance modeling to dynamically tune the parallelism of operations such as
    `tf.data.Dataset.map` or `tf.data.Dataset.interleave`.

    The options are set for the entire dataset and are carried over to datasets
    created through tf.data transformations.

    The options can be set by constructing an `Options` object and using the
    `tf.data.Dataset.with_options(options)` transformation, which returns a
    dataset with the options set.

    >>> dataset = tf.data.Dataset.range(42)
    >>> options = tf.data.Options()
    >>> options.deterministic = False
    >>> dataset = dataset.with_options(options)
    >>> print(dataset.options().deterministic)
    False

    Note: A known limitation of the `tf.data.Options` implementation is that the
    options are not preserved across tf.function boundaries. In particular, to
    set options for a dataset that is iterated within a tf.function, the options
    need to be set within the same tf.function.
    """
    autotune: Incomplete
    deterministic: bool
    experimental_deterministic: bool
    experimental_distribute: Incomplete
    experimental_external_state_policy: Incomplete
    experimental_optimization: Incomplete
    experimental_slack: bool
    experimental_symbolic_checkpoint: bool
    experimental_threading: Incomplete
    threading: Incomplete
    def merge(self, options: Options) -> Self:
        """
        Merges itself with the given `tf.data.Options`.

        If this object and the `options` to merge set an option differently, a
        warning is generated and this object's value is updated with the `options`
        object's value.

        Args:
          options: The `tf.data.Options` to merge with.

        Returns:
          New `tf.data.Options` object which is the result of merging self with
          the input `tf.data.Options`.
        """
        ...

class TFRecordDataset(Dataset[tf.Tensor]):
    """
    A `Dataset` comprising records from one or more TFRecord files.

    This dataset loads TFRecords from the files as bytes, exactly as they were
    written.`TFRecordDataset` does not do any parsing or decoding on its own.
    Parsing and decoding can be done by applying `Dataset.map` transformations
    after the `TFRecordDataset`.

    A minimal example is given below:

    >>> import tempfile
    >>> example_path = os.path.join(tempfile.gettempdir(), "example.tfrecords")
    >>> np.random.seed(0)

    >>> # Write the records to a file.
    ... with tf.io.TFRecordWriter(example_path) as file_writer:
    ...   for _ in range(4):
    ...     x, y = np.random.random(), np.random.random()
    ...
    ...     record_bytes = tf.train.Example(features=tf.train.Features(feature={
    ...         "x": tf.train.Feature(float_list=tf.train.FloatList(value=[x])),
    ...         "y": tf.train.Feature(float_list=tf.train.FloatList(value=[y])),
    ...     })).SerializeToString()
    ...     file_writer.write(record_bytes)

    >>> # Read the data back out.
    >>> def decode_fn(record_bytes):
    ...   return tf.io.parse_single_example(
    ...       # Data
    ...       record_bytes,
    ...
    ...       # Schema
    ...       {"x": tf.io.FixedLenFeature([], dtype=tf.float32),
    ...        "y": tf.io.FixedLenFeature([], dtype=tf.float32)}
    ...   )

    >>> for batch in tf.data.TFRecordDataset([example_path]).map(decode_fn):
    ...   print("x = {x:.4f},  y = {y:.4f}".format(**batch))
    x = 0.5488,  y = 0.7152
    x = 0.6028,  y = 0.5449
    x = 0.4237,  y = 0.6459
    x = 0.4376,  y = 0.8918
    """
    def __init__(
        self,
        filenames: TensorCompatible | Dataset[str],
        compression_type: _CompressionTypes = None,
        buffer_size: int | None = None,
        num_parallel_reads: int | None = None,
        name: str | None = None,
    ) -> None:
        """
        Creates a `TFRecordDataset` to read one or more TFRecord files.

        Each element of the dataset will contain a single TFRecord.

        Args:
          filenames: A `tf.string` tensor or `tf.data.Dataset` containing one or
            more filenames.
          compression_type: (Optional.) A `tf.string` scalar evaluating to one of
            `""` (no compression), `"ZLIB"`, or `"GZIP"`.
          buffer_size: (Optional.) A `tf.int64` scalar representing the number of
            bytes in the read buffer. If your input pipeline is I/O bottlenecked,
            consider setting this parameter to a value 1-100 MBs. If `None`, a
            sensible default for both local and remote file systems is used.
          num_parallel_reads: (Optional.) A `tf.int64` scalar representing the
            number of files to read in parallel. If greater than one, the records of
            files read in parallel are outputted in an interleaved order. If your
            input pipeline is I/O bottlenecked, consider setting this parameter to a
            value greater than one to parallelize the I/O. If `None`, files will be
            read sequentially.
          name: (Optional.) A name for the tf.data operation.

        Raises:
          TypeError: If any argument does not have the expected type.
          ValueError: If any argument does not have the expected shape.
        """
        ...
    @property
    def element_spec(self) -> tf.TensorSpec: ...

def __getattr__(name: str): ...  # incomplete module

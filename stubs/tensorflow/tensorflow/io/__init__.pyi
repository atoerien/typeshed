"""Public API for tf._api.v2.io namespace"""

from collections.abc import Iterable, Mapping
from types import TracebackType
from typing import Literal, NamedTuple, TypeAlias
from typing_extensions import Self

from tensorflow._aliases import DTypeLike, ShapeLike, TensorCompatible, TensorLike
from tensorflow.io import gfile as gfile

_FeatureSpecs: TypeAlias = Mapping[str, FixedLenFeature | FixedLenSequenceFeature | VarLenFeature | RaggedFeature | SparseFeature]

_CompressionTypes: TypeAlias = Literal["ZLIB", "GZIP", "AUTO", "", 0, 1, 2] | None
_CompressionLevels: TypeAlias = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] | None
_MemoryLevels: TypeAlias = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9] | None

class TFRecordOptions:
    """Options used for manipulating TFRecord files."""
    compression_type: _CompressionTypes | TFRecordOptions
    flush_mode: int | None  # The exact values allowed comes from zlib
    input_buffer_size: int | None
    output_buffer_size: int | None
    window_bits: int | None
    compression_level: _CompressionLevels
    compression_method: str | None
    mem_level: _MemoryLevels
    compression_strategy: int | None  # The exact values allowed comes from zlib

    def __init__(
        self,
        compression_type: _CompressionTypes | TFRecordOptions = None,
        flush_mode: int | None = None,
        input_buffer_size: int | None = None,
        output_buffer_size: int | None = None,
        window_bits: int | None = None,
        compression_level: _CompressionLevels = None,
        compression_method: str | None = None,
        mem_level: _MemoryLevels = None,
        compression_strategy: int | None = None,
    ) -> None:
        """
        Creates a `TFRecordOptions` instance.

        Options only effect TFRecordWriter when compression_type is not `None`.
        Documentation, details, and defaults can be found in
        [`zlib_compression_options.h`](https://www.tensorflow.org/code/tensorflow/core/lib/io/zlib_compression_options.h)
        and in the [zlib manual](http://www.zlib.net/manual.html).
        Leaving an option as `None` allows C++ to set a reasonable default.

        Args:
          compression_type: `"GZIP"`, `"ZLIB"`, or `""` (no compression).
          flush_mode: flush mode or `None`, Default: Z_NO_FLUSH.
          input_buffer_size: int or `None`.
          output_buffer_size: int or `None`.
          window_bits: int or `None`.
          compression_level: 0 to 9, or `None`.
          compression_method: compression method or `None`.
          mem_level: 1 to 9, or `None`.
          compression_strategy: strategy or `None`. Default: Z_DEFAULT_STRATEGY.

        Returns:
          A `TFRecordOptions` object.

        Raises:
          ValueError: If compression_type is invalid.
        """
        ...
    @classmethod
    def get_compression_type_string(cls, options: _CompressionTypes | TFRecordOptions) -> str:
        """
        Convert various option types to a unified string.

        Args:
          options: `TFRecordOption`, `TFRecordCompressionType`, or string.

        Returns:
          Compression type as string (e.g. `'ZLIB'`, `'GZIP'`, or `''`).

        Raises:
          ValueError: If compression_type is invalid.
        """
        ...

class TFRecordWriter:
    """
    A class to write records to a TFRecords file.

    [TFRecords tutorial](https://www.tensorflow.org/tutorials/load_data/tfrecord)

    TFRecords is a binary format which is optimized for high throughput data
    retrieval, generally in conjunction with `tf.data`. `TFRecordWriter` is used
    to write serialized examples to a file for later consumption. The key steps
    are:

     Ahead of time:

     - [Convert data into a serialized format](
     https://www.tensorflow.org/tutorials/load_data/tfrecord#tfexample)
     - [Write the serialized data to one or more files](
     https://www.tensorflow.org/tutorials/load_data/tfrecord#tfrecord_files_in_python)

     During training or evaluation:

     - [Read serialized examples into memory](
     https://www.tensorflow.org/tutorials/load_data/tfrecord#reading_a_tfrecord_file)
     - [Parse (deserialize) examples](
     https://www.tensorflow.org/tutorials/load_data/tfrecord#reading_a_tfrecord_file)

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

    This class implements `__enter__` and `__exit__`, and can be used
    in `with` blocks like a normal file. (See the usage example above.)
    """
    def __init__(self, path: str, options: _CompressionTypes | TFRecordOptions | None = None) -> None:
        """
        Opens file `path` and creates a `TFRecordWriter` writing to it.

        Args:
          path: The path to the TFRecords file.
          options: (optional) String specifying compression type,
              `TFRecordCompressionType`, or `TFRecordOptions` object.

        Raises:
          IOError: If `path` cannot be opened for writing.
          ValueError: If valid compression_type can't be determined from `options`.
        """
        ...
    def write(self, record: bytes) -> None:
        """
        Write a string record to the file.

        Args:
          record: str
        """
        ...
    def flush(self) -> None:
        """Flush the file."""
        ...
    def close(self) -> None:
        """Close the file."""
        ...
    def __enter__(self) -> Self:
        """__enter__(self: object) -> object"""
        ...
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        """__exit__(self: tensorflow.python.lib.io._pywrap_record_io.RecordWriter, *args) -> None"""
        ...

class FixedLenFeature(NamedTuple):
    """
    Configuration for parsing a fixed-length input feature.

    To treat sparse input as dense, provide a `default_value`; otherwise,
    the parse functions will fail on any examples missing this feature.

    Fields:
      shape: Shape of input data.
      dtype: Data type of input.
      default_value: Value to be used if an example is missing this feature. It
          must be compatible with `dtype` and of the specified `shape`.
    """
    shape: ShapeLike
    dtype: DTypeLike
    default_value: TensorCompatible | None = None

class FixedLenSequenceFeature(NamedTuple):
    """
    Configuration for parsing a variable-length input feature into a `Tensor`.

    The resulting `Tensor` of parsing a single `SequenceExample` or `Example` has
    a static `shape` of `[None] + shape` and the specified `dtype`.
    The resulting `Tensor` of parsing a `batch_size` many `Example`s has
    a static `shape` of `[batch_size, None] + shape` and the specified `dtype`.
    The entries in the `batch` from different `Examples` will be padded with
    `default_value` to the maximum length present in the `batch`.

    To treat a sparse input as dense, provide `allow_missing=True`; otherwise,
    the parse functions will fail on any examples missing this feature.

    Fields:
      shape: Shape of input data for dimension 2 and higher. First dimension is
        of variable length `None`.
      dtype: Data type of input.
      allow_missing: Whether to allow this feature to be missing from a feature
        list item. Is available only for parsing `SequenceExample` not for
        parsing `Examples`.
      default_value: Scalar value to be used to pad multiple `Example`s to their
        maximum length. Irrelevant for parsing a single `Example` or
        `SequenceExample`. Defaults to "" for dtype string and 0 otherwise
        (optional).
    """
    shape: ShapeLike
    dtype: DTypeLike
    allow_missing: bool = False
    default_value: TensorCompatible | None = None

class VarLenFeature(NamedTuple):
    """
    Configuration for parsing a variable-length input feature.

    Fields:
      dtype: Data type of input.
    """
    dtype: DTypeLike

class SparseFeature(NamedTuple):
    """
    Configuration for parsing a sparse input feature from an `Example`.

    Note, preferably use `VarLenFeature` (possibly in combination with a
    `SequenceExample`) in order to parse out `SparseTensor`s instead of
    `SparseFeature` due to its simplicity.

    Closely mimicking the `SparseTensor` that will be obtained by parsing an
    `Example` with a `SparseFeature` config, a `SparseFeature` contains a

    * `value_key`: The name of key for a `Feature` in the `Example` whose parsed
      `Tensor` will be the resulting `SparseTensor.values`.

    * `index_key`: A list of names - one for each dimension in the resulting
      `SparseTensor` whose `indices[i][dim]` indicating the position of
      the `i`-th value in the `dim` dimension will be equal to the `i`-th value in
      the Feature with key named `index_key[dim]` in the `Example`.

    * `size`: A list of ints for the resulting `SparseTensor.dense_shape`.

    For example, we can represent the following 2D `SparseTensor`

    ```python
    SparseTensor(indices=[[3, 1], [20, 0]],
                 values=[0.5, -1.0]
                 dense_shape=[100, 3])
    ```

    with an `Example` input proto

    ```python
    features {
      feature { key: "val" value { float_list { value: [ 0.5, -1.0 ] } } }
      feature { key: "ix0" value { int64_list { value: [ 3, 20 ] } } }
      feature { key: "ix1" value { int64_list { value: [ 1, 0 ] } } }
    }
    ```

    and `SparseFeature` config with 2 `index_key`s

    ```python
    SparseFeature(index_key=["ix0", "ix1"],
                  value_key="val",
                  dtype=tf.float32,
                  size=[100, 3])
    ```

    Fields:
      index_key: A single string name or a list of string names of index features.
        For each key the underlying feature's type must be `int64` and its length
        must always match that of the `value_key` feature.
        To represent `SparseTensor`s with a `dense_shape` of `rank` higher than 1
        a list of length `rank` should be used.
      value_key: Name of value feature.  The underlying feature's type must
        be `dtype` and its length must always match that of all the `index_key`s'
        features.
      dtype: Data type of the `value_key` feature.
      size: A Python int or list thereof specifying the dense shape. Should be a
        list if and only if `index_key` is a list. In that case the list must be
        equal to the length of `index_key`. Each for each entry `i` all values in
        the `index_key`[i] feature must be in `[0, size[i])`.
      already_sorted: A Python boolean to specify whether the values in
        `value_key` are already sorted by their index position. If so skip
        sorting. False by default (optional).
    """
    index_key: str | list[str]
    value_key: str
    dtype: DTypeLike
    size: int | list[int]
    already_sorted: bool = False

class RaggedFeature(NamedTuple):
    """
    Configuration for passing a RaggedTensor input feature.

    `value_key` specifies the feature key for a variable-length list of values;
    and `partitions` specifies zero or more feature keys for partitioning those
    values into higher dimensions.  Each element of `partitions` must be one of
    the following:

      * `tf.io.RaggedFeature.RowSplits(key: string)`
      * `tf.io.RaggedFeature.RowLengths(key: string)`
      * `tf.io.RaggedFeature.RowStarts(key: string)`
      * `tf.io.RaggedFeature.RowLimits(key: string)`
      * `tf.io.RaggedFeature.ValueRowIds(key: string)`
      * `tf.io.RaggedFeature.UniformRowLength(length: int)`.

    Where `key` is a feature key whose values are used to partition the values.
    Partitions are listed from outermost to innermost.

    * If `len(partitions) == 0` (the default), then:

      * A feature from a single `tf.Example` is parsed into a 1D `tf.Tensor`.
      * A feature from a batch of `tf.Example`s is parsed into a 2D
        `tf.RaggedTensor`, where the outer dimension is the batch dimension, and
        the inner (ragged) dimension is the feature length in each example.

    * If `len(partitions) == 1`, then:

      * A feature from a single `tf.Example` is parsed into a 2D
        `tf.RaggedTensor`, where the values taken from the `value_key` are
        separated into rows using the partition key.
      * A feature from a batch of `tf.Example`s is parsed into a 3D
        `tf.RaggedTensor`, where the outer dimension is the batch dimension,
        the two inner dimensions are formed by separating the `value_key` values
        from each example into rows using that example's partition key.

    * If `len(partitions) > 1`, then:

      * A feature from a single `tf.Example` is parsed into a `tf.RaggedTensor`
        whose rank is `len(partitions)+1`, and whose ragged_rank is
        `len(partitions)`.

      * A feature from a batch of `tf.Example`s is parsed into a `tf.RaggedTensor`
        whose rank is `len(partitions)+2` and whose ragged_rank is
        `len(partitions)+1`, where the outer dimension is the batch dimension.

    There is one exception: if the final (i.e., innermost) element(s) of
    `partitions` are `UniformRowLength`s, then the values are simply reshaped (as
    a higher-dimensional `tf.Tensor`), rather than being wrapped in a
    `tf.RaggedTensor`.

    #### Examples

    >>> import google.protobuf.text_format as pbtext
    >>> example_batch = [
    ...   pbtext.Merge(r'''
    ...     features {
    ...       feature {key: "v" value {int64_list {value: [3, 1, 4, 1, 5, 9]}}}
    ...       feature {key: "s1" value {int64_list {value: [0, 2, 3, 3, 6]}}}
    ...       feature {key: "s2" value {int64_list {value: [0, 2, 3, 4]}}}
    ...     }''', tf.train.Example()).SerializeToString(),
    ...   pbtext.Merge(r'''
    ...     features {
    ...       feature {key: "v" value {int64_list {value: [2, 7, 1, 8, 2, 8, 1]}}}
    ...       feature {key: "s1" value {int64_list {value: [0, 3, 4, 5, 7]}}}
    ...       feature {key: "s2" value {int64_list {value: [0, 1, 1, 4]}}}
    ...     }''', tf.train.Example()).SerializeToString()]

    >>> features = {
    ...     # Zero partitions: returns 1D tf.Tensor for each Example.
    ...     'f1': tf.io.RaggedFeature(value_key="v", dtype=tf.int64),
    ...     # One partition: returns 2D tf.RaggedTensor for each Example.
    ...     'f2': tf.io.RaggedFeature(value_key="v", dtype=tf.int64, partitions=[
    ...         tf.io.RaggedFeature.RowSplits("s1")]),
    ...     # Two partitions: returns 3D tf.RaggedTensor for each Example.
    ...     'f3': tf.io.RaggedFeature(value_key="v", dtype=tf.int64, partitions=[
    ...         tf.io.RaggedFeature.RowSplits("s2"),
    ...         tf.io.RaggedFeature.RowSplits("s1")])
    ... }

    >>> feature_dict = tf.io.parse_single_example(example_batch[0], features)
    >>> for (name, val) in sorted(feature_dict.items()):
    ...   print('%s: %s' % (name, val))
    f1: tf.Tensor([3 1 4 1 5 9], shape=(6,), dtype=int64)
    f2: <tf.RaggedTensor [[3, 1], [4], [], [1, 5, 9]]>
    f3: <tf.RaggedTensor [[[3, 1], [4]], [[]], [[1, 5, 9]]]>

    >>> feature_dict = tf.io.parse_example(example_batch, features)
    >>> for (name, val) in sorted(feature_dict.items()):
    ...   print('%s: %s' % (name, val))
    f1: <tf.RaggedTensor [[3, 1, 4, 1, 5, 9],
                          [2, 7, 1, 8, 2, 8, 1]]>
    f2: <tf.RaggedTensor [[[3, 1], [4], [], [1, 5, 9]],
                          [[2, 7, 1], [8], [2], [8, 1]]]>
    f3: <tf.RaggedTensor [[[[3, 1], [4]], [[]], [[1, 5, 9]]],
                          [[[2, 7, 1]], [], [[8], [2], [8, 1]]]]>

    Fields:
      dtype: Data type of the `RaggedTensor`.  Must be one of:
        `tf.dtypes.int64`, `tf.dtypes.float32`, `tf.dtypes.string`.
      value_key: (Optional.) Key for a `Feature` in the input `Example`, whose
        parsed `Tensor` will be the resulting `RaggedTensor.flat_values`.  If
        not specified, then it defaults to the key for this `RaggedFeature`.
      partitions: (Optional.) A list of objects specifying the row-partitioning
        tensors (from outermost to innermost).  Each entry in this list must be
        one of:
          * `tf.io.RaggedFeature.RowSplits(key: string)`
          * `tf.io.RaggedFeature.RowLengths(key: string)`
          * `tf.io.RaggedFeature.RowStarts(key: string)`
          * `tf.io.RaggedFeature.RowLimits(key: string)`
          * `tf.io.RaggedFeature.ValueRowIds(key: string)`
          * `tf.io.RaggedFeature.UniformRowLength(length: int)`.
        Where `key` is a key for a `Feature` in the input `Example`, whose parsed
        `Tensor` will be the resulting row-partitioning tensor.
      row_splits_dtype: (Optional.) Data type for the row-partitioning tensor(s).
        One of `int32` or `int64`.  Defaults to `int32`.
      validate: (Optional.) Boolean indicating whether or not to validate that
        the input values form a valid RaggedTensor.  Defaults to `False`.
    """
    # Mypy doesn't support nested NamedTuples, but at runtime they actually do use
    # nested collections.namedtuple.
    class RowSplits(NamedTuple):  # type: ignore[misc]
        """RowSplits(key,)"""
        key: str

    class RowLengths(NamedTuple):  # type: ignore[misc]
        """RowLengths(key,)"""
        key: str

    class RowStarts(NamedTuple):  # type: ignore[misc]
        """RowStarts(key,)"""
        key: str

    class RowLimits(NamedTuple):  # type: ignore[misc]
        """RowLimits(key,)"""
        key: str

    class ValueRowIds(NamedTuple):  # type: ignore[misc]
        """ValueRowIds(key,)"""
        key: str

    class UniformRowLength(NamedTuple):  # type: ignore[misc]
        """UniformRowLength(length,)"""
        length: int

    dtype: DTypeLike
    value_key: str | None = None
    partitions: tuple[  # type: ignore[name-defined]
        RowSplits | RowLengths | RowStarts | RowLimits | ValueRowIds | UniformRowLength, ...
    ] = ()
    row_splits_dtype: DTypeLike = ...
    validate: bool = False

def parse_example(
    serialized: TensorCompatible, features: _FeatureSpecs, example_names: Iterable[str] | None = None, name: str | None = None
) -> dict[str, TensorLike]:
    """
    Parses `Example` protos into a `dict` of tensors.

    Parses a number of serialized [`Example`](https://www.tensorflow.org/code/tensorflow/core/example/example.proto)
    protos given in `serialized`. We refer to `serialized` as a batch with
    `batch_size` many entries of individual `Example` protos.

    `example_names` may contain descriptive names for the corresponding serialized
    protos. These may be useful for debugging purposes, but they have no effect on
    the output. If not `None`, `example_names` must be the same length as
    `serialized`.

    This op parses serialized examples into a dictionary mapping keys to `Tensor`
    `SparseTensor`, and `RaggedTensor` objects. `features` is a Mapping from keys
    to `VarLenFeature`, `SparseFeature`, `RaggedFeature`, and `FixedLenFeature`
    objects. Each `VarLenFeature` and `SparseFeature` is mapped to a
    `SparseTensor`; each `FixedLenFeature` is mapped to a `Tensor`; and each
    `RaggedFeature` is mapped to a `RaggedTensor`.

    Each `VarLenFeature` maps to a `SparseTensor` of the specified type
    representing a ragged matrix. Its indices are `[batch, index]` where `batch`
    identifies the example in `serialized`, and `index` is the value's index in
    the list of values associated with that feature and example.

    Each `SparseFeature` maps to a `SparseTensor` of the specified type
    representing a Tensor of `dense_shape` `[batch_size] + SparseFeature.size`.
    Its `values` come from the feature in the examples with key `value_key`.
    A `values[i]` comes from a position `k` in the feature of an example at batch
    entry `batch`. This positional information is recorded in `indices[i]` as
    `[batch, index_0, index_1, ...]` where `index_j` is the `k-th` value of
    the feature in the example at with key `SparseFeature.index_key[j]`.
    In other words, we split the indices (except the first index indicating the
    batch entry) of a `SparseTensor` by dimension into different features of the
    `Example`. Due to its complexity a `VarLenFeature` should be preferred over a
    `SparseFeature` whenever possible.

    Each `FixedLenFeature` `df` maps to a `Tensor` of the specified type (or
    `tf.float32` if not specified) and shape `(serialized.size(),) + df.shape`.

    `FixedLenFeature` entries with a `default_value` are optional. With no default
    value, we will fail if that `Feature` is missing from any example in
    `serialized`.

    Each `FixedLenSequenceFeature` `df` maps to a `Tensor` of the specified type
    (or `tf.float32` if not specified) and shape
    `(serialized.size(), None) + df.shape`.
    All examples in `serialized` will be padded with `default_value` along the
    second dimension.

    Each `RaggedFeature` maps to a `RaggedTensor` of the specified type.  It
    is formed by stacking the `RaggedTensor` for each example, where the
    `RaggedTensor` for each individual example is constructed using the tensors
    specified by `RaggedTensor.values_key` and `RaggedTensor.partition`.  See
    the `tf.io.RaggedFeature` documentation for details and examples.

    Examples:

    For example, if one expects a `tf.float32` `VarLenFeature` `ft` and three
    serialized `Example`s are provided:

    ```
    serialized = [
      features
        { feature { key: "ft" value { float_list { value: [1.0, 2.0] } } } },
      features
        { feature []},
      features
        { feature { key: "ft" value { float_list { value: [3.0] } } }
    ]
    ```

    then the output will look like:

    ```python
    {"ft": SparseTensor(indices=[[0, 0], [0, 1], [2, 0]],
                        values=[1.0, 2.0, 3.0],
                        dense_shape=(3, 2)) }
    ```

    If instead a `FixedLenSequenceFeature` with `default_value = -1.0` and
    `shape=[]` is used then the output will look like:

    ```python
    {"ft": [[1.0, 2.0], [3.0, -1.0]]}
    ```

    Given two `Example` input protos in `serialized`:

    ```
    [
      features {
        feature { key: "kw" value { bytes_list { value: [ "knit", "big" ] } } }
        feature { key: "gps" value { float_list { value: [] } } }
      },
      features {
        feature { key: "kw" value { bytes_list { value: [ "emmy" ] } } }
        feature { key: "dank" value { int64_list { value: [ 42 ] } } }
        feature { key: "gps" value { } }
      }
    ]
    ```

    And arguments

    ```
    example_names: ["input0", "input1"],
    features: {
        "kw": VarLenFeature(tf.string),
        "dank": VarLenFeature(tf.int64),
        "gps": VarLenFeature(tf.float32),
    }
    ```

    Then the output is a dictionary:

    ```python
    {
      "kw": SparseTensor(
          indices=[[0, 0], [0, 1], [1, 0]],
          values=["knit", "big", "emmy"]
          dense_shape=[2, 2]),
      "dank": SparseTensor(
          indices=[[1, 0]],
          values=[42],
          dense_shape=[2, 1]),
      "gps": SparseTensor(
          indices=[],
          values=[],
          dense_shape=[2, 0]),
    }
    ```

    For dense results in two serialized `Example`s:

    ```
    [
      features {
        feature { key: "age" value { int64_list { value: [ 0 ] } } }
        feature { key: "gender" value { bytes_list { value: [ "f" ] } } }
       },
       features {
        feature { key: "age" value { int64_list { value: [] } } }
        feature { key: "gender" value { bytes_list { value: [ "f" ] } } }
      }
    ]
    ```

    We can use arguments:

    ```
    example_names: ["input0", "input1"],
    features: {
        "age": FixedLenFeature([], dtype=tf.int64, default_value=-1),
        "gender": FixedLenFeature([], dtype=tf.string),
    }
    ```

    And the expected output is:

    ```python
    {
      "age": [[0], [-1]],
      "gender": [["f"], ["f"]],
    }
    ```

    An alternative to `VarLenFeature` to obtain a `SparseTensor` is
    `SparseFeature`. For example, given two `Example` input protos in
    `serialized`:

    ```
    [
      features {
        feature { key: "val" value { float_list { value: [ 0.5, -1.0 ] } } }
        feature { key: "ix" value { int64_list { value: [ 3, 20 ] } } }
      },
      features {
        feature { key: "val" value { float_list { value: [ 0.0 ] } } }
        feature { key: "ix" value { int64_list { value: [ 42 ] } } }
      }
    ]
    ```

    And arguments

    ```
    example_names: ["input0", "input1"],
    features: {
        "sparse": SparseFeature(
            index_key="ix", value_key="val", dtype=tf.float32, size=100),
    }
    ```

    Then the output is a dictionary:

    ```python
    {
      "sparse": SparseTensor(
          indices=[[0, 3], [0, 20], [1, 42]],
          values=[0.5, -1.0, 0.0]
          dense_shape=[2, 100]),
    }
    ```

    See the `tf.io.RaggedFeature` documentation for examples showing how
    `RaggedFeature` can be used to obtain `RaggedTensor`s.

    Args:
      serialized: A vector (1-D Tensor) of strings, a batch of binary
        serialized `Example` protos.
      features: A mapping of feature keys to `FixedLenFeature`,
        `VarLenFeature`, `SparseFeature`, and `RaggedFeature` values.
      example_names: A vector (1-D Tensor) of strings (optional), the names of
        the serialized protos in the batch.
      name: A name for this operation (optional).

    Returns:
      A `dict` mapping feature keys to `Tensor`, `SparseTensor`, and
      `RaggedTensor` values.

    Raises:
      ValueError: if any feature is invalid.
    """
    ...
def __getattr__(name: str): ...  # incomplete module

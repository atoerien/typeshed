# The types here are all undocumented, but all feature columns are return types of the
# public functions in tf.feature_column. As they are undocumented internals while some
# common methods are included, they are incomplete and do not have getattr Incomplete fallback.


"""
This API defines FeatureColumn abstraction.

FeatureColumns provide a high level abstraction for ingesting and representing
features.

FeatureColumns can also be transformed into a generic input layer for
custom models using `input_layer`.

NOTE: Functions prefixed with "_" indicate experimental or private parts of
the API subject to change, and should not be relied upon!
"""

from _typeshed import Incomplete
from abc import ABC, ABCMeta, abstractmethod
from collections.abc import Callable, Sequence
from typing import Literal, TypeAlias
from typing_extensions import Self

import tensorflow as tf
from tensorflow._aliases import ShapeLike

_Combiners: TypeAlias = Literal["mean", "sqrtn", "sum"]
_ExampleSpec: TypeAlias = dict[str, tf.io.FixedLenFeature | tf.io.VarLenFeature]

class _FeatureColumn(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...
    @property
    @abstractmethod
    def parse_example_spec(self) -> _ExampleSpec: ...
    def __lt__(self, other: _FeatureColumn) -> bool: ...
    def __gt__(self, other: _FeatureColumn) -> bool: ...
    @property
    @abstractmethod
    def parents(self) -> list[_FeatureColumn | str]: ...

class DenseColumn(_FeatureColumn, metaclass=ABCMeta):
    """
    Represents a column which can be represented as `Tensor`.

    Some examples of this type are: numeric_column, embedding_column,
    indicator_column.
    """
    ...
class SequenceDenseColumn(_FeatureColumn, metaclass=ABCMeta):
    """Represents dense sequence data."""
    ...

# These classes are mostly subclasses of collections.namedtuple but we can't use
# typing.NamedTuple because they use multiple inheritance with other non namedtuple classes.
# _cls instead of cls is because collections.namedtuple uses _cls for __new__.
class NumericColumn(DenseColumn):
    """see `numeric_column`."""
    key: str
    shape: ShapeLike
    default_value: float
    dtype: tf.DType
    normalizer_fn: Callable[[tf.Tensor], tf.Tensor] | None

    def __new__(
        _cls,
        key: str,
        shape: ShapeLike,
        default_value: float,
        dtype: tf.DType,
        normalizer_fn: Callable[[tf.Tensor], tf.Tensor] | None,
    ) -> Self:
        """Create new instance of NumericColumn(key, shape, default_value, dtype, normalizer_fn)"""
        ...
    @property
    def name(self) -> str:
        """See `FeatureColumn` base class."""
        ...
    @property
    def parse_example_spec(self) -> _ExampleSpec:
        """See `FeatureColumn` base class."""
        ...
    @property
    def parents(self) -> list[_FeatureColumn | str]:
        """See 'FeatureColumn` base class."""
        ...

class CategoricalColumn(_FeatureColumn):
    """
    Represents a categorical feature.

    A categorical feature typically handled with a `tf.sparse.SparseTensor` of
    IDs.
    """
    @property
    @abstractmethod
    def num_buckets(self) -> int:
        """Returns number of buckets in this sparse feature."""
        ...

class BucketizedColumn(DenseColumn, CategoricalColumn):
    """See `bucketized_column`."""
    source_column: NumericColumn
    boundaries: list[float] | tuple[float, ...]

    def __new__(_cls, source_column: NumericColumn, boundaries: list[float] | tuple[float, ...]) -> Self:
        """Create new instance of BucketizedColumn(source_column, boundaries)"""
        ...
    @property
    def name(self) -> str:
        """See `FeatureColumn` base class."""
        ...
    @property
    def num_buckets(self) -> int:
        """See `CategoricalColumn` base class."""
        ...
    @property
    def parse_example_spec(self) -> _ExampleSpec:
        """See `FeatureColumn` base class."""
        ...
    @property
    def parents(self) -> list[_FeatureColumn | str]:
        """See 'FeatureColumn` base class."""
        ...

class EmbeddingColumn(DenseColumn, SequenceDenseColumn):
    """See `embedding_column`."""
    categorical_column: CategoricalColumn
    dimension: int
    combiner: _Combiners
    initializer: Callable[[ShapeLike], tf.Tensor] | None
    ckpt_to_load_from: str | None
    tensor_name_in_ckpt: str | None
    max_norm: float | None
    trainable: bool
    use_safe_embedding_lookup: bool

    # This one subclasses collections.namedtuple and overrides __new__.
    def __new__(
        cls,
        categorical_column: CategoricalColumn,
        dimension: int,
        combiner: _Combiners,
        initializer: Callable[[ShapeLike], tf.Tensor] | None,
        ckpt_to_load_from: str | None,
        tensor_name_in_ckpt: str | None,
        max_norm: float | None,
        trainable: bool,
        use_safe_embedding_lookup: bool = True,
    ) -> Self: ...
    @property
    def name(self) -> str:
        """See `FeatureColumn` base class."""
        ...
    @property
    def parse_example_spec(self) -> _ExampleSpec:
        """See `FeatureColumn` base class."""
        ...
    @property
    def parents(self) -> list[_FeatureColumn | str]:
        """See 'FeatureColumn` base class."""
        ...

class SharedEmbeddingColumnCreator:
    """Class that creates a `SharedEmbeddingColumn`."""
    def __init__(
        self,
        dimension: int,
        initializer: Callable[[ShapeLike], tf.Tensor] | None,
        ckpt_to_load_from: str | None,
        tensor_name_in_ckpt: str | None,
        num_buckets: int,
        trainable: bool,
        name: str = "shared_embedding_column_creator",
        use_safe_embedding_lookup: bool = True,
    ) -> None: ...
    def __getattr__(self, name: str) -> Incomplete: ...

class SharedEmbeddingColumn(DenseColumn, SequenceDenseColumn):
    """See `embedding_column`."""
    categorical_column: CategoricalColumn
    shared_embedding_column_creator: SharedEmbeddingColumnCreator
    combiner: _Combiners
    max_norm: float | None
    use_safe_embedding_lookup: bool

    def __new__(
        cls,
        categorical_column: CategoricalColumn,
        shared_embedding_column_creator: SharedEmbeddingColumnCreator,
        combiner: _Combiners,
        max_norm: float | None,
        use_safe_embedding_lookup: bool = True,
    ) -> Self: ...
    @property
    def name(self) -> str:
        """See `FeatureColumn` base class."""
        ...
    @property
    def parse_example_spec(self) -> _ExampleSpec:
        """See `FeatureColumn` base class."""
        ...
    @property
    def parents(self) -> list[_FeatureColumn | str]:
        """See 'FeatureColumn` base class."""
        ...

class CrossedColumn(CategoricalColumn):
    """See `crossed_column`."""
    keys: tuple[str, ...]
    hash_bucket_size: int
    hash_key: int | None

    def __new__(_cls, keys: tuple[str, ...], hash_bucket_size: int, hash_key: int | None) -> Self:
        """Create new instance of CrossedColumn(keys, hash_bucket_size, hash_key)"""
        ...
    @property
    def name(self) -> str:
        """See `FeatureColumn` base class."""
        ...
    @property
    def num_buckets(self) -> int:
        """Returns number of buckets in this sparse feature."""
        ...
    @property
    def parse_example_spec(self) -> _ExampleSpec:
        """See `FeatureColumn` base class."""
        ...
    @property
    def parents(self) -> list[_FeatureColumn | str]:
        """See 'FeatureColumn` base class."""
        ...

class IdentityCategoricalColumn(CategoricalColumn):
    """See `categorical_column_with_identity`."""
    key: str
    number_buckets: int
    default_value: int | None

    def __new__(_cls, key: str, number_buckets: int, default_value: int | None) -> Self:
        """Create new instance of IdentityCategoricalColumn(key, number_buckets, default_value)"""
        ...
    @property
    def name(self) -> str:
        """See `FeatureColumn` base class."""
        ...
    @property
    def num_buckets(self) -> int:
        """Returns number of buckets in this sparse feature."""
        ...
    @property
    def parse_example_spec(self) -> _ExampleSpec:
        """See `FeatureColumn` base class."""
        ...
    @property
    def parents(self) -> list[_FeatureColumn | str]:
        """See 'FeatureColumn` base class."""
        ...

class HashedCategoricalColumn(CategoricalColumn):
    """see `categorical_column_with_hash_bucket`."""
    key: str
    hash_bucket_size: int
    dtype: tf.DType

    def __new__(_cls, key: str, hash_bucket_size: int, dtype: tf.DType) -> Self:
        """Create new instance of HashedCategoricalColumn(key, hash_bucket_size, dtype)"""
        ...
    @property
    def name(self) -> str:
        """See `FeatureColumn` base class."""
        ...
    @property
    def num_buckets(self) -> int:
        """Returns number of buckets in this sparse feature."""
        ...
    @property
    def parse_example_spec(self) -> _ExampleSpec:
        """See `FeatureColumn` base class."""
        ...
    @property
    def parents(self) -> list[_FeatureColumn | str]:
        """See 'FeatureColumn` base class."""
        ...

class VocabularyFileCategoricalColumn(CategoricalColumn):
    """See `categorical_column_with_vocabulary_file`."""
    key: str
    vocabulary_file: str
    vocabulary_size: int | None
    num_oov_buckets: int
    dtype: tf.DType
    default_value: str | int | None
    file_format: str | None

    def __new__(
        cls,
        key: str,
        vocabulary_file: str,
        vocabulary_size: int | None,
        num_oov_buckets: int,
        dtype: tf.DType,
        default_value: str | int | None,
        file_format: str | None = None,
    ) -> Self: ...
    @property
    def name(self) -> str:
        """See `FeatureColumn` base class."""
        ...
    @property
    def num_buckets(self) -> int:
        """Returns number of buckets in this sparse feature."""
        ...
    @property
    def parse_example_spec(self) -> _ExampleSpec:
        """See `FeatureColumn` base class."""
        ...
    @property
    def parents(self) -> list[_FeatureColumn | str]:
        """See 'FeatureColumn` base class."""
        ...

class VocabularyListCategoricalColumn(CategoricalColumn):
    """See `categorical_column_with_vocabulary_list`."""
    key: str
    vocabulary_list: Sequence[str] | Sequence[int]
    dtype: tf.DType
    default_value: str | int | None
    num_oov_buckets: int

    def __new__(
        _cls, key: str, vocabulary_list: Sequence[str], dtype: tf.DType, default_value: str | int | None, num_oov_buckets: int
    ) -> Self:
        """Create new instance of VocabularyListCategoricalColumn(key, vocabulary_list, dtype, default_value, num_oov_buckets)"""
        ...
    @property
    def name(self) -> str:
        """See `FeatureColumn` base class."""
        ...
    @property
    def num_buckets(self) -> int:
        """Returns number of buckets in this sparse feature."""
        ...
    @property
    def parse_example_spec(self) -> _ExampleSpec:
        """See `FeatureColumn` base class."""
        ...
    @property
    def parents(self) -> list[_FeatureColumn | str]:
        """See 'FeatureColumn` base class."""
        ...

class WeightedCategoricalColumn(CategoricalColumn):
    """See `weighted_categorical_column`."""
    categorical_column: CategoricalColumn
    weight_feature_key: str
    dtype: tf.DType

    def __new__(_cls, categorical_column: CategoricalColumn, weight_feature_key: str, dtype: tf.DType) -> Self:
        """Create new instance of WeightedCategoricalColumn(categorical_column, weight_feature_key, dtype)"""
        ...
    @property
    def name(self) -> str:
        """See `FeatureColumn` base class."""
        ...
    @property
    def num_buckets(self) -> int:
        """See `DenseColumn` base class."""
        ...
    @property
    def parse_example_spec(self) -> _ExampleSpec:
        """See `FeatureColumn` base class."""
        ...
    @property
    def parents(self) -> list[_FeatureColumn | str]:
        """See 'FeatureColumn` base class."""
        ...

class IndicatorColumn(DenseColumn, SequenceDenseColumn):
    """
    Represents a one-hot column for use in deep networks.

    Args:
      categorical_column: A `CategoricalColumn` which is created by
        `categorical_column_with_*` function.
    """
    categorical_column: CategoricalColumn

    def __new__(_cls, categorical_column: CategoricalColumn) -> Self:
        """Create new instance of IndicatorColumn(categorical_column,)"""
        ...
    @property
    def name(self) -> str:
        """See `FeatureColumn` base class."""
        ...
    @property
    def parse_example_spec(self) -> _ExampleSpec:
        """See `FeatureColumn` base class."""
        ...
    @property
    def parents(self) -> list[_FeatureColumn | str]:
        """See 'FeatureColumn` base class."""
        ...

class SequenceCategoricalColumn(CategoricalColumn):
    """Represents sequences of categorical data."""
    categorical_column: CategoricalColumn

    def __new__(_cls, categorical_column: CategoricalColumn) -> Self:
        """Create new instance of _SequenceCategoricalColumn(categorical_column,)"""
        ...
    @property
    def name(self) -> str:
        """See `FeatureColumn` base class."""
        ...
    @property
    def num_buckets(self) -> int:
        """Returns number of buckets in this sparse feature."""
        ...
    @property
    def parse_example_spec(self) -> _ExampleSpec:
        """See `FeatureColumn` base class."""
        ...
    @property
    def parents(self) -> list[_FeatureColumn | str]:
        """See 'FeatureColumn` base class."""
        ...

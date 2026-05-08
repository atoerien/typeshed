"""Public API for tf._api.v2.random namespace"""

from collections.abc import Sequence
from enum import Enum
from typing import Literal, TypeAlias

import numpy as np
import numpy.typing as npt
import tensorflow as tf
from tensorflow._aliases import DTypeLike, ScalarTensorCompatible, ShapeLike
from tensorflow.python.trackable import autotrackable

class Algorithm(Enum):
    """
    A random-number-generation (RNG) algorithm.

    Many random-number generators (e.g. the `alg` argument of
    `tf.random.Generator` and `tf.random.stateless_uniform`) in TF allow
    you to choose the algorithm used to generate the (pseudo-)random
    numbers. You can set the algorithm to be one of the options below.

    * `PHILOX`: The Philox algorithm introduced in the paper ["Parallel
      Random Numbers: As Easy as 1, 2,
      3"](https://www.thesalmons.org/john/random123/papers/random123sc11.pdf).
    * `THREEFRY`: The ThreeFry algorithm introduced in the paper
      ["Parallel Random Numbers: As Easy as 1, 2,
      3"](https://www.thesalmons.org/john/random123/papers/random123sc11.pdf).
    * `AUTO_SELECT`: Allow TF to automatically select the algorithm
      depending on the accelerator device. Note that with this option,
      running the same TF program on different devices may result in
      different random numbers. Also note that TF may select an
      algorithm that is different from `PHILOX` and `THREEFRY`.
    """
    PHILOX = 1
    THREEFRY = 2
    AUTO_SELECT = 3

_Alg: TypeAlias = Literal[Algorithm.PHILOX, Algorithm.THREEFRY, Algorithm.AUTO_SELECT, "philox", "threefry", "auto_select"]

class Generator(autotrackable.AutoTrackable):
    """
    Random-number generator.

    Example:

    Creating a generator from a seed:

    >>> g = tf.random.Generator.from_seed(1234)
    >>> g.normal(shape=(2, 3))
    <tf.Tensor: shape=(2, 3), dtype=float32, numpy=
    array([[ 0.9356609 ,  1.0854305 , -0.93788373],
           [-0.5061547 ,  1.3169702 ,  0.7137579 ]], dtype=float32)>

    Creating a generator from a non-deterministic state:

    >>> g = tf.random.Generator.from_non_deterministic_state()
    >>> g.normal(shape=(2, 3))
    <tf.Tensor: shape=(2, 3), dtype=float32, numpy=...>

    All the constructors allow explicitly choosing an Random-Number-Generation
    (RNG) algorithm. Supported algorithms are `"philox"` and `"threefry"`. For
    example:

    >>> g = tf.random.Generator.from_seed(123, alg="philox")
    >>> g.normal(shape=(2, 3))
    <tf.Tensor: shape=(2, 3), dtype=float32, numpy=
    array([[ 0.8673864 , -0.29899067, -0.9310337 ],
           [-1.5828488 ,  1.2481191 , -0.6770643 ]], dtype=float32)>

    CPU, GPU and TPU with the same algorithm and seed will generate the same
    integer random numbers. Float-point results (such as the output of `normal`)
    may have small numerical discrepancies between different devices.

    This class uses a `tf.Variable` to manage its internal state. Every time
    random numbers are generated, the state of the generator will change. For
    example:

    >>> g = tf.random.Generator.from_seed(1234)
    >>> g.state
    <tf.Variable ... numpy=array([1234,    0,    0])>
    >>> g.normal(shape=(2, 3))
    <...>
    >>> g.state
    <tf.Variable ... numpy=array([2770,    0,    0])>

    The shape of the state is algorithm-specific.

    There is also a global generator:

    >>> g = tf.random.get_global_generator()
    >>> g.normal(shape=(2, 3))
    <tf.Tensor: shape=(2, 3), dtype=float32, numpy=...>

    When creating a generator inside a `tf.distribute.Strategy` scope, each
    replica will get a different stream of random numbers.

    For example, in this code:

    ```
    strat = tf.distribute.MirroredStrategy(devices=["cpu:0", "cpu:1"])
    with strat.scope():
      g = tf.random.Generator.from_seed(1)
      def f():
        return g.normal([])
      results = strat.run(f).values
    ```

    `results[0]` and `results[1]` will have different values.

    If the generator is seeded (e.g. created via `Generator.from_seed`), the
    random numbers will be determined by the seed, even though different replicas
    get different numbers.  One can think of a random number generated on a
    replica as a hash of the replica ID and a "master" random number that may be
    common to all replicas. Hence, the whole system is still deterministic.

    (Note that the random numbers on different replicas are not correlated, even
    if they are deterministically determined by the same seed. They are not
    correlated in the sense that no matter what statistics one calculates on them,
    there won't be any discernable correlation.)

    Generators can be freely saved and restored using `tf.train.Checkpoint`. The
    checkpoint can be restored in a distribution strategy with a different number
    of replicas than the original strategy. If a replica ID is present in both the
    original and the new distribution strategy, its state will be properly
    restored (i.e. the random-number stream from the restored point will be the
    same as that from the saving point) unless the replicas have already diverged
    in their RNG call traces before saving (e.g. one replica has made one RNG call
    while another has made two RNG calls). We don't have such guarantee if the
    generator is saved in a strategy scope and restored outside of any strategy
    scope, or vice versa.

    When a generator is created within the scope of
    `tf.distribute.experimental.ParameterServerStrategy`, the workers
    will share the generator's state (placed on one of the parameter
    servers). In this way the workers will still get different
    random-number streams, as stated above. (This is similar to replicas
    in a `tf.distribute.MirroredStrategy` sequentially accessing a
    generator created outside the strategy.) Each RNG call on a worker
    will incur a round-trip to a parameter server, which may have
    performance impacts. When creating a
    `tf.distribute.experimental.ParameterServerStrategy`, please make
    sure that the `variable_partitioner` argument won't shard small
    variables of shape `[2]` or `[3]` (because generator states must not
    be sharded). Ways to avoid sharding small variables include setting
    `variable_partitioner` to `None` or to
    `tf.distribute.experimental.partitioners.MinSizePartitioner` with a
    large enough `min_shard_bytes` (see
    `tf.distribute.experimental.ParameterServerStrategy`'s documentation
    for more details).
    """
    @classmethod
    def from_state(cls, state: tf.Variable, alg: _Alg | None) -> Generator:
        """
        Creates a generator from a state.

        See `__init__` for description of `state` and `alg`.

        Args:
          state: the new state.
          alg: the RNG algorithm.

        Returns:
          The new generator.
        """
        ...
    @classmethod
    def from_seed(cls, seed: int, alg: _Alg | None = None) -> Generator:
        """
        Creates a generator from a seed.

        A seed is a 1024-bit unsigned integer represented either as a Python
        integer or a vector of integers. Seeds shorter than 1024-bit will be
        padded. The padding, the internal structure of a seed and the way a seed
        is converted to a state are all opaque (unspecified). The only semantics
        specification of seeds is that two different seeds are likely to produce
        two independent generators (but no guarantee).

        Args:
          seed: the seed for the RNG.
          alg: (optional) the RNG algorithm. If None, it will be auto-selected. See
            `__init__` for its possible values.

        Returns:
          The new generator.
        """
        ...
    @classmethod
    def from_non_deterministic_state(cls, alg: _Alg | None = None) -> Generator:
        """
        Creates a generator by non-deterministically initializing its state.

        The source of the non-determinism will be platform- and time-dependent.

        Args:
          alg: (optional) the RNG algorithm. If None, it will be auto-selected. See
            `__init__` for its possible values.

        Returns:
          The new generator.
        """
        ...
    @classmethod
    def from_key_counter(
        cls, key: ScalarTensorCompatible, counter: Sequence[ScalarTensorCompatible], alg: _Alg | None
    ) -> Generator:
        """
        Creates a generator from a key and a counter.

        This constructor only applies if the algorithm is a counter-based algorithm.
        See method `key` for the meaning of "key" and "counter".

        Args:
          key: the key for the RNG, a scalar of type STATE_TYPE.
          counter: a vector of dtype STATE_TYPE representing the initial counter for
            the RNG, whose length is algorithm-specific.,
          alg: the RNG algorithm. If None, it will be auto-selected. See
            `__init__` for its possible values.

        Returns:
          The new generator.
        """
        ...
    def __init__(self, copy_from: Generator | None = None, state: tf.Variable | None = None, alg: _Alg | None = None) -> None:
        """
        Creates a generator.

        The new generator will be initialized by one of the following ways, with
        decreasing precedence:
        (1) If `copy_from` is not None, the new generator is initialized by copying
            information from another generator.
        (2) If `state` and `alg` are not None (they must be set together), the new
            generator is initialized by a state.

        Args:
          copy_from: a generator to be copied from.
          state: a vector of dtype STATE_TYPE representing the initial state of the
            RNG, whose length and semantics are algorithm-specific. If it's a
            variable, the generator will reuse it instead of creating a new
            variable.
          alg: the RNG algorithm. Possible values are
            `tf.random.Algorithm.PHILOX` for the Philox algorithm and
            `tf.random.Algorithm.THREEFRY` for the ThreeFry algorithm
            (see paper 'Parallel Random Numbers: As Easy as 1, 2, 3'
            [https://www.thesalmons.org/john/random123/papers/random123sc11.pdf]).
            The string names `"philox"` and `"threefry"` can also be used.
            Note `PHILOX` guarantees the same numbers are produced (given
            the same random state) across all architectures (CPU, GPU, XLA etc).
        """
        ...
    def reset(self, state: tf.Variable) -> None:
        """
        Resets the generator by a new state.

        See `__init__` for the meaning of "state".

        Args:
          state: the new state.
        """
        ...
    def reset_from_seed(self, seed: int) -> None:
        """
        Resets the generator by a new seed.

        See `from_seed` for the meaning of "seed".

        Args:
          seed: the new seed.
        """
        ...
    def reset_from_key_counter(self, key: ScalarTensorCompatible, counter: tf.Variable) -> None:
        """
        Resets the generator by a new key-counter pair.

        See `from_key_counter` for the meaning of "key" and "counter".

        Args:
          key: the new key.
          counter: the new counter.
        """
        ...
    @property
    def state(self) -> tf.Variable:
        """The internal state of the RNG."""
        ...
    @property
    def algorithm(self) -> int:
        """The RNG algorithm id (a Python integer or scalar integer Tensor)."""
        ...
    @property
    def key(self) -> ScalarTensorCompatible:
        """
        The 'key' part of the state of a counter-based RNG.

        For a counter-base RNG algorithm such as Philox and ThreeFry (as
        described in paper 'Parallel Random Numbers: As Easy as 1, 2, 3'
        [https://www.thesalmons.org/john/random123/papers/random123sc11.pdf]),
        the RNG state consists of two parts: counter and key. The output is
        generated via the formula: output=hash(key, counter), i.e. a hashing of
        the counter parametrized by the key. Two RNGs with two different keys can
        be thought as generating two independent random-number streams (a stream
        is formed by increasing the counter).

        Returns:
          A scalar which is the 'key' part of the state, if the RNG algorithm is
            counter-based; otherwise it raises a ValueError.
        """
        ...
    def skip(self, delta: int) -> tf.Tensor:
        """
        Advance the counter of a counter-based RNG.

        Args:
          delta: the amount of advancement. The state of the RNG after
            `skip(n)` will be the same as that after `normal([n])`
            (or any other distribution). The actual increment added to the
            counter is an unspecified implementation detail.

        Returns:
          A `Tensor` of type `int64`.
        """
        ...
    def normal(
        self,
        shape: tf.Tensor | Sequence[int],
        mean: ScalarTensorCompatible = 0.0,
        stddev: ScalarTensorCompatible = 1.0,
        dtype: DTypeLike = ...,
        name: str | None = None,
    ) -> tf.Tensor:
        """
        Outputs random values from a normal distribution.

        Args:
          shape: A 1-D integer Tensor or Python array. The shape of the output
            tensor.
          mean: A 0-D Tensor or Python value of type `dtype`. The mean of the normal
            distribution.
          stddev: A 0-D Tensor or Python value of type `dtype`. The standard
            deviation of the normal distribution.
          dtype: The type of the output.
          name: A name for the operation (optional).

        Returns:
          A tensor of the specified shape filled with random normal values.
        """
        ...
    def truncated_normal(
        self,
        shape: ShapeLike,
        mean: ScalarTensorCompatible = 0.0,
        stddev: ScalarTensorCompatible = 1.0,
        dtype: DTypeLike = ...,
        name: str | None = None,
    ) -> tf.Tensor:
        """
        Outputs random values from a truncated normal distribution.

        The generated values follow a normal distribution with specified mean and
        standard deviation, except that values whose magnitude is more than
        2 standard deviations from the mean are dropped and re-picked.

        Args:
          shape: A 1-D integer Tensor or Python array. The shape of the output
            tensor.
          mean: A 0-D Tensor or Python value of type `dtype`. The mean of the
            truncated normal distribution.
          stddev: A 0-D Tensor or Python value of type `dtype`. The standard
            deviation of the normal distribution, before truncation.
          dtype: The type of the output.
          name: A name for the operation (optional).

        Returns:
          A tensor of the specified shape filled with random truncated normal
            values.
        """
        ...
    def uniform(
        self,
        shape: ShapeLike,
        minval: ScalarTensorCompatible = 0,
        maxval: ScalarTensorCompatible | None = None,
        dtype: DTypeLike = ...,
        name: str | None = None,
    ) -> tf.Tensor:
        """
        Outputs random values from a uniform distribution.

        The generated values follow a uniform distribution in the range
        `[minval, maxval)`. The lower bound `minval` is included in the range, while
        the upper bound `maxval` is excluded. (For float numbers especially
        low-precision types like bfloat16, because of
        rounding, the result may sometimes include `maxval`.)

        For floats, the default range is `[0, 1)`.  For ints, at least `maxval` must
        be specified explicitly.

        In the integer case, the random integers are slightly biased unless
        `maxval - minval` is an exact power of two.  The bias is small for values of
        `maxval - minval` significantly smaller than the range of the output (either
        `2**32` or `2**64`).

        For full-range random integers, pass `minval=None` and `maxval=None` with an
        integer `dtype` (for integer dtypes, `minval` and `maxval` must be both
        `None` or both not `None`).

        Args:
          shape: A 1-D integer Tensor or Python array. The shape of the output
            tensor.
          minval: A Tensor or Python value of type `dtype`, broadcastable with
            `shape` (for integer types, broadcasting is not supported, so it needs
            to be a scalar). The lower bound (included) on the range of random
            values to generate. Pass `None` for full-range integers. Defaults to 0.
          maxval: A Tensor or Python value of type `dtype`, broadcastable with
            `shape` (for integer types, broadcasting is not supported, so it needs
            to be a scalar). The upper bound (excluded) on the range of random
            values to generate. Pass `None` for full-range integers. Defaults to 1
            if `dtype` is floating point.
          dtype: The type of the output.
          name: A name for the operation (optional).

        Returns:
          A tensor of the specified shape filled with random uniform values.

        Raises:
          ValueError: If `dtype` is integral and `maxval` is not specified.
        """
        ...
    def uniform_full_int(self, shape: ShapeLike, dtype: DTypeLike = ..., name: str | None = None) -> tf.Tensor:
        """
        Uniform distribution on an integer type's entire range.

        This method is the same as setting `minval` and `maxval` to `None` in the
        `uniform` method.

        Args:
          shape: the shape of the output.
          dtype: (optional) the integer type, default to uint64.
          name: (optional) the name of the node.

        Returns:
          A tensor of random numbers of the required shape.
        """
        ...
    def binomial(
        self, shape: ShapeLike, counts: tf.Tensor, probs: tf.Tensor, dtype: DTypeLike = ..., name: str | None = None
    ) -> tf.Tensor:
        """
        Outputs random values from a binomial distribution.

        The generated values follow a binomial distribution with specified count and
        probability of success parameters.

        Example:

        ```python
        counts = [10., 20.]
        # Probability of success.
        probs = [0.8]

        rng = tf.random.Generator.from_seed(seed=234)
        binomial_samples = rng.binomial(shape=[2], counts=counts, probs=probs)


        counts = ... # Shape [3, 1, 2]
        probs = ...  # Shape [1, 4, 2]
        shape = [3, 4, 3, 4, 2]
        rng = tf.random.Generator.from_seed(seed=1717)
        # Sample shape will be [3, 4, 3, 4, 2]
        binomial_samples = rng.binomial(shape=shape, counts=counts, probs=probs)
        ```


        Args:
          shape: A 1-D integer Tensor or Python array. The shape of the output
            tensor.
          counts: Tensor. The counts of the binomial distribution. Must be
            broadcastable with `probs`, and broadcastable with the rightmost
            dimensions of `shape`.
          probs: Tensor. The probability of success for the
            binomial distribution. Must be broadcastable with `counts` and
            broadcastable with the rightmost dimensions of `shape`.
          dtype: The type of the output. Default: tf.int32
          name: A name for the operation (optional).

        Returns:
          samples: A Tensor of the specified shape filled with random binomial
            values.  For each i, each samples[i, ...] is an independent draw from
            the binomial distribution on counts[i] trials with probability of
            success probs[i].
        """
        ...
    def make_seeds(self, count: int = 1) -> tf.Tensor:
        """
        Generates seeds for stateless random ops.

        For example:

        ```python
        seeds = get_global_generator().make_seeds(count=10)
        for i in range(10):
          seed = seeds[:, i]
          numbers = stateless_random_normal(shape=[2, 3], seed=seed)
          ...
        ```

        Args:
          count: the number of seed pairs (note that stateless random ops need a
            pair of seeds to invoke).

        Returns:
          A tensor of shape [2, count] and dtype int64.
        """
        ...
    def split(self, count: int = 1) -> list[Generator]:
        """
        Returns a list of independent `Generator` objects.

        Two generators are independent of each other in the sense that the
        random-number streams they generate don't have statistically detectable
        correlations. The new generators are also independent of the old one.
        The old generator's state will be changed (like other random-number
        generating methods), so two calls of `split` will return different
        new generators.

        For example:

        ```python
        gens = get_global_generator().split(count=10)
        for gen in gens:
          numbers = gen.normal(shape=[2, 3])
          # ...
        gens2 = get_global_generator().split(count=10)
        # gens2 will be different from gens
        ```

        The new generators will be put on the current device (possible different
        from the old generator's), for example:

        ```python
        with tf.device("/device:CPU:0"):
          gen = Generator(seed=1234)  # gen is on CPU
        with tf.device("/device:GPU:0"):
          gens = gen.split(count=10)  # gens are on GPU
        ```

        Args:
          count: the number of generators to return.

        Returns:
          A list (length `count`) of `Generator` objects independent of each other.
          The new generators have the same RNG algorithm as the old one.
        """
        ...

def all_candidate_sampler(
    true_classes: tf.Tensor, num_true: int, num_sampled: int, unique: bool, seed: int | None = None, name: str | None = None
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    """
    Generate the set of all classes.

    Deterministically generates and returns the set of all possible classes.
    For testing purposes.  There is no need to use this, since you might as
    well use full softmax or full logistic regression.

    Args:
      true_classes: A `Tensor` of type `int64` and shape `[batch_size,
        num_true]`. The target classes.
      num_true: An `int`.  The number of target classes per training example.
      num_sampled: An `int`.  The number of possible classes.
      unique: A `bool`. Ignored.
        unique.
      seed: An `int`. An operation-specific seed. Default is 0.
      name: A name for the operation (optional).

    Returns:
      sampled_candidates: A tensor of type `int64` and shape `[num_sampled]`.
        This operation deterministically returns the entire range
        `[0, num_sampled]`.
      true_expected_count: A tensor of type `float`.  Same shape as
        `true_classes`. The expected counts under the sampling distribution
        of each of `true_classes`. All returned values are 1.0.
      sampled_expected_count: A tensor of type `float`. Same shape as
        `sampled_candidates`. The expected counts under the sampling distribution
        of each of `sampled_candidates`. All returned values are 1.0.
    """
    ...
def categorical(
    logits: tf.Tensor,
    num_samples: int | tf.Tensor,
    dtype: DTypeLike | None = None,
    seed: int | None = None,
    name: str | None = None,
) -> tf.Tensor:
    """
    Draws samples from a categorical distribution.

    Example:

    ```python
    # samples has shape [1, 5], where each value is either 0 or 1 with equal
    # probability.
    samples = tf.random.categorical(tf.math.log([[0.5, 0.5]]), 5)
    ```

    Args:
      logits: 2-D Tensor with shape `[batch_size, num_classes]`.  Each slice
        `[i, :]` represents the unnormalized log-probabilities for all classes.
      num_samples: 0-D.  Number of independent samples to draw for each row slice.
      dtype: The integer type of the output: `int32` or `int64`. Defaults to
        `int64`.
      seed: A Python integer. Used to create a random seed for the distribution.
        See `tf.random.set_seed` for behavior.
      name: Optional name for the operation.

    Returns:
      The drawn samples of shape `[batch_size, num_samples]`.
    """
    ...
def create_rng_state(seed: int, alg: _Alg) -> npt.NDArray[np.int64]:
    """
    Creates a RNG state from an integer or a vector.

    Example:

    >>> tf.random.create_rng_state(
    ...     1234, "philox")
    <tf.Tensor: shape=(3,), dtype=int64, numpy=array([1234,    0,    0])>
    >>> tf.random.create_rng_state(
    ...     [12, 34], "threefry")
    <tf.Tensor: shape=(2,), dtype=int64, numpy=array([12, 34])>

    Args:
      seed: an integer or 1-D numpy array.
      alg: the RNG algorithm. Can be a string, an `Algorithm` or an integer.

    Returns:
      a 1-D numpy array whose size depends on the algorithm.
    """
    ...
def fixed_unigram_candidate_sampler(
    true_classes: tf.Tensor,
    num_true: int,
    num_sampled: int,
    unique: bool,
    range_max: int,
    vocab_file: str = "",
    distortion: float = 1.0,
    num_reserved_ids: int = 0,
    num_shards: int = 1,
    shard: int = 0,
    unigrams: Sequence[float] = (),
    seed: int | None = None,
    name: str | None = None,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    """
    Samples a set of classes using the provided (fixed) base distribution.

    This operation randomly samples a tensor of sampled classes
    (`sampled_candidates`) from the range of integers `[0, range_max)`.

    See the [Candidate Sampling Algorithms
    Reference](http://www.tensorflow.org/extras/candidate_sampling.pdf)
    for a quick course on Candidate Sampling.

    The elements of `sampled_candidates` are drawn without replacement
    (if `unique=True`) or with replacement (if `unique=False`) from
    the base distribution.

    The base distribution is read from a file or passed in as an
    in-memory array. There is also an option to skew the distribution by
    applying a distortion power to the weights.

    In addition, this operation returns tensors `true_expected_count`
    and `sampled_expected_count` representing the number of times each
    of the target classes (`true_classes`) and the sampled
    classes (`sampled_candidates`) is expected to occur in an average
    tensor of sampled classes.  These values correspond to `Q(y|x)`
    defined in the [Candidate Sampling Algorithms
    Reference](http://www.tensorflow.org/extras/candidate_sampling.pdf).
    If `unique=True`, then these are post-rejection probabilities and we
    compute them approximately.

    Note that this function (and also other `*_candidate_sampler`
    functions) only gives you the ingredients to implement the various
    Candidate Sampling algorithms listed in the big table in the
    [Candidate Sampling Algorithms
    Reference](http://www.tensorflow.org/extras/candidate_sampling.pdf). You
    still need to implement the algorithms yourself.

    For example, according to that table, the phrase "negative samples"
    may mean different things in different algorithms. For instance, in
    NCE, "negative samples" means `S_i` (which is just the sampled
    classes) which may overlap with true classes, while in Sampled
    Logistic, "negative samples" means `S_i - T_i` which excludes the
    true classes. The return value `sampled_candidates` corresponds to
    `S_i`, not to any specific definition of "negative samples" in any
    specific algorithm. It's your responsibility to pick an algorithm
    and calculate the "negative samples" defined by that algorithm
    (e.g. `S_i - T_i`).

    As another example, the `true_classes` argument is for calculating
    the `true_expected_count` output (as a by-product of this function's
    main calculation), which may be needed by some algorithms (according
    to that table). It's not for excluding true classes in the return
    value `sampled_candidates`. Again that step is algorithm-specific
    and should be carried out by you.

    Args:
      true_classes: A `Tensor` of type `int64` and shape `[batch_size,
        num_true]`. The target classes.
      num_true: An `int`.  The number of target classes per training example.
      num_sampled: An `int`.  The number of classes to randomly sample.
      unique: A `bool`. Determines whether all sampled classes in a batch are
        unique.
      range_max: An `int`. The number of possible classes.
      vocab_file: Each valid line in this file (which should have a CSV-like
        format) corresponds to a valid word ID. IDs are in sequential order,
        starting from num_reserved_ids. The last entry in each line is expected
        to be a value corresponding to the count or relative probability. Exactly
        one of `vocab_file` and `unigrams` needs to be passed to this operation.
      distortion: The distortion is used to skew the unigram probability
        distribution.  Each weight is first raised to the distortion's power
        before adding to the internal unigram distribution. As a result,
        `distortion = 1.0` gives regular unigram sampling (as defined by the vocab
        file), and `distortion = 0.0` gives a uniform distribution.
      num_reserved_ids: Optionally some reserved IDs can be added in the range
        `[0, num_reserved_ids)` by the users. One use case is that a special
        unknown word token is used as ID 0. These IDs will have a sampling
        probability of 0.
      num_shards: A sampler can be used to sample from a subset of the original
        range in order to speed up the whole computation through parallelism. This
        parameter (together with `shard`) indicates the number of partitions that
        are being used in the overall computation.
      shard: A sampler can be used to sample from a subset of the original range
        in order to speed up the whole computation through parallelism. This
        parameter (together with `num_shards`) indicates the particular partition
        number of the operation, when partitioning is being used.
      unigrams: A list of unigram counts or probabilities, one per ID in
        sequential order. Exactly one of `vocab_file` and `unigrams` should be
        passed to this operation.
      seed: An `int`. An operation-specific seed. Default is 0.
      name: A name for the operation (optional).

    Returns:
      sampled_candidates: A tensor of type `int64` and shape
        `[num_sampled]`. The sampled classes. As noted above,
        `sampled_candidates` may overlap with true classes.
      true_expected_count: A tensor of type `float`.  Same shape as
        `true_classes`. The expected counts under the sampling distribution
        of each of `true_classes`.
      sampled_expected_count: A tensor of type `float`. Same shape as
        `sampled_candidates`. The expected counts under the sampling distribution
        of each of `sampled_candidates`.
    """
    ...
def fold_in(seed: tf.Tensor | Sequence[int], data: int, alg: _Alg = "auto_select") -> int:
    """
    Folds in data to an RNG seed to form a new RNG seed.

    For example, in a distributed-training setting, suppose we have a master seed
    and a replica ID. We want to fold the replica ID into the master seed to
    form a "replica seed" to be used by that replica later on, so that different
    replicas will generate different random numbers but the reproducibility of the
    whole system can still be controlled by the master seed:

    >>> master_seed = [1, 2]
    >>> replica_id = 3
    >>> replica_seed = tf.random.experimental.stateless_fold_in(
    ...   master_seed, replica_id)
    >>> print(replica_seed)
    tf.Tensor([1105988140          3], shape=(2,), dtype=int32)
    >>> tf.random.stateless_normal(shape=[3], seed=replica_seed)
    <tf.Tensor: shape=(3,), dtype=float32, numpy=array([0.03197195, 0.8979765 ,
    0.13253039], dtype=float32)>

    Args:
      seed: an RNG seed (a tensor with shape [2] and dtype `int32` or `int64`).
        (When using XLA, only `int32` is allowed.)
      data: an `int32` or `int64` scalar representing data to be folded in to the
        seed.
      alg: The RNG algorithm used to generate the random numbers. See
        `tf.random.stateless_uniform` for a detailed explanation.

    Returns:
      A new RNG seed that is a deterministic function of the inputs and is
      statistically safe for producing a stream of new pseudo-random values. It
      will have the same dtype as `data` (if `data` doesn't have an explict dtype,
      the dtype will be determined by `tf.convert_to_tensor`).
    """
    ...
def gamma(
    shape: tf.Tensor | Sequence[int],
    alpha: tf.Tensor | float | Sequence[float],
    beta: tf.Tensor | float | Sequence[float] | None = None,
    dtype: DTypeLike = ...,
    seed: int | None = None,
    name: str | None = None,
) -> tf.Tensor:
    """
    Draws `shape` samples from each of the given Gamma distribution(s).

    `alpha` is the shape parameter describing the distribution(s), and `beta` is
    the inverse scale parameter(s).

    Note: Because internal calculations are done using `float64` and casting has
    `floor` semantics, we must manually map zero outcomes to the smallest
    possible positive floating-point value, i.e., `np.finfo(dtype).tiny`.  This
    means that `np.finfo(dtype).tiny` occurs more frequently than it otherwise
    should.  This bias can only happen for small values of `alpha`, i.e.,
    `alpha << 1` or large values of `beta`, i.e., `beta >> 1`.

    The samples are differentiable w.r.t. alpha and beta.
    The derivatives are computed using the approach described in
    (Figurnov et al., 2018).

    Example:

    ```python
    samples = tf.random.gamma([10], [0.5, 1.5])
    # samples has shape [10, 2], where each slice [:, 0] and [:, 1] represents
    # the samples drawn from each distribution

    samples = tf.random.gamma([7, 5], [0.5, 1.5])
    # samples has shape [7, 5, 2], where each slice [:, :, 0] and [:, :, 1]
    # represents the 7x5 samples drawn from each of the two distributions

    alpha = tf.constant([[1.],[3.],[5.]])
    beta = tf.constant([[3., 4.]])
    samples = tf.random.gamma([30], alpha=alpha, beta=beta)
    # samples has shape [30, 3, 2], with 30 samples each of 3x2 distributions.

    loss = tf.reduce_mean(tf.square(samples))
    dloss_dalpha, dloss_dbeta = tf.gradients(loss, [alpha, beta])
    # unbiased stochastic derivatives of the loss function
    alpha.shape == dloss_dalpha.shape  # True
    beta.shape == dloss_dbeta.shape  # True
    ```

    Args:
      shape: A 1-D integer Tensor or Python array. The shape of the output samples
        to be drawn per alpha/beta-parameterized distribution.
      alpha: A Tensor or Python value or N-D array of type `dtype`. `alpha`
        provides the shape parameter(s) describing the gamma distribution(s) to
        sample. Must be broadcastable with `beta`.
      beta: A Tensor or Python value or N-D array of type `dtype`. Defaults to 1.
        `beta` provides the inverse scale parameter(s) of the gamma
        distribution(s) to sample. Must be broadcastable with `alpha`.
      dtype: The type of alpha, beta, and the output: `float16`, `float32`, or
        `float64`.
      seed: A Python integer. Used to create a random seed for the distributions.
        See
        `tf.random.set_seed`
        for behavior.
      name: Optional name for the operation.

    Returns:
      samples: a `Tensor` of shape
        `tf.concat([shape, tf.shape(alpha + beta)], axis=0)` with values of type
        `dtype`.

    References:
      Implicit Reparameterization Gradients:
        [Figurnov et al., 2018]
        (http://papers.nips.cc/paper/7326-implicit-reparameterization-gradients)
        ([pdf]
        (http://papers.nips.cc/paper/7326-implicit-reparameterization-gradients.pdf))
    """
    ...
def get_global_generator() -> Generator:
    """
    Retrieves the global generator.

    This function will create the global generator the first time it is called,
    and the generator will be placed at the default device at that time, so one
    needs to be careful when this function is first called. Using a generator
    placed on a less-ideal device will incur performance regression.

    Returns:
      The global `tf.random.Generator` object.
    """
    ...
def learned_unigram_candidate_sampler(
    true_classes: tf.Tensor,
    num_true: int,
    num_sampled: int,
    unique: bool,
    range_max: int,
    seed: int | None = None,
    name: str | None = None,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    """
    Samples a set of classes from a distribution learned during training.

    This operation randomly samples a tensor of sampled classes
    (`sampled_candidates`) from the range of integers `[0, range_max)`.

    See the [Candidate Sampling Algorithms
    Reference](http://www.tensorflow.org/extras/candidate_sampling.pdf)
    for a quick course on Candidate Sampling.

    The elements of `sampled_candidates` are drawn without replacement
    (if `unique=True`) or with replacement (if `unique=False`) from
    the base distribution.

    The base distribution for this operation is constructed on the fly
    during training.  It is a unigram distribution over the target
    classes seen so far during training.  Every integer in `[0, range_max)`
    begins with a weight of 1, and is incremented by 1 each time it is
    seen as a target class.  The base distribution is not saved to checkpoints,
    so it is reset when the model is reloaded.

    In addition, this operation returns tensors `true_expected_count`
    and `sampled_expected_count` representing the number of times each
    of the target classes (`true_classes`) and the sampled
    classes (`sampled_candidates`) is expected to occur in an average
    tensor of sampled classes.  These values correspond to `Q(y|x)`
    defined in the [Candidate Sampling Algorithms
    Reference](http://www.tensorflow.org/extras/candidate_sampling.pdf).
    If `unique=True`, then these are post-rejection probabilities and we
    compute them approximately.

    Note that this function (and also other `*_candidate_sampler`
    functions) only gives you the ingredients to implement the various
    Candidate Sampling algorithms listed in the big table in the
    [Candidate Sampling Algorithms
    Reference](http://www.tensorflow.org/extras/candidate_sampling.pdf). You
    still need to implement the algorithms yourself.

    For example, according to that table, the phrase "negative samples"
    may mean different things in different algorithms. For instance, in
    NCE, "negative samples" means `S_i` (which is just the sampled
    classes) which may overlap with true classes, while in Sampled
    Logistic, "negative samples" means `S_i - T_i` which excludes the
    true classes. The return value `sampled_candidates` corresponds to
    `S_i`, not to any specific definition of "negative samples" in any
    specific algorithm. It's your responsibility to pick an algorithm
    and calculate the "negative samples" defined by that algorithm
    (e.g. `S_i - T_i`).

    As another example, the `true_classes` argument is for calculating
    the `true_expected_count` output (as a by-product of this function's
    main calculation), which may be needed by some algorithms (according
    to that table). It's not for excluding true classes in the return
    value `sampled_candidates`. Again that step is algorithm-specific
    and should be carried out by you.

    Args:
      true_classes: A `Tensor` of type `int64` and shape `[batch_size,
        num_true]`. The target classes.
      num_true: An `int`.  The number of target classes per training example.
      num_sampled: An `int`.  The number of classes to randomly sample.
      unique: A `bool`. Determines whether all sampled classes in a batch are
        unique.
      range_max: An `int`. The number of possible classes.
      seed: An `int`. An operation-specific seed. Default is 0.
      name: A name for the operation (optional).

    Returns:
      sampled_candidates: A tensor of type `int64` and shape
        `[num_sampled]`. The sampled classes. As noted above,
        `sampled_candidates` may overlap with true classes.
      true_expected_count: A tensor of type `float`.  Same shape as
        `true_classes`. The expected counts under the sampling distribution
        of each of `true_classes`.
      sampled_expected_count: A tensor of type `float`. Same shape as
        `sampled_candidates`. The expected counts under the sampling distribution
        of each of `sampled_candidates`.
    """
    ...
def log_uniform_candidate_sampler(
    true_classes: tf.Tensor,
    num_true: int,
    num_sampled: int,
    unique: bool,
    range_max: int,
    seed: int | None = None,
    name: str | None = None,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    """
    Samples a set of classes using a log-uniform (Zipfian) base distribution.

    This operation randomly samples a tensor of sampled classes
    (`sampled_candidates`) from the range of integers `[0, range_max)`.

    See the [Candidate Sampling Algorithms
    Reference](http://www.tensorflow.org/extras/candidate_sampling.pdf)
    for a quick course on Candidate Sampling.

    The elements of `sampled_candidates` are drawn without replacement
    (if `unique=True`) or with replacement (if `unique=False`) from
    the base distribution.

    The base distribution for this operation is an approximately log-uniform
    or Zipfian distribution:

    `P(class) = (log(class + 2) - log(class + 1)) / log(range_max + 1)`

    This sampler is useful when the target classes approximately follow such
    a distribution - for example, if the classes represent words in a lexicon
    sorted in decreasing order of frequency. If your classes are not ordered by
    decreasing frequency, do not use this op.

    In addition, this operation returns tensors `true_expected_count`
    and `sampled_expected_count` representing the number of times each
    of the target classes (`true_classes`) and the sampled
    classes (`sampled_candidates`) is expected to occur in an average
    tensor of sampled classes.  These values correspond to `Q(y|x)`
    defined in the [Candidate Sampling Algorithms
    Reference](http://www.tensorflow.org/extras/candidate_sampling.pdf).
    If `unique=True`, then these are post-rejection probabilities and we
    compute them approximately.

    Note that this function (and also other `*_candidate_sampler`
    functions) only gives you the ingredients to implement the various
    Candidate Sampling algorithms listed in the big table in the
    [Candidate Sampling Algorithms
    Reference](http://www.tensorflow.org/extras/candidate_sampling.pdf). You
    still need to implement the algorithms yourself.

    For example, according to that table, the phrase "negative samples"
    may mean different things in different algorithms. For instance, in
    NCE, "negative samples" means `S_i` (which is just the sampled
    classes) which may overlap with true classes, while in Sampled
    Logistic, "negative samples" means `S_i - T_i` which excludes the
    true classes. The return value `sampled_candidates` corresponds to
    `S_i`, not to any specific definition of "negative samples" in any
    specific algorithm. It's your responsibility to pick an algorithm
    and calculate the "negative samples" defined by that algorithm
    (e.g. `S_i - T_i`).

    As another example, the `true_classes` argument is for calculating
    the `true_expected_count` output (as a by-product of this function's
    main calculation), which may be needed by some algorithms (according
    to that table). It's not for excluding true classes in the return
    value `sampled_candidates`. Again that step is algorithm-specific
    and should be carried out by you.

    Args:
      true_classes: A `Tensor` of type `int64` and shape `[batch_size,
        num_true]`. The target classes.
      num_true: An `int`.  The number of target classes per training example.
      num_sampled: An `int`.  The number of classes to randomly sample.
      unique: A `bool`. Determines whether all sampled classes in a batch are
        unique.
      range_max: An `int`. The number of possible classes.
      seed: An `int`. An operation-specific seed. Default is 0.
      name: A name for the operation (optional).

    Returns:
      sampled_candidates: A tensor of type `int64` and shape
        `[num_sampled]`. The sampled classes. As noted above,
        `sampled_candidates` may overlap with true classes.
      true_expected_count: A tensor of type `float`.  Same shape as
        `true_classes`. The expected counts under the sampling distribution
        of each of `true_classes`.
      sampled_expected_count: A tensor of type `float`. Same shape as
        `sampled_candidates`. The expected counts under the sampling distribution
        of each of `sampled_candidates`.
    """
    ...
def normal(
    shape: ShapeLike,
    mean: ScalarTensorCompatible = 0.0,
    stddev: ScalarTensorCompatible = 1.0,
    dtype: DTypeLike = ...,
    seed: int | None = None,
    name: str | None = None,
) -> tf.Tensor:
    """
    Outputs random values from a normal distribution.

    Example that generates a new set of random values every time:

    >>> tf.random.set_seed(5);
    >>> tf.random.normal([4], 0, 1, tf.float32)
    <tf.Tensor: shape=(4,), dtype=float32, numpy=..., dtype=float32)>

    Example that outputs a reproducible result:

    >>> tf.random.set_seed(5);
    >>> tf.random.normal([2,2], 0, 1, tf.float32, seed=1)
    <tf.Tensor: shape=(2, 2), dtype=float32, numpy=
    array([[-1.3768897 , -0.01258316],
          [-0.169515   ,  1.0824056 ]], dtype=float32)>

    In this case, we are setting both the global and operation-level seed to
    ensure this result is reproducible.  See `tf.random.set_seed` for more
    information.

    Args:
      shape: A 1-D integer Tensor or Python array. The shape of the output tensor.
      mean: A Tensor or Python value of type `dtype`, broadcastable with `stddev`.
        The mean of the normal distribution.
      stddev: A Tensor or Python value of type `dtype`, broadcastable with `mean`.
        The standard deviation of the normal distribution.
      dtype: The float type of the output: `float16`, `bfloat16`, `float32`,
        `float64`. Defaults to `float32`.
      seed: A Python integer. Used to create a random seed for the distribution.
        See
        `tf.random.set_seed`
        for behavior.
      name: A name for the operation (optional).

    Returns:
      A tensor of the specified shape filled with random normal values.
    """
    ...
def poisson(
    shape: ShapeLike, lam: ScalarTensorCompatible, dtype: DTypeLike = ..., seed: int | None = None, name: str | None = None
) -> tf.Tensor:
    """
    Draws `shape` samples from each of the given Poisson distribution(s).

    `lam` is the rate parameter describing the distribution(s).

    Example:

    ```python
    samples = tf.random.poisson([10], [0.5, 1.5])
    # samples has shape [10, 2], where each slice [:, 0] and [:, 1] represents
    # the samples drawn from each distribution

    samples = tf.random.poisson([7, 5], [12.2, 3.3])
    # samples has shape [7, 5, 2], where each slice [:, :, 0] and [:, :, 1]
    # represents the 7x5 samples drawn from each of the two distributions
    ```

    Args:
      shape: A 1-D integer Tensor or Python array. The shape of the output samples
        to be drawn per "rate"-parameterized distribution.
      lam: A Tensor or Python value or N-D array of type `dtype`.
        `lam` provides the rate parameter(s) describing the poisson
        distribution(s) to sample.
      dtype: The type of the output: `float16`, `float32`, `float64`, `int32` or
        `int64`.
      seed: A Python integer. Used to create a random seed for the distributions.
        See
        `tf.random.set_seed`
        for behavior.
      name: Optional name for the operation.

    Returns:
      samples: a `Tensor` of shape `tf.concat([shape, tf.shape(lam)], axis=0)`
        with values of type `dtype`.
    """
    ...
def set_global_generator(generator: Generator) -> None:
    """
    Replaces the global generator with another `Generator` object.

    This function replaces the global generator with the provided `generator`
    object.
    A random number generator utilizes a `tf.Variable` object to store its state.
    The user shall be aware of caveats how `set_global_generator` interacts with
    `tf.function`:

    - tf.function puts restrictions on Variable creation thus one cannot freely
      create a new random generator instance inside `tf.function`.
      To call `set_global_generator` inside `tf.function`, the generator instance
      must have already been created eagerly.
    - tf.function captures the Variable during trace-compilation, thus a compiled
      f.function will not be affected `set_global_generator` as demonstrated by
      random_test.py/RandomTest.testResetGlobalGeneratorBadWithDefun .

    For most use cases, avoid calling `set_global_generator` after program
    initialization, and prefer to reset the state of the existing global generator
    instead, such as,

    >>> rng = tf.random.get_global_generator()
    >>> rng.reset_from_seed(30)


    Args:
      generator: the new `Generator` object.
    """
    ...
def set_seed(seed: int) -> None:
    """
    Sets the global random seed.

    Operations that rely on a random seed actually derive it from two seeds:
    the global and operation-level seeds. This sets the global seed.

    Its interactions with operation-level seeds is as follows:

      1. If neither the global seed nor the operation seed is set: A randomly
        picked seed is used for this op.
      2. If the global seed is set, but the operation seed is not:
        The system deterministically picks an operation seed in conjunction with
        the global seed so that it gets a unique random sequence. Within the
        same version of tensorflow and user code, this sequence is deterministic.
        However across different versions, this sequence might change. If the
        code depends on particular seeds to work, specify both global
        and operation-level seeds explicitly.
      3. If the operation seed is set, but the global seed is not set:
        A default global seed and the specified operation seed are used to
        determine the random sequence.
      4. If both the global and the operation seed are set:
        Both seeds are used in conjunction to determine the random sequence.

    To illustrate the user-visible effects, consider these examples:

    If neither the global seed nor the operation seed is set, we get different
    results for every call to the random op and every re-run of the program:

    ```python
    print(tf.random.uniform([1]))  # generates 'A1'
    print(tf.random.uniform([1]))  # generates 'A2'
    ```

    (now close the program and run it again)

    ```python
    print(tf.random.uniform([1]))  # generates 'A3'
    print(tf.random.uniform([1]))  # generates 'A4'
    ```

    If the global seed is set but the operation seed is not set, we get different
    results for every call to the random op, but the same sequence for every
    re-run of the program:

    ```python
    tf.random.set_seed(1234)
    print(tf.random.uniform([1]))  # generates 'A1'
    print(tf.random.uniform([1]))  # generates 'A2'
    ```

    (now close the program and run it again)

    ```python
    tf.random.set_seed(1234)
    print(tf.random.uniform([1]))  # generates 'A1'
    print(tf.random.uniform([1]))  # generates 'A2'
    ```

    The reason we get 'A2' instead 'A1' on the second call of `tf.random.uniform`
    above is because the second call uses a different operation seed.

    Note that `tf.function` acts like a re-run of a program in this case. When
    the global seed is set but operation seeds are not set, the sequence of random
    numbers are the same for each `tf.function`. For example:

    ```python
    tf.random.set_seed(1234)

    @tf.function
    def f():
      a = tf.random.uniform([1])
      b = tf.random.uniform([1])
      return a, b

    @tf.function
    def g():
      a = tf.random.uniform([1])
      b = tf.random.uniform([1])
      return a, b

    print(f())  # prints '(A1, A2)'
    print(g())  # prints '(A1, A2)'
    ```

    If the operation seed is set, we get different results for every call to the
    random op, but the same sequence for every re-run of the program:

    ```python
    print(tf.random.uniform([1], seed=1))  # generates 'A1'
    print(tf.random.uniform([1], seed=1))  # generates 'A2'
    ```

    (now close the program and run it again)

    ```python
    print(tf.random.uniform([1], seed=1))  # generates 'A1'
    print(tf.random.uniform([1], seed=1))  # generates 'A2'
    ```

    The reason we get 'A2' instead 'A1' on the second call of `tf.random.uniform`
    above is because the same `tf.random.uniform` kernel (i.e. internal
    representation) is used by TensorFlow for all calls of it with the same
    arguments, and the kernel maintains an internal counter which is incremented
    every time it is executed, generating different results.

    Calling `tf.random.set_seed` will reset any such counters:

    ```python
    tf.random.set_seed(1234)
    print(tf.random.uniform([1], seed=1))  # generates 'A1'
    print(tf.random.uniform([1], seed=1))  # generates 'A2'
    tf.random.set_seed(1234)
    print(tf.random.uniform([1], seed=1))  # generates 'A1'
    print(tf.random.uniform([1], seed=1))  # generates 'A2'
    ```

    When multiple identical random ops are wrapped in a `tf.function`, their
    behaviors change because the ops no long share the same counter. For example:

    ```python
    @tf.function
    def foo():
      a = tf.random.uniform([1], seed=1)
      b = tf.random.uniform([1], seed=1)
      return a, b
    print(foo())  # prints '(A1, A1)'
    print(foo())  # prints '(A2, A2)'

    @tf.function
    def bar():
      a = tf.random.uniform([1])
      b = tf.random.uniform([1])
      return a, b
    print(bar())  # prints '(A1, A2)'
    print(bar())  # prints '(A3, A4)'
    ```

    The second call of `foo` returns '(A2, A2)' instead of '(A1, A1)' because
    `tf.random.uniform` maintains an internal counter. If you want `foo` to return
    '(A1, A1)' every time, use the stateless random ops such as
    `tf.random.stateless_uniform`. Also see `tf.random.experimental.Generator` for
    a new set of stateful random ops that use external variables to manage their
    states.

    Args:
      seed: integer.
    """
    ...
def shuffle(value: tf.Tensor, seed: int | None = None, name: str | None = None) -> tf.Tensor:
    """
    Randomly shuffles a tensor along its first dimension.

    The tensor is shuffled along dimension 0, such that each `value[j]` is mapped
    to one and only one `output[i]`. For example, a mapping that might occur for a
    3x2 tensor is:

    ```python
    [[1, 2],       [[5, 6],
     [3, 4],  ==>   [1, 2],
     [5, 6]]        [3, 4]]
    ```

    Args:
      value: A Tensor to be shuffled.
      seed: A Python integer. Used to create a random seed for the distribution.
        See
        `tf.random.set_seed`
        for behavior.
      name: A name for the operation (optional).

    Returns:
      A tensor of same shape and type as `value`, shuffled along its first
      dimension.
    """
    ...
def split(seed: tf.Tensor | Sequence[int], num: int = 2, alg: _Alg = "auto_select") -> tf.Tensor:
    """
    Splits an RNG seed into `num` new seeds by adding a leading axis.

    Example:

    >>> seed = [1, 2]
    >>> new_seeds = tf.random.split(seed, num=3)
    >>> print(new_seeds)
    tf.Tensor(
    [[1105988140 1738052849]
     [-335576002  370444179]
     [  10670227 -246211131]], shape=(3, 2), dtype=int32)
    >>> tf.random.stateless_normal(shape=[3], seed=new_seeds[0, :])
    <tf.Tensor: shape=(3,), dtype=float32, numpy=array([-0.59835213, -0.9578608 ,
    0.9002807 ], dtype=float32)>

    Args:
      seed: an RNG seed (a tensor with shape [2] and dtype `int32` or `int64`).
        (When using XLA, only `int32` is allowed.)
      num: optional, a positive integer or scalar tensor indicating the number of
        seeds to produce (default 2).
      alg: The RNG algorithm used to generate the random numbers. See
        `tf.random.stateless_uniform` for a detailed explanation.

    Returns:
      A tensor with shape [num, 2] representing `num` new seeds. It will have the
      same dtype as `seed` (if `seed` doesn't have an explict dtype, the dtype
      will be determined by `tf.convert_to_tensor`).
    """
    ...
def stateless_binomial(
    shape: ShapeLike,
    seed: tuple[int, int] | tf.Tensor,
    counts: tf.Tensor,
    probs: tf.Tensor,
    output_dtype: DTypeLike = ...,
    name: str | None = None,
) -> tf.Tensor:
    """
    Outputs deterministic pseudorandom values from a binomial distribution.

    The generated values follow a binomial distribution with specified count and
    probability of success parameters.

    This is a stateless version of `tf.random.Generator.binomial`: if run twice
    with the same seeds and shapes, it will produce the same pseudorandom numbers.
    The output is consistent across multiple runs on the same hardware (and
    between CPU and GPU), but may change between versions of TensorFlow or on
    non-CPU/GPU hardware.

    Example:

    ```python
    counts = [10., 20.]
    # Probability of success.
    probs = [0.8]

    binomial_samples = tf.random.stateless_binomial(
        shape=[2], seed=[123, 456], counts=counts, probs=probs)

    counts = ... # Shape [3, 1, 2]
    probs = ...  # Shape [1, 4, 2]
    shape = [3, 4, 3, 4, 2]
    # Sample shape will be [3, 4, 3, 4, 2]
    binomial_samples = tf.random.stateless_binomial(
        shape=shape, seed=[123, 456], counts=counts, probs=probs)
    ```

    Args:
      shape: A 1-D integer Tensor or Python array. The shape of the output tensor.
      seed: A shape [2] Tensor, the seed to the random number generator. Must have
        dtype `int32` or `int64`. (When using XLA, only `int32` is allowed.)
      counts: Tensor. The counts of the binomial distribution. Must be
        broadcastable with `probs`, and broadcastable with the rightmost
        dimensions of `shape`.
      probs: Tensor. The probability of success for the binomial distribution.
        Must be broadcastable with `counts` and broadcastable with the rightmost
        dimensions of `shape`.
      output_dtype: The type of the output. Default: tf.int32
      name: A name for the operation (optional).

    Returns:
      samples: A Tensor of the specified shape filled with random binomial
        values.  For each i, each samples[..., i] is an independent draw from
        the binomial distribution on counts[i] trials with probability of
        success probs[i].
    """
    ...
def stateless_categorical(
    logits: tf.Tensor,
    num_samples: int | tf.Tensor,
    seed: tuple[int, int] | tf.Tensor,
    dtype: DTypeLike = ...,
    name: str | None = None,
) -> tf.Tensor:
    """
    Draws deterministic pseudorandom samples from a categorical distribution.

    This is a stateless version of `tf.categorical`: if run twice with the
    same seeds and shapes, it will produce the same pseudorandom numbers.  The
    output is consistent across multiple runs on the same hardware (and between
    CPU and GPU), but may change between versions of TensorFlow or on non-CPU/GPU
    hardware.


    Example:

    ```python
    # samples has shape [1, 5], where each value is either 0 or 1 with equal
    # probability.
    samples = tf.random.stateless_categorical(
        tf.math.log([[0.5, 0.5]]), 5, seed=[7, 17])
    ```

    Args:
      logits: 2-D Tensor with shape `[batch_size, num_classes]`.  Each slice `[i,
        :]` represents the unnormalized log-probabilities for all classes.
      num_samples: 0-D.  Number of independent samples to draw for each row slice.
      seed: A shape [2] Tensor, the seed to the random number generator. Must have
        dtype `int32` or `int64`. (When using XLA, only `int32` is allowed.)
      dtype: The integer type of the output: `int32` or `int64`. Defaults to
        `int64`.
      name: Optional name for the operation.

    Returns:
      The drawn samples of shape `[batch_size, num_samples]`.
    """
    ...
def stateless_gamma(
    shape: ShapeLike,
    seed: tuple[int, int] | tf.Tensor,
    alpha: tf.Tensor,
    beta: tf.Tensor | None = None,
    dtype: DTypeLike = ...,
    name: str | None = None,
) -> tf.Tensor:
    """
    Outputs deterministic pseudorandom values from a gamma distribution.

    The generated values follow a gamma distribution with specified concentration
    (`alpha`) and inverse scale (`beta`) parameters.

    This is a stateless version of `tf.random.gamma`: if run twice with the same
    seeds and shapes, it will produce the same pseudorandom numbers. The output is
    consistent across multiple runs on the same hardware (and between CPU and
    GPU),
    but may change between versions of TensorFlow or on non-CPU/GPU hardware.

    A slight difference exists in the interpretation of the `shape` parameter
    between `stateless_gamma` and `gamma`: in `gamma`, the `shape` is always
    prepended to the shape of the broadcast of `alpha` with `beta`; whereas in
    `stateless_gamma` the `shape` parameter must always encompass the shapes of
    each of `alpha` and `beta` (which must broadcast together to match the
    trailing dimensions of `shape`).

    Note: Because internal calculations are done using `float64` and casting has
    `floor` semantics, we must manually map zero outcomes to the smallest
    possible positive floating-point value, i.e., `np.finfo(dtype).tiny`.  This
    means that `np.finfo(dtype).tiny` occurs more frequently than it otherwise
    should.  This bias can only happen for small values of `alpha`, i.e.,
    `alpha << 1` or large values of `beta`, i.e., `beta >> 1`.

    The samples are differentiable w.r.t. alpha and beta.
    The derivatives are computed using the approach described in
    (Figurnov et al., 2018).

    Example:

    ```python
    samples = tf.random.stateless_gamma([10, 2], seed=[12, 34], alpha=[0.5, 1.5])
    # samples has shape [10, 2], where each slice [:, 0] and [:, 1] represents
    # the samples drawn from each distribution

    samples = tf.random.stateless_gamma([7, 5, 2], seed=[12, 34], alpha=[.5, 1.5])
    # samples has shape [7, 5, 2], where each slice [:, :, 0] and [:, :, 1]
    # represents the 7x5 samples drawn from each of the two distributions

    alpha = tf.constant([[1.], [3.], [5.]])
    beta = tf.constant([[3., 4.]])
    samples = tf.random.stateless_gamma(
        [30, 3, 2], seed=[12, 34], alpha=alpha, beta=beta)
    # samples has shape [30, 3, 2], with 30 samples each of 3x2 distributions.

    with tf.GradientTape() as tape:
      tape.watch([alpha, beta])
      loss = tf.reduce_mean(tf.square(tf.random.stateless_gamma(
          [30, 3, 2], seed=[12, 34], alpha=alpha, beta=beta)))
    dloss_dalpha, dloss_dbeta = tape.gradient(loss, [alpha, beta])
    # unbiased stochastic derivatives of the loss function
    alpha.shape == dloss_dalpha.shape  # True
    beta.shape == dloss_dbeta.shape  # True
    ```

    Args:
      shape: A 1-D integer Tensor or Python array. The shape of the output tensor.
      seed: A shape [2] Tensor, the seed to the random number generator. Must have
        dtype `int32` or `int64`. (When using XLA, only `int32` is allowed.)
      alpha: Tensor. The concentration parameter of the gamma distribution. Must
        be broadcastable with `beta`, and broadcastable with the rightmost
        dimensions of `shape`.
      beta: Tensor. The inverse scale parameter of the gamma distribution. Must be
        broadcastable with `alpha` and broadcastable with the rightmost dimensions
        of `shape`.
      dtype: Floating point dtype of `alpha`, `beta`, and the output.
      name: A name for the operation (optional).

    Returns:
      samples: A Tensor of the specified shape filled with random gamma values.
        For each i, each `samples[..., i] is an independent draw from the gamma
        distribution with concentration alpha[i] and scale beta[i].
    """
    ...
def stateless_normal(
    shape: tf.Tensor | Sequence[int],
    seed: tuple[int, int] | tf.Tensor,
    mean: float | tf.Tensor = 0.0,
    stddev: float | tf.Tensor = 1.0,
    dtype: DTypeLike = ...,
    name: str | None = None,
    alg: _Alg = "auto_select",
) -> tf.Tensor:
    """
    Outputs deterministic pseudorandom values from a normal distribution.

    This is a stateless version of `tf.random.normal`: if run twice with the
    same seeds and shapes, it will produce the same pseudorandom numbers.  The
    output is consistent across multiple runs on the same hardware (and between
    CPU and GPU), but may change between versions of TensorFlow or on non-CPU/GPU
    hardware.

    Args:
      shape: A 1-D integer Tensor or Python array. The shape of the output tensor.
      seed: A shape [2] Tensor, the seed to the random number generator. Must have
        dtype `int32` or `int64`. (When using XLA, only `int32` is allowed.)
      mean: A 0-D Tensor or Python value of type `dtype`. The mean of the normal
        distribution.
      stddev: A 0-D Tensor or Python value of type `dtype`. The standard deviation
        of the normal distribution.
      dtype: The float type of the output: `float16`, `bfloat16`, `float32`,
        `float64`. Defaults to `float32`.
      name: A name for the operation (optional).
      alg: The RNG algorithm used to generate the random numbers. See
        `tf.random.stateless_uniform` for a detailed explanation.

    Returns:
      A tensor of the specified shape filled with random normal values.
    """
    ...
def stateless_parameterized_truncated_normal(
    shape: tf.Tensor | Sequence[int],
    seed: tuple[int, int] | tf.Tensor,
    means: float | tf.Tensor = 0.0,
    stddevs: float | tf.Tensor = 1.0,
    minvals: tf.Tensor | float = -2.0,
    maxvals: tf.Tensor | float = 2.0,
    name: str | None = None,
) -> tf.Tensor:
    """
    Outputs random values from a truncated normal distribution.

    The generated values follow a normal distribution with specified mean and
    standard deviation, except that values whose magnitude is more than 2 standard
    deviations from the mean are dropped and re-picked.


    Examples:

    Sample from a Truncated normal, with deferring shape parameters that
    broadcast.

    >>> means = 0.
    >>> stddevs = tf.math.exp(tf.random.uniform(shape=[2, 3]))
    >>> minvals = [-1., -2., -1000.]
    >>> maxvals = [[10000.], [1.]]
    >>> y = tf.random.stateless_parameterized_truncated_normal(
    ...   shape=[10, 2, 3], seed=[7, 17],
    ...   means=means, stddevs=stddevs, minvals=minvals, maxvals=maxvals)
    >>> y.shape
    TensorShape([10, 2, 3])

    Args:
      shape: A 1-D integer `Tensor` or Python array. The shape of the output
        tensor.
      seed: A shape [2] Tensor, the seed to the random number generator. Must have
        dtype `int32` or `int64`. (When using XLA, only `int32` is allowed.)
      means: A `Tensor` or Python value of type `dtype`. The mean of the truncated
        normal distribution. This must broadcast with `stddevs`, `minvals` and
        `maxvals`, and the broadcasted shape must be dominated by `shape`.
      stddevs: A `Tensor` or Python value of type `dtype`. The standard deviation
        of the truncated normal distribution. This must broadcast with `means`,
        `minvals` and `maxvals`, and the broadcasted shape must be dominated by
        `shape`.
      minvals: A `Tensor` or Python value of type `dtype`. The minimum value of
        the truncated normal distribution. This must broadcast with `means`,
        `stddevs` and `maxvals`, and the broadcasted shape must be dominated by
        `shape`.
      maxvals: A `Tensor` or Python value of type `dtype`. The maximum value of
        the truncated normal distribution. This must broadcast with `means`,
        `stddevs` and `minvals`, and the broadcasted shape must be dominated by
        `shape`.
      name: A name for the operation (optional).

    Returns:
      A tensor of the specified shape filled with random truncated normal values.
    """
    ...
def stateless_poisson(
    shape: tf.Tensor | Sequence[int],
    seed: tuple[int, int] | tf.Tensor,
    lam: tf.Tensor,
    dtype: DTypeLike = ...,
    name: str | None = None,
) -> tf.Tensor:
    """
    Outputs deterministic pseudorandom values from a Poisson distribution.

    The generated values follow a Poisson distribution with specified rate
    parameter.

    This is a stateless version of `tf.random.poisson`: if run twice with the same
    seeds and shapes, it will produce the same pseudorandom numbers. The output is
    consistent across multiple runs on the same hardware, but may change between
    versions of TensorFlow or on non-CPU/GPU hardware.

    A slight difference exists in the interpretation of the `shape` parameter
    between `stateless_poisson` and `poisson`: in `poisson`, the `shape` is always
    prepended to the shape of `lam`; whereas in `stateless_poisson` the shape of
    `lam` must match the trailing dimensions of `shape`.

    Example:

    ```python
    samples = tf.random.stateless_poisson([10, 2], seed=[12, 34], lam=[5, 15])
    # samples has shape [10, 2], where each slice [:, 0] and [:, 1] represents
    # the samples drawn from each distribution

    samples = tf.random.stateless_poisson([7, 5, 2], seed=[12, 34], lam=[5, 15])
    # samples has shape [7, 5, 2], where each slice [:, :, 0] and [:, :, 1]
    # represents the 7x5 samples drawn from each of the two distributions

    rate = tf.constant([[1.], [3.], [5.]])
    samples = tf.random.stateless_poisson([30, 3, 1], seed=[12, 34], lam=rate)
    # samples has shape [30, 3, 1], with 30 samples each of 3x1 distributions.
    ```

    Args:
      shape: A 1-D integer Tensor or Python array. The shape of the output tensor.
      seed: A shape [2] Tensor, the seed to the random number generator. Must have
        dtype `int32` or `int64`. (When using XLA, only `int32` is allowed.)
      lam: Tensor. The rate parameter "lambda" of the Poisson distribution. Shape
        must match the rightmost dimensions of `shape`.
      dtype: Dtype of the samples (int or float dtypes are permissible, as samples
        are discrete). Default: int32.
      name: A name for the operation (optional).

    Returns:
      samples: A Tensor of the specified shape filled with random Poisson values.
        For each i, each `samples[..., i]` is an independent draw from the Poisson
        distribution with rate `lam[i]`.
    """
    ...
def stateless_truncated_normal(
    shape: tf.Tensor | Sequence[int],
    seed: tuple[int, int] | tf.Tensor,
    mean: float | tf.Tensor = 0.0,
    stddev: float | tf.Tensor = 1.0,
    dtype: DTypeLike = ...,
    name: str | None = None,
    alg: _Alg = "auto_select",
) -> tf.Tensor:
    """
    Outputs deterministic pseudorandom values, truncated normally distributed.

    This is a stateless version of `tf.random.truncated_normal`: if run twice with
    the same seeds and shapes, it will produce the same pseudorandom numbers.  The
    output is consistent across multiple runs on the same hardware (and between
    CPU and GPU), but may change between versions of TensorFlow or on non-CPU/GPU
    hardware.

    The generated values follow a normal distribution with specified mean and
    standard deviation, except that values whose magnitude is more than 2 standard
    deviations from the mean are dropped and re-picked.

    Args:
      shape: A 1-D integer Tensor or Python array. The shape of the output tensor.
      seed: A shape [2] Tensor, the seed to the random number generator. Must have
        dtype `int32` or `int64`. (When using XLA, only `int32` is allowed.)
      mean: A 0-D Tensor or Python value of type `dtype`. The mean of the
        truncated normal distribution.
      stddev: A 0-D Tensor or Python value of type `dtype`. The standard deviation
        of the normal distribution, before truncation.
      dtype: The type of the output.
      name: A name for the operation (optional).
      alg: The RNG algorithm used to generate the random numbers. See
        `tf.random.stateless_uniform` for a detailed explanation.

    Returns:
      A tensor of the specified shape filled with random truncated normal values.
    """
    ...
def stateless_uniform(
    shape: tf.Tensor | Sequence[int],
    seed: tuple[int, int] | tf.Tensor,
    minval: float | tf.Tensor = 0,
    maxval: float | tf.Tensor | None = None,
    dtype: DTypeLike = ...,
    name: str | None = None,
    alg: _Alg = "auto_select",
) -> tf.Tensor:
    """
    Outputs deterministic pseudorandom values from a uniform distribution.

    This is a stateless version of `tf.random.uniform`: if run twice with the
    same seeds and shapes, it will produce the same pseudorandom numbers.  The
    output is consistent across multiple runs on the same hardware (and between
    CPU and GPU), but may change between versions of TensorFlow or on non-CPU/GPU
    hardware.

    The generated values follow a uniform distribution in the range
    `[minval, maxval)`. The lower bound `minval` is included in the range, while
    the upper bound `maxval` is excluded.

    For floats, the default range is `[0, 1)`.  For ints, at least `maxval` must
    be specified explicitly.

    In the integer case, the random integers are slightly biased unless
    `maxval - minval` is an exact power of two.  The bias is small for values of
    `maxval - minval` significantly smaller than the range of the output (either
    `2**32` or `2**64`).

    For full-range (i.e. inclusive of both max and min) random integers, pass
    `minval=None` and `maxval=None` with an integer `dtype`. For an integer dtype
    either both `minval` and `maxval` must be `None` or neither may be `None`. For
    example:
    ```python
    ints = tf.random.stateless_uniform(
        [10], seed=(2, 3), minval=None, maxval=None, dtype=tf.int32)
    ```

    Args:
      shape: A 1-D integer Tensor or Python array. The shape of the output tensor.
      seed: A shape [2] Tensor, the seed to the random number generator. Must have
        dtype `int32` or `int64`. (When using XLA, only `int32` is allowed.)
      minval: A Tensor or Python value of type `dtype`, broadcastable with `shape`
        (for integer types, broadcasting is not supported, so it needs to be a
        scalar). The lower bound on the range of random values to generate. Pass
        `None` for full-range integers.  Defaults to 0.
      maxval: A Tensor or Python value of type `dtype`, broadcastable with `shape`
        (for integer types, broadcasting is not supported, so it needs to be a
        scalar). The upper bound on the range of random values to generate.
        Defaults to 1 if `dtype` is floating point. Pass `None` for full-range
        integers.
      dtype: The type of the output: `float16`, `bfloat16`, `float32`, `float64`,
        `int32`, or `int64`. For unbounded uniform ints (`minval`, `maxval` both
        `None`), `uint32` and `uint64` may be used. Defaults to `float32`.
      name: A name for the operation (optional).
      alg: The RNG algorithm used to generate the random numbers. Valid choices
        are `"philox"` for [the Philox
        algorithm](https://www.thesalmons.org/john/random123/papers/random123sc11.pdf),
        `"threefry"` for [the ThreeFry
        algorithm](https://www.thesalmons.org/john/random123/papers/random123sc11.pdf),
        and `"auto_select"` (default) for the system to automatically select an
        algorithm based the device type. Values of `tf.random.Algorithm` can also
        be used. Note that with `"auto_select"`, the outputs of this function may
        change when it is running on a different device.

    Returns:
      A tensor of the specified shape filled with random uniform values.

    Raises:
      ValueError: If `dtype` is integral and only one of `minval` or `maxval` is
        specified.
    """
    ...
def truncated_normal(
    shape: tf.Tensor | Sequence[int],
    mean: float | tf.Tensor = 0.0,
    stddev: float | tf.Tensor = 1.0,
    dtype: DTypeLike = ...,
    seed: int | None = None,
    name: str | None = None,
) -> tf.Tensor:
    """
    Outputs random values from a truncated normal distribution.

    The values are drawn from a normal distribution with specified mean and
    standard deviation, discarding and re-drawing any samples that are more than
    two standard deviations from the mean.

    Examples:

    >>> tf.random.truncated_normal(shape=[2])
    <tf.Tensor: shape=(2,), dtype=float32, numpy=array([..., ...], dtype=float32)>

    >>> tf.random.truncated_normal(shape=[2], mean=3, stddev=1, dtype=tf.float32)
    <tf.Tensor: shape=(2,), dtype=float32, numpy=array([..., ...], dtype=float32)>

    Args:
      shape: A 1-D integer Tensor or Python array. The shape of the output tensor.
      mean: A 0-D Tensor or Python value of type `dtype`. The mean of the
        truncated normal distribution.
      stddev: A 0-D Tensor or Python value of type `dtype`. The standard deviation
        of the normal distribution, before truncation.
      dtype: The type of the output. Restricted to floating-point types:
        `tf.half`, `tf.float`, `tf.double`, etc.
      seed: A Python integer. Used to create a random seed for the distribution.
        See `tf.random.set_seed` for more information.
      name: A name for the operation (optional).

    Returns:
      A tensor of the specified shape filled with random truncated normal values.
    """
    ...
def uniform(
    shape: tf.Tensor | Sequence[int],
    minval: float | tf.Tensor = 0,
    maxval: float | tf.Tensor | None = None,
    dtype: DTypeLike = ...,
    seed: int | None = None,
    name: str | None = None,
) -> tf.Tensor:
    """
    Outputs random values from a uniform distribution.

    The generated values follow a uniform distribution in the range
    `[minval, maxval)`. The lower bound `minval` is included in the range, while
    the upper bound `maxval` is excluded.

    For floats, the default range is `[0, 1)`.  For ints, at least `maxval` must
    be specified explicitly.

    In the integer case, the random integers are slightly biased unless
    `maxval - minval` is an exact power of two.  The bias is small for values of
    `maxval - minval` significantly smaller than the range of the output (either
    `2**32` or `2**64`).

    Examples:

    >>> tf.random.uniform(shape=[2])
    <tf.Tensor: shape=(2,), dtype=float32, numpy=array([..., ...], dtype=float32)>
    >>> tf.random.uniform(shape=[], minval=-1., maxval=0.)
    <tf.Tensor: shape=(), dtype=float32, numpy=-...>
    >>> tf.random.uniform(shape=[], minval=5, maxval=10, dtype=tf.int64)
    <tf.Tensor: shape=(), dtype=int64, numpy=...>

    The `seed` argument produces a deterministic sequence of tensors across
    multiple calls. To repeat that sequence, use `tf.random.set_seed`:

    >>> tf.random.set_seed(5)
    >>> tf.random.uniform(shape=[], maxval=3, dtype=tf.int32, seed=10)
    <tf.Tensor: shape=(), dtype=int32, numpy=2>
    >>> tf.random.uniform(shape=[], maxval=3, dtype=tf.int32, seed=10)
    <tf.Tensor: shape=(), dtype=int32, numpy=0>
    >>> tf.random.set_seed(5)
    >>> tf.random.uniform(shape=[], maxval=3, dtype=tf.int32, seed=10)
    <tf.Tensor: shape=(), dtype=int32, numpy=2>
    >>> tf.random.uniform(shape=[], maxval=3, dtype=tf.int32, seed=10)
    <tf.Tensor: shape=(), dtype=int32, numpy=0>

    Without `tf.random.set_seed` but with a `seed` argument is specified, small
    changes to function graphs or previously executed operations will change the
    returned value. See `tf.random.set_seed` for details.

    Args:
      shape: A 1-D integer Tensor or Python array. The shape of the output tensor.
      minval: A Tensor or Python value of type `dtype`, broadcastable with
        `shape` (for integer types, broadcasting is not supported, so it needs to
        be a scalar). The lower bound on the range of random values to generate
        (inclusive).  Defaults to 0.
      maxval: A Tensor or Python value of type `dtype`, broadcastable with
        `shape` (for integer types, broadcasting is not supported, so it needs to
        be a scalar). The upper bound on the range of random values to generate
        (exclusive). Defaults to 1 if `dtype` is floating point.
      dtype: The type of the output: `float16`, `bfloat16`, `float32`, `float64`,
        `int32`, or `int64`. Defaults to `float32`.
      seed: A Python integer. Used in combination with `tf.random.set_seed` to
        create a reproducible sequence of tensors across multiple calls.
      name: A name for the operation (optional).

    Returns:
      A tensor of the specified shape filled with random uniform values.

    Raises:
      ValueError: If `dtype` is integral and `maxval` is not specified.
    """
    ...
def uniform_candidate_sampler(
    true_classes: tf.Tensor,
    num_true: int,
    num_sampled: int,
    unique: bool,
    range_max: int,
    seed: int | None = None,
    name: str | None = None,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    """
    Samples a set of classes using a uniform base distribution.

    This operation randomly samples a tensor of sampled classes
    (`sampled_candidates`) from the range of integers `[0, range_max)`.

    See the [Candidate Sampling Algorithms
    Reference](http://www.tensorflow.org/extras/candidate_sampling.pdf)
    for a quick course on Candidate Sampling.

    The elements of `sampled_candidates` are drawn without replacement
    (if `unique=True`) or with replacement (if `unique=False`) from
    the base distribution.

    The base distribution for this operation is the uniform distribution
    over the range of integers `[0, range_max)`.

    In addition, this operation returns tensors `true_expected_count`
    and `sampled_expected_count` representing the number of times each
    of the target classes (`true_classes`) and the sampled
    classes (`sampled_candidates`) is expected to occur in an average
    tensor of sampled classes. These values correspond to `Q(y|x)`
    defined in the [Candidate Sampling Algorithms
    Reference](http://www.tensorflow.org/extras/candidate_sampling.pdf).
    If `unique=True`, then these are post-rejection probabilities and we
    compute them approximately.

    Note that this function (and also other `*_candidate_sampler`
    functions) only gives you the ingredients to implement the various
    Candidate Sampling algorithms listed in the big table in the
    [Candidate Sampling Algorithms
    Reference](http://www.tensorflow.org/extras/candidate_sampling.pdf). You
    still need to implement the algorithms yourself.

    For example, according to that table, the phrase "negative samples"
    may mean different things in different algorithms. For instance, in
    NCE, "negative samples" means `S_i` (which is just the sampled
    classes) which may overlap with true classes, while in Sampled
    Logistic, "negative samples" means `S_i - T_i` which excludes the
    true classes. The return value `sampled_candidates` corresponds to
    `S_i`, not to any specific definition of "negative samples" in any
    specific algorithm. It's your responsibility to pick an algorithm
    and calculate the "negative samples" defined by that algorithm
    (e.g. `S_i - T_i`).

    As another example, the `true_classes` argument is for calculating
    the `true_expected_count` output (as a by-product of this function's
    main calculation), which may be needed by some algorithms (according
    to that table). It's not for excluding true classes in the return
    value `sampled_candidates`. Again that step is algorithm-specific
    and should be carried out by you.

    Args:
      true_classes: A `Tensor` of type `int64` and shape `[batch_size,
        num_true]`. The target classes.
      num_true: An `int`.  The number of target classes per training example.
      num_sampled: An `int`.  The number of classes to randomly sample. The
        `sampled_candidates` return value will have shape `[num_sampled]`. If
        `unique=True`, `num_sampled` must be less than or equal to `range_max`.
      unique: A `bool`. Determines whether all sampled classes in a batch are
        unique.
      range_max: An `int`. The number of possible classes.
      seed: An `int`. An operation-specific seed. Default is 0.
      name: A name for the operation (optional).

    Returns:
      sampled_candidates: A tensor of type `int64` and shape
        `[num_sampled]`. The sampled classes, either with possible
        duplicates (`unique=False`) or all unique (`unique=True`). As
        noted above, `sampled_candidates` may overlap with true classes.
      true_expected_count: A tensor of type `float`.  Same shape as
        `true_classes`. The expected counts under the sampling distribution
        of each of `true_classes`.
      sampled_expected_count: A tensor of type `float`. Same shape as
        `sampled_candidates`. The expected counts under the sampling distribution
        of each of `sampled_candidates`.
    """
    ...

"""Public API for tf._api.v2.nn namespace"""

from collections.abc import Sequence
from typing import Any, Literal, overload

from tensorflow import RaggedTensor, Tensor
from tensorflow._aliases import ScalarTensorCompatible, TensorCompatible, TensorOrArray
from tensorflow.math import l2_normalize as l2_normalize, sigmoid as sigmoid, tanh as tanh
from tensorflow.sparse import SparseTensor

def atrous_conv2d(
    value: TensorOrArray, filters: TensorOrArray, rate: int, padding: Literal["VALID", "SAME"], name: str | None = None
) -> Tensor:
    """
    Atrous convolution (a.k.a. convolution with holes or dilated convolution).

    This function is a simpler wrapper around the more general
    `tf.nn.convolution`, and exists only for backwards compatibility. You can
    use `tf.nn.convolution` to perform 1-D, 2-D, or 3-D atrous convolution.

    Computes a 2-D atrous convolution, also known as convolution with holes or
    dilated convolution, given 4-D `value` and `filters` tensors. If the `rate`
    parameter is equal to one, it performs regular 2-D convolution. If the `rate`
    parameter is greater than one, it performs convolution with holes, sampling
    the input values every `rate` pixels in the `height` and `width` dimensions.
    This is equivalent to convolving the input with a set of upsampled filters,
    produced by inserting `rate - 1` zeros between two consecutive values of the
    filters along the `height` and `width` dimensions, hence the name atrous
    convolution or convolution with holes (the French word trous means holes in
    English).

    More specifically:

    ```
    output[batch, height, width, out_channel] =
        sum_{dheight, dwidth, in_channel} (
            filters[dheight, dwidth, in_channel, out_channel] *
            value[batch, height + rate*dheight, width + rate*dwidth, in_channel]
        )
    ```

    Atrous convolution allows us to explicitly control how densely to compute
    feature responses in fully convolutional networks. Used in conjunction with
    bilinear interpolation, it offers an alternative to `conv2d_transpose` in
    dense prediction tasks such as semantic image segmentation, optical flow
    computation, or depth estimation. It also allows us to effectively enlarge
    the field of view of filters without increasing the number of parameters or
    the amount of computation.

    For a description of atrous convolution and how it can be used for dense
    feature extraction, please see: (Chen et al., 2015). The same operation is
    investigated further in (Yu et al., 2016). Previous works that effectively
    use atrous convolution in different ways are, among others,
    (Sermanet et al., 2014) and (Giusti et al., 2013).
    Atrous convolution is also closely related to the so-called noble identities
    in multi-rate signal processing.

    There are many different ways to implement atrous convolution (see the refs
    above). The implementation here reduces

    ```python
    atrous_conv2d(value, filters, rate, padding=padding)
    ```

    to the following three operations:

    ```python
    paddings = ...
    net = space_to_batch(value, paddings, block_size=rate)
    net = conv2d(net, filters, strides=[1, 1, 1, 1], padding="VALID")
    crops = ...
    net = batch_to_space(net, crops, block_size=rate)
    ```

    Advanced usage. Note the following optimization: A sequence of `atrous_conv2d`
    operations with identical `rate` parameters, 'SAME' `padding`, and filters
    with odd heights/ widths:

    ```python
    net = atrous_conv2d(net, filters1, rate, padding="SAME")
    net = atrous_conv2d(net, filters2, rate, padding="SAME")
    ...
    net = atrous_conv2d(net, filtersK, rate, padding="SAME")
    ```

    can be equivalently performed cheaper in terms of computation and memory as:

    ```python
    pad = ...  # padding so that the input dims are multiples of rate
    net = space_to_batch(net, paddings=pad, block_size=rate)
    net = conv2d(net, filters1, strides=[1, 1, 1, 1], padding="SAME")
    net = conv2d(net, filters2, strides=[1, 1, 1, 1], padding="SAME")
    ...
    net = conv2d(net, filtersK, strides=[1, 1, 1, 1], padding="SAME")
    net = batch_to_space(net, crops=pad, block_size=rate)
    ```

    because a pair of consecutive `space_to_batch` and `batch_to_space` ops with
    the same `block_size` cancel out when their respective `paddings` and `crops`
    inputs are identical.

    Args:
      value: A 4-D `Tensor` of type `float`. It needs to be in the default "NHWC"
        format. Its shape is `[batch, in_height, in_width, in_channels]`.
      filters: A 4-D `Tensor` with the same type as `value` and shape
        `[filter_height, filter_width, in_channels, out_channels]`. `filters`'
        `in_channels` dimension must match that of `value`. Atrous convolution is
        equivalent to standard convolution with upsampled filters with effective
        height `filter_height + (filter_height - 1) * (rate - 1)` and effective
        width `filter_width + (filter_width - 1) * (rate - 1)`, produced by
        inserting `rate - 1` zeros along consecutive elements across the
        `filters`' spatial dimensions.
      rate: A positive int32. The stride with which we sample input values across
        the `height` and `width` dimensions. Equivalently, the rate by which we
        upsample the filter values by inserting zeros across the `height` and
        `width` dimensions. In the literature, the same parameter is sometimes
        called `input stride` or `dilation`.
      padding: A string, either `'VALID'` or `'SAME'`. The padding algorithm. See
        [here](https://www.tensorflow.org/api_docs/python/tf/nn#notes_on_padding_2)
        for more information.
      name: Optional name for the returned tensor.

    Returns:
      A `Tensor` with the same type as `value`.
      Output shape with `'VALID'` padding is:

          [batch, height - rate * (filter_width - 1),
           width - rate * (filter_height - 1), out_channels].

      Output shape with `'SAME'` padding is:

          [batch, height, width, out_channels].

    Raises:
      ValueError: If input/output depth does not match `filters`' shape, or if
        padding is other than `'VALID'` or `'SAME'`.

    References:
      Multi-Scale Context Aggregation by Dilated Convolutions:
        [Yu et al., 2016](https://arxiv.org/abs/1511.07122)
        ([pdf](https://arxiv.org/pdf/1511.07122.pdf))
      Semantic Image Segmentation with Deep Convolutional Nets and Fully
      Connected CRFs:
        [Chen et al., 2015](http://arxiv.org/abs/1412.7062)
        ([pdf](https://arxiv.org/pdf/1412.7062))
      OverFeat - Integrated Recognition, Localization and Detection using
      Convolutional Networks:
        [Sermanet et al., 2014](https://arxiv.org/abs/1312.6229)
        ([pdf](https://arxiv.org/pdf/1312.6229.pdf))
      Fast Image Scanning with Deep Max-Pooling Convolutional Neural Networks:
        [Giusti et al., 2013]
        (https://ieeexplore.ieee.org/abstract/document/6738831)
        ([pdf](https://arxiv.org/pdf/1302.1700.pdf))
    """
    ...
def atrous_conv2d_transpose(
    value: TensorOrArray,
    filters: TensorOrArray,
    output_shape: TensorOrArray,
    rate: int,
    padding: Literal["VALID", "SAME"],
    name: str | None = None,
) -> Tensor:
    """
    The transpose of `atrous_conv2d`.

    This operation is sometimes called "deconvolution" after
    (Zeiler et al., 2010), but is really the transpose (gradient) of
    `atrous_conv2d` rather than an actual deconvolution.

    Args:
      value: A 4-D `Tensor` of type `float`. It needs to be in the default `NHWC`
        format. Its shape is `[batch, in_height, in_width, in_channels]`.
      filters: A 4-D `Tensor` with the same type as `value` and shape
        `[filter_height, filter_width, out_channels, in_channels]`. `filters`'
        `in_channels` dimension must match that of `value`. Atrous convolution is
        equivalent to standard convolution with upsampled filters with effective
        height `filter_height + (filter_height - 1) * (rate - 1)` and effective
        width `filter_width + (filter_width - 1) * (rate - 1)`, produced by
        inserting `rate - 1` zeros along consecutive elements across the
        `filters`' spatial dimensions.
      output_shape: A 1-D `Tensor` of shape representing the output shape of the
        deconvolution op, of form `[batch, out_height, out_width, out_channels]`.
      rate: A positive int32. The stride with which we sample input values across
        the `height` and `width` dimensions. Equivalently, the rate by which we
        upsample the filter values by inserting zeros across the `height` and
        `width` dimensions. In the literature, the same parameter is sometimes
        called `input stride` or `dilation`.
      padding: A string, either `'VALID'` or `'SAME'`. The padding algorithm. See
        [here](https://www.tensorflow.org/api_docs/python/tf/nn#notes_on_padding_2)
        for more information.
      name: Optional name for the returned tensor.

    Returns:
      A `Tensor` with the same type as `value`.

    Raises:
      ValueError: If input/output depth does not match `filters`' shape, or if
        padding is other than `'VALID'` or `'SAME'`, or if the `rate` is less
        than one, or if the output_shape is not a tensor with 4 elements.

    References:
      Deconvolutional Networks:
        [Zeiler et al., 2010]
        (https://ieeexplore.ieee.org/abstract/document/5539957)
        ([pdf]
        (http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.232.4023&rep=rep1&type=pdf))
    """
    ...
def avg_pool(
    input: TensorOrArray,
    ksize: int | Sequence[int],
    strides: int | Sequence[int],
    padding: Literal["VALID", "SAME"],
    data_format: Literal["NWC", "NCW", "NHWC", "NCHW", "NDHWC", "NCDHW"] | None = None,
    name: str | None = None,
) -> Tensor:
    """
    Performs the avg pooling on the input.

    Each entry in `output` is the mean of the corresponding size `ksize`
    window in `value`.

    Args:
      input:  Tensor of rank N+2, of shape `[batch_size] + input_spatial_shape +
        [num_channels]` if `data_format` does not start with "NC" (default), or
        `[batch_size, num_channels] + input_spatial_shape` if data_format starts
        with "NC". Pooling happens over the spatial dimensions only.
      ksize: An int or list of `ints` that has length `1`, `N` or `N+2`. The size
        of the window for each dimension of the input tensor.
      strides: An int or list of `ints` that has length `1`, `N` or `N+2`. The
        stride of the sliding window for each dimension of the input tensor.
      padding: A string, either `'VALID'` or `'SAME'`. The padding algorithm. See
        [here](https://www.tensorflow.org/api_docs/python/tf/nn#notes_on_padding_2)
        for more information.
      data_format: A string. Specifies the channel dimension. For N=1 it can be
        either "NWC" (default) or "NCW", for N=2 it can be either "NHWC" (default)
        or "NCHW" and for N=3 either "NDHWC" (default) or "NCDHW".
      name: Optional name for the operation.

    Returns:
      A `Tensor` of format specified by `data_format`.
      The average pooled output tensor.
    """
    ...
def avg_pool1d(
    input: TensorOrArray,
    ksize: int | Sequence[int],
    strides: int | Sequence[int],
    padding: Literal["VALID", "SAME"],
    data_format: Literal["NWC", "NCW"] = "NWC",
    name: str | None = None,
) -> Tensor:
    """
    Performs the average pooling on the input.

    Each entry in `output` is the mean of the corresponding size `ksize`
    window in `value`.

    Note internally this op reshapes and uses the underlying 2d operation.

    Args:
      input: A 3-D `Tensor` of the format specified by `data_format`.
      ksize: An int or list of `ints` that has length `1` or `3`. The size of the
        window for each dimension of the input tensor.
      strides: An int or list of `ints` that has length `1` or `3`. The stride of
        the sliding window for each dimension of the input tensor.
      padding: A string, either `'VALID'` or `'SAME'`. The padding algorithm. See
        [here](https://www.tensorflow.org/api_docs/python/tf/nn#notes_on_padding_2)
        for more information.
      data_format: An optional string from: "NWC", "NCW". Defaults to "NWC".
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of format specified by `data_format`.
      The max pooled output tensor.
    """
    ...
def avg_pool2d(
    input: TensorOrArray,
    ksize: int | Sequence[int],
    strides: int | Sequence[int],
    padding: Literal["VALID", "SAME"],
    data_format: Literal["NHWC", "NCHW"] = "NHWC",
    name: str | None = None,
) -> Tensor:
    """
    Performs the average pooling on the input.

    Each entry in `output` is the mean of the corresponding size `ksize`
    window in `value`.

    Args:
      input: A 4-D `Tensor` of shape `[batch, height, width, channels]` and type
        `float32`, `float64`, `qint8`, `quint8`, or `qint32`.
      ksize: An int or list of `ints` that has length `1`, `2` or `4`. The size of
        the window for each dimension of the input tensor.
      strides: An int or list of `ints` that has length `1`, `2` or `4`. The
        stride of the sliding window for each dimension of the input tensor.
      padding: A string, either `'VALID'` or `'SAME'`. The padding algorithm. See
        [here](https://www.tensorflow.org/api_docs/python/tf/nn#notes_on_padding_2)
        for more information.
      data_format: A string. 'NHWC' and 'NCHW' are supported.
      name: Optional name for the operation.

    Returns:
      A `Tensor` with the same type as `value`.  The average pooled output tensor.
    """
    ...
def avg_pool3d(
    input: TensorOrArray,
    ksize: int | Sequence[int],
    strides: int | Sequence[int],
    padding: Literal["VALID", "SAME"],
    data_format: Literal["NDHWC", "NCDHW"] = "NDHWC",
    name: str | None = None,
) -> Tensor:
    """
    Performs the average pooling on the input.

    Each entry in `output` is the mean of the corresponding size `ksize`
    window in `value`.

    Args:
      input: A 5-D `Tensor` of shape `[batch, depth, height, width, channels]`
        and type `float32`, `float64`, `qint8`, `quint8`, or `qint32`.
      ksize: An int or list of `ints` that has length `1`, `3` or `5`. The size of
        the window for each dimension of the input tensor.
      strides: An int or list of `ints` that has length `1`, `3` or `5`. The
        stride of the sliding window for each dimension of the input tensor.
      padding: A string, either `'VALID'` or `'SAME'`. The padding algorithm. See
        [here](https://www.tensorflow.org/api_docs/python/tf/nn#notes_on_padding_2)
        for more information.
      data_format: A string. 'NDHWC' and 'NCDHW' are supported.
      name: Optional name for the operation.

    Returns:
      A `Tensor` with the same type as `value`.  The average pooled output tensor.
    """
    ...
def batch_normalization(
    x: Tensor, mean: Tensor, variance: Tensor, offset: Tensor, scale: Tensor, variance_epsilon: float, name: str | None = None
) -> Tensor:
    r"""
    Batch normalization.

    Normalizes a tensor by `mean` and `variance`, and applies (optionally) a
    `scale` \\(\gamma\\) to it, as well as an `offset` \\(\beta\\):

    \\(\frac{\gamma(x-\mu)}{\sigma}+\beta\\)

    `mean`, `variance`, `offset` and `scale` are all expected to be of one of two
    shapes:

      * In all generality, they can have the same number of dimensions as the
        input `x`, with identical sizes as `x` for the dimensions that are not
        normalized over (the 'depth' dimension(s)), and dimension 1 for the
        others which are being normalized over.
        `mean` and `variance` in this case would typically be the outputs of
        `tf.nn.moments(..., keepdims=True)` during training, or running averages
        thereof during inference.
      * In the common case where the 'depth' dimension is the last dimension in
        the input tensor `x`, they may be one dimensional tensors of the same
        size as the 'depth' dimension.
        This is the case for example for the common `[batch, depth]` layout of
        fully-connected layers, and `[batch, height, width, depth]` for
        convolutions.
        `mean` and `variance` in this case would typically be the outputs of
        `tf.nn.moments(..., keepdims=False)` during training, or running averages
        thereof during inference.

    See equation 11 in Algorithm 2 of source:
    [Batch Normalization: Accelerating Deep Network Training by
    Reducing Internal Covariate Shift; S. Ioffe, C. Szegedy]
    (http://arxiv.org/abs/1502.03167).

    Args:
      x: Input `Tensor` of arbitrary dimensionality.
      mean: A mean `Tensor`.
      variance: A variance `Tensor`.
      offset: An offset `Tensor`, often denoted \\(\beta\\) in equations, or
        None. If present, will be added to the normalized tensor.
      scale: A scale `Tensor`, often denoted \\(\gamma\\) in equations, or
        `None`. If present, the scale is applied to the normalized tensor.
      variance_epsilon: A small float number to avoid dividing by 0.
      name: A name for this operation (optional).

    Returns:
      the normalized, scaled, offset tensor.

    References:
      Batch Normalization - Accelerating Deep Network Training by Reducing
      Internal Covariate Shift:
        [Ioffe et al., 2015](http://arxiv.org/abs/1502.03167)
        ([pdf](http://proceedings.mlr.press/v37/ioffe15.pdf))
    """
    ...
def bias_add(
    value: Tensor, bias: Tensor, data_format: Literal["N...C", "NC..."] | None = None, name: str | None = None
) -> Tensor:
    """
    Adds `bias` to `value`.

    This is (mostly) a special case of `tf.add` where `bias` is restricted to 1-D.
    Broadcasting is supported, so `value` may have any number of dimensions.
    Unlike `tf.add`, the type of `bias` is allowed to differ from `value` in the
    case where both types are quantized.

    Args:
      value: A `Tensor` with type `float`, `double`, `int64`, `int32`, `uint8`,
        `int16`, `int8`, `complex64`, or `complex128`.
      bias: A 1-D `Tensor` with size matching the channel dimension of `value`.
        Must be the same type as `value` unless `value` is a quantized type,
        in which case a different quantized type may be used.
      data_format: A string. 'N...C' and 'NC...' are supported. If `None` (the
        default) is specified then 'N..C' is assumed.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` with the same type as `value`.

    Raises:
      ValueError if data format is unrecognized, if `value` has less than two
      dimensions when `data_format` is 'N..C'/`None` or `value` has less
      then three dimensions when `data_format` is `NC..`, if `bias` does not
      have exactly one dimension (is a vector), or if the size of `bias`
      does not match the size of the channel dimension of `value`.
    """
    ...
def collapse_repeated(labels: Tensor, seq_length: Tensor, name: str | None = None) -> tuple[Tensor, Tensor]:
    """
    Merge repeated labels into single labels.

    Args:
      labels: Tensor of shape [batch, max value in seq_length]
      seq_length: Tensor of shape [batch], sequence length of each batch element.
      name: A name for this `Op`. Defaults to "collapse_repeated_labels".

    Returns:
      A tuple `(collapsed_labels, new_seq_length)` where

      collapsed_labels: Tensor of shape [batch, max_seq_length] with repeated
      labels collapsed and padded to max_seq_length, eg:
      `[[A, A, B, B, A], [A, B, C, D, E]] => [[A, B, A, 0, 0], [A, B, C, D, E]]`

      new_seq_length: int tensor of shape [batch] with new sequence lengths.
    """
    ...
def compute_accidental_hits(
    true_classes: Tensor, sampled_candidates: Tensor, num_true: int, seed: int | None = None, name: str | None = None
) -> tuple[Tensor, Tensor, Tensor]:
    """
    Compute the position ids in `sampled_candidates` matching `true_classes`.

    In Candidate Sampling, this operation facilitates virtually removing
    sampled classes which happen to match target classes.  This is done
    in Sampled Softmax and Sampled Logistic.

    See our [Candidate Sampling Algorithms
    Reference](http://www.tensorflow.org/extras/candidate_sampling.pdf).

    We presuppose that the `sampled_candidates` are unique.

    We call it an 'accidental hit' when one of the target classes
    matches one of the sampled classes.  This operation reports
    accidental hits as triples `(index, id, weight)`, where `index`
    represents the row number in `true_classes`, `id` represents the
    position in `sampled_candidates`, and weight is `-FLOAT_MAX`.

    The result of this op should be passed through a `sparse_to_dense`
    operation, then added to the logits of the sampled classes. This
    removes the contradictory effect of accidentally sampling the true
    target classes as noise classes for the same example.

    Args:
      true_classes: A `Tensor` of type `int64` and shape `[batch_size,
        num_true]`. The target classes.
      sampled_candidates: A tensor of type `int64` and shape `[num_sampled]`.
        The sampled_candidates output of CandidateSampler.
      num_true: An `int`.  The number of target classes per training example.
      seed: An `int`. An operation-specific seed. Default is 0.
      name: A name for the operation (optional).

    Returns:
      indices: A `Tensor` of type `int32` and shape `[num_accidental_hits]`.
        Values indicate rows in `true_classes`.
      ids: A `Tensor` of type `int64` and shape `[num_accidental_hits]`.
        Values indicate positions in `sampled_candidates`.
      weights: A `Tensor` of type `float` and shape `[num_accidental_hits]`.
        Each value is `-FLOAT_MAX`.
    """
    ...
def compute_average_loss(
    per_example_loss: Tensor, sample_weight: Tensor | None = None, global_batch_size: int | None = None
) -> Tensor:
    """
    Scales per-example losses with sample_weights and computes their average.

    Usage with distribution strategy and custom training loop:

    ```python
    with strategy.scope():
      def compute_loss(labels, predictions, sample_weight=None):

        # If you are using a `Loss` class instead, set reduction to `NONE` so that
        # we can do the reduction afterwards and divide by global batch size.
        per_example_loss = tf.keras.losses.sparse_categorical_crossentropy(
            labels, predictions)

        # Compute loss that is scaled by sample_weight and by global batch size.
        return tf.nn.compute_average_loss(
            per_example_loss,
            sample_weight=sample_weight,
            global_batch_size=GLOBAL_BATCH_SIZE)
    ```

    Args:
      per_example_loss: Per-example loss.
      sample_weight: Optional weighting for each example.
      global_batch_size: Optional global batch size value. Defaults to (size of
        first dimension of `losses`) * (number of replicas).

    Returns:
      Scalar loss value, obtained by summing the `per_example_loss` and dividing
      by `global_batch_size`. If `global_batch_size` is zero, the result is zero.
    """
    ...
def conv1d(
    input: TensorOrArray,
    filters: TensorOrArray,
    stride: int | Sequence[int],
    padding: Literal["VALID", "SAME"],
    data_format: Literal["NWC", "NCW"] = "NWC",
    dilations: int | Sequence[int] | None = None,
    name: str | None = None,
) -> Tensor:
    r"""
    Computes a 1-D convolution given 3-D input and filter tensors.

    Given an input tensor of shape
      `batch_shape + [in_width, in_channels]`
    if `data_format` is `"NWC"`, or
      `batch_shape + [in_channels, in_width]`
    if `data_format` is `"NCW"`,
    and a filter / kernel tensor of shape
    `[filter_width, in_channels, out_channels]`, this op reshapes
    the arguments to pass them to `conv2d` to perform the equivalent
    convolution operation.

    Internally, this op reshapes the input tensors and invokes `tf.nn.conv2d`.
    For example, if `data_format` does not start with `"NC"`, a tensor of shape
      `batch_shape + [in_width, in_channels]`
    is reshaped to
      `batch_shape + [1, in_width, in_channels]`,
    and the filter is reshaped to
      `[1, filter_width, in_channels, out_channels]`.
    The result is then reshaped back to
      `batch_shape + [out_width, out_channels]`
    \(where out_width is a function of the stride and padding as in conv2d\) and
    returned to the caller.

    Args:
      input: A Tensor of rank at least 3. Must be of type `float16`, `float32`, or
        `float64`.
      filters: A Tensor of rank at least 3.  Must have the same type as `input`.
      stride: An int or list of `ints` that has length `1` or `3`.  The number of
        entries by which the filter is moved right at each step.
      padding: 'SAME' or 'VALID'. See
        [here](https://www.tensorflow.org/api_docs/python/tf/nn#notes_on_padding_2)
        for more information.
      data_format: An optional `string` from `"NWC", "NCW"`.  Defaults to `"NWC"`,
        the data is stored in the order of
        `batch_shape + [in_width, in_channels]`.  The `"NCW"` format stores data
        as `batch_shape + [in_channels, in_width]`.
      dilations: An int or list of `ints` that has length `1` or `3` which
        defaults to 1. The dilation factor for each dimension of input. If set to
        k > 1, there will be k-1 skipped cells between each filter element on that
        dimension. Dilations in the batch and depth dimensions must be 1.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`.  Has the same type as input.

    Raises:
      ValueError: if `data_format` is invalid.
    """
    ...
def conv1d_transpose(
    input: TensorOrArray,
    filters: TensorOrArray,
    output_shape: TensorOrArray,
    strides: int | Sequence[int],
    padding: Literal["VALID", "SAME"] = "SAME",
    data_format: Literal["NWC", "NCW"] = "NWC",
    dilations: int | Sequence[int] | None = None,
    name: str | None = None,
) -> Tensor:
    """
    The transpose of `conv1d`.

    This operation is sometimes called "deconvolution" after
    (Zeiler et al., 2010), but is actually the transpose (gradient) of `conv1d`
    rather than an actual deconvolution.

    Args:
      input: A 3-D `Tensor` of type `float` and shape
        `[batch, in_width, in_channels]` for `NWC` data format or
        `[batch, in_channels, in_width]` for `NCW` data format.
      filters: A 3-D `Tensor` with the same type as `input` and shape
        `[filter_width, output_channels, in_channels]`.  `filter`'s
        `in_channels` dimension must match that of `input`.
      output_shape: A 1-D `Tensor`, containing three elements, representing the
        output shape of the deconvolution op.
      strides: An int or list of `ints` that has length `1` or `3`.  The number of
        entries by which the filter is moved right at each step.
      padding: A string, either `'VALID'` or `'SAME'`. The padding algorithm. See
        [here](https://www.tensorflow.org/api_docs/python/tf/nn#notes_on_padding_2)
        for more information.
      data_format: A string. `'NWC'` and `'NCW'` are supported.
      dilations: An int or list of `ints` that has length `1` or `3` which
        defaults to 1. The dilation factor for each dimension of input. If set to
        k > 1, there will be k-1 skipped cells between each filter element on that
        dimension. Dilations in the batch and depth dimensions must be 1.
      name: Optional name for the returned tensor.

    Returns:
      A `Tensor` with the same type as `input`.

    Raises:
      ValueError: If input/output depth does not match `filter`'s shape, if
        `output_shape` is not at 3-element vector, if `padding` is other than
        `'VALID'` or `'SAME'`, or if `data_format` is invalid.

    References:
      Deconvolutional Networks:
        [Zeiler et al., 2010]
        (https://ieeexplore.ieee.org/abstract/document/5539957)
        ([pdf]
        (http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.232.4023&rep=rep1&type=pdf))
    """
    ...
def conv2d(
    input: TensorOrArray,
    filters: TensorOrArray,
    strides: int | Sequence[int],
    padding: Literal["VALID", "SAME"],
    data_format: Literal["NHWC", "NCHW"] = "NHWC",
    dilations: int | Sequence[int] | None = None,
    name: str | None = None,
) -> Tensor:
    """
    Computes a 2-D convolution given `input` and 4-D `filters` tensors.

    The `input` tensor may have rank `4` or higher, where shape dimensions `[:-3]`
    are considered batch dimensions (`batch_shape`).

    Given an input tensor of shape
    `batch_shape + [in_height, in_width, in_channels]` and a filter / kernel
    tensor of shape `[filter_height, filter_width, in_channels, out_channels]`,
    this op performs the following:

    1. Flattens the filter to a 2-D matrix with shape
       `[filter_height * filter_width * in_channels, output_channels]`.
    2. Extracts image patches from the input tensor to form a *virtual*
       tensor of shape `[batch, out_height, out_width,
       filter_height * filter_width * in_channels]`.
    3. For each patch, right-multiplies the filter matrix and the image patch
       vector.

    In detail, with the default NHWC format,

        output[b, i, j, k] =
            sum_{di, dj, q} input[b, strides[1] * i + di, strides[2] * j + dj, q] *
                            filter[di, dj, q, k]

    Must have `strides[0] = strides[3] = 1`.  For the most common case of the same
    horizontal and vertical strides, `strides = [1, stride, stride, 1]`.

    Usage Example:

    >>> x_in = np.array([[
    ...   [[2], [1], [2], [0], [1]],
    ...   [[1], [3], [2], [2], [3]],
    ...   [[1], [1], [3], [3], [0]],
    ...   [[2], [2], [0], [1], [1]],
    ...   [[0], [0], [3], [1], [2]], ]])
    >>> kernel_in = np.array([
    ...  [ [[2, 0.1]], [[3, 0.2]] ],
    ...  [ [[0, 0.3]], [[1, 0.4]] ], ])
    >>> x = tf.constant(x_in, dtype=tf.float32)
    >>> kernel = tf.constant(kernel_in, dtype=tf.float32)
    >>> tf.nn.conv2d(x, kernel, strides=[1, 1, 1, 1], padding='VALID')
    <tf.Tensor: shape=(1, 4, 4, 2), dtype=float32, numpy=..., dtype=float32)>

    Args:
      input: A `Tensor`. Must be one of the following types:
        `half`, `bfloat16`, `float32`, `float64`.
        A Tensor of rank at least 4. The dimension order is interpreted according
        to the value of `data_format`; with the all-but-inner-3 dimensions acting
        as batch dimensions. See below for details.
      filters: A `Tensor`. Must have the same type as `input`.
        A 4-D tensor of shape
        `[filter_height, filter_width, in_channels, out_channels]`
      strides: An int or list of `ints` that has length `1`, `2` or `4`.  The
        stride of the sliding window for each dimension of `input`. If a single
        value is given it is replicated in the `H` and `W` dimension. By default
        the `N` and `C` dimensions are set to 1. The dimension order is determined
        by the value of `data_format`, see below for details.
      padding: Either the `string` `"SAME"` or `"VALID"` indicating the type of
        padding algorithm to use, or a list indicating the explicit paddings at
        the start and end of each dimension. See
        [here](https://www.tensorflow.org/api_docs/python/tf/nn#notes_on_padding_2)
        for more information. When explicit padding is used and data_format is
        `"NHWC"`, this should be in the form `[[0, 0], [pad_top, pad_bottom],
        [pad_left, pad_right], [0, 0]]`. When explicit padding used and
        data_format is `"NCHW"`, this should be in the form `[[0, 0], [0, 0],
        [pad_top, pad_bottom], [pad_left, pad_right]]`.
      data_format: An optional `string` from: `"NHWC", "NCHW"`.
        Defaults to `"NHWC"`.
        Specify the data format of the input and output data. With the
        default format "NHWC", the data is stored in the order of:
            `batch_shape + [height, width, channels]`.
        Alternatively, the format could be "NCHW", the data storage order of:
            `batch_shape + [channels, height, width]`.
      dilations: An int or list of `ints` that has length `1`, `2` or `4`,
        defaults to 1. The dilation factor for each dimension of`input`. If a
        single value is given it is replicated in the `H` and `W` dimension. By
        default the `N` and `C` dimensions are set to 1. If set to k > 1, there
        will be k-1 skipped cells between each filter element on that dimension.
        The dimension order is determined by the value of `data_format`, see above
        for details. Dilations in the batch and depth dimensions if a 4-d tensor
        must be 1.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `input` and the same outer batch shape.
    """
    ...
def conv2d_transpose(
    input: TensorOrArray,
    filters: TensorOrArray,
    output_shape: TensorOrArray,
    strides: int | Sequence[int],
    padding: Literal["VALID", "SAME"] = "SAME",
    data_format: Literal["NHWC", "NCHW"] = "NHWC",
    dilations: int | Sequence[int] | None = None,
    name: str | None = None,
) -> Tensor:
    """
    The transpose of `conv2d`.

    This operation is sometimes called "deconvolution" after
    (Zeiler et al., 2010), but is really the transpose (gradient) of
    `atrous_conv2d` rather than an actual deconvolution.

    Args:
      input: A 4-D `Tensor` of type `float` and shape `[batch, height, width,
        in_channels]` for `NHWC` data format or `[batch, in_channels, height,
        width]` for `NCHW` data format.
      filters: A 4-D `Tensor` with the same type as `input` and shape `[height,
        width, output_channels, in_channels]`.  `filter`'s `in_channels` dimension
        must match that of `input`.
      output_shape: A 1-D `Tensor` representing the output shape of the
        deconvolution op.
      strides: An int or list of `ints` that has length `1`, `2` or `4`.  The
        stride of the sliding window for each dimension of `input`. If a single
        value is given it is replicated in the `H` and `W` dimension. By default
        the `N` and `C` dimensions are set to 0. The dimension order is determined
        by the value of `data_format`, see below for details.
      padding: Either the `string` `"SAME"` or `"VALID"` indicating the type of
        padding algorithm to use, or a list indicating the explicit paddings at
        the start and end of each dimension. See
        [here](https://www.tensorflow.org/api_docs/python/tf/nn#notes_on_padding_2)
        for more information.  When explicit padding is used and data_format is
        `"NHWC"`, this should be in the form `[[0, 0], [pad_top, pad_bottom],
        [pad_left, pad_right], [0, 0]]`. When explicit padding used and
        data_format is `"NCHW"`, this should be in the form `[[0, 0], [0, 0],
        [pad_top, pad_bottom], [pad_left, pad_right]]`.
      data_format: A string. 'NHWC' and 'NCHW' are supported.
      dilations: An int or list of `ints` that has length `1`, `2` or `4`,
        defaults to 1. The dilation factor for each dimension of`input`. If a
        single value is given it is replicated in the `H` and `W` dimension. By
        default the `N` and `C` dimensions are set to 1. If set to k > 1, there
        will be k-1 skipped cells between each filter element on that dimension.
        The dimension order is determined by the value of `data_format`, see above
        for details. Dilations in the batch and depth dimensions if a 4-d tensor
        must be 1.
      name: Optional name for the returned tensor.

    Returns:
      A `Tensor` with the same type as `input`.

    Raises:
      ValueError: If input/output depth does not match `filter`'s shape, or if
        padding is other than `'VALID'` or `'SAME'`.

    References:
      Deconvolutional Networks:
        [Zeiler et al., 2010]
        (https://ieeexplore.ieee.org/abstract/document/5539957)
        ([pdf]
        (http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.232.4023&rep=rep1&type=pdf))
    """
    ...
def conv3d(
    input: TensorOrArray,
    filters: TensorOrArray,
    strides: int | Sequence[int],
    padding: Literal["VALID", "SAME"],
    data_format: Literal["NDHWC", "NCDHW"] = "NDHWC",
    dilations: int | Sequence[int] | None = None,
    name: str | None = None,
) -> Tensor:
    """
    Computes a 3-D convolution given 5-D `input` and `filters` tensors.

    In signal processing, cross-correlation is a measure of similarity of
    two waveforms as a function of a time-lag applied to one of them. This
    is also known as a sliding dot product or sliding inner-product.

    Our Conv3D implements a form of cross-correlation.

    Args:
      input: A `Tensor`. Must be one of the following types: `half`, `bfloat16`, `float32`, `float64`.
        Shape `[batch, in_depth, in_height, in_width, in_channels]`.
      filters: A `Tensor`. Must have the same type as `input`.
        Shape `[filter_depth, filter_height, filter_width, in_channels,
        out_channels]`. `in_channels` must match between `input` and `filters`.
      strides: A list of `ints` that has length `>= 5`.
        1-D tensor of length 5. The stride of the sliding window for each
        dimension of `input`. Must have `strides[0] = strides[4] = 1`.
      padding: A `string` from: `"SAME", "VALID"`.
        The type of padding algorithm to use.
      data_format: An optional `string` from: `"NDHWC", "NCDHW"`. Defaults to `"NDHWC"`.
        The data format of the input and output data. With the
        default format "NDHWC", the data is stored in the order of:
            [batch, in_depth, in_height, in_width, in_channels].
        Alternatively, the format could be "NCDHW", the data storage order is:
            [batch, in_channels, in_depth, in_height, in_width].
      dilations: An optional list of `ints`. Defaults to `[1, 1, 1, 1, 1]`.
        1-D tensor of length 5.  The dilation factor for each dimension of
        `input`. If set to k > 1, there will be k-1 skipped cells between each
        filter element on that dimension. The dimension order is determined by the
        value of `data_format`, see above for details. Dilations in the batch and
        depth dimensions must be 1.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `input`.
    """
    ...
def conv3d_transpose(
    input: TensorOrArray,
    filters: TensorOrArray,
    output_shape: TensorOrArray,
    strides: int | Sequence[int],
    padding: Literal["VALID", "SAME"] = "SAME",
    data_format: Literal["NDHWC", "NCDHW"] = "NDHWC",
    dilations: int | Sequence[int] | None = None,
    name: str | None = None,
) -> Tensor:
    """
    The transpose of `conv3d`.

    This operation is sometimes called "deconvolution" after
    (Zeiler et al., 2010), but is really the transpose (gradient) of `conv3d`
    rather than an actual deconvolution.

    Args:
      input: A 5-D `Tensor` of type `float` and shape `[batch, depth, height,
        width, in_channels]` for `NDHWC` data format or `[batch, in_channels,
        depth, height, width]` for `NCDHW` data format.
      filters: A 5-D `Tensor` with the same type as `input` and shape `[depth,
        height, width, output_channels, in_channels]`.  `filter`'s `in_channels`
        dimension must match that of `input`.
      output_shape: A 1-D `Tensor` representing the output shape of the
        deconvolution op.
      strides: An int or list of `ints` that has length `1`, `3` or `5`.  The
        stride of the sliding window for each dimension of `input`. If a single
        value is given it is replicated in the `D`, `H` and `W` dimension. By
        default the `N` and `C` dimensions are set to 0. The dimension order is
        determined by the value of `data_format`, see below for details.
      padding: A string, either `'VALID'` or `'SAME'`. The padding algorithm. See
        [here](https://www.tensorflow.org/api_docs/python/tf/nn#notes_on_padding_2)
        for more information.
      data_format: A string. 'NDHWC' and 'NCDHW' are supported.
      dilations: An int or list of `ints` that has length `1`, `3` or `5`,
        defaults to 1. The dilation factor for each dimension of`input`. If a
        single value is given it is replicated in the `D`, `H` and `W` dimension.
        By default the `N` and `C` dimensions are set to 1. If set to k > 1, there
        will be k-1 skipped cells between each filter element on that dimension.
        The dimension order is determined by the value of `data_format`, see above
        for details. Dilations in the batch and depth dimensions if a 5-d tensor
        must be 1.
      name: Optional name for the returned tensor.

    Returns:
      A `Tensor` with the same type as `input`.

    References:
      Deconvolutional Networks:
        [Zeiler et al., 2010]
        (https://ieeexplore.ieee.org/abstract/document/5539957)
        ([pdf]
        (http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.232.4023&rep=rep1&type=pdf))
    """
    ...
def conv_transpose(
    input: TensorOrArray,
    filters: TensorOrArray,
    output_shape: TensorOrArray,
    strides: int | Sequence[int],
    padding: Literal["VALID", "SAME"] = "SAME",
    data_format: str | None = None,
    dilations: int | Sequence[int] | None = None,
    name: str | None = None,
) -> Tensor:
    """
    The transpose of `convolution`.

    This operation is sometimes called "deconvolution" after
    (Zeiler et al., 2010), but is really the transpose (gradient) of `conv3d`
    rather than an actual deconvolution.

    Args:
      input: An N+2 dimensional `Tensor` of shape
        `[batch_size] + input_spatial_shape + [in_channels]` if data_format does
        not start with "NC" (default), or
        `[batch_size, in_channels] + input_spatial_shape` if data_format starts
        with "NC". It must be one of the following types:
        `half`, `bfloat16`, `float32`, `float64`.
      filters: An N+2 dimensional `Tensor` with the same type as `input` and
        shape `spatial_filter_shape + [in_channels, out_channels]`.
      output_shape: A 1-D `Tensor` representing the output shape of the
        deconvolution op.
      strides: An int or list of `ints` that has length `1`, `N` or `N+2`.  The
        stride of the sliding window for each dimension of `input`. If a single
        value is given it is replicated in the spatial dimensions. By default
        the `N` and `C` dimensions are set to 0. The dimension order is determined
        by the value of `data_format`, see below for details.
      padding: A string, either `'VALID'` or `'SAME'`. The padding algorithm. See
        [here](https://www.tensorflow.org/api_docs/python/tf/nn#notes_on_padding_2)
        for more information.
      data_format: A string or None.  Specifies whether the channel dimension of
        the `input` and output is the last dimension (default, or if `data_format`
        does not start with "NC"), or the second dimension (if `data_format`
        starts with "NC").  For N=1, the valid values are "NWC" (default) and
        "NCW".  For N=2, the valid values are "NHWC" (default) and "NCHW".
        For N=3, the valid values are "NDHWC" (default) and "NCDHW".
      dilations: An int or list of `ints` that has length `1`, `N` or `N+2`,
        defaults to 1. The dilation factor for each dimension of`input`. If a
        single value is given it is replicated in the spatial dimensions. By
        default the `N` and `C` dimensions are set to 1. If set to k > 1, there
        will be k-1 skipped cells between each filter element on that dimension.
        The dimension order is determined by the value of `data_format`, see above
        for details.
      name: A name for the operation (optional). If not specified "conv_transpose"
        is used.

    Returns:
      A `Tensor` with the same type as `value`.

    References:
      Deconvolutional Networks:
        [Zeiler et al., 2010]
        (https://ieeexplore.ieee.org/abstract/document/5539957)
        ([pdf]
        (http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.232.4023&rep=rep1&type=pdf))
    """
    ...
def convolution(
    input: TensorOrArray,
    filters: TensorOrArray,
    strides: int | Sequence[int] | None = None,
    padding: Literal["VALID", "SAME"] = "VALID",
    data_format: Literal["NC", "NWC", "NCW", "NHWC", "NCHW", "NDHWC", "NCDHW"] | None = None,
    dilations: int | Sequence[int] | None = None,
    name: str | None = None,
) -> Tensor:
    """
    Computes sums of N-D convolutions (actually cross-correlation).

    This also supports either output striding via the optional `strides` parameter
    or atrous convolution (also known as convolution with holes or dilated
    convolution, based on the French word "trous" meaning holes in English) via
    the optional `dilations` parameter.  Currently, however, output striding
    is not supported for atrous convolutions.

    Specifically, in the case that `data_format` does not start with "NC", given
    a rank (N+2) `input` Tensor of shape

      [num_batches,
       input_spatial_shape[0],
       ...,
       input_spatial_shape[N-1],
       num_input_channels],

    a rank (N+2) `filters` Tensor of shape

      [spatial_filter_shape[0],
       ...,
       spatial_filter_shape[N-1],
       num_input_channels,
       num_output_channels],

    an optional `dilations` tensor of shape N (defaults to `[1]*N`) specifying
    the filter upsampling/input downsampling rate, and an optional list of N
    `strides` (defaults to `[1]*N`), this computes for each N-D spatial output
    position `(x[0], ..., x[N-1])`:

    ```
    output[b, x[0], ..., x[N-1], k] =
        sum_{z[0], ..., z[N-1], q}
            filter[z[0], ..., z[N-1], q, k] *
            padded_input[b,
                         x[0]*strides[0] + dilation_rate[0]*z[0],
                         ...,
                         x[N-1]*strides[N-1] + dilation_rate[N-1]*z[N-1],
                         q]
    ```

    where b is the index into the batch, k is the output channel number, q is the
    input channel number, and z is the N-D spatial offset within the filter. Here,
    `padded_input` is obtained by zero padding the input using an effective
    spatial filter shape of `(spatial_filter_shape-1) * dilation_rate + 1` and
    output striding `strides`.

    In the case that `data_format` does start with `"NC"`, the `input` and output
    (but not the `filters`) are simply transposed as follows:

    ```python
    convolution(input, data_format, **kwargs) =
      tf.transpose(convolution(tf.transpose(input, [0] + range(2,N+2) + [1]),
                               **kwargs),
                   [0, N+1] + range(1, N+1))
    ```

    It is required that 1 <= N <= 3.

    Args:
      input: An (N+2)-D `Tensor` of type `T`, of shape
        `[batch_size] + input_spatial_shape + [in_channels]` if data_format does
        not start with "NC" (default), or
        `[batch_size, in_channels] + input_spatial_shape` if data_format starts
        with "NC".
      filters: An (N+2)-D `Tensor` with the same type as `input` and shape
        `spatial_filter_shape + [in_channels, out_channels]`.
      padding: A string, either `"VALID"` or `"SAME"`. The padding algorithm.
        `"valid"` means no padding. `"same"` results in padding evenly to
        the left/right or up/down of the input such that output has the same
        height/width dimension as the input when the strides are 1. See
        [here](https://www.tensorflow.org/api_docs/python/tf/nn#notes_on_padding_2)
        for more information.
      strides: Optional.  Sequence of N ints >= 1.  Specifies the output stride.
        Defaults to `[1]*N`.  If any value of strides is > 1, then all values of
        dilation_rate must be 1.
      dilations: Optional.  Sequence of N ints >= 1.  Specifies the filter
        upsampling/input downsampling rate.  In the literature, the same parameter
        is sometimes called `input stride` or `dilation`.  The effective filter
        size used for the convolution will be `spatial_filter_shape +
        (spatial_filter_shape - 1) * (rate - 1)`, obtained by inserting
        (dilation_rate[i]-1) zeros between consecutive elements of the original
        filter in each spatial dimension i.  If any value of dilation_rate is > 1,
        then all values of strides must be 1.
      name: Optional name for the returned tensor.
      data_format: A string or None.  Specifies whether the channel dimension of
        the `input` and output is the last dimension (default, or if `data_format`
        does not start with "NC"), or the second dimension (if `data_format`
        starts with "NC").  For N=1, the valid values are "NWC" (default) and
        "NCW".  For N=2, the valid values are "NHWC" (default) and "NCHW".
        For N=3, the valid values are "NDHWC" (default) and "NCDHW".

    Returns:
      A `Tensor` with the same type as `input` of shape

          `[batch_size] + output_spatial_shape + [out_channels]`

      if data_format is None or does not start with "NC", or

          `[batch_size, out_channels] + output_spatial_shape`

      if data_format starts with "NC",
      where `output_spatial_shape` depends on the value of `padding`.

      If padding == "SAME":
        output_spatial_shape[i] = ceil(input_spatial_shape[i] / strides[i])

      If padding == "VALID":
        output_spatial_shape[i] =
          ceil((input_spatial_shape[i] -
                (spatial_filter_shape[i]-1) * dilation_rate[i])
               / strides[i]).

    Raises:
      ValueError: If input/output depth does not match `filters` shape, if padding
        is other than `"VALID"` or `"SAME"`, or if data_format is invalid.
    """
    ...
def crelu(features: TensorOrArray, axis: int = -1, name: str | None = None) -> Tensor:
    """
    Computes Concatenated ReLU.

    Concatenates a ReLU which selects only the positive part of the activation
    with a ReLU which selects only the *negative* part of the activation.
    Note that as a result this non-linearity doubles the depth of the activations.
    Source: [Understanding and Improving Convolutional Neural Networks via
    Concatenated Rectified Linear Units. W. Shang, et
    al.](https://arxiv.org/abs/1603.05201)

    Args:
      features: A `Tensor` with type `float`, `double`, `int32`, `int64`, `uint8`,
        `int16`, or `int8`.
      name: A name for the operation (optional).
      axis: The axis that the output values are concatenated along. Default is -1.

    Returns:
      A `Tensor` with the same type as `features`.

    References:
      Understanding and Improving Convolutional Neural Networks via Concatenated
      Rectified Linear Units:
        [Shang et al., 2016](http://proceedings.mlr.press/v48/shang16)
        ([pdf](http://proceedings.mlr.press/v48/shang16.pdf))
    """
    ...
def ctc_beam_search_decoder(
    inputs: TensorOrArray, sequence_length: TensorOrArray | Sequence[int], beam_width: int = 100, top_paths: int = 1
) -> tuple[list[SparseTensor], Tensor]:
    """
    Performs beam search decoding on the logits given in input.

    **Note** Although in general greedy search is a special case of beam-search
    with `top_paths=1` and `beam_width=1`, `ctc_beam_search_decoder` differs
    from `ctc_greedy_decoder` in the treatment of blanks when computing the
    probability of a sequence:
      - `ctc_beam_search_decoder` treats blanks as sequence termination
      - `ctc_greedy_decoder` treats blanks as regular elements

    Args:
      inputs: 3-D `float` `Tensor`, size `[max_time, batch_size, num_classes]`.
        The logits.
      sequence_length: 1-D `int32` vector containing sequence lengths, having size
        `[batch_size]`.
      beam_width: An int scalar >= 0 (beam search beam width).
      top_paths: An int scalar >= 0, <= beam_width (controls output size).

    Returns:
      A tuple `(decoded, log_probabilities)` where

      decoded: A list of length top_paths, where `decoded[j]`
        is a `SparseTensor` containing the decoded outputs:

        `decoded[j].indices`: Indices matrix `[total_decoded_outputs[j], 2]`;
          The rows store: `[batch, time]`.

        `decoded[j].values`: Values vector, size `[total_decoded_outputs[j]]`.
          The vector stores the decoded classes for beam `j`.

        `decoded[j].dense_shape`: Shape vector, size `(2)`.
          The shape values are: `[batch_size, max_decoded_length[j]]`.

      log_probability: A `float` matrix `[batch_size, top_paths]` containing
          sequence log-probabilities.
    """
    ...
def ctc_greedy_decoder(
    inputs: Tensor, sequence_length: Tensor | Sequence[int], merge_repeated: bool = True, blank_index: int | None = None
) -> tuple[list[SparseTensor], Tensor]:
    """
    Performs greedy decoding on the logits given in input (best path).

    Given a tensor as `inputs`, the `blank_index` parameter defines the class
    index of the blank symbol.

    For example:

    If `blank_index` is equal to 1:

    >>> inf = float("inf")
    >>> logits = tf.constant([[[   0., -inf, -inf],
    ...                        [ -2.3, -inf, -0.1]],
    ...                       [[ -inf, -0.5, -inf],
    ...                        [ -inf, -inf, -0.1]],
    ...                       [[ -inf, -inf, -inf],
    ...                        [ -0.1, -inf, -2.3]]])
    >>> seq_lens = tf.constant([2, 3])
    >>> outputs = tf.nn.ctc_greedy_decoder(
    ...     logits,
    ...     seq_lens,
    ...     blank_index=1)

    Notes:

    - Unlike `ctc_beam_search_decoder`, `ctc_greedy_decoder` considers blanks
      as regular elements when computing the probability of a sequence.
    - Default `blank_index` is `(num_classes - 1)`, unless overriden.

    If `merge_repeated` is `True`, merge repeated classes in output.
    This means that if consecutive logits' maximum indices are the same,
    only the first of these is emitted.  The sequence `A B B * B * B` (where '*'
    is the blank label) becomes

      * `A B B B` if `merge_repeated=True`.
      * `A B B B B` if `merge_repeated=False`.

    Args:
      inputs: 3-D `float` `Tensor` sized `[max_time, batch_size, num_classes]`.
        The logits.
      sequence_length: 1-D `int32` vector containing sequence lengths, having size
        `[batch_size]`.
      merge_repeated: Boolean.  Default: True.
      blank_index: (Optional). Default: `num_classes - 1`. Define the class index
        to use for the blank label. Negative values will start from num_classes,
        ie, -1 will reproduce the ctc_greedy_decoder behavior of using
        num_classes - 1 for the blank symbol, which corresponds to the default.

    Returns:
      A tuple `(decoded, neg_sum_logits)` where

      decoded: A single-element list. `decoded[0]`
        is an `SparseTensor` containing the decoded outputs s.t.:

        `decoded.indices`: Indices matrix `(total_decoded_outputs, 2)`.
          The rows store: `[batch, time]`.

        `decoded.values`: Values vector, size `(total_decoded_outputs)`.
          The vector stores the decoded classes.

        `decoded.dense_shape`: Shape vector, size `(2)`.
          The shape values are: `[batch_size, max_decoded_length]`

      neg_sum_logits: A `float` matrix `(batch_size x 1)` containing, for the
          sequence found, the negative of the sum of the greatest logit at each
          timeframe.
    """
    ...
def ctc_loss(
    labels: Tensor,
    logits: Tensor,
    label_length: Tensor,
    logit_length: Tensor,
    logits_time_major: bool = True,
    unique: int | None = None,
    blank_index: int | None = None,
    name: str | None = None,
) -> Tensor: ...
def ctc_unique_labels(labels: Tensor, name: str | None = None) -> tuple[Tensor, Tensor]: ...

@overload
def embedding_lookup(
    params: TensorCompatible, ids: TensorCompatible, max_norm: float | None = None, name: str | None = None
) -> Tensor:
    """
    Looks up embeddings for the given `ids` from a list of tensors.

    This function is used to perform parallel lookups on the list of tensors in
    `params`.  It is a generalization of `tf.gather`, where `params` is
    interpreted as a partitioning of a large embedding tensor.

    If `len(params) > 1`, each element `id` of `ids` is partitioned between the
    elements of `params` according to the "div" partition strategy, which means we
    assign ids to partitions in a contiguous manner. For instance, 13 ids are
    split across 5 partitions as:
    `[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10], [11, 12]]`.

    If the id space does not evenly divide the number of partitions, each of the
    first `(max_id + 1) % len(params)` partitions will be assigned one more id.

    The results of the lookup are concatenated into a dense
    tensor. The returned tensor has shape `shape(ids) + shape(params)[1:]`.

    Args:
      params: A single tensor representing the complete embedding tensor, or a
        list of tensors all of same shape except for the first dimension,
        representing sharded embedding tensors following "div" partition strategy.
      ids: A `Tensor` with type `int32` or `int64` containing the ids to be looked
        up in `params`.
      max_norm: If not `None`, each embedding is clipped if its l2-norm is larger
        than this value.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` with the same type as the tensors in `params`.

      For instance, if `params` is a 5x2 matrix:

      ```python
      [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
      ```

      or a list of matrices:

      ```python
      params[0]: [[1, 2], [3, 4]]
      params[1]: [[5, 6], [7, 8]]
      params[2]: [[9, 10]]
      ```

      and `ids` is:

      ```python
      [0, 3, 4]
      ```

      The output will be a 3x2 matrix:

      ```python
      [[1, 2], [7, 8], [9, 10]]
      ```

    Raises:
      ValueError: If `params` is empty.
    """
    ...
@overload
def embedding_lookup(
    params: TensorCompatible, ids: RaggedTensor, max_norm: float | None = None, name: str | None = None
) -> RaggedTensor: ...

def leaky_relu(features: TensorCompatible, alpha: float = 0.2, name: str | None = None) -> Tensor: ...
def log_poisson_loss(
    targets: TensorCompatible, log_input: TensorCompatible, compute_full_loss: bool = False, name: str | None = None
) -> Tensor:
    """
    Computes log Poisson loss given `log_input`.

    Gives the log-likelihood loss between the prediction and the target under the
    assumption that the target has a Poisson distribution.
    Caveat: By default, this is not the exact loss, but the loss minus a
      constant term [log(z!)]. That has no effect for optimization, but
      does not play well with relative loss comparisons. To compute an
      approximation of the log factorial term, specify
      compute_full_loss=True to enable Stirling's Approximation.

    For brevity, let `c = log(x) = log_input`, `z = targets`.  The log Poisson
    loss is

          -log(exp(-x) * (x^z) / z!)
        = -log(exp(-x) * (x^z)) + log(z!)
        ~ -log(exp(-x)) - log(x^z) [+ z * log(z) - z + 0.5 * log(2 * pi * z)]
            [ Note the second term is the Stirling's Approximation for log(z!).
              It is invariant to x and does not affect optimization, though
              important for correct relative loss comparisons. It is only
              computed when compute_full_loss == True. ]
        = x - z * log(x) [+ z * log(z) - z + 0.5 * log(2 * pi * z)]
        = exp(c) - z * c [+ z * log(z) - z + 0.5 * log(2 * pi * z)]

    Args:
      targets: A `Tensor` of the same type and shape as `log_input`.
      log_input: A `Tensor` of type `float32` or `float64`.
      compute_full_loss: whether to compute the full loss. If false, a constant
        term is dropped in favor of more efficient optimization.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of the same shape as `log_input` with the componentwise
      logistic losses.

    Raises:
      ValueError: If `log_input` and `targets` do not have the same shape.
    """
    ...

# tf.nn.moments's shift is not used in the current implementation.
def moments(
    x: TensorCompatible | RaggedTensor,
    axes: TensorCompatible,
    shift: None | Any = None,
    keepdims: bool = False,
    name: str | None = None,
) -> tuple[Tensor, Tensor]:
    """
    Calculates the mean and variance of `x`.

    The mean and variance are calculated by aggregating the contents of `x`
    across `axes`.  If `x` is 1-D and `axes = [0]` this is just the mean
    and variance of a vector.

    Note: shift is currently not used; the true mean is computed and used.

    When using these moments for batch normalization (see
    `tf.nn.batch_normalization`):

     * for so-called "global normalization", used with convolutional filters with
       shape `[batch, height, width, depth]`, pass `axes=[0, 1, 2]`.
     * for simple batch normalization pass `axes=[0]` (batch only).

    Args:
      x: A `Tensor`.
      axes: Array of ints.  Axes along which to compute mean and
        variance.
      shift: Not used in the current implementation.
      keepdims: produce moments with the same dimensionality as the input.
      name: Name used to scope the operations that compute the moments.

    Returns:
      Two `Tensor` objects: `mean` and `variance`.
    """
    ...
def relu(features: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Computes rectified linear: `max(features, 0)`.

    See: https://en.wikipedia.org/wiki/Rectifier_(neural_networks)
    Example usage:
    >>> tf.nn.relu([-2., 0., 3.]).numpy()
    array([0., 0., 3.], dtype=float32)

    Args:
      features: A `Tensor`. Must be one of the following types: `float32`, `float64`, `int32`, `uint8`, `int16`, `int8`, `int64`, `bfloat16`, `uint16`, `half`, `uint32`, `uint64`, `qint8`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `features`.
    """
    ...
def sigmoid_cross_entropy_with_logits(labels: TensorCompatible, logits: TensorCompatible, name: str | None = None) -> Tensor:
    r"""
    Computes sigmoid cross entropy given `logits`.

    Measures the probability error in tasks with two outcomes in which each
    outcome is independent and need not have a fully certain label. For instance,
    one could perform a regression where the probability of an event happening is
    known and used as a label. This loss may also be used for binary
    classification, where labels are either zero or one.

    For brevity, let `x = logits`, `z = labels`.  The logistic loss is

          z * -log(sigmoid(x)) + (1 - z) * -log(1 - sigmoid(x))
        = z * -log(1 / (1 + exp(-x))) + (1 - z) * -log(exp(-x) / (1 + exp(-x)))
        = z * log(1 + exp(-x)) + (1 - z) * (-log(exp(-x)) + log(1 + exp(-x)))
        = z * log(1 + exp(-x)) + (1 - z) * (x + log(1 + exp(-x))
        = (1 - z) * x + log(1 + exp(-x))
        = x - x * z + log(1 + exp(-x))

    For x < 0, to avoid overflow in exp(-x), we reformulate the above

          x - x * z + log(1 + exp(-x))
        = log(exp(x)) - x * z + log(1 + exp(-x))
        = - x * z + log(1 + exp(x))

    Hence, to ensure stability and avoid overflow, the implementation uses this
    equivalent formulation

        max(x, 0) - x * z + log(1 + exp(-abs(x)))

    `logits` and `labels` must have the same type and shape.

    >>> logits = tf.constant([1., -1., 0., 1., -1., 0., 0.])
    >>> labels = tf.constant([0., 0., 0., 1., 1., 1., 0.5])
    >>> tf.nn.sigmoid_cross_entropy_with_logits(
    ...     labels=labels, logits=logits).numpy()
    array([1.3132617, 0.3132617, 0.6931472, 0.3132617, 1.3132617, 0.6931472,
           0.6931472], dtype=float32)

    Compared to the losses which handle multiple outcomes,
    `tf.nn.softmax_cross_entropy_with_logits` for general multi-class
    classification and `tf.nn.sparse_softmax_cross_entropy_with_logits` for more
    efficient multi-class classification with hard labels,
    `sigmoid_cross_entropy_with_logits` is a slight simplification for binary
    classification:

          sigmoid(x) = softmax([x, 0])[0]

    $$\frac{1}{1 + e^{-x}} = \frac{e^x}{e^x + e^0}$$

    While `sigmoid_cross_entropy_with_logits` works for soft binary labels
    (probabilities between 0 and 1), it can also be used for binary classification
    where the labels are hard. There is an equivalence between all three symbols
    in this case, with a probability 0 indicating the second class or 1 indicating
    the first class:

    >>> sigmoid_logits = tf.constant([1., -1., 0.])
    >>> softmax_logits = tf.stack([sigmoid_logits, tf.zeros_like(sigmoid_logits)],
    ...                           axis=-1)
    >>> soft_binary_labels = tf.constant([1., 1., 0.])
    >>> soft_multiclass_labels = tf.stack(
    ...     [soft_binary_labels, 1. - soft_binary_labels], axis=-1)
    >>> hard_labels = tf.constant([0, 0, 1])
    >>> tf.nn.sparse_softmax_cross_entropy_with_logits(
    ...     labels=hard_labels, logits=softmax_logits).numpy()
    array([0.31326166, 1.3132616 , 0.6931472 ], dtype=float32)
    >>> tf.nn.softmax_cross_entropy_with_logits(
    ...     labels=soft_multiclass_labels, logits=softmax_logits).numpy()
    array([0.31326166, 1.3132616, 0.6931472], dtype=float32)
    >>> tf.nn.sigmoid_cross_entropy_with_logits(
    ...     labels=soft_binary_labels, logits=sigmoid_logits).numpy()
    array([0.31326166, 1.3132616, 0.6931472], dtype=float32)

    Args:
      labels: A `Tensor` of the same type and shape as `logits`. Between 0 and 1,
        inclusive.
      logits: A `Tensor` of type `float32` or `float64`. Any real number.
      name: A name for the operation (optional).

    Returns:
      A `Tensor` of the same shape as `logits` with the componentwise
      logistic losses.

    Raises:
      ValueError: If `logits` and `labels` do not have the same shape.
    """
    ...
def softmax(logits: TensorCompatible, axis: ScalarTensorCompatible | None = None, name: str | None = None) -> Tensor:
    """
    Computes softmax activations.

    Used for multi-class predictions. The sum of all outputs generated by softmax
    is 1.

    This function performs the equivalent of

    ```python
    softmax = tf.exp(logits) / tf.reduce_sum(tf.exp(logits), axis, keepdims=True)
    ```
    Example usage:

    >>> softmax = tf.nn.softmax([-1, 0., 1.])
    >>> softmax
    <tf.Tensor: shape=(3,), dtype=float32,
    numpy=array([0.09003057, 0.24472848, 0.66524094], dtype=float32)>
    >>> sum(softmax)
    <tf.Tensor: shape=(), dtype=float32, numpy=1.0>

    Args:
      logits: A non-empty `Tensor`. Must be one of the following types: `half`,
        `float32`, `float64`.
      axis: The dimension softmax would be performed on. The default is -1 which
        indicates the last dimension.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type and shape as `logits`.

    Raises:
      InvalidArgumentError: if `logits` is empty or `axis` is beyond the last
        dimension of `logits`.
    """
    ...
def selu(features: TensorCompatible, name: str | None = None) -> Tensor:
    """
    Computes scaled exponential linear: `scale * alpha * (exp(features) - 1)`

    if < 0, `scale * features` otherwise.

    To be used together with
    `initializer = tf.variance_scaling_initializer(factor=1.0, mode='FAN_IN')`.
    For correct dropout, use `tf.contrib.nn.alpha_dropout`.

    See [Self-Normalizing Neural Networks](https://arxiv.org/abs/1706.02515)

    Args:
      features: A `Tensor`. Must be one of the following types: `half`, `bfloat16`, `float32`, `float64`.
      name: A name for the operation (optional).

    Returns:
      A `Tensor`. Has the same type as `features`.
    """
    ...
def safe_embedding_lookup_sparse(
    embedding_weights: Tensor | list[Tensor],
    sparse_ids: SparseTensor,
    sparse_weights: SparseTensor | None = None,
    combiner: str = "mean",
    default_id: ScalarTensorCompatible | None = None,
    max_norm: float | None = None,
    name: str | None = None,
    allow_fast_lookup: bool = False,
) -> Tensor:
    """
    Lookup embedding results, accounting for invalid IDs and empty features.

    The partitioned embedding in `embedding_weights` must all be the same shape
    except for the first dimension. The first dimension is allowed to vary as the
    vocabulary size is not necessarily a multiple of num of shards.

    This is similar to `tf.nn.embedding_lookup_sparse`, except invalid IDs (< 0)
    are pruned from input IDs and weights, as well as any IDs with non-positive
    weight. For an entry with no features, the embedding vector for `default_id`
    is returned, or the 0-vector if `default_id` is not supplied. See
    `tf.nn.embedding_lookup_sparse` for more information on how sparse embedding
    lookups work in general.

    The ids and weights may be multi-dimensional `SparseTensor`s or
    `RaggedTensor`s with rank of 2. For `SpareTensor`s with left-aligned non-zero
    entries which can be described as `RaggedTensor`s, use of `RaggedTensor`s can
    yield higher performance.

    If `len(embedding_weights) > 1`, each element `id` of `ids` is partitioned
    between the elements of `embedding_weights` according to the "div" partition
    strategy, which means we assign ids to partitions in a contiguous manner. For
    instance, 13 ids are split across 5 partitions as:
    `[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10], [11, 12]]`.

    If the id space does not evenly divide the number of partitions, each of the
    first `(max_id + 1) % len(embedding_weights)` partitions will be assigned one
    more id.

    Args:
      embedding_weights: A single tensor representing the complete embedding
        tensor, or a list of tensors all of same shape except for the first
        dimension, representing sharded embedding tensors following "div"
        partition strategy.
      sparse_ids: `SparseTensor` of shape `[d_0, d_1, ..., d_n]` containing the
        ids, where `d_0` is typically batch size, or a `RaggedTensor` with rank 2.
      sparse_weights: `SparseTensor` or `RaggedTensor` of same type and shape as
        `sparse_ids`, containing float weights corresponding to `sparse_ids`, or
        `None` if all weights are assumed to be 1.0.
      combiner: A string specifying how to combine embedding results for each
        entry. Currently "mean", "sqrtn" and "sum" are supported, with "mean" the
        default.
      default_id: The id to use for an entry with no features. Defaults to
        0-vector.
      max_norm: If not `None`, all embeddings are l2-normalized to max_norm before
        combining.
      name: A name for this operation (optional).
      allow_fast_lookup: An optional boolean specifying whether to allow
        simplified embedding lookups when `params` is a single tensor and
        `max_norm` is `None`. Setting this flag to `True` during training can
        cause the use of dense gradients with increased memory footprint.

    Returns:
      A dense tensor representing the combined embeddings for the
      sparse ids. For each row in the dense tensor represented by `sparse_ids`,
      the op looks up the embeddings for all ids in that row, multiplies them by
      the corresponding weight, and combines these embeddings as specified.

      In other words, if

        `shape(combined embedding_weights) = [p0, p1, ..., pm]`

      and

        `shape(sparse_ids) = shape(sparse_weights) = [d0, d1, ..., dn]`

      then

        `shape(output) = [d0, d1, ... dn-1, p1, ..., pm]`.

      For instance, if params is a 10x20 matrix, and sp_ids / sp_weights are

        ```python
        [0, 0]: id 1, weight 2.0
        [0, 1]: id 3, weight 0.5
        [1, 0]: id -1, weight 1.0
        [2, 3]: id 1, weight 3.0
        ```

      `default_id` is 0.

      with `combiner`="mean", then the output will be a 3x20 matrix where

        ```python
        output[0, :] = (params[1, :] * 2.0 + params[3, :] * 0.5) / (2.0 + 0.5)
        output[1, :] = (params[0, :] * 1.0) / 1.0
        output[2, :] = (params[1, :] * 3.0) / 3.0
        ```

    Raises:
      ValueError: if `embedding_weights` is empty.
    """
    ...
def __getattr__(name: str): ...  # incomplete module

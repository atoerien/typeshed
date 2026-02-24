"""Public API for tf._api.v2.saved_model namespace"""

from _typeshed import Incomplete
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Generic, Literal, TypeVar
from typing_extensions import ParamSpec, TypeAlias

import tensorflow as tf
from tensorflow.python.training.tracking.autotrackable import AutoTrackable
from tensorflow.saved_model.experimental import VariablePolicy
from tensorflow.types.experimental import ConcreteFunction, PolymorphicFunction

_P = ParamSpec("_P")
_R_co = TypeVar("_R_co", covariant=True)

class Asset:
    """
    Represents a file asset to hermetically include in a SavedModel.

    A SavedModel can include arbitrary files, called assets, that are needed
    for its use. For example a vocabulary file used initialize a lookup table.

    When a trackable object is exported via `tf.saved_model.save()`, all the
    `Asset`s reachable from it are copied into the SavedModel assets directory.
    Upon loading, the assets and the serialized functions that depend on them
    will refer to the correct filepaths inside the SavedModel directory.

    Example:

    ```
    filename = tf.saved_model.Asset("file.txt")

    @tf.function(input_signature=[])
    def func():
      return tf.io.read_file(filename)

    trackable_obj = tf.train.Checkpoint()
    trackable_obj.func = func
    trackable_obj.filename = filename
    tf.saved_model.save(trackable_obj, "/tmp/saved_model")

    # The created SavedModel is hermetic, it does not depend on
    # the original file and can be moved to another path.
    tf.io.gfile.remove("file.txt")
    tf.io.gfile.rename("/tmp/saved_model", "/tmp/new_location")

    reloaded_obj = tf.saved_model.load("/tmp/new_location")
    print(reloaded_obj.func())
    ```

    Attributes:
      asset_path: A path, or a 0-D `tf.string` tensor with path to the asset.
    """
    @property
    def asset_path(self) -> tf.Tensor:
        """Fetch the current asset path."""
        ...
    def __init__(self, path: str | Path | tf.Tensor) -> None:
        """Record the full path to the asset."""
        ...

class LoadOptions:
    """
    Options for loading a SavedModel.

    This function may be used in the `options` argument in functions that
    load a SavedModel (`tf.saved_model.load`, `tf.keras.models.load_model`).
    """
    __slots__ = (
        "allow_partial_checkpoint",
        "experimental_io_device",
        "experimental_skip_checkpoint",
        "experimental_variable_policy",
        "experimental_load_function_aliases",
    )
    allow_partial_checkpoint: bool
    experimental_io_device: str | None
    experimental_skip_checkpoint: bool
    experimental_variable_policy: VariablePolicy | None
    experimental_load_function_aliases: bool

    def __init__(
        self,
        allow_partial_checkpoint: bool = False,
        experimental_io_device: str | None = None,
        experimental_skip_checkpoint: bool = False,
        experimental_variable_policy: (
            VariablePolicy | Literal["expand_distributed_variables", "save_variable_devices"] | None
        ) = None,
        experimental_load_function_aliases: bool = False,
    ) -> None:
        """
        Creates an object that stores options for SavedModel loading.

        *When to set `allow_partial_checkpoint=True`?*

        This can be used when loading a Keras model (`tf.keras.models.load_model`)
        with custom objects. When new variables are added to the custom object
        class, loading will fail the assertion check that all loaded variables have
        been restored, because the SavedModel checkpoint only contains the variables
        that were in original the custom object.
        See the following example:

        ```
        class Custom(tf.keras.Model):
          def __init__(self):
            super(Custom, self).__init__()
            self.v = tf.Variable(...)

          def call(self, inputs):
            return ...

        model = Custom()
        model.save(...)
        ```

        After saving, say that `Custom` is updated to include an additional
        variable.

        ```
        class Custom(tf.keras.Model):
          def __init__(self):
            super(Custom, self).__init__()
            self.v = tf.Variable(...)
            self.w = tf.Variable(...)

          def call(self, inputs):
            return ...
        ```

        `tf.keras.models.load_model(path, custom_objects={'Custom': Custom})` fails
        to load since `Custom.w` does not exist in the SavedModel checkpoint. To
        acknowledge that there are variables that are not restored from the
        checkpoint and successfully load the model, call:

        ```
        tf.keras.models.load_model(
          path, custom_objects={'Custom': Custom},
          options=tf.saved_model.LoadOptions(allow_partial_checkpoint=True))
        ```

        Args:
          allow_partial_checkpoint: bool. Defaults to `False`. When enabled, allows
            the SavedModel checkpoint to not entirely match the loaded object.
          experimental_io_device: string. Applies in a distributed setting.
            Tensorflow device to use to access the filesystem. If `None` (default)
            then for each variable the filesystem is accessed from the CPU:0 device
            of the host where that variable is assigned. If specified, the
            filesystem is instead accessed from that device for all variables.
            This is for example useful if you want to load from a local directory,
            such as "/tmp" when running in a distributed setting. In that case
            pass a device for the host where the "/tmp" directory is accessible.
          experimental_skip_checkpoint: bool. Defaults to `False`. If set to `True`,
            checkpoints will not be restored. Note that this in the majority of
            cases will generate an unusable model.
          experimental_variable_policy: string. The policy to apply to variables
            when loading. This is either a `saved_model.experimental.VariablePolicy`
            enum instance or one of its value strings (case is not important). See
            that enum documentation for details. A value of `None` corresponds to
            the default policy.
          experimental_load_function_aliases: bool. Defaults to `False`. If set to
            `True`, a `function_aliases` attribute will be added to the loaded
            SavedModel object.

        Example:

          load_options = tf.saved_model.LoadOptions(experimental_io_device=
            '/job:localhost')
          restoredmodel = tf.keras.models.load_model(saved_model_path,
                                                     options=load_options)
        """
        ...

class SaveOptions:
    """
    Options for saving to SavedModel.

    This function may be used in the `options` argument in functions that
    save a SavedModel (`tf.saved_model.save`, `tf.keras.models.save_model`).
    """
    __slots__ = (
        "namespace_whitelist",
        "save_debug_info",
        "function_aliases",
        "experimental_debug_stripper",
        "experimental_io_device",
        "experimental_variable_policy",
        "experimental_custom_gradients",
        "experimental_image_format",
        "experimental_skip_saver",
        "experimental_sharding_callback",
        "extra_tags",
    )
    namespace_whitelist: list[str]
    save_debug_info: bool
    function_aliases: dict[str, PolymorphicFunction[..., object]]
    experimental_debug_stripper: bool
    experimental_io_device: str
    experimental_variable_policy: VariablePolicy
    experimental_custom_gradients: bool
    experimental_image_format: bool
    experimental_skip_saver: bool
    experimental_sharding_callback: Incomplete | None
    extra_tags: Incomplete | None
    def __init__(
        self,
        namespace_whitelist: list[str] | None = None,
        save_debug_info: bool = False,
        function_aliases: Mapping[str, PolymorphicFunction[..., object]] | None = None,
        experimental_debug_stripper: bool = False,
        experimental_io_device: str | None = None,
        experimental_variable_policy: str | VariablePolicy | None = None,
        experimental_custom_gradients: bool = True,
        experimental_image_format: bool = False,
        experimental_skip_saver: bool = False,
        experimental_sharding_callback=None,
        extra_tags=None,
    ) -> None:
        """
        Creates an object that stores options for SavedModel saving.

        Args:
          namespace_whitelist: List of strings containing op namespaces to whitelist
            when saving a model. Saving an object that uses namespaced ops must
            explicitly add all namespaces to the whitelist. The namespaced ops must
            be registered into the framework when loading the SavedModel. If no
            whitelist is provided, all namespaced ops will be allowed.
          save_debug_info: Boolean indicating whether debug information is saved. If
            True, then a debug/saved_model_debug_info.pb file will be written with
            the contents of a GraphDebugInfo binary protocol buffer containing stack
            trace information for all ops and functions that are saved.
          function_aliases: Python dict. Mapping from string to object returned by
            @tf.function. A single tf.function can generate many ConcreteFunctions.
            If a downstream tool wants to refer to all concrete functions generated
            by a single tf.function you can use the `function_aliases` argument to
            store a map from the alias name to all concrete function names. E.g. >>>
            class Adder(tf.Module): ...   @tf.function ...   def double(self, x):
            ...     return x + x  >>> model = Adder() >>>
            model.double.get_concrete_function( ...   tf.TensorSpec(shape=[],
            dtype=tf.float32, name="float_input")) >>>
            model.double.get_concrete_function( ...   tf.TensorSpec(shape=[],
            dtype=tf.string, name="string_input"))  >>> options =
            tf.saved_model.SaveOptions( ...   function_aliases={'double':
            model.double}) >>> tf.saved_model.save(model, '/tmp/adder',
            options=options)
          experimental_debug_stripper: bool. If set to True, this strips the debug
            nodes from the graph, from both the nodes and the function defs. Note
            that this currently only strips the `Assert` nodes from the graph and
            converts them into `NoOp`s instead.
          experimental_io_device: string. Applies in a distributed setting.
            Tensorflow device to use to access the filesystem. If `None` (default)
            then for each variable the filesystem is accessed from the CPU:0 device
            of the host where that variable is assigned. If specified, the
            filesystem is instead accessed from that device for all variables.  This
            is for example useful if you want to save to a local directory, such as
            "/tmp" when running in a distributed setting. In that case pass a device
            for the host where the "/tmp" directory is accessible.
          experimental_variable_policy: The policy to apply to variables when
            saving. This is either a `saved_model.experimental.VariablePolicy` enum
            instance or one of its value strings (case is not important). See that
            enum documentation for details. A value of `None` corresponds to the
            default policy.
          experimental_custom_gradients: Boolean. When True, will save traced
            gradient functions for the functions decorated by `tf.custom_gradient`.
            Defaults to `True`.
          experimental_image_format: New (highly) experimental format that is
            capable of saving models larger than the 2GB protobuf limit. Enabling
            this option will likely break compatibility with downstream consumers.
            This option is currently disabled in OSS.
          experimental_skip_saver: If True, will prevent SavedModel from creating
            its native checkpointing ops - this is for models that do not use
            SavedModel's native checkpointing functionality to avoid the costs
            associated with creating and serializing those ops.
          experimental_sharding_callback: `tf.train.experimental.ShardingCallback`.
            A pre-made or custom callback that determines how checkpoints are
            sharded on disk. Pre-made callback options are
            `tf.train.experimental.ShardByDevicePolicy` and
            `tf.train.experimental.MaxShardSizePolicy`. You may also write a custom
            callback, see `tf.train.experimental.ShardingCallback`.
          extra_tags: Extra tags to be saved with the MetaGraph in the SavedModel.
        """
        ...

def contains_saved_model(export_dir: str | Path) -> bool:
    """
    Checks whether the provided export directory could contain a SavedModel.

    Note that the method does not load any data by itself. If the method returns
    `false`, the export directory definitely does not contain a SavedModel. If the
    method returns `true`, the export directory may contain a SavedModel but
    provides no guarantee that it can be loaded.

    Args:
      export_dir: Absolute path to possible export location. For example,
                  '/my/foo/model'.

    Returns:
      True if the export directory contains SavedModel files, False otherwise.
    """
    ...

class _LoadedAttributes(Generic[_P, _R_co]):
    signatures: Mapping[str, ConcreteFunction[_P, _R_co]]

class _LoadedModel(AutoTrackable, _LoadedAttributes[_P, _R_co]):
    variables: list[tf.Variable]
    trainable_variables: list[tf.Variable]
    # TF1 model artifact specific
    graph: tf.Graph

def load(
    export_dir: str, tags: str | Sequence[str] | None = None, options: LoadOptions | None = None
) -> _LoadedModel[..., Any]:
    """
    Load a SavedModel from `export_dir`.

    Signatures associated with the SavedModel are available as functions:

    ```python
    imported = tf.saved_model.load(path)
    f = imported.signatures["serving_default"]
    print(f(x=tf.constant([[1.]])))
    ```

    Objects exported with `tf.saved_model.save` additionally have trackable
    objects and functions assigned to attributes:

    ```python
    exported = tf.train.Checkpoint(v=tf.Variable(3.))
    exported.f = tf.function(
        lambda x: exported.v * x,
        input_signature=[tf.TensorSpec(shape=None, dtype=tf.float32)])
    tf.saved_model.save(exported, path)
    imported = tf.saved_model.load(path)
    assert 3. == imported.v.numpy()
    assert 6. == imported.f(x=tf.constant(2.)).numpy()
    ```

    _Loading Keras models_

    Keras models are trackable, so they can be saved to SavedModel. The object
    returned by `tf.saved_model.load` is not a Keras object (i.e. doesn't have
    `.fit`, `.predict`, etc. methods). A few attributes and functions are still
    available: `.variables`, `.trainable_variables` and `.__call__`.

    ```python
    model = tf.keras.Model(...)
    tf.saved_model.save(model, path)
    imported = tf.saved_model.load(path)
    outputs = imported(inputs)
    ```

    Use `tf.keras.models.load_model` to restore the Keras model.

    _Importing SavedModels from TensorFlow 1.x_

    1.x SavedModels APIs have a flat graph instead of `tf.function` objects.
    These SavedModels will be loaded with the following attributes:

    * `.signatures`: A dictionary mapping signature names to functions.
    * `.prune(feeds, fetches) `: A method which allows you to extract
      functions for new subgraphs. This is equivalent to importing the SavedModel
      and naming feeds and fetches in a Session from TensorFlow 1.x.

      ```python
      imported = tf.saved_model.load(path_to_v1_saved_model)
      pruned = imported.prune("x:0", "out:0")
      pruned(tf.ones([]))
      ```

      See `tf.compat.v1.wrap_function` for details.
    * `.variables`: A list of imported variables.
    * `.graph`: The whole imported graph.
    * `.restore(save_path)`: A function that restores variables from a checkpoint
      saved from `tf.compat.v1.Saver`.

    _Consuming SavedModels asynchronously_

    When consuming SavedModels asynchronously (the producer is a separate
    process), the SavedModel directory will appear before all files have been
    written, and `tf.saved_model.load` will fail if pointed at an incomplete
    SavedModel. Rather than checking for the directory, check for
    "saved_model_dir/saved_model.pb". This file is written atomically as the last
    `tf.saved_model.save` file operation.

    Args:
      export_dir: The SavedModel directory to load from.
      tags: A tag or sequence of tags identifying the MetaGraph to load. Optional
        if the SavedModel contains a single MetaGraph, as for those exported from
        `tf.saved_model.save`.
      options: `tf.saved_model.LoadOptions` object that specifies options for
        loading.

    Returns:
      A trackable object with a `signatures` attribute mapping from signature
      keys to functions. If the SavedModel was exported by `tf.saved_model.save`,
      it also points to trackable objects, functions, debug info which it has been
      saved.

    Raises:
      ValueError: If `tags` don't match a MetaGraph in the SavedModel.
    """
    ...

_TF_Function: TypeAlias = ConcreteFunction[..., object] | PolymorphicFunction[..., object]

def save(
    obj: tf.Module,
    export_dir: str,
    signatures: _TF_Function | Mapping[str, _TF_Function] | None = None,
    options: SaveOptions | None = None,
) -> None:
    """
    Exports a [tf.Module](https://www.tensorflow.org/api_docs/python/tf/Module) (and subclasses) `obj` to [SavedModel format](https://www.tensorflow.org/guide/saved_model#the_savedmodel_format_on_disk).

    The `obj` must inherit from the [`Trackable`
    class](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/trackable/base.py#L278).

    Example usage:

    >>> class Adder(tf.Module):
    ...   @tf.function(input_signature=[tf.TensorSpec(shape=[], dtype=tf.float32)])
    ...   def add(self, x):
    ...     return x + x

    >>> model = Adder()
    >>> tf.saved_model.save(model, '/tmp/adder')

    The resulting SavedModel is then servable with an input named "x", a scalar
    with dtype float32.

    _Signatures_

    Signatures define the input and output types for a computation. The optional
    save `signatures` argument controls which methods in `obj` will be
    available to programs which consume `SavedModel`s, for example, serving
    APIs. Python functions may be decorated with
    `@tf.function(input_signature=...)` and passed as signatures directly, or
    lazily with a call to `get_concrete_function` on the method decorated with
    `@tf.function`.

    Example:

    >>> class Adder(tf.Module):
    ...   @tf.function
    ...   def add(self, x):
    ...     return x + x

    >>> model = Adder()
    >>> tf.saved_model.save(
    ...   model, '/tmp/adder',signatures=model.add.get_concrete_function(
    ...     tf.TensorSpec([], tf.float32)))

    If a `@tf.function` does not have an input signature and
    `get_concrete_function` is not called on that method, the function will not
    be directly callable in the restored SavedModel.

    Example:

    >>> class Adder(tf.Module):
    ...   @tf.function
    ...   def add(self, x):
    ...     return x + x

    >>> model = Adder()
    >>> tf.saved_model.save(model, '/tmp/adder')
    >>> restored = tf.saved_model.load('/tmp/adder')
    >>> restored.add(1.)
    Traceback (most recent call last):
    ...
    ValueError: Found zero restored functions for caller function.

    If the `signatures` argument is omitted, `obj` will be searched for
    `@tf.function`-decorated methods. If exactly one traced `@tf.function` is
    found, that method will be used as the default signature for the SavedModel.
    Else, any `@tf.function` attached to `obj` or its dependencies will be
    exported for use with `tf.saved_model.load`.

    When invoking a signature in an exported SavedModel, `Tensor` arguments are
    identified by name. These names will come from the Python function's argument
    names by default. They may be overridden by specifying a `name=...` argument
    in the corresponding `tf.TensorSpec` object. Explicit naming is required if
    multiple `Tensor`s are passed through a single argument to the Python
    function.

    The outputs of functions used as `signatures` must either be flat lists, in
    which case outputs will be numbered, or a dictionary mapping string keys to
    `Tensor`, in which case the keys will be used to name outputs.

    Signatures are available in objects returned by `tf.saved_model.load` as a
    `.signatures` attribute. This is a reserved attribute: `tf.saved_model.save`
    on an object with a custom `.signatures` attribute will raise an exception.

    _Using `tf.saved_model.save` with Keras models_

    While Keras has its own [saving and loading
    API](https://www.tensorflow.org/guide/keras/save_and_serialize),
    this function can be used to export Keras models. For example, exporting with
    a signature specified:

    >>> class Adder(tf.keras.Model):
    ...   @tf.function(input_signature=[tf.TensorSpec(shape=[], dtype=tf.string)])
    ...   def concat(self, x):
    ...      return x + x

    >>> model = Adder()
    >>> tf.saved_model.save(model, '/tmp/adder')

    Exporting from a function without a fixed signature:

    >>> class Adder(tf.keras.Model):
    ...   @tf.function
    ...   def concat(self, x):
    ...      return x + x

    >>> model = Adder()
    >>> tf.saved_model.save(
    ...   model, '/tmp/adder',
    ...   signatures=model.concat.get_concrete_function(
    ...     tf.TensorSpec(shape=[], dtype=tf.string, name="string_input")))

    `tf.keras.Model` instances constructed from inputs and outputs already have a
    signature and so do not require a `@tf.function` decorator or a `signatures`
    argument. If neither are specified, the model's forward pass is exported.

    >>> x = tf.keras.layers.Input((4,), name="x")
    >>> y = tf.keras.layers.Dense(5, name="out")(x)
    >>> model = tf.keras.Model(x, y)
    >>> tf.saved_model.save(model, '/tmp/saved_model/')

    The exported SavedModel takes "x" with shape [None, 4] and returns "out"
    with shape [None, 5]

    _Variables and Checkpoints_

    Variables must be tracked by assigning them to an attribute of a tracked
    object or to an attribute of `obj` directly. TensorFlow objects (e.g. layers
    from `tf.keras.layers`, optimizers from `tf.train`) track their variables
    automatically. This is the same tracking scheme that `tf.train.Checkpoint`
    uses, and an exported `Checkpoint` object may be restored as a training
    checkpoint by pointing `tf.train.Checkpoint.restore` to the SavedModel's
    "variables/" subdirectory.

    `tf.function` does not hard-code device annotations from outside the function
    body, instead of using the calling context's device. This means for example
    that exporting a model that runs on a GPU and serving it on a CPU will
    generally work, with some exceptions:

      * `tf.device` annotations inside the body of the function will be hard-coded
        in the exported model; this type of annotation is discouraged.
      * Device-specific operations, e.g. with "cuDNN" in the name or with
        device-specific layouts, may cause issues.
      * For `ConcreteFunctions`, active distribution strategies will cause device
        placements to be hard-coded in the function.

    SavedModels exported with `tf.saved_model.save` [strip default-valued
    attributes](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/saved_model/README.md#stripping-default-valued-attributes)
    automatically, which removes one source of incompatibilities when the consumer
    of a SavedModel is running an older TensorFlow version than the
    producer. There are however other sources of incompatibilities which are not
    handled automatically, such as when the exported model contains operations
    which the consumer does not have definitions for.

    Args:
      obj: A trackable object (e.g. tf.Module or tf.train.Checkpoint) to export.
      export_dir: A directory in which to write the SavedModel.
      signatures: Optional, one of three types:
        * A `tf.function` with an input signature specified, which will use the
          default serving signature key.
        * The result of `f.get_concrete_function` on a `@tf.function`-decorated
          function `f`, in which case `f` will be used to generate a signature for
          the SavedModel under the default serving signature key.
        * A dictionary, which maps signature keys to either `tf.function`
          instances with input signatures or concrete functions. Keys of such a
          dictionary may be arbitrary strings, but will typically be from the
          `tf.saved_model.signature_constants` module.
      options: `tf.saved_model.SaveOptions` object for configuring save options.

    Raises:
      ValueError: If `obj` is not trackable.

    @compatibility(eager)
    Not well supported when graph building. From TensorFlow 1.x,
    `tf.compat.v1.enable_eager_execution()` should run first. Calling
    tf.saved_model.save in a loop when graph building from TensorFlow 1.x will
    add new save operations to the default graph each iteration.

    May not be called from within a function body.
    @end_compatibility
    """
    ...

ASSETS_DIRECTORY: str = "assets"
ASSETS_KEY: str = "saved_model_assets"
CLASSIFY_INPUTS: str = "inputs"
CLASSIFY_METHOD_NAME: str = "tensorflow/serving/classify"
CLASSIFY_OUTPUT_CLASSES: str = "classes"
CLASSIFY_OUTPUT_SCORES: str = "scores"
DEBUG_DIRECTORY: str = "debug"
DEBUG_INFO_FILENAME_PB: str = "saved_model_debug_info.pb"
DEFAULT_SERVING_SIGNATURE_DEF_KEY: str = "serving_default"
GPU: str = "gpu"
PREDICT_INPUTS: str = "inputs"
PREDICT_METHOD_NAME: str = "tensorflow/serving/predict"
PREDICT_OUTPUTS: str = "outputs"
REGRESS_INPUTS: str = "inputs"
REGRESS_METHOD_NAME: str = "tensorflow/serving/regress"
REGRESS_OUTPUTS: str = "outputs"
SAVED_MODEL_FILENAME_PB: str = "saved_model.pb"
SAVED_MODEL_FILENAME_PBTXT: str = "saved_model.pbtxt"
SAVED_MODEL_SCHEMA_VERSION: int = 1
SERVING: str = "serve"
TPU: str = "tpu"
TRAINING: str = "train"
VARIABLES_DIRECTORY: str = "variables"
VARIABLES_FILENAME: str = "variables"

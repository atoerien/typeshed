"""Public API for tf._api.v2.train namespace"""

from _typeshed import Incomplete
from collections.abc import Callable
from typing import Any, TypeVar
from typing_extensions import Self

import numpy as np
import tensorflow as tf
from tensorflow.core.example.example_pb2 import Example as Example
from tensorflow.core.example.feature_pb2 import (
    BytesList as BytesList,
    Feature as Feature,
    Features as Features,
    FloatList as FloatList,
    Int64List as Int64List,
)
from tensorflow.core.protobuf.cluster_pb2 import ClusterDef as ClusterDef
from tensorflow.core.protobuf.tensorflow_server_pb2 import ServerDef as ServerDef
from tensorflow.python.trackable.base import Trackable
from tensorflow.python.training.tracking.autotrackable import AutoTrackable

class CheckpointOptions:
    """
    Options for constructing a Checkpoint.

    Used as the `options` argument to either `tf.train.Checkpoint.save()` or
    `tf.train.Checkpoint.restore()` methods to adjust how variables are
    saved/restored.

    Example: Run IO ops on "localhost" while saving a checkpoint:

    ```
    step = tf.Variable(0, name="step")
    checkpoint = tf.train.Checkpoint(step=step)
    options = tf.train.CheckpointOptions(experimental_io_device="/job:localhost")
    checkpoint.save("/tmp/ckpt", options=options)
    ```
    """
    __slots__ = (
        "experimental_io_device",
        "experimental_enable_async_checkpoint",
        "experimental_write_callbacks",
        "enable_async",
        "experimental_sharding_callback",
        "experimental_skip_slot_variables",
    )
    experimental_io_device: None | str
    experimental_enable_async_checkpoint: bool
    experimental_write_callbacks: None | list[Callable[[str], object] | Callable[[], object]]
    enable_async: bool
    experimental_sharding_callback: Incomplete  # should be ShardingCallback
    experimental_skip_slot_variables: bool

    def __init__(
        self,
        experimental_io_device: None | str = None,
        experimental_enable_async_checkpoint: bool = False,
        experimental_write_callbacks: None | list[Callable[[str], object] | Callable[[], object]] = None,
        enable_async: bool = False,
        experimental_skip_slot_variables: bool = False,
        experimental_sharding_callback=None,
    ) -> None:
        """
        Creates an object that stores options for a Checkpoint. (deprecated arguments)

        Deprecated: SOME ARGUMENTS ARE DEPRECATED: `(experimental_enable_async_checkpoint)`. They will be removed in a future version.
        Instructions for updating:
        Use enable_async instead

        Args:
          experimental_io_device: string. Applies in a distributed setting.
            Tensorflow device to use to access the filesystem. If `None` (default)
            then for each variable the filesystem is accessed from the CPU:0 device
            of the host where that variable is assigned. If specified, the
            filesystem is instead accessed from that device for all variables.  This
            is for example useful if you want to save to a local directory, such as
            "/tmp" when running in a distributed setting. In that case pass a device
            for the host where the "/tmp" directory is accessible.
          experimental_enable_async_checkpoint: bool Type. Deprecated, please use
            the enable_async option.
          experimental_write_callbacks: List[Callable]. A list of callback functions
            that will be executed after each saving event finishes (i.e. after
            `save()` or `write()`). For async checkpoint, the callbacks will be
            executed only after the async thread finishes saving.  The return values
            of the callback(s) will be ignored. The callback(s) can optionally take
            the `save_path` (the result of `save()` or `write()`) as an argument.
            The callbacks will be executed in the same order of this list after the
            checkpoint has been written.
          enable_async: bool Type. Indicates whether async checkpointing is enabled.
            Default is False, i.e., no async checkpoint.  Async checkpoint moves the
            checkpoint file writing off the main thread, so that the model can
            continue to train while the checkpoint file writing runs in the
            background. Async checkpoint reduces TPU device idle cycles and speeds
            up model training process, while memory consumption may increase.
          experimental_skip_slot_variables: bool Type. If true, ignores slot
            variables during restore. Context: TPU Embedding layers for Serving do
            not properly restore slot variables. This option is a way to omit
            restoring slot variables which are not required for Serving usecase
            anyways.(b/315912101)
          experimental_sharding_callback: `tf.train.experimental.ShardingCallback`.
            A pre-made or custom callback that determines how checkpoints are
            sharded on disk. Pre-made callback options are
            `tf.train.experimental.ShardByDevicePolicy` and
            `tf.train.experimental.MaxShardSizePolicy`. You may also write a custom
            callback, see `tf.train.experimental.ShardingCallback`.
        """
        ...

_T = TypeVar("_T", bound=list[str] | tuple[str] | dict[int, str])

class ClusterSpec:
    """
    Represents a cluster as a set of "tasks", organized into "jobs".

    A `tf.train.ClusterSpec` represents the set of processes that
    participate in a distributed TensorFlow computation. Every
    `tf.distribute.Server` is constructed in a particular cluster.

    To create a cluster with two jobs and five tasks, you specify the
    mapping from job names to lists of network addresses (typically
    hostname-port pairs).

    ```python
    cluster = tf.train.ClusterSpec({"worker": ["worker0.example.com:2222",
                                               "worker1.example.com:2222",
                                               "worker2.example.com:2222"],
                                    "ps": ["ps0.example.com:2222",
                                           "ps1.example.com:2222"]})
    ```

    Each job may also be specified as a sparse mapping from task indices
    to network addresses. This enables a server to be configured without
    needing to know the identity of (for example) all other worker
    tasks:

    ```python
    cluster = tf.train.ClusterSpec({"worker": {1: "worker1.example.com:2222"},
                                    "ps": ["ps0.example.com:2222",
                                           "ps1.example.com:2222"]})
    ```
    """
    def __init__(self, cluster: dict[str, _T] | ClusterDef | ClusterSpec) -> None:
        """
        Creates a `ClusterSpec`.

        Args:
          cluster: A dictionary mapping one or more job names to (i) a list of
            network addresses, or (ii) a dictionary mapping integer task indices to
            network addresses; or a `tf.train.ClusterDef` protocol buffer.

        Raises:
          TypeError: If `cluster` is not a dictionary mapping strings to lists
            of strings, and not a `tf.train.ClusterDef` protobuf.
        """
        ...
    def as_dict(self) -> dict[str, list[str] | tuple[str] | dict[int, str]]:
        """
        Returns a dictionary from job names to their tasks.

        For each job, if the task index space is dense, the corresponding
        value will be a list of network addresses; otherwise it will be a
        dictionary mapping (sparse) task indices to the corresponding
        addresses.

        Returns:
          A dictionary mapping job names to lists or dictionaries
          describing the tasks in those jobs.
        """
        ...
    def num_tasks(self, job_name: str) -> int:
        """
        Returns the number of tasks defined in the given job.

        Args:
          job_name: The string name of a job in this cluster.

        Returns:
          The number of tasks defined in the given job.

        Raises:
          ValueError: If `job_name` does not name a job in this cluster.
        """
        ...

class _CheckpointLoadStatus:
    def assert_consumed(self) -> Self: ...
    def assert_existing_objects_matched(self) -> Self: ...
    def assert_nontrivial_match(self) -> Self: ...
    def expect_partial(self) -> Self: ...

class Checkpoint(AutoTrackable):
    """
    Manages saving/restoring trackable values to disk.

    TensorFlow objects may contain trackable state, such as `tf.Variable`s,
    `tf.keras.optimizers.Optimizer` implementations, `tf.data.Dataset` iterators,
    `tf.keras.Layer` implementations, or  `tf.keras.Model` implementations.
    These are called **trackable objects**.

    A `Checkpoint` object can be constructed to save either a single or group of
    trackable objects to a checkpoint file. It maintains a `save_counter` for
    numbering checkpoints.

    Example:

    ```python
    model = tf.keras.Model(...)
    checkpoint = tf.train.Checkpoint(model)

    # Save a checkpoint to /tmp/training_checkpoints-{save_counter}. Every time
    # checkpoint.save is called, the save counter is increased.
    save_path = checkpoint.save('/tmp/training_checkpoints')

    # Restore the checkpointed values to the `model` object.
    checkpoint.restore(save_path)
    ```

    Example 2:

    ```python
    import tensorflow as tf
    import os

    checkpoint_directory = "/tmp/training_checkpoints"
    checkpoint_prefix = os.path.join(checkpoint_directory, "ckpt")

    # Create a Checkpoint that will manage two objects with trackable state,
    # one we name "optimizer" and the other we name "model".
    checkpoint = tf.train.Checkpoint(optimizer=optimizer, model=model)
    status = checkpoint.restore(tf.train.latest_checkpoint(checkpoint_directory))
    for _ in range(num_training_steps):
      optimizer.minimize( ... )  # Variables will be restored on creation.
    status.assert_consumed()  # Optional sanity checks.
    checkpoint.save(file_prefix=checkpoint_prefix)
    ```

    `Checkpoint.save()` and `Checkpoint.restore()` write and read object-based
    checkpoints, in contrast to TensorFlow 1.x's `tf.compat.v1.train.Saver` which
    writes and
    reads `variable.name` based checkpoints. Object-based checkpointing saves a
    graph of dependencies between Python objects (`Layer`s, `Optimizer`s,
    `Variable`s, etc.) with named edges, and this graph is used to match variables
    when restoring a checkpoint. It can be more robust to changes in the Python
    program, and helps to support restore-on-create for variables.

    `Checkpoint` objects have dependencies on the objects passed as keyword
    arguments to their constructors, and each dependency is given a name that is
    identical to the name of the keyword argument for which it was created.
    TensorFlow classes like `Layer`s and `Optimizer`s will automatically add
    dependencies on their own variables (e.g. "kernel" and "bias" for
    `tf.keras.layers.Dense`). Inheriting from `tf.keras.Model` makes managing
    dependencies easy in user-defined classes, since `Model` hooks into attribute
    assignment. For example:

    ```python
    class Regress(tf.keras.Model):

      def __init__(self):
        super().__init__()
        self.input_transform = tf.keras.layers.Dense(10)
        # ...

      def call(self, inputs):
        x = self.input_transform(inputs)
        # ...
    ```

    This `Model` has a dependency named "input_transform" on its `Dense` layer,
    which in turn depends on its variables. As a result, saving an instance of
    `Regress` using `tf.train.Checkpoint` will also save all the variables created
    by the `Dense` layer.

    When variables are assigned to multiple workers, each worker writes its own
    section of the checkpoint. These sections are then merged/re-indexed to behave
    as a single checkpoint. This avoids copying all variables to one worker, but
    does require that all workers see a common filesystem.

    This function differs slightly from the Keras Model `save_weights` function.
    `tf.keras.Model.save_weights` creates a checkpoint file with the name
    specified in `filepath`, while `tf.train.Checkpoint` numbers the checkpoints,
    using `filepath` as the prefix for the checkpoint file names. Aside from this,
    `model.save_weights()` and `tf.train.Checkpoint(model).save()` are equivalent.

    See the [guide to training
    checkpoints](https://www.tensorflow.org/guide/checkpoint) for
    details.

    Attributes:
      save_counter: Incremented when `save()` is called. Used to number
        checkpoints.
    """
    def __init__(self, root: Trackable | None = None, **kwargs: Trackable) -> None:
        """
        Creates a training checkpoint for a single or group of objects.

        Args:
          root: The root object to checkpoint. `root` may be a trackable object or
            `WeakRef` of a trackable object.
          **kwargs: Keyword arguments are set as attributes of this object, and are
            saved with the checkpoint. All `kwargs` must be trackable objects, or a
            nested structure of trackable objects (`list`, `dict`, or `tuple`).

        Raises:
          ValueError: If `root` or the objects in `kwargs` are not trackable. A
            `ValueError` is also raised if the `root` object tracks different
            objects from the ones listed in attributes in kwargs (e.g.
            `root.child = A` and `tf.train.Checkpoint(root, child=B)` are
            incompatible).
        """
        ...
    def read(self, save_path: str, options: CheckpointOptions | None = None) -> _CheckpointLoadStatus:
        """
        Reads a training checkpoint written with `write`.

        Reads this `Checkpoint` and any objects it depends on.

        This method is just like `restore()` but does not expect the `save_counter`
        variable in the checkpoint. It only restores the objects that the checkpoint
        already depends on.

        The method is primarily intended for use by higher level checkpoint
        management utilities that use `write()` instead of `save()` and have their
        own mechanisms to number and track checkpoints.

        Example usage:

        ```python
        # Create a checkpoint with write()
        ckpt = tf.train.Checkpoint(v=tf.Variable(1.))
        path = ckpt.write('/tmp/my_checkpoint')

        # Later, load the checkpoint with read()
        # With restore() assert_consumed() would have failed.
        checkpoint.read(path).assert_consumed()

        # You can also pass options to read(). For example this
        # runs the IO ops on the localhost:
        options = tf.train.CheckpointOptions(
            experimental_io_device="/job:localhost")
        checkpoint.read(path, options=options)
        ```

        Args:
          save_path: The path to the checkpoint as returned by `write`.
          options: Optional `tf.train.CheckpointOptions` object.

        Returns:
          A load status object, which can be used to make assertions about the
          status of a checkpoint restoration.  See `restore` for details.
        """
        ...
    def restore(self, save_path: str, options: CheckpointOptions | None = None) -> _CheckpointLoadStatus:
        """
        Restores a training checkpoint.

        Restores this `Checkpoint` and any objects it depends on.

        This method is intended to be used to load checkpoints created by `save()`.
        For checkpoints created by `write()` use the `read()` method which does not
        expect the `save_counter` variable added by `save()`.

        `restore()` either assigns values immediately if variables to restore have
        been created already, or defers restoration until the variables are
        created. Dependencies added after this call will be matched if they have a
        corresponding object in the checkpoint (the restore request will queue in
        any trackable object waiting for the expected dependency to be added).

        ```python
        checkpoint = tf.train.Checkpoint( ... )
        checkpoint.restore(path)

        # You can additionally pass options to restore():
        options = tf.CheckpointOptions(experimental_io_device="/job:localhost")
        checkpoint.restore(path, options=options)
        ```

        To ensure that loading is complete and no more deferred restorations will
        take place, use the `assert_consumed()` method of the status object returned
        by `restore()`:

        ```python
        checkpoint.restore(path, options=options).assert_consumed()
        ```

        The assert will raise an error if any Python objects in the dependency graph
        were not found in the checkpoint, or if any checkpointed values do not have
        a matching Python object.

        Name-based `tf.compat.v1.train.Saver` checkpoints from TensorFlow 1.x can be
        loaded using this method. Names are used to match variables. Re-encode
        name-based checkpoints using `tf.train.Checkpoint.save` as soon as possible.

        **Loading from SavedModel checkpoints**

        To load values from a SavedModel, just pass the SavedModel directory
        to checkpoint.restore:

        ```python
        model = tf.keras.Model(...)
        tf.saved_model.save(model, path)  # or model.save(path, save_format='tf')

        checkpoint = tf.train.Checkpoint(model)
        checkpoint.restore(path).expect_partial()
        ```

        This example calls `expect_partial()` on the loaded status, since
        SavedModels saved from Keras often generates extra keys in the checkpoint.
        Otherwise, the program prints a lot of warnings about unused keys at exit
        time.

        Args:
          save_path: The path to the checkpoint, as returned by `save` or
            `tf.train.latest_checkpoint`. If the checkpoint was written by the
            name-based `tf.compat.v1.train.Saver`, names are used to match
            variables. This path may also be a SavedModel directory.
          options: Optional `tf.train.CheckpointOptions` object.

        Returns:
          A load status object, which can be used to make assertions about the
          status of a checkpoint restoration.

          The returned status object has the following methods:

          * `assert_consumed()`:
              Raises an exception if any variables are unmatched: either
              checkpointed values which don't have a matching Python object or
              Python objects in the dependency graph with no values in the
              checkpoint. This method returns the status object, and so may be
              chained with other assertions.

          * `assert_existing_objects_matched()`:
              Raises an exception if any existing Python objects in the dependency
              graph are unmatched. Unlike `assert_consumed`, this assertion will
              pass if values in the checkpoint have no corresponding Python
              objects. For example a `tf.keras.Layer` object which has not yet been
              built, and so has not created any variables, will pass this assertion
              but fail `assert_consumed`. Useful when loading part of a larger
              checkpoint into a new Python program, e.g. a training checkpoint with
              a `tf.compat.v1.train.Optimizer` was saved but only the state required
              for
              inference is being loaded. This method returns the status object, and
              so may be chained with other assertions.

          * `assert_nontrivial_match()`: Asserts that something aside from the root
              object was matched. This is a very weak assertion, but is useful for
              sanity checking in library code where objects may exist in the
              checkpoint which haven't been created in Python and some Python
              objects may not have a checkpointed value.

          * `expect_partial()`: Silence warnings about incomplete checkpoint
              restores. Warnings are otherwise printed for unused parts of the
              checkpoint file or object when the `Checkpoint` object is deleted
              (often at program shutdown).

        Raises:
          NotFoundError: if the a checkpoint or SavedModel cannot be found at
            `save_path`.
        """
        ...
    def save(self, file_prefix: str, options: CheckpointOptions | None = None) -> str:
        """
        Saves a training checkpoint and provides basic checkpoint management.

        The saved checkpoint includes variables created by this object and any
        trackable objects it depends on at the time `Checkpoint.save()` is
        called.

        `save` is a basic convenience wrapper around the `write` method,
        sequentially numbering checkpoints using `save_counter` and updating the
        metadata used by `tf.train.latest_checkpoint`. More advanced checkpoint
        management, for example garbage collection and custom numbering, may be
        provided by other utilities which also wrap `write` and `read`.
        (`tf.train.CheckpointManager` for example).

        ```
        step = tf.Variable(0, name="step")
        checkpoint = tf.train.Checkpoint(step=step)
        checkpoint.save("/tmp/ckpt")

        # Later, read the checkpoint with restore()
        checkpoint.restore("/tmp/ckpt-1")

        # You can also pass options to save() and restore(). For example this
        # runs the IO ops on the localhost:
        options = tf.train.CheckpointOptions(experimental_io_device="/job:localhost")
        checkpoint.save("/tmp/ckpt", options=options)

        # Later, read the checkpoint with restore()
        checkpoint.restore("/tmp/ckpt-1", options=options)
        ```

        Args:
          file_prefix: A prefix to use for the checkpoint filenames
            (/path/to/directory/and_a_prefix). Names are generated based on this
            prefix and `Checkpoint.save_counter`.
          options: Optional `tf.train.CheckpointOptions` object.

        Returns:
          The full path to the checkpoint.
        """
        ...
    def sync(self) -> None:
        """Wait for any outstanding save or restore operations."""
        ...
    def write(self, file_prefix: str, options: CheckpointOptions | None = None) -> str:
        """
        Writes a training checkpoint.

        The checkpoint includes variables created by this object and any
        trackable objects it depends on at the time `Checkpoint.write()` is
        called.

        `write` does not number checkpoints, increment `save_counter`, or update the
        metadata used by `tf.train.latest_checkpoint`. It is primarily intended for
        use by higher level checkpoint management utilities. `save` provides a very
        basic implementation of these features.

        Checkpoints written with `write` must be read with `read`.

        Example usage:

        ```
        step = tf.Variable(0, name="step")
        checkpoint = tf.Checkpoint(step=step)
        checkpoint.write("/tmp/ckpt")

        # Later, read the checkpoint with read()
        checkpoint.read("/tmp/ckpt")

        # You can also pass options to write() and read(). For example this
        # runs the IO ops on the localhost:
        options = tf.CheckpointOptions(experimental_io_device="/job:localhost")
        checkpoint.write("/tmp/ckpt", options=options)

        # Later, read the checkpoint with read()
        checkpoint.read("/tmp/ckpt", options=options)
        ```

        Args:
          file_prefix: A prefix to use for the checkpoint filenames
            (/path/to/directory/and_a_prefix).
          options: Optional `tf.train.CheckpointOptions` object.

        Returns:
          The full path to the checkpoint (i.e. `file_prefix`).
        """
        ...

class CheckpointManager:
    """
    Manages multiple checkpoints by keeping some and deleting unneeded ones.

    Example usage:

    ```python
    import tensorflow as tf
    checkpoint = tf.train.Checkpoint(optimizer=optimizer, model=model)
    manager = tf.train.CheckpointManager(
        checkpoint, directory="/tmp/model", max_to_keep=5)
    status = checkpoint.restore(manager.latest_checkpoint)
    while True:
      # train
      manager.save()
    ```

    `CheckpointManager` preserves its own state across instantiations (see the
    `__init__` documentation for details). Only one should be active in a
    particular directory at a time.
    """
    def __init__(
        self,
        checkpoint: Checkpoint,
        directory: str,
        max_to_keep: int,
        keep_checkpoint_every_n_hours: int | None = None,
        checkpoint_name: str = "ckpt",
        step_counter: tf.Variable | None = None,
        checkpoint_interval: int | None = None,
        init_fn: Callable[[], object] | None = None,
    ) -> None:
        """
        Configure a `CheckpointManager` for use in `directory`.

        If a `CheckpointManager` was previously used in `directory`, its
        state will be restored. This includes the list of managed checkpoints and
        the timestamp bookkeeping necessary to support
        `keep_checkpoint_every_n_hours`. The behavior of the new `CheckpointManager`
        will be the same as the previous `CheckpointManager`, including cleaning up
        existing checkpoints if appropriate.

        Checkpoints are only considered for deletion just after a new checkpoint has
        been added. At that point, `max_to_keep` checkpoints will remain in an
        "active set". Once a checkpoint is preserved by
        `keep_checkpoint_every_n_hours` it will not be deleted by this
        `CheckpointManager` or any future `CheckpointManager` instantiated in
        `directory` (regardless of the new setting of
        `keep_checkpoint_every_n_hours`). The `max_to_keep` checkpoints in the
        active set may be deleted by this `CheckpointManager` or a future
        `CheckpointManager` instantiated in `directory` (subject to its
        `max_to_keep` and `keep_checkpoint_every_n_hours` settings).

        `CheckpointManager` can be also used for initializing the model if
        there is no checkpoints for restoring in `directory`. An example usage is:

        >>> import tempfile

        >>> tmp_dir = tempfile.mkdtemp()
        >>> checkpoint = tf.train.Checkpoint()
        >>> init_path = checkpoint.save(os.path.join(tmp_dir, 'init'))

        >>> def init_fn():
        ...   # Partially restore the checkpoint from `init_path`.
        ...   checkpoint.restore(init_path)

        >>> manager = tf.train.CheckpointManager(
        ...     checkpoint,
        ...     directory=os.path.join(tmp_dir, 'ckpt'),
        ...     max_to_keep=None,
        ...     init_fn=init_fn)
        >>> # `restore_or_initialize` will call `init_fn` if there is no existing
        >>> # checkpoint in `directory`.
        >>> manager.restore_or_initialize()

        Args:
          checkpoint: The `tf.train.Checkpoint` instance to save and manage
            checkpoints for.
          directory: The path to a directory in which to write checkpoints. A
            special file named "checkpoint" is also written to this directory (in a
            human-readable text format) which contains the state of the
            `CheckpointManager`.
          max_to_keep: An integer, the number of checkpoints to keep. Unless
            preserved by `keep_checkpoint_every_n_hours`, checkpoints will be
            deleted from the active set, oldest first, until only `max_to_keep`
            checkpoints remain. If `None`, no checkpoints are deleted and everything
            stays in the active set. Note that `max_to_keep=None` will keep all
            checkpoint paths in memory and in the checkpoint state protocol buffer
            on disk.
          keep_checkpoint_every_n_hours: Upon removal from the active set, a
            checkpoint will be preserved if it has been at least
            `keep_checkpoint_every_n_hours` since the last preserved checkpoint. The
            default setting of `None` does not preserve any checkpoints in this way.
          checkpoint_name: Custom name for the checkpoint file.
          step_counter: A `tf.Variable` instance for checking the current step
            counter value, in case users want to save checkpoints every N steps.
          checkpoint_interval: An integer, indicates the minimum step interval
            between two checkpoints.
          init_fn: Callable. A function to do customized initialization if no
            checkpoints are in the directory.

        Raises:
          ValueError: If `max_to_keep` is not a positive integer.
        """
        ...
    def _sweep(self) -> None:
        """Deletes or preserves managed checkpoints."""
        ...

def latest_checkpoint(checkpoint_dir: str, latest_filename: str | None = None) -> str:
    """
    Finds the filename of latest saved checkpoint file.

    Gets the checkpoint state given the provided checkpoint_dir and looks for a
    corresponding TensorFlow 2 (preferred) or TensorFlow 1.x checkpoint path.
    The latest_filename argument is only applicable if you are saving checkpoint
    using `v1.train.Saver.save`


    See the [Training Checkpoints
    Guide](https://www.tensorflow.org/guide/checkpoint) for more details and
    examples.`

    Args:
      checkpoint_dir: Directory where the variables were saved.
      latest_filename: Optional name for the protocol buffer file that
        contains the list of most recent checkpoint filenames.
        See the corresponding argument to `v1.train.Saver.save`.

    Returns:
      The full path to the latest checkpoint or `None` if no checkpoint was found.
    """
    ...
def load_variable(ckpt_dir_or_file: str, name: str) -> np.ndarray[Any, Any]:
    """
    Returns the tensor value of the given variable in the checkpoint.

    When the variable name is unknown, you can use `tf.train.list_variables` to
    inspect all the variable names.

    Example usage:

    ```python
    import tensorflow as tf
    a = tf.Variable(1.0)
    b = tf.Variable(2.0)
    ckpt = tf.train.Checkpoint(var_list={'a': a, 'b': b})
    ckpt_path = ckpt.save('tmp-ckpt')
    var= tf.train.load_variable(
        ckpt_path, 'var_list/a/.ATTRIBUTES/VARIABLE_VALUE')
    print(var)  # 1.0
    ```

    Args:
      ckpt_dir_or_file: Directory with checkpoints file or path to checkpoint.
      name: Name of the variable to return.

    Returns:
      A numpy `ndarray` with a copy of the value of this variable.
    """
    ...
def list_variables(ckpt_dir_or_file: str) -> list[tuple[str, list[int]]]:
    """
    Lists the checkpoint keys and shapes of variables in a checkpoint.

    Checkpoint keys are paths in a checkpoint graph.

    Example usage:

    ```python
    import tensorflow as tf
    import os
    ckpt_directory = "/tmp/training_checkpoints/ckpt"
    ckpt = tf.train.Checkpoint(optimizer=optimizer, model=model)
    manager = tf.train.CheckpointManager(ckpt, ckpt_directory, max_to_keep=3)
    train_and_checkpoint(model, manager)
    tf.train.list_variables(manager.latest_checkpoint)
    ```

    Args:
      ckpt_dir_or_file: Directory with checkpoints file or path to checkpoint.

    Returns:
      List of tuples `(key, shape)`.
    """
    ...
def __getattr__(name: str): ...  # incomplete module

# typeshed - now with docstrings!

This is a fork of [typeshed](https://github.com/python/typeshed) adding
docstrings to the type stubs, allowing Python language servers like
[basedpyright](https://github.com/DetachHead/basedpyright) to provide
documentation on hover for compiled modules or modules that build their
docstrings at runtime.

## How?

A daily CI job pulls from upstream and runs
[docify](https://github.com/atoerien/docify) on the repo, adding docstrings
by dynamically importing every module. The script is run on each OS that GitHub
Actions supports (Ubuntu, macOS and Windows), and on every Python version
supported by typeshed. Where possible, third-party packages are installed on
the CI runners so that docstrings can also be added under `stubs/`.

## Issues/Contributions

For anything relating to the actual type stubs, please head
[upstream](https://github.com/python/typeshed), and for docstring-related
issues, go to [docify](https://github.com/atoerien/docify).

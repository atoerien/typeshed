#!/usr/bin/env python3

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from packaging.specifiers import Specifier
from utils import parse_metadata, subprocess_run

PYTHON_VERSIONS = ("3.13", "3.12", "3.11", "3.10", "3.9")

DOCIFY_VER = "1.1.0"
TYPING_EXTENSIONS_VER = "4.12.2"

IGNORED_PACKAGES = [
    "Jetson.GPIO",  # can't import
    "RPi.GPIO",  # only builds on RPi
    "gdb",  # internal to gdb, can't import directly
    "pyserial",  # no __name__ == "__main__" check :(
    "uWSGI",  # doesn't build from sdist properly
]
PACKAGE_PYVER_OVERRIDES = {
    "atheris": "<=3.10",  # >=3.11 is unsupported
    "cffi": "<=3.12",  # no bdist for 3.13, sdist build fails
    "corus": "<=3.12",  # depends on cgi module, removed in 3.13
    "humanfriendly": "<=3.12",  # depends on pipes module, removed in 3.13
    "ibm-db": "<=3.12",  # no bdist for 3.13, sdist build fails
    "networkx": ">=3.10",  # <=3.9 is unsupported
    "opentracing": "<=3.11",  # tornado==5.1.1 dependency doesn't build on >=3.12
    "pygit2": "<=3.12",  # no bdist for 3.13, sdist build is a pain
    "tensorflow": "<=3.12",  # 3.13 is unsupported
    "tree-sitter-languages": "<=3.12",  # bdist only, not available for 3.13 yet
    "tqdm": "<=3.12",  # tensorflow dependency
}
PACKAGE_EXTRA_EXTRAS = {
    "dateparser": ["calendars"],
    "docker": ["ssh"],
    "python-jose": ["cryptography", "pycryptodome"],
    "workalendar": ["astronomy"],
}
PACKAGE_OVERRIDE_DEPENDENCIES = {
    "tensorflow": [],
}
PACKAGE_EXTRA_DEPENDENCIES = {
    "docutils": ["recommonmark"],
    "openpyxl": ["numpy"],
    "opentracing": ["mock", "pytest-mock", "gevent", "tornado==5.1.*"],
    "python-gflags": ["six"],
}
OS_SPECIFIC_PACKAGES = {
    "JACK-Client": ["linux", "macos"],  # choco install jack fails on windows
    "atheris": ["linux"],  # building on macos/windows is a pain
    "capturer": ["linux", "macos"],  # requires unix-only stdlib modules
    "dateparser": ["linux", "macos"],  # requires unix-only fasttext module
    "ibm-db": ["linux"],  # arm is unsupported, import fails on windows
    "psycopg2": ["linux", "macos"],  # building on windows is a pain
    "pycurl": ["linux", "macos"],  # building on windows is a pain
    "pywin32": ["win32"],  # windows only
    "wurlitzer": ["linux", "macos"],  # unix only
}

EXTRA_APT_DEPENDENCIES = [
    "libgit2-1.7",  # pygit2
    "libcurl4-openssl-dev",  # many packages
]
IGNORE_APT_DEPENDENCIES: list[str] = []
EXTRA_BREW_DEPENDENCIES = [
    "jack",  # JACK-Client
    "libgit2",  # pygit2
    "mariadb",  # mysqlclient
    "postgresql@16",  # psycopg2
    "openssl",  # many packages
]
IGNORE_BREW_DEPENDENCIES = [
    "libuv",  # already installed
    "openssl",  # already installed
]
EXTRA_CHOCO_DEPENDENCIES = [
    # "jack",  # JACK-Client
    "mitkerberos",  # ldap3
]
IGNORE_CHOCO_DEPENDENCIES: list[str] = []


def make_venv_path(pyver: str) -> Path:
    return Path(f".venv_py{pyver}")


def init_venv(pyver: str) -> Path:
    venv = make_venv_path(pyver)
    subprocess_run(
        "uv",
        "venv",
        "-q",
        "--no-project",
        "--python-preference",
        "only-managed",
        "-p",
        f"python{pyver}",
        str(venv),
    )
    uv_pip_install(venv, [f"docify=={DOCIFY_VER}"])
    # uv_pip_install(venv, ["https://github.com/AThePeanut4/docify.git"])
    return venv


def uv_pip_install(venv: Path, reqs: list[str]) -> None:
    if sys.platform == "win32":
        python_path = venv / "Scripts" / "python.exe"
    else:
        python_path = venv / "bin" / "python"

    subprocess_run(
        "uv",
        "pip",
        "install",
        "-q",
        "-p",
        str(python_path),
        *reqs,
    )


def run_docify(venv: Path, input_dir: Path) -> None:
    if sys.platform == "win32":
        path = venv / "Scripts" / "docify.exe"
    else:
        path = venv / "bin" / "docify"

    subprocess_run(str(path), "-qi", str(input_dir))


def docify_stdlib(pyver: str) -> None:
    print("  stdlib:")
    venv = init_venv(pyver)
    print("    initialised venv")

    # typing-extensions is in stdlib/ but is a PyPI package
    req = f"typing-extensions=={TYPING_EXTENSIONS_VER}"
    uv_pip_install(venv, [req])
    print(f"    installed {req}")

    run_docify(venv, Path("stdlib"))
    print("    done")


def docify_package(pyver: str, path: Path) -> None:
    meta = parse_metadata(path)
    name = meta.name
    requires_python = meta.requires_python

    print(f"  {name}:")

    if name in IGNORED_PACKAGES:
        print("    ignoring")
        return

    if name in OS_SPECIFIC_PACKAGES and sys.platform not in OS_SPECIFIC_PACKAGES[name]:
        print(f"    ignoring - unavailable on {sys.platform}")
        return

    if name in PACKAGE_PYVER_OVERRIDES:
        requires_python = Specifier(PACKAGE_PYVER_OVERRIDES[name])
    if requires_python and pyver not in requires_python:
        print(f"    ignoring - requires python_version{requires_python}")
        return

    if name in PACKAGE_EXTRA_EXTRAS:
        meta.extras.extend(PACKAGE_EXTRA_EXTRAS[name])

    venv = init_venv(pyver)
    print("    initialised venv")

    extra_requirements = meta.extra_requirements
    if name in PACKAGE_OVERRIDE_DEPENDENCIES:
        extra_requirements = PACKAGE_OVERRIDE_DEPENDENCIES[name]

    reqs = [
        meta.make_requirement(include_python_version=False),
        *extra_requirements,
        *PACKAGE_EXTRA_DEPENDENCIES.get(name, []),
    ]
    try:
        uv_pip_install(venv, reqs)
    except subprocess.CalledProcessError:
        # ignore install errors
        return
    print(f"    installed {' '.join(reqs)}")

    try:
        run_docify(venv, path)
    except subprocess.CalledProcessError:
        # ignore docify errors
        return
    print("    done")


def run(pyver: str) -> None:
    print(f"Running on Python {pyver}:")
    try:
        docify_stdlib(pyver)

        for path in Path("stubs").iterdir():
            docify_package(pyver, path)
    finally:
        # remove the venv
        venv = make_venv_path(pyver)
        if venv.exists():
            shutil.rmtree(venv)
    print()


if __name__ == "__main__":
    for v in PYTHON_VERSIONS:
        run(v)

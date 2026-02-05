#!/usr/bin/env python3

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from packaging.specifiers import SpecifierSet
from utils import parse_metadata, subprocess_run

PYTHON_VERSIONS = ("3.14", "3.13", "3.12", "3.11", "3.10", "3.9")

DOCIFY_VER = "1.1.0"
TYPING_EXTENSIONS_VER = "4.15.0"

PACKAGE_IGNORE = [
    "Jetson.GPIO",  # can't import
    "RPi.GPIO",  # only builds on RPi
    "gdb",  # internal to gdb, can't import directly
    "pyserial",  # no __name__ == "__main__" check :(
    "uWSGI",  # doesn't build from sdist properly
]
PACKAGE_OVERRIDE_PLATFORMS = {
    "docker": ["linux", "win32"],  # some windows-specific stuff
    "pyinstaller": ["linux", "win32"],  # some windows-specific stuff
    "python-dateutil": ["linux", "win32"],  # some windows-specific stuff
    "vobject": ["linux", "win32"],  # some windows-specific stuff
}
PACKAGE_OVERRIDE_PYVER = {
    "atheris": ">=3.11,<=3.13",  # supports 3.11-3.13 only
    "gevent": ">=3.11",  # doesn't build on 3.10 or earlier
    "gunicorn": ">=3.11",  # gevent dependency doesn't build on 3.10 or earlier
}
PACKAGE_EXTRA_EXTRAS = {
    "dateparser": ["calendars"],
    "docker": ["ssh"],
    "geopandas": ["all"],
    "python-jose": ["cryptography", "pycryptodome"],
    "workalendar": ["astronomy"],
}
PACKAGE_OVERRIDE_DEPENDENCIES: dict[str, list[str]] = {}
PACKAGE_EXTRA_DEPENDENCIES = {
    "Authlib": [
        "pycryptodomex",
        "Django",
        "sqlalchemy",
        "Flask",
        "Werkzeug",
        "httpx",
        "requests",
        "starlette",
    ],
    "aws-xray-sdk": [
        "bottle",
        "mysql-connector-python",
        "aiohttp",
        "sqlalchemy",
        "Flask-SQLAlchemy",
        "httpx",
        "PyMySQL",
        "Django",
        "Flask",
        "pynamodb",
        "pymongo",
        "pg8000",
        "aiobotocore",
    ],
    "docutils": ["recommonmark"],
    "openpyxl": ["numpy"],
    # tornado 5.1.1 doesn't build on 3.12 or later
    "opentracing": ["mock", "pytest-mock", "gevent", "tornado==5.1.*;python_version<='3.11'"],
    # not including bottle, Flask, Flask-Login as these are only used in example packages
    # (and have stubs for some reason) and importing one starts a web server
    "pony": ["cx_Oracle", "psycopg2", "mysqlclient"],
}
NO_MULTIPROCESS_PACKAGES = [
    "gunicorn",  # eventlet dependency seems to interfere with multiprocessing
]

EXTRA_APT_DEPENDENCIES = [
    "libcurl4-openssl-dev",  # many packages
]
IGNORE_APT_DEPENDENCIES: list[str] = [
    "libomp-dev",  # hnswlib
]
EXTRA_BREW_DEPENDENCIES = [
    "openssl",  # many packages
]
IGNORE_BREW_DEPENDENCIES = [
    "libuv",  # already installed
    "openssl",  # already installed
]
EXTRA_CHOCO_DEPENDENCIES: list[str] = []
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
        "--clear",
        "-p",
        f"python{pyver}",
        str(venv),
    )
    uv_pip_install(venv, ["git+https://github.com/atoerien/docify@multiprocessing"])
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


def run_docify(venv: Path, input_dir: Path, *, workers=0) -> None:
    if sys.platform == "win32":
        path = venv / "Scripts" / "docify.exe"
    else:
        path = venv / "bin" / "docify"

    subprocess_run(str(path), "-qi", "--workers", str(workers), str(input_dir))


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
    platforms = meta.platforms

    print(f"  {name}:")

    if name in PACKAGE_IGNORE:
        print("    ignoring")
        return

    if name in PACKAGE_OVERRIDE_PLATFORMS:
        platforms = PACKAGE_OVERRIDE_PLATFORMS[name]
    if sys.platform not in platforms:
        print(f"    ignoring - requires sys.platform in {platforms}")
        return

    if name in PACKAGE_OVERRIDE_PYVER:
        requires_python = SpecifierSet(PACKAGE_OVERRIDE_PYVER[name])
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
        meta.make_requirement(),
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
        if name in NO_MULTIPROCESS_PACKAGES:
            run_docify(venv, path, workers=1)
        else:
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

#!/usr/bin/env python3

from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
from subprocess import CalledProcessError

from main import (
    EXTRA_APT_DEPENDENCIES,
    EXTRA_BREW_DEPENDENCIES,
    EXTRA_CHOCO_DEPENDENCIES,
    IGNORE_APT_DEPENDENCIES,
    IGNORE_BREW_DEPENDENCIES,
    IGNORE_CHOCO_DEPENDENCIES,
)
from utils import parse_metadata, subprocess_run


def run(cmd: list[str], *, sudo: bool = False) -> None:
    if sudo:
        cmd = ["sudo", *cmd]
    print(" ".join(cmd))
    subprocess_run(*cmd)


def main() -> None:
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "--sudo",
        action="store_true",
    )
    arg_parser.add_argument(
        "package_manager",
        metavar="PACKAGE_MANAGER",
        choices=(
            "apt",
            "brew",
            "choco",
        ),
    )

    args = arg_parser.parse_args()

    sudo = args.sudo
    pkg_manager = args.package_manager

    packages: set[str] = set()

    for path in Path("stubs").iterdir():
        meta = parse_metadata(path)
        if pkg_manager == "apt":
            packages.update(meta.apt_dependencies)
        elif pkg_manager == "brew":
            packages.update(meta.brew_dependencies)
        elif pkg_manager == "choco":
            packages.update(meta.choco_dependencies)

    if pkg_manager == "apt":
        packages.update(EXTRA_APT_DEPENDENCIES)
        packages.difference_update(IGNORE_APT_DEPENDENCIES)
    elif pkg_manager == "brew":
        packages.update(EXTRA_BREW_DEPENDENCIES)
        packages.difference_update(IGNORE_BREW_DEPENDENCIES)
    elif pkg_manager == "choco":
        packages.update(EXTRA_CHOCO_DEPENDENCIES)
        packages.difference_update(IGNORE_CHOCO_DEPENDENCIES)

    if not packages:
        return

    if pkg_manager == "apt":
        run(["apt-get", "-q", "update"], sudo=sudo)
        cmd = ["apt-get", "-q", "install", *packages]
    elif pkg_manager == "brew":
        run(["brew", "update"], sudo=sudo)
        cmd = ["brew", "install", *packages]
    elif pkg_manager == "choco":
        cmd = ["choco", "install", "--no-progress", *packages]
    else:
        return

    try:
        run(cmd, sudo=sudo)
    except CalledProcessError as e:
        # ignore choco 3010 - means reboot is required
        if pkg_manager != "choco" or e.returncode != 3010:
            raise


if __name__ == "__main__":
    main()

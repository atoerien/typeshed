from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

import tomllib
from packaging.specifiers import SpecifierSet


def subprocess_run(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, check=True)


@dataclass
class StubMetadata:
    name: str
    version: SpecifierSet
    extras: list[str]
    platforms: list[str]
    extra_requirements: list[str]
    requires_python: SpecifierSet | None
    apt_dependencies: list[str]
    brew_dependencies: list[str]
    choco_dependencies: list[str]

    def make_requirement(self, *, include_python_version=False) -> str:
        req = self.name

        if self.extras:
            req = f"{req}[{','.join(self.extras)}]"

        req = f"{req}{self.version}"

        if include_python_version and self.requires_python:
            rp = self.requires_python
            req = f"{req}; python_version{rp}"

        return req


def parse_metadata(path: Path) -> StubMetadata:
    with (path / "METADATA.toml").open("rb") as f:
        data = tomllib.load(f)

    name = path.name

    version = data["version"]
    if version[0].isdigit():
        version = f"=={version}"
    version = SpecifierSet(version)

    tools = data.get("tool", {})
    tools_stubtest = tools.get("stubtest", {})

    extras: list[str] = tools_stubtest.get("extras", [])

    platforms = tools_stubtest.get("ci_platforms", ["linux"])

    extra_requirements = tools_stubtest.get("stubtest_requirements", [])
    apt_dependencies = tools_stubtest.get("apt_dependencies", [])
    brew_dependencies = tools_stubtest.get("brew_dependencies", [])
    choco_dependencies = tools_stubtest.get("choco_dependencies", [])

    requires_python = data.get("requires_python")
    if requires_python:
        requires_python = SpecifierSet(requires_python)

    return StubMetadata(
        name,
        version,
        extras,
        platforms,
        extra_requirements,
        requires_python,
        apt_dependencies,
        brew_dependencies,
        choco_dependencies,
    )


def get_package_requirement(path: Path) -> str:
    m = parse_metadata(path)
    return m.make_requirement()

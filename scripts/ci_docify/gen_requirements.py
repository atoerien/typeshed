#!/usr/bin/env python3

from pathlib import Path

from main import DOCIFY_VER, TYPING_EXTENSIONS_VER
from utils import get_package_requirement


def main() -> None:
    print(f"docify=={DOCIFY_VER}")
    print()
    print(f"typing-extensions=={TYPING_EXTENSIONS_VER}")
    print()
    for path in Path("stubs").iterdir():
        req = get_package_requirement(path)
        print(req)


if __name__ == "__main__":
    main()

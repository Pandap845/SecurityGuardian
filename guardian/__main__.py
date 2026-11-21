"""
This module contains the main entry point of the program.
"""

import sys
from pathlib import Path

from .dispatcher import analyze_action
from .loader import load
from .report import print_report


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    path = sys.argv[1]
    mode, lines = load(path)
    actions = [analyze_action(n, text, mode) for n, text in lines]
    print_report(Path(path).name, mode, actions)


if __name__ == "__main__":
    main()

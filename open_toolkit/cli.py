"""
open-toolkit — a single CLI bundling four independent utilities.

Usage:
    toolkit diagram <path>
    toolkit sign apply <pdf> --x 100 --y 100 --text "Jane Doe"
    toolkit fizzbuzz [start] [end]
    toolkit doc2md <file-or-url>

Run `toolkit <command> --help` for details on any command.
"""
from __future__ import annotations

import argparse
import sys

from open_toolkit import __version__
from open_toolkit.commands import diagram, doc2md, fizzbuzz, sign


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="open-toolkit: diagram, sign, fizzbuzz, and doc2md in one CLI.",
    )
    parser.add_argument("-v", "--version", action="version", version=f"open-toolkit {__version__}")

    subparsers = parser.add_subparsers(dest="command", required=True)
    diagram.add_subparser(subparsers)
    sign.add_subparser(subparsers)
    fizzbuzz.add_subparser(subparsers)
    doc2md.add_subparser(subparsers)
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

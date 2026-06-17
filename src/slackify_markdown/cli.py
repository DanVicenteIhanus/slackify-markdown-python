from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence, TextIO

from .service import slackify_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="slackify-markdown",
        description="Convert Markdown to Slack mrkdwn.",
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        help="Markdown file to convert. Reads stdin when omitted or set to '-'.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write output to this file instead of stdout.",
    )
    return parser


def read_markdown(input_path: Path | None, stdin: TextIO) -> str:
    if input_path is None or str(input_path) == "-":
        return stdin.read()

    try:
        return input_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"cannot read {input_path}: {exc}") from exc


def write_output(slack_text: str, output_path: Path | None, stdout: TextIO) -> None:
    if output_path is None:
        stdout.write(slack_text)
        if slack_text and not slack_text.endswith("\n"):
            stdout.write("\n")
        return

    try:
        output_path.write_text(slack_text, encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"cannot write {output_path}: {exc}") from exc


def run(
    argv: Sequence[str] | None = None,
    *,
    stdin: TextIO = sys.stdin,
    stdout: TextIO = sys.stdout,
    stderr: TextIO = sys.stderr,
) -> int:
    args = build_parser().parse_args(argv)

    try:
        markdown = read_markdown(args.input, stdin)
        write_output(slackify_markdown(markdown), args.output, stdout)
    except RuntimeError as exc:
        print(f"slackify-markdown: {exc}", file=stderr)
        return 1

    return 0


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()

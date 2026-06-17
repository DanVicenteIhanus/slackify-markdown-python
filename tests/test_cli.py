from io import StringIO
from pathlib import Path

import pytest

from slackify_markdown.cli import run


def test_cli_reads_stdin() -> None:
    stdout = StringIO()

    exit_code = run([], stdin=StringIO("[Link](https://example.com)"), stdout=stdout)

    assert exit_code == 0
    assert stdout.getvalue() == "<https://example.com|Link>\n"


def test_cli_reads_and_writes_files(tmp_path: Path) -> None:
    input_path = tmp_path / "input.md"
    output_path = tmp_path / "output.txt"
    input_path.write_text("*italic*", encoding="utf-8")

    exit_code = run([str(input_path), "--output", str(output_path)])

    assert exit_code == 0
    assert output_path.read_text(encoding="utf-8") == "_italic_\n"


def test_cli_reports_missing_input() -> None:
    stderr = StringIO()

    exit_code = run(["missing.md"], stderr=stderr)

    assert exit_code == 1
    assert "cannot read missing.md" in stderr.getvalue()

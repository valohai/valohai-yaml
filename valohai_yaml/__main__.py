import argparse
import sys
from typing import List, Optional

from valohai_yaml.lint import LintResult, lint


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--strict-warnings",
        action="store_true",
        help="exit with error if there are warnings",
    )
    ap.add_argument(
        "--colors",
        action="store_true",
        dest="ansi_colors",
        help="enable ANSI colors",
        default=None,
    )
    ap.add_argument(
        "--no-colors",
        action="store_false",
        dest="ansi_colors",
        help="disable ANSI colors",
        default=None,
    )
    ap.add_argument("file", nargs="+", help="file(s) to validate")
    args = ap.parse_args(argv)

    if args.ansi_colors is None:
        try:
            default_ansi_colors = sys.stdout.isatty()
        except Exception:
            default_ansi_colors = False
        args.ansi_colors = default_ansi_colors

    errors = warnings = 0
    for file in args.file:
        result = process_file(file, ansi_colors=args.ansi_colors)
        errors += result.error_count
        warnings += result.warning_count

    if errors or warnings:
        print(f"*** {errors} errors, {warnings} warnings")

    return 1 if errors or (args.strict_warnings and warnings) else 0


def process_file(file: str, ansi_colors: bool = True) -> LintResult:
    header_printed = False

    with open(file, "rb") as stream:
        result = lint(stream, ansi_colors=ansi_colors)

    for item in result.messages:
        if not header_printed:
            print(">>>", file)
            header_printed = True
        print(f"{item['type']}: {item['message']}")
        print("-" * 60)
    return result


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

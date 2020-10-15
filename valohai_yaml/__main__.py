import argparse
import sys
from typing import List, Optional

from valohai_yaml.lint import lint, LintResult


def main(args: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        '--strict-warnings',
        action='store_true',
        help='exit with error if there are warnings',
    )
    ap.add_argument('file', nargs='+', help='file(s) to validate')
    args = ap.parse_args(args)
    errors = warnings = 0
    for file in args.file:
        result = process_file(file)
        errors += result.error_count
        warnings += result.warning_count

    if errors or warnings:
        print('*** {} errors, {} warnings'.format(errors, warnings))

    return 1 if errors or (args.strict_warnings and warnings) else 0


def process_file(file: str) -> LintResult:
    header_printed = False

    with open(file, 'rb') as stream:
        result = lint(stream)

    for item in result.messages:
        if not header_printed:
            print('>>>', file)
            header_printed = True
        print('{}: {}'.format(item['type'], item['message']))
        print('-' * 60)
    return result


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

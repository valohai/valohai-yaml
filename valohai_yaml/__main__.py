import argparse
import sys
from typing import List, Optional

from valohai_yaml.lint import lint


def main(args: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('file', nargs='+', help='file(s) to validate')
    args = ap.parse_args(args)
    errors = 0
    for file in args.file:
        errors += process_file(file)
    return (1 if errors > 0 else 0)


def process_file(file: str) -> int:
    header_printed = False

    with open(file, 'rb') as stream:
        result = lint(stream)
        for item in result.messages:
            if not header_printed:
                print('>>>', file)
                header_printed = True
            print(item['message'])
            print('-' * 60)
        return result.error_count


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

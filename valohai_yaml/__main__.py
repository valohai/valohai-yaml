from __future__ import print_function, unicode_literals

import argparse
import sys

from valohai_yaml.lint import lint


def main(args=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('file', nargs='+', help='file(s) to validate')
    args = ap.parse_args(args)
    errors = 0
    for file in args.file:
        errors += process_file(file)
    return (1 if errors > 0 else 0)


def process_file(file):
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
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

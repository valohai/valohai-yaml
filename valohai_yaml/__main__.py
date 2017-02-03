from __future__ import print_function, unicode_literals

import argparse
import sys
from collections import defaultdict

from .validation import validate


def main(args=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('file', nargs='+', help='file(s) to validate')
    args = ap.parse_args(args)
    errors_by_file = defaultdict(list)
    for file in args.file:
        for error in process_file(file):
            errors_by_file[file].append(error)
    return (1 if errors_by_file else 0)


def process_file(file):
    header_printed = False
    with open(file, 'rb') as stream:
        for error in validate(stream, raise_exc=False):
            if not header_printed:
                print('>>>', file)
                header_printed = True
            print(error)
            print('-' * 60)
            yield error


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

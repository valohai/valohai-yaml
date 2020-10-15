from itertools import chain

import pytest

from tests.utils import get_warning_example_path
from valohai_yaml.lint import lint_file


# Parameters of 'flag' type do not logically support 'optional' property so we warn about it.
def test_optional_flag():
    items = lint_file('./examples/flag-optional-example.yaml')
    warning = 'Step test, parameter case-insensitive: `optional` has no effect on flag-type parameters'
    assert any((warning in item['message']) for item in items.warnings)  # pragma: no branch


@pytest.mark.parametrize('file, expected_message', [
    ('invalid-string-parameter-default.yaml', 'is not a string'),
    ('invalid-numeric-parameter-default.yaml', 'is not an integer'),
    ('invalid-numeric-range-parameter-default.yaml', 'greater than the maximum allowed'),
])
def test_invalid_parameter_default(file, expected_message):
    items = lint_file(get_warning_example_path(file))
    messages = [item['message'] for item in chain(items.warnings, items.errors)]
    assert any(expected_message in message for message in messages), messages  # pragma: no branch

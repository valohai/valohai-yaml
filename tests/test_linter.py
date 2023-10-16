from itertools import chain

import pytest

from tests.utils import (
    get_error_example_path,
    get_valid_example_path,
    get_warning_example_path,
)
from valohai_yaml.lint import lint_file


# Parameters of 'flag' type do not logically support 'optional' property so we warn about it.
def test_optional_flag():
    items = lint_file("./examples/flag-optional-example.yaml")
    warning = "Step test, parameter case-insensitive: `optional` has no effect on flag-type parameters"
    assert any(
        (warning in item["message"]) for item in items.warnings
    )  # pragma: no branch


@pytest.mark.parametrize(
    "file, expected_message",
    [
        ("invalid-string-parameter-default.yaml", "is not a string"),
        ("invalid-numeric-parameter-default.yaml", "is not an integer"),
        (
            "invalid-numeric-range-parameter-default.yaml",
            "greater than the maximum allowed",
        ),
    ],
)
def test_invalid_parameter_default(file, expected_message):
    items = lint_file(get_warning_example_path(file))
    messages = [item["message"] for item in chain(items.warnings, items.errors)]
    assert any(
        expected_message in message for message in messages
    ), messages  # pragma: no branch


@pytest.mark.parametrize(
    "file, expected_message",
    [
        (
            "invalid-indentation-with-valid-YAML.yaml",
            "\x1b[34mFile contains valid YAML but there "
            "might be an indentation error in following "
            "configuration: \x1b[1m0.step\x1b",
        ),
        ("invalid-YAML-indentation.yaml", "Indentation Error at line 3, column 10"),
    ],
)
def test_invalid_indentation(file, expected_message):
    items = lint_file(get_error_example_path(file))
    messages = [item["message"] for item in chain(items.hints, items.errors)]
    assert any(
        expected_message in message for message in messages
    ), messages  # pragma: no branch


@pytest.mark.parametrize(
    "file_path",
    [
        "step-stop-condition.yaml",
        "task-stop-condition.yaml",
    ],
)
def test_expression_lint_ok(file_path):
    items = lint_file(get_valid_example_path(file_path))
    assert items.is_valid(), [
        item["message"] for item in chain(items.hints, items.errors)
    ]


@pytest.mark.parametrize(
    "file_path, expected_message",
    [
        (
            "step-stop-condition.yaml",
            "Step no-stop, `stop-condition` is not a valid expression:",
        ),
        (
            "task-stop-condition.yaml",
            "Task no-stop, `stop-condition` is not a valid expression:",
        ),
    ],
)
def test_expression_lint_fail(file_path, expected_message):
    items = lint_file(get_error_example_path(file_path))
    messages = [item["message"] for item in chain(items.hints, items.errors)]
    assert any(expected_message in message for message in messages), messages

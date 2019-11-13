from valohai_yaml.lint import lint, lint_file


# Parameters of 'flag' type do not logically support 'optional' property so we warn about it.
def test_optional_flag():
    items = lint_file('./examples/flag-optional-example.yaml')
    warning = 'Step test, parameter case-insensitive: `optional` has no effect on flag-type parameters'
    assert any((warning in item['message']) for item in items.warnings)  # pragma: no branch

from valohai_yaml import parse


def test_unknown_parse():
    cfg = parse("[{ city_name: Constantinople }]")
    lint_result = cfg.lint()
    assert lint_result.warning_count == 1
    assert next(iter(lint_result.warnings))["message"] == "No parser for {'city_name': 'Constantinople'}"

import pytest
from valohai_yaml import parse


def test_unknown_parse():
    with pytest.raises(ValueError) as e:
        fail_config = '[{ city_name: Constantinople }]'
        parse(fail_config)
    assert e.value.args[0] == "No parser for {'city_name': 'Constantinople'}"

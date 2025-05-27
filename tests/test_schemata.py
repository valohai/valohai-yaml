import pytest

from valohai_yaml.schema_data import SCHEMATA


def assert_no_underscores(schema: dict) -> None:
    for key, value in schema.items():
        if isinstance(value, dict):
            assert_no_underscores(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    assert_no_underscores(item)
        assert "_" not in key, f"Schema key '{key}' contains an underscore."


@pytest.mark.parametrize("schema_name", SCHEMATA.keys())
def test_schemata_has_no_underscores(schema_name):
    assert_no_underscores(SCHEMATA[schema_name])

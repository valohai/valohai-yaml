from valohai_yaml.utils import listify


def test_listify():
    assert listify(None) == []
    assert listify([]) == []
    assert listify(()) == []
    assert listify(6) == [6]
    assert listify("foo") == ["foo"]

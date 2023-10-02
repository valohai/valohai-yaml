import pytest

from valohai_yaml.excs import ValidationError
from valohai_yaml.objs import Edge


def test_edge_dots():
    with pytest.raises(ValidationError):
        Edge(source="foo.bar", target="baz.quux")
    e = Edge(source="foo.bar.baz", target="baz.quux.peasoup")
    with pytest.raises(ValidationError):
        e.source = "8"

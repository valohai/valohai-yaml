import json

from valohai_yaml.objs import Parameter
from valohai_yaml.objs.parameter_widget import ParameterWidget


def test_simple_widget_roundtrip():
    param = Parameter(
        name="query",
        type="string",
        widget=ParameterWidget(type="sql"),
    )
    as_data = param.get_data()
    as_json = json.dumps(as_data)

    re_data = json.loads(as_json)
    parsed = Parameter.parse(re_data)
    assert parsed.name == param.name
    assert parsed.type == param.type
    assert isinstance(parsed.widget, ParameterWidget)
    assert parsed.widget.type == "sql"
    assert parsed.widget.settings == {}


def test_complex_widget_roundtrip():
    param = Parameter(
        name="query",
        type="string",
        widget=ParameterWidget(type="sql", settings={"language": "sql"}),
    )
    as_data = param.get_data()
    as_json = json.dumps(as_data)

    re_data = json.loads(as_json)
    parsed = Parameter.parse(re_data)
    assert parsed.name == param.name
    assert parsed.type == param.type
    assert isinstance(parsed.widget, ParameterWidget)
    assert parsed.widget.type == "sql"
    assert parsed.widget.settings == {"language": "sql"}

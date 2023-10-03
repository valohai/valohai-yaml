import pytest

from valohai_yaml import ValidationErrors
from valohai_yaml.objs import Parameter


@pytest.mark.parametrize("case", (-5, 15))
def test_minmax(case):
    param = Parameter(name="test", type="integer", min=0, max=10)
    with pytest.raises(ValidationErrors):
        param.validate(case)
    param.validate(5)


@pytest.mark.parametrize(
    "case, message",
    [
        ("5.3", "5.3 is not an integer"),
        ("hello", "hello is not an integer"),
        (True, "True is not an integer"),
        (False, "False is not an integer"),
        (None, "No value supplied"),
        ("", "No value supplied"),
    ],
)
def test_integer(case, message):
    param = Parameter(name="test", type="integer")
    with pytest.raises(ValidationErrors) as exc_info:
        param.validate(case)
    assert list(exc_info.value) == [message]
    param.validate(5)


@pytest.mark.parametrize(
    "case, message",
    [
        ("hello", "hello is not a floating-point number"),
        (True, "True is not a floating-point number"),
        (False, "False is not a floating-point number"),
        (None, "No value supplied"),
        ("", "No value supplied"),
    ],
)
def test_float(case, message):
    param = Parameter(name="test", type="float")
    with pytest.raises(ValidationErrors) as exc_info:
        param.validate(case)
    assert list(exc_info.value) == [message]
    param.validate(1.5)


@pytest.mark.parametrize("case", ("blop",))
def test_choice(case):
    param = Parameter(name="test", choices={"blep", "mlem"})
    with pytest.raises(ValidationErrors):
        param.validate(case)
    param.validate("blep")

import pytest

from valohai_yaml import ValidationErrors
from valohai_yaml.objs import Parameter


@pytest.mark.parametrize('case', (-5, 15))
def test_minmax(case):
    param = Parameter(name='test', type='integer', min=0, max=10)
    with pytest.raises(ValidationErrors):
        param.validate(case)
    param.validate(5)


@pytest.mark.parametrize('case', ('5.3', 'hello'))
def test_integer(case):
    param = Parameter(name='test', type='integer')
    with pytest.raises(ValidationErrors):
        param.validate(case)
    param.validate(5)


@pytest.mark.parametrize('case', ('hello',))
def test_float(case):
    param = Parameter(name='test', type='float')
    with pytest.raises(ValidationErrors):
        param.validate(case)
    param.validate(1.5)


@pytest.mark.parametrize('case', ('blop',))
def test_choice(case):
    param = Parameter(name='test', choices={'blep', 'mlem'})
    with pytest.raises(ValidationErrors):
        param.validate(case)
    param.validate('blep')

from __future__ import unicode_literals
import glob
import os

import pytest
from jsonschema.exceptions import ValidationError

from valohai_yaml.__main__ import main
from valohai_yaml.validate import validate

examples_path = os.path.realpath(
    os.path.join(os.path.dirname(__file__), '..', 'examples')
)

valid_bytes = b'''
- step:
    name: foo
    command: foo
    image: foo
'''

invalid_obj = [
    {
        'step': {
            'nerm': 'blerp',
        }
    },
]

valid_obj = [
    {
        'step': {
            'name': 'foo',
            'command': 'foo',
            'image': 'foo',
        }
    },
]


@pytest.mark.parametrize('path', glob.glob(os.path.join(examples_path, '*.yaml')))
def test_valid_file_cli(path):
    "Test that known-good files validate via the CLI."
    assert main([path]) == 0


def test_bytes_validation():
    "Test that you can pass in bytestring YAML and validate it."
    assert not validate(valid_bytes)


def test_popo_validation():
    "Test that you can pass in pre-parsed data and validate it."
    # (POPO: Plain Old Python Object.)
    assert not validate(valid_obj)


def test_raise():
    with pytest.raises(ValidationError):
        validate(invalid_obj, raise_exc=True)


def test_error_list():
    err = validate(invalid_obj)[0]
    assert 'required property' in (u'%s' % err)

from __future__ import unicode_literals

import glob
import os

import pytest

from tests.consts import bad_example_path
from valohai_yaml import validate, ValidationErrors
from valohai_yaml.__main__ import main

from .consts import examples_path, invalid_obj, valid_bytes, valid_obj

@pytest.mark.parametrize('path', glob.glob(os.path.join(examples_path, '*.yaml')))
def test_valid_file_cli(path):
    "Test that known-good files validate via the CLI."
    assert main([path]) == 0


def test_invalid_file_cli(capsys):
    assert main([bad_example_path]) == 1
    out, err = capsys.readouterr()
    assert "invalid.yaml" in out
    assert "'command' is a required property" in out
    assert "'name' is a required property" in out
    assert "8 is not valid under any of the given schemas" in out


def test_bytes_validation():
    "Test that you can pass in bytestring YAML and validate it."
    assert not validate(valid_bytes)


def test_popo_validation():
    "Test that you can pass in pre-parsed data and validate it."
    # (POPO: Plain Old Python Object.)
    assert not validate(valid_obj)


def test_raise():
    with pytest.raises(ValidationErrors) as ei:
        validate(invalid_obj, raise_exc=True)
    assert list(ei.value)  # test iteration over errors


def test_error_list():
    errs = [u'%s' % err for err in validate(invalid_obj, raise_exc=False)]
    assert any(('Additional properties are not allowed' in err) for err in errs)  # pragma: no branch
    assert any(('required property' in err) for err in errs)  # pragma: no branch

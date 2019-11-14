

import glob
import os

import pytest

from tests.consts import bad_examples_path, examples_path, invalid_obj, valid_bytes, valid_obj
from tests.utils import get_bad_example_path
from valohai_yaml import validate, ValidationErrors
from valohai_yaml.__main__ import main


@pytest.mark.parametrize('good_example_path', glob.glob(os.path.join(examples_path, '*.yaml')))
def test_good_examples_cli(good_example_path):
    "Test that known-good files validate via the CLI."
    assert main([good_example_path]) == 0


@pytest.mark.parametrize('bad_example_path', glob.glob(os.path.join(bad_examples_path, '*.yaml')))
def test_bad_examples_cli(capsys, bad_example_path):
    "Test that bad examples don't validate via the CLI."
    assert main([bad_example_path]) == 1
    out, err = capsys.readouterr()
    assert out


def test_invalid_file_missing_properties_cli(capsys):
    assert main([get_bad_example_path('step-missing-required-properties.yaml')]) == 1
    out, err = capsys.readouterr()
    assert "step-missing-required-properties.yaml" in out
    assert "'command' is a required property" in out
    assert "'name' is a required property" in out
    assert "8 is not valid under any of the given schemas" in out


def test_invalid_file_too_long_input_name_cli(capsys):
    assert main([get_bad_example_path('input-name-too-long.yaml')]) == 1
    out, err = capsys.readouterr()
    assert "input-name-too-long.yaml" in out
    assert "'this-input-name-is-way-too-long-and-will-cause-the-validation-to-fail' is too long" in out


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
    errs = ['%s' % err for err in validate(invalid_obj, raise_exc=False)]
    assert any(('Additional properties are not allowed' in err) for err in errs)  # pragma: no branch
    assert any(('required property' in err) for err in errs)  # pragma: no branch

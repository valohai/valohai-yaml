import glob
import os

import pytest

from tests.consts import (
    error_examples_path,
    examples_path,
    invalid_obj,
    valid_bytes,
    valid_obj,
    warning_examples_path,
)
from tests.utils import get_error_example_path, get_valid_example_path
from valohai_yaml import ValidationErrors, validate
from valohai_yaml.__main__ import main


@pytest.mark.parametrize('good_example_path', glob.glob(os.path.join(examples_path, '*.yaml')))
def test_good_examples_cli(good_example_path):
    """Test that known-good files validate via the CLI."""
    assert main([good_example_path]) == 0


@pytest.mark.parametrize('bad_example_path', glob.glob(os.path.join(error_examples_path, '*.yaml')))
def test_bad_examples_cli(capsys, bad_example_path):
    """Test that bad examples don't validate via the CLI."""
    assert main([bad_example_path]) == 1
    out, err = capsys.readouterr()
    assert out


@pytest.mark.parametrize('yaml_path', glob.glob(os.path.join(warning_examples_path, '*.yaml')))
def test_warning_examples_cli(capsys, yaml_path):
    """Test that warning examples don't validate via the CLI in strict mode."""
    assert main(['--strict-warnings', yaml_path]) == 1
    out, err = capsys.readouterr()
    assert out


def test_invalid_file_missing_properties_cli(capsys):
    assert main([get_error_example_path('step-missing-required-properties.yaml')]) == 1
    out, err = capsys.readouterr()
    assert "step-missing-required-properties.yaml" in out
    assert "'command' is a required property" in out
    assert "'name' is a required property" in out
    assert "8 is not valid under any of the given schemas" in out


def test_invalid_file_too_long_input_name_cli(capsys):
    assert main([get_error_example_path('input-name-too-long.yaml')]) == 1
    out, err = capsys.readouterr()
    assert "input-name-too-long.yaml" in out
    assert "'this-input-name-is-way-too-long-and-will-cause-the-validation-to-fail' is too long" in out


def test_invalid_on_error_value(capsys):
    assert main([get_error_example_path('invalid-on-error-value.yaml')]) == 1
    out, err = capsys.readouterr()
    assert "invalid-on-error-value.yaml" in out
    assert "is not valid under any of the given schemas" in out


def test_valid_endpoint_name_cli(capsys):
    assert main([get_valid_example_path('endpoint-names-valid.yaml')]) == 0


def test_invalid_endpoint_name_cli(capsys):
    assert main([get_error_example_path('endpoint-names-invalid.yaml')]) == 1
    out, err = capsys.readouterr()
    assert "endpoint-names-invalid.yaml" in out
    assert "'wsgi_endpoint' does not match '^[a-z][a-z0-9-]+$'" in out
    assert "'server@endpoint' does not match '^[a-z][a-z0-9-]+$'" in out
    assert "'3-server-endpoint' does not match '^[a-z][a-z0-9-]+$'" in out
    assert "'Server-endpoint' does not match '^[a-z][a-z0-9-]+$'" in out


def test_bytes_validation():
    """Test that you can pass in bytestring YAML and validate it."""
    assert not validate(valid_bytes)


def test_popo_validation():
    """Test that you can pass in pre-parsed data and validate it."""
    # (POPO: Plain Old Python Object.)
    assert not validate(valid_obj)


def test_raise():
    with pytest.raises(ValidationErrors) as ei:
        validate(invalid_obj, raise_exc=True)
    assert list(ei.value)  # test iteration over errors


def test_error_list():
    errs = [f'{err}' for err in validate(invalid_obj, raise_exc=False)]
    assert any(('Additional properties are not allowed' in err) for err in errs)  # pragma: no branch
    assert any(('required property' in err) for err in errs)  # pragma: no branch

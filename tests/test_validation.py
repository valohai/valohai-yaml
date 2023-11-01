import glob
import os
import re

import pytest

from tests.consts import (
    error_examples_path,
    examples_path,
    invalid_obj,
    valid_bytes,
    valid_examples_path,
    valid_obj,
    warning_examples_path,
)
from valohai_yaml import ValidationErrors, validate
from valohai_yaml.__main__ import main


def assert_validation_output(capsys, snapshot, yaml_path: str) -> bool:
    out, err = capsys.readouterr()
    # Replace the path with just the filename,
    # so this is agnostic to where the tests are run from.
    out = out.replace(yaml_path, os.path.basename(yaml_path))
    # Normalize Python version differences in certain error messages.
    out = re.sub(
        r"unterminated string literal \(.+?\)",
        "EOL while scanning string literal",
        out,
    )
    assert out == snapshot
    return True


@pytest.mark.parametrize(
    "good_example_path",
    glob.glob(os.path.join(examples_path, "*.yaml")),
    ids=os.path.basename,
)
def test_good_examples_cli(good_example_path):
    """Test that known-good files validate via the CLI."""
    assert main([good_example_path]) == 0


@pytest.mark.parametrize(
    "yaml_path",
    glob.glob(os.path.join(error_examples_path, "*.yaml")),
    ids=os.path.basename,
)
def test_bad_examples_cli(capsys, yaml_path, snapshot):
    """Test that bad examples don't validate via the CLI."""
    assert main([yaml_path]) == 1
    assert assert_validation_output(capsys, snapshot, yaml_path)


@pytest.mark.parametrize(
    "yaml_path",
    glob.glob(os.path.join(warning_examples_path, "*.yaml")),
    ids=os.path.basename,
)
def test_warning_examples_cli(capsys, yaml_path, snapshot):
    """Test that warning examples don't validate via the CLI in strict mode."""
    assert main(["--strict-warnings", yaml_path]) == 1
    assert assert_validation_output(capsys, snapshot, yaml_path)


@pytest.mark.parametrize(
    "valid_example_path",
    glob.glob(os.path.join(valid_examples_path, "*.yaml")),
    ids=os.path.basename,
)
def test_valid_examples_cli(valid_example_path):
    """Test that valid example files validate via the CLI."""
    assert main([valid_example_path]) == 0


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
    errs = [f"{err}" for err in validate(invalid_obj, raise_exc=False)]
    assert any(
        ("Additional properties are not allowed" in err) for err in errs
    )  # pragma: no branch
    assert any(("required property" in err) for err in errs)  # pragma: no branch
    assert any(("0 is not of type 'string'" in err) for err in errs)

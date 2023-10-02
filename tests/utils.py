import os

import pytest

from tests.consts import (
    error_examples_path,
    examples_path,
    valid_examples_path,
    warning_examples_path,
)
from valohai_yaml import parse


def _load_config(filename, roundtrip):
    with open(os.path.join(examples_path, filename)) as infp:
        config = parse(infp)
    if roundtrip:
        config = parse(config.serialize())
    return config


def config_fixture(name):
    @pytest.fixture(params=[False, True], ids=["direct", "roundtrip"])
    def _config_fixture(request):
        return _load_config(name, roundtrip=request.param)

    return _config_fixture


def get_error_example_path(filename):
    return os.path.join(error_examples_path, filename)


def get_warning_example_path(filename):
    return os.path.join(warning_examples_path, filename)


def get_valid_example_path(filename):
    return os.path.join(valid_examples_path, filename)

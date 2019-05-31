import os

import pytest

from tests.consts import examples_path, bad_examples_path
from valohai_yaml import parse


def _load_config(filename, roundtrip):
    with open(os.path.join(examples_path, filename), 'r') as infp:
        config = parse(infp)
    if roundtrip:
        config = parse(config.serialize())
    return config


def config_fixture(name):
    @pytest.fixture(params=[False, True], ids=['direct', 'roundtrip'])
    def _config_fixture(request):
        return _load_config(name, roundtrip=request.param)

    return _config_fixture


def get_bad_example_path(filename):
    return os.path.join(bad_examples_path, filename)

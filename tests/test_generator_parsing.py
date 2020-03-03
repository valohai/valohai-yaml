import glob
import json
import os
from collections import namedtuple

import pytest

from valohai_yaml.generator.parser import parse


def read_test_data():
    """
    Expected files (tests/generator_examples/parsing):
        mytest.py -- Python file calling valohai.prepare()
        mytest.inputs.json -- Expected parsed inputs
        mytest.parameters.json -- Expected parsed parameters
        mytest.step.json -- Expected parsed step

    """
    test_data = []
    for source_path in glob.glob("tests/generator_examples/parsing/*.py"):
        dirname = os.path.dirname(source_path)
        name, extension = os.path.splitext(os.path.basename(source_path))
        prefix = os.path.join(dirname, name)
        with open("%s.py" % prefix, "r") as source_python, \
            open("%s.parameters.json" % prefix, "r") as parameters_json, \
            open("%s.inputs.json" % prefix, "r") as inputs_json, \
            open("%s.step.json" % prefix, "r") as step_json:
            test_data.append((
                source_python.read(),
                json.loads(inputs_json.read()),
                json.loads(parameters_json.read()),
                json.loads(step_json.read())['name']
            ))
    return test_data


@pytest.mark.parametrize("source, inputs, parameters, step", read_test_data())
def test_parse(source, inputs, parameters, step):
    result = parse(source)

    assert result.inputs == inputs
    assert result.parameters == parameters
    assert result.step == step

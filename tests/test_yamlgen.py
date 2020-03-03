import glob
import os
import shutil

import pytest

from valohai_yaml.yamlgen.yamlgen import update_yaml_from_source, yaml_needs_update


def read_test_data():
    """
    Expected files (tests/test_yaml):
        mytest.py -- Python file calling valohai.prepare()
        mytest.original.valohai.yaml -- Original valohai.yaml
        mytest.expected.valohai.yaml -- Expected valohai.yaml after update

    """
    test_data = []
    for source_path in glob.glob("tests/yamlgen_examples/yaml/*.py"):
        dirname = os.path.dirname(source_path)
        name, extension = os.path.splitext(os.path.basename(source_path))
        test_data.append((
            "%s/%s.original.valohai.yaml" % (dirname, name),
            source_path,
            "%s/%s.expected.valohai.yaml" % (dirname, name)
        ))
    return test_data


@pytest.mark.parametrize("original_yaml, source_python, expected_yaml", read_test_data())
def test_update_yaml_from_source(local_repository_path, original_yaml, source_python, expected_yaml):
    yaml_path = os.path.join(local_repository_path, "valohai.yaml")
    source_path = os.path.join(local_repository_path, "test.py")

    # Build repository with test.py and valohai.yaml
    if os.path.isfile(original_yaml):
        shutil.copy(original_yaml, yaml_path)

    shutil.copy(source_python, source_path)

    # Update valohai.yaml based on test.py
    update_yaml_from_source(source_path, yaml_path)

    with open(expected_yaml, "r") as expected_yaml, open(yaml_path, "r") as updated_yaml:
        assert updated_yaml.read() == expected_yaml.read()


@pytest.mark.parametrize("original_yaml, source_python, expected_yaml", read_test_data())
def test_yaml_needs_update(local_repository_path, original_yaml, source_python, expected_yaml):
    yaml_path = os.path.join(local_repository_path, "valohai.yaml")
    source_path = os.path.join(local_repository_path, "test.py")

    # Build repository with test.py and valohai.yaml
    if os.path.isfile(original_yaml):
        shutil.copy(original_yaml, yaml_path)
    shutil.copy(source_python, source_path)

    if os.path.isfile(yaml_path):
        with open(expected_yaml, "r") as expected_yaml, open(yaml_path, "r") as original_yaml:
            needs_update = original_yaml.read() != expected_yaml.read()
            assert yaml_needs_update(source_path, yaml_path) == needs_update
    else:
        assert yaml_needs_update(source_path, yaml_path)

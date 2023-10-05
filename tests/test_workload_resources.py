"""
Tests WorkloadResources properties handling.

Resources are optional; missing values are None.
"""

import copy
from collections import OrderedDict

import pytest

from valohai_yaml.objs.workload_resources import (
    ResourceCPU,
    ResourceDevices,
    ResourceMemory,
    WorkloadResources,
)

RESOURCE_DATA = {
    "cpu": {"max": 10, "min": 1},
    "memory": {"max": 20, "min": 2},
    "devices": {"foo": 1, "bar": 2},
}


def test_create_resources():
    """All YAML properties are correctly parsed into the object."""
    resources = WorkloadResources.parse(OrderedDict(RESOURCE_DATA))

    assert isinstance(resources.cpu, ResourceCPU)
    assert resources.cpu.min == 1
    assert resources.cpu.max == 10

    assert isinstance(resources.memory, ResourceMemory)
    assert resources.memory.min == 2
    assert resources.memory.max == 20

    assert isinstance(resources.devices, ResourceDevices)
    assert resources.devices.get_data() == {"foo": 1, "bar": 2}


def test_missing_resources():
    """None of the workload properties are required."""
    resources = WorkloadResources.parse(OrderedDict([]))

    assert resources.cpu is None
    assert resources.memory is None
    assert resources.devices is None


@pytest.mark.parametrize(
    "resource_name,missing_key",
    [
        ("cpu", "min"),
        ("cpu", "max"),
        ("memory", "min"),
        ("memory", "max"),
    ],
)
def test_missing_sub_resources(resource_name, missing_key):
    """Missing sub resources have a value of None."""
    resources = create_resources(resource_name, missing_key)

    for this_resource_name, sub_resources in resources.get_data().items():
        for name, value in sub_resources.get_data().items():
            if this_resource_name == resource_name and name == missing_key:
                assert value is None
            else:
                assert value is not None


def create_resources(resource_name, missing_key) -> WorkloadResources:
    """Create workflow resources with one missing sub-property."""
    resource_data = copy.deepcopy(RESOURCE_DATA)
    resource_data[resource_name].pop(missing_key)

    return WorkloadResources.parse(OrderedDict(resource_data))

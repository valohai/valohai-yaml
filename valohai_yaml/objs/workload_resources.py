from collections import OrderedDict

from valohai_yaml.objs.base import Item
from valohai_yaml.types import SerializedDict


class ResourceCPU(Item):
    """CPU configuration."""

    # TODO after removing support for Python 3.8 set cpu_resource type: OrderedDict[str, int]
    def __init__(self, cpu_resource) -> None:  # noqa: ANN001
        self.max: int | None = cpu_resource.get("max")
        self.min: int | None = cpu_resource.get("min")

    def __repr__(self) -> str:
        """CPU data."""
        return f'ResourceCPU("max": {self.max}, "min": {self.min})'


class ResourceMemory(Item):
    """Memory configuration."""

    def __init__(self, memory_resource: dict) -> None:
        self.max: int | None = memory_resource.get("max")
        self.min: int | None = memory_resource.get("min")

    def __repr__(self) -> str:
        """Memory data."""
        return f'ResourceMemory("max": {self.max}, "min": {self.min})'


class ResourceDevices(Item):
    """Devices configuration."""

    def __init__(self, devices: dict) -> None:
        """
        Devices list device name: nr of devices.

        Keys (and number of items) unknown, e.g.:
        'nvidia.com/cpu': 2, 'nvidia.com/gpu': 1.
        """
        self.devices: dict[str, int] = devices

    def __repr__(self) -> str:
        """List the devices."""
        return f"ResourceDevices({self.devices})"

    def get_data(self) -> SerializedDict:
        return self.devices


class WorkloadResources(Item):
    """
    Represents a workload resource definition.

    Resources include: cpu, memory, devices.
    Both the resources and their properties are optional.
    """

    def __init__(
        self,
        *args: OrderedDict,
    ) -> None:
        self.cpu: ResourceCPU | None = None
        self.memory: ResourceMemory | None = None
        self.devices: ResourceDevices | None = None
        self._parse_args(args[0])

    def __repr__(self) -> str:
        """Resources contents."""
        return f'WorkflowResources("cpu": {self.cpu}, "memory": {self.memory}, "devices": {self.devices})'

    def _parse_args(self, resources: dict) -> None:
        if not resources:
            return

        if cpu := resources.get("cpu"):
            self.cpu = ResourceCPU(cpu)
        if memory := resources.get("memory"):
            self.memory = ResourceMemory(memory)
        if devices := resources.get("devices"):
            self.devices = ResourceDevices(devices)

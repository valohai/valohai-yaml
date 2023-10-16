from typing import Dict, Optional

from valohai_yaml.objs.base import Item
from valohai_yaml.types import SerializedDict


class ResourceCPU(Item):
    """CPU configuration."""

    def __init__(
        self,
        max: Optional[int] = None,
        min: Optional[int] = None,
    ) -> None:
        self.max = max
        self.min = min

    def __repr__(self) -> str:
        """CPU data."""
        return f'ResourceCPU("max": {self.max}, "min": {self.min})'


class ResourceMemory(Item):
    """Memory configuration."""

    def __init__(
        self,
        max: Optional[int] = None,
        min: Optional[int] = None,
    ) -> None:
        self.max = max
        self.min = min

    def __repr__(self) -> str:
        """Memory data."""
        return f'ResourceMemory("max": {self.max}, "min": {self.min})'


class ResourceDevices(Item):
    """Devices configuration."""

    def __init__(self, devices: SerializedDict) -> None:
        """
        Devices list device name: nr of devices.

        Keys (and number of items) unknown, e.g.:
        'nvidia.com/cpu': 2, 'nvidia.com/gpu': 1.
        """
        self.devices: Dict[str, int] = devices

    @classmethod
    def parse(cls, data: SerializedDict) -> "ResourceDevices":
        """
        Initialize a devices resource.

        Properties are not known beforehand, so are added as-is.
        This is a convenience method added for usage uniformity.
        """
        return ResourceDevices(data)

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
        *,
        cpu: Optional[ResourceCPU],
        memory: Optional[ResourceMemory],
        devices: Optional[ResourceDevices],
    ) -> None:
        self.cpu = cpu
        self.memory = memory
        self.devices = devices

    @classmethod
    def parse(cls, data: SerializedDict) -> "WorkloadResources":
        cpu_data = data.get("cpu")
        memory_data = data.get("memory")
        device_data = data.get("devices")
        data_with_resources = dict(
            data,
            cpu=ResourceCPU.parse(cpu_data) if cpu_data else None,
            memory=ResourceMemory.parse(memory_data) if memory_data else None,
            devices=ResourceDevices.parse(device_data) if device_data else None,
        )
        return super().parse(data_with_resources)

    def __repr__(self) -> str:
        """Resources contents."""
        return f'WorkloadResources("cpu": {self.cpu}, "memory": {self.memory}, "devices": {self.devices})'

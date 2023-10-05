from typing import Optional

from valohai_yaml.objs.base import Item
from valohai_yaml.types import SerializedDict


class ResourceCPU(Item):
    """CPU configuration."""

    def __init__(
        self,
        max_value: Optional[int],
        min_value: Optional[int],
    ) -> None:
        self.max = max_value
        self.min = min_value

    def __repr__(self) -> str:
        """CPU data."""
        return f'ResourceCPU("max": {self.max}, "min": {self.min})'


class ResourceMemory(Item):
    """Memory configuration."""

    def __init__(
        self,
        max_value: Optional[int],
        min_value: Optional[int],
    ) -> None:
        self.max = max_value
        self.min = min_value

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
        data_with_resources = dict(
            data,
            cpu=cls._parse_cpu(data.get("cpu")),
            memory=cls._parse_memory(data.get("memory")),
            devices=cls._parse_devices(data.get("devices")),
        )
        return super().parse(data_with_resources)

    @classmethod
    def _parse_cpu(cls, cpu_data: Optional[dict]) -> Optional["ResourceCPU"]:
        if not cpu_data:
            return None
        return ResourceCPU(cpu_data.get("max"), cpu_data.get("min"))

    @classmethod
    def _parse_memory(cls, memory_data: Optional[dict]) -> Optional["ResourceMemory"]:
        if not memory_data:
            return None
        return ResourceMemory(memory_data.get("max"), memory_data.get("min"))

    @classmethod
    def _parse_devices(
        cls,
        devices_data: Optional[dict],
    ) -> Optional["ResourceDevices"]:
        if not devices_data:
            return None
        return ResourceDevices(devices_data)

    def __repr__(self) -> str:
        """Resources contents."""
        return f'WorkloadResources("cpu": {self.cpu}, "memory": {self.memory}, "devices": {self.devices})'

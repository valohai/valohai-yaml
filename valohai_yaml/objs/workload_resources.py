from __future__ import annotations

from valohai_yaml.objs.base import Item
from valohai_yaml.types import SerializedDict


class WorkloadResourceItem(Item):
    """
    Adds get_data_or_none method supporting distinction between an empty SerializedDict and None.

    The method allows defining an empty devices dictionary for ResourceDevices that will override default values,
    if any are defined. Other subclasses will get default behaviour.
    """

    def get_data_or_none(self) -> SerializedDict | None:
        return self.get_data() or None


class ResourceCPU(WorkloadResourceItem):
    """CPU configuration."""

    def __init__(
        self,
        max: int | None = None,
        min: int | None = None,
    ) -> None:
        self.max = max
        self.min = min

    def __repr__(self) -> str:
        """CPU data."""
        return f'ResourceCPU("max": {self.max}, "min": {self.min})'

    def get_data(self) -> SerializedDict:
        return {key: value for key, value in super().get_data().items() if value is not None}


class ResourceMemory(WorkloadResourceItem):
    """Memory configuration."""

    def __init__(
        self,
        max: int | None = None,
        min: int | None = None,
    ) -> None:
        self.max = max
        self.min = min

    def __repr__(self) -> str:
        """Memory data."""
        return f'ResourceMemory("max": {self.max}, "min": {self.min})'

    def get_data(self) -> SerializedDict:
        return {key: value for key, value in super().get_data().items() if value is not None}


class ResourceDevices(WorkloadResourceItem):
    """Devices configuration."""

    def __init__(self, devices: SerializedDict | None) -> None:
        """
        Devices list device name: nr of devices.

        Keys (and number of items) unknown, e.g.:
        'nvidia.com/cpu': 2, 'nvidia.com/gpu': 1.
        """
        self.devices: dict[str, int] | None = devices

    @classmethod
    def parse(cls, data: SerializedDict | None) -> ResourceDevices:
        """
        Initialize a devices resource.

        Properties are not known beforehand, so are added as-is.
        This is a convenience method added for usage uniformity.
        """
        return ResourceDevices(data)

    def __repr__(self) -> str:
        """List the devices."""
        return f"ResourceDevices({self.devices})"

    def get_data_or_none(self) -> SerializedDict | None:
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
        cpu: ResourceCPU,
        memory: ResourceMemory,
        devices: ResourceDevices,
    ) -> None:
        self.cpu = cpu
        self.memory = memory
        self.devices = devices

    @classmethod
    def parse(cls, data: SerializedDict) -> WorkloadResources:
        cpu_data = data.get("cpu", {})
        memory_data = data.get("memory", {})
        device_data = data.get("devices")
        data_with_resources = dict(
            data,
            cpu=ResourceCPU.parse(cpu_data),
            memory=ResourceMemory.parse(memory_data),
            devices=ResourceDevices.parse(device_data),
        )
        return super().parse(data_with_resources)

    def get_data(self) -> SerializedDict:
        data = {}
        for key, value in super().get_data().items():
            item_data = value.get_data_or_none()
            if item_data is not None:
                data[key] = item_data
        return data

    def __repr__(self) -> str:
        """Resources contents."""
        return f'WorkloadResources("cpu": {self.cpu}, "memory": {self.memory}, "devices": {self.devices})'

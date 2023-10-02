from typing import Optional, Union

from valohai_yaml.objs.base import Item
from valohai_yaml.types import MountOptions, SerializedDict


class Mount(Item):
    """Represents a mount definition within a step definition."""

    def __init__(
        self,
        *,
        source: str,
        destination: str,
        readonly: bool = False,
        type: Optional[str] = None,
        options: Optional[MountOptions] = None,
    ) -> None:
        if options is None:
            options = {}
        self.source = source
        self.destination = destination
        self.readonly = bool(readonly)
        self.type = str(type).lower() if type else None
        self.options = options

    @classmethod
    def parse(cls, data: Union[SerializedDict, str]) -> "Mount":
        if isinstance(data, str):
            source, destination = str(data).split(":", 1)
            data = {
                "source": source,
                "destination": destination,
            }
        return super().parse(data)

    def get_data(self) -> SerializedDict:
        data = super().get_data()
        if self.options:
            data["options"] = {
                str(k): v for (k, v) in self.options.items() if v is not None
            }
        else:
            data.pop("options", None)
        return data

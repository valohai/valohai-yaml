from __future__ import annotations

from typing import TYPE_CHECKING

from valohai_yaml.objs.base import Item

if TYPE_CHECKING:
    from valohai_yaml.types import MountOptions, SerializedDict


class Mount(Item):
    """Represents a mount definition within a step definition."""

    def __init__(
        self,
        *,
        source: str,
        destination: str,
        readonly: bool = False,
        type: str | None = None,
        options: MountOptions | None = None,
    ) -> None:
        if options is None:
            options = {}
        self.source = source
        self.destination = destination
        self.readonly = bool(readonly)
        self.type = str(type).lower() if type else None
        self.options = options

    @classmethod
    def parse(cls, data: SerializedDict | str) -> Mount:
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
            data["options"] = {str(k): v for (k, v) in self.options.items() if v is not None}
        else:
            data.pop("options", None)
        return data

from typing import Optional, Union

from valohai_yaml.objs.base import Item
from valohai_yaml.types import SerializedDict


class ParameterWidget(Item):
    """An UI widget for editing parameter values."""

    def __init__(
        self,
        *,
        type: str,
        settings: Optional[dict] = None,
    ) -> None:
        self.type = str(type).lower()
        self.settings = dict(settings or {})

    def serialize(self) -> Optional[Union[SerializedDict, str]]:
        if self.settings:
            return {
                "type": self.type,
                "settings": self.settings,
            }
        return self.type

    @classmethod
    def parse(cls, data: Union["ParameterWidget", dict, str]) -> "ParameterWidget":
        if isinstance(data, dict):
            return cls(
                type=data["type"],
                settings=data.get("settings"),
            )

        if isinstance(data, cls):
            return data

        return cls(type=str(data))

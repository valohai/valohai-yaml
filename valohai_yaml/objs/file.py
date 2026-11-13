from __future__ import annotations

from typing import TYPE_CHECKING

from valohai_yaml.objs.base import Item

if TYPE_CHECKING:
    from valohai_yaml.types import SerializedDict


class File(Item):
    """Represents a file within a deployment endpoint."""

    def __init__(
        self,
        *,
        name: str,
        path: str,
        description: str | None = None,
        optional: bool = False,
    ) -> None:
        self.name = name
        self.path = path
        self.description = description
        self.optional = optional

    def get_data(self) -> SerializedDict:
        data = super().get_data()
        if not self.optional:
            data.pop("optional")
        return data

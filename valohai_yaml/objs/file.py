from __future__ import annotations

from valohai_yaml.objs.base import Item


class File(Item):
    """Represents a file within a deployment endpoint."""

    def __init__(
        self,
        *,
        name: str,
        path: str,
        description: str | None = None,
    ) -> None:
        self.name = name
        self.path = path
        self.description = description

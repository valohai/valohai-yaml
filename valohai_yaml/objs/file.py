from typing import Optional

from valohai_yaml.objs.base import Item


class File(Item):
    """Represents a file within a deployment endpoint."""

    def __init__(
        self,
        *,
        name: str,
        path: str,
        description: Optional[str] = None,
    ) -> None:
        self.name = name
        self.path = path
        self.description = description

from .base import Item


class File(Item):
    """Represents a file within a deployment endpoint."""

    def __init__(
        self,
        *,
        name,
        path,
        description=None
    ) -> None:
        self.name = name
        self.path = path
        self.description = description

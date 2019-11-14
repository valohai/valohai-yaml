from .base import Item


class File(Item):

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

from .base import _SimpleObject


class File(_SimpleObject):

    def __init__(
        self,
        name,
        path,
        description=None,
    ):
        self.name = name
        self.path = path
        self.description = description

from .base import _SimpleObject


class Input(_SimpleObject):
    def __init__(
        self,
        name,
        default=None,
    ):
        self.name = name
        self.default = default

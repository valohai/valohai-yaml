from .base import _SimpleObject


class Input(_SimpleObject):
    def __init__(
        self,
        name,
        default=None,
        optional=False,
    ):
        self.name = name
        self.default = default
        self.optional = optional

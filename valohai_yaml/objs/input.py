from .base import _SimpleObject


class Input(_SimpleObject):

    def __init__(
        self,
        name,
        default=None,
        optional=False,
        description=None,
    ):
        self.name = name
        self.default = default
        self.optional = bool(optional)
        self.description = description

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
        self.default = default  # may be None, a string or a list of strings
        self.optional = bool(optional)
        self.description = description

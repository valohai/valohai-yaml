from .base import Item


class Input(Item):

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

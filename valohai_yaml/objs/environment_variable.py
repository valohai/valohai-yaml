from .base import Item


class EnvironmentVariable(Item):

    def __init__(
        self,
        name,
        default=None,
        optional=True,
        description=None,
    ):
        self.name = name
        self.default = default  # may be None or a string
        self.optional = bool(optional)
        self.description = description

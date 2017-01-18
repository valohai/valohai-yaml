from .base import _SimpleObject


class Parameter(_SimpleObject):
    def __init__(
        self,
        name, type='string', optional=False, min=None, max=None, description=None, default=None, pass_as=None
    ):
        self.name = name
        self.type = type
        self.optional = bool(optional)
        self.min = min
        self.max = max
        self.description = description
        self.default = default
        self.pass_as = pass_as

from enum import Enum

from .base import Item


class KeepDirectories(Enum):
    NONE = 'none'
    SUFFIX = 'suffix'
    FULL = 'full'

    @classmethod
    def cast(cls, value):
        if not value:
            return KeepDirectories.NONE
        if value is True:
            return KeepDirectories.FULL
        return KeepDirectories(str(value).lower())


class Input(Item):

    def __init__(
        self,
        *,
        name,
        default=None,
        optional=False,
        description=None,
        keep_directories=False,
        filename=None
    ) -> None:
        self.name = name
        self.default = default  # may be None, a string or a list of strings
        self.optional = bool(optional)
        self.description = description
        self.keep_directories = KeepDirectories.cast(keep_directories)
        self.filename = filename

    def get_data(self) -> dict:
        data = super().get_data()
        if self.keep_directories is not KeepDirectories.NONE:
            data['keep_directories'] = data['keep_directories'].value
        else:
            data.pop('keep_directories', None)
        return data

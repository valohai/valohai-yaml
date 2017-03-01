from six import string_types, text_type

from .base import _SimpleObject


class Mount(_SimpleObject):
    def __init__(
        self,
        source,
        destination,
        readonly=False,
    ):
        self.source = source
        self.destination = destination
        self.readonly = bool(readonly)

    @classmethod
    def parse(cls, data):
        if isinstance(data, string_types):
            source, destination = text_type(data).split(':', 1)
            data = {
                'source': source,
                'destination': destination,
            }
        return super(Mount, cls).parse(data)

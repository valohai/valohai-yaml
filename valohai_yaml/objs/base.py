from collections import OrderedDict

from ..objs.utils import serialize_into
from ..utils.merge import merge_simple


class Item(object):
    """
    Base class for all objects represented in a valohai.yaml file.

    Provides basic parsing and serialization.
    """
    _original_data = None  # Possible original data dict this object was parsed from

    def get_data(self) -> dict:
        """
        Get data for serialization.
        """
        data = vars(self).copy()
        data.pop('_original_data', None)
        return data

    def serialize(self) -> dict:
        out = OrderedDict()
        # Default sorting except always start with 'name'
        sorted_items = sorted(
            self.get_data().items(),
            key=lambda kv: kv[0] if kv[0] != 'name' else '\t',
        )

        for key, value in sorted_items:
            if value is None:
                continue
            key = key.replace('_', '-')
            serialize_into(out, key, value)
        return out

    @classmethod
    def parse(cls, data: dict) -> 'Item':
        inst = cls(**{
            key.replace('-', '_'): value
            for (key, value)
            in data.items()
            if not key.startswith('_')
        })
        inst._original_data = data
        return inst

    def lint(self, lint_result, context):
        pass

    def merge_with(self, other, strategy=None) -> 'Item':
        if strategy is None:
            strategy = self.default_merge
        return strategy(self, other)

    @classmethod
    def default_merge(cls, a, b):
        return merge_simple(a, b)

from collections import OrderedDict
from typing import Any, Callable, Optional, Type, TypeVar

from ..lint import LintResult
from ..objs.utils import serialize_into
from ..utils.merge import merge_simple

T = TypeVar('T', bound='Item')


class Item:
    """
    Base class for all objects represented in a valohai.yaml file.

    Provides basic parsing and serialization.
    """

    _original_data = None  # Possible original data dict this object was parsed from

    def get_data(self) -> dict:
        """Get the object's data for serialization."""
        data = vars(self).copy()
        data.pop('_original_data', None)
        return data

    def serialize(self) -> Any:  # type = Any because subclasses may override
        out = OrderedDict()  # type: OrderedDict
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
    def parse(cls: Type[T], data: dict) -> T:
        inst = cls(**{  # type: ignore
            key.replace('-', '_'): value
            for (key, value)
            in data.items()
            if not key.startswith('_')
        })
        inst._original_data = data
        return inst

    def lint(self, lint_result: LintResult, context: dict) -> None:
        pass

    def merge_with(self: T, other: T, strategy: Optional[Callable[[T, T], T]] = None) -> 'Item':
        if strategy is None:
            strategy = self.default_merge
        return strategy(self, other)

    @classmethod
    def default_merge(cls: Type[T], a: T, b: T) -> T:
        return merge_simple(a, b)

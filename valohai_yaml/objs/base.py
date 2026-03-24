from __future__ import annotations

from collections import OrderedDict
from typing import TYPE_CHECKING, Any, Callable, TypeVar

from valohai_yaml.objs.utils import serialize_into
from valohai_yaml.utils.merge import merge_simple

if TYPE_CHECKING:
    from collections.abc import Iterable

    from valohai_yaml.lint import LintResult
    from valohai_yaml.types import LintContext, SerializedDict

T = TypeVar("T", bound="Item")


class Item:
    """
    Base class for all objects represented in a valohai.yaml file.

    Provides basic parsing and serialization.
    """

    _original_data: Iterable | None = None  # Possible original data dict or list this object was parsed from

    def get_data(self) -> SerializedDict:
        """Get the object's data for serialization."""
        data = vars(self).copy()
        data.pop("_original_data", None)
        return data

    def serialize(self) -> Any:  # type = Any because subclasses may override
        out = OrderedDict()  # type: OrderedDict[str, Any]
        # Default sorting except always start with 'name'
        sorted_items = sorted(
            self.get_data().items(),
            key=lambda kv: kv[0] if kv[0] != "name" else "\t",
        )

        for key, value in sorted_items:
            if value is None:
                continue
            key = key.replace("_", "-")
            serialize_into(out, key, value)
        return out

    @classmethod
    def parse(cls: type[T], data: SerializedDict) -> T:
        inst = cls(
            **{key.replace("-", "_"): value for (key, value) in data.items() if not key.startswith("_")},
        )
        inst._original_data = data
        return inst

    def lint(self, lint_result: LintResult, context: LintContext) -> None:
        pass

    def merge_with(
        self: T,
        other: T,
        strategy: Callable[[T, T], T] | None = None,
    ) -> T:
        if strategy is None:
            strategy = self.default_merge
        return strategy(self, other)

    @classmethod
    def default_merge(cls: type[T], a: T, b: T) -> T:
        return merge_simple(a, b)

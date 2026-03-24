from __future__ import annotations

from collections import OrderedDict
from collections import OrderedDict as OrderedDictType
from enum import Enum
from typing import TYPE_CHECKING, Any, Callable, TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterable

    from valohai_yaml.objs.base import Item
    from valohai_yaml.types import SerializedDict

TItem = TypeVar("TItem", bound="Item")
T = TypeVar("T")


def consume_array_of(
    source: SerializedDict,
    key: str,
    type: type[TItem],
) -> list[TItem]:
    return [type.parse(datum) for datum in source.pop(key, ())]


def check_type_and_listify(
    source: Iterable[Any] | None,
    type: type[T],
    parse: Callable[[Any], T] | None = None,
) -> list[T]:
    """
    Check that all items in the `source` iterable are of the type `type`, return a list.

    If `parse` is given, and the item is not of the type, that function is called to parse it to one.

    """
    if source is None:
        return []
    out = []
    for item in source:
        if not isinstance(item, type):
            if not parse:
                raise TypeError(f"{item} not a {type}")
            item = parse(item)
            assert isinstance(item, type)  # Make sure `parse` was up to spec
        out.append(item)
    return out


def check_type_and_dictify(
    source: Iterable[Any] | None,
    type: type[T],
    attr: str,
) -> OrderedDictType[str, T]:
    """Check that all items in the `source` iterable are of the type `type` and map them into an OrderedDict."""
    out = OrderedDict()  # type: OrderedDict[str, T]
    if source is None:
        return out

    for item in source:
        if not isinstance(item, type):
            raise TypeError(f"{item} not a {type}")
        out[getattr(item, attr)] = item
    return out


def serialize_into(
    dest,  # type: OrderedDict[str, Any] # noqa: ANN001
    key: str,
    value: Any,
    *,
    flatten_dicts: bool = False,
    elide_empty_iterables: bool = False,
) -> None:
    if value is None:
        return

    if flatten_dicts and isinstance(value, dict):
        value = list(value.values())

    if isinstance(value, (tuple, list)):  # can't use collections.Collection :(
        if elide_empty_iterables and not value:
            return
        value = [_serialize_if_able(item) for item in value]
    else:
        value = _serialize_if_able(value)

    dest[key] = value


def _serialize_if_able(v: Any) -> Any:
    if isinstance(v, Enum):
        return v.value

    return v.serialize() if hasattr(v, "serialize") else v

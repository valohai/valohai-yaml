import typing
from collections import OrderedDict
from typing import Any, Dict, Iterable, List, Optional, Type, TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from valohai_yaml.objs.base import Item

TItem = TypeVar('TItem', bound='Item')
T = TypeVar('T')


def consume_array_of(source: Dict[str, Any], key: str, type: Type[TItem]) -> List[TItem]:
    return [type.parse(datum) for datum in source.pop(key, ())]


def check_type_and_listify(source: Optional[Iterable[Any]], type: Type[T]) -> List[T]:
    """Check that all items in the `source` iterable are of the type `type`, return a list."""
    if source is None:
        return []
    out = []
    for item in source:
        if not isinstance(item, type):
            raise TypeError("{} not a {}".format(item, type))
        out.append(item)
    return out


# TODO: use `typing.OrderedDict` as return type when only 3.7.2+ supported
def check_type_and_dictify(source: Optional[Iterable[Any]], type: Type[T], attr: str) -> typing.MutableMapping[str, T]:
    """Check that all items in the `source` iterable are of the type `type` and map them into an OrderedDict."""
    out = OrderedDict()  # type: OrderedDict[str, T]
    if source is None:
        return out

    for item in source:
        if not isinstance(item, type):
            raise TypeError("{} not a {}".format(item, type))
        out[getattr(item, attr)] = item
    return out


def serialize_into(
    dest: OrderedDict,
    key: str,
    value: Any,
    *,
    flatten_dicts: bool = False,
    elide_empty_iterables: bool = False
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
    return (v.serialize() if hasattr(v, 'serialize') else v)

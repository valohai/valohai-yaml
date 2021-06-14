from collections import OrderedDict
from typing import Any, Dict, List, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from valohai_yaml.objs.base import Item


# TODO: use TypeVar?
def consume_array_of(source: Dict[str, Any], key: str, type: Type['Item']) -> List[Any]:
    return [type.parse(datum) for datum in source.pop(key, ())]


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

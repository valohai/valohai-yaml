from typing import Any, List, Optional, Tuple, TypeVar, Union, overload

from yaml import safe_load

from valohai_yaml.types import YamlReadable


def read_yaml(yaml: YamlReadable) -> Any:
    if isinstance(yaml, (dict, list)):  # Smells already parsed
        return yaml
    if isinstance(yaml, bytes):
        yaml = yaml.decode("utf-8")
    return safe_load(yaml)  # can be a stream or a string


T = TypeVar("T")


@overload
def listify(value: None) -> List[Any]:
    ...


@overload
def listify(value: Union[List[T], Tuple[T]]) -> List[T]:
    ...


@overload
def listify(value: T) -> List[T]:
    ...


def listify(value: Optional[Union[List[T], Tuple[T], T]]) -> List[T]:
    """
    Wrap the given value into a list, with provisions outlined below.

    * If the value is a list or a tuple, it's coerced into a new list.
    * If the value is None, an empty list is returned.
    * Otherwise, a single-element list is returned, containing the value.

    :param value: A value.
    :return: a list!
    """
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]

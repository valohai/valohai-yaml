from typing import Any, IO, Union

from yaml import safe_load


def read_yaml(yaml: Union[dict, list, bytes, str, IO]) -> Any:
    if isinstance(yaml, (dict, list)):  # Smells already parsed
        return yaml
    if isinstance(yaml, bytes):
        yaml = yaml.decode('utf-8')
    return safe_load(yaml)  # can be a stream or a string


def listify(value: Any) -> list:
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

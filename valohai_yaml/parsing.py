from typing import IO, Union

from valohai_yaml.objs import Config

from .utils import read_yaml


def parse(yaml: Union[dict, list, bytes, str, IO], validate: bool = True) -> Config:
    """
    Parse the given YAML data into a `Config` object, optionally validating it first.

    :param yaml: YAML data (either a string, a stream, or pre-parsed Python dict/list)
    :type yaml: list|dict|str|file
    :param validate: Whether to validate the data before attempting to parse it.
    :type validate: bool
    :return: Config object
    :rtype: valohai_yaml.objs.Config
    """
    data = read_yaml(yaml)
    if validate:  # pragma: no branch
        from .validation import validate as do_validate
        do_validate(data, raise_exc=True)
    return Config.parse(data)

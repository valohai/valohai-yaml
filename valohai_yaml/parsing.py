from valohai_yaml.objs import Config
from valohai_yaml.types import YamlReadable
from valohai_yaml.utils import read_yaml


def parse(yaml: YamlReadable, validate: bool = True) -> Config:
    """
    Parse the given YAML data into a `Config` object, optionally validating it first.

    :param yaml: YAML data (either a string, a stream, or pre-parsed Python dict/list)
    :param validate: Whether to validate the data before attempting to parse it.
    :return: Config object
    """
    data = read_yaml(yaml)
    if data is None:  # empty file
        return Config()
    if validate:  # pragma: no branch
        from valohai_yaml.validation import validate as do_validate

        do_validate(data, raise_exc=True)
    return Config.parse(data)

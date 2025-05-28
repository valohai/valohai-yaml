from functools import cache
from typing import List

from jsonschema import Draft202012Validator, ValidationError

from valohai_yaml import schema_data
from valohai_yaml.excs import ValidationErrors
from valohai_yaml.types import YamlReadable
from valohai_yaml.utils import read_yaml


def get_json_schema() -> dict:
    schemata = schema_data.SCHEMATA.copy()
    base = schemata.pop("https://valohai.com/schemas/base")
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Valohai YAML Schema",
        "description": "Base schema for Valohai YAML files.",
        **base,
        "$defs": schemata,
    }


@cache
def get_validator() -> Draft202012Validator:
    schema = get_json_schema()
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def validate(yaml: YamlReadable, raise_exc: bool = True) -> List[ValidationError]:
    """
    Validate the given YAML document and return a list of errors.

    :param yaml: YAML data (either a string, a stream, or pre-parsed Python dict/list)
    :param raise_exc: Whether to raise a meta-exception containing all discovered errors after validation.
    :return: A list of errors encountered.
    """
    data = read_yaml(yaml)
    validator = get_validator()
    # Nb: this uses a list instead of being a generator function in order to be
    # easier to call correctly. (Were it a generator function, a plain
    # `validate(..., raise_exc=True)` would not do anything.
    errors = list(validator.iter_errors(data))
    if errors and raise_exc:
        raise ValidationErrors(errors)
    return errors

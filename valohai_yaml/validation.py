import json
import os
import re
from functools import lru_cache
from typing import IO, List, Union

import yaml
from jsonschema import Draft4Validator, RefResolver, ValidationError

from .excs import ValidationErrors
from .utils import read_yaml

SCHEMATA_DIRECTORY = os.path.join(os.path.dirname(__file__), 'schema')


class LocalRefResolver(RefResolver):
    """Loads relative URLs (as it were) from the `schema` directory."""

    local_scope_re = re.compile(r'^https?://valohai.com/(.+\.json)$')

    def resolve_from_url(self, url: str) -> dict:
        local_match = self.local_scope_re.match(url)
        if local_match:
            schema = get_schema(name=local_match.group(1))
            self.store[url] = schema
            return schema  # noqa: R504
        raise NotImplementedError('remote URL resolution is not supported for security reasons')  # pragma: no cover


@lru_cache()
def get_schema(name: str) -> dict:
    json_filename = os.path.join(SCHEMATA_DIRECTORY, name)
    yaml_filename = os.path.splitext(json_filename)[0] + '.yaml'
    for filename, loader in [
        (json_filename, json.load),
        (yaml_filename, yaml.safe_load),
    ]:
        if os.path.isfile(filename):
            with open(filename, encoding='utf-8') as infp:
                return loader(infp)  # type: ignore
    raise ValueError('unable to read schema %s' % name)  # pragma: no cover


def get_validator() -> Draft4Validator:
    schema = get_schema('base.json')
    cls = Draft4Validator
    cls.check_schema(schema)
    return cls(schema, resolver=LocalRefResolver.from_schema(schema))


def validate(yaml: Union[dict, list, bytes, str, IO], raise_exc: bool = True) -> List[ValidationError]:
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

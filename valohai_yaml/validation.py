import json
import os
import re
from functools import lru_cache
from typing import Any, Dict, List

import yaml
from jsonschema import Draft202012Validator, RefResolver, ValidationError

from valohai_yaml.excs import ValidationErrors
from valohai_yaml.types import YamlReadable
from valohai_yaml.utils import read_yaml

SCHEMATA_DIRECTORY = os.path.join(os.path.dirname(__file__), "schema")


class LocalRefResolver(RefResolver):  # type: ignore[misc]
    """Loads relative URLs (as it were) from the `schema` directory."""

    local_scope_re = re.compile(r"^https?://valohai.com/(.+\.json)$")

    def resolve_from_url(self, url: str) -> Dict[Any, Any]:
        local_match = self.local_scope_re.match(url)
        if local_match:
            schema = get_schema(name=local_match.group(1))
            self.store[url] = schema
            return schema
        raise NotImplementedError(
            "remote URL resolution is not supported for security reasons",
        )  # pragma: no cover


@lru_cache
def get_schema(name: str) -> Dict[Any, Any]:
    json_filename = os.path.join(SCHEMATA_DIRECTORY, name)
    yaml_filename = os.path.splitext(json_filename)[0] + ".yaml"
    for filename, loader in [
        (json_filename, json.load),
        (yaml_filename, yaml.safe_load),
    ]:
        if os.path.isfile(filename):
            with open(filename, encoding="utf-8") as infp:
                return loader(infp)  # type: ignore
    raise ValueError(f"unable to read schema {name}")  # pragma: no cover


def get_validator() -> Draft202012Validator:
    schema = get_schema("base.json")
    cls = Draft202012Validator
    cls.check_schema(schema)
    return cls(schema, resolver=LocalRefResolver.from_schema(schema))


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

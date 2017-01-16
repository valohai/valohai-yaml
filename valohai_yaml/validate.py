import json
import os
import re
from codecs import open  # required for Python 2, doesn't hurt for Python 3

from jsonschema import Draft4Validator, RefResolver
from jsonschema.compat import lru_cache
from yaml import safe_load

SCHEMATA_DIRECTORY = os.path.join(os.path.dirname(__file__), 'schema')


class LocalRefResolver(RefResolver):
    """
    Loads relative URLs (as it were) from the `schema` directory.
    """
    local_scope_re = re.compile('^https?://valohai.com/(.+\.json)$')

    def resolve_from_url(self, url):
        local_match = self.local_scope_re.match(url)
        if local_match:
            local_filename = os.path.join(SCHEMATA_DIRECTORY, local_match.group(1))
            with open(local_filename, 'r', encoding='utf-8') as infp:
                schema = json.load(infp)
                self.store[url] = schema
                return schema
        raise NotImplementedError('remote URL resolution is not supported for security reasons')  # pragma: no cover


@lru_cache()
def get_schema(name):
    with open(
        os.path.join(SCHEMATA_DIRECTORY, name),
        'r',
        encoding='utf-8'
    ) as infp:
        return json.load(infp)


def get_validator():
    schema = get_schema('base.json')
    cls = Draft4Validator
    cls.check_schema(schema)
    return cls(schema, resolver=LocalRefResolver.from_schema(schema))


def parse_yaml(yaml):
    if isinstance(yaml, (dict, list)):  # Smells already parsed
        return yaml
    if isinstance(yaml, bytes):
        yaml = yaml.decode('utf-8')
    return safe_load(yaml)  # can be a stream or a string


def validate(yaml, raise_exc=False):
    """
    Validate the given YAML document and return a list of errors.

    :param yaml: YAML data (either a string, a stream, or pre-parsed Python dict/list)
    :type yaml: list|dict|str|file
    :param raise_exc: Whether to raise an exception at the first discovered error.
    :type raise_exc: bool
    :return: A list of errors encountered.
    :rtype: list[jsonschema.exceptions.ValidationError]
    """
    data = parse_yaml(yaml)
    validator = get_validator()
    # Nb: this uses a list instead of being a generator function in order to be
    # easier to call correctly. (Were it a generator function, a plain
    # `validate(..., raise_exc=True)` would not do anything.
    errors = []
    for error in validator.iter_errors(data):
        if raise_exc:
            raise error
        errors.append(error)
    return errors

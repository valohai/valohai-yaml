from typing import IO, Iterator, List, Optional, Union

from jsonschema.exceptions import relevance

from valohai_yaml.excs import ValidationError
from valohai_yaml.utils import read_yaml
from valohai_yaml.utils.terminal import style
from valohai_yaml.validation import get_validator


class LintResult:
    """Container for lint results."""

    def __init__(self) -> None:
        self.messages = []  # type: List[dict]

    def add_error(self, message: str, location: None = None, exception: Optional[Exception] = None) -> None:
        self.messages.append({'type': 'error', 'message': message, 'location': location, 'exception': exception})

    def add_warning(self, message: str, location: None = None, exception: Optional[Exception] = None) -> None:
        self.messages.append({'type': 'warning', 'message': message, 'location': location, 'exception': exception})

    @property
    def warning_count(self) -> int:
        return sum(1 for m in self.messages if m['type'] == 'warning')

    @property
    def error_count(self) -> int:
        return sum(1 for m in self.messages if m['type'] == 'error')

    @property
    def warnings(self) -> Iterator[dict]:
        return (m for m in self.messages if m['type'] == 'warning')

    @property
    def errors(self) -> Iterator[dict]:
        return (m for m in self.messages if m['type'] == 'error')

    def is_valid(self) -> bool:
        return (self.warning_count == 0 and self.error_count == 0)


def lint_file(file_path: str) -> LintResult:
    """
    Validate & lint `file_path` and return a LintResult.

    :param file_path: YAML filename
    :return: LintResult object
    """
    with open(file_path) as yaml:
        try:
            return lint(yaml)
        except Exception as e:
            lr = LintResult()
            lr.add_error('could not parse YAML: %s' % e, exception=e)
            return lr


def lint(yaml: Union[dict, list, bytes, str, IO]) -> LintResult:
    lr = LintResult()

    data = read_yaml(yaml)
    validator = get_validator()
    errors = sorted(
        validator.iter_errors(data),
        key=lambda error: (relevance(error), repr(error.path)),
    )
    for error in errors:
        simplified_schema_path = [
            el
            for el
            in list(error.relative_schema_path)
            if el not in ('properties', 'items')
        ]
        obj_path = [str(el) for el in error.path]
        lr.add_error('  {validator} validation on {schema_path}: {message} ({path})'.format(
            validator=style(error.validator.title(), bold=True),
            schema_path=style('.'.join(simplified_schema_path), bold=True),
            message=style(error.message, fg='red'),
            path=style('.'.join(obj_path), bold=True),
        ))

    if len(errors) > 0:
        return lr

    try:
        from valohai_yaml.objs import Config
        config = Config.parse(data)
    except ValidationError as err:  # Could happen before we get to linting things
        lr.add_error(str(err), exception=err)
    else:
        config.lint(lr, context={})
    return lr

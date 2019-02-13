from valohai_yaml.utils import read_yaml
from valohai_yaml.utils.terminal import style
from valohai_yaml.validation import get_validator
from jsonschema.exceptions import relevance


class LintResult:
    def __init__(self):
        self.messages = []

    def add_error(self, message, location=None, exception=None):
        self.messages.append({'type': 'error', 'message': message, 'location': location, 'exception': exception})

    def add_warning(self, message, location=None, exception=None):
        self.messages.append({'type': 'warning', 'message': message, 'location': location, 'exception': exception})

    @property
    def warning_count(self):
        return sum(1 for m in self.messages if m['type'] == 'warning')

    @property
    def error_count(self):
        return sum(1 for m in self.messages if m['type'] == 'error')


def lint_file(filename):
    """
    Validate `filename` and return a LintResult.

    :param filename: YAML filename
    :type filename: str
    :return: LintResult object
    """
    lr = LintResult()
    with open(filename, 'r') as infp:
        try:
            data = read_yaml(infp)
        except Exception as e:
            lr.add_error('could not parse YAML: %s' % e, exception=e)
            return lr

    validator = get_validator()
    errors = sorted(
        validator.iter_errors(data),
        key=lambda error: (relevance(error), repr(error.path)),
    )
    for error in errors:
        simplified_schema_path = [
            el
            for el
            in list(error.relative_schema_path)[:-1]
            if el not in ('properties', 'items')
        ]
        obj_path = [str(el) for el in error.path]
        lr.add_error('  {validator} validation on {schema_path}: {message} ({path})'.format(
            validator=style(error.validator.title(), bold=True),
            schema_path=style('.'.join(simplified_schema_path), bold=True),
            message=style(error.message, fg='red'),
            path=style('.'.join(obj_path), bold=True),
        ))
    return lr

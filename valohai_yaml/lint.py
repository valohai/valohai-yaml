from valohai_yaml.objs import Config
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

    @property
    def warnings(self):
        return (m for m in self.messages if m['type'] == 'warning')

    @property
    def errors(self):
        return (m for m in self.messages if m['type'] == 'error')


def lint_file(file_path):
    """
    Validate & lint `file_path` and return a LintResult.

    :param file_path: YAML filename
    :type file_path: str
    :return: LintResult object
    """

    with open(file_path, 'r') as yaml:
        try:
            return lint(yaml)
        except Exception as e:
            lr = LintResult()
            lr.add_error('could not parse YAML: %s' % e, exception=e)
            return lr


def lint(yaml):
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

    if len(errors) > 0:
        return lr

    config = Config.parse(data)
    config.lint(lr, context={})
    return lr

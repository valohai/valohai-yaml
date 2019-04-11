from valohai_yaml._compat import text_type
from valohai_yaml.validation import ValidationErrors

from .base import Item


class Parameter(Item):

    def __init__(
        self,
        name,
        type='string',
        optional=False,
        min=None,
        max=None,
        description=None,
        default=None,
        pass_as=None,
        choices=None,
    ):
        self.name = name
        self.type = type
        self.optional = bool(optional)
        self.min = min
        self.max = max
        self.description = description
        self.default = default
        self.pass_as = pass_as
        self.choices = (list(choices) if choices else None)
        if self.type == 'flag':
            self.optional = True
            self.choices = (True, False)

    def get_data(self):
        data = super(Parameter, self).get_data()
        if self.type == 'flag':
            data.pop('optional', None)
            data.pop('choices', None)
        return data

    def _validate_value(self, value, errors):
        if self.min is not None and value < self.min:
            errors.append('%s is less than the minimum allowed (%s)' % (value, self.min))
        if self.max is not None and value > self.max:
            errors.append('%s is greater than the maximum allowed (%s)' % (value, self.max))
        if self.choices is not None and value not in self.choices:
            errors.append('%s is not among the choices allowed (%r)' % (value, self.choices))

    def _validate_type(self, value, errors):
        if self.type == 'integer':
            try:
                value = int(text_type(value), 10)
            except ValueError:
                errors.append('%s is not an integer' % value)
        elif self.type == 'float':
            try:
                value = float(text_type(value))
            except ValueError:
                errors.append('%s is not a floating-point number' % value)
        return value

    def validate(self, value):
        """
        Validate (and possibly typecast) the given parameter value value.

        :param value: Parameter value
        :return: Typecast parameter value
        :raises ValidationErrors: if there were validation errors
        """
        errors = []
        value = self._validate_type(value, errors)
        self._validate_value(value, errors)

        if errors:
            raise ValidationErrors(errors)

        return value

    @property
    def default_pass_as(self):
        if self.type == 'flag':
            return '--{name}'
        return '--{name}={value}'

    def format_cli(self, value):
        """
        Build a single parameter argument.

        :return: list of CLI strings -- not escaped. If the parameter should not be expressed, returns None.
        :rtype: list[str]|None
        """
        if value is None or (self.type == 'flag' and not value):
            return None
        pass_as_bits = text_type(self.pass_as or self.default_pass_as).split()
        env = dict(name=self.name, value=value, v=value)
        return [bit.format(**env) for bit in pass_as_bits]

    def lint(self, lint_result, context):
        if self.type == 'flag' and self._original_data.get('optional'):
            lint_result.add_warning(
                'Step {step}, parameter {param}: `optional` has no effect on flag-type parameters'.format(
                    step=context['step'].name,
                    param=self.name,
                )
            )
